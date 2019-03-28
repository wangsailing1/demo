#!/usr/bin/python
# encoding: utf-8


# import time
from lib.db import ModelBase
# from gconfig import game_config
from lib.core.environ import ModelManager
from lib.utils.active_inreview_tools import get_version_by_active_id


# 钻石福利基金
class RmbFoundation(ModelBase):
    """
    User make foundation for themselves
    """
    # _need_diff = ('items',)
    ACTIVE_TYPE = 2012

    def __init__(self, uid=None):
        """
        version: 1
        activate_mark: {
            1: "2019-03-01",
        }
        withdraw_log: {

        }
        reward_dict: {
            1: [3, 4, 5, 6, 7]  # 记录第几天的奖励未被领取
        }
        """
        self.uid = uid

        self._attrs = {
            'version': 0,  # 版本号
            # 'withdraw_log': {},  # 领取基金信息
            'activate_mark': {},  # 各类基金激活的日期
            'reward_dict': {},  # 统计未被领取的奖励
            'a_id':0,
        }

        super(RmbFoundation, self).__init__(self.uid)

    def pre_use(self):
        # if not self.is_open():
        if self.can_open():
            if not self.a_id:
                self.a_id, _ = self.get_version()
                self.save()
            return
        if self.version != self.get_version():
            self.refresh()
        self.get_foundation_status()
        self.save()

    def get_version(self):
        a_id, version = get_version_by_active_id(active_id=self.ACTIVE_TYPE)
        return a_id, version

    def refresh(self):
        self.a_id, self.version = self.get_version()
        self.score = 0

    def is_open(self):
        a_id , version = self.get_version()
        if version:
            return True
        return False

    def can_open(self):
        tag = 0
        for days, reward_list in self.reward_dict.iteritems():
            if reward_list:
                tag = 1
                break
        if tag or self.get_version():
            return True
        return False


    # def add_score(self, order_diamond):
    #     if not self.is_open():
    #         return
    #     self.score += order_diamond
    #     self.save()

    # def get_foundation_status(self):
    #     for f_id, foundation_info in game_config.foundation.iteritems():
    #         if foundation_info['version'] != self.version:
    #             continue
    #
    #         if self.score >= foundation_info['need_coin'] and f_id not in self.reward_dict:
    #             self.activate_mark[f_id] = time.strftime('%F')
    #             reward_dict = []
    #             for key, value in foundation_info.iteritems():
    #                 if key.startswith('day'):
    #                     day = int(key.split('day')[1])
    #                     reward_dict.append(day)
    #             self.reward_dict[f_id] = sorted(reward_dict)

ModelManager.register_model('rmbfoundation', RmbFoundation)