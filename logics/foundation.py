#!/usr/bin/python
# encoding: utf-8

import time
import datetime
from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils.active_inreview_tools import get_version_by_active_id

class Foundation(object):

    def __init__(self, mm=None):
        self.mm = mm

    def foundation_index(self):
        data = {}
        actice_id, _ = get_version_by_active_id(active_id=self.mm.foundation.ACTIVE_TYPE)
        can_open = self.mm.foundation.can_open()
        if not can_open:
            return 1, {}  # 活动未开启
        end_date = game_config.active[actice_id]['end_time']
        end_time = int(time.mktime(time.strptime(end_date, '%Y-%m-%d %H:%M:%S')) - time.time())
        data['end_time'] = end_time
        data['version'] = self.mm.foundation.version
        data['score'] = self.mm.foundation.score
        data['f_active_dates'] = {}
        for f_id, f_active_date in self.mm.foundation.activate_mark.iteritems():
            f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
            data['f_active_dates'][f_id] = (datetime.date.today() - f_active_date).days + 1
        data['reward_dict'] = self.mm.foundation.reward_dict
        return 0, data

    def withdraw(self, f_id, days):
        f_active_date = self.mm.foundation.activate_mark[f_id]
        f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
        active_days = (datetime.date.today() - f_active_date).days + 1
        reward_list = self.mm.foundation.reward_dict[f_id]
        foundation_info = game_config.foundation[f_id]

        if days not in reward_list or active_days < days:
            return 4, {}  # 无奖励可领取

        index = reward_list.index(days)
        reward_list.pop(index)
        reward = foundation_info['day%s' % days]
        gift = add_mult_gift(self.mm, reward)
        self.mm.foundation.save()
        rc, data = self.foundation_index()
        data['reward'] = gift
        return rc, data