# -*- coding: utf-8 –*-

import time
import datetime
from lib.db import ModelBase
from gconfig import game_config
from tools.gift import calc_gift
from lib.core.environ import ModelManager
from lib.utils.time_tools import strftimestamp, datetime_to_timestamp, str2timestamp
from lib.utils.active_inreview_tools import get_version_by_active_id, get_inreview_version


class SingleRecharge(ModelBase):
    """ 单笔充值
    """

    ACTIVE_TYPE = 3102
    FORMAT = '%Y-%m-%d'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'version': '',                  # 版本号
            'charge_data': {},              # 充值数据
            'end_time': 0,                  # 活动结束时间
            'reward_mail': {},              # 发送邮件信息
        }
        self.cache = {}

        super(SingleRecharge, self).__init__(uid)

    def pre_use(self):
        now_time = int(time.time())
        if now_time >= self.end_time:
            self.send_mail()
        active_id, version = self.get_version()
        if version and self.version != version:
            self.fresh(version)
            self.version = version
            end_time = str2timestamp(game_config.active[active_id]['end_time'])
            self.end_time = end_time

    def fresh(self, new_version):
        """ 刷新
        """
        self.charge_data = {}
        self.reward_mail = {}

    def send_mail(self):
        """ 发放未领取奖励
        """
        if self.reward_mail:
            return
        version = self.version
        charge_data = self.charge_data
        left_dict = {}
        gift = []
        for k, v in charge_data.iteritems():
            left_num = max(v['complete_times']-v['reward'], 0)
            if not left_num:
                continue
            v['send_mail'] = left_num
            left_dict[k] = left_num
        if left_dict:
            config_mapping = game_config.get_single_recharge_mapping().get(version, {})
            if config_mapping:
                for id_, num in left_dict.iteritems():
                    config = config_mapping[id_]
                    gift.extend(config['reward'] * num)
        if gift:
            gift = calc_gift(gift)
            mail = config_mapping[id_]['mail']
            mail_title = config_mapping[id_]['mail_title']
            msg = self.mm.mail.generate_mail_lan(mail, title=mail_title, gift=gift)
            self.mm.mail.add_mail(msg)
        self.reward_mail = left_dict if left_dict else {'send': 1}
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

    def new_record(self, is_complete=False, version=0):
        """ 生成记录
        """
        return {
            'complete_times': 1 if is_complete else 0,
            'reward': 0,
            'version': version or self.version
        }

    def add_charge_value(self, charge_id, can_open_gift=True, is_save=False):
        """ 添加充值信息
        """
        if not self.is_open():
            return
        if not can_open_gift:
            return
        charge_data = self.charge_data
        single_recharge = game_config.get_single_recharge_mapping().get(self.version, {})
        for k, config in single_recharge.iteritems():
            if charge_id != config['charge_id']:
                continue
            v = charge_data.setdefault(k, self.new_record())
            limit_num = config['limit_num']
            if v['complete_times'] >= limit_num:
                continue
            v['complete_times'] += 1

        if is_save:
            self.save()


class ServerSingleRecharge(ModelBase):
    """ 新服单笔充值
    """

    ACTIVE_TYPE = 3002
    FORMAT = '%Y-%m-%d'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'version': '',                  # 版本号
            'charge_data': {},              # 充值数据
            'end_time': 0,                  # 活动结束时间
            'reward_mail': {},              # 发送邮件信息
        }
        self.cache = {}

        super(ServerSingleRecharge, self).__init__(uid)

    def pre_use(self):
        now_time = int(time.time())
        if now_time >= self.end_time:
            self.send_mail()
        version, new_server, s_time, e_time = self.get_version()
        if version and self.version != version:
            self.fresh(version)
            self.version = version
            # self.start_time = datetime_to_timestamp(s_time)
            self.end_time = datetime_to_timestamp(e_time)

    def fresh(self, new_version):
        """ 刷新
        """
        self.charge_data = {}
        self.reward_mail = {}

    def send_mail(self):
        """ 发放未领取奖励
        """
        if self.reward_mail:
            return
        version = self.version
        charge_data = self.charge_data
        left_dict = {}
        gift = []
        for k, v in charge_data.iteritems():
            left_num = max(v['complete_times']-v['reward'], 0)
            if not left_num:
                continue
            v['send_mail'] = left_num
            left_dict[k] = left_num
        if left_dict:
            config_mapping = game_config.get_server_single_recharge_mapping().get(version, {})
            if config_mapping:
                for id_, num in left_dict.iteritems():
                    config = config_mapping[id_]
                    gift.extend(config['reward'] * num)
        if gift:
            gift = calc_gift(gift)
            mail = config_mapping[id_]['mail']
            mail_title = config_mapping[id_]['mail_title']
            msg = self.mm.mail.generate_mail_lan(mail, title=mail_title, gift=gift)
            self.mm.mail.add_mail(msg)
        self.reward_mail = left_dict if left_dict else {'send': 1}
        self.save()

    def is_open(self):
        """ 是否开启
        """
        version, new_server, s_time, e_time = self.get_version()
        if version:
            return True
        return False

    def get_version(self):
        """ 获取活动版本号
        """
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_TYPE)
        return version, new_server, s_time, e_time

    def new_record(self, is_complete=False, version=0):
        """ 生成记录
        """
        return {
            'complete_times': 1 if is_complete else 0,
            'reward': 0,
            'version': version or self.version
        }

    def add_charge_value(self, charge_id, can_open_gift=True, is_save=False):
        """ 添加充值信息
        """
        if not self.is_open():
            return
        if not can_open_gift:
            return
        charge_data = self.charge_data
        single_recharge = game_config.get_server_single_recharge_mapping().get(self.version, {})
        for k, config in single_recharge.iteritems():
            if charge_id != config['charge_id']:
                continue
            v = charge_data.setdefault(k, self.new_record())
            limit_num = config['limit_num']
            if v['complete_times'] >= limit_num:
                continue
            v['complete_times'] += 1

        if is_save:
            self.save()

ModelManager.register_model('single_recharge', SingleRecharge)
ModelManager.register_model('server_single_recharge', ServerSingleRecharge)


