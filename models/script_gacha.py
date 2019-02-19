#! --*-- coding: utf-8 --*--
__author__ = 'sm'

import time
import random

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
import settings
from models.vip_company import scriptgacha_maxnum


class ScriptGacha(ModelBase):

    def __init__(self, uid):
        """
        抽卡
        :param uid:
        :return:
        """
        self.uid = uid
        self._attrs = {
            'refresh_date': '',         # 登录日期

            'coin_left_times': self.coin_gacha_times_limit(),         # 普通抽剩余次数
            'coin_update_time': int(time.time()),           # 普通抽次数刷新时间
            'coin_recover_times': 0,                        # 当日恢复了几次

            'coin_times': 0,            # 普通抽取次数
            'coin_time': 0,             # 探寻时间

            'diamond_times': 0,         # 钻石抽取次数
            'diamond_time': 0,          # 钻石抽取时间
            'build_level':1


        }
        super(ScriptGacha, self).__init__(self.uid)

    def pre_use(self):
        # 清除cd
        today = time.strftime('%F')
        if self.refresh_date != today:
            self.refresh_date = today
            self.coin_times = 0
            self.diamond_times = 0
            self.coin_recover_times = 0

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

    def coin_gacha_times_limit(self):
        return game_config.common[41] + scriptgacha_maxnum(self.mm.user)

    def can_recover_coin_times(self):
        gacha_cd = game_config.script_gacha_cd.get('cd', [])
        if self.coin_recover_times >= len(gacha_cd):
            return False

        return self.coin_left_times < self.coin_gacha_times_limit()

    def recover_need_time(self):
        """自动恢复时间 单位：秒"""
        if not game_config.script_gacha_cd:
            return 0
        gacha_cd = game_config.script_gacha_cd['cd']
        times = self.coin_recover_times
        if times >= len(gacha_cd):
            times = -1
        build_effect = self.mm.user.build_effect
        effect_time = build_effect.get(6, 0)
        return gacha_cd[times] * 60 - effect_time

    def recover_expire(self):
        """恢复倒计时"""
        if not game_config.script_gacha_cd:
            return 0

        if not self.can_recover_coin_times():
            return 0

        gacha_cd = game_config.script_gacha_cd['cd']
        times = self.coin_recover_times
        if times >= len(gacha_cd):
            return 0

        need_time = gacha_cd[times] * 60
        return need_time - (int(time.time()) - self.coin_update_time)

    def gacha_times_enough(self, gacha_type=1):
        if gacha_type == 1:
            return [self.coin_left_times > 0, self.recover_expire()]
        return [True, 0]


ModelManager.register_model('script_gacha', ScriptGacha)
