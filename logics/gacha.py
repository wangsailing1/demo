#! --*-- coding: utf-8 --*--
__author__ = 'sm'

import time
import bisect
import copy
import random

from gconfig import game_config
from lib.utils import weight_choice
from tools.gift import add_mult_gift, del_mult_goods
from lib.utils.debug import print_log
from lib.utils import not_repeat_weight_choice


class GachaLogics(object):

    def __init__(self, mm, sort):
        """
        :param mm:
        :param sort: 1:金币抽, 0:钻石抽
        :return:
        """
        self.mm = mm
        self.gacha = self.mm.gacha
        self.sort = sort
        self.refresh()

    def refresh(self, sort=None):
        """
        gacha自动刷新免费次数
        :return:
        """
        sort = self.sort if sort is None else sort

    def gacha_index(self):
        """
        gacha界面
        :return:
        """
        self.refresh(1 if self.sort == 0 else 0)

        data = {
            'coin_pool': self.gacha.coin_pool,  # 探寻到的3个gacha_id
            'coin_time': self.gacha.coin_time,  # 探寻时间
            'coin_times': self.gacha.coin_times,           # 探寻次数
            'coin_lv': self.gacha.coin_lv,           # 探寻等级
            'coin_receive': self.gacha.coin_receive,  # 接受的gacha id
            'coin_pool_expire': self.gacha.coin_pool_expire()
        }

        return data

    def get_gacha(self, sort, count=1):
        """
        抽卡
        :param sort: 1:钻石抽, 0:金币抽,
        :param count: 1或10次
        :return:
        """
        cost_type = ''
        cost_num = 0

        sort = 0

        if sort == 0:
            if self.gacha.coin_pool_expire():
                return 2, {}
            cost_type = 'coin'
            gacha_pool, _ = self.get_coin_gacha()
            if not gacha_pool:
                return 1, {}  # 没有普通补给的奖励配置

        self.gacha.save()
        self.mm.user.save()
        result = {
            '_bdc_event_info': {'cost_num': cost_num, 'cost_type': cost_type}
        }
        result.update(self.gacha_index())

        return 0, result

    def get_coin_gacha(self):
        """
        普通抽卡
        :param count: 次数
        :return:
        """
        coin_gacha_mapping = game_config.get_coin_gacha_mapping()
        if not coin_gacha_mapping:
            return [], {}  # 没有普通补给的奖励配置

        can_use_ids = []
        for lv, id_weights in coin_gacha_mapping['weight'].iteritems():
            if self.gacha.coin_lv >= lv:
                can_use_ids.extend(id_weights)

        pool = []
        for i in xrange(self.gacha.MAX_POOL_NUM):
            id_weight = weight_choice(can_use_ids)
            can_use_ids.remove(id_weight)
            pool.append(id_weight[0])

        self.gacha.coin_times += 1
        self.gacha.coin_time = int(time.time())
        self.gacha.coin_pool = pool
        self.gacha.coin_receive = []

        return pool, {}

    def receive(self, gacha_id):
        if gacha_id not in self.gacha.coin_pool:
            return 1, {}
        if gacha_id in self.gacha.coin_receive:
            return 2, {}

        user = self.mm.user
        gacha_config = game_config.coin_gacha[gacha_id]
        cost = gacha_config['cost']
        if not user.is_like_enough(cost):
            return 'error_like', {}

        reward = add_mult_gift(self.mm, gacha_config['reward'])
        self.gacha.coin_receive.append(gacha_id)
        self.gacha.save()

        user.deduct_like(cost)
        user.save()

        data = {'reward': reward}
        data.update(self.gacha_index())
        return 0, data

    def clear_gacha_cd(self):
        cost = game_config.coin_gacha_cd['cost']
        rc, _ = del_mult_goods(self.mm, cost)
        if rc:
            return rc, {}

        self.gacha.coin_gacha_time = 0
        self.gacha.save()
        return self.gacha_index()