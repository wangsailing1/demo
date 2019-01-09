# -*- coding: utf-8 –*-

"""
Created on 2018-12-03

@author: sm
"""

import random
import itertools

from gconfig import game_config
from lib.core.environ import ModelManager

from lib.utils import weight_choice


class KingOfSongLogics(object):
    def __init__(self, mm):
        self.mm = mm

    def is_robot(self, uid):
        return 'robot' in uid

    def index(self):
        king = self.mm.king_of_song
        data = {
            'battle_times': king.battle_times,
            'left_times': king.left_battle_times(),
            'buy_times': king.buy_times,
            'enemy': king.enemy,
            'script_pool': king.script_pool,

            'star': king.star,
        }
        return 0, data

    def battle(self, role_card, script_id, target_uid):
        """

        :param align:
        :param role_card:  [(role, card_id), (role, card_id)]
        :return:
        """
        align = dict(role_card)
        king = self.mm.king_of_song
        if not king.left_battle_times() > 0:
            return 1, {}        # 挑战次数不足

        if target_uid not in king.enemy:
            return 2, {}        # 不是可选对手

        is_robot = self.is_robot(target_uid)
        if is_robot:
            enemy_mm = None
        else:
            enemy_mm = ModelManager(target_uid)

        enemy_info = king.enemy[target_uid]

        if script_id not in king.script_pool:
            return 3, {}        # 所选剧本存在

        data = {}
        tag_score = {}
        script_config = game_config.script[script_id]
        enemy_align = enemy_info['cards']

        fight_data = self.do_fight(self.mm, script_id, align)
        enemy_fight_data = self.do_fight(enemy_mm, enemy_info['script_id'], enemy_align)

        data['win'] = fight_data['all_score'] >= enemy_fight_data['all_score']
        data['gift'] = []
        data['self_fight_data'] = fight_data
        data['enemy_fight_data'] = enemy_fight_data
        if not data['win']:
            return 0, data

        gift = self.get_reward(script_id)
        data['gift'] = gift
        return 0, data

        data = {}
        start = random.randint(1, 5)



        #
        # data['win'] = star >= 2
        # data['gift'] = []
        # data['fight_data'] = fight_data
        # data['all_score'] = all_score
        # data['star'] = star
        # data['tag_score'] = tag_score
        # return 0, {}

    def get_reward(self, script_id):
        return {}

    def do_fight(self, mm, script_id, align, is_enemy=True):

        chapter_enemy = align
        data = {}
        tag_score = {}
        all_pro = 0
        script_config = game_config.script[script_id]
        style = script_config['style']

        if isinstance(align, dict):
            align = [(k, v) for k, v in align.items()]

        # 角色、剧本得分
        for role_id, card_id in align:
            # 计算擅长角色，擅长剧本得分
            score = self.tag_score(script_id, role_id, card_id)
            tag_score[card_id] = score
            if mm:
                all_pro += mm.card.get_card(card_id).get('style_pro').get(style, {}).get('lv', 0)
            else:
                all_pro += 0

        # 拍片演员得分
        fight_data = {}
        rounds = game_config.common.get(23, 2)
        all_score = 0
        for round_num in range(1, rounds + 1):
            if round_num not in fight_data:
                fight_data[round_num] = {}
            for role_id, card_id in align:
                # 助战卡牌
                if role_id in chapter_enemy:
                    # 卡牌两个必触发属性伤害
                    attr = game_config.script_role[role_id]['role_attr']
                    hurts = {'more_attr': {},
                             'attr': {}}
                    for attr_id in attr:
                        hurt = self.get_hurt(attr_id, card_id, tag_score[card_id], is_enemy=True)
                        hurts['attr'][attr_id] = hurt
                        all_score += hurt[0]
                    fight_data[round_num][card_id] = hurts
                    # 概率触发属性伤害
                    hurts['more_attr'] = {}
                    # config = game_config.chapter_enemy[int(card_id)]
                    # rate = config['ex_special_rate']
                    # rate_ = random.randint(1, 10001) <= rate
                    # if rate_:
                    #     more_attr = config['special_quality']
                    #     more_attr = weight_choice(more_attr)
                    #     hurt = self.get_hurt(more_attr[0], card_id, tag_score[card_id], is_enemy=True)
                    #     hurts['more_attr'][more_attr[0]] = hurt
                    #     all_score += hurt[0]
                    fight_data[round_num][card_id] = hurts
                    continue

                # 卡牌两个必触发属性伤害
                attr = game_config.script_role[role_id]['role_attr']
                hurts = {'more_attr': {},
                         'attr': {}}
                for attr_id in attr:
                    hurt = self.get_hurt(attr_id, card_id, tag_score[card_id])
                    all_score += hurt[0]
                    hurts['attr'][attr_id] = hurt
                fight_data[round_num][card_id] = hurts
                # 概率触发属性伤害 special_rate2 5娱乐 special_rate1 6艺术
                card_info = self.mm.card.get_card(card_id)
                config = game_config.card_basis[card_info['id']]
                rate = config['ex_special_rate']
                rate_ = random.randint(1, 10001) <= rate
                if rate_:
                    more_attr = config['special_quality']
                    more_attr = weight_choice(more_attr)
                    hurt = self.get_hurt(more_attr[0], card_id, tag_score[card_id])
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

    def tag_score(self, script_id, role_id, card_id, is_enemy=True):
        return random.randint(1, 100)

    def get_hurt(self, attr_id, card_id, tag_score, is_enemy=True):
        return [random.randint(1, 100), False]

    def get_star(self, all_score, score_config):
        return random.randint(1, 3)

        for level, score in enumerate(score_config, 1):
            if level == 1 and all_score < score:
                return level
            elif level == len(score_config) and all_score >= score:
                return level
            elif score <= all_score < score_config[level]:
                return level + 1
