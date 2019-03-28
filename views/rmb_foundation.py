#!/usr/bin/python
# encoding: utf-8

from logics.rmb_foundation import RmbFoundation


def rmbfoundation_index(hm):
    # 基金活动的首页
    mm = hm.mm
    if not mm.rmbfoundation.has_reward() and not mm.rmbfoundation.is_open():
        return 1, {}  # 活动未开启
    rmbfoundation = RmbFoundation(mm)
    rc, data = rmbfoundation.rmbfoundation_index()
    return rc, data

def buy_rmbf(hm):
    mm = hm.mm
    f_id = hm.get_argument('f_id', 0, is_int=True)

    if not f_id:
        return 1, {}  # 参数错误
    if f_id in mm.rmbfoundation.activate_mark:
        return 2, {}  # 不能重复购买
    rmbfoundation = RmbFoundation(mm)
    rc, data = rmbfoundation.buy_rmbf(f_id)
    return rc, data

def withdraw(hm):
    # 领取奖励的接口
    mm = hm.mm
    f_id = hm.get_argument('f_id', 0, is_int=True)
    days = hm.get_argument('days', 0, is_int=True)
    if not mm.rmbfoundation.can_open():
        return 1, {}  # 活动未开启
    if not f_id or not days:
        return 2, {}  # 参数错误
    if f_id not in mm.rmbfoundation.activate_mark:
        return 3, {}  # 该基金未激活
    rmbfoundation = RmbFoundation(mm)
    rc, data = rmbfoundation.withdraw(f_id, days)
    return rc, data