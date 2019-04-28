# -*- coding: utf-8 -*-

__author = 'ljm'

from gconfig import game_config
from tools.gift import add_mult_gift
from lib.core.environ import ModelManager


class ActiveScore(object):

    def __init__(self, mm):
        self.mm = mm
        if self.mm.user.config_type == 1:
            self.active_score = self.mm.server_active_score
            self.reward_config = game_config.active_score_new.get(self.active_score.version, {})
            self.rank_reward_config = game_config.active_score_rank_new
        else:
            self.active_score = self.mm.active_score
            self.reward_config = game_config.active_score.get(self.active_score.version, {})
            self.rank_reward_config = game_config.active_score_rank

    def index(self):
        if not self.active_score.get_inreview():
            return 1, {}  # 活动已关闭
        if not self.active_score.version:
            return 2, {} # 活动未开启
        data = {
            'version': self.active_score.version,
            'score_daily': self.active_score.score_daily,
            'score_total': self.active_score.score_total,
            'got_reward_daily': self.active_score.got_reward_daily,
            'got_reward_total': self.active_score.got_reward_total,
            'got_rank_reward': self.active_score.got_rank_reward
        }
        return 0, data

    def get_reward(self, tp, reward_id):
        if not self.active_score.version:
            return 2, {} # 活动未开启
        if not self.active_score.get_inreview():
            return 1, {}  # 活动已关闭
        if tp == 1:  # 每日奖励
            rc, data = self.get_reward_daily(reward_id)
        elif tp == 2:  # 累计奖励
            rc, data = self.get_reward_total(reward_id)
        else:  # 排行奖励
            rc, data = self.get_reward_rank()
        self.active_score.save()
        _, data_ = self.index()
        data.update(data_)
        return rc, data

    def get_reward_daily(self, reward_id):
        if reward_id > len(self.reward_config['award_daily']) or reward_id <= 0:
            return 11, {}  # 奖品id错误
        if reward_id in self.active_score.got_reward_daily:
            return 12, {}  # 奖品已领
        if self.reward_config['need_daily'][reward_id - 1] > self.active_score.score_daily:
            return 13, {}  # 积分未达到
        self.active_score.got_reward_daily.append(reward_id)
        gift = self.reward_config['award_daily'][reward_id - 1]
        reward = add_mult_gift(self.mm, gift)
        data = {'reward': reward}
        return 0, data

    def get_reward_total(self, reward_id):
        if reward_id > len(self.reward_config['award_total']) or reward_id <= 0:
            return 21, {}  # 奖品id错误
        if reward_id in self.active_score.got_reward_total:
            return 22, {}  # 奖品已领
        if self.reward_config['need_total'][reward_id - 1] > self.active_score.score_total:
            return 23, {}  # 积分未达到
        self.active_score.got_reward_total.append(reward_id)
        gift = self.reward_config['award_total'][reward_id - 1]
        reward = add_mult_gift(self.mm, gift)
        data = {'reward': reward}
        return 0, data

    def get_reward_rank(self):
        if self.active_score.get_version():
            return 31, {}  # 活动尚未结束
        rank = self.active_score.get_rank()
        if not rank:
            return 32, {}  # 没有排名信息
        if self.active_score.got_rank_reward:
            return 33, {}  # 排名奖励已领
        gift = []
        for _ , value in self.rank_reward_config.iteritems():
            if value['rank'][0] <= rank <= value['rank'][1] and self.active_score.version in value['active_id']:
                gift = value['award']
                break
        self.active_score.got_rank_reward = True
        reward = add_mult_gift(self.mm, gift)
        data = {'reward': reward}
        return 0, data

    def rank_info(self, start, end):
        if not self.active_score.get_inreview():
            return 1, {}  # 活动已关闭
        if not self.active_score.version:
            return 2, {} # 活动未开启
        rank_info = self.active_score.get_rank_all(start=start - 1, end=end - 1, withscores=True)
        result = {}
        for rank, info in enumerate(rank_info, start):
            uid = info[0]
            score = info[1]
            umm = ModelManager(uid)
            result[rank] = {
                'name': umm.user.name,
                'score': score
            }
        own_rank = self.active_score.get_rank()
        own_score = self.active_score.get_score()
        data = {
            'rank_info': result,
            'own_info': {'rank': own_rank, 'score': own_score}
        }
        return 0, data

