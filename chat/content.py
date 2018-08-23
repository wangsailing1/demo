#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import re
import redis

import settings
from models.user import User as UserM


class Content(object):

    REDIS_CLIENT_DICT = {}
    KEY_PREFIX = ''
    DEFAULT_PUSH_MESSAGE_NUM = 60
    MESSAGE_SHOW_SIZE = 20

    def __init__(self, server, redis_config):
        self.server = server
        self.redis_config = redis_config
        self.msgs = []

    @classmethod
    def get_redis_client(cls, redis_config):
        """# make_redis_client: docstring
        args:
            redis_config:    ---    arg
        returns:
            0    ---
        """
        client_key = '_'.join([redis_config['host'], str(redis_config['port']), str(redis_config['db'])])
        if client_key not in cls.REDIS_CLIENT_DICT:
            if cmp(redis.VERSION, (2, 10, 1)) >= 0:
                pool = redis.BlockingConnectionPool(retry_on_timeout=True, **redis_config)
            else:
                pool = redis.BlockingConnectionPool(**redis_config)
            client = redis.Redis(connection_pool=pool)
            cls.REDIS_CLIENT_DICT[client_key] = client
        return cls.REDIS_CLIENT_DICT[client_key]

    def get_key_prefix(self, key=''):
        return '%s%s_%s' % (self.KEY_PREFIX, self.server, key)

    def get(self, key=''):
        redis_obj = self.get_redis_client(self.redis_config)
        self._key = self.get_key_prefix(key)
        self._redis = redis_obj
        msgs = self._redis.lrange(self._key, 0, -1)
        self.msgs += msgs
        return self.msgs

    def show(self, next_flag=0, uid=''):
        if next_flag:
            msg = self.msgs[-self.MESSAGE_SHOW_SIZE * (next_flag + 1): -self.MESSAGE_SHOW_SIZE * next_flag]
        else:
            msg = self.msgs[-self.MESSAGE_SHOW_SIZE:]

        if not uid:
            return msg

        # 过滤屏蔽的玩家
        user = UserM.get(uid, from_req=False)
        for i in msg[:]:
            re_data = re.findall('"uid": "(%s\d+)"' % settings.UID_PREFIX, i)
            if not re_data:
                continue
            re_uid = re_data[0]
            if re_uid in user.blacklist:
                msg.remove(i)

        return msg

    def save(self, key=''):
        if not hasattr(self, '_redis'):
            redis_obj = self.get_redis_client(self.redis_config)
            self._key = self.get_key_prefix(key)
            self._redis = redis_obj
        self._redis.delete(self._key)
        if self.msgs:
            self._redis.rpush(self._key, *self.msgs)
            self._redis.ltrim(self._key, -self.DEFAULT_PUSH_MESSAGE_NUM, -1)

    def add(self, *msg):
        # self._redis.rpush(self._key, *msg)
        # self._redis.ltrim(self._key, -self.DEFAULT_PUSH_MESSAGE_NUM, -1)
        self.msgs.extend(msg)
        self.msgs = self.msgs[-self.DEFAULT_PUSH_MESSAGE_NUM:]


class FriendContent(Content):
    KEY_PREFIX = 'chat_msg_friend_'
    FRIEND_MAPPING_KEY = 'chat_msg_friend_mapping_'
    FRIEND_MESSAGE_CACHE_EXPIRE = 7 * 24 * 60 * 60  # 私聊信息有效期

    def get(self, key=''):
        super(FriendContent, self).get(key)
        # self._redis.delete(self._key)
        return self.msgs

    def save(self, key=''):
        super(FriendContent, self).save(key)
        if self.msgs:
            self._redis.expire(self._key, self.FRIEND_MESSAGE_CACHE_EXPIRE)

    def add(self, *msg):
        self.msgs.extend(msg)
        self.msgs = self.msgs[-self.DEFAULT_PUSH_MESSAGE_NUM:]

    def get_friend_mapping_key(self, uid):
        return '%s%s_%s' % (self.FRIEND_MAPPING_KEY, self.server, uid)

    def add_friend_mapping(self, uid, friend_uid):
        key = self.get_friend_mapping_key(uid)
        uids = self.get_friend_mapping(uid)
        if friend_uid in uids:
            return
        self._redis.rpush(key, friend_uid)
        self._redis.expire(key, self.FRIEND_MESSAGE_CACHE_EXPIRE)

    def get_friend_mapping(self, uid):
        key = self.get_friend_mapping_key(uid)
        uids = self._redis.lrange(key, 0, -1)
        return uids


class WorldSystemContent(Content):
    KEY_PREFIX = 'chat_msg_world_system_'


class SystemContent(Content):
    KEY_PREFIX = 'chat_msg_system_'


class AllWorldContent(Content):
    KEY_PREFIX = 'chat_msg_all_world_'

    def __init__(self, server, redis_config):
        self.server = 'chat'
        self.redis_config = settings.chat_config
        self.msgs = []


class GuildContent(Content):
    KEY_PREFIX = 'chat_msg_guild_'


class GuildWarContent(Content):
    KEY_PREFIX = 'chat_msg_guild_war_'


class RobContent(Content):
    KEY_PREFIX = 'chat_msg_rob_'


class EscortContent(Content):
    KEY_PREFIX = 'chat_msg_escort_'


class ContentFactory(object):
    MAPPINGS = {
        'all_world': 'AllWorld',
        'world': 'WorldSystem',
        'system': 'System',
        'guild': 'Guild',
        # 'guild_war': 'GuildWar',
        # 'rob': 'Rob',
        # 'escort': 'Escort',
        'friend': 'Friend',
    }
    IGNORE = ['Friend', 'Guild']

    def __init__(self, redis_config):
        self._contents = {}
        self.redis_config = redis_config

    def generate_key(self, sort, server, key):
        return '%s_%s_%s' % (sort, server, key)

    def get(self, sort, server, key=''):
        _key = self.generate_key(sort, server, key)
        if _key in self._contents:
            return self._contents[_key]

        class_name = '%sContent' % sort
        class_func = globals().get(class_name)
        if class_func:
            self._contents[_key] = class_func(server, self.redis_config)
            # if sort in self.IGNORE:
            #     self._contents[_key].get(key)
            self._contents[_key].get(key)

        return self._contents[_key]

    def delete(self, sort, server, key=''):
        _key = self.generate_key(sort, server, key)
        if _key in self._contents:
            del self._contents[_key]

    def save(self):
        for content in self._contents.itervalues():
            content.save()
