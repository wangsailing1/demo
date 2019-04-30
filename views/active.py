#! --*-- coding: utf-8 --*--

from logics.active import ActiveCard, SevenLoginLogic, MonthlySignLogic, OmniExchange, ServerOmniExchange


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

def get_gift(hm):
    mm = hm.mm
    active_id = hm.get_argument('active_id', 0, is_int=True)
    acl = ActiveCard(mm)
    rc, data = acl.get_gift(active_id)
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
    if not mm.seven_login.is_open():
        return 1, {}  # 活动已结束

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

def box_get(hm):
    """
    宝箱领取
    :param hm: 
    :return: 
    """
    mm = hm.mm
    days = hm.get_argument('days', 0, is_int=True)
    msl = MonthlySignLogic(mm)
    rc, data = msl.box_get(days)
    return rc, data

def omni_index(hm):
    mm = hm.mm
    server_type = int(mm.user.config_type)
    if server_type == 1:
        nel = ServerOmniExchange(mm)
        log_m = mm.omni_exchange
    else:
        nel = OmniExchange(mm)
        log_m = mm.omni_exchange

    remain_time = nel.remain_time()

    return 0, {
        'exchange_log': log_m.get_cur_exchange_log(),
        'remain_time': remain_time,
        'version': log_m.version,
    }

def omni_exchange(hm):
    """
    限时兑换
    :param env:
    :return:
    """
    mm = hm.mm
    exchange_id = hm.get_argument('exchange_id', 0, is_int=True)
    times = hm.get_argument('times', 1, is_int=True)

    if times <= 0:
        return 'error_100', {}

    server_type = int(mm.user.config_type)
    if server_type == 1:
        nel = ServerOmniExchange(mm)
    else:
        nel = OmniExchange(mm)
    rs, result = nel.omni_exchange(exchange_id, times)
    print result

    return rs, result
