#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import datetime
import random

from lib.db import ModelBase
from lib.core.environ import ModelManager
from tools.task_event import TaskEventBase
from gconfig import game_config
from lib.utils.timelib import datetime_to_str
from return_msg_config import i18n_msg


class GiftCenter(ModelBase):
    """ 福利中心

    :var monthly_sign: {   每月签到
        'month': 0,         # 月份
        'date': '',         # 签到日期
        'days': 0,          # 签到次数
        'usable_days':0,    # 可用次数
        'reward': [],       # 奖励和状态
    }
    :var "daily_login": {   # 每日登陆
        "version": "",      # 每期的版本号, '2017-02-22 00:00:00_2017-03-22 23:59:59'
        "login_days": 0,    # 活动期间累积登陆的天数
        "got_ids": [],      # 领取的奖励id
        "login_date": "",   # 登陆日期
    },
    :var "card_login": {        # 连续登陆(翻牌)
        "version": "",          # 每期版本号, '2017-02-22 00:00:00_2017-03-22 23:59:59'
        "login_date": "",       # 登陆日期
        "card_times": 0,        # 翻牌次数
        "login_days": 0,        # 连续登陆天数
    },
    :var "three_days_login": {       # 三顾茅庐
        "version": '',          # 每期版本号, '2017-02-22 00:00:00_2017-03-22 23:59:59'
        "login_date": '',       # 登陆日期
        "login_days": 0,        # 连续登陆天数
        "got_ids": []           # 已领取的奖励id, 1-3
        "usable_days": 0,       # 登陆未领取标记, 0: 已领取, 1: 未领取
        "reward": {1: []},      # 存储配置奖励, {第几天: 奖励}
    },
    :var "online_duration": {   # 累计在线
        "got_ids": [],          # 已领取的奖励配置id
        "online_time": 0,       # 当前奖励在线开始时间戳
    },
    :var "level_gift": {        # 等级礼包
        "god_ids": [],          # 已领取的奖励配置id
    },
    :var "energy": {            # 领取体力
        "refresh_date": '',     # 每日刷新
        "god_ids": [],          # 已领取的体力配置id
    }
    """
    LEVEL_GIFT_EXIST_TIME = 3600    # 等级礼包存在时间

    WELFARE_SIGN = 1        # 签到
    # WELFARE_LOGIN = 2       # 累计登录
    WELFARE_CARD_LOGIN = 3  # 登陆翻牌
    WELFARE_THREE_DAYS = 4  # 三顾茅庐
    WELFARE_ENERGY = 5      # 领取体力
    WELFARE_ONLINE = 6      # 累积在线
    WELFARE_LEVEL = 7       # 等级礼包

    def __init__(self, uid):
        """

        :param uid:
        :return:
        """
        self.uid = uid
        self.today = datetime.datetime.today()
        self._attrs = {
            'monthly_sign': {    # 每月签到
                'month': 0,         # 月份
                'login_date': '',   # 登录日期
                'date': '',         # 签到日期
                'days': 0,          # 签到次数
                'usable_days':0,    # 可用次数
                'reward': [],       # 奖励
            },
            # 'pay_sign': {        # 豪华签到
            #     'date': '',                 # 签到日期
            #     'days': 0,          # 签到次数
            #     'usable_days':0,    # 可用次数
            #     'version': 0,       # 版本号
            #     'pay': 0,           # 当天支付金额
            #     'reward': [],           # 签到数据
            # },
            # 'first_week_sign': {    # 首周登陆奖励
            #     'date': '',         # 领取日期, 只有点击领取才能设置
            #     'days': 0,          # 领奖次数
            #     'reward': [],       # 奖励
            # },
            # 'first_payment': {      # 首充奖励
            #     'pay': 0,           # 支付金额
            #     'status': 0,        # 状态, 0 不能领奖  1 可领奖  2 领完
            # },
            # 'level_limit_gift': {   # 等级限时礼包
            #     'expire_time': 0,       # 过期时间
            #     'level': 0,             # 激活的等级
            # },
            # 'daily_login': {        # 每日登陆
            #     'version': '',      # 每期的版本号, '2017-02-22 00:00:00_2017-03-22 23:59:59'
            #     'login_days': 0,    # 活动期间累积登陆的天数
            #     'got_ids': [],      # 领取的奖励id
            #     'login_date': '',   # 登陆日期
            # },
            'card_login': {         # 连续登陆(翻牌)
                'version': '',      # 每期版本号, '2017-02-22 00:00:00_2017-03-22 23:59:59'
                'login_date': '',   # 登陆日期
                'card_times': 0,    # 翻牌次数
                'login_days': 0,    # 连续登陆天数
            },
            'three_days_login': {   # 三顾茅庐
                'version': '',
                'login_date': '',
                'login_days': 0,
                'got_ids': [],
                'usable_days': 0,
                'reward': {},
            },
            'online_duration': {    # 累计在线
                'got_ids': [],      # 已领取的奖励配置id
                'online_time': 0,   # 当前奖励在线开始时间戳
            },
            'level_gift': {         # 等级礼包
                'got_ids': [],      # 已领取的奖励配置id
            },
            'energy': {              # 领取体力
                'refresh_date': '',  # 每日刷新
                'got_ids': [],       # 已领取的体力配置id
            }
        }
        super(GiftCenter, self).__init__(self.uid)

    @classmethod
    def get(cls, uid, server_name='', **kwargs):
        o = super(GiftCenter, cls).get(uid, server_name=server_name, **kwargs)
        o.refresh_data()
        return o

    def init_monthly_sign(self):
        """ 初始化每日签到数据

        :return:
        """
        reward = []
        for day, value in sorted(game_config.welfare_sign.iteritems(), key=lambda x: x[0]):
            reward.append(value['reward'])

        self.monthly_sign = {
            'month': self.today.month,  # 那个月
            'login_date': '',           # 登录日期
            'date': '',                 # 签到日期
            'days': 0,                  # 签到次数
            'usable_days': 0,           # 可用次数
            'reward': reward,           # 签到数据
        }

    def refresh_monthly_sign(self):
        """
        每月签到,登录但未签到的自动发邮件
        :return:
        """
        monthly_sign = self.monthly_sign
        reward = monthly_sign['reward']
        mail_save = False
        for i in xrange(monthly_sign['usable_days']):
            if monthly_sign['days'] < len(reward):
                gifts = reward[monthly_sign['days']]
                monthly_sign['days'] += 1
                mail_dict = self.mm.mail.generate_mail(i18n_msg.get(15, self.mm.user.language_sort), title=i18n_msg.get('monthly_sign', self.mm.user.language_sort), gift=gifts)
                self.mm.mail.add_mail(mail_dict)
                mail_save = True

        if mail_save:
            self.mm.mail.save()
            monthly_sign['usable_days'] = 0
            self.save()

    def refresh_three_days_login(self):
        """
        三顾茅庐, 登陆未领奖的,发邮件
        :return:
        """
        is_save = False
        got_ids = self.three_days_login['got_ids']
        login_days = self.three_days_login['login_days']
        day_reward = self.three_days_login['reward']

        if self.three_days_login['usable_days']:    # 有上次登陆未领取的奖励
            # if not got_ids:
            #     day_id = 1
            # else:
            #     day_id = max(got_ids) + 1

            gifts = day_reward.get(login_days, [])
            mail_dict = self.mm.mail.generate_mail(i18n_msg.get(16, self.mm.user.language_sort), title=i18n_msg.get('three_days_login', self.mm.user.language_sort), gift=gifts)
            self.mm.mail.add_mail(mail_dict)

            got_ids.append(login_days)
            self.three_days_login['usable_days'] = 0

            is_save = True

        # if len(got_ids) >= len(day_reward):
        #     self.init_three_days_login(self.three_days_login['version'])
        #     is_save = True

        if is_save:
            self.mm.mail.save()
            self.save()

    def init_pay_sign(self):
        """ 初始化每日豪华签到数据

        :return:
        """
        version = self.pay_sign['version']
        max_version = max(game_config.sign_daily_charge)
        if version:
            version += 1
            if version > max_version:
                version = max_version
        else:
            version = min(game_config.sign_daily_charge)
        reward = []
        for day, value in sorted(game_config.sign_daily_charge[version].iteritems(), key=lambda x: x[0]):
            reward.append(value['reward'])

        self.pay_sign = {
            'date': '',                 # 签到日期
            'days': 0,          # 签到次数
            'usable_days': 0,    # 可用次数
            'version': version,  # 版本号
            'pay': 0,           # 当天支付金额
            'reward': reward,   # 签到数据
        }

    def init_first_week_sign(self):
        """ 初始化首周签到

        :return:
        """
        reward = []
        for day, value in sorted(game_config.sign_first_week.iteritems(), key=lambda x: x[0]):
            reward.append(value['reward'])

        self.first_week_sign = {
            'date': '',         # 领取日期, 只有点击领取才能设置
            'days': 0,          # 领奖次数
            'reward': reward,       # 奖励
        }

    # def init_level_limit_gift(self):
    #     """ 初始化等级限时礼包
    #
    #     :return:
    #     """
    #     self.level_limit_gift = {
    #         'expire_time': 0,
    #         'level': 0,
    #     }

    # def init_daily_login(self, version):
    #     """
    #     初始化每日登陆
    #     :param version:
    #     :return:
    #     """
    #     self.daily_login = {
    #         'version': version,
    #         'login_date': '',
    #         'login_days': 0,
    #         'got_ids': [],
    #     }

    def init_card_login(self, version):
        """
        初始化连续登陆(翻牌)
        :param version:
        :return:
        """
        self.card_login = {
            'version': version,
            'login_date': '',
            'card_times': 0,
            'login_days': 0,
        }

    def init_three_days_login(self, version, reward):
        """
        初始化三顾茅庐
        :param version:
        :param reward: {}
        :return:
        """
        self.three_days_login = {
            'version': version,
            'login_date': '',
            'login_days': 0,
            'got_ids': [],
            'usable_days': 0,
            'reward': reward,
        }

    def init_online_duration(self):
        """
        初始化累计在线
        :return:
        """
        self.online_duration = {
            'got_ids': [],
            'online_time': int(time.time()),
        }

    def init_level_gift(self):
        """
        初始化等级礼包
        :return:
        """
        self.level_gift = {
            'got_ids': []
        }

    def init_energy(self):
        """
        初始化领取体力
        :return:
        """
        self.energy = {
            'refresh_date': self.today.strftime('%F'),
            'got_ids': [],
        }

    def refresh_data(self):
        """ 初始化数据

        :return:
        """
        is_save = False
        # 初始化每月签到
        # if (not self.monthly_sign['reward']) or self.monthly_sign['month'] != self.today.month:
        #     self.init_monthly_sign()
        #     is_save = True

        # 豪华签到
        # cur_time = datetime_to_str(self.today, datetime_format='%Y-%m-%d')
        # if (not self.pay_sign['reward']) or \
        #         (cur_time != self.pay_sign['date'] and
        #                  max(game_config.sign_daily_charge.get(self.pay_sign['version'], [0])) <=
        #                  (self.pay_sign['days'] + self.pay_sign['usable_days'])):
        #     self.init_pay_sign()
        #     is_save = True

        # 首周登陆奖励
        # if not self.first_week_sign['reward']:
        #     self.init_first_week_sign()
        #     is_save = True

        # 等级限时礼包
        # expire_time = self.level_limit_gift['expire_time']
        # if expire_time and int(time.time()) - expire_time > 0:
        #     self.init_level_limit_gift()
        #     is_save = True

        # 累计登录
        # if self.is_open(self.WELFARE_LOGIN):
        #     start_time, end_time = self.get_active_start_end_time(self.WELFARE_LOGIN)
        #     daily_login_version = '%s_%s' % (start_time, end_time)
        #     if start_time <= self.today.strftime('%F %T') <= end_time and \
        #             self.daily_login['version'] != daily_login_version:
        #         self.init_daily_login(daily_login_version)
        #         is_save = True

        # 连续登陆(翻牌)
        # if self.is_open(self.WELFARE_CARD_LOGIN):
        #     start_time, end_time = self.get_active_start_end_time(self.WELFARE_CARD_LOGIN)
        #     card_login_version = '%s_%s' % (start_time, end_time)
        #     if start_time <= self.today.strftime('%F %T') <= end_time and \
        #             self.card_login['version'] != card_login_version:
        #         self.init_card_login(card_login_version)
        #         is_save = True

        # 三顾茅庐
        # if self.is_open(self.WELFARE_THREE_DAYS):
        #     start_time, end_time = self.get_active_start_end_time(self.WELFARE_THREE_DAYS)
        #     three_days_login_version = '%s_%s' % (start_time, end_time)
        #     if start_time <= self.today.strftime('%F %T') <= end_time and \
        #             self.three_days_login['version'] != three_days_login_version:
        #         reward = game_config.welfare_3days.get(1, {}).get('day_reward', {})
        #         self.init_three_days_login(three_days_login_version, reward)
        #         is_save = True

        # 累计在线
        # if self.is_open(self.WELFARE_ONLINE):
        #     if not self.online_duration['online_time']:
        #         self.init_online_duration()
        #         is_save = True

        # 领取体力
        if self.today.strftime('%F') != self.energy['refresh_date']:
            self.init_energy()
            is_save = True

        if is_save:
            self.save()

    def enter_game(self):
        """ 进入游戏, 设置可用数据

        :return:
        """
        is_save = False
        cur_time = datetime_to_str(self.today, datetime_format='%Y-%m-%d')

        # 签到
        if self.is_open(self.WELFARE_SIGN) and cur_time != self.monthly_sign['login_date']:
            # 每月签到,登录但未签到的自动发邮件
            self.refresh_monthly_sign()
            if max(game_config.welfare_sign) > (self.monthly_sign['days'] + self.monthly_sign['usable_days']):
                self.monthly_sign['login_date'] = cur_time
                self.monthly_sign['usable_days'] += 1
                is_save = True

        # 累积登陆
        # if self.is_open(self.WELFARE_LOGIN) and \
        #         self.daily_login['version'] and \
        #         self.in_active_time(self.WELFARE_LOGIN) and \
        #         cur_time != self.daily_login['login_date']:
        #     self.daily_login['login_date'] = cur_time
        #     self.daily_login['login_days'] += 1
        #     is_save = True

        # 连续登陆翻牌
        if self.is_open(self.WELFARE_CARD_LOGIN) and \
                self.card_login['version'] and \
                self.in_active_time(self.WELFARE_CARD_LOGIN) and \
                cur_time != self.card_login['login_date']:
            login_date = self.card_login['login_date']
            if login_date:
                last_login_date = self.today.strptime(login_date, '%Y-%m-%d')
            else:
                last_login_date = self.today
            diff_days = (self.today.date() - last_login_date.date()).days
            if diff_days == 1:
                login_days = self.card_login['login_days'] + 1
                if login_days > len(game_config.welfare_card_login):
                    login_days = 1
            else:
                login_days = 1

            self.card_login['login_date'] = cur_time
            self.card_login['card_times'] += game_config.welfare_card_login.get(login_days, {}).get('card_times', 0)
            self.card_login['login_days'] = login_days
            is_save = True

        # 三顾茅庐
        if self.is_open(self.WELFARE_THREE_DAYS) and \
                self.three_days_login['version'] and \
                self.in_active_time(self.WELFARE_THREE_DAYS) and \
                cur_time != self.three_days_login['login_date']:
            self.refresh_three_days_login()
            login_date = self.three_days_login['login_date']
            if login_date:
                last_login_date = self.today.strptime(login_date, '%Y-%m-%d')
            else:
                last_login_date = self.today
            diff_days = (self.today.date() - last_login_date.date()).days
            if diff_days == 1:  # 连续登陆
                login_days = self.three_days_login['login_days'] + 1
                if login_days > 3:
                    login_days = 1
                    self.three_days_login['got_ids'] = []
            else:
                login_days = 1
                self.three_days_login['got_ids'] = []
            self.three_days_login['login_date'] = cur_time
            self.three_days_login['login_days'] = login_days
            self.three_days_login['usable_days'] = 1
            is_save = True

        if is_save:
            self.save()

    def today_can_sign(self):
        """ 今天能否签

        :return:
        """
        cur_time = datetime_to_str(self.today, datetime_format='%Y-%m-%d')

        monthly_sign = self.monthly_sign
        return 1 if cur_time != monthly_sign['date'] else 0

    def get_active_start_end_time(self, active_id):
        """
        获得活动开始,结束时间
        :param active_id:
        :return:
        """
        welfare_config = game_config.welfare.get(active_id, {})

        start_time = welfare_config.get('start_time', '')
        end_time = welfare_config.get('end_time', '')

        time_sort = welfare_config.get('time_sort', 0)
        if time_sort == 1:
            start_time, end_time = '0', '9'

        return start_time, end_time

    def in_active_time(self, active_id):
        """
        是否在活动时间内
        :param active_id:
        :return:
        """
        start_time, end_time = self.get_active_start_end_time(active_id)
        today_str = self.today.strftime('%F %T')
        if start_time <= today_str <= end_time:
            return True

        return False

    def is_open(self, active_id):
        """
        活动是否开启
        :return:
        """
        is_show = game_config.welfare.get(active_id, {}).get('is_show', 0)
        level_limit = game_config.welfare.get(active_id, {}).get('level', 0)
        if not is_show or self.mm.user.level < level_limit:
            return False

        return True

    def receive_energy(self, energy_id):
        """
        记录领取体力
        :param energy_id: 体力id
        :return:
        """
        if energy_id not in self.energy['got_ids']:
            self.energy['got_ids'].append(energy_id)
            return True
        else:
            return False

    def energy_has_received(self, energy_id):
        """
        是否领取
        :param energy_id:
        :return:
        """
        return energy_id in self.energy['got_ids']

    # def is_welfare_login_awarded(self, reward_id):
    #     """
    #     是否已领取累积登陆奖励
    #     :param reward_id:
    #     :return:
    #     """
    #     return reward_id in self.daily_login['got_ids']
    #
    # def can_welfare_login_award(self, reward_id):
    #     """
    #     是否可领取累积登陆奖励
    #     :param reward_id:
    #     :return:
    #     """
    #     welfare_login_config = game_config.welfare_login.get(reward_id, {})
    #     if not welfare_login_config:
    #         return False
    #
    #     if self.daily_login['login_days'] < welfare_login_config['login_days']:
    #         return False
    #
    #     return True
    #
    # def welfare_login_award(self, reward_id):
    #     """
    #     记录累积登陆领奖
    #     :param reward_id:
    #     :return:
    #     """
    #     if reward_id not in self.daily_login['got_ids']:
    #         self.daily_login['got_ids'].append(reward_id)

    def has_card_login_times(self):
        """
        是否有登陆翻牌次数
        :return:
        """
        return self.card_login['card_times'] > 0

    def get_card_login_days(self):
        """
        获取登陆翻牌连续登陆天数
        :return:
        """
        return self.card_login['login_days']

    def get_card_login_times(self):
        """
        获取登陆翻牌次数
        :return:
        """
        return self.card_login['card_times']

    def decr_card_login_times(self, times=1):
        """
        扣除登陆翻牌次数
        :param times:
        :return:
        """
        self.card_login['card_times'] -= times

    def three_days_award(self, day_id):
        """
        三顾茅庐领奖记录
        :return:
        """
        if day_id not in self.three_days_login['got_ids']:
            self.three_days_login['got_ids'].append(day_id)

        self.three_days_login['usable_days'] = 0

    def online_award(self, reward_id):
        """
        累计在线奖励领取记录
        :param reward_id:
        :return:
        """
        if reward_id not in self.online_duration['got_ids']:
            self.online_duration['got_ids'].append(reward_id)
            self.online_duration['online_time'] = int(time.time())

    def level_gift_award(self, reward_id):
        """
        等级礼包领取记录
        :param reward_id:
        :return:
        """
        if reward_id not in self.level_gift['got_ids']:
            self.level_gift['got_ids'].append(reward_id)

    def get_online_duration_remain_time(self, reward_id):
        """
        获取累计在线奖励累计剩余时间
        :param reward_id:
        :return:
        """
        welfare_online_config = game_config.welfare_online.get(reward_id, {})
        online_time = welfare_online_config.get('online_time', 0) * 60
        remain_time = max(0, online_time - (int(time.time()) - self.online_duration['online_time']))

        return remain_time

    def payment(self, product_id, order_money, diamond):
        """ 支付接口调用

        :param product_id:
        :param order_money:
        :param diamond:
        :return:
        """
        is_save = False

        pay_sign_status = self.callback_pay_sign(product_id, order_money, diamond)
        if pay_sign_status:
            is_save = True

        first_payment_status = self.callback_first_payment(product_id, order_money, diamond)
        if first_payment_status:
            is_save = True

        if is_save:
            self.save()

    def callback_pay_sign(self, product_id, order_money, diamond):
        """ 调用豪华签到

        :param product_id:
        :param order_money:
        :param diamond:
        :return:
        """
        cur_time = datetime_to_str(self.today, datetime_format='%Y-%m-%d')
        if cur_time != self.pay_sign['date']:
            self.pay_sign['date'] = cur_time
            self.pay_sign['pay'] = 0

        sign_config = game_config.sign_daily_charge[self.pay_sign['version']]
        config = sign_config[self.pay_sign['days'] + self.pay_sign['usable_days'] + 1]
        if self.pay_sign['pay'] >= config['pay']:
            return False
        pay_sort = config['pay_sort']
        if pay_sort == 1:  # money
            cost = order_money
        elif pay_sort == 2:  # diamond
            cost = diamond
        else:
            return False
        self.pay_sign['pay'] += cost
        if self.pay_sign['pay'] >= config['pay']:
            self.pay_sign['usable_days'] += 1

        return True

    def callback_first_payment(self, product_id, order_money, diamond):
        """ 调用首充

        :param product_id:
        :param order_money:
        :param diamond:
        :return:
        """
        if self.first_payment['status']:
            return False

        self.first_payment['pay'] += order_money

        first_charge_reward_id = max(game_config.first_charge_reward)

        if self.first_payment['pay'] > first_charge_reward_id:
            self.first_payment['status'] = 1

        return True

    def level_upgrade(self, level, *args, **kwargs):
        """
        战队升级
        :param level: 战队当前等级
        :param args:
        :param kwargs:
        :return:
        """
        # config = game_config.level_gift.get(level)
        # if not config:
        #     return
        #
        # expire_time = int(time.time()) + self.LEVEL_GIFT_EXIST_TIME
        #
        # self.level_limit_gift = {   # 等级限时礼包
        #     'expire_time': expire_time,       # 过期时间
        #     'level': level,             # 激活的等级
        # }
        # self.save()
        pass

    # def level_limit_gift_status(self):
    #     """ 等级限时礼包状态
    #
    #     :return:
    #     """
    #     # return 1 if self.level_limit_gift['level'] else 0
    #     return 0

    def get_gift_center_red_dot(self):
        """
        福利中心小红点
        :return:
        """
        welfare = set()
        for welfare_id, config in game_config.welfare.iteritems():
            # if welfare_id == 1:
            #     today_can_sign = self.today_can_sign()
            #     if today_can_sign and self.monthly_sign['usable_days']:
            #         welfare.add(welfare_id)
            # elif welfare_id == 2:
            #     login_ids = set(game_config.welfare_login) - set(self.daily_login['got_ids'])
            #     for login_id in sorted(login_ids):
            #         if self.can_welfare_login_award(login_id):
            #             welfare.add(welfare_id)
            #             break
            # elif welfare_id == 3:
            #     if self.has_card_login_times():
            #         welfare.add(welfare_id)
            # elif welfare_id == 4:
            #     if self.three_days_login['usable_days']:
            #         welfare.add(welfare_id)
            if welfare_id == 5:
                if self.get_welfare_energy_red_dot():
                    welfare.add(welfare_id)
            elif welfare_id == 6:
                online_ids = set(game_config.welfare_online) - set(self.online_duration['got_ids'])
                online_id = 0 if not online_ids else min(online_ids)
                if online_id and self.get_online_duration_remain_time(online_id) <= 0:
                    welfare.add(welfare_id)
            elif welfare_id == 7:
                for reward_id, welfare_level_config in game_config.welfare_level.iteritems():
                    if reward_id in self.level_gift['got_ids']:
                        continue
                    if self.mm.user.level >= welfare_level_config['level']:
                        welfare.add(welfare_id)
                        break
            elif welfare_id == 8:   # 公告
                pass
            elif welfare_id == 9:   # 激活码
                pass
            elif welfare_id == 10:  # 福利基金
                if any(self.mm.growth_fund.is_alert().values()):
                    welfare.add(welfare_id)
            elif welfare_id == 11:  # 月卡季卡
                if self.mm.active_card.is_alert():
                    welfare.add(welfare_id)
            elif welfare_id == 12:  # 开服狂欢
                if self.mm.rank_reward_show.alert():
                    welfare.add(welfare_id)
            elif welfare_id == 13:  # 签到
                if self.mm.free_sign.is_alert():
                    welfare.add(welfare_id)

        return list(welfare)

    def get_welfare_energy_red_dot(self):
        """
        体力领取小红点
        :return:
        """
        hour = time.strftime('%H:%M:%S')
        for energy_id, energy_config in game_config.welfare_energy.iteritems():
            start, end = energy_config['time_rage']
            if start <= hour <= end and not self.energy_has_received(energy_id):
                return True

        return False

    def get_level_gift_dot(self):
        """
        等级礼包可领取的奖励
        :return:
        """
        for i in sorted(game_config.welfare_level):
            config = game_config.welfare_level[i]
            # level = config['level']
            if i in self.level_gift['got_ids']:
                continue
            # if self.mm.user.level >= level:
            return i

        return 0


# ModelManager.register_model('gift_center', GiftCenter)
