#!/usr/bin/python
# encoding: utf-8

import time
import datetime
from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils.active_inreview_tools import get_inreview_version
from lib.utils.time_tools import strftimestamp, datetime_to_timestamp

class ServerFoundation(object):

    def __init__(self, mm=None):
        self.mm = mm
        self.foundation = self.mm.serverfoundation

    def server_foundation_index(self):
        data = {}
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.foundation.ACTIVE_TYPE)
        end_date = strftimestamp(datetime_to_timestamp(e_time))
        if not version:
            end_time = 0
        else:
            end_time = int(time.mktime(time.strptime(end_date, '%Y-%m-%d %H:%M:%S')) - time.time())
            end_time = end_time if end_time > 0 else 0
        data['end_time'] = end_time
        data['version'] = self.foundation.version
        data['score'] = self.foundation.score
        data['f_active_dates'] = {}
        for f_id, f_active_date in self.foundation.activate_mark.iteritems():
            f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
            data['f_active_dates'][f_id] = (datetime.date.today() - f_active_date).days + 1
        data['reward_dict'] = self.foundation.reward_dict
        return 0, data

    def server_withdraw(self, f_id, days):
        f_active_date = self.foundation.activate_mark[f_id]
        f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
        active_days = (datetime.date.today() - f_active_date).days + 1
        reward_list = self.foundation.reward_dict[f_id]
        foundation_info = game_config.get_server_foundation_mapping().get(self.foundation.version)[f_id]

        if days not in reward_list or active_days < days:
            return 4, {}  # 无奖励可领取

        index = reward_list.index(days)
        reward_list.pop(index)
        reward = foundation_info['day%s' % days]
        gift = add_mult_gift(self.mm, reward)
        self.foundation.save()
        _, data = self.server_foundation_index()
        data['reward'] = gift
        return 0, data