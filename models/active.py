#! --*-- coding: utf-8 --*--

import time
import datetime
import copy

from lib.core.environ import ModelManager
from gconfig import game_config
from lib.db import ModelBase


class ActiveCard(ModelBase):
    """
    月卡至尊卡卡活动
    """

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'reward_info': {},
            'his_record': [],  # 购买过的月卡
        }
        super(ActiveCard, self).__init__(self.uid)

    def pre_use(self):
        user_card = self.reward_info
        if not user_card:
            return 0
        _format = "%Y-%m-%d"
        today_time = time.strftime(_format)
        one_day = 3600 * 24
        month_card_config = game_config.month_privilege
        if month_card_config:
            reward_data = copy.deepcopy(self.reward_info)
            now = int(time.time())
            for k, v in reward_data.iteritems():
                effective_days = month_card_config[k]['effective_days']
                remain_time = effective_days * 3600 * 24 + v['buy_time'] - now
                remain_day = (one_day + remain_time - 1) // one_day
                if k != 2:
                    self.reward_info[k]['remain_time'] = remain_day
                if self.reward_info[k]['last_receive'] != today_time:
                    self.reward_info[k]['status'] = 1
                if remain_time <= 0 and k != 2:  # 结束删除数据
                    self.reward_info.pop(k)
            self.save()

    def record(self, charge_id):
        today = datetime.date.today()
        time_0 = time.mktime(today.timetuple())
        month_card_config = game_config.month_privilege
        self.reward_info[charge_id] = {
            'status': 1,
            'remain_time': month_card_config[charge_id]['effective_days'],
            'last_receive': '',
            'had_receive': 0,
            'buy_time': time_0,
        }

        self.save()

    def get_status(self, tp):
        """
        获取月卡、至尊卡状态
        :param tp: 1:月卡，2:至尊卡
        status:0未激活1能领奖2已领奖
        :return:
        """
        return self.reward_info.get(tp, {}).get('status', 0)

    def is_alert(self):
        not_alert = False
        month_card_config = game_config.month_privilege
        reward_info = self.reward_info
        if not reward_info or not month_card_config:
            return not_alert
        for k, v in reward_info.iteritems():
            if v['status'] == 1:
                return True
        return not_alert

    def month_remain_times(self):
        """月卡剩余次数"""
        if self.get_status(1):
            return int(self.reward_info[1]['remain_time'])
        else:
            return 0


ModelManager.register_model('active_card', ActiveCard)
