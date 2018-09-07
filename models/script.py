# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
from gconfig import game_config

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import weight_choice
from lib.core.environ import ModelManager


class Script(ModelBase):
    POOL_SIZE = 3

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'cur_script': {},  # 当前在在拍的片子
            'scripts': {},  # 所有已拍完的片子

            'script_pool': {},
        }
        super(Script, self).__init__(self.uid)

    def pre_use(self):
        # todo 拍摄完的片子结算
        if 0:
            cur_script = self.cur_script
            if cur_script:
                if cur_script['step'] == 4:
                    self.scripts[cur_script['oid']] = cur_script
                    self.cur_script = {}

    @classmethod
    def _make_oid(cls, script_id):
        """ 生成only id

        :param script_id:
        :return:
        """
        return '%s-%s-%s' % (script_id, int(time.time()), salt_generator())

    def pre_filming(self):
        self.script_pool.clear()
        can_use_ids = [(k, v['rate']) for k, v in game_config.script.iteritems()]
        for i in xrange(self.POOL_SIZE):
            id_weight = weight_choice(can_use_ids)
            can_use_ids.remove(id_weight)
            self.script_pool[id_weight[0]] = 0

    def make_film(self, script_id, name):
        data = {
            'step': 1,  # 拍摄进度  1: 艺人选择; 2: 类型选择 3: 宣传预热  4: 杀青
            'name': name,
            'card': {},  # 艺人角色 {rol_id: card_oid}
            'id': script_id,
            'oid': self._make_oid(script_id),
            'style': '',            # 剧本类型
            'ts': int(time.time())
        }
        return data


ModelManager.register_model('script', Script)
