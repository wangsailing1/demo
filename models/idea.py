#! --*-- coding: utf-8 --*--

import settings
from lib.db import make_redis_client
from lib.core.environ import ModelManager
import pickle
import time


class Idea(object):
    redis = make_redis_client(settings.SERVERS['public']['redis'])
    pre_key = 'idea||player||'

    @classmethod
    def get(cls, uid=None):
        return cls()

    def format_message(self, uid, msg):
        mm = ModelManager(uid)
        name = mm.user.name
        value = pickle.dumps({
            'name': name,
            'uid': uid,
            'msg': msg
        }, pickle.HIGHEST_PROTOCOL)
        return value

    def get_num(self):
        key = '%s%s' % (self.pre_key, 'num')
        return str(self.redis.incr(key))

    def add_msg(self, uid, msg):
        date = time.strftime('%F')
        key = self.get_num()
        message = self.format_message(uid, msg)
        h_key = '%s%s' % (self.pre_key, date)
        self.redis.hset(h_key, key, message)
        self.redis.expire(h_key, 3600 * 24 * 7)

    def get_msg(self, date=''):
        result = []
        if date:
            h_key = '%s%s' % (self.pre_key, date)
            data = self.redis.hgetall(h_key)
            for k, value in data.iteritems():
                result.append({'key': k,
                               'date': date,
                               'msg': pickle.loads(value)})
        else:
            for i in range(7):
                date = time.strftime('%F', time.localtime(time.time() - 3600 * 24 * i))
                h_key = '%s%s' % (self.pre_key, date)
                data = self.redis.hgetall(h_key)
                for k, value in data.iteritems():
                    result.append({'key': k,
                                   'date': date,
                                   'msg': pickle.loads(value)})
        return result

    def del_msg(self,date,k):
        h_key = '%s%s' % (self.pre_key, date)
        self.redis.hdel(h_key,k)

# ModelManager.register_model('idea', Idea)
