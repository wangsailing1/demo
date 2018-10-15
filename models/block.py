#! --*-- coding: utf-8 --*--

import time

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class Block(ModelBase):
    NUM = 'num'
    REWORD_TIME = '22:30:00'

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'block_num': 1,
            'cup': 0,
            'block_group': 1,
        }

        super(Block, self).__init__(self.uid)

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
        :param type:  剧本type ，男，女，媒体评分，观众评分
        :return: 
        """
        if not group and not type:
            return '%s' % (block)
        if not type:
            return '%s||%s' % (block, group)
        return '%s||%s||%s' % (block, group, type)



ModelManager.register_model('block', Block)
