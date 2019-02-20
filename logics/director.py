#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

from gconfig import game_config
from tools.gift import has_mult_goods, del_mult_goods, add_mult_gift

class Director(object):

    def __init__(self,mm=None):
        self.mm = mm
        self.director = self.mm.director


    def index(self):
        data = {
            # 'directors': self.director.directors,
            'director_box': self.director.director_box,
            'web_remain_time': self.director.remain_time(1),
            'introduce_remain_time': self.director.remain_time(2),
            'total_times': self.director.total_gacha_times,
            'buy_times': self.director.add_gacha_times,
            'use_times': self.director.total_times,
            'gacha_pool':self.director.gacha_pool
        }
        return 0, data

    def get_gacha_id(self, gacha_type, gacha_id):
        gacha_pool = self.director.gacha_pool[gacha_type]
        if gacha_id not in gacha_pool:
            return 11, {}  # 选择导演未在列表
        config = game_config.director_gacha.get(gacha_id,[])
        if not config:
            return 12, {}  # 配置错误
        if not has_mult_goods(self.mm, config['cost']):
            return 13, {}  # 道具不足
        director_id = config['director'][0][1]
        if director_id in self.director.all_director:
            return 14, {}  # 已经拥有这个导演
        del_mult_goods(self.mm, config['cost'])
        reward = add_mult_gift(self.mm, config['director'])
        director_oids = reward['directors']
        for director_oid in director_oids:
            self.director.directors[director_oid]['source'] = gacha_type
        rc, data = self.index()
        data['reward'] = reward
        return rc, data


    def up_level(self, director_id):
        if director_id not in self.director.directors:
            return 11, {}  # 未拥有这个导演
        director_dict = self.director.directors[director_id]
        config = game_config.director_lv
        cur_lv = director_dict['lv']
        cost = config[cur_lv]['level_cost']
        if not has_mult_goods(self.mm, cost):
            return 12, {}  # 道具不足
        del_mult_goods(self.mm, cost)
        director_dict['lv'] += 1
        self.director.save()
        rc, data = self.index()
        return rc, data

    def work(self,director_id, pos):
        if director_id not in self.director.directors:
            return 11, {}  # 未拥有这个导演
        if pos > self.director.director_box:
            return 12, {}  # 位置尚未开启
        if pos in self.director.all_director_pos:
            return 13, {}  # 已经有导演坐镇
        director_dict = self.director.directors[director_id]
        if director_dict['pos']:
            return 14, {}  # 该导演已经坐镇
        director_dict['pos'] = pos
        self.director.save()
        rc, data = self.index()
        return rc, data


    def rest(self, director_id):
        if director_id not in self.director.directors:
            return 11, {}  # 未拥有这个导演
        director_dict = self.director.directors[director_id]
        if not director_dict['pos']:
            return 12, {}  # 该导演已经在休息了
        director_dict['pos'] = 0
        self.director.save()
        rc, data = self.index()
        return rc, data

    def get_gacha(self, gacha_type):
        if self.director.total_times >= self.director.total_gacha_times:
            return 13, {}  # 已达最大次数
        if self.director.remain_time(gacha_type):
            return 11, {}  # 恢复中
        pool = self.director.refresh_gacha(gacha_type)
        if not pool:
            return 12, {}  # 该组导演你已全部招至麾下
        rc, data = self.index()
        return rc, data


    def unlock_pos(self, pos):
        if pos <= self.director.director_box:
            return 11, {}  #  位置已经开启
        if pos > self.director.director_box + 1:
            return 12, {}  #  请顺序开启
        cost_config = game_config.price_ladder
        cost = cost_config[self.director.director_box]['director_cost']
        if not self.mm.user.is_diamond_enough(cost):
            return 13, {}  # 钻石不足
        self.mm.user.deduct_diamond(cost)
        self.director.director_box += 1
        self.director.save()
        self.mm.user.save()
        rc, data = self.index()
        return rc, data

    def buy_more_gacha_times(self):
        cost_config = game_config.price_ladder
        cost = cost_config[self.director.add_gacha_times + 1]['director_gacha_buy']
        if not self.mm.user.is_diamond_enough(cost):
            return 13, {}  # 钻石不足
        self.mm.user.deduct_diamond(cost)
        self.director.add_gacha_times += 1
        self.director.save()
        self.mm.user.save()
        rc, data = self.index()
        return rc, data



