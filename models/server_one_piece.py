# -*- coding: utf-8 -*-

__author__ = 'ljm'

import datetime    # 统计key代码需要用到
import time
import settings

from gconfig import game_config
from lib.db import ModelBase
from lib.core.environ import ModelManager

from lib.utils import generate_rank_score, round_float_or_str
from lib.utils.time_tools import timestamp_from_relative_time
from lib.utils.time_tools import relative_activity_remain_time
from lib.utils.debug import print_log


class ServerOnePiece(ModelBase):
    """ 藏宝图
    """
    ONE_PIECE_RANK_KEY_PREFIX = 'server_one_piece_score_'
    ONE_PIECE_PRO_KEY_PREFIX = 'server_one_piece_pro_'
    ONE_PIECE_GLOBAL_KEY_PREFIX = 'server_one_piece_global_'

    TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

    DURATION_TIME = 60 * 60 * 24 * 3        # 秒
    MAX_FREE_ONE_PIECE_TIMES = 3
    KEY_ID = 203

    SERVER_INREVIEW_ID = 912

    def __init__(self, uid=None):
        self.uid = uid
        self.rank_key = None
        self.pro_key = None
        self.global_key = None
        self._attrs = {
            'version': 0,                   # 版本号
            'score': {},                     # 积分, {1; 100, 2: 200, 3: 300, 4: 400}
            'times': 0,                     # 次数
            'open_times': 0,                # 开启次数
            'goods': {},                    # 兑换物品
            'step_reward': [],              # 阶段奖励领取数据
        }
        self.open_switch = False
        self.remainder_time = 0
        self.start_time = None
        super(ServerOnePiece, self).__init__(self.uid)

    @classmethod
    def get(cls, uid, server_name='', need_init=True):
        o = super(ServerOnePiece, cls).get(uid, server_name=server_name, need_init=need_init)
        setattr(o, "fredis", o.get_father_redis())
        o.rank_db = o.fredis
        o.check_version()
        return o

    def check_version(self):
        """ 检查版本如果更新需要更新数据

        :return:
        """
        version, remainder_time = self.get_cur_version()

        # 活动没有开启不刷新
        if not version:
            return
        self.open_switch = True
        self.remainder_time = remainder_time
        if self.version != version:
            self.version = version
            self.times = 0
            self.open_times = 0
            self.step_reward = []
            for k, v in game_config.server_one_piece_exchange.iteritems():
                if v.get('version') == version and v['sort'] != 1 and k in self.goods:
                    del self.goods[k]
            self.save()

    def get_cur_version(self):
        """ 获取当前的版本

        :return 0: 表示没有开启
        """
        server_inreview_config = game_config.server_inreview.get(self.SERVER_INREVIEW_ID)
        if not server_inreview_config:
            return 0, 0
        config_time = server_inreview_config.get('name')
        if not config_time:
            return 0, 0
        config_time = config_time.split(',')
        now = time.time()
        for i, config in enumerate(config_time):
            start_time, end_time = config.split('-')
            remain_time = relative_activity_remain_time(self.get_server_open_time(), start_time, end_time, now=now)
            if remain_time:
                self.start_time = timestamp_from_relative_time(self.get_server_open_time(), start_time)
                return i + 1, remain_time

        return 0, 0

    def get_server_open_time(self):
        return game_config.get_server_config(self._server_name).get('open_time', 0)

    def is_open(self):
        """ 是否开启, 时间统一判断, 返回剩余时间
        """
        if self.open_switch:
            return self.remainder_time
        else:
            return 0

    def get_remain_free_times(self):
        """ 获取剩余免费次数

        :return:
        """
        return self.MAX_FREE_ONE_PIECE_TIMES - self.open_times
    #
    ######################################本服积分排行榜######################################################
    def get_rank_key(self, server_name=None, version=None):
        if self.rank_key is None:
            version = version if version else self.version
            server_name = server_name if server_name else self._server_name
            server_name = settings.get_father_server(server_name)
            prefix = '%s%s' % (self.ONE_PIECE_RANK_KEY_PREFIX, version)
            self.rank_key = self.make_key_cls(prefix, server_name)
        return self.rank_key

    def get_rank(self):
        """ 获取自己排名

        :return:
        """
        rank_key = self.get_rank_key()
        rank = self.rank_db.zrevrank(rank_key, self.uid)
        if rank is None:
            rank = -1
        return rank + 1

    def get_score_ranks(self, start=1, end=50):
        """ 获取前N名 start=1, end=50 为1到50名

        :param start:
        :param end:
        :return:
        """
        rank_key = self.get_rank_key()
        return self.rank_db.zrevrange(rank_key, start - 1, end - 1, withscores=True, score_cast_func=round_float_or_str)

    def update_key(self, score, save=True):
        """ 更新钥匙
        """
        self.times += score
        rank_key = self.get_rank_key()
        self.rank_db.zadd(rank_key, **{self.uid: generate_rank_score(self.times)})

        # 统计用key
        date = str(datetime.date.today())
        server_name = self._server_name
        prefix = self.ONE_PIECE_RANK_KEY_PREFIX
        new_rank_key = self.make_key_cls(prefix, server_name)
        stats_key = new_rank_key + '_stats_' + date

        self.rank_db.zadd(stats_key, **{self.uid: self.times})

        if save:
            self.save()
    ######################################本服积分排行榜######################################################

    ######################################本服伪概率排行榜######################################################
    def get_pro_key(self, server_name=None, version=None):
        if self.pro_key is None:
            version = version if version else self.version
            server_name = server_name if server_name else self._server_name
            server_name = settings.get_father_server(server_name)
            prefix = '%s%s' % (self.ONE_PIECE_PRO_KEY_PREFIX, version)
            self.pro_key = self.make_key_cls(prefix, server_name)
        return self.pro_key

    def get_pro_data(self):
        """ 获取数据

        :param start:
        :param end:
        :return:
        """
        pro_key = self.get_pro_key()
        data = self.rank_db.hgetall(pro_key)
        return data if data else {}

    def incrby_pro(self, score):
        """ 更新积分
        """
        pro_key = self.get_pro_key()
        self.rank_db.hincrby(pro_key, 'score', score)

    def update_status(self, status):
        pro_key = self.get_pro_key()
        self.rank_db.hset(pro_key, 'status', status)
    ######################################本服伪概率排行榜######################################################

    ######################################本服物品######################################################
    def get_global_key(self, server_name=None, version=None):
        if self.global_key is None:
            version = version if version else self.version
            server_name = server_name if server_name else self._server_name
            server_name = settings.get_father_server(server_name)
            prefix = '%s%s' % (self.ONE_PIECE_GLOBAL_KEY_PREFIX, version)
            self.global_key = self.make_key_cls(prefix, server_name)
        return self.global_key

    def get_all_global_data(self):
        """ 获取数据

        :param start:
        :param end:
        :return:
        """
        global_key = self.get_global_key()
        data = self.rank_db.hgetall(global_key)
        return data if data else {}

    def get_global_data(self, goods_id):
        """ 获取数据

        :param start:
        :param end:
        :return:
        """
        global_key = self.get_global_key()
        num = self.rank_db.hget(global_key, goods_id)
        return int(num) if num else 0

    def incrby_global(self, goods_id, num=1):
        """ 更新兑换物品数量
        """
        global_key = self.get_global_key()
        self.rank_db.hincrby(global_key, goods_id, num)
    ######################################本服物品######################################################
