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
        show_data['double_pay_id'] = self.mm.user_payment.get_double_pay()
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
            return 1, {}  # 无该配置
        status = self.active_card.reward_info.get(active_id, {}).get('status', 0)
        if status == 0:
            return 2, {}  # 尚未激活
        if status == 2:
            return 3, {}  # 已领取
        if status == 1:
            # 兑换
            reward = {}
            reward = add_mult_gift(self.mm, month_card_config[active_id]['daily_rebate'], reward)
            if not reward:
                return 4, {}  # 配置错误
            _format = "%Y-%m-%d"
            today_time = time.strftime(_format)
            self.active_card.reward_info[active_id]['status'] = 2
            self.active_card.reward_info[active_id]['last_receive'] = today_time
            diamond_num = reward.get('diamond', 0)
            self.active_card.reward_info[active_id]['had_receive'] += diamond_num
            self.active_card.save()
            return 0, {'reward': reward}


class SevenLoginLogic(object):
    """
    七日登录
    """

    def __init__(self, mm):
        self.mm = mm
        self.seven_login = self.mm.seven_login

    def seven_login_index(self):
        """
        七日登录index
        :return:
        """
        if not self.seven_login.is_open():
            return 1, {}    # 活动已结束

        data = {
            'days': self.seven_login.days,  # 登录天数
            'got': self.seven_login.got,    # 已领取id
            'can_get_reward':self.seven_login.can_get_reward()
        }

        return 0, data

    def seven_login_award(self):
        """
        领取七日登录奖励
        :param day_id:
        :return:
        """
        if not self.seven_login.is_open():
            return 3, {}    # 活动已结束
        day_id = self.seven_login.days
        if not self.seven_login.can_receive(day_id):
            return 1, {}    # 条件不足，不能领取
        now = time.strftime(self.seven_login.FORMAT)
        if day_id in self.seven_login.got or now == self.seven_login.refresh:
            return 2, {}    # 已领取

        log_reward_config = game_config.sign_first_week.get(day_id)
        if not log_reward_config:
            return 'error_config', {}

        self.seven_login.add_got(day_id)

        reward = {}
        add_mult_gift(self.mm, log_reward_config['reward'], reward)
        self.seven_login.refresh = time.strftime(self.seven_login.FORMAT)
        self.seven_login.days += 1

        self.seven_login.save()

        data = {
            'reward': reward,
            'seven_login_flag': self.seven_login.is_open(),  # 七日登录图标
            'seven_login_num': self.seven_login.get_next_reward_day(),  # 获取下次可以领取的天数
        }
        _, data1 = self.seven_login_index()
        data.update(data1)

        return 0, data


class MonthlySignLogic(object):
    """ 每日签到

    """

    def __init__(self, mm):
        self.mm = mm
        self.monthly_sign = self.mm.monthly_sign

    def index(self):
        """ 首页

        :return:
        """

        monthly_sign = self.monthly_sign.monthly_sign
        result = {
            'today_can_sign': self.monthly_sign.today_can_sign(),
            'days': monthly_sign['days'],
            # 'usable_days': monthly_sign['usable_days'],
            'config': monthly_sign['reward'],
        }
        return result

    def sign(self):
        """ 签到

        :return:
        """
        monthly_sign = self.monthly_sign.monthly_sign
        today = time.strftime('%F')

        if not monthly_sign['usable_days']:
            return 1, {}

        gifts = monthly_sign['reward'][monthly_sign['days']]
        reward = add_mult_gift(self.mm, gifts)

        monthly_sign['days'] += 1
        monthly_sign['usable_days'] -= 1
        monthly_sign['date'] = today

        self.monthly_sign.save()

        result = {
            'reward': reward,
        }
        result.update(self.index())

        return 0, result

