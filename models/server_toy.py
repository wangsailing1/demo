#! --*-- coding: utf-8 --*--


import time
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import generate_rank_score, round_float_or_str, weight_choice
import settings
from lib.utils.active_inreview_tools import get_inreview_version
from models import server as serverM
from lib.utils.time_tools import strftimestamp, timestamp_from_relative_time


class ServerToy(ModelBase):
    ACTIVE_ID = 2021

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'toy_list': {},  # 奖池
            'version': 0,  # 版本号
            'toy_num': 0,  # 本次抓取次数
            'all_toy_num': 0,  # 总抓取次数
            'got_reward': [],  # 获得的娃娃
            'catch_num_current': 0,  # 本次抓住次数
            'last_refresh_time': 0,  # 刷新时间
            'catch_num': 0,  # 排行用
            'rank_reward': [],  # 排行奖励
        }
        super(ServerToy, self).__init__(self.uid)
        server = self.get_server_name(self.uid)
        father_server = settings.get_father_server(server)
        self.fredis = self.get_father_redis(father_server)

    def pre_use(self):
        version = self.get_version()
        save = False
        now = int(time.time())
        if version and version != self.version:
            self.version = version
            self.init_reward()
            self.toy_num = 0
            self.all_toy_num = 0
            self.catch_num = 0
            self.got_reward = []
            self.rank_reward = []
            self.catch_num_current = 0
            self.last_refresh_time = now
            save = True
        if save:
            self.save()

    def get_key(self, version=0):
        if not version:
            version = self.version
        server = self.get_server_name(self.uid)
        father_server = settings.get_father_server(server)
        self._key = self.make_key(self.__class__.__name__, server_name=father_server)
        self._key = '%s%s' % (self._key, version)
        return self._key

    def get_start_time_end_time(self):
        server_open_time = serverM.get_server_config(self._server_name).get('open_time')
        config = game_config.server_inreview.get(self.ACTIVE_ID, {})
        name = config.get('name_show', '')
        if not name:
            return '', ''
        name = name.split(',')[self.version - 1]
        name = name.split('-')
        start_time = name[0]
        end_time = name[1]
        start_time = strftimestamp(timestamp_from_relative_time(server_open_time, start_time))
        end_time = strftimestamp(timestamp_from_relative_time(server_open_time, end_time))
        return start_time, end_time

    def get_version(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_ID)
        return version

    def is_free_refresh(self):
        return int(time.time()) >= self.last_refresh_time + self.get_refresh_time()

    def remain_refresh_time(self):
        remain_time = self.last_refresh_time + self.get_refresh_time() - int(time.time())
        return max(remain_time, 0)

    def get_refresh_time(self):
        config = game_config.server_rmb_gacha_control[self.version]
        return config['cd'] * 60

    def init_reward(self, save=False):
        """
        :param save: 
        :return: 
        """
        config = game_config.server_rmb_gacha_control[self.version]
        reward_list_id = game_config.server_inreview[self.ACTIVE_ID]['param1'][self.version - 1]
        toy_reward_weight = game_config.server_toy_rmb_reward_weight_mapping()[reward_list_id]
        num = 1
        for group_id, group_num in config['group_num']:
            for _ in range(group_num):
                weight_config = toy_reward_weight[group_id]
                reward_id = weight_choice(weight_config)[0]
                self.toy_list[num] = {'reward_id': reward_id, 'num': 0, 'flag': 0}
                num += 1
        if save:
            self.save()

    def refresh_reward(self, save=False):
        self.init_reward()
        self.toy_num = 0
        self.catch_num_current = 0
        self.got_reward = []
        if save:
            self.save()

    def add_rank(self, uid, score):
        _key = self.get_key()
        self.fredis.zadd(_key, uid, generate_rank_score(score))

    def get_all_user(self, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str, r_key=''):
        if not r_key:
            r_key = self.get_key()
        return self.fredis.zrevrange(r_key, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_score(self, uid, score_cast_func=round_float_or_str):
        _key = self.get_key()
        score = self.fredis.zscore(_key, uid) or 0
        score = score_cast_func(score)
        return score

    def get_rank(self, uid):
        _key = self.get_key()
        rank = self.fredis.zrevrank(_key, uid)
        if rank is None:
            rank = -1
        return rank + 1


class ServerFreeToy(ServerToy):
    ACTIVE_ID = 2022

    def __int__(self, uid):
        super(ServerToy, self).__init__(self.uid)

    def get_version(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_ID)
        return version

    def get_refresh_time(self):
        config = game_config.server_free_gacha_control[self.version]
        return config['cd'] * 60

    def init_reward(self, save=False):
        """
        :param save: 
        :return: 
        """
        config = game_config.server_free_gacha_control[self.version]
        reward_list_id = game_config.server_inreview[self.ACTIVE_ID]['param1'][self.version - 1]
        toy_reward_weight = game_config.server_toy_rmb_reward_weight_mapping()[reward_list_id]
        num = 1
        for group_id, group_num in config['group_num']:
            for _ in range(group_num):
                weight_config = toy_reward_weight[group_id]
                reward_id = weight_choice(weight_config)[0]
                self.toy_list[num] = {'reward_id': reward_id, 'num': 0, 'flag': 0}
                num += 1
        if save:
            self.save()


ModelManager.register_model('servertoy', ServerToy)
ModelManager.register_model('serverfreetoy', ServerFreeToy)
