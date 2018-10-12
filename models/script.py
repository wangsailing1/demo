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
from models.ranking_list import AppealRank


class Script(ModelBase):
    POOL_SIZE = 3

    _need_diff = ('own_script',)

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'style_log': [],  # 连续拍片类型，保留最近10个
            'own_script': [],  # 已获得的可拍摄的片子
            'cur_script': {},  # 当前在在拍的片子
            'scripts': {},  # 所有已拍完的片子

            'script_pool': {},
            'cur_market': [],  # 当前市场关注度


            # 各种最高收入排行
            'top_script': {},       # 按剧本id
            'top_group': {},        # 按剧本系列 {gruop_id: film_info}
            'top_all': {},          # 单片票房最高

        }
        super(Script, self).__init__(self.uid)

    def pre_use(self):
        # 连续拍片类型，保留最近10个
        self.style_log = self.style_log[-10:]
        if self.cur_script:
            if 'finished_step' not in self.cur_script:
                self.cur_script['finished_step'] = 0
            for k in ['finished_common_reward', 'finished_attr', 'finished_attention',
                      'finished_first_income', 'finished_summary']:
                if k not in self.cur_script:
                    self.cur_script[k] = {}

        # todo 拍摄完的片子结算 9 是票房分析，目前流程没有
        if self.cur_script.get('finished_step') in [8, 9]:
            self.check_top_income(self.cur_script)
            self.cur_script = {}
            self.script_pool = {}

            # if cur_script['step'] == 4:
            #     self.scripts[cur_script['oid']] = cur_script
            #     self.cur_script = {}

    def check_top_income(self, film_info):
        script_id = film_info['id']
        script_config = game_config.script[script_id]
        group_id = script_config['group']

        cur_top_script = self.top_script.get(script_id, {})
        cur_top_group = self.top_group.get(group_id, {})
        income = film_info['finished_summary']['income']

        save = False
        # 按剧本id记录
        top_script_income = cur_top_script.get('finished_summary', {'income': 0})['income']
        if top_script_income < income:
            self.top_script[script_id] = dict(film_info)
            save = True

        # 按剧本系列记录
        top_group_income = cur_top_group.get('finished_summary', {'income': 0})['income']
        if top_group_income < income:
            self.top_group[group_id] = dict(film_info)
            save = True

        # 单片记录
        top_income = self.top_all.get('finished_summary', {'income': 0})['income']
        if top_income < income:
            self.top_all = dict(film_info)
            save = True

        self.mm.script_book.add_book(script_id)
        self.mm.script_book.add_script_group(script_id, True, income)

        # todo 跟新艺人号召力排行
        # guid = self.uid + '|' + str(group_id)
        # ar = AppealRank(uid=guid)  # uid 格式 uid + '|' + group_id

        if save:
            self.save()

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
        self.script_pool = {}
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
            'finished_step': 0,  # 拍摄结算进度 1: 通用奖励、艺人关注度；2：拍摄属性、熟练度；3：弹出新闻关注度
            # 4: 首日上映; 5: 专业评价; 6: 持续上映; 7: 观众评价
            'name': name,
            'card': {},  # 艺人角色 {rol_id: card_oid}
            'id': script_id,
            'oid': self._make_oid(script_id),
            'style': 0,  # 剧本类型
            'ts': int(time.time()),
            'single_style': False,  # 是否连续同样类型
            'suit': 0,  # 片子类型适合档次
            'pro': [0] * 6,  # 各个属性值

            'result_step': 0,  # 结算阶段，前端修改，前端使用
            'result': {},  # 拍片结算结果 {'reward': {}, }

            'summary': {'income': 100, 'cost': 50},  # 票房总结

            # 结算的几个阶段奖励
            'finished_common_reward': {},
            'finished_attr': {},
            'finished_attention': {},
            'finished_first_income': {},
            'finished_curve': {},           # 持续上映曲线
            'finished_medium_judge': 0,     # 评价 专业评价 100
            'finished_audience_judge': 0,   # 评价 观众评价 200
            'finished_summary': {},         # 票房总结{'income': 100, 'cost': 50},
            'finished_analyse': {},         # 票房分析


            'attention': 0,  # 关注度
            'audience': 0,  # 观众
        }
        return data

    def get_top_group(self):

        top_group = {}
        for script_id, info in self.top_script.iteritems():
            group_id = game_config.script[script_id]['group']
            if group_id not in top_group:
                top_group[group_id] = {}
            top_group[group_id][script_id] = info
            top_group[group_id]['top_income'] = top_group[group_id].get('top_income', 0) + info['income']
            sequel_count = game_config.script[script_id]['sequel_count']
            if top_group[group_id].get('max_script', 0) <= sequel_count:
                top_group[group_id]['max_script'] = sequel_count
        return top_group

    def get_top_group_id(self):
        group_id = 0
        income = 0
        for k, v in self.get_top_group().iteritems():
            if v['top_income'] > income:
                income = v['top_income']
                group_id = k
        return group_id


ModelManager.register_model('script', Script)
