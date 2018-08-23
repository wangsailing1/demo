#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time

import settings
from lib.db import ModelTools, ModelBase
from lib.utils import rand_string
from lib.core.environ import ModelManager
from gconfig import game_config

STR_SOURCE = '0123456789'


class ServerUid(ModelTools):
    """ 服中对应的用户uid
    sorted set

    """
    SERVER_NAME = 'master'

    ONLINE_USERS_TIME_RANGE = 5 * 60            # 判断用户在线的时间参考

    def __init__(self, server):
        super(ServerUid, self).__init__()
        self.server = server
        self._key = self.make_key(self.server, server_name=self.SERVER_NAME)
        self._redis = self.get_redis_client(self.SERVER_NAME)

    def owned_count(self):
        """ 获取服务器拥有的人数

        :return:
        """
        return self._redis.zcard(self._key)

    def uid_exist(self, uid):
        """ 用户是否存在

        :param uid:
        :return:
        """
        return self._redis.zscore(self._key, uid) is not None

    def add_uid(self, uid):
        """ 增加用户

        :param uid:
        :return:
        """
        return self._redis.zadd(self._key, uid, int(time.time()))

    def del_uid(self, uid):
        """ 删除用户

        :param uid:
        :return:
        """
        return self._redis.zrem(self._key, uid)

    def get_online_user_count(self):
        """
        获得在线用户总数
        """
        ts = int(time.time())
        return self._redis.zcount(self._key, ts - self.ONLINE_USERS_TIME_RANGE, ts)

    def get_all_uid(self):
        """ 获取所有uid

        :return:
        """
        for i in self._redis.zscan_iter(self._key):
            yield i[0]


class ServerUidList(object):
    """ 服对应用户列表

    """
    def __init__(self):
        pass

    @classmethod
    def all_server(self):
        """ 所有的server

        :return:
        """
        for server_name in settings.SERVERS.iterkeys():
            if server_name in ['master', 'public']:
                continue
            yield server_name

    @classmethod
    def get_server_info(cls):
        """ 获取服务器信息

        :return:
        """
        info = []
        for server_name in cls.all_server():
            server_uid = ServerUid(server_name)
            info.append((server_name, server_uid.owned_count()))

        info_sorted = sorted(info, key=lambda x: x[1])

        return info_sorted

    def get_idle_server(self):
        """ 获取相对空闲的服

        :return:
        """
        info = self.get_server_info()
        if not info:
            return None

        return info[0][0]

    def create_uid(self, server):
        """ 创建一个uid

        :return:
        """
        server_uid = ServerUid(server)
        uid = self.generate_uid(server)

        while server_uid.uid_exist(uid):
            uid = self.generate_uid(server)

        server_uid.add_uid(uid)

        return uid

    def generate_uid(self, server):
        """ 生成一个uid
        :param server:
        :return:
        """
        uid = '%s%s' % (server, rand_string(7, STR_SOURCE))
        return uid


class ServerConfig(ModelBase):
    """
    关于分服的设置,开关,名字等
    """
    SERVER_NAME = 'master'

    def __init__(self, uid=''):
        self.uid = 'server_config'
        self._attrs = {
            'config_value': {},
            'start_time': 0,
            'is_open': 0,
        }
        super(ServerConfig, self).__init__(self.uid)

    @classmethod
    def get(cls, uid='', server_name='', **kwargs):
        uid = 'server_config'
        server_name = cls.SERVER_NAME
        o = super(ServerConfig, cls).get(uid, server_name=server_name, **kwargs)
        for k in settings.SERVERS:
            if k not in o.config_value:
                o.config_value[k] = {
                    'name': u'' if k not in ['master', 'public'] else k,
                    'is_open': False if k not in ['master', 'public'] else True,
                    'is_open_for_test': True,
                    'sort_id': 0,   # 排序权重
                    'flag': 0,      # 0, 1, 2: 维护，新服流畅绿，老服爆满红
                    'open_time': -1,
                }
        return o

    def modify_start_time(self, t, save=True):
        """ 修改开始时间

        :param t:
        :param save:
        :return:
        """
        self.start_time = t
        if save:
            self.save()

    def server_list(self, need_filter=True, ignore_master_public=True, tpid=None):
        """
        获取服务器所有信息
        :param need_filter: 是否过滤
        :param account:
        :return:
        """
        # l = []
        # for k, v in settings.SERVERS.iteritems():
        #     if k in ['master', 'public'] and need_filter:
        #         continue
        #     v['server'] = k
        #     l.append(v)
        #
        # l.sort(key=lambda x: (x['server'], x['net_name']))
        # return l
        l = []
        account_pt = None
        if tpid is not None:
            account_pt = tpid
        for k, v in self.config_value.iteritems():
            if k in ['master', 'public'] and need_filter and ignore_master_public:
                continue
            if (v['is_open'] and v['name']) or not need_filter:
                if k not in settings.SERVERS:
                    continue

                include_pt = v.get('include_pt', [])
                exclude_pt = v.get('exclude_pt', [])
                # elites_account = v.get('elites_account', [])
                if account_pt is not None:
                    if include_pt and account_pt not in include_pt:
                        continue
                    if exclude_pt and account_pt in exclude_pt:
                        continue
                    # if elites_account and account not in elites_account:
                    #     continue

                se = settings.SERVERS[k]
                long_ip, long_port = se.get('long_addr', (None, None))
                # 有配置读配置，否则读settings里的的默认配置
                default_cpp_addr = se.get('cpp_addr', {})
                cpp_addr_config = game_config.slg_server_addr.get(k, default_cpp_addr)
                info = {
                    'server': k,
                    'sort_id': v.get('sort_id', 0),
                    'flag': v.get('flag', 0),
                    'open_time': v.get('open_time', -1),
                    'uid': '',
                    'master_url': settings.SERVERS['master']['server'],
                    'server_name': v['name'],
                    'is_open': v['is_open'],
                    'is_open_for_test': v['is_open_for_test'],
                    'domain': se['server'],
                    'chat_ip': se.get('chat_ip', ''),
                    'chat_port': se.get('chat_port', ''),
                    'config_type': se.get('config_type', 1),
                    'long_ip': long_ip,
                    'long_port': long_port,
                    'cpp_addr': cpp_addr_config,
                    'is_inreview': se.get('is_inreview', False),
                }
                if not need_filter:
                    info.update(include_pt=include_pt, exclude_pt=exclude_pt)   # , elites_account=elites_account)
                l.append(info)
        l.sort(key=lambda x: (x['server'] not in ['master', 'public'], -x['sort_id'], x['server']))
        return l

    def get_server(self, server_name):
        """
        获取单服配置
        :param server_name:
        :return:
        """
        config = self.config_value.get(server_name)
        return config

    # 用yield方法取分服
    def yield_open_servers(self):
        """
        返回已经开启的分服数据
        """
        for server_id, server_data in self.config_value.iteritems():
            if server_id not in settings.SERVERS or server_id in ['master', 'public']:
                continue
            if server_data['is_open']:
                yield server_id, server_data

    @classmethod
    def get_redis_userd_memory(self, server_name):
        """
        获取redis使用信息
        :param server_name:
        :return:
        """
        redis = self.get_redis_client(server_name)
        info = redis.info()
        config = redis.config_get()
        bind = config['bind'].split(' ')[0]
        port = config['port']
        used_memory_rss = info.get('used_memory_rss', 0)
        used_memory = info.get('used_memory', 0)
        mem_fragmentation_ratio = info.get('mem_fragmentation_ratio')
        return '%s/%s/%sG/%s/%s' % (info.get('used_memory_human'),
                                 info.get('used_memory_peak_human'),
                                 '%0.2f' % (used_memory_rss / 1024.0 ** 3),
                                 mem_fragmentation_ratio,
                                 info.get('connected_clients')), {bind: {port: {'rss': used_memory_rss,
                                                                                'used': used_memory, 'mem_fragmentation_ratio': mem_fragmentation_ratio}}}, used_memory

# 记录服务器配置
all_server_config = {}


def reload_server_config():
    """ 加载服配置, 请根据需要增加字段, 现在支持name

    """
    global all_server_config

    sc = ServerConfig.get()
    for server, value in sc.config_value.iteritems():
        if server not in settings.SERVERS:
            continue
        all_server_config[server] = {'name': value['name'], 'is_open': value['is_open'],
                                     'open_time': value.get('open_time', 0)}


reload_server_config()


def get_server_config(server):
    server = settings.get_father_server(server)
    config = all_server_config.get(server, {})
    if not config.get('is_open'):
        reload_server_config()
        config = all_server_config.get(server, {})
    if not config:
        reload_server_config()
        config = all_server_config.get(server, {})
    return config


ModelManager.register_model('server_config', ServerConfig)
