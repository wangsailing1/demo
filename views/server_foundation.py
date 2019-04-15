#!/usr/bin/python
# encoding: utf-8

from logics.server_foundation import ServerFoundation


def server_foundation_index(hm):
    # 基金活动的首页
    mm = hm.mm

    foundation = ServerFoundation(mm)
    has_reward = mm.serverfoundation.has_reward()
    if not has_reward and not mm.serverfoundation.is_open():
        return 1, {}  # 活动未开启
    rc, data = foundation.server_foundation_index()
    return rc, data


def server_withdraw(hm):
    # 领取奖励的接口
    mm = hm.mm
    f_id = hm.get_argument('f_id', 0, is_int=True)
    days = hm.get_argument('days', 0, is_int=True)
    if not f_id or not days:
        return 2, {}  # 参数错误
    if f_id not in mm.serverfoundation.activate_mark:
        return 3, {}  # 该基金未激活
    has_reward = mm.serverfoundation.has_reward()
    if not has_reward and not mm.serverfoundation.is_open():
        return 1, {}  # 活动未开启
    foundation = ServerFoundation(mm)
    rc, data = foundation.server_withdraw(f_id, days)
    return rc, data