#! --*-- coding: utf-8 --*--

__author__ = 'sm'


import time
import datetime

import settings
from lib.db import ModelBase
from lib.utils import md5


class Account(ModelBase):
    """ 账号类

    :var passwd: 密码
    :var servers: 服对应游戏号 {'g1': 'g11234567'}, 默认只有一个服
    :var cur_server: 当前的服
    :var sid: session_id
    :var expired: session过期时间
    """
    SERVER_NAME = 'master'
    REGIST_COUNT_PREFIX = 'regist_account_hash_'
    DEVICE_MARK_COUNT_PREFIX = 'regist_device_hash_mark_'
    EXPIRE_TIME = 30 * 24 * 3600

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'passwd': '',
            'servers': {},
            'cur_server': 0,
            'sid': '',
            'mk': '',
            'expired': '',
            'reg_time': 0,  # 账号注册时间
            'tpid': 0,  # 英雄互娱给的 渠道id, 0为母包，母包不上线
        }
        super(Account, self).__init__(self.uid)

    def set_tpid(self, tpid):
        self.tpid = tpid

    @classmethod
    def get_account_count(cls, server=None, today=None):
        key = cls.REGIST_COUNT_PREFIX
        today = today or datetime.datetime.now()
        day_key = '%s%s' % (key, today.strftime('%F'))
        redis = cls.get_redis_client(cls.SERVER_NAME)

        today_info = redis.hgetall(day_key)

        if server:
            today_count = sum([int(v) for k, v in today_info.iteritems() if server == k.split('||')[0]])
        else:
            today_count = sum((int(v) for v in today_info.values()))

        return {'count': today_count, 'info': today_info}

    @classmethod
    def incr_account_count(cls, server, tpid, today=None):
        key = cls.REGIST_COUNT_PREFIX
        today = today or datetime.datetime.now()
        day_key = '%s%s' % (key, today.strftime('%F'))

        redis = cls.get_redis_client(cls.SERVER_NAME)
        pipe = redis.pipeline()

        tp = '%s||%s' % (server, tpid)
        pipe.hincrby(day_key, tp, 1)
        pipe.expire(day_key, cls.EXPIRE_TIME)

        pipe.execute()

    @classmethod
    def get_device_mark_count(cls, server=None, today=None):
        key = cls.DEVICE_MARK_COUNT_PREFIX
        today = today or datetime.datetime.now()
        day_key = '%s%s' % (key, today.strftime('%F'))
        redis = cls.get_redis_client(cls.SERVER_NAME)

        today_info = redis.hgetall(day_key)

        if server:
            today_count = sum([int(v) for k, v in today_info.iteritems() if server == k.split('||')[0]])
        else:
            today_count = sum((int(v) for v in today_info.values()))

        return {'count': today_count, 'info': today_info}

    @classmethod
    def incr_device_mark_count(cls, server, tpid, today=None):
        key = cls.DEVICE_MARK_COUNT_PREFIX
        today = today or datetime.datetime.now()
        day_key = '%s%s' % (key, today.strftime('%F'))

        redis = cls.get_redis_client(cls.SERVER_NAME)
        pipe = redis.pipeline()

        tp = '%s||%s' % (server, tpid)
        pipe.hincrby(day_key, tp, 1)
        pipe.expire(day_key, cls.EXPIRE_TIME)

        pipe.execute()

    @classmethod
    def check_exist(cls, account):
        """ 检查账号是否存在

        :param account:
        :return:
        """
        r = cls.get_redis_client(cls.SERVER_NAME)
        key = cls.make_key_cls(account, cls.SERVER_NAME)
        return r.exists(key)

    def update_passwd(self, passwd):
        """ 更新密码

        :param passwd:
        :return:
        """
        self.passwd = md5(passwd)

    def check_passwd(self, passwd):
        """ 检查密码

        :param passwd:
        :return:
        """
        return self.passwd == md5(passwd)

    def change_account_name(self, new_account):
        """ 更换账号

        :param new_account:
        :return:
        """
        old_key = self.make_key(self.uid, self._server_name)
        new_key = self.make_key_cls(new_account, self._server_name)
        self.redis.rename(old_key, new_key)
        self.uid = new_account

    def get_or_create_session_and_expired(self, force=False):
        """ 获取或者创建session

        :return:
        """
        now = int(time.time())
        is_save = False
        if self.sid:
            if self.expired < now:
                self.sid = md5('%s%s' % (str(now), self.uid))
                self.expired = now + settings.SESSION_EXPIRED
                is_save = True
        else:
            self.sid = md5('%s%s' % (str(now), self.uid))
            self.expired = now + settings.SESSION_EXPIRED
            is_save = True

        if is_save and not force:
            self.save()

        return self.sid, self.expired
