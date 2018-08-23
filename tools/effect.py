#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import bisect

from gconfig import game_config
from lib.utils import add_dict, merge_dict
from tools.skill import SkillFactory
# from tools.unlock_build import TEAM_SKILL, HERO_MILESTONE, COMMANDER, POKEDEX


class Effect(object):
    """ 英雄效果加成

    """

    def __init__(self, mm):
        self.mm = mm
        self.cache = {}
        self.cache_skill = {}

    def clear_cache(self):
        """ 清理cache缓存

        :return:
        """
        self.cache.clear()
        self.cache_skill.clear()

    def calc_hero_basis(self, hero_dict, hero_config, mm):
        """
        英雄基础属性计算
        :param hero_dict:
        :param hero_config:
        :return:
        """

        star = hero_dict['star']
        lv = hero_dict['lv']
        is_awaken = hero_dict['is_awaken']
        # grade = hero_config['grade']
        quality = hero_config['quality']
        grade_lv = quality  # 资质
        evo = hero_dict['evo']
        hero_id = hero_dict['id']

        hero_basis_attr = {}
        hero_attribute_config = game_config.hero_attribute

        for attr_id in game_config.hero_basis_init_attr:
            attr = game_config.attr_mapping[attr_id]
            attr_new = '%s%s' % ('lvl_', attr)
            value = hero_attribute_config.get(hero_id, {}).get(attr_new, 0)
            add_dict(hero_basis_attr, attr, value)

        for _type in ['lvl_', 'growth_', 'star_']:
            for attr_id in game_config.base_attr:
                attr = game_config.attr_mapping[attr_id]
                attr_new = '%s%s' % (_type, attr)
                value = hero_attribute_config.get(hero_id, {}).get(attr_new, 0)

                if _type == 'lvl_':
                    hero_lvl_rate = game_config.hero_growth_rate.get(lv, {}).get('hero_lvl_rate', {})
                    lvlup_rate = hero_lvl_rate.get(grade_lv) or hero_lvl_rate[1]
                    value *= lvlup_rate
                elif _type == 'growth_':
                    evo_rate = game_config.grade_lvlup_reward_new.get(evo, {}).get('evo_rate', 1)
                    value *= evo_rate
                elif _type == 'star_':
                    if is_awaken:
                        hero_star_rate = game_config.hero_star_rate.get(star, {}).get('hero_awaken_star', {})
                        star_rate = hero_star_rate.get(grade_lv) or hero_star_rate[1]
                    else:
                        hero_star_rate = game_config.hero_star_rate.get(star, {}).get('hero_star_rate', {})
                        star_rate = hero_star_rate.get(grade_lv) or hero_star_rate[1]
                    value *= star_rate

                if value >= 0:
                    add_dict(hero_basis_attr, attr, value)

        # for attr_id in game_config.hero_basis_init_attr:
        #     attr = game_config.attr_mapping[attr_id]
        #     add_dict(hero_basis_attr, attr, hero_config.get(attr, 0))
        #
        # ## 每次重新计算基础数值
        # if is_awaken:
        #     hero_star_rate = game_config.hero_star_rate.get(star, {}).get('hero_awaken_star', {})
        #     star_rate = hero_star_rate.get(grade_lv) or hero_star_rate[1]
        # else:
        #     hero_star_rate = game_config.hero_star_rate.get(star, {}).get('hero_star_rate', {})
        #     star_rate = hero_star_rate.get(grade_lv) or hero_star_rate[1]
        # hero_lvl_rate = game_config.hero_growth_rate.get(lv, {}).get('hero_lvl_rate', {})
        # lvlup_rate = hero_lvl_rate.get(grade_lv) or hero_lvl_rate[1]
        # for attr_id in game_config.base_attr:
        #     attr = game_config.attr_mapping[attr_id]
        #     # 基础数值*升级系数*升星系数
        #     value = hero_config[attr] * lvlup_rate * star_rate
        #     add_dict(hero_basis_attr, attr, value)
        #
        # ## 英雄进阶
        # evo = hero_dict['evo']
        # job = hero_config['job']
        # grade = hero_config['quality']
        # for i in xrange(1, evo):
        #     effect_value = game_config.grade_lvlup_reward.get(job, {}).get(grade, {}).get(i, {})
        #     # effect_value = game_config.grade_lvlup_reward_new.get(i, {})
        #     for attr, attr_value in effect_value.iteritems():
        #         add_dict(hero_basis_attr, attr, attr_value)

        # 星座之力属性
        if self.mm:
            for i in mm.star_array.own_log:
                config = game_config.star_array.get(i)
                if not config:
                    continue
                attr = config['attr']
                attr_name = game_config.attr_mapping.get(attr)
                if not attr_name:
                    continue
                add_dict(hero_basis_attr, attr_name, config['value'])

        # 计算英雄特性加成属性
        hero_character_config = game_config.hero_character
        for cid in hero_config.get('character', []):
            config = hero_character_config.get(cid)
            if not config or config['type'] != 1:
                continue
            attr = config['property']
            value = config['value']
            attr_name = game_config.attr_mapping.get(attr)
            if not attr_name:
                continue
            add_dict(hero_dict, attr_name, value)

        hero_effect = hero_dict.setdefault('effect', {})
        hero_effect['hero'] = hero_basis_attr

    def get_hero(self, hero_oid, h_dict=None, for_battle=False, battle_sort=0, favor_team_effect=None):
        """ 获取英雄数据

        :param hero_oid:
        :param h_dict: 英雄数据
        :param for_battle: 是否是战斗
        :return:
        """
        hero_dict = self.cache.get(hero_oid)
        if hero_dict is None:
            # 获取卡牌属性
            hero_dict = h_dict if h_dict else self.mm.hero.get_hero(hero_oid)
            if not hero_dict:
                return hero_dict
            hero_config = game_config.hero_basis[hero_dict['id']]

            # 清空旧数据
            for i, j in game_config.attr_mapping.iteritems():
                if hero_dict.get(j):
                    hero_dict[j] = 0

            # 英雄基础属性计算
            self.calc_hero_basis(hero_dict, hero_config, self.mm)

            # 其他加成计算
            effect = hero_dict['effect']
            for effect_name, effect_dict in effect.iteritems():
                if effect_name in game_config.bonus_attr:  # 过滤bonus加成的属性，hp,phy_atk,mag_atk,phy_def,mag_def
                    attr_dict = game_config.bonus_attr[effect_name]
                    for attr, value in effect_dict.iteritems():
                        if attr in attr_dict:
                            continue
                        add_dict(hero_dict, attr, value)
                else:  # 其他属性直接求和
                    for attr, value in effect_dict.iteritems():
                        add_dict(hero_dict, attr, value)

            if self.mm and for_battle:
                # 升星被动加成
                star_passive_effect = self.mm.hero.get_star_passive_effect(hero_dict, hero_config)
                for attr, value in star_passive_effect.iteritems():
                    add_dict(hero_dict, attr, value)

                # 同阵营属性加成
                # favor_camp_effect = self.get_favor_camp_effect(hero_config['camp'])
                # for attr, value in favor_camp_effect.iteritems():
                #     add_dict(hero_dict, attr, value)

                # 全队加成
                if favor_team_effect is not None:
                    for attr, value in favor_team_effect.iteritems():
                        add_dict(hero_dict, attr, value)

                # 战斗数据加成
                self.calc_hero_battle_data({hero_dict['oid']: hero_dict}, battle_sort)

            # todo 特殊属性，一条属性对应多条普通属性
            for i, j in game_config.bonus_split.iteritems():
                for k in j:
                    if not hero_dict.get(i):
                        continue
                    hero_dict[k] = hero_dict.get(k, 0) + hero_dict[i]

            # todo 计算公式放在最后
            # hp,phy_atk,mag_atk,phy_def,mag_def加成的属性最后算
            # （英雄生命总和 *（1 + 英雄生命提升）+装备生命总和 *（1 + 装备生命提升）+基因生命总和 *（1 + 基因生命加成）+ (1 + 援护英雄团队加成)） * （1 + 最终生命提升）
            # （英雄普攻总和 *（1 + 英雄普攻提升）+装备普攻总和 *（1 + 装备普攻提升）+基因普攻总和 *（1 + 基因普攻加成）+ (1 + 援护英雄团队加成)） * (1 + 特性普攻)
            # （英雄绝攻总和 *（1 + 英雄绝攻提升）+装备绝攻总和 *（1 + 装备绝攻提升）+基因绝攻总和 *（1 + 基因绝攻加成）+ (1 + 援护英雄团队加成)） * (1 + 特性绝攻)
            # （英雄普防总和 *（1 + 英雄普防提升）+装备普防总和 *（1 + 装备普防提升）+基因普防总和 *（1 + 基因普防加成）+ (1 + 援护英雄团队加成)） * (1 + 特性普防)
            # （英雄绝防总和 *（1 + 英雄绝防提升）+装备绝防总和 *（1 + 装备绝防提升）+基因绝防总和 *（1 + 基因绝防加成）+ (1 + 援护英雄团队加成)） * (1 + 特性绝防)
            for effect_name, attr_dict in game_config.bonus_attr.iteritems():
                effect_dict = effect.get(effect_name, {})
                for attr, value in effect_dict.iteritems():
                    if attr not in attr_dict:
                        continue
                    attr_bonus = attr_dict[attr]
                    add_value = value * (1 + hero_dict.get(attr_bonus, 0) / 100.0)
                    add_dict(hero_dict, attr, add_value)

            # 计算属性公式中最后一步的乘法，如：* （1 + 最终生命提升）。。。
            # hero_dict['hp'] *= 1 + hero_dict.get('final_hp_bonus', 0) / 100.0
            for i, j in game_config.hero_attr_final_bonus.iteritems():
                hero_dict[i] *= 1 + hero_dict.get(j, 0) / 100.0

            # 队长加成
            if self.mm:
                self.mm.role_info.calc_leading_role_effect(hero_dict)

            self.cache[hero_oid] = hero_dict

        return hero_dict

    def merge_attr_effect(self, hero_dict, effect):
        for attr_id, value in effect:
            attr = game_config.attr_mapping.get(attr_id)
            if attr is None:
                continue
            add_dict(hero_dict, attr, value)

    def calc_hero_battle_data(self, hero_datas, battle_sort):
        """
        计算战斗英雄数据加成
        :param hero_datas: {hero_oid: hero_dict}
        :param battle_sort: 战斗sort
        :return:
        """
        sort_mapping = {
            5: 7,  # 血沉拉力赛
            8: 1,  # 黑街
            9: 6,  # 公会战
            10: 5,  # 战队技能副本
            13: 8,  # 金币副本
            15: 9,  # 经验副本
            16: 4,  # 觉醒副本
            17: 3,  # 克隆大作战
            18: 2,  # 竞技场
        }
        # skill_effect = self.mm.biography.get_skill_effect(default={})

        for hero_oid, hero_dict in hero_datas.iteritems():
            # effect = []
            # hero_config = game_config.hero_basis.get(hero_dict['id'])

            # # 在某玩法中，我方英雄提升一项属性
            # effect1 = skill_effect.get(2, {}).get(sort_mapping.get(battle_sort), [])
            # # merge_list_2(effect, effect1)
            # self.merge_attr_effect(hero_dict, effect1)
            #
            # # 所有玩法中，我方某类英雄上阵提升属性
            # gender = hero_config['gender']
            # job = hero_config['job']
            # camp = hero_config['camp']
            # for data, data2 in {1: gender, 2: job, 3: camp}.iteritems():
            #     effect2 = skill_effect.get(3, {}).get(data, {}).get(data2, [])
            #     # merge_list_2(effect, effect2)
            #     self.merge_attr_effect(hero_dict, effect2)
            #
            # # 所有玩法中，该传记英雄提升某项属性
            # father_id = hero_config['father_id']
            # effect3 = skill_effect.get(4, {}).get(father_id, [])
            # # merge_list_2(effect, effect3)
            # self.merge_attr_effect(hero_dict, effect3)
            #
            # # 当前传记中，我方英雄提升属性
            # if battle_sort == 12:
            #     effect4 = skill_effect.get(5, [])
            #     # merge_list_2(effect, effect4)
            #     self.merge_attr_effect(hero_dict, effect4)
            #
            # # 首个回合必然触发小技能
            # effect5 = skill_effect.get(7, {})
            # if father_id in effect5:
            #     hero_dict['first_round_ext'] = True
            #
            # # 首次释放怒气技能消耗减少
            # effect6 = skill_effect.get(8, {}).get(father_id, 0)
            # if effect6:
            #     hero_dict['first_decr_cost_skill'] = effect6

            # 公会科技效果
            guild = self.mm.get_obj_by_id('guild', self.mm.user.guild_id)
            for k, v in game_config.guild_technology.iteritems():
                if v['sort'] == 3:  # 工会战sort为3
                    # 公会战普攻、绝攻加成
                    if battle_sort == 9 and self.mm.user.guild_id:
                        effect7 = guild.get_tech_effect_by_id(k)
                        effect7 = [[v['attr'], effect7]]
                        # merge_list_2(effect, effect7)
                        self.merge_attr_effect(hero_dict, effect7)
                if v['sort'] == 4:  # 公会boss sort为4
                    # 公会boss普攻、绝攻加成
                    if battle_sort == 22 and self.mm.user.guild_id:
                        effect9 = guild.get_tech_effect_by_id(k)
                        effect9 = [[v['attr'], effect9]]
                        # merge_list_2(effect, effect9)
                        self.merge_attr_effect(hero_dict, effect9)
                # if v['sort'] == 5:  # 公会经验副本sort为5
                #     # 公会战普攻、绝攻加成
                #     if battle_sort == 15 and self.mm.user.guild_id:
                #         effect11 = guild.get_tech_effect_by_id(k)
                #         effect11 = [[v['attr'], effect11]]
                #         # merge_list_2(effect, effect11)
                #         self.merge_attr_effect(hero_dict, effect11)

    def get_skill_factory(self, hero_oid, hero_dict=None):
        """ 获取英雄对应的技能factory

        :param hero_oid:
        :param hero_dict:
        :return:
        """
        skill_factory = self.cache_skill.get(hero_oid)
        if skill_factory is None:
            hero_dict = hero_dict or self.get_hero(hero_oid)
            skill_factory = SkillFactory(hero_dict)
            self.cache_skill[hero_oid] = skill_factory

        return skill_factory

    def get_favor_camp_effect(self, camp):
        """
        获得好感度阵营加成
        :param camp:阵营
        :return:
        """
        effect = {}
        for hero_fid, data in self.mm.hero.favor_camp_attr.get(camp, {}).iteritems():
            for sort, value in data:
                attr = game_config.attr_mapping[sort]
                add_dict(effect, attr, value)

        return effect

    def get_favor_team_effect(self, hero_dict):
        effect = {}
        fid = self.mm.hero.get_father_id_by_id(hero_dict['id'])
        team_attrs = game_config.hero_favor.get(fid, {}).get('teamattr_level', [])
        for ek, ev in hero_dict['favor'].get('ex_attr', {}).iteritems():
            if int(ek) * 10 in team_attrs:
                attr = game_config.attr_mapping[ev[0][0]]
                add_dict(effect, attr, ev[0][1])

        return effect
