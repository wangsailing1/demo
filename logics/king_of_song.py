# -*- coding: utf-8 –*-

"""
Created on 2018-12-03

@author: sm
"""

import random

from gconfig import game_config
from lib.core.environ import ModelManager


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
        }
        return 0, data

    def battle(self, role_card, target_uid):
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
            target = ''
        else:
            target = ModelManager(target_uid)

        data = {}
        start = random.randint(1, 5)

        data['win'] = star >= 2
        data['gift'] = []
        data['fight_data'] = fight_data
        data['all_score'] = all_score
        data['star'] = star
        data['tag_score'] = tag_score
        return 0, {}
