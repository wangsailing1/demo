#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import sys
import itertools
import time
import redis
import hashlib


import settings
from lib.utils.debug import print_log_maker
from lib.utils.debug import print_log, get_stack_info
import cPickle as pickle
from lib.utils.zip_date import dencrypt_data, encrypt_data

REDIS_CLIENT_DICT = {}  # 每个db都有一个pool


def make_redis_client(redis_config):
    """# make_redis_client: docstring
    args:
        redis_config:    ---    arg
    returns:
        0    ---    
    """
    try:
        if cmp(redis.VERSION, (2, 10, 1)) >= 0:
            pool = redis.BlockingConnectionPool(retry_on_timeout=True, **redis_config)
        else:
            pool = redis.BlockingConnectionPool(**redis_config)
    except:
        pool = redis.BlockingConnectionPool(**redis_config)

    redis_client = redis.Redis(connection_pool=pool)

    return redis_client


def get_redis_client(redis_config):
    """
    args:
        redis_config:
                {'db': 4,
                 'host': '10.6.7.25',
                 'password': 'F8974044A778',
                 'port': 6379,
                 'socket_timeout': 5}
    """
    client_key = '_'.join([redis_config['host'], str(redis_config['port']), str(redis_config['db'])])
    if client_key not in REDIS_CLIENT_DICT:
        client = make_redis_client(redis_config)
        REDIS_CLIENT_DICT[client_key] = client
    return REDIS_CLIENT_DICT[client_key]


def dict_diff(old, new):
    """# dict_diff: 比较两个字典
    args:
        old, new:    ---    arg
    returns:
        0    ---    
    """
    old_keys = set(old.keys())
    new_keys = set(new.keys())

    remove_keys = old_keys - new_keys       # 要被删除的key
    add_keys = new_keys - old_keys          # 要添加的key
    same_keys = new_keys & old_keys         # 新旧共同拥有的key，这个是用来准备做比较修改

    update = {}

    for k in same_keys:
        new_data = new[k]
        if old[k] != new_data:
            update[k] = new_data
    for k in add_keys:
        update[k] = new[k]
    return update, remove_keys


class ModelTools(object):
    """# ModelTools: 一堆工具"""

    @classmethod
    def print_log(cls, *args, **kargs):
        print_log_maker(2)(*args, **kargs)

    @classmethod
    def get_server_name(cls, user_id):
        x = user_id[-7:]
        if not x.isdigit():
            return user_id[:-5]
        return user_id[:-7]

    @classmethod
    def get_redis_client(cls, server_name):
        """ 通过服标志获取redis实例

        :param server_name:
        :return:
        """
        redis_config = settings.SERVERS[server_name]['redis']
        client_key = '_'.join([redis_config['host'], str(redis_config['port']), str(redis_config['db'])])
        client = REDIS_CLIENT_DICT.get(client_key)
        if client is None:
            client = make_redis_client(redis_config)
            REDIS_CLIENT_DICT[client_key] = client
        return client

    @classmethod
    def get_father_redis(cls, server_name):
        """ 通过服标志获取redis实例

        :param server_name:
        :return:
        """
        father_name = settings.get_father_server(server_name)
        return cls.get_redis_client(father_name)

    @classmethod
    def _key_prefix(cls, server_name=''):
        if not server_name:
            server_name = cls.SERVER_NAME
        return "%s||%s||%s"%(cls.__module__, cls.__name__, server_name)

    @classmethod
    def _key_to_uid(cls, _key, server_name=''):
        return _key.repalce(cls._key_prefix(server_name)+'||', '')
    
    def make_key(self,uid='', server_name=''):
        """# make_key: docstring
        args:
            :    ---    arg
        returns:
            0    ---    
        """
        if not uid:
            uid = self.uid
        if not server_name:
            server_name = self._server_name
        if not server_name:
            server_name = self.SERVER_NAME
        return self.__class__.make_key_cls(uid, server_name)

    @classmethod
    def make_key_cls(cls, uid, server_name):
        return cls._key_prefix(server_name)+"||%s"%str(uid)

    @classmethod
    def run_data_version_update(cls, _key, o):
        next_dv = o._data_version__ + 1
        data_update_func = getattr(o, 'data_update_func_%d' % next_dv, None)
        while data_update_func and callable(data_update_func):
            o._data_version__ = next_dv
            data_update_func()
            if settings.DEBUG:
                print '%s.%s complate' % (_key, data_update_func.__name__)
            next_dv += 1
            data_update_func = getattr(o, 'data_update_func_%d' % next_dv, None)


class ModelBase(ModelTools):
    """

    """
    SERVER_NAME = None
    _need_diff = ()     # 开关，判断是否需要对数据进行对比，如果需要，则元组中的元素为需要diff的key的名字
    def __new__(cls, *args, **kwargs):
        """

        :param cls:
        :param args:
        :param kwargs:
        :return:
        """
        cls._attrs_base = {
            '_data_version__': 0,
        }
        cls._attrs = {}

        return object.__new__(cls)

    def __init__(self, uid=None):
        """

        :param uid:
        :return:
        """
        if not self._attrs:
            raise ValueError, '_attrs_base must be not empty'
        self._attrs_base.update(self._attrs)
        self.__dict__.update(self._attrs_base)
        self.uid = str(uid)
        self._model_key = None
        self._server_name = None
        self.redis = None
        self.mm = None
        self.model_status = -1  # -1 无状态、1 更改
        self.async_save = False
        self._old_data = {}
        self._diff = {  # 数据的变化
                     # attr_key: {
                     #     'update': {key: data}, # 新加入的和修改的数据
                     #     'remove': set(keys),   # 删除的key
        }
        super(ModelBase, self).__init__()

    def _client_cache_update(self):
        """ 前端cache更新机制中，数据的处理方法，有些数据是需要特殊处理的

        :return:
        """
        return self._diff

    @classmethod
    def loads(cls, uid, data, o=None):
        """ 数据反序列化

        :return:
        """
        o = o or cls(uid)

        loads_data = dencrypt_data(data)
        old_loads_data = dencrypt_data(data)

        for k in cls._attrs_base:
            v = loads_data.get(k)
            if v is None:
                v = o._attrs_base[k]
                if k in cls._need_diff:
                    o._old_data[k] = v
            else:
                if k in cls._need_diff:
                    o._old_data[k] = old_loads_data[k]
            setattr(o, k, v)

        return o

    def dumps(self, compress=True):
        """ 数据序列化

        :return:
        """
        r = {}

        for k in self._attrs_base:
            data = getattr(self, k)
            r[k] = data

            if k in self._need_diff:
                if k in self._old_data:
                    old_v = self._old_data[k]
                    if data != old_v:
                        if isinstance(data, dict):  # 如果是字典就dict_diff
                            update_data, remove_keys = dict_diff(old_v, data)
                        elif isinstance(data, list):  # 如果是列表就list_diff
                            update_data = data
                            remove_keys = {}
                        else:
                            update_data = data
                            remove_keys = {}
                        self._diff[k] = {
                            'update': update_data,
                            'remove': remove_keys,
                        }
                else:
                    if isinstance(data, dict):  # 如果是字典就dict_diff
                        update_data, remove_keys = dict_diff({}, data)
                    elif isinstance(data, list):  # 如果是列表就list_diff
                        update_data = data
                        remove_keys = {}
                    else:
                        update_data = data
                        remove_keys = {}

                    self._diff[k] = {
                        'update': update_data,
                        'remove': remove_keys,
                    }

        if compress:
            r = encrypt_data(r, pickle.HIGHEST_PROTOCOL)

        return r

    def save(self, uid='', server_name=''):
        """ 保存

        :param uid:
        :param server_name:
        :return:
        """
        if self.async_save:
            self.model_status = 1
        else:
            self._save(uid=uid, server_name=server_name)

    def _save(self, uid='', server_name=''):
        """ 保存

        :param uid:
        :param server_name:
        :return:
        """

        if server_name:
            if server_name not in settings.SERVERS:
                raise KeyError('ERROR SERVER NAME: %s' % server_name)

        _key = self._model_key

        if not _key:
            if not server_name or self._server_name:
                server_name = self.SERVER_NAME
            if server_name not in settings.SERVERS:
                raise KeyError('ERROR SERVER NAME: %s' % server_name)
            self._server_name = server_name
            _key = self.make_key(uid, server_name)

        s = self.dumps()

        self.redis.set(_key, s)

        if settings.DEBUG:
            print 'model save : ', _key, 'length: %s' % len(s)

    @classmethod
    def get(cls, uid, server_name='', mm=None, *args, **kwargs):
        """
        获得数据
        server_name = 用于指定数据库列表
        need_init : 如果数据库中没有这个数据，是否需要初始化
        """
        if not server_name:
            server_name = cls.SERVER_NAME
        if not server_name:
            server_name = cls.get_server_name(uid)
        if server_name not in settings.SERVERS:
            raise KeyError('ERORR SERVER NAME: %s, UID: %s'%(server_name, str(uid)))

        _key = cls.make_key_cls(uid, server_name)
        redis_client = cls.get_redis_client(server_name)

        o = cls(uid)
        o._server_name = server_name
        o._model_key = _key
        o.redis = redis_client

        o.fredis = cls.get_father_redis(server_name)

        redis_data = redis_client.get(_key)

        if not redis_data:
            o.inited = True
            o.mm = mm
        else:
            o = cls.loads(uid, redis_data, o=o)
            o.inited = False
            o.mm = mm

            cls.run_data_version_update(_key, o)

        if settings.DEBUG:
            print 'model get : %s, status: %s' % (_key, o.inited)

        return o

    def reset(self, save=True):
        """ 重置数据

        :param save:
        :return:
        """
        self.__dict__.update(self._attrs)
        if save:
            self.save()

    def reload(self):
        """ 重新加载数据

        :return:
        """
        self.__dict__.update(self.get(self.uid).__dict__)

    def delete(self):
        """ 删除数据

        :return:
        """
        _key = self._model_key

        self.redis.delete(_key)

    def pre_use(self):
        """模块使用前的预处理方法,在挂载 weak_user 之后调用
        """
        pass

# class SortedSetBase(ModelTools):
#     """ redis 中sortedset封装
#
#     """
#     SERVER_NAME = None
#
#     def __init__(self):
#         super(SortedSetBase, self).__init__()
#
#     def get_rank(self, uid):
#         """ 获取自己排名
#
#         :return:
#         """
#         rank = self.redis.zrevrank(self._key, uid)
#         if rank is None:
#             rank = -1
#         return rank + 1
#
#     def get_score_ranks(self, start=1, end=50, with_score=True):
#         """ 获取前N名 start=1, end=50 为1到50名
#
#         :param start:
#         :param end:
#         :return:
#         """
#         return self.redis.zrevrange(self._key, start - 1, end - 1,
#                                     withscores=with_score, score_cast_func=round_float_or_str)
#
#     def update_score(self, uid, score):
#         """ 更新积分
#
#         :param uid: 玩家uid
#         :param score: 玩家积分
#         :return:
#         """
#         self.redis.zadd(self._key, uid, generate_rank_score(score))
#
#     def rename_rank(self):
#         """ 重命名的数据
#
#         :return:
#         """
#         if self.redis.exists(self._key):
#             self.redis.rename(self._key, '%s_%s' % (self._key, self.get_before_monday_date()))
#
#     def delete(self):
#         """ 删除
#
#         :return:
#         """
#         self.redis.delete(self._key)
#
#     def zcard(self):
#         """ 获得数量
#
#         :return:
#         """
#         return self.redis.zcard(self._key)
