#! --*-- coding: utf-8 --*--


from lib.db import ModelBase
from lib.core.environ import ModelManager
from lib.utils.active_inreview_tools import get_inreview_version
from lib.utils.time_tools import strftimestamp, datetime_to_timestamp
import datetime
from gconfig import game_config
import time


# 新服人民币基金
class ServerRmbFoundation(ModelBase):

    ACTIVE_TYPE = 2017

    def __init__(self, uid=None):
        """
        version: 1
        activate_mark: {
            1: "2019-03-01",
        }
        reward_dict: {
            1: [3, 4, 5, 6, 7]  # 记录第几天的奖励未被领取
        }
        """
        self.uid = uid

        self._attrs = {
            'version': 0,  # 版本号
            'activate_mark': {},  # 各类基金激活的日期
            'reward_dict': {},  # 统计未被领取的奖励
            'start_time': '',  # 开启时间
            'end_time': '',  # 结束时间
        }

        super(ServerRmbFoundation, self).__init__(self.uid)

    def pre_use(self):
        save = self.check_reward()
        if self.has_reward():
            if save:
                self.save()
            return
        version, new_server, s_time, e_time = self.get_version()
        if self.version != version:
            self.version = version
            self.start_time = strftimestamp(datetime_to_timestamp(s_time))
            self.end_time = strftimestamp(datetime_to_timestamp(e_time))
        if save:
            self.save()

    def get_version(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_TYPE)
        return version, new_server, s_time, e_time


    def is_open(self):
        version, new_server, s_time, e_time = self.get_version()
        if version:
            return True
        return False

    def has_reward(self):
        return self.reward_dict


    def check_reward(self):
        del_list = []
        save = False
        for id, reward_list in self.reward_dict.iteritems():
            f_active_date = self.activate_mark[id]
            f_active_date = datetime.datetime.strptime(f_active_date, '%Y-%m-%d').date()
            days = (datetime.date.today() - f_active_date).days + 1
            for day in range(days):
                if day in reward_list:
                    reward_list.remove(day)
                    save = True
            if not reward_list:
                del_list.append(id)
                save = True
        for id in del_list:
            if id in self.reward_dict:
                self.reward_dict.pop(id)
                save = True
        if not self.reward_dict:
            self.activate_mark = {}
            save = True

        return save

    def open_foundation(self, act_item_id,save=False):
        version, new_server, s_time, e_time = self.get_version()
        print 11111111111
        config = game_config.get_server_rmbfoundation_mapping()
        if not version or version not in config or \
                        act_item_id not in config[version]:
            return False
        rmbfoundation_info = config[version][act_item_id]
        if rmbfoundation_info and act_item_id not in self.activate_mark:
            self.activate_mark[act_item_id] = time.strftime('%F')
            reward_dict = []
            for key, value in rmbfoundation_info.iteritems():
                if key.startswith('day'):
                    day = int(key.split('day')[1])
                    reward_dict.append(day)
            self.reward_dict[act_item_id] = sorted(reward_dict)
            if save:
                self.save()
            return True
        return False



ModelManager.register_model('serverrmbfoundation', ServerRmbFoundation)