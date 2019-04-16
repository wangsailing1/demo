#! --*-- coding: utf-8 --*--
from logics.rest import Rest

def rest_index(hm):
    mm = hm.mm
    sort = hm.get_argument('sort', 0, is_int=True)
    if not sort:
        return 1, {}  # 建筑错误
    rest = Rest(mm,sort)
    rc, data = rest.rest_index()
    return rc, data

def card_rest(hm):
    mm = hm.mm
    sort = hm.get_argument('sort', 0, is_int=True)
    pos = hm.get_argument('pos', 0, is_int=True)
    card = hm.get_argument('card','')
    if not sort:
        return 1, {}  # 参数错误
    if not pos:
        return 2, {}  # 请选择位置
    if not card:
        return 3, {}  # 请选择卡牌
    rest = Rest(mm, sort)
    rc, data = rest.card_rest(pos, card)
    return rc, data

def get_rest_card(hm):
    mm = hm.mm
    sort = hm.get_argument('sort', 0, is_int=True)
    pos = hm.get_argument('pos', 0, is_int=True)
    if not sort:
        return 1, {}  # 参数错误
    if not pos:
        return 2, {}  # 请选择位置
    rest = Rest(mm, sort)
    rc, data = rest.get_rest_card(pos)
    return rc, data

def done_now(hm):
    mm = hm.mm
    sort = hm.get_argument('sort', 0, is_int=True)
    pos = hm.get_argument('pos', 0, is_int=True)
    if not sort:
        return 1, {}  # 参数错误
    if not pos:
        return 2, {}  # 请选择位置
    rest = Rest(mm, sort)
    rc, data = rest.done_now(pos)
    return rc, data

def buy_extra_pos(hm):
    mm = hm.mm
    sort = hm.get_argument('sort', 0, is_int=True)
    if not sort:
        return 1, {}  # 参数错误
    rest = Rest(mm, sort)
    rc, data = rest.buy_extra_pos()
    return rc, data