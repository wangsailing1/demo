#! --*-- encoding:utf-8 --*--

import redis
import settings

REDIS_CLIENT_DICT = {}


def make_redis_client(redis_config):
    pool = redis.BlockingConnectionPool(**redis_config)
    redis_client = redis.Redis(connection_pool=pool)
    return redis_client

class ModelBase():
    _need_diff = ()
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

    @classmethod
    def get_redis_client(cls, feature=''):
        redis_config = settings.SERVERS[feature]['redis']
        redis_client = make_redis_client(redis_config)

        return redis_client

    @classmethod
    def make_key_cls(cls, uid, feature=''):
        _key = '_'.join(uid, feature)
        return _key

    @classmethod
    def loads(cls, uid, data, o=None):

        o = o or cls(uid)
        for k in cls._attrs_base:
            v = data.get(k)
            if v is None:
                v = o._attrs_base[k]
                if k in cls._need_diff:
                    o._old_data[k] = v
            else:
                if k in cls._need_diff:
                  o._old_data[k] = 'ok'
            setattr(o, k, v)

        return o

    def dumps(self):
        """
        :param : 数据序列化, 准备存数据库
        :return:
        """
        r = {}

        for k in self._attrs_base:
            data = getattr(self, k)
            r[k] = data

        return r

    @classmethod
    def get(cls, uid='', feature=''):
        """
        :param uid:
        :return:
        """
        _key = cls.make_key_cls(uid, feature)
        redis_client = cls.get_redis_client(feature)
        o = cls(uid)
        o._model_key = _key
        o.redis = redis_client
        redis_data = redis_client.get(_key)
        o = cls.loads(uid, redis_data)

        return o








