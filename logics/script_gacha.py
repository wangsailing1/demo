#! --*-- coding: utf-8 --*--
__author__ = 'sm'

import time
import bisect
import copy
import random

from gconfig import game_config
from lib.utils import weight_choice
from tools.gift import add_mult_gift
from lib.utils.debug import print_log
from lib.utils import not_repeat_weight_choice


class ScriptGachaLogics(object):

    def __init__(self, mm, sort):
        """
        :param mm:
        :param sort: 1:金币抽, 0:钻石抽
        :return:
        """
        self.mm = mm
        self.gacha = self.mm.script_gacha
        self.sort = sort

    def gacha_index(self):
        """
        gacha界面
        :return:
        """

        data = {
            'coin_cd_expire': self.gacha.cd_expire(),                   # 普通抽cd倒计时
            'diamond_cd_expire': self.gacha.cd_expire(gacha_type=1),    # 钻石抽cd倒计时
            'coin_time': self.gacha.coin_time,                  # 探寻时间
            'coin_times': self.gacha.coin_times,                # 探寻次数
            'diamond_time': self.gacha.diamond_time,            # 探寻时间
            'diamond_times': self.gacha.diamond_times,          # 探寻次数
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

        if sort == 1:
            cost = ''
            script_id = self.get_diamond_gacha()
            self.gacha.diamond_times += 1
            self.gacha.diamond_time = int(time.time())
        else:
            cost_type = 'coin'
            cost = ''
            script_id = self.get_coin_gacha()
            self.gacha.coin_times += 1
            self.gacha.coin_time = int(time.time())

        new_script = self.mm.script.add_own_script(script_id)

        self.mm.script.save()
        self.gacha.save()
        self.mm.user.save()

        result = {
            '_bdc_event_info': {'cost_num': cost_num, 'cost_type': cost_type},
            'script_id': script_id,
            'new_script': new_script,
        }
        result.update(self.gacha_index())

        return 0, result

    def get_coin_gacha(self):
        """
        普通抽卡
        :param count: 次数
        :return:
        """
        gacha_config = game_config.script_gacha

        special_mapping = {v['weight_special']: v for v in gacha_config.itervalues() if v['weight_special']}
        next_times = self.gacha.coin_times + 1

        if next_times in special_mapping:
            script_id = special_mapping[next_times]['script_id']
        else:
            id_weights = [(v['script_id'], v['weight']) for k, v in gacha_config.iteritems()]
            script_id = weight_choice(id_weights)[0]

        return script_id

    def get_diamond_gacha(self):
        """
        钻石抽卡
        :param count: 次数
        :return:
        """
        gacha_config = game_config.diamond_script_gacha

        special_mapping = {v['weight_special']: v for v in gacha_config.itervalues() if v['weight_special']}
        next_times = self.gacha.diamond_times + 1

        if next_times in special_mapping:
            script_id = special_mapping[next_times]['script_id']
        else:
            id_weights = [(v['script_id'], v['weight']) for k, v in gacha_config.iteritems()]
            script_id = weight_choice(id_weights)[0]

        return script_id

