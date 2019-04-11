# /usr/bin/python
# encoding: utf-8

import time
from lib.db import ModelBase
from lib.db import get_redis_client
import settings
from lib.utils.active_inreview_tools import get_inreview_version
from lib.core.environ import ModelManager

def get_global_redis():
    return get_redis_client(settings.SERVERS['public']['redis'])


class ServerEgg(ModelBase):
    ACTIVE_ID = 2018
    # TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

    def __init__(self, uid=None):
        self.uid = uid
        self.g_redis = get_global_redis()
        self._attrs = {
            'egg_diamond_times': 0,
            'egg_item_times': 0,
            'egg_item_super_times': 0,
            'version': 0,
            'payment': 0,
            'egg_item_used_times': 0,
            # 'egg_item_open_times': 0,
            'egg_item_reward_list': [],
            'egg_item_reward_best': [],
            'egg_diamond_reward_list': [],
            'egg_diamond_reward_best': [],
            'egg_sort_used': {1: 0, 2: 0}

        }

        super(ServerEgg, self).__init__(self.uid)

    def get_version(self):
        # 新服砸金蛋 active_type 为 2018
        version, new_server, start_time, end_time = get_inreview_version(self.mm.user, self.ACTIVE_ID)
        return version

    def pre_use(self):
        if self.version != self.get_version():
            self.refresh_egg()
            self.save()

    def refresh_egg(self):
        self.egg_diamond_times = 0
        self.egg_item_times = 0
        self.egg_item_super_times = 0
        self.version = self.get_version()
        self.payment = 0
        # self.egg_item_open_times = 0
        self.egg_item_used_times = 0
        self.egg_item_reward_list = []
        self.egg_item_reward_best = []
        self.egg_diamond_reward_list = []
        self.egg_diamond_reward_best = []
        self.egg_sort_used = {1: 0, 2: 0}

    def get_key(self):
        return 'egg_best_reward_log_%s' % self.version

    def add_log(self, data):
        key = self.get_key()
        self.g_redis.lpush(key, data)
        self.g_redis.ltrim(key, 0, 50)
        self.g_redis.expire(key, 3600 * 24 * 3)

    def get_log(self):
        key = self.get_key()
        data = self.g_redis.lrange(key, 0, -1)
        return data

ModelManager.register_model('serveregg', ServerEgg)