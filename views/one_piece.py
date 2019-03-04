# -*- coding: utf-8 -*-

__author__ = 'ljm'


from logics.one_piece import OnePieceLogic


def index(hm):
    """ 活动首页
        -1: 活动没有开启

    :param env:
    :return:
    """
    mm = hm.mm

    one_piece_logic = OnePieceLogic(mm)

    if one_piece_logic.get_remain_time() <= 0:
        return -1, {}

    return 0, one_piece_logic.index()


def open_roulette(hm):
    """ 开启轮盘
        -1: 活动没有开启
        error_4: 钻石不足

    :param env:
    :return:
    """
    mm = hm.mm

    one_piece_logic = OnePieceLogic(mm)

    if not one_piece_logic.is_open():
        return -100, {}

    if one_piece_logic.get_remain_time() <= 0:
        return -1, {}

    rc, data = one_piece_logic.open_roulette()

    return rc, data


def open_roulette10(hm):
    """ 开启轮盘10次
        -1: 活动没有开启
        error_4: 钻石不足

    :param env:
    :return:
    """
    mm = hm.mm

    one_piece_logic = OnePieceLogic(mm)

    if not one_piece_logic.is_open():
        return -100, {}

    if one_piece_logic.get_remain_time() <= 0:
        return -1, {}

    rc, data = one_piece_logic.open_roulette10()

    return rc, data


def info(hm):
    """ 获取详情

    :param env:
    :return:
    """
    mm = hm.mm

    one_piece_logic = OnePieceLogic(mm)

    if not one_piece_logic.is_open():
        return -100, {}

    if not one_piece_logic.is_show_rank():
        return -2, {}

    if one_piece_logic.get_remain_time() <= 0:
        return -1, {}

    return 0, one_piece_logic.info()


def exchange_index(hm):
    """ 兑换首页
        -1: 活动没有开启
        error_4: 钻石不足

    :param env:
    :return:
    """
    mm = hm.mm

    one_piece_logic = OnePieceLogic(mm)

    if not one_piece_logic.is_open():
        return -100, {}

    if one_piece_logic.get_remain_time() <= 0:
        return -1, {}

    return 0, one_piece_logic.exchange_index()


def exchange(hm):
    """ 兑换
        -1: 活动没有开启
        error_4: 钻石不足

    :param env:
    :return:
    """
    mm = hm.mm

    exchange_id = hm.get_argument('id',is_int=True)

    one_piece_logic = OnePieceLogic(mm)

    if not one_piece_logic.is_open():
        return -100, {}

    if one_piece_logic.get_remain_time() <= 0:
        return -1, {}

    rc, data = one_piece_logic.exchange(exchange_id)

    if rc != 0:
        return rc, {}

    data.update(one_piece_logic.index())

    return 0, data


def step_reward(hm):
    """ 阶段奖励

    :param env:
    :return:
    """
    mm = hm.mm

    step = hm.get_argument('step',is_int=True)

    one_piece_logic = OnePieceLogic(mm)

    if one_piece_logic.get_remain_time() <= 0:
        return -1, {}

    rc, data = one_piece_logic.step_reward(step)

    if rc != 0:
        return rc, {}

    data.update(one_piece_logic.index())

    return 0, data