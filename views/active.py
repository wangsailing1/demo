#! --*-- coding: utf-8 --*--

from logics.active import ActiveCard, SevenLoginLogic, MonthlySignLogic


def active_card_index(hm):
    """月卡至尊卡活动首页
    :param hm:
    :return:
    """
    mm = hm.mm
    acl = ActiveCard(mm)
    data = acl.show()

    return 0, data


def active_card_award(hm):
    """月卡至尊卡奖励领取"""
    mm = hm.mm

    active_id = hm.get_argument('active_id', 0, is_int=True)

    acl = ActiveCard(mm)

    rc, data = acl.receive(active_id)
    # data['active_center'] = mm.active_hot_dot.hot_dot()
    if rc != 0:
        return rc, data

    data['show'] = acl.show()

    return 0, data


def seven_login(hm):
    """
    七日登录index
    :param hm:
    :return:
    """
    mm = hm.mm

    sll = SevenLoginLogic(mm)
    rc, data = sll.seven_login_index()

    return rc, data


def seven_login_award(hm):
    """
    领取七日登录奖励
    :param hm:
    :return:
    """
    mm = hm.mm

    # day_id = hm.get_argument('day_id', is_int=True)

    # if day_id <= 0:
    #     return 'error_100', {}

    sll = SevenLoginLogic(mm)
    rc, data = sll.seven_login_award()

    return rc, data


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
