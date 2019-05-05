# -*- coding: utf-8 –*-

import time
import datetime
from lib.db import ModelBase
from gconfig import game_config
from tools.gift import calc_gift
from lib.core.environ import ModelManager
from lib.utils.time_tools import strftimestamp, datetime_to_timestamp, str2timestamp
from lib.utils.active_inreview_tools import get_version_by_active_id, get_inreview_version


class DailyRecharge(ModelBase):

    ACTIVE_TYPE = 3101
    FORMAT = '%Y-%m-%d'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'version': '',                  # 版本号
            'day': 1,                       # 第几天
            'day_str': '',                  # 当前日期
            'charge_data': {},              # 充值数据
            'done': [],                     # 完成的日期
            'done_data': {},                # 数据
            'reward_mail': [],              # 发送邮件id
            'end_time': 0,                  # 结束时间
        }
        self.cache = {}

        super(DailyRecharge, self).__init__(uid)

    def pre_use(self):

        now_time = int(time.time())
        if now_time >= self.end_time:
            self.send_mail()
        active_id, version = self.get_version()
        if version and self.version != version:
            end_time = str2timestamp(game_config.active[active_id]['end_time'])
            self.end_time = end_time
            self.fresh()
            self.version = version
        day_str = self.get_day_str()
        if version and self.day_str < day_str:
            self.daily_fresh()
            self.day_str = day_str

    def daily_fresh(self):
        """ 每日刷新
        """
        day_str = self.day_str

        if day_str in self.done:
            self.day += 1
        elif self.done_data.get(self.day, {}).get('is_complete', 0):
            self.done.append(day_str)
            self.day += 1
        self.done_data[self.day] = self.new_record()

    def get_day_str(self):
        """ 获取当天时间
        """
        if 'day_str' not in self.cache:
            self.cache['day_str'] = time.strftime(self.FORMAT)
        return self.cache['day_str']

    def get_daily_value(self):
        """ 获取当日充值数
        """
        day_str = self.get_day_str()
        value = self.charge_data.get(day_str, 0)
        return value

    def new_record(self, num=0, is_complete=False):
        """ 生成记录
        """
        return {
            'value': num,
            'is_complete': 1 if is_complete else 0,
            'reward': 0,
        }

    def add_charge_value(self, coin_num, order_money, is_save=False):
        """ 添加充值信息
        """
        if not self.is_open():
            return
        day = self.day
        day_str = self.get_day_str()
        if day_str in self.done:
            return
        data = self.done_data.get(day, {})
        if data and data['is_complete']:
           return

        config_mapping = game_config.get_daily_recharge_mapping()
        config = config_mapping[self.version][day]
        add_type = config['type']
        num = coin_num if add_type == 1 else order_money
        day_num = self.charge_data.get(day_str, 0) + num
        self.charge_data[day_str] = day_num

        if day_num >= config['number']:
            self.done_data[day] = self.new_record(day_num, is_complete=True)

        if is_save:
            self.save()

    def fresh(self):
        """ 刷新
        """
        day_str = self.get_day_str()
        self.day_str = day_str
        self.day = 1
        self.done = []
        self.done_data = {}
        self.reward_mail = []

    def send_mail(self):
        """发未领取奖励
        """
        if self.reward_mail:
            return
        version = self.version
        done_data = self.done_data
        day_ids = []
        gift = []
        for k, v in done_data.iteritems():
            if v['reward'] >= v['is_complete']:
                continue
            day_ids.append(k)
        if day_ids:
            config_mapping = game_config.get_daily_recharge_mapping().get(version, {})
            if config_mapping:
                for d in day_ids:
                    config = config_mapping[d]
                    gift.extend(config['reward'])
        if gift:
            gift = calc_gift(gift)
            mail = config_mapping[d]['mail']
            mail_title = config_mapping[d]['mail_title']
            msg = self.mm.mail.generate_mail_lan(mail, title=mail_title, gift=gift)
            self.mm.mail.add_mail(msg)
        self.reward_mail = day_ids if day_ids else ['No mail']
        self.save()

    def is_open(self):
        """ 是否开启
        """
        a_id, version = self.get_version()
        if version:
            return True
        return False

    def get_version(self):
        """ 获取活动版本号
        """
        a_id, version = get_version_by_active_id(active_id=self.ACTIVE_TYPE)
        return a_id, version

    def get_red_dot(self):
        """ 小红点
        """
        if not self.is_open():
            return 0
        done_data = self.done_data
        for k, v in done_data.iteritems():
            if v['reward'] >= v['is_complete']:
                continue
            return 1
        return 0


class ServerDailyRecharge(ModelBase):
    """ 新服天天充值
    """

    ACTIVE_TYPE = 3001
    FORMAT = '%Y-%m-%d'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'version': '',                  # 版本号
            'day': 1,                       # 第几天
            'day_str': '',                  # 当前日期
            'charge_data': {},              # 充值数据
            'done': [],                     # 完成的日期
            'done_data': {},                # 数据
            'reward_mail': [],              # 发送邮件id
            'end_time': 0,                  # 结束时间
        }
        self.cache = {}

        super(ServerDailyRecharge, self).__init__(uid)

    def pre_use(self):
        now_time = int(time.time())
        if now_time >= self.end_time:
            self.send_mail()
        version, new_server, s_time, e_time = self.get_version()
        if version and self.version != version:
            self.fresh()
            self.start_time = datetime_to_timestamp(s_time)
            self.end_time = datetime_to_timestamp(e_time)
            self.version = version
        day_str = self.get_day_str()
        if version and self.day_str < day_str:
            self.daily_fresh()
            self.day_str = day_str

    def daily_fresh(self):
        """ 每日刷新
        """
        day_str = self.day_str

        if day_str in self.done:
            self.day += 1
        elif self.done_data.get(self.day, {}).get('is_complete', 0):
            self.done.append(day_str)
            self.day += 1
        self.done_data[self.day] = self.new_record()

    def get_day_str(self):
        """ 获取当天时间
        """
        if 'day_str' not in self.cache:
            self.cache['day_str'] = time.strftime(self.FORMAT)
        return self.cache['day_str']

    def get_daily_value(self):
        """ 获取当日充值数
        """
        day_str = self.get_day_str()
        value = self.charge_data.get(day_str, 0)
        return value

    def new_record(self, num=0, is_complete=False):
        """ 生成记录
        """
        return {
            'value': num,
            'is_complete': 1 if is_complete else 0,
            'reward': 0,
        }

    def add_charge_value(self, coin_num, order_money, is_save=False):
        """ 添加充值信息
        """
        if not self.is_open():
            return
        day = self.day
        day_str = self.get_day_str()
        if day_str in self.done:
            return
        data = self.done_data.get(day, {})
        if data and data['is_complete']:
           return

        config_mapping = game_config.get_server_daily_recharge_mapping()
        config = config_mapping[self.version][day]
        add_type = config['type']
        num = coin_num if add_type == 1 else order_money
        day_num = self.charge_data.get(day_str, 0) + num
        self.charge_data[day_str] = day_num

        if day_num >= config['number']:
            self.done_data[day] = self.new_record(day_num, is_complete=True)

        if is_save:
            self.save()

    def fresh(self):
        """ 刷新
        """
        day_str = self.get_day_str()
        self.day_str = day_str
        self.day = 1
        self.done = []
        self.done_data = {}
        self.reward_mail = []

    def send_mail(self):
        """发未领取奖励
        """
        if self.reward_mail:
            return
        version = self.version
        done_data = self.done_data
        day_ids = []
        gift = []
        for k, v in done_data.iteritems():
            if v['reward'] >= v['is_complete']:
                continue
            day_ids.append(k)
        if day_ids:
            config_mapping = game_config.get_server_daily_recharge_mapping().get(version, {})
            if config_mapping:
                for d in day_ids:
                    config = config_mapping[d]
                    gift.extend(config['reward'])
        if gift:
            gift = calc_gift(gift)
            mail = config_mapping[d]['mail']
            mail_title = config_mapping[d]['mail_title']
            msg = self.mm.mail.generate_mail_lan(mail, title=mail_title, gift=gift)
            self.mm.mail.add_mail(msg)
        self.reward_mail = day_ids if day_ids else ['No mail']
        self.save()

    def is_open(self):
        """ 是否开启
        """
        version, new_server, s_time, e_time = self.get_version()
        if version:
            return True
        return False

    def get_version(self):
        """ 获取版本号
        """
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_TYPE)
        return version, new_server, s_time, e_time

    def get_red_dot(self):
        """ 小红点
        """
        if not self.is_open():
            return 0
        done_data = self.done_data
        for k, v in done_data.iteritems():
            if v['reward'] >= v['is_complete']:
                continue
            return 1
        return 0


ModelManager.register_model('daily_recharge', DailyRecharge)
ModelManager.register_model('server_daily_recharge', ServerDailyRecharge)