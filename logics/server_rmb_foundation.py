#! --*-- coding: utf-8 --*--

import time
import datetime
from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils.active_inreview_tools import get_inreview_version
from lib.utils.time_tools import strftimestamp, datetime_to_timestamp

class ServerRmbFoundation(object):

    def __init__(self, mm=None):
        self.mm = mm
        self.rmbfoundation = self.mm.serverrmbfoundation

    def server_rmbfoundation_index(self):
        data = {}
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.rmbfoundation.ACTIVE_TYPE)
        end_date = strftimestamp(datetime_to_timestamp(e_time))
        if not version:
            end_time = 0
        else:
            end_time = int(time.mktime(time.strptime(end_date, '%Y-%m-%d %H:%M:%S')) - time.time())
            end_time = end_time if end_time > 0 else 0
        data['end_time'] = end_time
        data['version'] = self.rmbfoundation.version
        data['rmbf_active_dates'] = {}
        for f_id, f_active_date in self.rmbfoundation.activate_mark.iteritems():
            f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
            data['rmbf_active_dates'][f_id] = (datetime.date.today() - f_active_date).days + 1
        data['reward_dict'] = self.rmbfoundation.reward_dict
        return 0, data


    def server_withdraw(self, f_id, days):
        f_active_date = self.rmbfoundation.activate_mark[f_id]
        f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
        active_days = (datetime.date.today() - f_active_date).days + 1
        reward_list = self.rmbfoundation.reward_dict[f_id]
        config = game_config.get_rmbfoundation_mapping()
        rmbfoundation_info = config.get(self.rmbfoundation.version, {}).get(f_id, {})
        if not rmbfoundation_info:
            return 5, {}  # 基金活动配置错误

        if days not in reward_list or active_days < days:
            return 4, {}  # 无奖励可领取

        index = reward_list.index(days)
        reward_list.pop(index)
        reward = rmbfoundation_info['day%s' % days]
        gift = add_mult_gift(self.mm, reward)
        self.rmbfoundation.save()
        rc, data = self.server_rmbfoundation_index()
        data['reward'] = gift
        return rc, data