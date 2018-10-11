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

        self.save()

    #
    def get_key(self):
        return self.make_key(uid=self.block_num)

    #
    def get_block_key(self):
        key = self.make_key(uid=self.block_num)
        key_date = key + '|' + self.get_date()
        return key_date

    #获取日期
    def get_date(self):
        now = time.strftime('%F')
        now_time = time.strftime('%T')
        if now_time >= self.REWORD_TIME:
            now = time.strftime('%F', time.localtime(time.time() + 3600 * 24))
        return now

    #把玩家添加到所属街区
    def add_user_by_block(self, uid=None, score=0):
        if not uid:
            uid = self.uid
        key_date = self.get_block_key()
        self.fredis.zadd(self._key_date, uid, score)
        self.fredis.expire(self._key_date, 7 * 24 * 3600)

    #从街区删除玩家（玩家升级街区后操作）
    def delete_user_by_block(self, uid=None):
        if not uid:
            uid = self.block_num - 1
        self._key = self.make_key(uid=uid)
        self.fredis.zrem(self._key, self.uid)

    #检查玩家是否在所属街区
    def check_user_exist_by_block(self, uid=None):
        if not uid:
            uid = self.uid
        return self.fredis.zscore(self._key_date,uid)

    #获取编号
    def get_num(self):
        self._key_date = '%s|%s'%(self._key_date,self.NUM)
        return self.fredis.incr(self._key_date)


    #计算玩家所属组
    def get_group(self,rank=None):
        # if not uid:
        #     uid = self.uid
        #rank = self.fredis.zrank(self._key_date, uid)
        if rank == 0:
            return 1
        if rank % 100 or not rank % 100 and rank / 100:
            return rank / 100 + 1
        return rank / 100



ModelManager.register_model('block', Block)
