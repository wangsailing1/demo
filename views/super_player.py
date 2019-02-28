#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

from logics.super_player import SuperPlayer
from lib.utils.debug import print_log


def index(env):
    """
    首页

    """
    user = env.user
    super_user = SuperPlayer(user)

    rc = super_user.is_enter()
    if rc != 0:
        return rc, {}
    print_log('super_user',user.superplayer.version)

    rc, data = super_user.index()
    if rc != 0:
        return rc, {}
    return 0, data


def buy_goods(env):
    # 购买商品
    user = env.user
    super_user = SuperPlayer(user)

    rc = super_user.is_enter()
    if rc != 0:
        return rc, {}
    sort_id = int(env.get_argument('sort_id', 0))
    good_id = int(env.get_argument('good_id', 0))
    if sort_id <= 0 or sort_id > 3:
        return -1, {}  # 参数错误

    rc, data = super_user.buy_goods(sort_id, good_id)
    return rc, data


def get_reward(env):
    user = env.user
    step_id = int(env.get_argument('step_id', 0))
    reward_id = int(env.get_argument('reward_id', 0))
    if not step_id or not reward_id:
        return -1, {}  # 没有要领取的成就id

    super_user = SuperPlayer(user)
    rc = super_user.is_enter()
    if rc != 0:
        return rc, {}

    rc, data = super_user.get_reward(step_id, reward_id)
    return rc, data


def get_bag_code(env):
    user = env.user
    super_user = SuperPlayer(user)
    rc = super_user.is_enter()
    if rc != 0:
        return rc, {}
    redbag_info = super_user.get_red_bag()
    return 0, {'redbag_info': redbag_info,
               'grep_time': user.superplayer.get_time,
               'can_receive_times': user.superplayer.can_receive_times,
            }


def grab_bag(env):
    user = env.user
    bag_code = env.get_argument('bag_code', '')
    if not bag_code:
        return -1, {}  # 没有要领取的红包code

    super_user = SuperPlayer(user)
    rc = super_user.is_enter()
    if rc != 0:
        return rc, {}
    rc, data = super_user.grab_bag(bag_code)
    return rc, data


def get_rank_info(env):
    user = env.user
    super_user = SuperPlayer(user)
    rc = super_user.is_enter()
    if rc != 0:
        return rc, {}
    rc, data = super_user.get_rank_info(20)
    return rc, data


