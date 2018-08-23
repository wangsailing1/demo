# -*- coding: utf-8 -*-

import datetime
import cPickle as pickle
from hashlib import md5
from lib.db import ModelTools


class Admin(ModelTools):
    """
    管理员
    """
    SERVER_NAME = 'master'
    redis = ModelTools.get_redis_client(SERVER_NAME)
    ADMIN_PREFIX = 'game_admin'     # admin 存储hash表

    def __init__(self, username=None):

        self.username = username    # 管理员账号
        self.password = ""    # 管理员密码
        self.email = ""    # 邮件
        self.last_ip = "0.0.0.0"
        self.last_login = datetime.datetime.now()
        self.permissions = {}    # 管理员可用权限
        self.is_super = False      # 是否是超级管理员
        self.disable = False        # 是否禁用该管理员

    @classmethod
    def get(cls, username):
        d = cls.redis.hget(cls.ADMIN_PREFIX, username)
        if d:
            o = cls()
            o.__dict__.update(pickle.loads(d))
            return o

    @classmethod
    def get_all_user(cls):
        d = cls.redis.hgetall(cls.ADMIN_PREFIX)
        return {k:pickle.loads(v) for k, v in d.iteritems()}

    def save(self):
        if self.password and not self.password[0] == '\x01':
            self.password = '\x01' + md5(self.password).hexdigest()
        d = self.__dict__
        self.redis.hset(self.ADMIN_PREFIX, self.username, pickle.dumps(d))

    def set_password(self, raw_password):
        """ 设置密码

        :param raw_password:
        :return:
        """
        self.password = raw_password

    def check_password(self, raw_password):
        """ 检查密码

        :param raw_password:
        :return:
        """
        if self.password and self.password[0] == '\x01':
            return self.password == '\x01' + md5(raw_password).hexdigest()
        else:
            return self.password == raw_password

    def set_last_login(self, time, ip):
        self.last_login = time
        self.last_ip = ip

    def delete(self):
        self.redis.hdel(self.ADMIN_PREFIX, self.username)

    def check_permission(self, module_name, method_name):
        if module_name == 'menu':
            return True
        if method_name in self.permissions.get(module_name, []):
            return True
        else:
            return False
