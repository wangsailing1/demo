#! --*-- coding: utf-8 --*--
__author__ = 'sm'

from logics.script_gacha import ScriptGachaLogics
from tools.unlock_build import GACHA_SORT


def index(hm):
    """
    抽剧本入口
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(GACHA_SORT):
    #     return 'error_unlock', {}

    gl = ScriptGachaLogics(mm, 0)
    data = gl.gacha_index()

    return 0, data


def get_gacha(hm):
    """
    gacha抽剧本
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(GACHA_SORT):
    #     return 'error_unlock', {}

    sort = hm.get_argument('sort', is_int=True)

    gl = ScriptGachaLogics(mm, sort)

    rc, data = gl.get_gacha(sort)

    if rc != 0:
        return rc, {}

    return 0, data

def up_build(hm):
    cl = ScriptGachaLogics(hm.mm,0)
    rc, data = cl.up_build_level()
    return rc, data
