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
        withdraw_log: {withdraw_time: {activate_time, f_id, period_of_reward, gift}, ... },
        withdraw_log: {143221233: {140110000, 2, 5, [[2,0,1000]]}, ... },
        score_history: {'2014-09-15': 3000, ...},
        activate_mark: { fid_1: '140143532', ...},
        reward_dict: {f_id1: {1: [[1,0,2000], [6,1255, 1]], 2:[[2,0,1555]], ... }, f_id2:{...}, ... },
        score_anchor: 142311989
        """
        self.uid = uid
        # self.inreview_index = 127
        # self.active_inreview = 508   # 活动的编号
        self._attrs = {
            'version': 0,  # 版本号
            'withdraw_log': {},  # 领取基金信息
            'score': 0,  # 本次活动期间充值钻石数
            'activate_mark': {},  # 各类基金激活的日期
            'reward_dict': {},  # 统计未被领取的奖励
            # 'score_anchor': None,  # to prevent score jump between multiple period of activity  #基金积分清除
            # 'mail_mark': False,  # 以邮件的形势发放
            # 'happy_ending': False,  # 最大奖的展示
        }
        super(Foundation, self).__init__(self.uid)

    def pre_use(self):
        if not self.is_open():
            return
        if self.version != self.get_version():
            self.refresh()
        self.get_foundation_status()
        self.save()

    def get_version(self):
        _, version = get_version_by_active_id(active_id=self.ACTIVE_TYPE)
        return version

    def refresh(self):
        self.version = self.get_version()
        self.withdraw_log = {}
        self.score = 0
        self.activate_mark = {}
        self.reward_dict = {}

    def is_open(self):
        if self.get_version():
            return True
        return False

    def add_score(self, order_diamond):
        self.score += order_diamond
        self.save()

    def get_foundation_status(self):
        for f_id, foundation_info in game_config.foundation.iteritems():
            if foundation_info['version'] != self.version:
                continue

            if self.score >= foundation_info['need_coin'] and f_id not in self.reward_dict:
                self.activate_mark[f_id] = time.strftime('%F')
                reward_dict = [0]  # 预先填充大奖
                for key, value in foundation_info.iteritems():
                    if key.startswith('day'):
                        day = int(key.split('day')[1])
                        reward_dict.append(day)
                self.reward_dict[f_id] = sorted(reward_dict)

ModelManager.register_model('foundation', Foundation)