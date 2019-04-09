#! --*-- coding: utf-8 --*--


import time
from lib.db import ModelBase
from gconfig import game_config, MUITL_LAN
from lib.core.environ import ModelManager
from lib.utils.active_inreview_tools import get_inreview_version
from lib.utils.time_tools import datetime_to_timestamp

# 限时签约
class ServerLimitSign(ModelBase):
    """
    """
    ACTIVE_TYPE = 2015

    def __init__(self, uid=None):
        """
        """
        self.uid = uid
        self._attrs = {
            'version': 0,  # 版本号
            'score': 0,  # 本次活动期间充值钻石数
            'reward_dict': {},  # 统计未被领取的奖励{id:{time:'',status:0}} 0充值未领取 1 已领取
        }
        super(ServerLimitSign, self).__init__(self.uid)

    def pre_use(self):
        save = False
        version = self.get_version()
        if self.version != version:
            self.send_mail()
            self.score = 0
            self.version = version
            self.reward_dict = {}
            save = True
        if save:
            self.save()

    def get_version(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_TYPE)
        return version

    def send_mail(self):
        for id, value in self.reward_dict.iteritems():
            if not value['status']:
                config = game_config.get_server_add_recharge_limit_mapping()[self.version][id]
                lan = getattr(self, 'lan', None) or self.mm.user.language_sort
                des = game_config.get_language_config(MUITL_LAN[lan])[config['mail_des']]
                title = game_config.get_language_config(MUITL_LAN[lan])[config['mail_name']]
                message = self.mm.mail.generate_mail(des, title, config['reward'])
                self.mm.mail.add_mail(message, save=False)
                value['status'] = 1
        self.mm.mail.save()

    def get_remain_time(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_TYPE)
        end_time = datetime_to_timestamp(e_time)
        now = int(time.time())
        if not version:
            return -1
        remain_time = end_time - now
        return remain_time if remain_time > 0 else 0

    def is_open(self):
        version = self.get_version()
        if version and game_config.get_config_type(self._server_name) == 1:
            return True
        return False

    def has_reward(self):
        reward_id = []
        for r_id, value in self.reward_dict.iteritems():
            if not value['status']:
                reward_id.append(r_id)
        return reward_id

    def add_score(self, order_diamond, order_money):
        if not self.is_open():
            return
        config = game_config.get_server_add_recharge_limit_mapping()[self.version]
        tp = config[min(config.keys())]['type']
        if tp == 1:
            add_score = order_diamond
        else :
            add_score = order_money
        self.score += add_score
        for id, value in config.iteritems():
            if id in self.reward_dict:
                continue
            if self.score >= value['number']:
                self.reward_dict[id] = {'time': int(time.time()), 'status': 0}
        self.save()


ModelManager.register_model('server_limit_sign', ServerLimitSign)
