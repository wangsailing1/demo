#! --*-- coding: utf-8 --*--

import time
import datetime
import copy

from lib.core.environ import ModelManager
from gconfig import game_config
from lib.db import ModelBase
from lib.utils.timelib import datetime_to_str
from lib.utils.active_inreview_tools import active_inreview_version


class ActiveCard(ModelBase):
    """
    月卡至尊卡卡活动
    """


    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'reward_info': {},  # 月卡信息
            'buy_times': {},  # 购买次数
            'version': 0,  # 版本号
            'get_reward_times': 0, # 领取奖励次数
            'gift': 0,
            'last_data': '',
        }
        self.config = game_config.month_privilege
        super(ActiveCard, self).__init__(self.uid)


    def pre_use(self):
        user_card = self.reward_info
        version = self.get_version()
        if not user_card:
            if version > self.version:
                self.version = version
                self.save()
            return 0
        _format = "%Y-%m-%d"
        today_time = time.strftime(_format)
        one_day = 3600 * 24
        if not self.version:
            return
        if self.config:
            now = int(time.time())
            effective_days = self.config[self.version]['effective_days']
            remain_time = effective_days * 3600 * 24 + self.reward_info['buy_time'] - now
            remain_day = (one_day + remain_time - 1) // one_day
            self.reward_info['remain_time'] = remain_day
            if self.last_data != today_time:
                self.last_data = today_time
                self.gift = 0
            if self.reward_info['last_receive'] != today_time:
                self.reward_info['status'] = 1
            if remain_time <= 0:  # 结束删除数据
                self.reward_info = {}
                self.get_reward_times = 0
                if version > self.version:
                    self.version = version
            self.save()

    def get_version(self):
        return active_inreview_version(self.config)

    def record(self):
        today = datetime.date.today()
        time_0 = time.mktime(today.timetuple())
        self.buy_times[self.version] = self.buy_times.get(self.version, 0) + 1
        self.reward_info = {
            'status': 1,
            'remain_time': self.config[self.version]['effective_days'],
            'last_receive': '',
            'had_receive': 0,
            'buy_time': time_0,
        }

        self.save()

    def get_status(self):
        """
        获取月卡状态
        status:0未激活1能领奖2已领奖
        :return:
        """
        return self.reward_info.get('status', 0)

    def is_alert(self):
        not_alert = False
        reward_info = self.reward_info
        if not reward_info or not self.config:
            return not_alert
        if reward_info['status'] == 1:
            return True
        return not_alert

    def month_remain_times(self):
        """月卡剩余次数"""
        if self.get_status():
            return int(self.reward_info['remain_time'])
        else:
            return 0

    def buy_gift(self):
        self.gift = 1
        self.save()

class BigMonth(ActiveCard):
    """
    至尊月卡
    """
    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'reward_info': {},
            'buy_times': {},  #
            'version': 0,
            'get_reward_times': 0,
            'gift': 0,
        }
        self.config = game_config.month_privilege
        super(BigMonth, self).__init__(self.uid)



class SevenLogin(ModelBase):
    """
    七日登录
    """
    FORMAT = '%F'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'days': 1,  # 登录天数
            'got': [],  # 已领取id
            'refresh': '',  # 领取日期
        }
        super(SevenLogin, self).__init__(self.uid)

    # def pre_use(self):
    #     # days = self.mm.user.regist_days()
    #     # if days <= 0:
    #     #     days = 1
    #     # self.days = days
    #
    #     if not self.is_open():
    #         return
    #
    #     # today = time.strftime('%F')
    #     # if not self.refresh or self.refresh != today:
    #     #     # self.send_mail()
    #     #     self.refresh = today
    #     #     # self.days += 1
    #     #     self.save()

    def get_next_reward_day(self):
        """获取下次可以领取的天数"""
        day = 0
        if self.is_open():
            config = game_config.sign_first_week
            if not self.got:
                day = min(config.keys())
            else:
                days = set(config.keys()) - set(self.got)
                if days:
                    day = min(days)

        return day

    # def send_mail(self):
    #     mail_save = False
    #     is_save = False
    #     for i, j in game_config.sign_first_week.iteritems():
    #         if i in self.got or i >= self.days:
    #             continue
    #         title = get_str_words(self.mm.user.language_sort, j['mail'])
    #         des = get_str_words(self.mm.user.language_sort, j['mail_des'])  # 活动内容
    #         if des:
    #             des = des % i
    #         mail_dict = self.mm.mail.generate_mail(
    #             des,
    #             title=title,
    #             gift=j['reward'],
    #         )
    #         self.mm.mail.add_mail(mail_dict, save=False)
    #         self.add_got(i)
    #         mail_save = True
    #         is_save = True
    #
    #     if mail_save:
    #         self.mm.mail.save()
    #     if is_save:
    #         self.save()

    def is_open(self):
        return not set(self.got) == set(game_config.sign_first_week)
        # max_login_day = max(game_config.sign_first_week) if game_config.sign_first_week else 0
        # if self.mm.user.regist_days() > max_login_day or set(self.got) == set(game_config.sign_first_week):
        #     return False
        #
        # return True

    def can_receive(self, day_id):
        if not self.is_open() or day_id > self.days:
            return False

        return True

    def can_get_reward(self):
        return self.refresh != time.strftime(self.FORMAT)

    def add_got(self, day_id):
        if day_id not in self.got:
            self.got.append(day_id)

    def get_red_dot(self):
        if not self.is_open():
            return False

        return self.can_get_reward()


class MonthlySign(ModelBase):
    '''每日登陆'''

    def __init__(self, uid):
        """

        :param uid:
        :return:
        """
        self.uid = uid
        self.today = datetime.datetime.today()
        self._attrs = {
            'monthly_sign': {  # 每月签到
                'month': 0,  # 月份
                'login_date': '',  # 登录日期
                'date': '',  # 签到日期
                'days': 0,  # 签到次数
                'usable_days': 0,  # 可用次数
                'reward': [],  # 奖励
                'box_got': {},  # 宝箱领取
            },
        }
        super(MonthlySign, self).__init__(self.uid)

    def pre_use(self):
        is_save = False
        cur_time = datetime_to_str(self.today, datetime_format='%Y-%m-%d')
        if (not self.monthly_sign['reward']) or self.monthly_sign['month'] != self.today.month:
            reward = []
            for day, value in sorted(game_config.sign_daily_normal.iteritems(), key=lambda x: x[0]):
                reward.append(value['reward'])

            self.monthly_sign = {
                'month': self.today.month,  # 那个月
                'login_date': '',  # 登录日期
                'date': '',  # 签到日期
                'days': 0,  # 签到次数
                'usable_days': 0,  # 可用次数
                'reward': reward,  # 签到数据
                'box_got': {},  # 宝箱领取
            }
            is_save = True
        if cur_time != self.monthly_sign['login_date'] and max(game_config.sign_daily_normal) > (
                    self.monthly_sign['days'] + self.monthly_sign['usable_days']):
            self.monthly_sign['login_date'] = cur_time
            self.monthly_sign['usable_days'] += 1
            is_save = True
        if is_save:
            self.save()

    def today_can_sign(self,red_dot=True):
        """ 今天能否签

        :return:
        """
        cur_time = datetime_to_str(self.today, datetime_format='%Y-%m-%d')

        monthly_sign = self.monthly_sign
        if red_dot:
            for k, v in monthly_sign['box_got'].iteritems():
                if v == 1:
                    return 1
        return 1 if cur_time != monthly_sign['date'] else 0


ModelManager.register_model('active_card', ActiveCard)
ModelManager.register_model('seven_login', SevenLogin)
ModelManager.register_model('monthly_sign', MonthlySign)
ModelManager.register_model('big_month', BigMonth)
