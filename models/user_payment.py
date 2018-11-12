#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import datetime

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class UserPayment(ModelBase):
    """ 用户充值信息

    :var first_charge_done: {       # 首充礼包
        config_id: 0,               # 礼包id：0：不可领取，1：可领取，2：已领取
    },
    """
    DOUBLE_PAY_REFRESH = ''           # 首充双倍刷新时间
    FIRST_CHARGE_TIME = 3600 * 72       # 首充倒计时

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'daily': {},                # 每日充值数 {date: rmb}
            'charge_price': 0,            # 历史充值数

            # 'week': {'reward': {},      # 奖励
            #          'award_day': '',   # 最近一次领奖日期
            #          'days': 0,     # 已领奖天数
            #          'pay_dt': ''   # 充值时间
            #          },
            # 'month': {'reward': {}, 'award_day': '', 'days': 0, 'pay_dt': ''},
            'double_pay': [],               # 记录首充双倍的充值项
            'double_pay_refresh': '',       # 首充双倍刷新时间

            'active_double_pay': [],               # 记录首充双倍的充值项
            'active_double_pay_refresh': '',       # 首充双倍刷新时间

            'buy_log': {},      # 每个商品id的购买时间，用于限购次数的刷新
            'first_charge_done': {},    # 首充礼包已领取的id
            'first_charge_time': 0,     # 首充开始倒计时的时间
        }
        #首充双倍活动时间段
        time_config = {}
        time_config_name = time_config.get('name', '')
        if time_config_name:
            self.double_start_time, self.double_end_time = time_config_name.split(',')
        else:
            self.double_start_time, self.double_end_time = '', ''
        super(UserPayment, self).__init__(self.uid)

    def pre_use(self):
        now = datetime.datetime.now()
        is_save = False

        # if self.week['pay_dt']:
        #     pay_dt = datetime.datetime.strptime(self.week['pay_dt'], '%Y-%m-%d %H:%M:%S')
        #     if self.week['days'] >= len(self.week['reward']) and \
        #                     pay_dt.isocalendar()[:2] != now.isocalendar()[:2]:
        #         self.week = {'reward': {}, 'award_day': '', 'days': 0, 'pay_dt': ''}
        #         is_save = True
        #
        # if self.month['pay_dt']:
        #     pay_dt = datetime.datetime.strptime(self.month['pay_dt'], '%Y-%m-%d %H:%M:%S')
        #     if self.month['days'] >= len(self.month['reward']) and (pay_dt.year, pay_dt.month) != (now.year, now.month):
        #         self.month = {'reward': {}, 'award_day': '', 'days': 0, 'pay_dt': ''}
        #         is_save = True

        today = time.strftime('%F')
        if self.double_start_time <= today <= self.double_end_time and \
                not (self.double_start_time <= self.active_double_pay_refresh <= self.double_end_time):
            self.active_double_pay_refresh = today
            self.active_double_pay = []
            is_save = True

        # 清空首充双倍记录
        if self.DOUBLE_PAY_REFRESH and self.double_pay_refresh < self.DOUBLE_PAY_REFRESH <= today:
            self.double_pay_refresh = self.DOUBLE_PAY_REFRESH
            self.double_pay = []
            is_save = True

        # 限购次数的刷新
        week = time.strftime('%W')  # 一年中第几周
        month = time.strftime('%B')  # %B 英文的月份   %m 01 - 12
        for product_id, dt in self.buy_log.items():
            charge_config = game_config.charge.get(product_id)
            if not charge_config:
                continue

            buy_times = charge_config['buy_times']
            dt_time = datetime.datetime.strptime(dt, '%Y-%m-%d')
            if buy_times == 1:  # 每周刷新
                if dt_time.strftime('%W') != week:
                    self.buy_log.pop(product_id)
                # if datetime.datetime.strptime(today, '%Y-%m-%d') - dt_time + 1 > 7:
                #     self.buy_log.pop(product_id)
                    is_save = True
            elif buy_times == 2:    # 每月刷新
                if dt_time.strftime('%B') != month:
                    self.buy_log.pop(product_id)
                # if datetime.datetime.strptime(today, '%Y-%m-%d') - dt_time + 1 > 30:
                #     self.buy_log.pop(product_id)
                    is_save = True
            elif buy_times == 3:    # 永不刷新
                pass

        if is_save:
            self.save()

    def get_double_pay(self):
        """ 获取首冲双倍数据

        :return:
        """

        today = time.strftime('%F')
        if self.double_start_time <= today <= self.double_end_time:
            pay_list = self.active_double_pay
        else:
            pay_list = self.double_pay

        return pay_list

    # def get_status(self, tp='week'):
    #     """ 获取周卡或者月卡状态
    #
    #     :param tp:
    #     :return: 0: 可领奖 1: 今日已经领过 2: 需要充值
    #     """
    #     today = time.strftime('%Y-%m-%d')
    #     model = self.week if tp == 'week' else self.month
    #     if model['pay_dt']:
    #         if model['award_day'] != today:
    #             if model['days'] == len(model['reward']):
    #                 return 1
    #             else:
    #                 return 0    # 可领奖
    #         else:
    #             return 1    # 今日已领取奖励
    #     else:
    #         return 2        # 可充值

    def is_double_pay(self, product_id, charge_config=None):
        """ 是否充值双倍

        :param product_id:
        :return:
        """
        charge_config = charge_config or game_config.charge.get(product_id)
        if not charge_config['is_double']:
            return False

        return 0 if product_id in self.get_double_pay() else 1

    def add_double_pay(self, product_id):
        """ 增加双倍

        :param product_id:
        :return:
        """
        double_data = self.get_double_pay()
        double_data.append(product_id)
        self.save()

    def add_pay(self, sort, price=0, order_diamond=0, order_rmb=0, product_id=0, can_open_gift=True):
        """ 记录充值

        :param sort:
        :param price:
        :param product_id:
        :return:
        """
        if can_open_gift:   # 实付金额大于或等于订单金额才会给gift
            now = int(time.time())
            if sort == 1:      # 月卡
                if not self.mm.active_card.get_status(sort):
                    self.mm.active_card.record(sort)
                else:
                    return order_diamond
            elif sort == 2:    # 至尊卡卡
                if not self.mm.active_card.get_status(sort):
                    self.mm.active_card.record(sort)
                else:
                    return order_diamond
            elif sort == 3:     # 等级限时礼包
                charge_config = game_config.charge.get(product_id, {})
                lv = charge_config.get('gift_reward_id', 0)
                level_gift_config = game_config.level_gift.get(lv)
                if level_gift_config and lv in self.mm.user.level_gift:
                    self.mm.user.level_gift[lv]['status'] = 1
                    # self.mm.user.level_gift.pop(lv)
                    # message = self.mm.mail.generate_mail(
                    #     i18n_msg.get(25, self.mm.user.language_sort),
                    #     i18n_msg.get('level_gift', self.mm.user.language_sort),
                    #     gift=level_gift_config['reward'])
                    # self.mm.mail.add_mail(message)
                    self.mm.user.save()
                else:
                    return order_rmb * 10
            return 0
        else:
            return 0

    def add_buy_log(self, product_id):
        """
        记录购买商品
        :param product_id:
        :return:
        """
        today = time.strftime('%F')
        self.buy_log[product_id] = today

    def add_first_charge_done(self, config_id, status=2):
        """
        记录首充礼包领取
        :param config_id:
        :return:
        """
        self.first_charge_done[config_id] = status
        if config_id == 1 and status == 2:
            self.first_charge_time = int(time.time())

    def get_first_charge_status(self, config_id):
        """
        首充礼包领取状态
        :param config_id:
        :return:
        """
        return self.first_charge_done.get(config_id, 0)

    def add_first_charge(self, price, charge_config=None):
        """
        首充礼包
        :param price:
        :return:
        """
        self.charge_price += price
        # 充值钻石任务，对应人民币*10
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('charge_price', price * 10)

        # 过滤不算首充的充值项
        if charge_config and 2 in charge_config.get('charge_condition', []):
            return

        for active_id, config in game_config.first_recharge.iteritems():
            if self.get_first_charge_status(active_id) > 0:
                continue
            config_price = config['price_CN']
            charge_type = config['type']
            if not charge_type or (charge_type == 2 and price >= config_price) or \
                    (charge_type == 1 and self.charge_price >= config_price):
                self.add_first_charge_done(active_id, status=1)

            # mail_dict = self.mm.mail.generate_mail(
            #     i18n_msg[29],
            #     title=i18n_msg['first_recharge'],
            #     gift=config['gift'],
            # )
            # self.mm.mail.add_mail(mail_dict)
            # self.add_first_charge_done(active_id, status=1)

        self.save()

    def get_first_charge_remain_time(self):
        """
        获取首充剩余时间
        :return:
        """
        if not self.first_charge_time:
            return -1

        now = int(time.time())
        remain_time = self.FIRST_CHARGE_TIME - (now - self.first_charge_time)
        if remain_time < 0:
            remain_time = -2

        return remain_time

    def get_first_charge(self):
        """
        首充活动标志
        :return:
        """
        remain_time = self.get_first_charge_remain_time()
        if remain_time == -2:
            return False

        received_id = []
        charge_done = self.first_charge_done
        for k, v in charge_done.iteritems():
            if v == 2:
                received_id.append(k)
        charge_done_config = game_config.first_recharge.keys()
        if received_id == charge_done_config:
            return False

        return True

    def get_first_charge_pop(self):
        """
        首充弹板
        :return:
        """
        open_days = self.mm.user.server_opening_time_info().get('open_days')
        if open_days is not None and open_days <= 3:
            data = self.first_charge_done
            if not sum(data.values()):
                return True

        return False

    def first_charge_alert(self):
        """
        首冲小红点
        :param hm:
        :return:
        """
        is_alert = False
        for reward_id in game_config.first_recharge.keys():
            first_recharge_config = game_config.first_recharge.get(reward_id)
            if self.mm.user_payment.get_first_charge_status(reward_id) == 2:
                continue  # 奖励已领取

            if self.mm.user_payment.get_first_charge_status(reward_id) == 0:
                # if reward_id == 1:
                #     now = int(time.time())
                #     if now - self.mm.user.reg_time < first_recharge_config['time'] * 3600:
                #         continue  # 没有到领取时间
                # else:
                #     continue  # 未达到条件
                continue

            is_alert = True

        return is_alert


ModelManager.register_model('user_payment', UserPayment)
