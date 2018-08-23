# coding: utf-8
from fields import ModelItemMixIn
import itertools

class RedisItemMixIn(ModelItemMixIn):
    STORAGE_TYPE = 'redis'

    def init(self, env, attr_name, carrier):
        raise NotImplementedError

    def get_database(self):
        """
        """

        return self.use_db

class RedisString(RedisItemMixIn):
    """ 对Redis String类型操作的封装

    透明Redis的处理细节，方便业务层快速处理调用

    Attributes:
       env: 运行环境
       use_db: 所使用的对应settings里的db
       shared_key: 散列的数值
       value: 当前数值
       to_pyfunc: 将Redis里的数值通过某中方式转成Python对象
    """

    def __init__(self, db_name, to_pyfunc=str):
        self.env = None
        self.use_db = db_name
        self.shared_key = None
        self.value = None
        self.to_pyfunc = to_pyfunc

    def init(self, env, attr_name, carrier):
        """ 初始化操作

        当要加载数据时，会根据名称和model初始化内容

        Args:
            env: 运行环境
            attr_name: 名称
            carrier: 载体Model
        """

        self.key = env.generate_store_key(carrier, attr_name)
        self.env = env
        connect = env.storage.connects.get(self)
        self.value = self.to_pyfunc(connect.get(self.key))

    def set(self, value):
        """ 设置变量数值

        Args:
           value: 要设置的数值

        Returns:
           是否设置成功
        """

        connect = self.env.storage.connects.get(self)
        seted = connect.set(self.key, value)

        if seted:
            self.value = value

        return seted

    def incr(self, value):
        """ 增量修改数值

        Args:
            value: 增量数值

        Returns:
            增量修改后的数值
        """

        connect = self.env.storage.connects.get(self)
        return self.to_pyfunc(connect.incrby(self.key, value))

    def set_if_none(self, value):
        """ 当key为空时才设置数值

        Args:
            value: 要设置的数值

        Returns:
            是否设置成功
        """
        
        connect = self.env.storage.connects.get(self)
        seted = connect.setnx(value)

        if seted:
            self.value = value

        return seted

class RedisHash(dict, RedisItemMixIn):
    """ 对Redis Hash类型操作的封装

    透明Hash的处理细节，方便业务层快速处理调用

    Attributes:
       env: 运行环境
       use_db: 使用settings所对应的db
       shared_key: 散列数值
    """

    def __init__(self, db_name):
        """ 初始化
        
        Model层的初始化

        Args:
           db_name: 对应settings里的db配置
        """

        self.env = None
        self.use_db = db_name
        self.shared_key = None

    def init(self, env, attr_name, carrier):
        """ 初始化操作

        当要加载数据时，会根据名称和model初始化内容

        Args:
            env: 运行环境
            attr_name: 名称
            carrier: 载体Model
        """

        self.key = env.generate_store_key(carrier, attr_name)
        self.env = env

    def length(self):
        """ 获取当前数据的总长度

        Returns:
            数据在Redis的长度
        """

        connect = self.env.storage.connects.get(self)
        return connect.hlen(self.key)

    def all(self):
        """ 加载全部Redis里的数据
        
        一次性加载全部Redis的数据
        """

        connect = self.env.storage.connects.get(self)
        self.update(connect.hgetall(self.key))

    def incr(self, key, value):
        """ 对Hash里的一个key进行增量的操作

        Args:
           key: Hash里的一个key
           value: 增量数值
        """

        connect = self.env.storage.connects.get(self)
        self.__setitem___(key,  self.to_pyfunc(
            connect.hincrbyfloat(self.key, key, value)))

    def pick_out(self, *keys):
        """ 挑选指定的key加载

        Args:
            keys: 要加载的key列表
        """

        connect = self.env.storage.connects.get(self)
        self.update(connect.hmget(self.key, keys))

    def mset(self, **kwargs):
        """ 设置多个key的数值

        Args:
           kwargs: 要设置的字典
        """

        connect = self.env.storage.connects.get(self)

        if connect.hmset(self.key, kwargs):
            self.update(kwargs)

    def set(self, key, value):
        """ 设置单个key的数据

        Args:
           key: Hash里对应的一个key
           value: 要设置的数值
        """

        connect = self.env.storage.connects.get(self)
        connect.hset(self.key, key, value)
        self.__setitem___(key, value)

    def set_if_none(self, key, value):
        """ 当key为空时设置单个key的数据

        Args:
           key: Hash里对应的一个key
           value: 要设置的数值

        Returns:
           是否设置成功
        """

        connect = self.env.storage.connects.get(self)

        if connect.hsetnx(self.key, key, value):
            self.__setitem___(key, value)
            return True
        
        return False

    def save(self, keys=None):
        """ 保存现有数据

        当对自身对象产生操作时候时，需要同步到Redis服务器

        Args:
           keys: 指定要保存的key列表， 当为空时默认为全局保存

        Returns:
           是否保存成功
        """

        kwargs = None

        if keys:
            kwargs = {}
            for key in keys:
                kwargs[key] = self.__getitem__(key)
        else:
            kwargs = self.iteritems()

        connect = self.env.storage.connects.get(self)

        return connect.hmset(self.key, kwargs)

class RedisSortedSetHM(RedisItemMixIn):
    def __init__(self, db_name):
        self.use_db = db_name
        self.key = None
        self.env = None
        self.changed = False

    def init(self, env, attr_name, carrier):
        self.key = env.generate_store_key(carrier, attr_name)
        self.env = env

    def zadd(self, key, score):
        """
        """
        connect = self.env.storage.connects.get(self)
        connect.zadd(self.key, key, score)

    def zcard(self):
        """
        """
        connect = self.env.storage.connects.get(self)

        return connect.zcard(self.key)

    def evalsha(self, script_sha, argc, *args):
        """
        """

        connect = self.env.storage.connects.get(self)

        return connect.evalsha(script_sha, argc, *args)

class RedisSortedSet(RedisItemMixIn):
    def __init__(self, db_name):
        self.score = 0
        self.rank = 0
        self.key = None
        self.pk = None
        self.use_db = db_name
        self.changed = False
        self.env = None
        self.shared_key = None

    def init(self, env, attr_name, carrier):
        """ 排名数据初始化

        从Redis里取排名数据
        
        Args:
           env: 运行环境
           attr_name: 所处于model的名字
           carrier: model对象
        """

        self.pk = carrier.pk
        self.key = env.generate_store_key(carrier, attr_name)
        self.env = env

        connect = env.storage.connects.get(self)
        pipe = connect.pipeline(transaction=False)
        pipe.zrevrank(self.key, self.pk)
        pipe.zscore(self.key, self.pk)

        self.rank, self.score = pipe.execute()
        
        if not self.rank is None:
            self.rank += 1

    def reset(self):
        """
        """

        connect = self.env.storage.connects.get(self)
        connect.zrem(self.key, self.pk)

    def zcard(self):
        """ 获取当前key里所有的人数

        Returns:
            总人数
        """

        connect = self.env.storage.connects.get(self)

        return connect.zcard(self.key)

    def snapshot_to(self, snapshot_key):
        """ 将redis数据快照到另一个key上

        Args:
           要快照的key
        """

        connect = self.env.storage.connects.get(self)
        connect.zunionstore(snapshot_key, {self.key: 1}, aggregate=None)

    def incr(self, value):
        """ 将自身积分增量

        Args: 
           value: 增量数值
        """

        connect = self.env.storage.connects.get(self)
        pipe = connect.pipeline(transaction=False)
        pipe.zincrby(self.key, self.pk, value)
        pipe.zrevrank(self.key, self.pk)

        self.score, self.rank = pipe.execute()

        if not self.rank is None:
            self.rank += 1

    def zadd(self, value):
        """ 更改自身的积分数值

        Args:
           value: 积分数值
        """

        connect = self.env.storage.connects.get(self)
        pipe = connect.pipeline(transaction=False)
        pipe.zadd(self.key, self.pk, value)
        pipe.zrevrank(self.key, self.pk)
        pipe.zscore(self.key, self.pk)

        _zadd, self.rank, self.score = pipe.execute()

        if not self.rank is None:
            self.rank += 1

    def zrevrange(self, min_rank, max_rank, with_score=False):
        """ 查找从指定名次到指定名次间的所有排名

        Args:
            min_rank: 最小排名
            max_rank: 最大排名
            with_score: 是否返回积分

        Returns:
            符合条件的列表
        """

        connect = self.env.storage.connects.get(self)

        return connect.zrevrange(self.key, min_rank - 1, max_rank - 1, with_score)

    def pick_out(self, ranks, with_score=False):
        """ 挑选排名用户的数据

        会尽量优化查询次数，当排名有连续的情况时，会使用一次命令
        所以当追求性能时，需要传入排序过的列表

        Args:
            ranks: 要挑选的排名列表
            with_score: 是否返回积分

        Returns:
            以排名为key的字典
        """

        outs = {}
        all_ranks = []

        prev = ranks.pop(0)
        prev -= 1
        groups = [[prev, prev]]

        for value in ranks:
            rank = value - 1

            if rank - prev == 1:
                groups[-1][1] = rank
            else:
                start, end = groups[-1]
                all_ranks.append(xrange(start + 1, end + 2))
                groups.append([rank, rank])

            prev = rank

        start, end = groups[-1]
        all_ranks.append(xrange(start + 1, end + 2))

        connect = self.env.storage.connects.get(self)
        pipe = connect.pipeline(transaction=False)
        
        for min_rank, max_rank in groups:
            pipe.zrevrange(self.key, min_rank, max_rank, with_score)

        data = pipe.execute()

        return dict(itertools.izip(itertools.chain(*all_ranks), 
                                   itertools.chain(*data)))

    def nearby_pos(self, ahead, behind, with_score=False):
        """ 查找自身的前后多少名数据

        Args:
           ahead: 向前多少名
           behind: 向后多少名
           with_score: 是否返回积分

        Returns:
           符合条件的id列表
        """

        min_rank = self.rank - ahead
        max_rank = self.rank + behind

        connect = self.env.storage.connects.get(self)

        return connect.zrevrange(self.key, min_rank, max_rank, with_score)

    def nearby_score(self, ahead, behind, num=None, with_score=False):
        """ 查找自身的前后多少积分数据

        Args:
           ahead: 向前多少分
           behind: 向后多少分
           num: 数量控制
           with_score: 是否返回积分

        Returns:
           符合条件的id列表
        """

        min_score = self.score - ahead
        max_score = self.score + behind

        connect = self.env.storage.connects.get(self)

        return connect.zrevrangebyscore(self.key, max_score, min_score,
                                        num=num, withscores=with_score)
