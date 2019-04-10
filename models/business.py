#! --*-- coding: utf-8 --*--


import time
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils.time_tools import timestamp_day
from lib.utils import weight_choice


class Business(ModelBase):
    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'last_recover_time': 0,  # 最近刷新时间
            'recover_times': 0,  # 刷新次数
            'last_date': '',  # 最近登陆日期
            'business_times': game_config.common[68],  # 初始值 事物次数
            'business_id': 0,
            'business_done': [],
        }
        super(Business, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        now = int(time.time())
        save = False
        if self.last_date != today:
            self.last_date = today
            self.last_recover_time = int(timestamp_day())
            self.recover_times = 0
            self.business_done = []
            # save = True
        recover_need_time = self.business_recover_need_time()
        if recover_need_time:
            div, mod = divmod(now - self.last_recover_time, recover_need_time)
            while div and self.can_recover_business_times():
                if self.business_times >= game_config.common[68]:
                    self.last_recover_time = now
                    break
                self.business_times += 1
                self.recover_times += 1
                self.last_recover_time += recover_need_time
                recover_need_time = self.business_recover_need_time()
                if not recover_need_time:
                    break
                div, mod = divmod(now - self.last_recover_time, recover_need_time)
            if not self.can_recover_business_times():
                self.last_recover_time = now
            # save = True
        if self.business_times and not self.business_id:
            self.business_id = self.get_business_id()
            self.business_log = []
            save = True
        if save:
            self.save()

    def get_business_id(self):
        if not self.business_times:
            return 0
        weights = self.get_business_weight()
        weight = self.business_done[-1] if self.business_done else 0
        while True:
            choice_id = weight_choice(weights)[0]
            if choice_id != weight:
                weight = choice_id
                break
        return weight

    def get_business_weight(self):
        weights = []
        config = game_config.business
        for id, value in config.iteritems():
            if not value['pre_type']:
                weights.append([id,value['rate']])
            elif value['pre_num1'] in self.mm.card.group_ids:
                weights.append([id, value['rate']])
        return weights

    def business_recover_need_time(self):
        config = game_config.business_times
        for _, v in config.iteritems():
            if v['time'][0] <= self.recover_times <= v['time'][1]:
                return v['cd'] * 60
        build_effect = self.mm.user.build_effect
        effect_time = build_effect.get(2, 0)
        return config[max(config.keys())]['cd'] * 60 - effect_time

    def can_recover_business_times(self):
        if self.business_times >= game_config.common[68]:
            return False
        return self.recover_times < game_config.common[69]  # 恢复最大次数取配置

    def get_all_done(self):
        return not self.business_times and self.recover_times >= game_config.common[69]

    def business_recover_expire(self):
        """恢复倒计时"""
        if not game_config.business:
            return 0

        if not self.can_recover_business_times():
            return 0
        need_time = self.business_recover_need_time()
        return need_time - (int(time.time()) - self.last_recover_time)


    def get_red_dot(self):
        return True if self.business_times else False


ModelManager.register_model('business', Business)
