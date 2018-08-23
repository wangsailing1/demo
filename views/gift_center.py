#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'

from logics.gift_center import (
    GiftCenterLogic,
    MonthlySignLogic,
    # PaySignLogic,
    # FirstWeekSignLogic,
    # FirstPaymentLogic,
    # LevelLimitGiftLogic,
    # WelfareLoginLogics,
    WelfareCardLoginLogics,
    WelfareThreeDayLogics,
    OnlineDurationLogics,
    LevelGiftLogics,
    EnergyLogics,
)


def index(hm):
    """ 福利中心

    :param hm:
    :return:
    """
    mm = hm.mm

    gcl = GiftCenterLogic(mm)
    result = gcl.index()

    return 0, result


def monthly_sign_index(hm):
    """ 每日签到首页

    :param hm:
    :return:
    """
    mm = hm.mm

    msl = MonthlySignLogic(mm)
    result = msl.index()

    return 0, result


def monthly_sign(hm):
    """ 每日签到

    :param hm:
    :return:
    """
    mm = hm.mm

    msl = MonthlySignLogic(mm)
    rc, data = msl.sign()
    if rc != 0:
        return rc, {}

    return 0, data


# def pay_sign_index(hm):
#     """ 豪华签到首页
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     psl = PaySignLogic(mm)
#     result = psl.index()
#
#     return 0, result


# def pay_sign(hm):
#     """ 豪华签到
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     psl = PaySignLogic(mm)
#     rc, data = psl.sign()
#     if rc != 0:
#         return rc, {}
#
#     return 0, data


# def first_week_sign_index(hm):
#     """ 首周签到首页
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     fsl = FirstWeekSignLogic(mm)
#     result = fsl.index()
#
#     return 0, result


# def first_week_sign(hm):
#     """ 首周签到签到
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     fsl = FirstWeekSignLogic(mm)
#     rc, data = fsl.sign()
#     if rc != 0:
#         return rc, {}
#
#     return 0, data


# def first_payment_index(hm):
#     """ 首充首页
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     fpl = FirstPaymentLogic(mm)
#     result = fpl.index()
#
#     return 0, result


# def first_payment(hm):
#     """ 首充领奖
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     fpl = FirstPaymentLogic(mm)
#     rc, data = fpl.award()
#     if rc != 0:
#         return rc, {}
#
#     return 0, data


# def level_limit_gift_index(hm):
#     """ 等级限时礼包首页
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     llgl = LevelLimitGiftLogic(mm)
#     result = llgl.index()
#
#     return 0, result


# def level_limit_gift(hm):
#     """ 等级限时礼包领奖
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     llgl = LevelLimitGiftLogic(mm)
#     rc, data = llgl.award()
#     if rc != 0:
#         return rc, {}
#
#     return 0, data


# def login_index(hm):
#     """
#     累积登陆首页
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     wll = WelfareLoginLogics(mm)
#     data = wll.index()
#
#     return 0, data
#
#
# def login_award(hm):
#     """
#     领取累积登陆奖励
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     reward_id = hm.get_argument('reward_id', is_int=True)
#
#     if reward_id <= 0:
#         return 'error_100', {}
#
#     wll = WelfareLoginLogics(mm)
#     rc, data = wll.award(reward_id)
#     if rc != 0:
#         return rc, {}
#
#     return 0, data


def card_login_index(hm):
    """
    登陆翻牌首页
    :param hm:
    :return:
    """
    mm = hm.mm

    wcll = WelfareCardLoginLogics(mm)
    data = wcll.index()

    return 0, data


def card_login_open(hm):
    """
    登陆翻牌
    :param hm:
    :return:
    """
    mm = hm.mm

    wcll = WelfareCardLoginLogics(mm)
    rc, data = wcll.open_card()
    if rc != 0:
        return rc, {}

    return 0, data


def three_days_index(hm):
    """
    三顾茅庐首页
    :param hm:
    :return:
    """
    mm = hm.mm

    wtdl = WelfareThreeDayLogics(mm)
    data = wtdl.index()

    return 0, data


def three_days_award(hm):
    """
    三顾茅庐领奖
    :param hm:
    :return:
    """
    mm = hm.mm

    day_id = hm.get_argument('day_id', is_int=True)

    if day_id <= 0:
        return 'error_100', {}

    wtdl = WelfareThreeDayLogics(mm)
    rc, data = wtdl.award(day_id)
    if rc != 0:
        return rc, {}

    return 0, data


def online_index(hm):
    """
    累计在线首页
    :param hm:
    :return:
    """
    mm = hm.mm

    odl = OnlineDurationLogics(mm)
    data = odl.index()

    return 0, data


def online_award(hm):
    """
    累计在线领奖
    :param hm:
    :return:
    """
    mm = hm.mm

    reward_id = hm.get_argument('reward_id', is_int=True)

    if reward_id <= 0:
        return 'error_100', {}

    odl = OnlineDurationLogics(mm)
    rc, data = odl.award(reward_id)
    if rc != 0:
        return rc, {}

    return 0, data


def level_index(hm):
    """
    等级礼包首页
    :param hm:
    :return:
    """
    mm = hm.mm

    lgl = LevelGiftLogics(mm)
    data = lgl.index()

    return 0, data


def level_award(hm):
    """
    等级礼包领取奖励
    :param hm:
    :return:
    """
    mm = hm.mm

    reward_id = hm.get_argument('reward_id', is_int=True)

    if reward_id <= 0:
        return 'error_100', {}

    lgl = LevelGiftLogics(mm)
    rc, data = lgl.award(reward_id)
    if rc != 0:
        return rc, {}

    return 0, data


def energy_index(hm):
    """
    领取体力界面
    :param hm:
    :return:
    """
    mm = hm.mm

    el = EnergyLogics(mm)
    data = el.index()

    return 0, data


def get_energy(hm):
    """
    领取体力
    :param hm:
    :return:
    """
    mm = hm.mm
    energy_id = hm.get_argument('energy_id', is_int=True)

    if not energy_id:
        return 'error_100', {}   # 参数错误

    el = EnergyLogics(mm)
    rc, data = el.get_energy(energy_id)

    return rc, data
