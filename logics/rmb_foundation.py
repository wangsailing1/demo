#!/usr/bin/python
# encoding: utf-8

import time
import datetime
from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils.active_inreview_tools import get_version_by_active_id

class RmbFoundation(object):

    def __init__(self, mm=None):
        self.mm = mm

    def rmbfoundation_index(self):
        data = {}
        active_id, _ = get_version_by_active_id(active_id=self.mm.rmbfoundation.ACTIVE_TYPE)
        end_date = game_config.active[self.mm.rmbfoundation.a_id]['end_time']
        end_time = int(time.mktime(time.strptime(end_date, '%Y-%m-%d %H:%M:%S')) - time.time())
        data['end_time'] = end_time
        data['version'] = self.mm.rmbfoundation.version
        data['rmbf_active_dates'] = {}
        for f_id, f_active_date in self.mm.rmbfoundation.activate_mark.iteritems():
            f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
            data['rmbf_active_dates'][f_id] = (datetime.date.today() - f_active_date).days + 1
        data['reward_dict'] = self.mm.rmbfoundation.reward_dict
        return 0, data


    def withdraw(self, f_id, days):
        f_active_date = self.mm.rmbfoundation.activate_mark[f_id]
        f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
        active_days = (datetime.date.today() - f_active_date).days + 1
        reward_list = self.mm.rmbfoundation.reward_dict[f_id]
        config = game_config.get_rmbfoundation_mapping()
        rmbfoundation_info = config.get(self.mm.rmbfoundation.version, {}).get(f_id, {})
        if not rmbfoundation_info:
            return 5, {}  # 基金活动配置错误

        if days not in reward_list or active_days < days:
            return 4, {}  # 无奖励可领取

        index = reward_list.index(days)
        reward_list.pop(index)
        reward = rmbfoundation_info['day%s' % days]
        gift = add_mult_gift(self.mm, reward)
        self.mm.rmbfoundation.save()
        rc, data = self.rmbfoundation_index()
        data['reward'] = gift
        return rc, data