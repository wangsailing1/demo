#! --*-- coding: utf-8 --*--
__author__ = 'ljm'

import time

from lib.db import ModelBase
from lib.core.environ import ModelManager
from models.vip_company import more_license


class Assistant(ModelBase):

    def __init__(self,uid=None):
        self.uid = uid
        self._attrs = {
            'assistant': 0,     # 是否激活助理
            'last_time': '',    # 最近操作日期
            'assistant_gift': 0,  # 助理特权奖励
            'assistant_daily': 0,  # 助理日常奖励
            'license_apply_times': 0,   # 许可证申请次数
            'license_apply_done_time': 0 # 许可证申请完成时间
        }
        super(Assistant, self).__init__(self.uid)

    def pre_use(self):
        if self.assistant:
            today = time.strftime('%F')
            if today != self.last_time:
                self.last_time = today
                self.assistant_daily = 0
                self.assistant_gift = 0
                self.license_apply_times = 0
                self.save()

    def open_assistant(self, sort):
        save = False
        if sort == 3:
            self.assistant = 1
            save = True
        elif sort == 4:
            self.assistant_gift = 1
            save = True
        if save:
            self.save()

    def get_max_time(self):
        return more_license(self.mm.user) + 1

    def get_status(self):
        """
        :return:  1 全部领取完 2，可领取，3可申请,4 申请中
        """
        now = int(time.time())
        if self.license_apply_times >= self.get_max_time() and self.license_apply_done_time == 0:
            return 1
        if self.license_apply_done_time != 0:
            if now >= self.license_apply_done_time:
                return 2
            else :
                return 4
        else:
            return 3



ModelManager.register_model('assistant',Assistant)
