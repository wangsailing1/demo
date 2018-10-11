#! --*-- coding: utf-8 --*--

import time
import math

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class Block(ModelBase):
    NUM = 'num'
    REWORD_TIME = '22:30:00'

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'block': 1,
            'cup': 0,
            'block_group': 1,
        }
        self._key = self.make_key(uid=uid)
        self._key_date = self._key + '|' + self.get_date()

        super(Block, self).__init__(self.uid)

    def up_block(self, cup):
        config = game_config.dan_grading_list
        self.cup += cup
        if self.cup >= config[self.block]['promotion_cup_num']:
            self.block += 1

        self.save()

    def get_date(self):
        now = time.strftime('%F')
        now_time = time.strftime('%T')
        if now_time >= self.REWORD_TIME:
            now = time.strftime('%F', time.localtime(time.time() + 3600 * 24))
        return now

    def add_user_by_block(self, uid=None, score=0):
        if not uid:
            uid = self.uid
        self.fredis.zadd(self._key_date, uid, score)
        self.fredis.expire(self._key_date, 7 * 24 * 3600)


    def delete_user_by_block(self, uid=None):
        if not uid:
            uid = self.block - 1
        self._key = self.make_key(uid=uid)
        self.fredis.zrem(self._key, self.uid)

    def check_user_exist_by_block(self, uid=None):
        return self.fredis.zrank(self._key_date)


ModelManager.register_model('block', Block)
