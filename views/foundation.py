#!/usr/bin/python
# encoding: utf-8

from logics.foundation import Foundation


def foundation_index(hm):
    # 基金活动的首页
    mm = hm.mm
    if not mm.foundation.is_open():
        return 1, {}  # 活动未开启
    foundation = Foundation(mm)
    rc, data = foundation.foundation_index()
    return rc, data


def withdraw(hm):
    # 领取奖励的接口
    mm = hm.mm
    # if not mm.foundation.is_open():
    #     return 1, {}  # 活动未开启
    f_id = hm.get_argument('f_id', 0, is_int=True)
    if not f_id:
        return 2, {}  # 活动id错误
    if f_id not in mm.foundation.activate_mark:
        return 3, {}  # 该基金未激活
    foundation = Foundation(mm)
    rc, data = foundation.withdraw(f_id)
    return rc, data