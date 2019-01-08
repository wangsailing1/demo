# -*- coding: utf-8 –*-

"""
Created on 2018-12-03

@author: sm
"""

import time
import random

from lib.db import ModelBase
from lib.core.environ import ModelManager

from gconfig import game_config, get_str_words


class KingOfSong(ModelBase):
    """
    谁是歌王
    enemy: {    # 可选对手
        uid: {  # 对手uid
            'script_id': 1,

        }
    }
    """

    MAX_TIMES = 5

    def __init__(self, uid=None):
        """
        :param uid:
        """
        self.uid = uid
        self._attrs = {
            'last_date': '',            # 上次更新时间
            'battle_times': 0,          # 当天挑战次数
            'buy_times': 0,             # 购买次数
            'enemy': {},                # 可选对手uid列表 {uid: {'script_id': '', 'cards': {}}}
            'script_pool': [],          # 自己的可选剧本
        }
        super(KingOfSong, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        if self.last_date != today:
            self.last_date = today
            self.battle_times = 0
            self.buy_times = 0

        if not self.enemy:
            self.refresh_enemy()
        if not self.script_pool:
            self.refresh_scripts()

    def left_battle_times(self):
        return self.MAX_TIMES + self.buy_times - self.battle_times

    def refresh_scripts(self):
        script_pool = random.sample(game_config.script, 3)
        self.script_pool = script_pool
        return self.script_pool

    def refresh_enemy(self):
        if self.mm:
            language_sort = self.mm.user.language_sort
        else:
            language_sort = 1
        enemy = {}
        for i in range(1, 4):
            uid = 'robot_%s' % i
            card_ids = game_config.card_basis.keys()
            name = get_str_words(language_sort, random.choice(game_config.first_random_name['first_name']))
            script_id = random.choice(game_config.script.keys())
            script_config = game_config.script[script_id]

            cards = {}
            for role_id in script_config['role_id']:
                card_id = random.choice(card_ids)
                card_ids.remove(card_id)
                cards[role_id] = card_id
            enemy[uid] = {
                'user_name': name,
                'script_id': script_id,
                'cards': cards          # {role_id: card_id}
            }

        self.enemy = enemy
        return self.enemy


ModelManager.register_model('king_of_song', KingOfSong)
