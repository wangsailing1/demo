#! --*-- coding: utf-8 --*--

import time

from gconfig import game_config
from tools.gift import add_mult_gift



class ActiveCard(object):
    """ 月卡至尊卡逻辑
    """
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, mm):
        self.mm = mm
        self.active_card = self.mm.active_card

    def show(self):
        month_card_config = game_config.month_privilege
        if not month_card_config:
            return {}
        show_data = {}
        if not self.active_card.reward_info:
            for k, v in month_card_config.iteritems():
                show_data[k] = {'status': 0, 'remain_time': 0, 'had_receive': 0}
            return show_data
        else:
            for k, v in month_card_config.iteritems():
                status = self.active_card.reward_info.get(k, {}).get('status', 0)
                remain_time = self.active_card.reward_info.get(k, {}).get('remain_time', 0)
                had_receive = self.active_card.reward_info.get(k, {}).get('had_receive', 0)
                show_data[k] = {'status': status, 'remain_time': remain_time, 'had_receive': had_receive}
            return show_data

    def receive(self, active_id):
        month_card_config = game_config.month_privilege
        if not month_card_config:
            return 1, {}        # 无该配置
        status = self.active_card.reward_info.get(active_id, {}).get('status', 0)
        if status == 0:
            return 2, {}        # 尚未激活
        if status == 2:
            return 3, {}        # 已领取
        if status == 1:
            # 兑换
            reward = {}
            reward = add_mult_gift(self.mm, month_card_config[active_id]['daily_rebate'], reward)
            if not reward:
                return 4, {}        # 配置错误
            _format = "%Y-%m-%d"
            today_time = time.strftime(_format)
            self.active_card.reward_info[active_id]['status'] = 2
            self.active_card.reward_info[active_id]['last_receive'] = today_time
            diamond_num = reward.get('diamond', 0)
            self.active_card.reward_info[active_id]['had_receive'] += diamond_num
            self.active_card.save()
            return 0, {'reward': reward}