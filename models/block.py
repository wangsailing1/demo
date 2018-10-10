#! --*-- coding: utf-8 --*--

import time
import math

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class Block(ModelBase):
    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'block': 1,
            'cup': 0,
            'block_group': 1,
        }

        super(Block, self).__init__(self.uid)

    def up_block(self, cup):
        config = game_config.dan_grading_list
        self.cup += cup
        while True:
            if self.cup >= config[self.block]['promotion_cup_num']:
                self.block += 1
            else:
                break

        # todo 升级街区  删除原有排行 增加新排行 更新block，block_group
        self.save()
