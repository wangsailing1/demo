#! --*-- coding: utf-8 --*--

from logics.server_rmb_foundation import ServerRmbFoundation


def server_rmbfoundation_index(hm):
    # 基金活动的首页
    mm = hm.mm
    ser_rmb_f = mm.serverrmbfoundation
    if not ser_rmb_f.has_reward() and not ser_rmb_f.is_open():
        return 1, {}  # 活动未开启
    s_rmbfoundation = ServerRmbFoundation(mm)
    rc, data = s_rmbfoundation.server_rmbfoundation_index()
    return rc, data


def server_withdraw(hm):
    # 领取奖励的接口
    mm = hm.mm
    f_id = hm.get_argument('f_id', 0, is_int=True)
    days = hm.get_argument('days', 0, is_int=True)
    ser_rmb_f = mm.serverrmbfoundation
    if not ser_rmb_f.has_reward() and not ser_rmb_f.is_open():
        return 1, {}  # 活动未开启
    if not f_id or not days:
        return 2, {}  # 参数错误
    if f_id not in ser_rmb_f.activate_mark:
        return 3, {}  # 该基金未激活
    s_rmbfoundation = ServerRmbFoundation(mm)
    rc, data = s_rmbfoundation.server_withdraw(f_id, days)
    return rc, data