# -*- coding: utf-8 –*-

from logics.daily_recharge import DailyRecharge as DRL


def index(hm):
    """ 首页
    """
    mm = hm.mm
    drl = DRL(mm)
    rc, data = drl.index()
    return rc, data


def reward(hm):
    """ 领奖
    """
    mm = hm.mm
    day = hm.get_argument('day', is_int=True)

    drl = DRL(mm)
    rc, data = drl.reward(day)
    return rc, data



