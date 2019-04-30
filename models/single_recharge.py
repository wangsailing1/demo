# -*- coding: utf-8 –*-

import time
import datetime
from lib.db import ModelBase
from gconfig import game_config
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
        }
        self.cache = {}

        super(SingleRecharge, self).__init__(uid)

    def pre_use(self):
        active_id, version = self.get_version()
        if version and self.version != version:
            self.fresh(version)
            self.version = version
            end_time = str2timestamp(game_config.active[active_id]['end_time'])
            self.end_time = end_time

    def fresh(self, new_version):
        """ 刷新
        """
        del_ids = []
        charge_data = self.charge_data
        for k, v in charge_data.iteritems():
            if v['version'] != new_version and v['complete_times'] <= v['reward']:
                del_ids.append(k)
        for del_k in del_ids:
            charge_data.pop(del_k, None)

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
        }
        self.cache = {}

        super(ServerSingleRecharge, self).__init__(uid)

    def pre_use(self):
        version, new_server, s_time, e_time = self.get_version()
        if version and self.version != version:
            self.fresh(version)
            self.version = version
            # self.start_time = datetime_to_timestamp(s_time)
            self.end_time = datetime_to_timestamp(e_time)

    def fresh(self, new_version):
        """ 刷新
        """
        del_ids = []
        charge_data = self.charge_data
        for k, v in charge_data.iteritems():
            if v['version'] != new_version and v['complete_times'] <= v['reward']:
                del_ids.append(k)
        for del_k in del_ids:
            charge_data.pop(del_k, None)

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


