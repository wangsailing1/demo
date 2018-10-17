#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import copy
import bisect
import types
import random
import time
import hashlib
import json

from models.config import Config, ConfigVersion, ConfigMd5
from models.config import FrontConfig, FrontConfigVersion, FrontConfigMd5
from gconfig.back_contents import mapping_config as back_mapping_config
from gconfig.front_contents import mapping_config as front_mapping_config
from gconfig.trans import trans_config
from lib.utils.debug import print_log
import settings
from lib.utils.singleton import Singleton
from handler_tools import to_json
from config_operation import RESOLVE_LIST, FAKE_CONFIG


class ReadonlyDict(dict):
    def __readyonly__(self, *args, **kwargs):
        raise RuntimeError('cannot modify readyonly dict')

    __setitem__ = __readyonly__
    __delitem__ = __readyonly__
    pop = __readyonly__
    popitem = __readyonly__
    clear = __readyonly__
    setdefault = __readyonly__
    del __readyonly__


class ReadonlyList(list):
    def __readyonly__(self, *args, **kwargs):
        raise RuntimeError('cannot modify readyonly list')

    __setitem__ = __readyonly__
    __delitem__ = __readyonly__
    __iadd__ = __readyonly__
    __imul__ = __readyonly__
    pop = __readyonly__
    append = __readyonly__
    insert = __readyonly__
    remove = __readyonly__
    extend = __readyonly__
    del __readyonly__


def make_readonly(x, deep=0):
    if x.__class__ is list:
        d = []
        for i in x:
            d.append(make_readonly(i, deep + 1))
        return ReadonlyList(d)
    elif x.__class__ is dict:
        d = {}
        for k, v in x.iteritems():
            d[k] = make_readonly(v, deep + 1)
        return d if deep else ReadonlyDict(d)
    return x


class GameConfigMixIn(object):
    """ 配置嵌入类
1	攻击	phy_atk
2	生命	hp
3	防御	phy_def
4	魔强	mag_atk
5	魔抗	mag_def
#6	伤害	damage
7	速度	speed
8	暴击(%)	crit_chance
9	暴击伤害(%)	crit_atk
10	效果命中(%)	hit
11	效果抵抗(%)	resistance
16	抗暴（%）	def_crit

#12	伤害加成（%）	atk_bonus
13	基因生命加成（%）	hp_bonus
14	基因攻击加成（%）	def_bonus
15	基因绝攻加成（%）	mag_def_bonus
40	基因普防提升（%）	gene_def_bonus
41	基因绝防提升（%）	gene_mag_def_bonus
24	装备普攻提升(%) equip_atk_bonus
25	装备绝攻提升(%) equip_mag_bonus
26	装备生命提升(%) equip_hp_bonus
27	英雄普攻提升(%) hero_atk_bonus
28	英雄绝攻提升（%）hero_mag_bonus
29	英雄生命提升（%）hero_hp_bonus
21	最终生命提升（%）final_hp_bonus
38  英雄普防提升(%)  hero_def_bonus
39  英雄绝防提升(%)  hero_mag_def_bonus
42  英雄普攻绝攻（装备副属性专用  hero_bothatk_bonus
43  基因普攻绝攻（装备副属性专用  gene_bothatk_bonus

19	最终普攻提升（%）final_atk_bonus
20	最终绝攻提升（%）final_mag_bonus
17	最终输出伤害率（%）final_damage
18	最终输出免疫率（%）final_damage_immune
22	最终普攻免疫提升（%）final_atk_immune_bonus
23	最终绝攻免疫提升（%）final_mag_immune_bonus
30	普攻伤害系数（%）act_damage
31	绝技伤害系数（%）mag_damage
32	受治疗效果提升（%）treated_bonus
33	初始怒气加成  initial_anger
34	怒气上限加成  limit_anger
35	怒气回复加成(概率)  rec_anger
36  小技能触发概率（百分比、加法） skill_str_point
37	怒气回复加成(回复值)  rec_anger_value

# 特殊的属性，不加在英雄身上,只单独影响战斗怒气
44	初始怒气加成  final_initial_anger

45	特性普攻提升(%)  character_atk_bonus
46	特性绝攻提升(%)  character_mag_bonus
47	特性普防提升(%)  character_def_bonus
48	特性绝防提升(%)  character_magdef_bonus

    """
    ATTR_MAPPING = {
        'phy_atk': u'普攻',
        'hp': u'生命',
        'phy_def': u'防御',
        'mag_atk': u'绝攻',
        'mag_def': u'绝防',
        # 'damage': u'伤害',
        'speed': u'速度',
        'crit_chance': u'暴击(%)',
        'crit_atk': u'暴击伤害(%)',
        'hit': u'效果命中(%)',
        'resistance': u'效果抵抗(%）',
        'def_crit': u'抗暴（%）',
        # 'atk_bonus': u'伤害加成（%）',
        'hp_bonus': u'装备生命加成（%）',
        'def_bonus': u'装备攻击加成（ % ）',
        'mag_def_bonus': u'装备绝攻加成（ % ）',
        'equip_atk_bonus': u'基因普攻提升( %)',
        'equip_mag_bonus': u'基因绝攻提升( %)',
        'equip_hp_bonus': u'基因生命提升( %)',
        'hero_atk_bonus': u'英雄普攻提升( %)',
        'hero_mag_bonus': u'英雄绝攻提升（ % ）',
        'hero_hp_bonus': u'英雄生命提升（ % ）',
        'final_hp_bonus': u'最终生命提升（ % ）',
        'final_atk_bonus': u'最终普攻提升（ % ）',
        'final_mag_bonus': u'最终绝攻提升（ % ）',
        'final_damage': u'最终输出伤害率（ % ）',
        'final_damage_immune': u'最终输出免疫率（ % ）',
        'final_atk_immune_bonus': u'最终普攻免疫提升（ % ）',
        'final_mag_immune_bonus': u'最终绝攻免疫提升（ % ）',
        'act_damage': u'普攻伤害系数（ % ）',
        'mag_damage': u'绝技伤害系数（ % ）',
        'treated_bonus': u'受治疗效果提升（ % ）',
        'initial_anger': u'初始怒气加成',
        'limit_anger': u'怒气上限加成',
        'rec_anger': u'怒气回复加成(概率)',
        'skill_str_point': u'小技能触发概率（百分比、加法）',
        'rec_anger_value': u'怒气回复加成(回复值)',
        'gene_def_bonus': u'基因普防提升（ % ）',
        'gene_mag_def_bonus': u'基因绝防提升（ % ）',
        'hero_def_bonus': u'英雄普防提升(%)',
        'hero_mag_def_bonus': u'英雄绝防提升(%)',
        'hero_bothatk_bonus': u'英雄普攻绝攻（装备副属性专用）',
        'gene_bothatk_bonus': u'基因普攻绝攻（装备副属性专用）',
        'final_initial_anger': u'最终初始怒气加成',
        'character_atk_bonus': u'特性普攻提升(%)',
        'character_mag_bonus': u'特性绝攻提升(%)',
        'character_def_bonus': u'特性普防提升(%)',
        'character_magdef_bonus': u'特性绝防提升(%)',
    }

    def __init__(self):
        self.attr_mapping = {
            1: 'phy_atk', 2: 'hp', 3: 'phy_def', 4: 'mag_atk', 5: 'mag_def', 6: 'damage',
            7: 'speed', 8: 'crit_chance', 9: 'crit_atk', 10: 'hit', 11: 'resistance',
            12: 'atk_bonus', 13: 'hp_bonus', 14: 'def_bonus', 15: 'mag_def_bonus',
            16: 'def_crit', 17: 'final_damage', 18: 'final_damage_immune', 19: 'final_atk_bonus',
            20: 'final_mag_bonus', 21: 'final_hp_bonus', 22: 'final_atk_immune_bonus', 23: 'final_mag_immune_bonus',
            24: 'equip_atk_bonus', 25: 'equip_mag_bonus', 26: 'equip_hp_bonus', 27: 'hero_atk_bonus',
            28: 'hero_mag_bonus', 29: 'hero_hp_bonus', 30: 'act_damage', 31: 'mag_damage',
            32: 'treated_bonus', 33: 'initial_anger', 34: 'limit_anger', 35: 'rec_anger',
            36: 'skill_str_point', 37: 'rec_anger_value', 38: 'hero_def_bonus', 39: 'hero_mag_def_bonus',
            40: 'gene_def_bonus', 41: 'gene_mag_def_bonus',
            42: 'hero_bothatk_bonus', 43: 'gene_bothatk_bonus',
            44: 'final_initial_anger',
            45: 'character_atk_bonus', 46: 'character_mag_bonus', 47: 'character_def_bonus',
            48: 'character_magdef_bonus',
        }
        self.no_in_hero_dict = [44]
        # self.attr_mapping = {  # 属性对应表
        #     1: 'hp', 2: 'phy_atk', 3: 'phy_def', 4: 'mag_atk', 5: 'mag_def',
        #     6: 'dodge', 7: 'hit', 8: 'crit_atk', 9: 'crit_def', 10: 'phy_pen',
        #     11: 'mag_pen', 12: 'speed', 13: 'atkspeed', 14: 'suck', 15: 'phy_imm',
        #     16: 'mag_imm', 17: 'recover', 18: 'rage', 19: 'luck_ck', 20: 'luck_fm',
        #     21: 'luck_sl', 22: 'luck_wq', 23: 'luck_fj', 24: 'luck_lj', 25: 'medical_effect', 26: 'crit_damage',
        #     100: 'damage', 101: 'strength', 102: 'agility', 103: 'intelligence',
        #     104: 'change_skill', 105: 'add_normal_damage', 106: 'change_atk_skill'
        # }
        self.base_attr = (1, 2, 3, 4, 5)  # 基础属性
        self.hero_basis_init_attr = (7, 8, 9, 10, 11)  # 英雄表基础属性
        self.bonus_attr = {  # 加成属性影响的基础属性
            'hero': {'hp': 'hero_hp_bonus', 'phy_atk': 'hero_atk_bonus', 'mag_atk': 'hero_mag_bonus',
                     'phy_def': 'hero_def_bonus', 'mag_def': 'hero_mag_def_bonus'},
            'equip': {'hp': 'equip_hp_bonus', 'phy_atk': 'equip_atk_bonus', 'mag_atk': 'equip_mag_bonus',
                      'phy_def': 'gene_def_bonus', 'mag_def': 'gene_mag_def_bonus'},
            'gene': {'hp': 'hp_bonus', 'phy_atk': 'def_bonus', 'mag_atk': 'mag_def_bonus'}
        }
        self.bonus_split = {
            'hero_bothatk_bonus': ['hero_atk_bonus', 'hero_mag_bonus'],
            'gene_bothatk_bonus': ['def_bonus', 'mag_def_bonus']
        }
        self.hero_attr_final_bonus = {
            'hp': 'final_hp_bonus', 'phy_atk': 'character_atk_bonus', 'mag_atk': 'character_mag_bonus',
            'phy_def': 'character_def_bonus', 'mag_def': 'character_magdef_bonus',
        }
        self.bonus_to_base_mapping = {12: {1: 1, 2: 4}, 13: 2, 14: 3, 15: 5}  # 百分比加成对应属性, hp_bonus:hp
        self.bonus_mapping = {'atk_bonus': 12, 'hp_bonus': 13, 'def_bonus': 14, 'mag_def_bonus': 15}

        # self.hero_battle_job = [1, 2, 3, 4, 5, 6]  # 战斗英雄职业
        self.hero_dress_all_equip = [6]  # 英雄穿戴所有装备
        # self.hero_to_stone_num = {1: 7, 2: 15, 3: 30, 4: 30, 5: 30}

        # self.major_to_minor_by_pro = {'strength': {'hp': 12, 'phy_def': 0.3, 'mag_def': 0.2},     # 力量
        #                               'agility': {'phy_atk': 0.5},        # 敏捷
        #                               'intelligence': {'mag_atk': 0.5, 'mag_def': 0.1}}     # 智力
        self.coll_star_rate = {1: 0.025, 2: 0.05, 3: 0.075, 4: 0.1, 5: 0.125, 6: 0.15, 7: 0.175, 8: 0.2, 9: 0.225,
                               10: 0.25, 11: 0.275, 12: 0.3, 13: 0.325, 14: 0.35, 15: 0.375, 16: 0.4, 17: 0.425,
                               18: 0.45, 19: 0.475, 20: 0.5, 21: 0.6, 22: 0.7, 23: 0.8, 24: 0.9, 25: 1}
        self.manu_star_rate = {1: 0.005, 2: 0.01, 3: 0.015, 4: 0.02, 5: 0.025, 6: 0.03, 7: 0.035, 8: 0.04, 9: 0.045,
                               10: 0.05, 11: 0.055, 12: 0.06, 13: 0.065, 14: 0.07, 15: 0.075, 16: 0.08, 17: 0.085,
                               18: 0.09, 19: 0.095, 20: 0.1, 21: 0.11, 22: 0.12, 23: 0.13, 24: 0.14, 25: 0.15}

        self.MUITL_LAN = {'0': 'CN', '1': 'TW'}

        # server_open 后端记录开服信息用的，用于开新服后run_timer脚本 reload game_config，运行新服各个刷新脚本
        self.server_open = {}

        self.guide_mapping = {}
        self.use_item_mapping = {}
        self.shop_id_mapping = {}
        self.denate_shop_id_mapping = {}
        self.rally_shop_id_mapping = {}
        self.period_shop_id_mapping = {}
        self.exchange_shop_id_mapping = {}
        self._server_start_time = 0
        # self.task_mapping = {}
        self.achievement_starts_mapping = {}
        self.achievement_collection_mapping = {}
        self.stage_chapter_mapping = {}
        self.stage_degree_mapping = {}
        self.value_mapping = {}
        self.arena_award_mapping = {}
        self.building_unlock_mapping = {}
        self.manufacture_mapping = {}
        self.manufacture_skill_sort_mapping = {}
        self.manufacture_sort_mapping = {}
        self.robots_mapping = {}
        self.collection_resource_mapping = {}
        self.daily_rewards_boss_mapping = {}
        self.collection_resource_exchange_mapping = {}
        self.extra_skill_growth_mapping = {}
        self.commander_reward_mapping = {}
        self.equip_random_mapping = {}
        self.equip_suit_mapping = {}
        self.gene_suit_mapping = {}
        self.manufacture_stone_mapping = {}
        self.daily_advance_mapping = {}
        self.darkstreet_reward_break_mapping = {}
        self.darkstreet_fight_mapping = {}
        self.darkstreet_fight_mapping1 = {}
        self.dark_shop_id_mapping = {}
        self.hero_milestone_sort_mapping = {}
        self.guild_shop_mapping = {}
        self.guild_boss_coin_mapping = {}
        self.sevenday_info_mapping = {}
        self.message_mapping = {}
        self.collection_manufacture_mapping = {}
        self.hero_stone_mappnig = {}
        self.team_boss_mapping = {}
        self.play_help_sort = []
        self.level_mail_mapping = {}
        self.new_equip_awake_mapping = {}
        self.gene_random_mapping = {}
        self.arena_once_reward_mapping = {}
        self.darkstreet_milestone_mapping = {}
        self.awaken_chapter_mapping = {}
        self.arena_shop_id_mapping = {}
        self.wormhole_shop_id_mapping = {}
        self.equip_shop_id_mapping = {}
        self.profiteer_shop_id_mapping = {}
        self.honor_shop_id_mapping = {}
        self.rally_stage_mapping = {}
        self.gift_show_mapping = {}
        self.buy_reward_mapping = {}
        self.server_gift_show_mapping = {}
        self.server_buy_reward_mapping = {}
        self.super_rich_mapping = {}
        self.title_task_sort_mapping = {}
        self.diamond_gacha_mapping = {}
        self.diamond_gacha_score_mapping = {}
        self.box_gacha_score_mapping = {}
        self.coin_gacha_mapping = {}
        self.box_gacha_mapping = {}
        self.clone_bank_grade_mapping = {}
        self.box_shop_id_mapping = {}
        self.charge_ios_mapping = {}
        self.language_config_mapping = {}
        self.all_equip_item_exp_mapping = {}
        self.donate_shop_id_mapping = {}
        self.limit_hero_mapping = {}
        self.server_limit_hero_mapping = {}
        self.king_war_shop_id_mapping = {}
        self.sign_reward_mapping = {}
        self.doomsday_hunt_mapping = {}
        self.server_link_mapping = {}  # 限时神将跨服
        self.server_link_uc_mapping = {}  # 极限挑战跨服
        self.chapter_mapping = {}
        self.shop_goods_mapping = {}
        self.book_mapping = {}
        self.phone_chapter_dialogue_mapping = {}

    def reset(self):
        """ 配置更新后重置数据

        :return:
        """
        self.guide_mapping.clear()
        self.use_item_mapping.clear()
        self.shop_id_mapping.clear()
        self.shop_goods_mapping.clear()
        self.denate_shop_id_mapping.clear()
        self.rally_shop_id_mapping.clear()
        self.period_shop_id_mapping.clear()
        self.exchange_shop_id_mapping.clear()
        self._server_start_time = 0
        # self.task_mapping.clear()
        self.achievement_starts_mapping.clear()
        self.achievement_collection_mapping.clear()
        self.stage_chapter_mapping.clear()
        self.stage_degree_mapping.clear()
        self.value_mapping.clear()
        self.arena_award_mapping.clear()
        self.building_unlock_mapping.clear()
        self.manufacture_mapping.clear()
        self.manufacture_skill_sort_mapping.clear()
        self.manufacture_sort_mapping.clear()
        self.robots_mapping.clear()
        self.collection_resource_mapping.clear()
        self.daily_rewards_boss_mapping.clear()
        self.collection_resource_exchange_mapping.clear()
        self.extra_skill_growth_mapping.clear()
        self.super_rich_mapping.clear()
        self.commander_reward_mapping.clear()
        self.equip_random_mapping.clear()
        self.equip_suit_mapping.clear()
        self.gene_suit_mapping.clear()
        self.manufacture_stone_mapping.clear()
        self.daily_advance_mapping.clear()
        self.darkstreet_reward_break_mapping.clear()
        self.darkstreet_fight_mapping.clear()
        self.darkstreet_fight_mapping1.clear()
        self.dark_shop_id_mapping.clear()
        self.hero_milestone_sort_mapping.clear()
        self.guild_shop_mapping.clear()
        self.guild_boss_coin_mapping.clear()
        self.sevenday_info_mapping.clear()
        self.message_mapping.clear()
        self.collection_manufacture_mapping.clear()
        self.hero_stone_mappnig.clear()
        self.team_boss_mapping.clear()
        self.play_help_sort = []
        self.level_mail_mapping.clear()
        self.new_equip_awake_mapping.clear()
        self.gene_random_mapping.clear()
        self.arena_once_reward_mapping.clear()
        self.darkstreet_milestone_mapping.clear()
        self.awaken_chapter_mapping.clear()
        self.arena_shop_id_mapping.clear()
        self.wormhole_shop_id_mapping.clear()
        self.equip_shop_id_mapping.clear()
        self.profiteer_shop_id_mapping.clear()
        self.honor_shop_id_mapping.clear()
        self.rally_stage_mapping.clear()
        self.gift_show_mapping.clear()
        self.buy_reward_mapping.clear()
        self.diamond_gacha_mapping.clear()
        self.diamond_gacha_score_mapping.clear()
        self.box_gacha_score_mapping.clear()
        self.coin_gacha_mapping.clear()
        self.box_gacha_mapping.clear()
        self.clone_bank_grade_mapping.clear()
        self.box_shop_id_mapping.clear()
        self.charge_ios_mapping.clear()
        self.language_config_mapping.clear()
        self.all_equip_item_exp_mapping.clear()
        self.donate_shop_id_mapping.clear()
        self.limit_hero_mapping.clear()
        self.title_task_sort_mapping.clear()
        self.server_limit_hero_mapping.clear()
        self.server_gift_show_mapping.clear()
        self.server_buy_reward_mapping.clear()
        self.king_war_shop_id_mapping.clear()
        self.sign_reward_mapping.clear()
        self.doomsday_hunt_mapping.clear()
        self.server_link_mapping.clear()
        self.server_link_uc_mapping.clear()
        self.chapter_mapping.clear()
        self.book_mapping.clear()
        self.phone_chapter_dialogue_mapping.clear()

    def update_funcs_version(self, config_name):
        """
        更新配置版本号
        :param config_name:
        :return:
        """
        cm = ConfigMd5.get()
        cv = ConfigVersion.get()

        config = getattr(self, config_name, {})
        cv_version = cm.generate_custom_md5(config)
        cv.update_version(config_name, cv_version, save=True)

        ver_md5 = cm.generate_md5(cv.versions)
        cm.update_md5(cv.versions, gen_md5=ver_md5, save=True)

    def get_server_link_mapping(self, tp='world_id'):
        """
        跨服分组mapping
        :param tp: world_id or challenge_id
        :return:
        """
        if tp == 'world_id':
            server_link_mapping = self.server_link_mapping
        elif tp == 'challenge_id':
            server_link_mapping = self.server_link_uc_mapping
        else:
            return {}

        if not server_link_mapping:
            for i, j in self.server_link.iteritems():
                world_id = j[tp]
                if world_id not in server_link_mapping:
                    server_link_mapping[world_id] = []
                if i not in server_link_mapping[world_id]:
                    server_link_mapping[world_id].append(i)

            for i, j in server_link_mapping.iteritems():
                j.sort()

        return server_link_mapping

    def get_server_link_group(self, server_id, tp='world_id'):
        """
        获取跨服分组
        :param server_id:
        :param tp: world_id or challenge_id
        :return:
        """
        group_id = self.server_link.get(server_id, {}).get(tp)
        if group_id is None:
            group_id = min(self.get_server_link_mapping(tp).keys())
        master_server = self.get_server_link_mapping(tp)[group_id][0]

        return group_id, master_server

    def get_guide_mapping(self, sort):
        """
        新手引导映射
        :param sort:
        :return: [guide_id,]
        """
        if not self.guide_mapping:
            for i, j in self.guide.iteritems():
                s = j['sort']
                if s not in self.guide_mapping:
                    self.guide_mapping[s] = [i]
                else:
                    self.guide_mapping[s].append(i)

        return self.guide_mapping.get(sort, [])

    def get_doomsday_hunt_mapping(self, _hard, _sort):
        """
        猛兽boss难度映射
        :return:
        """
        if not self.doomsday_hunt_mapping:
            doomsday_hunt_mapping = self.doomsday_hunt_mapping
            for i, j in self.doomsday_hunt.iteritems():
                hard = j['hard']
                sort = j['sort']
                if hard not in doomsday_hunt_mapping:
                    doomsday_hunt_mapping[hard] = {}
                if sort not in doomsday_hunt_mapping[hard]:
                    doomsday_hunt_mapping[hard][sort] = i

        return self.doomsday_hunt_mapping.get(_hard, {}).get(_sort, 0)

    def get_title_task_sort_mapping(self):
        """
        获取称号配置中的sort映射
        :return:
        """
        if not self.title_task_sort_mapping:
            for i, j in self.title.iteritems():
                s = j['sort']
                if s not in self.title_task_sort_mapping:
                    self.title_task_sort_mapping[s] = {}
                self.title_task_sort_mapping[s][i] = {}

        return self.title_task_sort_mapping

    def get_rally_stage_mapping(self, rally_id):
        """
        血沉拉力赛购买宝箱
        :param rally_id:
        :return:
        """
        if not self.rally_stage_mapping:
            for i, j in self.rally_box.iteritems():
                r_id = j['rally_id']
                s_id = j['stage_id']
                if r_id not in self.rally_stage_mapping:
                    self.rally_stage_mapping[r_id] = {}
                self.rally_stage_mapping[r_id][s_id] = i

        if not self.rally_stage_mapping:
            return {}

        if rally_id not in self.rally_stage_mapping:
            return self.rally_stage_mapping[max(self.rally_stage_mapping)]
        else:
            return self.rally_stage_mapping.get(rally_id, {})

    def get_play_help_mapping(self):
        """
        提示系统,按优先级排序id
        :return:
        """
        if not self.play_help_sort:
            play_help_sort = []
            for i, j in self.play_help.iteritems():
                play_help_sort.append((i, j['priority']))

            self.play_help_sort = sorted(play_help_sort, key=lambda x: x[1])

        return self.play_help_sort

    def get_arena_award_mapping(self, rank):
        """
        竞技场奖励mapping
        :param rank:
        :return:
        """
        if not self.arena_award_mapping:
            for i, j in self.arena_award.iteritems():
                start_rank = j.get('start_rank')
                if not start_rank:
                    continue
                self.arena_award_mapping[start_rank] = i

        rank_list = sorted(self.arena_award_mapping)
        r = bisect.bisect(rank_list, rank)

        return self.arena_award_mapping.get(rank_list[r - 1], 0)

    def get_team_boss_id_by_sort(self, sort):
        """
        组队boss的关卡id映射
        :param sort:
        :return:
        """
        if not self.team_boss_mapping:
            for i, j in self.team_boss.iteritems():
                s = j['sort']
                unlock_lvl = j['unlock_lvl']
                if s not in self.team_boss_mapping:
                    self.team_boss_mapping[s] = {}
                self.team_boss_mapping[s][i] = unlock_lvl

        return self.team_boss_mapping.get(sort, {})

    def get_summon_cost_by_stone_id(self, stone_id):
        """
        通过英雄灵魂石id获取召唤需要数量和银币数量
        :param stone_id: 灵魂石id
        :return:
        """
        if not self.hero_stone_mappnig:
            for i, j in self.hero_basis.iteritems():
                if not j['if_show']:
                    continue
                star_stone_num = j.get('combine', 80)
                star_cost = 0
                # star_stone_config = j['star_stone']
                # star_cost_config = j['star_cost']
                init_star = j['init_star']
                # grade_lv = j['grade'] + 10  # 资质
                grade_lv = j['quality']
                for lv in xrange(1, init_star + 1):
                    # hero_stone = self.hero_star.get(lv, {}).get('hero_stone', {})
                    # star_stone_num += hero_stone.get(grade_lv) or hero_stone[12]
                    # star_stone_num += star_stone_config.get(lv, 0)
                    hero_cost = self.hero_star.get(lv, {}).get('hero_cost', {})
                    star_cost += hero_cost.get(grade_lv) or hero_cost[1]
                    # star_cost += star_cost_config.get(lv, 0)
                if star_stone_num and j['stone'] not in self.hero_stone_mappnig:
                    self.hero_stone_mappnig[j['stone']] = {
                        'stone': star_stone_num,
                        'cost': star_cost,
                        'hero_id': i,
                    }

        return self.hero_stone_mappnig.get(stone_id, {})

    def get_item_id_with_sort(self, sort):
        """ 通过类型获取item_id, 排序规则为效果从大到小

        :param sort:
        :return: []
        """
        item_ids = self.use_item_mapping.get(sort, [])
        if item_ids:
            return item_ids

        data = [(k, v['use_effect']) for k, v in self.use_item.iteritems() if v['is_use'] == 7]
        data_sorted = sorted(data, key=lambda x: x[1], reverse=True)

        self.use_item_mapping[sort] = item_ids = [k for k, v in data_sorted]

        return item_ids

    def get_shop_id_with_level(self, shop_id, level):
        """
        通过玩家等级获得可购买范围的物品
        :param level:
        :return: []
        """
        if not self.shop_goods_mapping.get(shop_id, {}):
            data = {}
            for k, v in self.get_shop_config(shop_id).iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.shop_goods_mapping[shop_id] = result
        pos = bisect.bisect(self.shop_goods_mapping[shop_id]['index'], level)
        if not pos:
            return {}
        else:
            lv = self.shop_goods_mapping[shop_id]['index'][pos - 1]
            return self.shop_goods_mapping[shop_id]['data'][lv]

    def get_rally_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的物品
        :param level:
        :return: []
        """
        if not self.rally_shop_id_mapping:
            data = {}
            for k, v in self.rally_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.rally_shop_id_mapping = result

        pos = bisect.bisect(self.rally_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.rally_shop_id_mapping['index'][pos - 1]
            return self.rally_shop_id_mapping['data'][lv]

    def get_donate_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的物品
        :param level:
        :return: []
        """
        if not self.donate_shop_id_mapping:
            data = {}
            for k, v in self.donate_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.donate_shop_id_mapping = result

        pos = bisect.bisect(self.donate_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.donate_shop_id_mapping['index'][pos - 1]
            return self.donate_shop_id_mapping['data'][lv]

    def get_arena_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的竞技场物品
        :param level:
        :return: []
        """
        if not self.arena_shop_id_mapping:
            data = {}
            for k, v in self.arena_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.arena_shop_id_mapping = result

        pos = bisect.bisect(self.arena_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.arena_shop_id_mapping['index'][pos - 1]
            return self.arena_shop_id_mapping['data'][lv]

    def get_sign_reward_mapping(self):
        """
        普通签到映射
        :return:
        """
        if not self.sign_reward_mapping:
            for i, j in self.sign_reward.iteritems():
                version = j['version']
                if version not in self.sign_reward_mapping:
                    self.sign_reward_mapping[version] = {}
                if i not in self.sign_reward_mapping[version]:
                    self.sign_reward_mapping[version][i] = j

        return self.sign_reward_mapping

    def get_guild_shop_with_level(self, level):
        """
        通过玩家等级获得可购买范围的公会物品
        :param level:
        :return: []
        """
        if not self.guild_shop_mapping:
            data = {}
            for k, v in self.guild_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.guild_shop_mapping = result

        pos = bisect.bisect(self.guild_shop_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.guild_shop_mapping['index'][pos - 1]
            return self.guild_shop_mapping['data'][lv]

    def get_dark_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的物品
        :param level:
        :return: []
        """
        if not self.dark_shop_id_mapping:
            data = {}
            for k, v in self.darkstreet_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.dark_shop_id_mapping = result

        pos = bisect.bisect(self.dark_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.dark_shop_id_mapping['index'][pos - 1]
            return self.dark_shop_id_mapping['data'][lv]

    def get_wormhole_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的虫洞矿坑物品
        :param level:
        :return: []
        """
        if not self.wormhole_shop_id_mapping:
            data = {}
            for k, v in self.tower_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.wormhole_shop_id_mapping = result

        pos = bisect.bisect(self.wormhole_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.wormhole_shop_id_mapping['index'][pos - 1]
            return self.wormhole_shop_id_mapping['data'][lv]

    def get_equip_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的装备商店物品
        :param level:
        :return: []
        """
        if not self.equip_shop_id_mapping:
            data = {}
            for k, v in self.equip_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.equip_shop_id_mapping = result

        pos = bisect.bisect(self.equip_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.equip_shop_id_mapping['index'][pos - 1]
            return self.equip_shop_id_mapping['data'][lv]

    def get_profiteer_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的装备商店物品
        :param level:
        :return: []
        """
        if not self.profiteer_shop_id_mapping:
            data = {}
            for k, v in self.profiteer_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.profiteer_shop_id_mapping = result

        pos = bisect.bisect(self.profiteer_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.profiteer_shop_id_mapping['index'][pos - 1]
            return self.profiteer_shop_id_mapping['data'][lv]

    def get_honor_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的荣誉商店物品
        :param level:
        :return: []
        """
        if not self.honor_shop_id_mapping:
            data = {}
            for k, v in self.honor_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.honor_shop_id_mapping = result

        pos = bisect.bisect(self.honor_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.honor_shop_id_mapping['index'][pos - 1]
            return self.honor_shop_id_mapping['data'][lv]

    def get_commander_reward_with_level(self, level):
        """
        通过玩家等级获得统帅合成掉落随机奖励
        :param level:
        :return: []
        """
        if not self.commander_reward_mapping:
            data = {}
            for k, v in self.commander_reward.iteritems():
                use_lv = v['use_lvl']
                if use_lv not in data:
                    data[use_lv] = [[v['reward'], v['weight']]]
                else:
                    data[use_lv].append([v['reward'], v['weight']])

            result = {'index': [], 'data': []}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = []
            for use_lv, value in data_sort:
                pre_data.extend(value)
                result['index'].append(use_lv)
                result['data'].append(copy.deepcopy(pre_data))

            self.commander_reward_mapping = result

        pos = bisect.bisect(self.commander_reward_mapping['index'], level)
        if not pos:
            return []
        else:
            return self.commander_reward_mapping['data'][pos - 1]

    def get_period_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的物品
        :param level:
        :return: []
        """
        if not self.period_shop_id_mapping:
            data = {}
            for k, v in self.period_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.period_shop_id_mapping = result

        pos = bisect.bisect(self.period_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.period_shop_id_mapping['index'][pos - 1]
            return self.period_shop_id_mapping['data'][lv]

    def get_box_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的物品
        :param level:
        :return: []
        """
        if not self.box_shop_id_mapping:
            data = {}
            for k, v in self.shop_box.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.box_shop_id_mapping = result

        pos = bisect.bisect(self.box_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.box_shop_id_mapping['index'][pos - 1]
            return self.box_shop_id_mapping['data'][lv]

    def get_king_war_shop_id_with_level(self, level):
        """
        通过玩家等级获得可购买范围的物品
        :param level:
        :return: []
        """
        if not self.king_war_shop_id_mapping:
            data = {}
            for k, v in self.king_war_shop.iteritems():
                use_lv = v['show_lv']
                pos_id = v['pos_id']
                if use_lv not in data:
                    data[use_lv] = {}
                if pos_id not in data[use_lv]:
                    data[use_lv][pos_id] = []
                if not v['weight']:
                    continue
                data[use_lv][pos_id].append([k, v['weight']])

            result = {'index': [], 'data': {}}
            data_sort = sorted(data.iteritems(), key=lambda x: x[0])
            pre_data = {}
            for use_lv, value in data_sort:
                for pos_id, v in value.iteritems():
                    if pos_id not in pre_data:
                        pre_data[pos_id] = []

                    pre_data[pos_id].extend(v)
                for pos_id, v in pre_data.iteritems():
                    if use_lv not in result['data']:
                        result['data'][use_lv] = {}
                    if pos_id not in result['data'][use_lv]:
                        result['data'][use_lv][pos_id] = []
                    result['data'][use_lv][pos_id].extend(copy.deepcopy(pre_data[pos_id]))
                result['index'].append(use_lv)

            self.king_war_shop_id_mapping = result

        pos = bisect.bisect(self.king_war_shop_id_mapping['index'], level)
        if not pos:
            return {}
        else:
            lv = self.king_war_shop_id_mapping['index'][pos - 1]
            return self.king_war_shop_id_mapping['data'][lv]

    def get_skill_config(self, skill_id):
        """ 通过技能id获取技能表
            技能id范围	技能类型	升级规则
            10001~20000	普通技能	不能超过自身英雄lvl
            20001~30000	必杀技	不能超过自身英雄lvl
            30001~40000	专业技	不能超过自身英雄lvl
            40001~50000	专业必杀技	不能超过自身英雄进阶lvl

        :param skill_id:
        :return:
        """
        if 10001 <= skill_id <= 30000:
            return 1, self.skill_detail[skill_id]
        elif 30001 <= skill_id <= 40000:
            return 3, self.extra_skill[skill_id]
        else:
            return 0, {}

    def get_lvlup_skill_max_level(self, skill_id, level, evo):
        """ 获取升级技能最大等级
            技能id范围	技能类型	升级规则
            10001~20000	普通技能	不能超过自身英雄lvl
            20001~30000	必杀技	不能超过自身英雄lvl
            30001~40000	专业技	不能超过自身英雄lvl
            40001~50000	专业必杀技	不能超过自身英雄进阶lvl

        :param skill_id:
        :param level:
        :param evo:
        :return:
        """
        return min(level, max(self.skill_lvlup_cost))

    def get_lvlup_skill_cost(self, skill_id, level):
        """ 获取升级技能花费
            技能id范围	技能类型	升级规则
            10001~20000	普通技能	不能超过自身英雄lvl
            20001~30000	必杀技	不能超过自身英雄lvl
            30001~40000	专业技	不能超过自身英雄lvl
            40001~50000	专业必杀技	不能超过自身英雄进阶lvl

        :param skill_id:
        :param level:
        :return:
        """
        skill_lvlup_cost = self.skill_lvlup_cost.get(level, {})

        return skill_lvlup_cost.get('normal_skill_cost')

    def get_skill_growth_rate(self, skill_sort, skill_level, skill_type=0):
        """ 获取技能成长值

        :param skill_sort:
        :param skill_level:
        :param skill_type:
        :return:
        """
        skill_growth_rate = self.skill_growth_rate.get(skill_level)
        if not skill_growth_rate:
            return 1

        if skill_sort == 1:  # 战斗技能
            return skill_growth_rate.get('rate', 1)
        elif skill_sort == 2:  # 英雄被动技能
            return skill_growth_rate.get('passive_rate', 1)
        else:
            return 1

    # def get_extra_skill_growth_mapping(self, sort):
    #     if not self.extra_skill_growth_mapping:
    #         result = {1: {}, 2: {}, 3: {}, 4: {}}
    #         for lv, config in self.extra_skill_growth.iteritems():
    #             for index, name in enumerate(('dab', 'fan', 'expert', 'master'), start=1):
    #                 quality = config['%s_quality' % name]
    #                 effect = config['%s_effect' % name]
    #                 if quality not in result[index] or result[index][quality] < effect:
    #                     result[index][quality] = effect
    #
    #         self.extra_skill_growth_mapping = result
    #
    #     return self.extra_skill_growth_mapping.get(sort, {})

    def get_extra_skill_growth_rate(self, skill_sort, skill_level):
        """ 获取附加技能成长值

        :param skill_sort:
        :param skill_level:
        :param skill_type:
        :return:
        """
        skill_growth_rate = self.extra_skill_growth.get(skill_level)
        effect = 0

        if not skill_growth_rate:
            return effect

        if skill_sort == 1:  # 能手
            name = 'dab'
        elif skill_sort == 2:  # 爱好者
            name = 'fan'
        elif skill_sort == 3:  # 专家
            name = 'expert'
        elif skill_sort == 4:  # 大师
            name = 'master'
        else:
            return effect

        effect = skill_growth_rate.get('%s_effect' % name, 0)

        return effect

    def server_start_time(self, server_name):
        # if not self._server_start_time:
        from models.server import ServerConfig
        sc = ServerConfig.get()
        data = sc.get_server(server_name)
        self._server_start_time = data['open_time']
        return self._server_start_time

    def get_config_type(self, server_name, now=None):
        """ 获取config_type

        :param server_name:
        :return: str
        """
        server_name = settings.get_server_num(server_name)
        server_type = self.server_type
        now = now or time.strftime("%Y-%m-%d %H:%M:%S")

        config = server_type.get(server_name)
        if config and now >= config['time']:
            config_type = config['type']
        else:
            config_type = settings.SERVERS.get(server_name, {}).get('config_type', 1)

        return int(config_type)

    # def get_task_config_by_sort(self, sort):
    #     """ 通过类型获取任务配置
    #
    #     :param sort: 等级
    #     :return:
    #     """
    #     if not self.task_mapping:
    #         for task_id, task_config in self.task_main_detail.iteritems():
    #             task_sort = task_config['sort']
    #             if task_sort not in self.task_mapping:
    #                 self.task_mapping[task_sort] = {
    #                     task_id: [task_config['target1'], task_config['target2']],
    #                 }
    #             else:
    #                 self.task_mapping[task_sort][task_id] = [task_config['target1'], task_config['target2']]
    #
    #     task_config = self.task_mapping.get(sort, {})
    #
    #     return task_config

    def get_achievement_starts_mapping(self):
        """
        获取每类成就的第一个任务
        :return:
        """
        if not self.achievement_starts_mapping:
            for ach_id, ach_config in self.achievement.iteritems():
                start_id = ach_config['start_id']
                if start_id and ach_id not in self.achievement_starts_mapping:
                    self.achievement_starts_mapping[ach_id] = start_id

        return self.achievement_starts_mapping

    def get_achievement_collection_mapping(self, need_tag=None):
        """
        按收集成就的tag分类
        :param need_tag:
        :return:
        """
        if not self.achievement_collection_mapping:
            for task_id, task_config in self.achievement_collection.iteritems():
                tag = task_config['tag']
                if tag not in self.achievement_collection_mapping:
                    self.achievement_collection_mapping[tag] = []

                for i in task_config['need']:
                    if i not in self.achievement_collection_mapping[tag]:
                        self.achievement_collection_mapping[tag].append(i)

        if not need_tag:
            return self.achievement_collection_mapping
        else:
            return self.achievement_collection_mapping.get(need_tag, {})

    def get_chapter(self, need_stage_id):
        """ 通过关卡id获取章节

        :param need_stage_id:
        :return:
        """
        if not self.stage_chapter_mapping:
            result = {}
            for chapter_id, chapter_config in self.chapter.iteritems():
                stage_teams = chapter_config['stage']
                for stage_team_id in stage_teams:
                    if stage_team_id:
                        chapter_to_stage_config = self.chapter_to_stage.get(stage_team_id)
                        if not chapter_to_stage_config:
                            continue
                        for sort in ['easy', 'hard', 'hell']:
                            stage_id = chapter_to_stage_config[sort]
                            if stage_id:
                                result[stage_id] = chapter_id
            self.stage_chapter_mapping = result

        return self.stage_chapter_mapping.get(need_stage_id)

    def get_degree(self, need_stage_id):
        """ 通过关卡id获取难度

        :param need_stage_id:
        :return:
        """
        if not self.stage_degree_mapping:
            result = {}
            for chapter_id, chapter_config in self.chapter.iteritems():
                stage_teams = chapter_config['stage']
                for stage_team_id in stage_teams:
                    if stage_team_id:
                        chapter_to_stage_config = self.chapter_to_stage.get(stage_team_id)
                        if not chapter_to_stage_config:
                            continue
                        for index, sort in enumerate(['easy', 'hard', 'hell']):
                            stage_id = chapter_to_stage_config[sort]
                            if stage_id:
                                result[stage_id] = index + 1
            self.stage_degree_mapping = result

        return self.stage_degree_mapping.get(need_stage_id)

    def get_value(self, valud_id, default=None):
        """
        获取value配置的数据
        :param valud_id:
        :param default:
        :return:
        """
        if not self.value_mapping:
            for k, v in self.value.iteritems():
                self.value_mapping[k] = v.get('value')

        return self.value_mapping.get(valud_id) or default

    def get_building_unlock_mapping(self, unlock_type):
        """
        通过解锁类型获取解锁建筑配置id
        :param unlock_type:
        :return:
        """
        if not self.building_unlock_mapping:
            result = {}
            for unlock_id, unlock_config in self.building_unlock.iteritems():
                unlock_type_config = unlock_config['unlock_type']
                if unlock_type_config not in result:
                    result[unlock_type_config] = {
                        unlock_id: {
                            'unlock_limit': unlock_config['unlock_limit'],
                            'unlock_look': unlock_config['unlock_look'],
                        },
                    }
                else:
                    result[unlock_type_config][unlock_id] = {
                        'unlock_limit': unlock_config['unlock_limit'],
                        'unlock_look': unlock_config['unlock_look'],
                    }
            self.building_unlock_mapping = result

        return self.building_unlock_mapping.get(unlock_type, {})

    def get_random_name(self, lan_sort, mod_id=None):
        """ 获取随机名字

        :return:
        """
        first_name = self.get_first_random_name(lan_sort, mod_id)
        last_name = self.get_last_random_name(lan_sort, mod_id)
        name = first_name + last_name
        return name

    def get_last_random_name(self, lan_sort, mod_id=None,sex=1):
        """ 获取后缀随机名字
        :param mod_id: 指定第几个名字
        :return:
        """
        from gconfig import get_str_words
        last_name = self.last_random_name.get(sex,{}).get('last_name', [])
        name = ''
        if last_name:
            if mod_id is None:
                name += random.choice(last_name)
            else:
                mod_id %= len(last_name)
                name += last_name[mod_id]
            name = get_str_words(lan_sort, name)
        return name

    def get_first_random_name(self, lan_sort, mod_id=None):
        """ 获取后缀随机名字
        :param mod_id: 指定第几个名字
        :return:
        """
        from gconfig import get_str_words
        first_name = self.first_random_name.get('first_name', [])
        name = ''
        if first_name:
            if mod_id is None:
                name += random.choice(first_name)
            else:
                mod_id %= len(first_name)
                name += first_name[mod_id]
            name = get_str_words(lan_sort, name)
        return name

    def get_manufacture_mapping(self):
        if not self.manufacture_mapping:
            result = {}
            for manu_id, manu_dict in self.manufacture.iteritems():
                # 随机不考虑
                if manu_dict['random']:
                    continue
                # 只考虑装备
                sort = manu_dict['sort']
                if sort >= 6:
                    continue
                job = manu_dict['job']
                evolution = manu_dict['evolution']
                if sort not in result:
                    result[sort] = {'job': job, 'value': []}
                result[sort]['value'].append((evolution, manu_id))

            for sort, data in result.iteritems():
                data['value'] = [v for k, v in sorted(data['value'], key=lambda x: x[0], reverse=True)]
            self.manufacture_mapping = result
        return self.manufacture_mapping

    def get_manufacture_skill_sort_mapping(self):
        if not self.manufacture_skill_sort_mapping:
            result = {}
            for manu_id, manu_dict in self.manufacture.iteritems():
                # 只考虑战斗道具
                sort = manu_dict['sort']
                if sort != 6:
                    continue
                skill_sort = manu_dict['skill_sort']
                evolution = manu_dict['evolution']
                if skill_sort not in result:
                    result[skill_sort] = []
                result[skill_sort].append((evolution, manu_id))

            for skill_sort in result:
                result[skill_sort] = [v for k, v in sorted(result[skill_sort], key=lambda x: x[0], reverse=True)]
            self.manufacture_skill_sort_mapping = result
        return self.manufacture_skill_sort_mapping

    def get_manufacture_sort_mapping(self):
        if not self.manufacture_sort_mapping:
            result = {}
            for manu_id, manu_dict in self.manufacture.iteritems():
                # 随机不考虑
                if manu_dict['random']:
                    continue
                # 只考虑装备
                sort = manu_dict['sort']
                if sort >= 6:
                    continue
                job = manu_dict['job']
                if job not in result:
                    result[job] = []
                if sort not in result[job]:
                    result[job].append(sort)

            self.manufacture_sort_mapping = result
        return self.manufacture_sort_mapping

    def get_robots_mapping(self):
        if not self.robots_mapping:
            result = {}
            for robot_id, robot_dict in self.robots.iteritems():
                lvl = robot_dict['lvl']
                if lvl not in result:
                    result[lvl] = []

                result[lvl].append((robot_id, robot_dict['weight']))

            self.robots_mapping = result

        return self.robots_mapping

    def get_collection_resource_mapping(self):
        if not self.collection_resource_mapping:
            result = {}
            for coll_id, roll_config in self.collection_resource.iteritems():
                if not roll_config['type']:
                    continue
                sort = roll_config['sort']
                if sort not in result:
                    result[sort] = []
                # (采集资源id, 采集资源等阶, 采集一个需要的能力, 权重)
                result[sort].append((coll_id, roll_config['lv'],
                                     roll_config['collection_value'], roll_config['weight']))
            for sort, value in result.iteritems():
                value.sort(key=lambda x: x[1])

            self.collection_resource_mapping = result

        return self.collection_resource_mapping

    def get_collection_resource_exchange_mapping(self):
        if not self.collection_resource_exchange_mapping:
            result = {}
            for coll_id, coll_config in self.collection_resource.iteritems():
                exchange_type = coll_config['exchange_type']
                if exchange_type not in result:
                    result[exchange_type] = {}
                result[exchange_type][coll_config['lv']] = coll_id
            self.collection_resource_exchange_mapping = result

        return self.collection_resource_exchange_mapping

    def get_daily_rewards_boss_mapping(self):
        if not self.daily_rewards_boss_mapping:
            sections = []
            configs = []
            boss_sorted = sorted(self.daily_rewards_boss.iteritems(), key=lambda x: x[0])
            for section, config in boss_sorted:
                sections.append(section)
                configs.append(config)

            result = {'sections': sections, 'configs': configs}
            self.daily_rewards_boss_mapping = result

        return self.daily_rewards_boss_mapping

    def get_equip_random_by_quality(self, quality):
        """
        通过装备颜色获取随机附加属性
        :param quality: 装备颜色 1-6
        :return:
        """
        if not self.equip_random_mapping:
            for i, j in self.equip_random.iteritems():
                q_id = j['quality']
                if q_id not in self.equip_random_mapping:
                    self.equip_random_mapping[q_id] = []
                self.equip_random_mapping[q_id].append([j['random_sort'], j['random_range'], j['weight']])

        return self.equip_random_mapping[quality]

    def get_equip_random_by_quality_refine(self, quality):
        """
        通过装备颜色获取随机附加属性,用于洗练
        :param quality: 装备颜色 1-6
        :return:
        """
        if not self.equip_random_mapping:
            for i, j in self.equip_random.iteritems():
                q_id = j['quality']
                if q_id not in self.equip_random_mapping:
                    self.equip_random_mapping[q_id] = []
                self.equip_random_mapping[q_id].append([j['random_sort'], j['random_range_rebuild'], j['weight']])

        return self.equip_random_mapping[quality]

    def get_equip_suit_add(self, s_id):
        """
        通过装备套装id获取套装加成
        :param s_id: suit_id 套装id
        :return:
        """
        if not self.equip_suit_mapping:
            for i, j in self.equip_suit.iteritems():
                suit_id = j['suit_id']
                suit_sort = j['suit_sort']
                suit_add = j['suit_add']
                if suit_id not in self.equip_suit_mapping:
                    self.equip_suit_mapping[suit_id] = {}
                self.equip_suit_mapping[suit_id][suit_sort] = suit_add

        return self.equip_suit_mapping[s_id]

    def get_gene_suit_add(self, s_id):
        """
        通过基因套装id获取套装加成
        :param s_id: suit_id 套装id
        :return:
        """
        if not self.gene_suit_mapping:
            for i, j in self.gene_suit.iteritems():
                suit_id = j['suit_id']
                suit_sort = j['suit_sort']
                star = j['star']
                suit_add = j['suit_add']
                # if not suit_add:
                #     continue

                if suit_id not in self.gene_suit_mapping:
                    self.gene_suit_mapping[suit_id] = {}
                if suit_sort not in self.gene_suit_mapping[suit_id]:
                    self.gene_suit_mapping[suit_id][suit_sort] = {}
                self.gene_suit_mapping[suit_id][suit_sort][star] = [suit_add, i]

        return self.gene_suit_mapping.get(s_id, {})

    def get_manufacture_stone_attr(self, combine_id):
        """
        通过精炼石组合id: '11_1-12_2',获取额外附加属性
        :param combine_id:
        :return:
        """
        if not self.manufacture_stone_mapping:
            for i, j in self.manufacture_stone.iteritems():
                combination = j['combination']
                extra_att = sorted(j['extra_attribute'], key=lambda x: x[0])
                if extra_att:
                    c_id = '-'.join(map(lambda x: '%s_%s' % (x[0], x[1]), combination))
                    self.manufacture_stone_mapping[c_id] = extra_att

        return self.manufacture_stone_mapping.get(combine_id, [])

    def get_daily_advance_mapping(self):
        """
        进阶副本映射
        :return:
        """
        if not self.daily_advance_mapping:
            for i, j in self.daily_advance.iteritems():
                sort = j['sort']
                hard = j['hard']
                j['id'] = i
                if sort not in self.daily_advance_mapping:
                    self.daily_advance_mapping[sort] = {hard: j}
                else:
                    self.daily_advance_mapping[sort][hard] = j

        return self.daily_advance_mapping

    def get_clone_bank_grade_mapping(self, grade):
        """
        克隆人，英雄资质映射
        :param grade:
        :return:
        """
        if not self.clone_bank_grade_mapping:
            for i, j in self.clone_bank.iteritems():
                g = j['grade']
                w = j['weight']
                if g not in self.clone_bank_grade_mapping:
                    self.clone_bank_grade_mapping[g] = []
                self.clone_bank_grade_mapping[g].append([i, w])

        return self.clone_bank_grade_mapping.get(grade, [])

    def get_darkstreet_reward_break(self):
        """
        黑街擂台击破奖励映射
        :return:
        """
        if not self.darkstreet_reward_break_mapping:
            for i, j in self.darkstreet_reward_break.iteritems():
                times = j['times']
                reward = j['reward']
                self.darkstreet_reward_break_mapping[times] = reward

        return self.darkstreet_reward_break_mapping

    def get_darkstreet_fight_mapping1(self, need_round, grade, lv=None):
        """
        战力匹配表的映射
        :param round: 轮数
        :param grade: 档次
        :return:
        """
        if not self.darkstreet_fight_mapping:
            for i, j in self.darkstreet_fight.iteritems():
                r = j['round']
                g = j['grade']
                if r not in self.darkstreet_fight_mapping:
                    self.darkstreet_fight_mapping[r] = {}
                self.darkstreet_fight_mapping[r][g] = j

        if need_round in self.darkstreet_fight_mapping:
            config = self.darkstreet_fight_mapping[need_round]
        elif self.darkstreet_fight_mapping:
            config = self.darkstreet_fight_mapping[max(self.darkstreet_fight_mapping)]
        else:
            config = {}

        return config.get(grade, {})

    def get_darkstreet_fight_mapping(self, need_round, grade, lv):
        """
        战力匹配表的映射
        :param round: 轮数
        :param grade: 档次
        :return:
        """
        if not self.darkstreet_fight_mapping1:
            for i, j in self.darkstreet_fight.iteritems():
                r = j['round']
                g = j['grade']
                level = j['level']
                if level not in self.darkstreet_fight_mapping1:
                    self.darkstreet_fight_mapping1[level] = {}
                if r not in self.darkstreet_fight_mapping1[level]:
                    self.darkstreet_fight_mapping1[level][r] = {}
                self.darkstreet_fight_mapping1[level][r][g] = j

        lv_list = sorted(self.darkstreet_fight_mapping1.keys())
        index = bisect.bisect_left(lv_list, lv)
        if index >= len(lv_list):
            index = len(lv_list) - 1

        mapping_config = self.darkstreet_fight_mapping1[lv_list[index]]
        if need_round in mapping_config:
            config = mapping_config[need_round]
        elif mapping_config:
            config = mapping_config[max(mapping_config)]
        else:
            config = {}

        return config.get(grade, {})

    def get_hero_milestone_sort_mapping(self, hero_fid):
        """
        获取英雄里程碑任务包含的类型
        :param hero_fid:
        :return: {
            milestone_task_sort: {      # 配置milestone的任务类型sort
                task_n: task_id,        # 配置hero_milestone的task任务n: 任务id
            },
        }
        """
        if not self.hero_milestone_sort_mapping:
            for i, j in self.hero_milestone.iteritems():
                task = j['task']
                if i not in self.hero_milestone_sort_mapping:
                    self.hero_milestone_sort_mapping[i] = {}
                for task_n, task_id in task.iteritems():
                    sort = self.milestone.get(task_id, {}).get('sort', 0)
                    if not sort:
                        continue
                    if sort not in self.hero_milestone_sort_mapping[i]:
                        self.hero_milestone_sort_mapping[i][sort] = {task_n: task_id}
                    else:
                        self.hero_milestone_sort_mapping[i][sort][task_n] = task_id

        return self.hero_milestone_sort_mapping.get(hero_fid, {})

    def get_sevenday_info_mapping(self):
        """
        七日盛典任务配置映射
        :return:
        """
        if not self.sevenday_info_mapping:
            for i, j in self.sevenday_info.iteritems():
                sort = j['sort']
                if sort not in self.sevenday_info_mapping:
                    self.sevenday_info_mapping[sort] = {}
                self.sevenday_info_mapping[sort][i] = j

        return self.sevenday_info_mapping

    def get_message_mapping(self, sort):
        """
        跑马灯配置映射
        :param sort: 条件类型
        :return:
        """
        if not self.message_mapping:
            for i, j in self.message.iteritems():
                s = j['sort']
                if s not in self.message_mapping:
                    self.message_mapping[s] = {}
                self.message_mapping[s][i] = j

        return self.message_mapping.get(sort, {})

    def get_collection_manufacture_mapping(self, sort):
        """
        获取采集生产随机经验块映射
        :param sort:
        :return: {
            time: reward,
        }
        """
        if not self.collection_manufacture_mapping:
            for i, j in self.collection_manufacture.iteritems():
                s = j['sort']
                t = j['time']
                reward = j['reward']
                if s not in self.collection_manufacture_mapping:
                    self.collection_manufacture_mapping[s] = {t: reward}
                else:
                    self.collection_manufacture_mapping[s][t] = reward

        return self.collection_manufacture_mapping.get(sort, {})

    def get_awaken_chapter_mapping(self):
        """
        获取觉醒副本映射
        :return:
        """
        if not self.awaken_chapter_mapping:
            for i, j in self.awaken_chapter.iteritems():
                sort = j['sort']
                hard = j['hard']
                if sort not in self.awaken_chapter_mapping:
                    self.awaken_chapter_mapping[sort] = {}
                if hard not in self.awaken_chapter_mapping[sort]:
                    self.awaken_chapter_mapping[sort][hard] = {}
                self.awaken_chapter_mapping[sort][hard][i] = j

        return self.awaken_chapter_mapping

    def get_level_mail_mapping(self):
        """
        等级奖励邮件映射
        :return:
        """
        if not self.level_mail_mapping:
            for i, j in self.level_mail.iteritems():
                lv = j['level']
                if lv not in self.level_mail_mapping:
                    self.level_mail_mapping[lv] = {i}
                else:
                    self.level_mail_mapping[lv].add(i)

        return self.level_mail_mapping

    def get_new_equip_awake_mapping(self, equip_id):
        """
        新装备觉醒父id与子id的映射
        :param equip_id:
        :return:
        """
        if not self.new_equip_awake_mapping:
            for i, j in self.new_equip_detail.iteritems():
                awake_id = j['awake_id']
                if awake_id and awake_id not in self.new_equip_awake_mapping:
                    self.new_equip_awake_mapping[awake_id] = i

        return self.new_equip_awake_mapping.get(equip_id, equip_id)

    def get_gene_random_mapping(self, evo):
        """
        基因随机属性品阶映射
        :param evo:
        :return:
        """
        if not self.gene_random_mapping:
            for i, j in self.gene_random.iteritems():
                evo_limit = j['evo_limit']
                weight = j['weight']
                if evo_limit not in self.gene_random_mapping:
                    self.gene_random_mapping[evo_limit] = [[i, weight]]
                else:
                    self.gene_random_mapping[evo_limit].append([i, weight])

        return self.gene_random_mapping.get(evo, [])

    def get_arena_once_reward_mapping(self):
        """
        天梯竞技场最高排名奖励映射
        :return:
        """
        if not self.arena_once_reward_mapping:
            for i, j in self.arena_once_reward.iteritems():
                rank = j['rank']
                self.arena_once_reward_mapping[rank] = i

        return self.arena_once_reward_mapping

    def get_darkstreet_milestone_mapping(self):
        """
        段位id映射，战斗次数-段位id
        :return:
        """
        if not self.darkstreet_milestone_mapping:
            for i, j in self.darkstreet_milestone.iteritems():
                times = j['times']
                if times not in self.darkstreet_milestone_mapping:
                    self.darkstreet_milestone_mapping[times] = i

        return self.darkstreet_milestone_mapping

    def get_gift_show_mapping(self, version):
        """
        每日礼包活动映射
        :param version:
        :return:
        """
        if not self.gift_show_mapping:
            for i, j in self.gift_show.iteritems():
                v = j['version']
                if v not in self.gift_show_mapping:
                    self.gift_show_mapping[v] = {}
                self.gift_show_mapping[v][i] = j

        return self.gift_show_mapping.get(version, {})

    def get_buy_reward_mapping(self, show_id):
        """
        每日礼包奖励活动映射
        :param show_id:
        :return:
        """
        if not self.buy_reward_mapping:
            for i, j in self.buy_reward.iteritems():
                s_id = j['show_id']
                if s_id not in self.buy_reward_mapping:
                    self.buy_reward_mapping[s_id] = []
                self.buy_reward_mapping[s_id].append(i)

        return self.buy_reward_mapping.get(show_id, [])

    def get_super_rich_mapping(self, version):
        """
        宇宙最强排名奖励映射
        :param version:
        :return:
        """
        if not self.super_rich_mapping:
            for i, j in self.super_rich.iteritems():
                v = j['version']
                if v not in self.super_rich_mapping:
                    self.super_rich_mapping[v] = {}
                self.super_rich_mapping[v][i] = j

        return self.super_rich_mapping.get(version, {})

    def server_get_gift_show_mapping(self, version):
        """
        每日礼包活动映射
        :param version:
        :return:
        """
        if not self.server_gift_show_mapping:
            for i, j in self.server_gift_show.iteritems():
                v = j['version']
                if v not in self.server_gift_show_mapping:
                    self.server_gift_show_mapping[v] = {}
                self.server_gift_show_mapping[v][i] = j

        return self.server_gift_show_mapping.get(version, {})

    def server_get_buy_reward_mapping(self, show_id):
        """
        每日礼包奖励活动映射
        :param show_id:
        :return:
        """
        if not self.server_buy_reward_mapping:
            for i, j in self.server_buy_reward.iteritems():
                s_id = j['show_id']
                if s_id not in self.server_buy_reward_mapping:
                    self.server_buy_reward_mapping[s_id] = []
                self.server_buy_reward_mapping[s_id].append(i)

        return self.server_buy_reward_mapping.get(show_id, [])

    def get_coin_gacha_mapping(self):
        """
        金币抽卡配置处理
        :return: {
            'weight1': {        # 字段名
                1: [[1,2]],     # 等级: [id, 权重]
            },
            'weight2': {        # 字段名
                1: {            # 序号
                    1: [[1,2]], # 等级: [id, 权重]
                },
            },
        }
        """
        if not self.coin_gacha_mapping:
            for i, j in self.coin_gacha.iteritems():
                unlock_lvl = j['unlock_lvl']
                for m, n in j.iteritems():
                    if not m.startswith('weight'):
                        continue
                    if isinstance(n, int):
                        if not n:
                            continue
                        if m not in self.coin_gacha_mapping:
                            self.coin_gacha_mapping[m] = {}
                        if unlock_lvl not in self.coin_gacha_mapping[m]:
                            self.coin_gacha_mapping[m][unlock_lvl] = []
                        self.coin_gacha_mapping[m][unlock_lvl].append([i, n])
                    elif isinstance(n, dict):
                        for a, b in n.iteritems():
                            if not b:
                                continue
                            if m not in self.coin_gacha_mapping:
                                self.coin_gacha_mapping[m] = {}
                            if a not in self.coin_gacha_mapping[m]:
                                self.coin_gacha_mapping[m][a] = {}
                            if unlock_lvl not in self.coin_gacha_mapping[m][a]:
                                self.coin_gacha_mapping[m][a][unlock_lvl] = []
                            self.coin_gacha_mapping[m][a][unlock_lvl].append([i, b])

        return self.coin_gacha_mapping

    def get_diamond_gacha_mapping(self):
        """
        钻石抽卡配置处理
        :return: {
            'weight1': {        # 字段名
                1: [[1,2]],     # 等级: [id, 权重]
            },
            'weight2': {        # 字段名
                1: {            # 序号
                    1: [[1,2]], # 等级: [id, 权重]
                },
            },
        }
        """
        if not self.diamond_gacha_mapping:
            for i, j in self.diamond_gacha.iteritems():
                unlock_lvl = j['unlock_lvl']
                group = j.get('group', 0)
                if group not in self.diamond_gacha_mapping:
                    gacha_mapping = self.diamond_gacha_mapping.setdefault(group, {})

                for m, n in j.iteritems():
                    if not m.startswith('weight_'):
                        continue
                    if isinstance(n, int):
                        if not n:
                            continue
                        if m not in gacha_mapping:
                            gacha_mapping[m] = {}
                        if unlock_lvl not in gacha_mapping[m]:
                            gacha_mapping[m][unlock_lvl] = []
                        gacha_mapping[m][unlock_lvl].append([i, n])
                    elif isinstance(n, dict):
                        for a, b in n.iteritems():
                            if not b:
                                continue
                            if m not in gacha_mapping:
                                gacha_mapping[m] = {}
                            if a not in gacha_mapping[m]:
                                gacha_mapping[m][a] = {}
                            if unlock_lvl not in gacha_mapping[m][a]:
                                gacha_mapping[m][a][unlock_lvl] = []
                            gacha_mapping[m][a][unlock_lvl].append([i, b])

        return self.diamond_gacha_mapping

    def limit_hero_gacha_mapping(self):
        """
        限时英雄抽卡配置处理
        :return: {
            'weight1': {        # 字段名
                1: [[1,2]],     # 等级: [id, 权重]
            },
            'weight2': {        # 字段名
                1: {            # 序号
                    1: [[1,2]], # 等级: [id, 权重]
                },
            },
        }
        """
        if not self.limit_hero_mapping:
            for i, j in self.limit_diamond_gacha.iteritems():
                unlock_lvl = j['unlock_lvl']
                for m, n in j.iteritems():
                    if not m.startswith('weight_'):
                        continue
                    if isinstance(n, int):
                        if not n:
                            continue
                        if m not in self.limit_hero_mapping:
                            self.limit_hero_mapping[m] = {}
                        if unlock_lvl not in self.limit_hero_mapping[m]:
                            self.limit_hero_mapping[m][unlock_lvl] = []
                        self.limit_hero_mapping[m][unlock_lvl].append([i, n])
                    elif isinstance(n, dict):
                        for a, b in n.iteritems():
                            if not b:
                                continue
                            if m not in self.limit_hero_mapping:
                                self.limit_hero_mapping[m] = {}
                            if a not in self.limit_hero_mapping[m]:
                                self.limit_hero_mapping[m][a] = {}
                            if unlock_lvl not in self.limit_hero_mapping[m][a]:
                                self.limit_hero_mapping[m][a][unlock_lvl] = []
                            self.limit_hero_mapping[m][a][unlock_lvl].append([i, b])

        return self.limit_hero_mapping

    def server_limit_hero_gacha_mapping(self):
        """
        限时英雄抽卡配置处理
        :return: {
            'weight1': {        # 字段名
                1: [[1,2]],     # 等级: [id, 权重]
            },
            'weight2': {        # 字段名
                1: {            # 序号
                    1: [[1,2]], # 等级: [id, 权重]
                },
            },
        }
        """
        if not self.server_limit_hero_mapping:
            for i, j in self.server_limit_diamond_gacha.iteritems():
                unlock_lvl = j['unlock_lvl']
                for m, n in j.iteritems():
                    if not m.startswith('weight_'):
                        continue
                    if isinstance(n, int):
                        if not n:
                            continue
                        if m not in self.server_limit_hero_mapping:
                            self.server_limit_hero_mapping[m] = {}
                        if unlock_lvl not in self.server_limit_hero_mapping[m]:
                            self.server_limit_hero_mapping[m][unlock_lvl] = []
                        self.server_limit_hero_mapping[m][unlock_lvl].append([i, n])
                    elif isinstance(n, dict):
                        for a, b in n.iteritems():
                            if not b:
                                continue
                            if m not in self.server_limit_hero_mapping:
                                self.server_limit_hero_mapping[m] = {}
                            if a not in self.server_limit_hero_mapping[m]:
                                self.server_limit_hero_mapping[m][a] = {}
                            if unlock_lvl not in self.server_limit_hero_mapping[m][a]:
                                self.server_limit_hero_mapping[m][a][unlock_lvl] = []
                            self.server_limit_hero_mapping[m][a][unlock_lvl].append([i, b])

        return self.server_limit_hero_mapping

    def get_box_gacha_mapping(self):
        """
        钻石抽卡配置处理
        :return: {
            'weight1': {        # 字段名
                1: [[1,2]],     # 等级: [id, 权重]
            },
            'weight2': {        # 字段名
                1: {            # 序号
                    1: [[1,2]], # 等级: [id, 权重]
                },
            },
        }
        """
        if not self.box_gacha_mapping:
            for i, j in self.box_gacha.iteritems():
                unlock_lvl = j['unlock_lvl']
                for m, n in j.iteritems():
                    if not m.startswith('weight_'):
                        continue
                    if isinstance(n, int):
                        if not n:
                            continue
                        if m not in self.box_gacha_mapping:
                            self.box_gacha_mapping[m] = {}
                        if unlock_lvl not in self.box_gacha_mapping[m]:
                            self.box_gacha_mapping[m][unlock_lvl] = []
                        self.box_gacha_mapping[m][unlock_lvl].append([i, n])
                    elif isinstance(n, dict):
                        for a, b in n.iteritems():
                            if not b:
                                continue
                            if m not in self.box_gacha_mapping:
                                self.box_gacha_mapping[m] = {}
                            if a not in self.box_gacha_mapping[m]:
                                self.box_gacha_mapping[m][a] = {}
                            if unlock_lvl not in self.box_gacha_mapping[m][a]:
                                self.box_gacha_mapping[m][a][unlock_lvl] = []
                            self.box_gacha_mapping[m][a][unlock_lvl].append([i, b])

        return self.box_gacha_mapping

    def get_diamond_gacha_score_mapping(self):
        """
        钻石抽卡奖励组映射
        :return:
        """
        if not self.diamond_gacha_score_mapping:
            for i, j in self.diamond_gacha_score.iteritems():
                group = j['group']
                if group not in self.diamond_gacha_score_mapping:
                    self.diamond_gacha_score_mapping[group] = []
                self.diamond_gacha_score_mapping[group].append(i)

        return self.diamond_gacha_score_mapping

    def get_box_gacha_score_mapping(self):
        """
        觉醒宝箱奖励组映射
        :return:
        """
        if not self.box_gacha_score_mapping:
            for i, j in self.box_gacha_score.iteritems():
                group = j['group']
                if group not in self.box_gacha_score_mapping:
                    self.box_gacha_score_mapping[group] = []
                self.box_gacha_score_mapping[group].append(i)

        return self.box_gacha_score_mapping

    def get_charge_ios_mapping(self):
        """
        ios充值映射
        :return:
        """
        if not self.charge_ios_mapping:
            for i, j in self.charge_ios.iteritems():
                if j['goods_id'] not in self.charge_ios_mapping:
                    self.charge_ios_mapping[j['goods_id']] = i

        return self.charge_ios_mapping

    def get_language_config(self, lan):
        """
        根据语言获取语言配置
        :param lan:
        :return:
        """
        if not self.language_config_mapping.get(lan):
            if lan not in self.language_config_mapping:
                self.language_config_mapping[lan] = {}
            a = getattr(self, 'ZH_%s' % lan, {})
            b = getattr(self, 'ZH_%s_YUNYING' % lan, {})
            self.language_config_mapping[lan].update(a)
            self.language_config_mapping[lan].update(b)

        return self.language_config_mapping[lan]

    def all_equip_item_exp(self):
        """
        装备经验道具映射
        :return:
        """
        if not self.all_equip_item_exp_mapping:
            self.all_equip_item_exp_mapping = {2: {}, 6: {}, 7: {}}  # 两种特殊装备需要不同的材料升级
            for k, v in self.use_item.iteritems():
                if v['is_use'] == 9:
                    self.all_equip_item_exp_mapping[6][k] = v['use_effect']
                    self.all_equip_item_exp_mapping[7][k] = v['use_effect']
                if v['is_use'] == 10:
                    self.all_equip_item_exp_mapping[2][k] = v['use_effect']
        return self.all_equip_item_exp_mapping

    def get_chapter_mapping(self):
        if not self.chapter_mapping:
            for i, j in self.chapter.iteritems():
                if j['num'] not in self.chapter_mapping:
                    self.chapter_mapping[j['num']] = {}
                j['chapter_id'] = i
                self.chapter_mapping[j['num']][j['hard_type']] = j
        return self.chapter_mapping

    def get_shop_config(self, shop_id):
        config = self.shop_goods
        shop_config = {}
        for good_id, value in config.iteritems():
            if value['shop_id'] == shop_id:
                shop_config[good_id] = value
        return shop_config

    def get_book_mapping(self, type='card_book'):
        if not self.book_mapping.get(type):
            self.book_mapping[type] = {}
            for i, j in getattr(self, type, {}).iteritems():
                for card in j.get(type.split('_')[0]):
                    self.book_mapping[type][card] = i
        return self.book_mapping[type]

    def get_phone_chapter_dialogue_mapping(self):
        if not self.phone_chapter_dialogue_mapping:
            for i, j in self.phone_chapter_dialogue.iteritems():
                if j['hero_id'] not in self.phone_chapter_dialogue_mapping:
                    self.phone_chapter_dialogue_mapping[j['hero_id']] = {}
                self.phone_chapter_dialogue_mapping[j['hero_id']][j['chapter_id']] = {'dialogue_id': j['dialogue_id']}
                self.phone_chapter_dialogue_mapping[j['hero_id']][j['chapter_id']]['id'] = i
        return self.phone_chapter_dialogue_mapping



class GameConfig(GameConfigMixIn):
    __metaclass__ = Singleton

    IGONE_NAME = ('keys', 'locked', 'ver_md5')

    def __init__(self):
        super(GameConfig, self).__init__()
        self.locked = True
        self.keys = []
        self.ver_md5 = ''
        self.versions = {}
        self.reload()
        self.locked = False

    def __getattribute__(self, name):
        """ 获取属性

        :param name:
        :return:
        """
        try:
            value = GameConfigMixIn.__getattribute__(self, name)
        except AttributeError:
            front_game_config = FrontGameConfig()
            value = GameConfigMixIn.__getattribute__(front_game_config, name)
        if isinstance(value, types.MethodType):
            return value

        keys = GameConfigMixIn.__getattribute__(self, 'keys')
        if name not in keys and not GameConfigMixIn.__getattribute__(self, 'locked') and \
                        name not in GameConfigMixIn.__getattribute__(self, 'IGONE_NAME'):
            keys.append(name)
        return value

    def reload(self):
        """ 更新进程配置

        :return:
        """
        self.locked = True
        cm = ConfigMd5.get()
        if cm.ver_md5 == self.ver_md5:
            self.locked = False
            return False

        cv = ConfigVersion.get()
        if cv.versions and cv.versions == self.versions:
            self.locked = False
            return False
        # print 'reload'
        cv_save = False
        for name, v in back_mapping_config.iteritems():
            if name in FAKE_CONFIG:
                for i in FAKE_CONFIG[name][1]:
                    r_name = i
                    r_version = cv.versions.get(r_name)
                    c = FrontConfig.get(r_name)
                    if v[0]:  # 加载的策划配置的xlsx
                        # print 'reload: %s' % name
                        setattr(self, r_name, c.value)
                        self.versions[r_name] = r_version if r_version else ''
            cv_version = cv.versions.get(name)
            if cv_version and self.versions.get(name) == cv_version:
                continue

            c = Config.get(name)
            if cv_version and c.version != cv_version:
                if settings.BACK_CONFIG_SWITCH:
                    cv.versions[name] = c.version
                    cv_save = True
                    # continue

            if v[0]:  # 加载的策划配置的xlsx
                # print 'reload: %s' % name
                setattr(self, name, make_readonly(c.value))

                if cv_version:  # 设置服务器配置版本号
                    self.versions[name] = cv_version
            elif cv_version:  # 不是策划配置的xlsx, 服务器自己使用的配置存储在Config中
                # print 'reload: %s' % name
                setattr(self, name, make_readonly(c.value))

                # 设置服务器配置版本号
                self.versions[name] = cv_version

        if cv_save:
            cv.save()
        self.ver_md5 = cm.ver_md5
        self.reset()
        self.locked = False
        return True

    def upload(self, file_name, xl=None):
        """ 上传一个文件

        :param file_name:
        :param xl:
        :return:
        """
        self.locked = True
        save_list = []
        warning_msg = []
        data = trans_config(file_name, 'back', xl)
        if not data:
            self.locked = False
            return save_list, []

        cv = ConfigVersion.get()
        for config_name, m, config in data:
            # pop掉警告信息
            check_warning = config.pop('check_warning', [])
            if check_warning:
                warning_msg += check_warning
            if cv.versions.get(config_name) == m:
                continue
            c = Config.get(config_name)
            c.update_config(config, m, save=True)
            cv.update_version(config_name, m)
            save_list.append(config_name)
            # 生成假配置
            if config_name in FAKE_CONFIG:
                if 1 in FAKE_CONFIG[config_name][2]:
                    fake_config_list = FAKE_CONFIG[config_name][0](config)
                    for one_fake_list in fake_config_list:
                        if len(one_fake_list) != 2:
                            continue
                        md5_value = hashlib.md5(repr(one_fake_list[1])).hexdigest()
                        if cv.versions.get(one_fake_list[0]) == md5_value:
                            continue
                        c = FrontConfig.get(one_fake_list[0])
                        c.update_config(one_fake_list[1], md5_value, save=True)
                        cv.update_version(one_fake_list[0], md5_value)
                        save_list.append(one_fake_list[0])

        if save_list:
            cv.save()
        self.locked = False
        return save_list, warning_msg

    def refresh(self):
        """ 刷新配置，用于进程加载配置

        :return:
        """
        if not settings.BACK_CONFIG_SWITCH:
            return False

        self.locked = True
        cv = ConfigVersion.get()
        cm = ConfigMd5.get()
        ver_md5 = cm.generate_md5(cv.versions)
        if ver_md5 == cm.ver_md5:
            self.locked = False
            return False

        cm.update_md5(cv.versions, gen_md5=ver_md5, save=True)
        self.locked = False
        return True


class FrontGameConfig(GameConfigMixIn):
    __metaclass__ = Singleton

    def __init__(self):
        super(FrontGameConfig, self).__init__()
        self.locked = True
        self.keys = []
        self.ver_md5 = ''
        self.versions = {}
        self.reload()
        self.locked = False

    def reload(self):
        """ 更新进程配置

        :return:
        """
        self.locked = True
        cm = FrontConfigMd5.get()
        if cm.ver_md5 == self.ver_md5:
            self.locked = False
            return False

        cv = FrontConfigVersion.get()
        if cv.versions and cv.versions == self.versions:
            self.locked = False
            return False
        # print 'reload'
        cv_save = False
        for name, v in front_mapping_config.iteritems():
            if name in RESOLVE_LIST:
                for i in xrange(0, RESOLVE_LIST[name]):
                    r_name = '%s_%d' % (name, i)
                    r_version = cv.versions.get(r_name)
                    c = FrontConfig.get(r_name)
                    if v[0]:  # 加载的策划配置的xlsx
                        # print 'reload: %s' % name
                        setattr(self, r_name, make_readonly(c.value))
                        self.versions[r_name] = r_version if r_version else ''
            if name in FAKE_CONFIG:
                for i in FAKE_CONFIG[name][1]:
                    r_name = i
                    r_version = cv.versions.get(r_name)
                    c = FrontConfig.get(r_name)
                    if v[0]:  # 加载的策划配置的xlsx
                        # print 'reload: %s' % name
                        setattr(self, r_name, make_readonly(c.value))
                        self.versions[r_name] = r_version if r_version else ''

            cv_version = cv.versions.get(name)
            if cv_version and self.versions.get(name) == cv_version:
                continue

            c = FrontConfig.get(name)
            if cv_version and c.version != cv_version:
                if settings.FRONT_CONFIG_SWITCH:
                    cv.versions[name] = c.version
                    cv_save = True
                    # continue

            if v[0]:  # 加载的策划配置的xlsx
                # print 'reload: %s' % name
                setattr(self, name, make_readonly(c.value))

                if v[1]:  # 前端可见配置
                    self.versions[name] = cv_version if cv_version else ''

            elif cv_version:  # 不是策划配置的xlsx, 服务器自己使用的配置存储在Config中
                # print 'reload: %s' % name
                setattr(self, name, make_readonly(c.value))

                if v[1]:  # 前端可见配置
                    self.versions[name] = cv_version if cv_version else ''

            else:  # 不是策划配置的xlsx, 服务器自己使用的配置, 在gconfig.model属性中, 每次更改需要重启服务器
                if v[1]:  # 前端可见配置
                    config = getattr(self, name, '')
                    cv_version = cm.generate_custom_md5(config)
                    self.versions[name] = cv_version if cv_version else ''

        if cv_save:
            cv.save()
        self.ver_md5 = cm.ver_md5
        self.reset()
        self.locked = False
        return True

    def upload(self, file_name, xl=None):
        """ 上传一个文件

        :param file_name:
        :param xl:
        :return:
        """
        self.locked = True
        save_list = []
        save_file_data = []
        warning_msg = []
        data = trans_config(file_name, 'front', xl)
        if not data:
            self.locked = False
            return save_list, save_file_data, []

        cv = FrontConfigVersion.get()
        for config_name, m, config in data:
            # pop掉警告信息
            check_warning = config.pop('check_warning', [])
            if check_warning:
                warning_msg += check_warning
            # 生成假配置
            if config_name in FAKE_CONFIG:
                if 2 in FAKE_CONFIG[config_name][2]:
                    fake_config_list = FAKE_CONFIG[config_name][0](config)
                    for one_fake_list in fake_config_list:
                        if len(one_fake_list) != 2:
                            continue
                        md5_value = hashlib.md5(repr(one_fake_list[1])).hexdigest()
                        if cv.versions.get(one_fake_list[0]) == md5_value:
                            continue
                        c = FrontConfig.get(one_fake_list[0])
                        c.update_config(one_fake_list[1], md5_value, save=True)
                        cv.update_version(one_fake_list[0], md5_value)
                        save_list.append(one_fake_list[0])
                        save_file_data.append((one_fake_list[0], md5_value, one_fake_list[1]))

            # 拆分表
            if config_name in RESOLVE_LIST:
                r = {}
                for k, v in config.iteritems():
                    key = '%s_%d' % (config_name, (int(k) / 10000) % RESOLVE_LIST[config_name])
                    if key not in r:
                        r[key] = {k: v}
                    else:
                        r[key][k] = v
                for k, v in r.iteritems():
                    md5_value = hashlib.md5(repr(v)).hexdigest()
                    if cv.versions.get(k) == md5_value:
                        continue
                    c = FrontConfig.get(k)
                    c.update_config(v, md5_value, save=True)
                    cv.update_version(k, md5_value)
                    save_list.append(k)
                    save_file_data.append((k, md5_value, v))

            if cv.versions.get(config_name) == m:
                continue
            c = FrontConfig.get(config_name)
            c.update_config(config, m, save=True)
            cv.update_version(config_name, m)
            save_list.append(config_name)
            save_file_data.append((config_name, m, config))

        if save_list:
            cv.save()
        self.locked = False

        # 配置cdn文件
        if settings.CONFIG_RESOURCE_OPEN:
            for config_name, m, config in save_file_data:
                filename = '%s%s_%s.json' % (settings.CONFIG_RESOURCE_PATH, config_name, m)
                with open(filename, 'wb+') as f:
                    r = json.dumps(config, ensure_ascii=False, separators=(',', ':'), encoding='utf-8', default=to_json)
                    f.write(r)

        return save_list, save_file_data, check_warning

    def refresh(self):
        """ 刷新配置，用于进程加载配置

        :return:
        """
        if not settings.FRONT_CONFIG_SWITCH:
            return False

        self.locked = True
        cv = FrontConfigVersion.get()
        cm = FrontConfigMd5.get()
        ver_md5 = cm.generate_md5(cv.versions)
        if ver_md5 == cm.ver_md5:
            self.locked = False
            return False

        cm.update_md5(cv.versions, gen_md5=ver_md5, save=True)
        self.locked = False
        return True
