#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

# 首页
from logics.director import Director
from gconfig import game_config
from tools.gift import has_mult_goods, del_mult_goods


def director_index(hm):
    mm = hm.mm
    director = Director(mm)
    rc, data = director.index()
    return rc, data


# 随机抽导演

def get_gacha(hm):
    mm = hm.mm
    gacha_type = hm.get_argument('gacha_type', 1, is_int=True)
    config = game_config.director_gacha_cost[gacha_type]
    rc = has_mult_goods(mm, config['cost'])
    if not rc:
        return rc, {}  # 道具不足
    director = Director(mm)
    rc, data = director.get_gacha(gacha_type)
    del_mult_goods(mm, config['cost'])
    mm.director.save()
    return rc, data

# 招聘导演
def get_gacha_id(hm):
    mm = hm.mm
    gacha_type = hm.get_argument('gacha_type', 1, is_int=True)
    gacha_id = hm.get_argument('gacha_id', 0, is_int=True)
    if not gacha_id:
        return 1, {}
    director = Director(mm)
    rc, data = director.get_gacha_id(gacha_type, gacha_id)
    mm.director.save()
    return rc, data


# 导演升级
def up_level(hm):
    mm = hm.mm
    director_id = hm.get_argument('director_id', '')
    if not director_id:
        return 1, {}  # 导演id错误
    director = Director(mm)
    rc, data = director.up_level(director_id)
    return rc, data

# 导演上阵
def work(hm):
    mm = hm.mm
    director_id = hm.get_argument('director_id', '')
    pos = hm.get_argument('pos', 0, is_int=True)
    if not director_id:
        return 1, {}  # 导演id错误
    if not pos:
        return 2, {}  #  位置错误
    director = Director(mm)
    rc, data = director.work(director_id, pos)
    return rc, data

# 导演休息
def rest(hm):
    mm = hm.mm
    director_id = hm.get_argument('director_id', '')
    if not director_id:
        return 1, {}  # 导演id错误
    director = Director(mm)
    rc, data = director.rest(director_id)
    return rc, data

# 位置解锁
def unlock_pos(hm):
    mm = hm.mm
    pos = hm.get_argument('pos', 0, is_int=True)
    if not pos:
        return 1, {}  #  位置错误
    director = Director(mm)
    rc, data = director.unlock_pos(pos)
    return rc, data

def buy_more_gacha_times(hm):
    mm = hm.mm
    director = Director(mm)
    rc, data = director.buy_more_gacha_times()
    return rc, data



