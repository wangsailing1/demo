#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import datetime

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils.active_inreview_tools import get_version_by_active_id, get_inreview_version
from lib.utils.time_tools import str2timestamp, datetime_to_timestamp
from return_msg_config import i18n_msg
from lib.utils.debug import print_log
from models.payment import CURRENCY_VIP_EXP, Payment
import math


class UserPayment(ModelBase):
    """ 用户充值信息

    :var first_charge_done: {       # 首充礼包
        config_id: 0,               # 礼包id：0：不可领取，1：可领取，2：已领取
    },
    """
    DOUBLE_PAY_REFRESH = ''  # 首充双倍刷新时间
    FIRST_CHARGE_TIME = 3600 * 72  # 首充倒计时
    ADD_RECHARGE_ID = 2007  # 活动id

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'daily': {},  # 每日充值数 {date: rmb}
            'charge_price': 0,  # 历史充值数

            # 'week': {'reward': {},      # 奖励
            #          'award_day': '',   # 最近一次领奖日期
            #          'days': 0,     # 已领奖天数
            #          'pay_dt': ''   # 充值时间
            #          },
            # 'month': {'reward': {}, 'award_day': '', 'days': 0, 'pay_dt': ''},
            'double_pay': [],  # 记录首充双倍的充值项
            'double_pay_refresh': '',  # 首充双倍刷新时间

            'active_double_pay': [],  # 记录首充双倍的充值项
            'active_double_pay_refresh': '',  # 首充双倍刷新时间

            'buy_log': {},  # 每个商品id的购买时间，用于限购次数的刷新
            'first_charge_done': {},  # 首充礼包已领取的id 1 充值未领取  2 已领取
            'first_charge_time': 0,  # 首充开始倒计时的时间
            'first_charge_show': 1,
            'last_day': '',  # 最近操作时间
            'add_recharge_done': {},  # 累充礼包 1 充值未领取  2 已领取
            'add_recharge_version': 0,  # 累充版本号
            'add_recharge_price': 0,  # 总累充
        }
        # 首充双倍活动时间段
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
        _, add_recharge_version = get_version_by_active_id(active_id=self.ADD_RECHARGE_ID)
        if add_recharge_version != self.add_recharge_version:
            config = game_config.add_recharge
            mail_save = False
            for recharge_id, status in self.add_recharge_done.iteritems():
                if status == 1:
                    gift = config[recharge_id]['reward']
                    mail_dict = self.mm.mail.generate_mail(i18n_msg.get(44, self.mm.user.language_sort),
                                                           title=i18n_msg.get('add_recharge',
                                                                              self.mm.user.language_sort), gift=gift)
                    self.mm.mail.add_mail(mail_dict)
                    mail_save = True

            self.add_recharge_version = add_recharge_version
            self.add_recharge_done = {}
            self.add_recharge_price = 0
            is_save = True
            if mail_save:
                self.mm.mail.save()

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

        if self.last_day == today and self.first_charge_show != 0:
            self.first_charge_show = 0
            is_save = True
        if self.last_day != today:
            self.last_day = today
            self.first_charge_show = 1
            is_save = True

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
        today = time.strftime('%F')  # %F 日期
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
            elif buy_times == 2:  # 每月刷新
                if dt_time.strftime('%B') != month:
                    self.buy_log.pop(product_id)
                    # if datetime.datetime.strptime(today, '%Y-%m-%d') - dt_time + 1 > 30:
                    #     self.buy_log.pop(product_id)
                    is_save = True
            elif buy_times == 4:  # 每日刷新
                if dt_time.strftime('%F') != today:
                    self.buy_log.pop(product_id)
                    # if datetime.datetime.strptime(today, '%Y-%m-%d') - dt_time + 1 > 30:
                    #     self.buy_log.pop(product_id)
                    is_save = True
            elif buy_times == 3:  # 永不刷新
                pass

        if is_save:
            self.save()

    def data_update_func_1(self):
        if self.charge_price:
            payment = Payment()
            for item in payment.find_by_uid(self.uid):
                order_date = item['order_time'][:10]
                order_rmb = float(item['order_rmb'])
                self.daily[order_date] = self.daily.get(order_date, 0) + order_rmb
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

    def add_pay(self, sort, currency, price=0, order_diamond=0, order_rmb=0, product_id=0, can_open_gift=True,
                act_id=0, act_item_id=0):
        """ 记录充值

        :param sort:
        :param price:
        :param product_id:
        :return:
        """
        if order_rmb > 0:
            today = time.strftime('%F')
            self.daily[today] = self.daily.get(today, 0) + order_rmb

        if can_open_gift:  # 实付金额大于或等于订单金额才会给gift
            now = int(time.time())
            add_diamond = int(math.ceil(order_rmb * CURRENCY_VIP_EXP.get(currency, 1)))
            if not act_id:
                if sort == 1:  # 月卡
                    if not self.mm.active_card.get_status():
                        self.mm.active_card.record()
                    else:
                        return order_diamond
                elif sort == 2:  # 至尊月卡
                    if not self.mm.big_month.get_status():
                        self.mm.big_month.record()
                    else:
                        return order_diamond
                # elif sort == 3:     # 等级限时礼包
                #     charge_config = game_config.charge.get(product_id, {})
                #     lv = charge_config.get('gift_reward_id', 0)
                #     level_gift_config = game_config.level_gift.get(lv)
                #     if level_gift_config and lv in self.mm.user.level_gift:
                #         self.mm.user.level_gift[lv]['status'] = 1
                #         # self.mm.user.level_gift.pop(lv)
                #         # message = self.mm.mail.generate_mail(
                #         #     i18n_msg.get(25, self.mm.user.language_sort),
                #         #     i18n_msg.get('level_gift', self.mm.user.language_sort),
                #         #     gift=level_gift_config['reward'])
                #         # self.mm.mail.add_mail(message)
                #         self.mm.user.save()
                #     else:
                #         return order_rmb * 10
                elif sort == 3:  # 激活终身助理
                    if not self.mm.assistant.assistant:
                        self.mm.assistant.open_assistant(sort)
                    else:
                        return order_diamond
                elif sort == 4:  # 助理特权礼包
                    if self.mm.assistant.assistant and not self.mm.assistant.assistant_gift:
                        self.mm.assistant.open_assistant(sort)
                    else:
                        return order_diamond

                elif sort == 5:  # 月卡優惠禮包
                    if self.mm.active_card.reward_info and not self.mm.active_card.gift:
                        self.mm.active_card.buy_gift()
                    else:
                        return order_diamond
                elif sort == 6:  # 至尊優惠禮包
                    if self.mm.big_month.reward_info and not self.mm.big_month.gift:
                        self.mm.big_month.buy_gift()
                else:
                    return 0


            elif act_id == 3001:  # 限时等级礼包
                if not act_item_id:
                    return add_diamond
                lv = act_item_id
                level_gift_config = game_config.level_gift.get(lv)
                if level_gift_config and lv in self.mm.user.level_gift and not self.mm.user.can_buy_level_gift(lv):
                    self.mm.user.level_gift[lv]['status'] = 1
                    return 0
                return add_diamond

            elif act_id == 2012:
                if not act_item_id:
                    return add_diamond
                _, rmbfoundation_version = self.mm.rmbfoundation.get_version()
                config = game_config.get_rmbfoundation_mapping()
                if not rmbfoundation_version or rmbfoundation_version not in config or \
                                act_item_id not in config[rmbfoundation_version]:
                    return add_diamond
                rmbfoundation_info = config[rmbfoundation_version][act_item_id]
                if rmbfoundation_info and act_item_id not in self.mm.rmbfoundation.activate_mark:
                    self.mm.rmbfoundation.activate_mark[act_item_id] = time.strftime('%F')
                    reward_dict = []
                    for key, value in rmbfoundation_info.iteritems():
                        if key.startswith('day'):
                            day = int(key.split('day')[1])
                            reward_dict.append(day)
                    self.mm.rmbfoundation.reward_dict[act_item_id] = sorted(reward_dict)
                    return 0
                return add_diamond

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
        # if config_id == 1 and status == 2:
        #     self.first_charge_time = int(time.time())

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
            if not charge_type or (charge_type == 2 and price == config_price) or \
                    (charge_type == 1 and price):
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
        # remain_time = self.get_first_charge_remain_time()
        # if remain_time == -2:
        #     return False

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
        # open_days = self.mm.user.server_opening_time_info().get('open_days')
        # if open_days is not None and open_days <= 3:
        #     data = self.first_charge_done
        #     if not sum(data.values()):
        #         return True
        #
        # return False

    def first_charge_alert(self):
        """
        首冲小红点
        :param hm:
        :return:
        """
        is_alert = False
        if not self.first_charge_show:
            return False
        for reward_id in game_config.first_recharge.keys():
            if self.mm.user_payment.get_first_charge_status(reward_id) == 2:
                continue  # 奖励已领取

            # if self.mm.user_payment.get_first_charge_status(reward_id) == 0:
            #     # if reward_id == 1:
            #     #     now = int(time.time())
            #     #     if now - self.mm.user.reg_time < first_recharge_config['time'] * 3600:
            #     #         continue  # 没有到领取时间
            #     # else:
            #     #     continue  # 未达到条件
            #     continue

            is_alert = True

        return is_alert

    # 添加累充礼包
    def add_add_recharge(self, price_dict):
        if not self.add_recharge_version:
            return
        config = game_config.get_add_recharge_mapping()[self.add_recharge_version]
        price_type = config.values()[0]['type']
        price = price_dict.get(price_type, 0)
        self.add_recharge_price += price
        for recharge_id, value in config.iteritems():
            if recharge_id in self.add_recharge_done:
                continue
            if value['number'] > self.add_recharge_price:
                continue
            self.add_add_recharge_done(recharge_id, status=1)
        self.save()

    # 添加累充礼包done
    def add_add_recharge_done(self, recharge_id, status=2):
        self.add_recharge_done[recharge_id] = status

    # 获取剩余时间
    def get_add_recharge_remain_time(self):
        a_id, add_recharge_version = get_version_by_active_id(active_id=self.ADD_RECHARGE_ID)
        if not a_id:
            return 0
        config = game_config.active[a_id]
        end_time = int(str2timestamp(config['end_time']))
        now = int(time.time())
        return end_time - now

    # 获取累充礼包状态
    def get_add_recharge_status(self, recharge_id):
        return self.add_recharge_done.get(recharge_id, 0)

    # 红点
    def get_add_recharge_red_dot(self):
        for recharge_id, status in self.add_recharge_done.iteritems():
            if status == 1:
                return True
        return False


# 新服充值活动
class ServerUserPayment(ModelBase):

    ADD_RECHARGE_ID = 2027  # 活动id

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'add_recharge_done': {},  # 累充礼包 1 充值未领取  2 已领取
            'add_recharge_version': 0,  # 累充版本号
            'add_recharge_price': 0,  # 总累充
        }
        super(ServerUserPayment, self).__init__(self.uid)

    def pre_use(self):

        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ADD_RECHARGE_ID)
        if version != self.add_recharge_version:
            config = game_config.server_add_recharge
            mail_save = False
            for recharge_id, status in self.add_recharge_done.iteritems():
                if status == 1:
                    gift = config[recharge_id]['reward']
                    mail_dict = self.mm.mail.generate_mail(i18n_msg.get(44, self.mm.user.language_sort),
                                                           title=i18n_msg.get('add_recharge',
                                                                              self.mm.user.language_sort), gift=gift)
                    self.mm.mail.add_mail(mail_dict)
                    mail_save = True

            self.add_recharge_version = version
            self.add_recharge_done = {}
            self.add_recharge_price = 0
            is_save = True
            if mail_save:
                self.mm.mail.save()


    # 添加累充礼包
    def add_add_recharge(self, price_dict):
        if not self.add_recharge_version:
            return
        config = game_config.get_server_add_recharge_mapping()[self.add_recharge_version]
        price_type = config.values()[0]['type']
        price = price_dict.get(price_type, 0)
        self.add_recharge_price += price
        for recharge_id, value in config.iteritems():
            if recharge_id in self.add_recharge_done:
                continue
            if value['number'] > self.add_recharge_price:
                continue
            self.add_add_recharge_done(recharge_id, status=1)
        self.save()

    # 添加累充礼包done
    def add_add_recharge_done(self, recharge_id, status=2):
        self.add_recharge_done[recharge_id] = status

    # 获取剩余时间
    def get_add_recharge_remain_time(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ADD_RECHARGE_ID)
        if not version:
            return 0
        end_time = int(datetime_to_timestamp(e_time))
        now = int(time.time())
        return end_time - now

    # 获取累充礼包状态
    def get_add_recharge_status(self, recharge_id):
        return self.add_recharge_done.get(recharge_id, 0)

    # 红点
    def get_add_recharge_red_dot(self):
        for recharge_id, status in self.add_recharge_done.iteritems():
            if status == 1:
                return True
        return False


ModelManager.register_model('server_user_payment', ServerUserPayment)
ModelManager.register_model('user_payment', UserPayment)
