#!/usr/bin/python
# encoding: utf-8

from logics.egg import Egg
from gconfig import game_config


# 首页默认彩蛋
def egg_index(hm):
    mm = hm.mm
    egg = Egg(mm)
    if not egg.is_open():
        return 1, {}  # 活动未开启
    if not mm.egg.egg_diamond_reward_list or not mm.egg.egg_item_reward_list:
        rc, _ = egg.init_reward(save=True)
        if rc != 0:
            return rc, {}

    data = egg.index()
    data['reward_log'] = mm.egg.get_log()
    data['version'] = mm.egg.version
    return 0, data


# 开奖 egg_sort egg_type
def open_egg(hm):
    mm = hm.mm
    egg_type = hm.get_argument('egg_type', 0, is_int=True)
    is_super = hm.get_argument('is_super', 0, is_int=True)
    egg_sort = hm.get_argument('egg_sort', 0, is_int=True)
    lan = hm.get_argument('lan', 0, is_int=True)
    if not is_super and egg_sort not in [1, 2, 3]:
        return 1, {}  # 参数错误
    egg = Egg(mm)
    rc, reward = egg.open_egg(egg_type, is_super, egg_sort, lan)
    if rc != 0:
        return rc, {}

    data = egg.index()
    data['reward'] = reward['gift']
    # data['refresh_flog'] = reward['refresh_flog']
    data['reward_log'] = mm.egg.get_log()
    return 0, data


# 刷新
def refresh_egg(hm):
    mm = hm.mm
    egg_type = hm.get_argument('egg_type', 0, is_int=True)
    egg = Egg(mm)
    if not egg.is_open():
        return 1, {}  # 活动未开启
    if egg_type not in [1, 2]:
        return 4, {}  # 参数错误
    egg_diamond_info = game_config.egg_diamond.get(mm.egg.version)
    if egg_type == 1:
        need_num = egg_diamond_info.get('refresh_price')
    egg_item_info = game_config.egg_item.get(mm.egg.version)
    if egg_type == 2:
        need_num = egg_item_info.get('refresh_price')
    if not mm.user.is_diamond_enough(need_num):
        return 3, {}  # 钻石不足
    rc, _ = egg.init_reward(egg_type=egg_type)
    if rc != 0:
        return rc, {}
    mm.user.deduct_diamond(need_num)
    mm.egg.save()
    mm.user.save()

    data = egg.index()
    data['reward_log'] = mm.egg.get_log()
    return 0, data
