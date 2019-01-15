# -*- coding: utf-8 –*-

"""
Created on 2018-12-03

@author: sm
"""

import math
import random
import bisect
import itertools

from gconfig import game_config
from lib.core.environ import ModelManager

from lib.utils import weight_choice
from tools.gift import add_mult_gift


class KingOfSongLogics(object):
    def __init__(self, mm):
        self.mm = mm

    def is_robot(self, uid):
        return 'robot' in uid

    def index(self):
        king = self.mm.king_of_song
        data = {
            'version': '',
            'battle_times': king.battle_times,
            'left_times': king.left_battle_times(),
            'buy_times': king.buy_times,
            'enemy': king.enemy,
            'script_pool': king.script_pool,

            'enemy_fight_data': king.enemy_fight_data,
            'star': king.star,
            'rank': king.rank,
            'continue_win_times': king.continue_win_times,
        }
        return 0, data

    def enemy_battle(self, target_uid):
        """对手拍片

        :param target_uid:
        :return:
        """
        king = self.mm.king_of_song
        if king.enemy_fight_data:
            return 1, {}        # 对手已经拍完

        if target_uid not in king.enemy:
            return 2, {}        # 不是可选对手

        is_robot = self.is_robot(target_uid)
        if is_robot:
            enemy_mm = None
        else:
            enemy_mm = ModelManager(target_uid)

        enemy_info = king.enemy[target_uid]
        cards = enemy_info['cards']
        script_id = enemy_info['script_id']
        script_config = game_config.script[script_id]

        enemy_align = enemy_info.get('align') or zip(script_config['role_id'], cards)

        enemy_fight_data = self.do_fight(enemy_mm, enemy_info['script_id'], enemy_align, cards)
        king.enemy_fight_data = {
            'enemy_fight_data': enemy_fight_data,
            'enemy_uid': target_uid,
        }
        king.save()
        return 0, {
            'enemy_fight_data': enemy_fight_data,
            'enemy': {
                target_uid: king.enemy[target_uid]
            }
        }

    def battle(self, script_id, role_card):
        """

        :param align:
        :param role_card:  [(role, card_id), (role, card_id)]
        :return:
        """
        align = dict(role_card)
        king = self.mm.king_of_song
        if not king.left_battle_times() > 0:
            return 1, {}        # 挑战次数不足

        if script_id not in king.script_pool:
            return 2, {'script_pool': king.script_pool}        # 所选剧本不存在

        if not king.enemy_fight_data:
            return 3, {}        # 对手还未拍片

        data = {}

        fight_data = self.do_fight(self.mm, script_id, align, self.mm.card.cards, is_enemy=False)
        enemy_fight_data = king.enemy_fight_data.get('enemy_fight_data')
        enemy_uid = king.enemy_fight_data.get('enemy_uid')

        data['gift'] = []
        data['self_fight_data'] = fight_data
        data['enemy_fight_data'] = enemy_fight_data
        data['enemy'] = {enemy_uid: king.enemy[enemy_uid]}

        # 我方总评分：
        # 如果分差>=1且<=1.2,RANDBETWEEN(我方最低+1,我方最高)，
        # 否则，RANDBETWEEN(我方最低,我方最高)

        # 敌方总评分：
        # 如果分差>=1,则RANDBETWEEN(敌方最低，min（我方评分-1，敌方最高）
        # 否则，RANDBETWEEN(敌方最低，敌方最高）

        # 分差 = 我方输出结果/敌方输出结果
        score_rate = fight_data['all_score'] * 100.0 / enemy_fight_data['all_score']

        # 评分计算
        sorted_rate = sorted(game_config.singerking_rate.iteritems(), key=lambda x: x[0])
        idx = bisect.bisect_left([i[0] for i in sorted_rate], score_rate)
        if idx >= len(sorted_rate):
            idx = -1
        rate_config = sorted_rate[idx][1]

        # 我方总评分
        if 100 <= score_rate <= 120:
            myscore_min = rate_config['myscore_min'] + 1
        else:
            myscore_min = rate_config['myscore_min']
        self_rating = random.randint(myscore_min, rate_config['myscore_max'])

        # 敌方总评分
        if score_rate >= 1:
            left, right = rate_config['enemyscore_min'], min(self_rating - 1, rate_config['enemyscore_max'])
            enemy_rating = random.randint(*sorted([left, right]))
        else:
            enemy_rating = random.randint(rate_config['enemyscore_min'], rate_config['enemyscore_max'])

        data['self_judge_rating'] = self.get_judge_rating(self_rating)
        data['enemy_judge_rating'] = self.get_judge_rating(enemy_rating)
        is_win = data['win'] = self_rating >= enemy_rating

        rank_config = game_config.pvp_rank[king.rank]
        old_rank = king.rank
        if is_win:
            rank_up = king.add_star()
            gift = add_mult_gift(self.mm, rank_config['award_win'])
            data['rank_up'] = rank_up
        else:
            rank_down = king.deduct_star()
            gift = add_mult_gift(self.mm, rank_config['award_lose'])
            data['rank_down'] = rank_down

        data['gift'] = gift
        data['rank'] = king.rank
        data['old_rank'] = old_rank
        data['continue_win_times'] = king.continue_win_times

        king.enemy_fight_data.clear()
        king.refresh_scripts()
        king.refresh_enemy()
        king.save()
        return 0, data

    @staticmethod
    def get_judge_rating(all_score):
        """
        评委评分
        :param all_score:
        :param is_enemy:
        :return:
        """
        # 已知总评分求评委分数（无论敌我评分均使用此规则）
        # 评委1：向下取整（评委评分/3）
        # 评委2：如果总评分-评委1-1>=10,RANDBETWEEN(总评分-评委1-10,10)
        #   否则，RANDBETWEEN(1，总评分-评委1-1）
        # 评委3：总评分-评委1-评委2
        # 输出时，三个评委顺序随机打乱一下

        s1 = all_score / 3
        if all_score - s1 - 1 >= 10:
            s2 = random.randint(*sorted([all_score - s1 - 10, 10]))
        else:
            s2 = random.randint(1, all_score - s1 - 1)
        s3 = all_score - s1 - s2

        rating = [s1, s2, s3]
        # print rating
        random.shuffle(rating)
        return [i for i in rating]

    def get_reward(self, script_id):
        return {}

    def do_fight(self, mm, script_id, align, cards_info, is_enemy=True):
        """

        :param mm:
        :param script_id:
        :param align:       [(role_id, card_oid), (rold_id, card_oid)]
        :param cards_info:
        :param is_enemy:
        :return:
        """
        data = {}
        tag_score = {}
        all_pro = 0
        script_config = game_config.script[script_id]
        style = script_config['style']

        if isinstance(align, dict):
            align = [(k, v) for k, v in align.items()]

        # 角色、剧本得分
        for role_id, card_id in align:
            card_info = self.mm.card.calc_card_battle_info(cards_info[card_id])
            # 计算擅长角色，擅长剧本得分
            score = self.tag_score(script_id, role_id, card_info)
            tag_score[card_id] = score
            all_pro += cards_info[card_id].get('style_pro').get(style, {}).get('lv', 0)

        # 拍片演员得分
        fight_data = {}
        rounds = game_config.common.get(23, 2)
        all_score = 0
        for round_num in range(1, rounds + 1):
            if round_num not in fight_data:
                fight_data[round_num] = {}
            for role_id, card_id in align:
                card_info = self.mm.card.calc_card_battle_info(cards_info[card_id])
                # 助战卡牌
                # if role_id in chapter_enemy:
                #     # 卡牌两个必触发属性伤害
                #     attr = game_config.script_role[role_id]['role_attr']
                #     hurts = {'more_attr': {},
                #              'attr': {}}
                #     for attr_id in attr:
                #         hurt = self.get_hurt(attr_id, card_info, tag_score[card_id], is_enemy=True)
                #         hurts['attr'][attr_id] = hurt
                #         all_score += hurt[0]
                #     fight_data[round_num][card_id] = hurts
                #     # 概率触发属性伤害
                #     hurts['more_attr'] = {}
                #     # config = game_config.chapter_enemy[int(card_id)]
                #     # rate = config['ex_special_rate']
                #     # rate_ = random.randint(1, 10001) <= rate
                #     # if rate_:
                #     #     more_attr = config['special_quality']
                #     #     more_attr = weight_choice(more_attr)
                #     #     hurt = self.get_hurt(more_attr[0], card_id, tag_score[card_id], is_enemy=True)
                #     #     hurts['more_attr'][more_attr[0]] = hurt
                #     #     all_score += hurt[0]
                #     fight_data[round_num][card_id] = hurts
                #     continue

                # 卡牌两个必触发属性伤害
                attr = game_config.script_role[role_id]['role_attr']
                hurts = {'more_attr': {},
                         'attr': {}}
                for attr_id in attr:
                    hurt = self.get_hurt(attr_id, card_info, tag_score[card_id])
                    all_score += hurt[0]
                    hurts['attr'][attr_id] = hurt
                fight_data[round_num][card_id] = hurts
                # 概率触发属性伤害 special_rate2 5娱乐 special_rate1 6艺术
                config = game_config.card_basis[card_info['id']]
                rate = config['ex_special_rate']
                rate_ = random.randint(1, 10001) <= rate
                if rate_:
                    more_attr = config['special_quality']
                    more_attr = weight_choice(more_attr)
                    hurt = self.get_hurt(more_attr[0], card_info, tag_score[card_id])
                    hurts['more_attr'][more_attr[0]] = hurt
                    all_score += hurt[0]
                else:
                    hurts['more_attr'] = {}
                fight_data[round_num][card_id] = hurts

        m = game_config.common[10]
        all_score = int(all_score * (1 + all_pro * 1.0 / m))
        score_config = script_config['stage_score']
        star = self.get_star(all_score, score_config)
        return {
            'star': star,
            'all_score': all_score,
            'fight_data': fight_data,
            'tag_score': tag_score,
        }

    def tag_score(self, script_id, role_id, card_info):
        score = 0
        card_tag = self.mm.card.card_tag(card_info)

        tag_role = game_config.script_role[role_id]['tag_role']
        script_config = game_config.script[script_id]
        tag_script = script_config['tag_script']
        for tag in tag_role:
            if tag in card_tag['tag_role']:
                tag_num = card_tag['tag_role'][tag]
                score += game_config.tag_score.get(tag_num, {}).get('score', 0)
        for tag in tag_script:
            if tag in card_tag['tag_script']:
                tag_num = card_tag['tag_script'][tag]
                score += game_config.tag_score.get(tag_num, {}).get('score', 0)
        return score

    def get_hurt(self, attr_id, card_info, score, is_enemy=False):
        is_crit = False

        v = card_info['char_pro'][attr_id - 1]
        # 计算普通
        love_lv = card_info.get('love_lv', 0)
        rate = game_config.card_love_level[love_lv]['dps_rate']
        dps_rate = random.randint(rate[0], rate[1]) / 10000.0
        hurt = max(int(v * dps_rate), 1)
        # 是否暴击
        if self.is_crit(card_info, score, is_enemy=is_enemy):
            # 暴击伤害
            hurt = self.crit_hurt(hurt, score)
            is_crit = True
        return [hurt, is_crit]

    def crit_hurt(self, hurt, score):
        crit = 1.1 + score / 100.0
        hurt = int(hurt * crit)
        return hurt

    def is_crit(self, card_info, score, is_enemy=False):
        crit_rate_base = game_config.card_basis[card_info['id']]['crit_rate_base']
        crit_rate = crit_rate_base + score / 100
        return crit_rate > random.randint(1, 10000)

    def get_star(self, all_score, score_config):
        return random.randint(1, 3)

        for level, score in enumerate(score_config, 1):
            if level == 1 and all_score < score:
                return level
            elif level == len(score_config) and all_score >= score:
                return level
            elif score <= all_score < score_config[level]:
                return level + 1
