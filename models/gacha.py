#! --*-- coding: utf-8 --*--
__author__ = 'sm'

import time
import random

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
import settings


class Gacha(ModelBase):
    DIAMOND_FREE_MAX_TIMES = 1  # 钻石免费最大次数
    DIAMOND_REFRESH_TIME = 24 * 3600  # 钻石刷新时间
    COIN_FREE_MAX_TIMES = 5  # 银币免费最大次数
    COIN_REFRESH_TIME = 24 * 3600  # 银币免费最大次数
    BOX_REFRESH_TIME = 24 * 3600  # 觉醒宝箱免费刷新时间
    COIN_FREE_TIME = 0  # 银币免费抽取间隔时间
    SERVER_DIAMOND_SCORE = 'server_diamond_score'  # 钻石全服积分
    SERVER_BOX_SCORE = 'server_box_score'  # 宝箱全服积分

    MAX_POOL_NUM = 3
    POOL_EXPIRE = 30 * 60       # gacha池子有效期 30分钟

    def __init__(self, uid):
        """
        抽卡
        :param uid:
        :return:
        """
        self.uid = uid
        self._attrs = {
            'coin_times': 0,
            'coin_lv': 0,

            'coin_pool': [],          # 探寻到的3个gacha_id
            'coin_time': 0,           # 探寻时间
            'coin_receive': [],       # 接受的gacha id

        }
        super(Gacha, self).__init__(self.uid)

    def pre_use(self):
        if self.coin_pool_expire() <= 0:
            self.clear_coin_pool()

    def clear_coin_pool(self):
        self.coin_gacha_time = 0
        self.coin_gacha_pool = []
        self.coin_receive = []

    def coin_pool_expire(self):
        expire = self.POOL_EXPIRE - (int(time.time()) - self.coin_time)
        return max(expire, 0)

    def add_coin_times(self, times=1):
        next_times = self.coin_times + times

        while 1:
            if self.coin_lv + 1 not in game_config.coin_gacha_lv:
                break
            break
        self.coin_times = next_times


ModelManager.register_model('gacha', Gacha)
