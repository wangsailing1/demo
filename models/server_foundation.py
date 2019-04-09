#!/usr/bin/python
# encoding: utf-8


import time
from lib.db import ModelBase
from gconfig import game_config
from lib.core.environ import ModelManager
from lib.utils.active_inreview_tools import get_inreview_version
from lib.utils.time_tools import strftimestamp, datetime_to_timestamp

# 新服钻石福利基金
class ServerFoundation(ModelBase):
    """
    User make foundation for themselves
    """
    # _need_diff = ('items',)
    ACTIVE_TYPE = 2014

    def __init__(self, uid=None):
        """
                       # 领取基金的时间  活动的开启时间   基金类型  第几天
        activate_mark: { fid_1: '140143532', ...},
        reward_dict: {f_id1: [3, 4, 5, 6, 7], ... },
        """
        self.uid = uid
        self._attrs = {
            'version': 0,  # 版本号
            'score': 0,  # 本次活动期间充值钻石数
            'activate_mark': {},  # 各类基金激活的日期
            'reward_dict': {},  # 统计未被领取的奖励
            'start_time': '',  # 开启时间
            'end_time': '',  # 结束时间
        }
        super(ServerFoundation, self).__init__(self.uid)

    def pre_use(self):
        if self.has_reward():
            self.get_foundation_status()
            self.save()
            return
        version, new_server, s_time, e_time = self.get_version()
        if self.version != version:
            self.version = version
            self.start_time = strftimestamp(datetime_to_timestamp(s_time))
            self.end_time = strftimestamp(datetime_to_timestamp(e_time))
            self.save()
        self.get_foundation_status()
        self.save()

    def get_version(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_TYPE)
        return version, new_server, s_time, e_time


    def is_open(self):
        if self.version:
            return True
        return False

    def has_reward(self):
        tag = 0
        for days, reward_list in self.reward_dict.iteritems():
            if reward_list:
                tag = 1
                break
        if tag :
            return True
        return False

    def add_score(self, order_diamond):
        if not self.is_open():
            return
        self.score += order_diamond
        self.save()

    def get_foundation_status(self):
        for f_id, foundation_info in game_config.server_foundation.iteritems():
            if foundation_info['version'] != self.version:
                continue
            id = foundation_info['id']
            if self.score >= foundation_info['need_coin'] and id not in self.reward_dict:
                self.activate_mark[id] = time.strftime('%F')
                reward_dict = []
                for key, value in foundation_info.iteritems():
                    if key.startswith('day'):
                        day = int(key.split('day')[1])
                        reward_dict.append(day)
                self.reward_dict[id] = sorted(reward_dict)

ModelManager.register_model('serverfoundation', ServerFoundation)