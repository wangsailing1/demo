#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

import time
from gconfig import game_config
import random
# from logics.notice import add_notice_all_server
from return_msg_config import i18n_msg
from math import ceil
from lib.db import ModelBase, ModelTools
from lib.core.environ import ModelManager
from lib.utils import generate_rank_score
from lib.utils.debug import print_log
from lib.utils.active_inreview_tools import get_version_by_active_id
from chat.to_server import send_to_all


class SuperPlayer(ModelBase):

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    FREE_TIME = 1
    ADD_CAN_RECEIVED_TIME = 10
    SPEND_SEND_NEED = 5000
    PAY_SEND_NEED = 300
    ACTIVE_ID = 2010

    def __init__(self, uid=None):
        """
        """
        self.uid = uid
        self._attrs = {
            'version': 0,            # 版本号
            'shop_id': 0,            # 商店id
            'shop_buy_times': {1: 0, 2: 0, 3: 0},    # 购买商品次数  {id: times,}
            'day_pay': 0,            # 当日充值
            'day_pay_send': 0,       # 当日充值发红包次数
            'day_spend': 0,          # 当日消费
            'day_spend_send': 0,     # 当日消费发红包次数
            'day_send_bag': 0,       # 当日发红包数
            'receive_bag_times': 0,  # 领红包次数
            'can_receive_times': 0,  # 可领次数
            'reward_step': {1: 0, 2: 0, 3: 0},   # 领取成就
            'get_time': 0,           # 下一次可获取红包时间戳
            'refreshplayer': 1,      # 刷新自己数据
            'a_id':0,                # active表里的id
        }
        super(SuperPlayer, self).__init__(self.uid)

    @classmethod
    def get(cls, uid, server_name='', **kwargs):
        o = super(SuperPlayer, cls).get(uid, server_name=server_name, **kwargs)
        o.check_version()
        return o

    def check_version(self):
        """ 检查版本如果更新需要更新数据

        :return:
        """
        a_id, version = get_version_by_active_id(active_id=self.ACTIVE_ID)
        if version and self.version < version:
            self.version = version
            self.a_id = a_id
            self.all_clear()

    def all_clear(self):
        self.shop_id = 0
        self.shop_buy_times = {1: 0, 2: 0, 3: 0}
        self.day_pay = 0
        self.day_pay_send = 0
        self.day_spend = 0
        self.day_spend_send = 0
        self.day_send_bag = 0
        self.receive_bag_times = 0
        self.can_receive_times = 0
        self.reward_step = {1: 0, 2: 0, 3: 0}
        self.refreshplayer = 1
        self.save()

    def clear(self):
        self.shop_buy_times = {1: 0, 2: 0, 3: 0}
        self.save()

    def add_day_spend(self, coin_num):
        if self.version:
            super_player_config = game_config.player.get(self.version)
            if super_player_config:
                FORMAT = '%Y-%m-%d %H:%M:%S'
                start_time = super_player_config['start_time']
                end_time = super_player_config['end_time']
                if start_time and end_time:
                    now_str = time.strftime(FORMAT)
                    if start_time <= now_str <= end_time:
                        self.day_spend += coin_num
                        self.send_bag(tp='spend')

    def send_bag(self, tp='spend'):
        can_send_times = 0
        if tp == 'spend' and self.day_spend:
            can_send_times = int(self.day_spend/self.SPEND_SEND_NEED - self.day_spend_send)
        elif tp == 'pay' and self.day_pay:
            can_send_times = int(self.day_pay/self.PAY_SEND_NEED - self.day_pay_send)

        configs = game_config.play_redbag_mapping.get(self.version, {})
        if can_send_times and configs:
            id_list = configs.keys()
            send_rank = SuperPlayerRank(self.version)
            for i in range(can_send_times):
                id_ = random.choice(id_list)
                num_ = configs[id_]['quantity']
                min_ = configs[id_]['min']
                max_ = configs[id_]['max']
                total = configs[id_]['donate']
                list_ = random_red_bag(num_, min_, max_, total)
                print_log('num_, min_, max_, total',num_, min_, max_, total, 'list_', list_)
                if tp == 'spend':
                    self.day_spend_send += 1
                else:
                    self.day_pay_send += 1
                self.day_send_bag += 1
                redbag = RedBag(self.version)
                redbag.add_red_bag('%s_%s' % (self.uid, self.day_send_bag), list_)
            self.add_send_notice()
            send_rank.update_user_score(self.uid, can_send_times)

        self.save()

    def add_send_notice(self):
        server_name = self._server_name
        msg = i18n_msg[1208] % (server_name, self.mm.user.name)
        data_ = {
            'msg': msg,
            'notice_lv': 6,
        }
        send_to_all(data_, server_name)

    def add_day_pay(self, coin_num):
        if self.version:
            super_player_config = game_config.player.get(self.version)
            if super_player_config:
                FORMAT = '%Y-%m-%d %H:%M:%S'
                start_time = super_player_config['start_time']
                end_time = super_player_config['end_time']
                if start_time and end_time:
                    now_str = time.strftime(FORMAT)
                    if start_time <= now_str <= end_time:
                        self.day_pay += coin_num
                        self.send_bag(tp='pay')


class RedBag(ModelTools):
    SERVER_NAME = 'master'
    KEYS = 'super_player_red_bag'
    ALL_KEYS = 'all_red_bag'

    def __init__(self, version):
        """
        红包类
        """
        super(RedBag, self).__init__()
        self.version = version
        self.all_bag_key = None
        self.redis = self.get_redis_client(self.__class__.__name__, self.SERVER_NAME)

    # 获取全部红包code存储的key
    def get_all_bag_key(self):
        if self.all_bag_key:
            return self.all_bag_key
        self.all_bag_key = self.make_key('%s_%s' % (self.ALL_KEYS, self.version), server_name=self.SERVER_NAME)
        return self.all_bag_key

    def get_red_keys(self, red_bag_code):
        red_keys = self.make_key('%s_%s' % (self.KEYS, red_bag_code), self.SERVER_NAME)
        return red_keys

    # 添加红包
    def add_red_bag(self, red_bag_code, lst):
        all_keys = self.get_all_bag_key()
        print_log('all_keys', all_keys, 'red_bag_code',red_bag_code)
        self.redis.sadd(all_keys, red_bag_code)
        self.set_redbag(red_bag_code, lst)

    # 存储红包大小列表
    def set_redbag(self, red_bag_code, lst):
        red_keys = self.get_red_keys(red_bag_code)
        for num_ in lst:
            self.redis.rpush(red_keys, num_)

    # 获取所有的红包的code
    def get_all_red_code(self):
        all_keys = self.get_all_bag_key()
        all_code = self.redis.smembers(all_keys)
        return all_code

    # 获取num个红包
    def get_red_num_code(self, num=20):
        all_keys = self.get_all_bag_key()
        codes = self.redis.srandmember(all_keys, num)
        return codes

    # 通过code抽取一个红包
    def get_redbag(self, red_bag_code):
        red_keys = self.get_red_keys(red_bag_code)
        num = self.redis.rpop(red_keys)
        if not num:
            num = 0
        if not self.redis.llen(red_keys):
            self.redis.delete(red_keys)      # TODO 列表为空时不知道需不需要删除keys?
            all_keys = self.get_all_bag_key()
            self.redis.srem(all_keys, red_bag_code)
        return int(num)

    # 获取红包剩余个数
    def get_redbag_last(self, red_bag_code):
        red_keys = self.get_red_keys(red_bag_code)
        num = self.redis.llen(red_keys)
        return num


class SuperPlayerShop(ModelBase):
    SERVER_NAME = 'master'

    def __init__(self, version=None):
        """
        """
        self.version = version
        self._attrs = {
            'shop_goods': {},        # 商店物品1  {1:{type:1, num: 100}}
            'shop_id': 0,            # 商点id
            'shop_info': {},         # 商店详情
            'refresh_time': 0,       # 刷新时间
            'refresh_times': 0,      # 刷新次数
        }
        super(SuperPlayerShop, self).__init__(self.version)

    @classmethod
    def get(cls, version):
        o = super(SuperPlayerShop, cls).get('superplayershop%s' % version, server_name=cls.SERVER_NAME)
        o.version = version
        return o


class SuperPlayerRank(ModelTools):

    """
    超级大玩家发红包次数排行
    """
    SERVER_NAME = 'master'

    def __init__(self, version=None):
        self.version = version
        self.rank_key = None
        self.redis = self.get_redis_client(self.__class__.__name__, self.SERVER_NAME)

    # 获取排行榜的keys
    def get_rank_key(self):
        if self.rank_key is None:
            self.rank_key = self.make_key_cls('%s_%s' % ('superplayerrank', self.version), self.SERVER_NAME)
        return self.rank_key

    # 获取玩家排名榜积分
    def get_user_score(self, user):
        rank_key = self.get_rank_key()
        return self.redis.zscore(rank_key, user if isinstance(user, (str, unicode)) else user.uid) or 0

    # 更新积分排名
    def update_user_score(self, user_uid, score):
        rank_key = self.get_rank_key()
        score_ = self.redis.zscore(rank_key, user_uid) or 0
        self.redis.zadd(rank_key, **{'%s' % user_uid: generate_rank_score(score + int(ceil(score_)))})

    # 获取玩家排名
    def get_user_score_rank(self, user):
        rank_key = self.get_rank_key()
        rank = self.redis.zrevrank(rank_key, user.uid)
        rank = 0 if rank is None else rank + 1
        return rank

    # 获取积分排名前num名玩家
    def get_users_rank(self, num=10):
        uids = self.redis.zrevrange(self.get_rank_key(), 0, num - 1, withscores=1)
        return uids

    # 获取两个积分之间的人数
    def get_user_num(self, min_score, max_score):
        num = self.redis.zcount(self.get_rank_key(), min_score, max_score)
        return num

    # 获取两个排名之间的信息
    def get_rank_users(self, min_rank, max_rank):
        uids = self.redis.zrevrange(self.get_rank_key(), min_rank-1, max_rank-1, withscores=1)
        return uids

    # 清除排行榜
    def clear_rank(self):
        rank_key = self.get_rank_key()
        self.redis.delete(rank_key)


def random_red_bag(num, min_, max_, total=1000):
    min_ = min_
    max_ = max_
    random_list = []
    if num == 1:
        random_list.append(total)
    else:
        for i in range(1, num):
            safe_total = min(total - (num - i) * min_, max_)
            money = random.randint(min_, safe_total)
            random_list.append(money)
            total -= money
        random_list.append(total)
        random.shuffle(random_list)
    return random_list


ModelManager.register_model('superplayer', SuperPlayer)