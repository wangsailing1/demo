# -*- coding: utf-8 –*-

import time
import random
import datetime
from lib.db import ModelBase
from lib.core.environ import ModelManager
from lib.utils.zip_date import encrypt_data, dencrypt_data
from gconfig import game_config
from strategy_mission import Mission


class Strategy(ModelBase):

    APPLY_KEY = 'apply_key'
    INVITE_KEY = 'invite_key'
    REFUSE_KEY = 'refuse_key'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'strategy_id': '',          # 战略合作id
            'strategy_uid': '',         # 战略合作uid
            'strategy_server': '',      # 战略合作区服信息
            'yesterday_str': '',        # 昨天日期
            'y_income': 0,              # 昨天最高票房
            'quit_msg': {},             # 解除合作提示消息
        }
        super(Strategy, self).__init__(self.uid)

    def pre_use(self):
        y_str = self.get_yesterday().strftime('%F')
        if self.yesterday_str != y_str:
            self.yesterday_str = y_str
            self.daily_fresh(y_str)

    @staticmethod
    def get_yesterday():
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        return yesterday

    def daily_fresh(self, y_str=None):
        self.y_income = self.get_yesterday_income(y_str)

    def get_yesterday_income(self, y_str=None):
        mm = self.mm
        y_str = y_str or self.get_yesterday().strftime('%F')
        top_script = mm.block.top_script.get(y_str, {})
        y_income = 0 if not top_script else sum([v['finished_summary']['income'] for v in top_script.itervalues()])

        return y_income

    def get_apply_key(self, sort='apply'):
        """ 获取申请信息的key
        """
        key_prefix = ''
        if sort=='apply':
            key_prefix = self.APPLY_KEY
        elif sort=='invite':
            key_prefix = self.INVITE_KEY
        elif sort=='refuse':
            key_prefix = self.REFUSE_KEY

        key = '%s_%s' % (self.uid, key_prefix)
        return self.make_key(key, server_name=self._server_name)

    def apply_strategy(self, apply_info, sort='apply'):
        """
        申请合作: sort: apply
        被邀合作: sort: invite
        """
        to_uid = apply_info['uid']
        apply_key = self.get_apply_key(sort)
        info = encrypt_data(apply_info)
        self.redis.hset(apply_key, to_uid, info)

    def del_apply(self, from_uid, sort='apply'):
        """ 删除被邀信息
        """
        invite_key = self.get_apply_key(sort)

        self.redis.hdel(invite_key, from_uid)

    def del_all_apply(self, sort='apply'):
        """ 删除所有的请求
        """
        invite_key = self.get_apply_key(sort)
        self.redis.delete(invite_key)

    @property
    def apply_info(self):
        """ 我的申请信息
        """
        apply_key = self.get_apply_key(sort='apply')
        info = {k: dencrypt_data(v) for k, v in self.redis.hgetall(apply_key).iteritems()}
        return info

    @property
    def invite_info(self):
        """ 我的受邀信息
        """
        invite_key = self.get_apply_key(sort='invite')
        info = {k: dencrypt_data(v) for k, v in self.redis.hgetall(invite_key).iteritems()}
        return info

    @property
    def refuse_info(self):
        """ 我被拒绝的信息
        """
        invite_key = self.get_apply_key(sort='refuse')
        info = {k: dencrypt_data(v) for k, v in self.redis.hgetall(invite_key).iteritems()}
        return info

    @property
    def strategy_mission(self):
        if not self.strategy_uid:
            return None
        if not hasattr(self, '_strategy_mission'):
            strategy_uids = sorted([self.mm.uid, self.strategy_uid])
            self.strategy_server = strategy_uids[0][:-7]
            self.strategy_id = '_'.join(strategy_uids)
            self._strategy_mission = self.mm.get_obj_by_id('strategy_mission', self.strategy_id, server=self.strategy_server)
        return self._strategy_mission


ModelManager.register_model('strategy', Strategy)