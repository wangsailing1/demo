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
from models.card import Card as CardM


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
            'star': 0,                  # 当前赛季星级
            'rank': 1,                  # 当前段位
            'last_date': '',            # 上次更新时间
            'battle_times': 0,          # 当天挑战次数
            'buy_times': 0,             # 购买次数
            'enemy': {},                # 可选对手uid列表 {uid: {'script_id': '', 'cards': {}}}
            'script_pool': [],          # 自己的可选剧本
            'enemy_fight_data': {},     # 自己和对手的战斗分开接口计算，cache一下
        }
        super(KingOfSong, self).__init__(self.uid)

    def pre_use(self):
        save = False
        today = time.strftime('%F')
        if self.last_date != today:
            self.last_date = today
            self.battle_times = 0
            self.buy_times = 0

        if not self.enemy:
            self.refresh_enemy()
            save = True
        if not self.script_pool:
            self.refresh_scripts()
            save = True
        if save:
            self.save()

    def left_battle_times(self):
        return self.MAX_TIMES + self.buy_times - self.battle_times

    def choice_scripts(self, num=3):
        rank_config = game_config.pvp_rank[self.rank]
        script_pool = random.sample(rank_config['script'], num)
        return script_pool

    def refresh_scripts(self):
        self.script_pool = self.choice_scripts()

    def refresh_enemy(self):
        enemy = {}
        robot_pool = [k for k, v in game_config.pvp_robots.items() if v['rank'] == self.rank]

        # todo 筛选真人或者robot
        for i in random.sample(robot_pool, 3):
            uid = 'robot_%s' % i
            robot_config = game_config.pvp_robots[i]
            # name = get_str_words(language_sort, random.choice(game_config.first_random_name['first_name']))
            name = robot_config['name']
            script_id = random.choice(self.choice_scripts())
            script_config = game_config.script[script_id]

            cards = {}
            for i in robot_config['card']:
                card_id, lv, love_lv = i[:3]
                card_oid, card_info = CardM.generate_card(card_id, lv=lv, love_lv=love_lv)
                cards[card_oid] = card_info

            enemy_align = dict(zip(script_config['role_id'], cards))
            enemy[uid] = {
                'user_name': name,
                'script_id': script_id,
                'cards': cards,          # {role_id: card_id}
                'align': enemy_align,
            }

        self.enemy = enemy
        return self.enemy


ModelManager.register_model('king_of_song', KingOfSong)
