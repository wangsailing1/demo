# -*- coding: utf-8 –*-

"""
Created on 2018-12-03

@author: sm
"""

import time
import datetime
import random
import itertools

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

    OPEN_DAY = (1, 25)      # 每月1至25号开启
    MAX_TIMES = 5
    ENEMY_COUNT = 3

    BUY_ADD_BATTLE_TIMES = 5        # 每次购买添加的战斗次数

    def __init__(self, uid=None):
        """
        :param uid:
        """
        self.uid = uid
        self._attrs = {
            'season': '',               # 当前赛季
            'last_season_info': [],     # 上赛季信息 [season, rank]
            'season_reward_log': [],    # 赛季奖励记录

            'star': 0,                  # 当前赛季星级
            'rank': 1,                  # 当前段位
            'rank_win_times': {},       # 每个段位胜利次数
            'rank_reward_log': [],      # 领取过的段位排行奖励
            'continue_win_times': 0,    # 连胜次数

            'last_date': '',            # 上次更新时间
            'battle_times': 0,          # 当天挑战次数
            'last_battle_team': [],     # 最近一次的战斗队伍
            'buy_times': 0,             # 购买次数
            'enemy': {},                # 可选对手uid列表 {uid: {'script_id': '', 'cards': {}}}
            'script_pool': [],          # 自己的可选剧本
            'enemy_fight_data': {},     # 自己和对手的战斗分开接口计算，cache一下
        }
        super(KingOfSong, self).__init__(self.uid)

    def pre_use(self):
        save = False

        today = datetime.datetime.now()
        season = today.strftime('%Y-%m')
        if self.season != season:
            self.last_season_info = [self.season, self.rank]
            self.season = season
            self.last_battle_team = []

            self.star = 0
            self.rank = 1
            self.rank_win_times = {}
            self.rank_reward_log = []
            self.continue_win_times = 0

        today_str = time.strftime('%F')
        if self.last_date != today_str:
            self.last_date = today_str
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

    def add_star(self):
        """
        :return: 下一次再加星是否升级
        """
        rank_up = False
        self.rank_win_times[self.rank] = self.rank_win_times.get(self.rank, 0) + 1

        if self.continue_win_times:
            # 连胜状态 多加一颗star
            self.star += 1

        self.star += 1
        rank_config = game_config.pvp_rank[self.rank]
        # 晋级赛 达到区间晋级要求后，再胜1场区间+1（不奖励星星）
        if rank_config['star'] and self.rank + 1 in game_config.pvp_rank:
            # 提前判断下次再加星是否升级
            if self.star + 1 > rank_config['star']:
                rank_up = True

            if self.star > rank_config['star']:
                self.rank += 1
                self.star = 0

        self.continue_win_times += 1
        # 最高等级星级限制
        max_rank = max(game_config.pvp_rank)
        max_config = game_config.pvp_rank[max_rank]
        if self.rank == max_rank:
            self.star = min(self.star, max_config['star'])
        return rank_up

    def deduct_star(self):
        """
        :return: 下一次再减星是否降级
        """
        rank_down = False
        self.star -= 1
        last_rank_config = game_config.pvp_rank.get(self.rank - 1)
        # 提前判断下次再加星是否升级
        if last_rank_config:
            if self.star - 1 < 0:
                rank_down = True

        # 淘汰赛 达到区间降级临界时，再败1场区间-1（不扣星星）
        if self.star < 0:
            if last_rank_config:
                self.star = last_rank_config['star'] - 1
                self.rank -= 1
            else:
                self.star = 0

        self.continue_win_times = 0
        return rank_down

    def red_dot(self):
        return {
            'left_battle_times': self.left_battle_times(),
            'has_rank_reward': self.has_rank_reward()
        }

    def has_rank_reward(self):
        for rank in game_config.pvp_rank:
            if rank in self.rank_reward_log:
                continue
            win_times = 0
            for k, v in self.rank_win_times.items():
                if k >= rank:
                    win_times += v
            if win_times >= game_config.common[77]:
                return True
        return False

    def left_battle_times(self):
        return self.MAX_TIMES + self.buy_times * self.BUY_ADD_BATTLE_TIMES - self.battle_times

    def choice_scripts(self, num=3):
        rank_config = game_config.pvp_rank[self.rank]
        script_pool = random.sample(rank_config['script'], num)
        return script_pool

    def refresh_scripts(self):
        self.script_pool = self.choice_scripts()

    def refresh_enemy(self):
        enemy = {}
        robot_pool = [k for k, v in game_config.pvp_robots.items() if v['rank'] == self.rank]
        rank_config = game_config.pvp_rank[self.rank]

        rank_obj = self.mm.get_obj_tools('level_rank')
        level = self.mm.user.level
        uids = rank_obj.nearby_score(max(1, level - 10), level+5, start=0, num=20)

        for tp, uids in [('user', uids), ('robot', robot_pool)]:
            random.shuffle(uids)
            for i in uids:
                if len(enemy) >= self.ENEMY_COUNT:
                    break

                if tp == 'user':
                    if i == self.uid:
                        continue
                    uid = i
                    enemy_mm = self.mm.get_mm(i)
                    name = enemy_mm.user.name
                    cards = {}
                    for card_oid, card_info in sorted(enemy_mm.card.cards.iteritems(), key=lambda x: x[1]['lv'], reverse=True):
                        cards[card_oid] = card_info
                        if len(cards) >= rank_config['card_num']:
                            break
                    if not cards:
                        continue
                else:
                    uid = 'robot_%s' % i
                    robot_config = game_config.pvp_robots[i]
                    # name = get_str_words(language_sort, random.choice(game_config.first_random_name['first_name']))
                    name = get_str_words(self.mm.lan, robot_config['name'])
                    cards = {}
                    for i in robot_config['card']:
                        card_id, lv, love_lv = i[:3]
                        card_oid, card_info = CardM.generate_card(card_id, lv=lv, love_lv=love_lv, lan=self.mm.lan)
                        cards[card_oid] = card_info

                script_id = random.choice(self.choice_scripts())
                script_config = game_config.script[script_id]

                enemy_align = dict(zip(script_config['role_id'], cards))
                enemy[uid] = {
                    'user_name': name,
                    'script_id': script_id,
                    'cards': cards,  # {role_id: card_id}
                    'align': enemy_align,
                }

        self.enemy = enemy
        return self.enemy


ModelManager.register_model('king_of_song', KingOfSong)
