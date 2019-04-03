#! --*-- coding: utf-8 --*--


import time
from lib.db import ModelBase
from gconfig import game_config, MUITL_LAN
from lib.core.environ import ModelManager
from lib.utils.active_inreview_tools import get_version_by_active_id


# 限时签约
class LimitSign(ModelBase):
    """
    """
    ACTIVE_TYPE = 2014

    def __init__(self, uid=None):
        """
        """
        self.uid = uid
        self._attrs = {
            'version': 0,  # 版本号
            'score': 0,  # 本次活动期间充值钻石数
            'reward_dict': {},  # 统计未被领取的奖励{id:{time:'',status:0}} 0充值未领取 1 已领取
            'a_id': 0,
        }
        super(LimitSign, self).__init__(self.uid)

    def pre_use(self):
        save = False
        a_id, version = self.get_version()
        if self.version != version or self.a_id != a_id:
            self.send_mail()
            self.score = 0
            self.a_id = a_id
            self.version = version
            self.reward_dict = {}
            save = True
        if save:
            self.save()

    def get_version(self):
        a_id, version = get_version_by_active_id(active_id=self.ACTIVE_TYPE)
        return a_id, version

    def send_mail(self):
        for id, value in self.reward_dict.iteritems():
            if not value['status']:
                config = game_config.get_add_recharge_limit_mapping()[self.version][id]
                lan = getattr(self, 'lan', None) or self.mm.user.language_sort
                des = game_config.get_language_config(MUITL_LAN[lan])[config['mail_des']]
                title = game_config.get_language_config(MUITL_LAN[lan])[config['mail_name']]
                message = self.mm.mail.generate_mail(des, title, config['reward'])
                self.mm.mail.add_mail(message, save=False)
                value['status'] = 1
        self.mm.mail.save()

    def is_open(self):
        a_id, version = self.get_version()
        if version and game_config.get_config_type(self._server_name) == 2:
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
        config = game_config.get_add_recharge_limit_mapping()[self.version]
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


ModelManager.register_model('limit_sign', LimitSign)
