#! --*-- coding: utf-8 --*--
__author__ = 'sm'

import time
import random

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from models import vip_company
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
    POOL_EXPIRE = 30 * 60  # gacha池子有效期 30分钟

    def __init__(self, uid):
        """
        抽卡
        :param uid:
        :return:
        """
        self.uid = uid
        self._attrs = {
            'refresh_date': '',
            'coin_times': 0,
            'today_coin_times': 0,
            'coin_lv': 1,

            'coin_update_time': int(time.time()),  # gacha恢复时间
            'coin_recover_times': 0,  # gacha当日恢复次数
            'coin_left_times': vip_company.init_vip_coin_gacha_count(),      # 剩余gacha次数

            'coin_pool': [],  # 探寻到的3个gacha_id
            'coin_time': 0,  # 探寻时间 按钮刷新
            'coin_receive': [],  # 接受的gacha id
            'clear_pool_time': 0,  # 清除pool的时间  艺人离开

        }
        super(Gacha, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')

        # 老号容错 开始初始值从0 改为1
        if not self.coin_lv:
            self.coin_lv = 1
        if self.refresh_date != today:
            self.refresh_date = today
            self.today_coin_times = 0
            self.coin_recover_times = 0
            if self.can_recover_coin_times():
                if not self.inited:
                    self.coin_left_times += 1

        # 自动恢复抽卡次数
        now = int(time.time())
        recover_need_time = self.recover_need_time()
        if recover_need_time:
            div, mod = divmod(now - self.coin_update_time, recover_need_time)
            while div and self.can_recover_coin_times():
                self.coin_left_times += 1
                self.coin_recover_times += 1
                self.coin_update_time += recover_need_time

                recover_need_time = self.recover_need_time()
                if not recover_need_time:
                    break
                div, mod = divmod(now - self.coin_update_time, recover_need_time)

        if not self.can_recover_coin_times():
            self.coin_update_time = now

        if self.clear_remain_time() <= 0:
            self.clear_coin_pool()

    def can_recover_coin_times(self):
        gacha_cd = game_config.coin_gacha_cd.get('cd', [])
        if self.coin_recover_times >= len(gacha_cd):
            return False

        return self.coin_left_times < self.coin_gacha_times_limit()

    def coin_gacha_times_limit(self):
        return vip_company.vip_coin_gacha_count(self.mm.user)

    def recover_need_time(self):
        """自动恢复时间 单位：秒"""
        gacha_cd = game_config.script_gacha_cd['cd']
        times = self.coin_recover_times
        if times >= len(gacha_cd):
            times = -1
        build_effect = self.mm.user.build_effect
        effect_time = build_effect.get(6, 0)
        return gacha_cd[times] * 60 - effect_time

    def clear_coin_pool(self):
        self.coin_gacha_time = 0
        self.clear_pool_time = 0
        self.coin_pool = []
        self.coin_receive = []

    def clear_remain_time(self):
        cd = game_config.common[52]
        remain_time = cd - (int(time.time()) - self.clear_pool_time)
        return max(remain_time, 0)

    def coin_pool_expire(self):
        cd = game_config.coin_gacha_cd['cd']
        times = self.today_coin_times
        if times >= len(cd):
            times = -1
        expire = cd[times] * 60 - (int(time.time()) - self.coin_time)
        return max(expire, 0)

    def add_coin_times(self, times=1):
        self.today_coin_times += times
        self.coin_times += times
        self.coin_left_times -= times
        # next_times = self.coin_times + times
        # next_lv = self.coin_lv
        #
        # while 1:
        #     if next_lv + 1 not in game_config.coin_gacha_lv:
        #         break
        #     if next_times >= game_config.coin_gacha_lv[next_lv + 1]['count']:
        #         next_lv += 1
        #         continue
        #     break
        # self.coin_times = next_times
        # self.coin_lv = next_lv

    def get_gacha_red_dot(self):
        """
        :return: [是否能抽取，抽取倒计时]
        """
        return [self.coin_left_times > - 0, self.coin_pool_expire()]

    def get_can_up_red_hot(self):
        config = game_config.coin_gacha_lv
        lv = self.coin_lv
        next_lv = lv + 1
        if next_lv not in config:
            return False
        need_count = config[next_lv]
        if self.coin_times < need_count:
            return False
        return True


ModelManager.register_model('gacha', Gacha)
