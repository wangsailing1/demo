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
        :param block: 
        :param group: 
        :param type:  剧本type ，男，女，媒体评分，观众评分
        :return: 
        """
        if not group and not type:
            return '%s' % (block)
        if not type:
            return '%s||%s' % (block, group)
        return '%s||%s||%s' % (block, group, type)

    # 获取玩家存储key
    def get_block_key(self):
        key = self.make_key(uid=self.block_num)
        key_date = key + '|' + self.get_date()
        return key_date

    # 获取日期
    def get_date(self):
        now = time.strftime('%F')
        now_time = time.strftime('%T')
        if now_time >= self.REWORD_TIME:
            now = time.strftime('%F', time.localtime(time.time() + 3600 * 24))
        return now

    # 把玩家添加到所属街区
    def add_user_by_block(self, uid=None, score=0):
        if not uid:
            uid = self.uid
        key_date = self.get_block_key()
        self.fredis.zadd(key_date, uid, score)
        self.fredis.expire(key_date, 7 * 24 * 3600)

    # 从街区删除玩家（玩家升级街区后操作）
    def delete_user_by_block(self, uid=None, date=None, num=None):
        if not num:
            num = self.block_num - 1
        if not date:
            date = self.get_date()
        if not uid:
            uid = self.uid
        key = self.make_key(uid=num)
        key_date = key + '|' + date
        self.fredis.zrem(key_date, uid)

    # 检查玩家是否在所属街区
    def check_user_exist_by_block(self, uid=None):
        if not uid:
            uid = self.uid
        key_date = self.get_block_key()
        return self.fredis.zscore(key_date, uid)

    # 获取编号
    def get_num(self):
        key_date = self.get_block_key()
        key_date = '%s|%s' % (key_date, self.NUM)
        return self.fredis.incr(key_date)

    # 计算玩家所属组
    def get_group(self, uid=None):
        if not uid:
            uid = self.uid
        rank = self.fredis.zrank(self._key_date, uid)
        if rank == 0:
            return 1
        if rank % 100 or not rank % 100 and rank / 100:
            return rank / 100 + 1
        return rank / 100

    # 记录最大的有人街区
    def set_max_block(self):
        key = self.make_key(uid='block')
        max_block = int(self.fredis.get(key)) if self.fredis.get(key) else 0
        if self.block_num > max_block:
            self.fredis.set(key, self.block_num)

    # 获取最大的有人街区
    def get_max_block(self):
        key = self.make_key(uid='block')
        return int(self.fredis.get(key)) if self.fredis.get(key) else 0


ModelManager.register_model('block', Block)
