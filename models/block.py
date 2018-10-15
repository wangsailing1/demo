#! --*-- coding: utf-8 --*--

import time

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config

REWORD_TIME = '22:30:00'

class Block(ModelBase):
    NUM = 'num'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'block_num': 1,
            'cup': 0,
            'block_group': 1,
            'top_script':{},
            'big_sale':0,
            'last_date':'',
            'reward_data':{},
            'award_ceremony':0,
            'reward_daily':'',
        }

        super(Block, self).__init__(self.uid)

    def pre_use(self):
        if self.last_date != get_date():
            self.last_date = get_date()

            #todo 计算奖杯
            self.reward_data = self.count_cup()
            self.big_sale = 0
            self.top_script = {}
            self.award_ceremony = 0
            self.save()

    def count_cup(self):
        return {}

    def up_block(self, cup):
        config = game_config.dan_grading_list
        self.cup += cup
        if self.cup >= config[self.block_num]['promotion_cup_num']:
            self.block_num += 1
            self.cup = 0
        self.save()

    def get_key_profix(self, block=1, group='', type=''):
        """
        :param block: block(记录街区所有人)  block_num(取编码)
        :param group: 
        :param type:  剧本type ，nan=男，nv=女，medium=媒体评分，audience=观众评分,income=总票房,script=单片票房
        :return: 
        """
        if not group and not type:
            return '%s' % (block)
        if not type:
            return '%s||%s' % (block, group)
        return '%s||%s||%s' % (block, group, type)

# 获取日期
def get_date():
    now = time.strftime('%F')
    now_time = time.strftime('%T')
    if now_time >= REWORD_TIME:
        now = time.strftime('%F', time.localtime(time.time() + 3600 * 24))
    return now



ModelManager.register_model('block', Block)
