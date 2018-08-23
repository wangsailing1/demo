# -*- coding: utf-8 –*-

"""
Created on 2018-05-30

@author: sm
"""

from lib.db import ModelBase


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in value:
            ret += ret * self.seed + ord(i)
        return (self.cap - 1) & ret


class BloomFilter(object):
    # 128M 7个seed 够 4kw 条数据使用了，设备码判重也不需要那么精确，不够的话可以扩展key数量
    KEY = 'bloomfilter.device_mark'
    SERVER_NAME = 'master'

    def __init__(self):
        self.redis = ModelBase.get_redis_client(self.SERVER_NAME)

        self.bit_size = 1 << 30  # Redis的String类型最大容量为512M，现使用128M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.hash_funcs = []

        for seed in self.seeds:
            self.hash_funcs.append(SimpleHash(self.bit_size, seed))

    def is_contains(self, value):
        ret = True
        for f in self.hash_funcs:
            offset = f.hash(value)
            ret = ret & self.redis.getbit(self.KEY, offset)
        return ret

    def insert(self, value):
        for f in self.hash_funcs:
            offset = f.hash(value)
            self.redis.setbit(self.KEY, offset, 1)
