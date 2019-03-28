#!/usr/bin/python
# encoding: utf-8


import time
from lib.db import ModelBase
from gconfig import game_config
from lib.core.environ import ModelManager
from lib.utils.active_inreview_tools import get_version_by_active_id


# 钻石福利基金
class Foundation(ModelBase):
    """
    User make foundation for themselves
    """
    # _need_diff = ('items',)
    ACTIVE_TYPE = 2009

    def __init__(self, uid=None):
        """
                       # 领取基金的时间  活动的开启时间   基金类型  第几天
        activate_mark: { fid_1: '140143532', ...},
        reward_dict: {f_id1: [3, 4, 5, 6, 7], ... },
        """
        self.uid = uid
        # self.inreview_index = 127
        # self.active_inreview = 508   # 活动的编号
        self._attrs = {
            'version': 0,  # 版本号
            'score': 0,  # 本次活动期间充值钻石数
            'activate_mark': {},  # 各类基金激活的日期
            'reward_dict': {},  # 统计未被领取的奖励
            'a_id': 0,
            # 'score_anchor': None,  # to prevent score jump between multiple period of activity  #基金积分清除
            # 'mail_mark': False,  # 以邮件的形势发放
            # 'happy_ending': False,  # 最大奖的展示
        }
        super(Foundation, self).__init__(self.uid)

    def pre_use(self):
        # if not self.is_open():
        if self.has_reward():
            self.get_foundation_status()
            self.save()
            return
        a_id, version = self.get_version()
        if self.version != version or self.a_id != a_id:
            self.refresh()
        self.get_foundation_status()
        self.save()

    def get_version(self):
        a_id, version = get_version_by_active_id(active_id=self.ACTIVE_TYPE)
        return a_id, version

    def refresh(self):
        if (self.a_id and self.version) or (not self.a_id and not self.version):
            self.score = 0
        self.a_id, self.version = self.get_version()


    def is_open(self):
        a_id , version = self.get_version()
        if version:
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
        for f_id, foundation_info in game_config.foundation.iteritems():
            if foundation_info['version'] != self.version:
                continue

            if self.score >= foundation_info['need_coin'] and f_id not in self.reward_dict:
                self.activate_mark[f_id] = time.strftime('%F')
                reward_dict = []
                for key, value in foundation_info.iteritems():
                    if key.startswith('day'):
                        day = int(key.split('day')[1])
                        reward_dict.append(day)
                self.reward_dict[f_id] = sorted(reward_dict)

ModelManager.register_model('foundation', Foundation)