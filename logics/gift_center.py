#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time

from lib.utils import not_repeat_weight_choice_2
from tools.gift import add_mult_gift, add_mult_gift_by_weights
from lib.utils.timelib import now_time_to_str, datetime_to_str
from gconfig import game_config


class GiftCenterLogic(object):

    def __init__(self, mm):
        self.mm = mm
        self.gift_center = self.mm.gift_center

    def index(self):
        """ 首页

        :return:
        """
        cur_time_str = now_time_to_str()
        cur_level = self.mm.user.level
        result = {}
        for welfare_id, config in game_config.welfare.iteritems():
            start_time = config['start_time']
            end_time = config['end_time']
            if not config['is_show'] or cur_level < config['level']:
                continue

            if config['time_sort'] == 1:    # 永久显示
                result[welfare_id] = True

            elif config['time_sort'] == 2 and start_time <= cur_time_str <= end_time:
                result[welfare_id] = True

            elif config['time_sort'] == 3:  # 领完奖励不再显示
                if welfare_id == 6:     # 在线奖励
                    logic = OnlineDurationLogics(self.mm)
                    if not logic.all_reward_done():
                        result[welfare_id] = True
                elif welfare_id == 7:   # 等级奖励
                    logic = LevelGiftLogics(self.mm)
                    if not logic.all_reward_done():
                        result[welfare_id] = True

            elif config['time_sort'] == 4:  # 特殊条件
                if welfare_id == 10:    # 福利基金
                    if self.mm.growth_fund.is_open():
                        result[welfare_id] = True
                elif welfare_id == 12:  # 开服狂欢
                    data = self.mm.rank_reward_show.show()
                    if data.get('show_sort'):
                        result[welfare_id] = True

            # if welfare_id == 1:     # 签到
            #     logic = MonthlySignLogic(self.mm)
            # elif welfare_id == 2:   # 累计登录
            #     logic = WelfareLoginLogics(self.mm)
            # elif welfare_id == 3:   # 登录翻牌
            #     logic = WelfareCardLoginLogics(self.mm)
            # elif welfare_id == 4:   # 三顾茅庐
            #     logic = WelfareThreeDayLogics(self.mm)
            # if welfare_id == 5:   # 领取体力
            #     logic = EnergyLogics(self.mm)
            # elif welfare_id == 6:   # 累计在线
            #     logic = OnlineDurationLogics(self.mm)
            # elif welfare_id == 7:   # 等级礼包
            #     logic = LevelGiftLogics(self.mm)
            # elif welfare_id == 8:   # 公告
            #     result[welfare_id] = True
            #     continue
            # else:
            #     continue
            # data = logic.index()
            # result[welfare_id] = True

        return {
            'gift_data': result,
        }


class MonthlySignLogic(object):
    """ 每日签到

    """

    def __init__(self, mm):
        self.mm = mm
        self.gift_center = self.mm.gift_center

    def index(self):
        """ 首页

        :return:
        """
        if not self.gift_center.is_open(self.gift_center.WELFARE_SIGN):
            return {}

        self.gift_center.enter_game()
        monthly_sign = self.gift_center.monthly_sign
        result = {
            'today_can_sign': self.gift_center.today_can_sign(),
            'days': monthly_sign['days'],
            # 'usable_days': monthly_sign['usable_days'],
            'config': monthly_sign['reward'],
            'welfare': self.gift_center.get_gift_center_red_dot(),  # 小红点
        }
        return result

    def sign(self):
        """ 签到

        :return:
        """
        monthly_sign = self.gift_center.monthly_sign
        today = time.strftime('%F')

        if not monthly_sign['usable_days']:
            return 1, {}

        gifts = monthly_sign['reward'][monthly_sign['days']]
        reward = add_mult_gift(self.mm, gifts)

        monthly_sign['days'] += 1
        monthly_sign['usable_days'] -= 1
        monthly_sign['date'] = today

        self.gift_center.save()

        result = {
            'reward': reward,
        }
        result.update(self.index())

        return 0, result


# class WelfareLoginLogics(object):
#     """
#     累积登陆
#     """
#     def __init__(self, mm):
#         self.mm = mm
#         self.gift_center = self.mm.gift_center
#
#     def index(self):
#         """
#         首页
#         :return:
#         """
#         if not self.gift_center.is_open(self.gift_center.WELFARE_LOGIN):
#             return {}
#
#         self.gift_center.enter_game()
#
#         result = self.gift_center.daily_login
#         result['welfare'] = self.gift_center.get_gift_center_red_dot()  # 小红点
#
#         return result
#
#     def award(self, reward_id):
#         """
#         领取累积登陆奖励
#         :param reward_id:
#         :return:
#         """
#         welfare_login_config = game_config.welfare_login.get(reward_id, {})
#         if not welfare_login_config:
#             return 1, {}    # 没有配置
#
#         if self.gift_center.is_welfare_login_awarded(reward_id):
#             return 2, {}    # 已领取
#
#         if not self.gift_center.can_welfare_login_award(reward_id):
#             return 3, {}    # 条件不足
#
#         reward = {}
#         # vip = welfare_login_config['vip']
#         # if vip:
#         #     if self.mm.user.vip >= vip:
#         #         add_mult_gift(self.mm, welfare_login_config['compensate'], reward)
#         #     else:
#         #         self.mm.user.vip = vip
#         #         self.mm.user.vip_exp = 0
#         #         self.mm.user.save()
#
#         add_mult_gift(self.mm, welfare_login_config['reward'], reward)
#         self.gift_center.welfare_login_award(reward_id)
#
#         self.gift_center.save()
#
#         result = {
#             'reward': reward
#         }
#         result.update(self.index())
#
#         return 0, result


class WelfareCardLoginLogics(object):
    """
    连续登陆翻牌
    """

    def __init__(self, mm):
        self.mm = mm
        self.gift_center = self.mm.gift_center

    def index(self):
        """
        首页
        :return:
        """
        if not self.gift_center.is_open(self.gift_center.WELFARE_CARD_LOGIN):
            return {}

        self.gift_center.enter_game()

        return {
            'login_days': self.gift_center.card_login['login_days'],    # 当前连续登陆天数
            'card_times': self.gift_center.get_card_login_times(),      # 可翻牌次数
            'welfare': self.gift_center.get_gift_center_red_dot(),  # 小红点
        }

    def open_card(self):
        """
        翻牌
        :return:
        """
        if not self.gift_center.has_card_login_times():
            return 1, {}    # 剩余次数不足

        login_days = self.gift_center.get_card_login_days()
        welfare_card_login_config = game_config.welfare_card_login.get(login_days, {})
        if not welfare_card_login_config:
            return 2, {}    # 没有配置

        self.gift_center.decr_card_login_times()

        reward_total = welfare_card_login_config['reward_total']
        gifts = not_repeat_weight_choice_2(reward_total, num=3)
        gifts = [i[:3] for i in gifts]
        gift = gifts.pop(0)

        reward = add_mult_gift(self.mm, [gift])

        self.gift_center.save()

        data = {
            'reward': reward,
            'gift': gift,
            'other_gifts': gifts,
        }
        data.update(self.index())

        return 0, data


class WelfareThreeDayLogics(object):
    """
    三顾茅庐
    """

    def __init__(self, mm):
        self.mm = mm
        self.gift_center = self.mm.gift_center

    def index(self):
        """
        三顾茅庐首页
        :return:
        """
        if not self.gift_center.is_open(self.gift_center.WELFARE_THREE_DAYS):
            return {}

        data = {
            'login_days': self.gift_center.three_days_login['login_days'],  # 连续登陆天数
            'got_ids': self.gift_center.three_days_login['got_ids'],        # 已领奖的id
            'can_award': self.gift_center.three_days_login['usable_days'],  # 今天是否领奖
            'welfare': self.gift_center.get_gift_center_red_dot(),  # 小红点
        }

        return data

    def award(self, day_id):
        """
        三顾茅庐领奖
        :param day_id: 第几天的奖励
        :return:
        """
        if not self.gift_center.three_days_login['usable_days']:
            return 1, {}    # 今天已领

        got_ids = self.gift_center.three_days_login['got_ids']
        if day_id in got_ids:
            return 2, {}    # 已领取

        if (not got_ids and day_id != 1) or (got_ids and day_id != max(got_ids) + 1):
            return 3, {}    # 前面的奖励还未领取

        day_reward = self.gift_center.three_days_login['reward']
        gifts = day_reward.get(day_id, [])
        if not gifts:
            return 4, {}    # 没有奖励配置

        self.gift_center.three_days_award(day_id)
        reward = add_mult_gift(self.mm, gifts)

        self.gift_center.save()

        data = {
            'reward': reward
        }
        data.update(self.index())

        return 0, data


class OnlineDurationLogics(object):
    """
    累计在线
    """
    def __init__(self, mm):
        self.mm = mm
        self.gift_center = self.mm.gift_center

    def index(self):
        """
        累计在线首页
        :return:
        """
        got_ids = self.gift_center.online_duration['got_ids']

        if not self.gift_center.is_open(self.gift_center.WELFARE_ONLINE) or len(got_ids) >= len(game_config.welfare_online):
            return {}

        data = {
            'got_ids': got_ids,             # 已领取奖励配置id
            'online_time': self.gift_center.online_duration['online_time'],  # 开始计时时间
            'welfare': self.gift_center.get_gift_center_red_dot(),  # 小红点
        }

        return data

    def all_reward_done(self):
        """
        是否已领取所有奖励
        :return:
        """
        got_ids = self.gift_center.online_duration['got_ids']
        is_done = set(game_config.welfare_online.keys()) - set(got_ids) == set()
        return is_done

    def award(self, reward_id):
        """
        累计在线领取奖励
        :param reward_id:
        :return:
        """
        welfare_online_config = game_config.welfare_online.get(reward_id, {})
        if not welfare_online_config:
            return 1, {}    # 没有奖励配置

        got_ids = self.gift_center.online_duration['got_ids']
        if reward_id in got_ids:
            return 3, {}    # 已领取

        if (not got_ids and reward_id != 1) or (got_ids and reward_id != max(got_ids) + 1):
            return 4, {}    # 前面的奖励还未领取

        remain_time = self.gift_center.get_online_duration_remain_time(reward_id)
        if remain_time > 0:
            return 2, {}    # 还没到时间

        gift = welfare_online_config['reward']

        reward = add_mult_gift(self.mm, gift)

        self.gift_center.online_award(reward_id)
        self.gift_center.save()

        data = {
            'reward': reward
        }
        data.update(self.index())

        return 0, data


class LevelGiftLogics(object):
    """
    等级礼包
    """
    def __init__(self, mm):
        self.mm = mm
        self.gift_center = self.mm.gift_center

    def index(self):
        """
        等级礼包首页
        :return:
        """
        if not self.gift_center.is_open(self.gift_center.WELFARE_LEVEL):
            return {}

        got_ids = self.gift_center.level_gift['got_ids']

        return {
            'got_ids': got_ids,     # 已领取的id
            'welfare': self.gift_center.get_gift_center_red_dot(),  # 小红点
        }

    def all_reward_done(self):
        """
        是否已领取所有奖励
        :return:
        """
        got_ids = self.gift_center.level_gift['got_ids']
        is_done = set(game_config.welfare_level.keys()) - set(got_ids) == set()
        return is_done

    def award(self, reward_id):
        """
        等级礼包领取奖励
        :param reward_id:
        :return:
        """
        if reward_id in self.gift_center.level_gift['got_ids']:
            return 1, {}    # 已领取

        welfare_level_config = game_config.welfare_level.get(reward_id, {})
        if not welfare_level_config:
            return 2, {}    # 没有配置

        if self.mm.user.level < welfare_level_config['level']:
            return 3, {}    # 等级不足

        gift = welfare_level_config['reward']
        reward = add_mult_gift(self.mm, gift)
        self.gift_center.level_gift_award(reward_id)

        self.gift_center.save()

        data = {
            'reward': reward,
        }
        data.update(self.index())

        return 0, data


class EnergyLogics(object):
    """
    领取体力
    """
    def __init__(self, mm):
        self.mm = mm
        self.gift_center = self.mm.gift_center

    def index(self):
        """
        领取体力界面
        :return:
        """
        if not self.gift_center.is_open(self.gift_center.WELFARE_ENERGY):
            return {}

        data = {
            'got_ids': self.gift_center.energy['got_ids'],
            'welfare': self.gift_center.get_gift_center_red_dot(),  # 小红点
        }

        return data

    def get_energy(self, energy_id):
        """
        领取体力
        :param energy_id:
        :return:
        """
        config = game_config.welfare_energy.get(energy_id, {})
        if not config:
            return 1, {}    # 没有领取体力的配置

        hour = time.strftime('%H:%M:%S')
        start, end = config['time_rage']
        if not (start <= hour <= end):
            return 2, {}    # 领奖时间已过

        if self.gift_center.energy_has_received(energy_id):
            return 3, {}    # 已领取

        self.gift_center.receive_energy(energy_id)
        reward = add_mult_gift(self.mm, [[20, 0, config['power']]])
        reward = add_mult_gift_by_weights(self.mm, config['extra_reward'], cur_data=reward)

        self.gift_center.save()

        result = {
            'reward': reward,
        }
        result.update(self.index())

        return 0, result


# class PaySignLogic(object):
#     """ 每日豪华签到
#
#     """
#
#     def __init__(self, mm):
#         self.mm = mm
#         self.gift_center = self.mm.gift_center
#
#     def index(self):
#         """ 首页
#
#         :return:
#         """
#         pay_sign = self.gift_center.pay_sign
#         result = {
#             'today_can_sign': self.today_can_sign(),
#             'days': pay_sign['days'],
#             'usable_days': pay_sign['usable_days'],
#             'version': pay_sign['version'],
#             'pay': pay_sign['pay'],
#             'config': pay_sign['reward'],
#         }
#         return result
#
#     def today_can_sign(self):
#         """ 今天能否签
#
#         :return:
#         """
#         cur_time = datetime_to_str(self.gift_center.today, datetime_format='%Y-%m-%d')
#
#         pay_sign = self.gift_center.pay_sign
#         return 1 if cur_time != pay_sign['date'] else 0
#
#     def sign(self):
#         """ 签到
#
#         :return:
#         """
#         pay_sign = self.gift_center.pay_sign
#
#         if not pay_sign['usable_days']:
#             return 1, {}
#
#         gifts = pay_sign['reward'][pay_sign['days']]
#         reward = add_mult_gift(self.mm, gifts)
#
#         pay_sign['days'] += 1
#         pay_sign['usable_days'] -= 1
#
#         self.gift_center.save()
#
#         result = {
#             'reward': reward,
#         }
#         result.update(self.index())
#
#         return 0, result
#
#
# class FirstWeekSignLogic(object):
#     """  首周签到
#
#     """
#
#     def __init__(self, mm):
#         self.mm = mm
#         self.gift_center = self.mm.gift_center
#
#     def can_sign(self):
#         """ 能否签
#
#         :return:
#         """
#         cur_time = now_time_to_str(datetime_format='%Y-%m-%d')
#         first_week_sign = self.gift_center.first_week_sign
#         if cur_time != first_week_sign['date'] and len(first_week_sign['reward']) > first_week_sign['days']:
#             return 1
#         else:
#             return 0
#
#     def index(self):
#         """ 首页
#
#         :return:
#         """
#         first_week_sign = self.gift_center.first_week_sign
#
#         result = {
#             'days': first_week_sign['days'],
#             'today_can_sign': self.can_sign(),
#             'config': first_week_sign['reward'],
#         }
#         return result
#
#     def sign(self):
#         """ 签到
#
#         :return:
#         """
#         first_week_sign = self.gift_center.first_week_sign
#
#         if not self.can_sign():
#             return 1, {}
#
#         first_week_sign['date'] = now_time_to_str(datetime_format='%Y-%m-%d')
#
#         gifts = first_week_sign['reward'][first_week_sign['days']]
#         reward = add_mult_gift(self.mm, gifts)
#
#         first_week_sign['days'] += 1
#
#         self.gift_center.save()
#
#         result = {
#             'reward': reward,
#         }
#         result.update(self.index())
#
#         return 0, result
#
#
# class FirstPaymentLogic(object):
#     """  首充
#
#     """
#
#     def __init__(self, mm):
#         self.mm = mm
#         self.gift_center = self.mm.gift_center
#
#     def can_award(self):
#         """ 能否领奖
#
#         :return:
#         """
#         return self.gift_center.first_payment['status'] == 1
#
#     def index(self):
#         """ 首页
#
#         :return:
#         """
#
#         result = {
#             'status': self.gift_center.first_payment['status'],
#         }
#         return result
#
#     def award(self):
#         """ 领奖
#
#         :return:
#         """
#         first_payment = self.gift_center.first_payment
#
#         if not self.can_award():
#             return 1, {}
#
#         first_charge_reward_id = max(game_config.first_charge_reward)
#         first_charge_reward_config = game_config.first_charge_reward[first_charge_reward_id]
#
#         gifts = first_charge_reward_config['reward']
#         reward = add_mult_gift(self.mm, gifts)
#
#         first_payment['status'] = 2
#
#         self.gift_center.save()
#
#         result = {
#             'reward': reward,
#             'status': first_payment['status'],
#         }
#
#         return 0, result
#
#
# class LevelLimitGiftLogic(object):
#     """  等级限时礼包
#
#     """
#
#     def __init__(self, mm):
#         self.mm = mm
#         self.gift_center = self.mm.gift_center
#
#     def index(self):
#         """ 首页
#
#         :return:
#         """
#
#         result = {
#             'level': self.gift_center.level_limit_gift['level'],
#             'rem_time': self.rem_time(),
#         }
#         return result
#
#     def rem_time(self):
#         """ 剩余时间
#
#         :return:
#         """
#         level_limit_gift = self.gift_center.level_limit_gift
#         if not level_limit_gift['expire_time']:
#             return 0
#         return max(level_limit_gift['expire_time'] - int(time.time()),0)
#
#     def award(self):
#         """ 领奖
#
#         :return:
#         """
#         if not self.rem_time():
#             return 1, {}
#
#         level_limit_gift = self.gift_center.level_limit_gift
#
#         level_gift_config = game_config.level_gift.get(level_limit_gift['level'])
#         if level_gift_config is None:
#             return 2, {}
#
#         cost = level_gift_config['coin']
#         if not self.mm.user.is_diamond_enough(cost):
#             return 'error_diamond', {}
#
#         self.mm.user.deduct_diamond(cost)
#
#         gifts = level_gift_config['reward']
#         reward = add_mult_gift(self.mm, gifts)
#
#         self.gift_center.init_level_limit_gift()
#
#         self.gift_center.save()
#         self.mm.user.save()
#
#         result = {
#             'reward': reward,
#         }
#         result.update(self.index())
#
#         return 0, result
