#! --*-- coding: utf-8 --*--
__author__ = 'sm'

import time
import random

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
import settings


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
            'coin_times': 0,            # 普通抽取次数
            'coin_time': 0,             # 探寻时间

            'diamond_times': 0,         # 钻石抽取次数
            'diamond_time': 0,          # 钻石抽取时间


        }
        super(ScriptGacha, self).__init__(self.uid)

    def pre_use(self):
        # 清除cd
        today = time.strftime('%F')
        if self.refresh_date != today:
            self.refresh_date = today
            self.coin_times = 0
            self.diamond_times = 0

    def cd_expire(self, gacha_type=1):
        if not game_config.script_gacha_cd:
            return 0

        if gacha_type == 1:
            times = self.coin_times
            last_time = self.coin_time
        else:
            return 0        # 钻石抽不cd
            # times = self.diamond_times
            # last_time = self.diamond_time

        if not times:
            return 0

        if times in game_config.script_gacha_cd:
            config = game_config.script_gacha_cd[times]
        else:
            max_times = max(game_config.script_gacha_cd)
            config = game_config.script_gacha_cd[max_times]

        expire = config['cd'] * 60 - int(time.time() - last_time)
        return expire if expire > 0 else 0


ModelManager.register_model('script_gacha', ScriptGacha)
