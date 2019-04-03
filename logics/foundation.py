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
        end_date = game_config.active.get(self.mm.foundation.a_id, {}).get('end_time', '')
        if not end_date:
            end_time = 0
        else:
            end_time = int(time.mktime(time.strptime(end_date, '%Y-%m-%d %H:%M:%S')) - time.time())
            end_time = end_time if end_time > 0 else 0
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
        foundation = self.mm.foundation
        f_active_date = foundation.activate_mark[f_id]
        f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
        active_days = (datetime.date.today() - f_active_date).days + 1
        reward_list = foundation.reward_dict[f_id]
        foundation_info = game_config.get_foundation_mapping().get(foundation.version)[f_id]

        if days not in reward_list or active_days < days:
            return 4, {}  # 无奖励可领取

        index = reward_list.index(days)
        reward_list.pop(index)
        reward = foundation_info['day%s' % days]
        gift = add_mult_gift(self.mm, reward)
        self.mm.foundation.save()
        _, data = self.foundation_index()
        data['reward'] = gift
        return 0, data