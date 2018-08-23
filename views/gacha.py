#! --*-- coding: utf-8 --*--
__author__ = 'sm'

from logics.gacha import GachaLogics
from tools.unlock_build import GACHA_SORT


def index(hm):
    """
    抽卡入口
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(GACHA_SORT):
    #     return 'error_unlock', {}

    gl = GachaLogics(mm, 0)
    data = gl.gacha_index()

    return 0, data


def get_gacha(hm):
    """
    gacha抽卡
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(GACHA_SORT):
    #     return 'error_unlock', {}

    sort = hm.get_argument('sort', is_int=True)

    gl = GachaLogics(mm, sort)

    rc, data = gl.get_gacha(sort)

    if rc != 0:
        return rc, {}

    return 0, data


def receive(hm):
    """
    gacha接受卡牌
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(GACHA_SORT):
    #     return 'error_unlock', {}

    sort = hm.get_argument('sort', is_int=True)
    gacha_id = hm.get_argument('gacha_id', is_int=True)

    gl = GachaLogics(mm, sort)

    rc, data = gl.receive(gacha_id)
    return rc, data
