#! --*-- encoding:utf-8 --*--
import hashlib
import redis
import settings
import ast
REDIS_CLIENT_DICT = {}


def make_redis_client(redis_config):
    pool = redis.BlockingConnectionPool(**redis_config)
    redis_client = redis.Redis(connection_pool=pool)
    return redis_client

def md5(s):
    """# md5: docstring
    args:
        s:    ---    arg
    returns:
        0    ---
    """
    return hashlib.md5(str(s)).hexdigest()


class ModelBase(object):
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
        self._model_key = None
        self.redis = None

    @classmethod
    def get_redis_client(cls):
        redis_config = settings.SERVERS['user']['redis']
        redis_client = make_redis_client(redis_config)

        return redis_client

    @classmethod
    def make_key_cls(cls, uid):
        return cls._key_prefix()+"||%s"%str(uid)

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
        r = str(r)
        return r

    @classmethod
    def get(cls, uid='', mm=None):
        """
        :param uid:
        :return:
        """
        _key = cls.make_key_cls(uid)
        redis_client = cls.get_redis_client()
        o = cls(uid)
        o._model_key = _key
        o.redis = redis_client
        redis_data = o.redis.get(_key)
        redis_data = ast.literal_eval(redis_data) if redis_data else {}
        if not redis_data:
            o.inited = True
            o.mm = mm
        else:
            o = cls.loads(uid, redis_data, o=o)
            o.inited = False
            o.mm = mm
        return o

    def save(self, uid=''):
        self._save(uid)

    def _save(self, uid=''):
        _key = self._model_key
        if not _key:
            _key = self.__class__.make_key_cls(uid)
        s = self.dumps()
        self.redis.set(_key, s)
        print '保存数据成功 : %s' % _key

    @classmethod
    def _key_prefix(cls):
        return "%s||%s" % (cls.__module__, cls.__name__)










