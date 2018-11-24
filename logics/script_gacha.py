#! --*-- coding: utf-8 --*--
__author__ = 'sm'

import time
import bisect
import copy
import random

from gconfig import game_config
from lib.utils import weight_choice
from tools.gift import add_mult_gift, del_mult_goods


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
            'coin_left_times': self.gacha.coin_left_times,                # 剩余普通抽取次数
            'coin_update_time': self.gacha.coin_update_time,              # 上次恢复时间
            'coin_recover_times': self.gacha.coin_recover_times,          # 今日已恢复次数
            'coin_times_limit': self.gacha.coin_gacha_times_limit(),          # 普通抽取可恢复次数上线

            'coin_cd_expire': self.gacha.recover_expire(),                   # 普通抽cd倒计时
            'diamond_cd_expire': 0,    # 钻石抽cd倒计时
            'coin_time': self.gacha.coin_time,                  # 探寻时间
            'coin_times': self.gacha.coin_times,                # 探寻次数
            'diamond_time': self.gacha.diamond_time,            # 探寻时间
            'diamond_times': self.gacha.diamond_times,          # 探寻次数
        }

        return data

    def get_gacha(self, sort, count=1):
        """
        抽卡
        :param sort: 1:金币抽, 2:钻石抽
        :param count: 1或10次
        :return:
        """
        # 钻石抽不判断cd
        enough = self.gacha.gacha_times_enough(sort)
        if not enough:
            return 1, {}    # 可抽取次数不足

        cost = game_config.script_gacha_cost[sort]['cost']
        rc, _ = del_mult_goods(self.mm, cost)
        if rc:
            return rc, {}

        if sort == 1:
            cost_type = 'coin'
            gacha_config = self.get_coin_gacha()
            self.gacha.coin_times += 1
            self.gacha.coin_left_times -= 1
            self.gacha.coin_time = int(time.time())
        else:
            cost_type = 'diamond'
            gacha_config = self.get_diamond_gacha()
            self.gacha.diamond_times += 1
            self.gacha.diamond_time = int(time.time())

        if gacha_config['gifts_id']:
            reward = add_mult_gift(self.mm, gacha_config['gifts_id'])
        else:
            script_id = gacha_config['script_id']
            self.mm.script.add_own_script(script_id)
            reward = {'own_script': [script_id]}

        self.mm.script.save()
        self.gacha.save()
        self.mm.user.save()

        result = {
            '_bdc_event_info': {'cost': cost, 'cost_type': cost_type},

            # 'script_id': script_id,
            # 'new_script': new_script,

            'reward': reward,
        }
        result.update(self.gacha_index())

        return 0, result

    def get_coin_gacha(self):
        """
        普通抽卡
        :param count: 次数
        :return:
        """
        script = self.mm.script
        gacha_config = game_config.script_gacha

        special_mapping = {v['weight_special']: k for k, v in gacha_config.iteritems()
                           if v['weight_special'] and v['script_id'] not in script.own_script}
        next_times = self.gacha.coin_times + 1

        if next_times in special_mapping:
            gacha_id = special_mapping[next_times]
        else:
            id_weights = [(k, v['weight']) for k, v in gacha_config.iteritems()
                          if v['script_id'] not in script.own_script]
            gacha_id = weight_choice(id_weights)[0]

        return gacha_config[gacha_id]

    def get_diamond_gacha(self):
        """
        钻石抽卡
        :param count: 次数
        :return:
        """
        script = self.mm.script
        gacha_config = game_config.diamond_script_gacha

        special_mapping = {v['weight_special']: k for k, v in gacha_config.iteritems()
                           if v['weight_special'] and v['script_id'] not in script.own_script}

        next_times = self.gacha.diamond_times + 1

        if next_times in special_mapping:
            gacha_id = special_mapping[next_times]
        else:
            id_weights = [(k, v['weight']) for k, v in gacha_config.iteritems()
                          if v['script_id'] not in script.own_script]
            gacha_id = weight_choice(id_weights)[0]

        return gacha_config[gacha_id]


    def up_build_level(self):

        config = game_config.script_gacha_building
        next_lv = self.gacha.building_level + 1
        if next_lv not in config:
            return 1, {}  # 等级最大
        if self.mm.user.level < config[next_lv]['player_lv']:
            return 2, {}  # 等级未达到
        cost = config[next_lv]['cost']
        rc, data = del_mult_goods(self.mm, cost)
        if rc:
            return rc, data
        self.gacha.building_level = next_lv
        self.mm.user.up_build(config[next_lv]['build_id'], is_save=True)
        self.gacha.save()
        return 0, {}


