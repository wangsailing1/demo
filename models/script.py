# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
import random
import itertools
from gconfig import game_config

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import weight_choice
from lib.core.environ import ModelManager


class Script(ModelBase):
    POOL_SIZE = 3

    _need_diff = ('own_script', )
    
    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'style_log': [],       # 连续拍片类型，保留最近10个
            'own_script': [],      # 已获得的可拍摄的片子
            'cur_script': {},  # 当前在在拍的片子
            'scripts': {},  # 所有已拍完的片子

            'script_pool': {},
            'cur_market': [],       # 当前市场关注度
        }
        super(Script, self).__init__(self.uid)

    def pre_use(self):
        # 连续拍片类型，保留最近10个
        self.style_log = self.style_log[-10:]
        if self.cur_script:
            if 'finished_step' not in self.cur_script:
                self.cur_script['finished_step'] = 0
            for k in ['finished_common_reward', 'finished_attr', 'finished_attention',
                      'finished_first_income']:
                if k not in self.cur_script:
                    self.cur_script[k] = {}

        # todo 拍摄完的片子结算
        if self.cur_script.get('result'):
            cur_script = self.cur_script
            # if cur_script['step'] == 4:
            #     self.scripts[cur_script['oid']] = cur_script
            #     self.cur_script = {}

    def add_own_script(self, script_id):
        if script_id in self.own_script:
            return False
        self.own_script.append(script_id)
        return True

    @classmethod
    def _make_oid(cls, script_id):
        """ 生成only id

        :param script_id:
        :return:
        """
        return '%s-%s-%s' % (script_id, int(time.time()), salt_generator())

    def pre_filming(self):
        self.script_pool.clear()
        can_use_ids = [(k, v['rate']) for k, v in game_config.script.iteritems() if k in self.own_script]
        for i in xrange(self.POOL_SIZE):
            if not can_use_ids:
                break
            id_weight = weight_choice(can_use_ids)
            can_use_ids.remove(id_weight)
            self.script_pool[id_weight[0]] = 0

        # 初始化市场关注度
        all_market = [(v['market'], v['rate']) for k, v in game_config.script_market.iteritems()]
        if all_market:
            choiced_market = weight_choice(all_market)
            cur_market = list(choiced_market[0])
            del_unit = game_config.common[17]
            # 随机三次减少关注度
            market_length = len(cur_market)
            for i in range(3):
                idx = random.randint(0, market_length - 1)
                if cur_market[idx] > del_unit:
                    cur_market[idx] = cur_market[idx] - del_unit

            self.cur_market = cur_market

    def make_film(self, script_id, name):
        data = {
            'step': 1,  # 拍摄进度  1: 艺人选择; 2: 类型选择 3: 宣传预热  4: 杀青
            'finished_step': 0,     # 拍摄结算进度 1: 通用奖励、艺人关注度；2：拍摄属性、熟练度；3：弹出新闻关注度
                                    # 4: 专业评价; 5: 持续上映; 6: 观众评价; 7: 票房总结
            'name': name,
            'card': {},  # 艺人角色 {rol_id: card_oid}
            'id': script_id,
            'oid': self._make_oid(script_id),
            'style': 0,            # 剧本类型
            'ts': int(time.time()),
            'single_style': False,           # 是否连续同样类型
            'suit': 0,                       # 片子类型适合档次
            'pro': [0] * 6,                       # 各个属性值

            'result_step': 0,       # 结算阶段，前端修改，前端使用
            'result': {},           # 拍片结算结果 {'reward': {}, }

            'attention_info': {},
            'continue_reward': [],      # 持续上映奖励
            'summary': {'income': 100, 'cost': 50},              # 票房总结

            # 结算的几个阶段奖励
            'finished_common_reward': {},
            'finished_attr': {},
            'finished_attention': {},
            'finished_first_income': {},
            'finished_medium_judge': 0,  # 评价 专业评价 100
            'finished_audience_judge': 0,  # 评价 观众评价 200


            'attention': 0,     # 关注度
            'audience': 0,      # 观众
        }
        return data


ModelManager.register_model('script', Script)
