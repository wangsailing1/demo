#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from logics.shop import (
    AllShopLogics,
    ShopLogics,
    PeriodShopLogics,
    GiftShopLogics,
    ResourceShopLogics,
    MysticalShopLogics,
)
from tools.unlock_build import SHOP_SORT, PERIOD_SHOP, DARK_STREET, GUILD_SHOP_SORT, PROFITEER_SHOP, HONOR_SHOP
from tools.unlock_build import check_build


def check_close(func):
    def wrapper(hm):
        return 'error_close_shop', {}
    return wrapper


def all_shop(hm):
    """
    商店统一接口
    :param hm:
    :return:
    """
    mm = hm.mm

    asl = AllShopLogics(mm)
    rc, data = asl.all_shop()
    if rc != 0:
        return rc, {}

    return rc, data


def index(hm):
    """
    商店入口
    :param hm:
    :return:
    """
    mm = hm.mm

    if not mm.user.check_build(SHOP_SORT):
        return -1, {}   # 未解锁

    sl = ShopLogics(mm)
    rc, data = sl.index()
    if rc != 0:
        return rc, {}

    return rc, data


def buy(hm):
    """
    购买商品
    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)

    if not id:
        return 'error_100', {}

    if not mm.user.check_build(SHOP_SORT):
        return -1, {}

    sl = ShopLogics(mm)
    rc, data = sl.buy(good_id)
    if rc != 0:
        return rc, {}
    # # 触发商城购买任务
    # task_event_dispatch = mm.get_event('task_event_dispatch')
    # task_event_dispatch.call_method('shop_buy', 1)
    return 0, data


def refresh_goods(hm):
    """
    刷新商店普通物品
    :param hm:
    :return:
    """
    mm = hm.mm

    if not mm.user.check_build(SHOP_SORT):
        return -1, {}

    shop_logics = ShopLogics(mm)
    rc, data = shop_logics.refresh_goods()
    if rc != 0:
        return rc, {}

    return rc, data


def sell(hm):
    """
    物品回收
    :param hm:
    :return:
    """
    mm = hm.mm

    items = hm.get_mapping_arguments('item', params_type=(int, str, int))
    if not items:
        return 'error_100', {}

    if not mm.user.check_build(SHOP_SORT):
        return -1, {}

    sl = ShopLogics(mm)
    rc, data = sl.sell(items)
    if rc != 0:
        return rc, {}

    return 0, data

#礼品商店首页
def gift_index(hm):
    mm = hm.mm

    # if not mm.user.check_build(SHOP_SORT):
    #     return -1, {}

    psl = GiftShopLogics(mm)
    rc, data = psl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def gift_buy(hm):
    """ 限时商店购买

    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)

    if not good_id:
        return -1, {}

    # if not mm.user.check_build(SHOP_SORT):
    #     return -2, {}

    psl = GiftShopLogics(mm)
    rc, data = psl.buy(good_id)
    if rc != 0:
        return rc, {}

    return 0, data


#资源商店首页
def resource_index(hm):
    mm = hm.mm

    # if not mm.user.check_build(SHOP_SORT):
    #     return -1, {}

    psl = ResourceShopLogics(mm)
    rc, data = psl.index()
    if rc != 0:
        return rc, {}

    return 0, data

def resource_buy(hm):
    """ 限时商店购买

    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)

    if not good_id:
        return -1, {}

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -2, {}

    psl = ResourceShopLogics(mm)
    rc, data = psl.buy(good_id)
    if rc != 0:
        return rc, {}

    return 0, data


#神秘商店首页
def mystical_index(hm):
    mm = hm.mm

    # if not mm.user.check_build(SHOP_SORT):
    #     return -1, {}

    psl = MysticalShopLogics(mm)
    rc, data = psl.index()
    if rc != 0:
        return rc, {}

    return 0, data

def mystical_buy(hm):
    """ 限时商店购买

    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)

    if not good_id:
        return -1, {}

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -2, {}

    psl = MysticalShopLogics(mm)
    rc, data = psl.buy(good_id)
    if rc != 0:
        return rc, {}

    return 0, data

def period_index(hm):
    """ 限时商店首页

    :param hm:
    :return:
    """
    mm = hm.mm

    if not mm.user.check_build(PERIOD_SHOP):
        return -1, {}

    psl = PeriodShopLogics(mm)
    rc, data = psl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def period_buy(hm):
    """ 限时商店购买

    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)

    if not good_id:
        return -1, {}

    if not mm.user.check_build(PERIOD_SHOP):
        return -2, {}

    psl = PeriodShopLogics(mm)
    rc, data = psl.buy(good_id)
    if rc != 0:
        return rc, {}

    return 0, data


def period_refresh(hm):
    """ 限时商店刷新

    :param hm:
    :return:
    """
    mm = hm.mm

    if not mm.user.check_build(PERIOD_SHOP):
        return -1, {}

    psl = PeriodShopLogics(mm)
    rc, data = psl.refresh_goods()
    if rc != 0:
        return rc, {}

    return rc, data
