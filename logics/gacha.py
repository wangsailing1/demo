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
            'today_coin_times': self.gacha.today_coin_times,    # 当日gacha次数
            'coin_pool': self.gacha.coin_pool,  # 探寻到的3个gacha_id
            'coin_time': self.gacha.coin_time,  # 探寻时间
            'coin_times': self.gacha.coin_times,           # 探寻次数
            'coin_lv': self.gacha.coin_lv,           # 探寻等级
            'coin_receive': self.gacha.coin_receive,  # 接受的gacha id
            'coin_pool_expire': self.gacha.coin_pool_expire(),
            'clear_pool_time': self.gacha.clear_remain_time()   #艺人离开剩余时间
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

        self.gacha.add_coin_times()
        self.gacha.coin_time = int(time.time())
        self.gacha.clear_pool_time = int(time.time())
        self.gacha.coin_pool = pool
        self.gacha.coin_receive = []

        return pool, {}

    def receive(self, gacha_id):
        if gacha_id not in self.gacha.coin_pool:
            return 1, {}
        if gacha_id in self.gacha.coin_receive:
            return 2, {}
        if not self.mm.card.can_add_new_card():
            return 3, {}   #活跃卡牌已达上限，请先雪藏艺人

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
        gacha_pool, _ = self.get_coin_gacha()
        self.gacha.coin_gacha_time = 0
        self.gacha.save()
        data = self.gacha_index()
        return 0, data


    def up_gacha(self):
        config = game_config.coin_gacha_lv
        lv = self.gacha.coin_lv
        next_lv = lv + 1
        if next_lv not in config:
            return 1, {}  #已到最大等级
        need_count = config[next_lv]
        if self.gacha.coin_times < need_count:
            return 2, {}  #招募次数不够
        cost = config[next_lv]['cost']
        rc, data = del_mult_goods(self.mm,cost)
        if rc:
            return rc, data
        self.gacha.coin_lv = next_lv
        build_id = config[next_lv]['build_id']
        self.mm.build.up_build(build_id)
        self.gacha.save()
        self.mm.build.save()
        return 0, {}

