#! --*-- coding: utf-8 --*--

__author__ = 'ljm'


import random
import time

from lib.core.environ import ModelManager
from gconfig import game_config
from math import ceil
from tools.gift import add_mult_gift
from lib.utils.active_inreview_tools import get_version_by_active_id, get_inreview_version
from models.super_player import SuperPlayerShop, SuperPlayerRank, RedBag
from lib.utils.time_tools import str2timestamp, strftimestamp, datetime_to_timestamp
import datetime
from return_msg_config import i18n_msg

class ServerSuperPlayer(object):

    def __init__(self, mm=None):
        super(ServerSuperPlayer, self).__init__()
        self.mm = mm
        self.user = self.mm.user
        self.serversuperplayer = self.mm.serversuperplayer
        self.superplayer_config = game_config.server_player.get(self.serversuperplayer.version, {})
        if self.superplayer_config:
            self.superplayer_config['start_time'] = self.mm.serversuperplayer.start_time
            self.superplayer_config['end_time'] = self.mm.serversuperplayer.end_time

    def is_enter(self):
        config = self.superplayer_config
        if not config:
            return 'error_superplayer'
        start_time = str2timestamp(config['start_time'])
        end_time = str2timestamp(config['end_time'])
        if not (start_time and end_time):
            return 'error_superplayer'
        now_str = int(time.time())
        if start_time <= now_str <= end_time:
            return 0
        return 'error_superplayer'

    # 刷新商店
    def refresh(self):
        shop_config = game_config.get_server_play_shop_mapping().get(self.serversuperplayer.version, {})
        if not shop_config:
            return -1
        superplayershop = SuperPlayerShop.get(self.serversuperplayer.version)
        for i in range(1, 4):
            shop_id_cong = shop_config.get(i, {})
            good_ids = shop_id_cong.keys()
            id_ = random.choice(good_ids)
            superplayershop.shop_goods[i] = shop_config[i][id_]
        superplayershop.refresh_times += 1
        start_time_ = self.superplayer_config['start_time']
        start_time = time.strptime(start_time_, '%Y-%m-%d %H:%M:%S')
        superplayershop.refresh_time =time.mktime(start_time)
        superplayershop.save()
        return 0

    def index(self):
        # 初始刷新商店
        superplayershop = SuperPlayerShop.get(self.serversuperplayer.version)
        if not superplayershop.refresh_times or not superplayershop.shop_goods:
            rc = self.refresh()
            superplayershop = SuperPlayerShop.get(self.serversuperplayer.version)
            self.serversuperplayer.clear()
            if rc:
                return 1, {}  # 没有配置, 活动未开启
        if self.serversuperplayer.refreshplayer < superplayershop.refresh_times:
            self.serversuperplayer.refreshplayer = superplayershop.refresh_times
            self.serversuperplayer.clear()
        data = {}
        data['version'] = self.serversuperplayer.version
        data['shop_goods'] = superplayershop.shop_goods
        data['shop_id'] = superplayershop.shop_id
        data['shop_buy_times'] = self.serversuperplayer.shop_buy_times
        super_rank = SuperPlayerRank(self.serversuperplayer.version)
        data['send_bag_times'] = int(ceil(super_rank.get_user_score(self.user)))
        data['reward_step'] = self.serversuperplayer.reward_step
        rank_notice = []
        rank_uids = super_rank.get_users_rank(3)
        if rank_uids:
            for keys, score_ in rank_uids:
                mm = ModelManager(keys)
                user = mm.user
                rank_notice.append({'uid': user.uid, 'server_name': user._server_name, 'score': int(ceil(score_)), 'name': user.name})
        data['rank_notice'] = rank_notice
        data['bag_info'] = self.get_red_bag(1)
        data['next_refresh_time'] = int(superplayershop.refresh_time + 1800 - int(time.time()))
        return 0, data

    def buy_goods(self, sort_id, good_id):
        superplayershop = SuperPlayerShop.get(self.serversuperplayer.version)
        shop_goods = superplayershop.shop_goods
        print shop_goods
        if good_id != shop_goods[sort_id]['id']:
            return 1, {}  # 该商品已售完
        if shop_goods[sort_id]['limit_num'] <= 0:
            return 2, {}  # 全服可购买次数不足
        if self.serversuperplayer.shop_buy_times[sort_id] >= shop_goods[sort_id]['player_limit']:
            return 3, {}  # 个人购买次数达到上限
        cost_ = abs(shop_goods[sort_id]['cost_coin'])
        if self.user.diamond < cost_:
            return 'error_diamond', {}  # 钻石不足
        self.user.deduct_diamond(cost_)
        self.serversuperplayer.can_receive_times += superplayershop.shop_goods[sort_id]['time']
        if superplayershop.shop_goods[sort_id]['limit_type'] == 1:
            superplayershop.shop_goods[sort_id]['limit_num'] -= 1
        if superplayershop.shop_goods[sort_id]['limit_num'] < 0:
            superplayershop.shop_goods[sort_id]['limit_num'] = 0
        self.serversuperplayer.shop_buy_times[sort_id] += 1
        gift = shop_goods[sort_id]['reward']
        reward = add_mult_gift(self.mm, gift)
        superplayershop.save()
        self.serversuperplayer.save()
        rc, data = self.index()
        data['reward'] = reward
        return 0, data

    def get_rank_info(self, num=10):
        super_rank = SuperPlayerRank(self.serversuperplayer.version)
        mytimes = int(ceil(super_rank.get_user_score(self.user)))
        myrank = super_rank.get_user_score_rank(self.user)
        rank_uids = super_rank.get_users_rank(num)
        rank_info = []
        if rank_uids:
            for keys, score_ in rank_uids:
                mm = ModelManager(keys)
                user = mm.user
                rank_info.append({'uid': user.uid, 'server_name': user._server_name, 'score': int(ceil(score_)), 'name': user.name})
        return 0, {'rank_info': rank_info, 'mytimes': mytimes, 'myrank': myrank}

    def get_reward(self, step, reward_id):
        if self.serversuperplayer.reward_step.get(step, 0):
            return -2, {}  # 该奖励已领取
        reward = []
        super_rank = SuperPlayerRank(self.serversuperplayer.version)
        mytimes = int(ceil(super_rank.get_user_score(self.user)))
        active_config = game_config.get_server_play_points_mapping().get(self.serversuperplayer.version, {})
        need_point = active_config.get(reward_id, {}).get('point', 0)
        print need_point,mytimes
        if need_point and mytimes >= need_point:
            gift = active_config.get(reward_id, {}).get('reward', [])
            if gift:
                reward = add_mult_gift(self.mm, gift)
                self.serversuperplayer.reward_step[step] = 1
                self.serversuperplayer.save()
        rc, data = self.index()
        data['reward'] = reward
        data['reward_step'] = self.serversuperplayer.reward_step
        data['mytimes'] = mytimes
        return 0, data

    def get_red_bag(self, num=10):
        redbags = RedBag(self.serversuperplayer.version)
        codes = redbags.get_red_num_code(num)
        redbag_info = []
        for code_ in codes:
            uid, sendtime_ = code_.split('_')
            mm = ModelManager(uid)
            server_name = mm.server
            num_ = redbags.get_redbag_last(code_)
            redbag_info.append({'red_code': code_, 'uid': uid, 'name': mm.user.name, 'server_name': server_name, 'num': num_})
        return redbag_info

    def grab_bag(self, red_code):
        if self.serversuperplayer.can_receive_times <= 0:
            return 1, {}
        new_time = time.time()
        if new_time < self.serversuperplayer.get_time:
            return 2, {}
        redbags = RedBag(self.serversuperplayer.version)
        num = redbags.get_redbag(red_code)
        if not num:
            return 3, {}
        reward = {}
        if num and num > 0:
            gift = [[2, 0, num]]
            reward = add_mult_gift(self.mm, gift)
            self.serversuperplayer.get_time = int(time.time()) + 10   # 记录下一次抢红包时间戳
            self.serversuperplayer.can_receive_times -= 1
            self.serversuperplayer.save()
        redbag_info = self.get_red_bag()
        return 0, {'reward': reward,
                   'redbag_info': redbag_info,
                   'grep_time': self.serversuperplayer.get_time,
                   'can_receive_times': self.serversuperplayer.can_receive_times,
                   }


def server_refresh(server):
    config_type = game_config.get_config_type(server)
    if config_type != 1:
        return
    uid = '%s1234567' % server
    mm = ModelManager(uid)

    version, new_server, s_time, e_time = get_inreview_version(mm.user, mm.serversuperplayer.ACTIVE_ID)
    if not version:
        version, new_server, s_time, e_time = get_inreview_version(mm.user, mm.serversuperplayer.ACTIVE_ID,diff_hour=-1)
    shop_config = {}
    if version:
        shop_config = game_config.get_server_play_shop_mapping().get(version, {})
    if shop_config:
        superplayershop = SuperPlayerShop.get(version)
        for i in range(1, 4):
            shop_id_cong = shop_config.get(i, {})
            good_ids = shop_id_cong.keys()
            id_ = random.choice(good_ids)
            superplayershop.shop_goods[i] = shop_config[i][id_]
        superplayershop.refresh_times += 1
        superplayershop.refresh_time = time.time()
        superplayershop.save()


def server_active_reward(server):
    config_type = game_config.get_config_type(server)
    if config_type != 1:
        return
    uid = '%s1234567' % server
    mm = ModelManager(uid)

    version, new_server, s_time, e_time = get_inreview_version(mm.user, mm.serversuperplayer.ACTIVE_ID,diff_hour=1)
    super_rank = SuperPlayerRank(version)
    uids_rank = super_rank.get_users_rank(100)
    playrankreward_config = game_config.get_server_play_rankreward_mapping().get(version, {})
    rank_id = playrankreward_config.keys()
    rank_id.sort()
    for idx, info in enumerate(uids_rank):
        rank = idx + 1
        uid = info[0]
        reward = []
        if rank <= playrankreward_config.get(rank_id[0], {}).get('rank', [1])[-1]:
            reward =playrankreward_config.get(rank_id[0], {}).get('rank_reward', [])
        elif rank <= playrankreward_config.get(rank_id[1], {}).get('rank', [1])[-1]:
            reward =playrankreward_config.get(rank_id[1], {}).get('rank_reward', [])
        elif rank <= playrankreward_config.get(rank_id[2], {}).get('rank', [1])[-1]:
            reward =playrankreward_config.get(rank_id[2], {}).get('rank_reward', [])
        elif rank <= playrankreward_config.get(rank_id[3], {}).get('rank', [1])[-1]:
            reward =playrankreward_config.get(rank_id[3], {}).get('rank_reward', [])
        elif rank <= playrankreward_config.get(rank_id[4], {}).get('rank', [1])[-1]:
            reward =playrankreward_config.get(rank_id[4], {}).get('rank_reward', [])
        if reward:
            mm = ModelManager(uid)
            msg = i18n_msg.get(1213, mm.user.language_sort) % rank
            title = i18n_msg.get(1214, mm.user.language_sort)
            message = mm.mail.generate_mail(msg, title, reward)
            mm.mail.add_mail(message, save=True)


# 刷新时间func
def server_super_player_refresh_time(server):
    config_type = game_config.get_config_type(server)
    if config_type != 1:
        return
    uid = '%s1234567'%server
    mm = ModelManager(uid)

    version, new_server, s_time, e_time = get_inreview_version(mm.user, mm.serversuperplayer.ACTIVE_ID)
    str_time = strftimestamp(datetime_to_timestamp(s_time))
    str_end_time = strftimestamp(datetime_to_timestamp(e_time))
    result = []
    now = time.time()

    tmp_time = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    utc_time = time.mktime(tmp_time) - 30 *60
    if utc_time not in result:
        result.append(utc_time)
    i = 0
    while True:
        next_time = (ceil(now / 1800) + i) * 1800
        i += 1
        tmp_end_time = time.strptime(str_end_time, '%Y-%m-%d %H:%M:%S')
        utc_end_time = time.mktime(tmp_end_time)
        if next_time > utc_end_time:
            break
        if next_time in result:
            continue
        result.append(next_time)


    return [datetime.datetime.fromtimestamp(t) for t in sorted(result)]

# 发奖时间func
def server_active_reward_time(server):
    config_type = game_config.get_config_type(server)
    if config_type != 1:
        return
    uid = '%s1234567' % server
    mm = ModelManager(uid)

    version, new_server, s_time, e_time = get_inreview_version(mm.user, mm.serversuperplayer.ACTIVE_ID)
    str_times = strftimestamp(datetime_to_timestamp(e_time))
    result = []
    for str_time in str_times:
        tmp_time = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
        utc_time = time.mktime(tmp_time) + 5
        if utc_time in result:
            continue
        result.append(utc_time)

    return [datetime.datetime.fromtimestamp(t) for t in sorted(result)]
