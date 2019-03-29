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
from tools.unlock_build import check_build
import time
from gconfig import game_config


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

    # if not mm.user.check_build(SHOP_SORT):
    #     return -1, {}  # 未解锁

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
    num = int(hm.get_argument('num', 1))

    if not id:
        return 'error_100', {}

    # if not mm.user.check_build(SHOP_SORT):
    #     return -1, {}

    sl = ShopLogics(mm)
    rc, data = sl.buy(good_id, num)
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

    # if not mm.user.check_build(SHOP_SORT):
    #     return -1, {}

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

    # if not mm.user.check_build(SHOP_SORT):
    #     return -1, {}

    sl = ShopLogics(mm)
    rc, data = sl.sell(items)
    if rc != 0:
        return rc, {}

    return 0, data


# 礼品商店首页
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
    """ 礼品商店购买

    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)
    num = int(hm.get_argument('num', 1))

    if not good_id:
        return -1, {}

    # if not mm.user.check_build(SHOP_SORT):
    #     return -2, {}

    psl = GiftShopLogics(mm)
    rc, data = psl.buy(good_id, num)
    if rc != 0:
        return rc, {}

    return 0, data


# 资源商店首页
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
    """ 资源商店购买

    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)
    num = int(hm.get_argument('num', 1))

    if not good_id:
        return -1, {}

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -2, {}

    psl = ResourceShopLogics(mm)
    rc, data = psl.buy(good_id, num)
    if rc != 0:
        return rc, {}

    return 0, data


# 神秘商店首页
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
    """ 神秘商店购买

    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)
    num = int(hm.get_argument('num', 1))

    if not good_id:
        return -1, {}

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -2, {}

    psl = MysticalShopLogics(mm)
    rc, data = psl.buy(good_id, num)
    if rc != 0:
        return rc, {}

    return 0, data


def mystical_refresh(hm):
    """ 神秘商店刷新

    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -2, {}

    now = time.strftime(mm.mystical_shop.FORMAT)
    mm.mystical_shop.refresh_time = now
    mm.mystical_shop.refresh_goods()
    config = game_config.price_ladder
    # if mm.mystical_shop.refresh_times >= len(config):
    #     return 1, {}  # 刷新次数也达最大次数
    mm.mystical_shop.refresh_times += 1
    times = min(mm.mystical_shop.refresh_times, len(config))
    need_coin = config[times]['mystical_store_cost']
    if need_coin > mm.user.diamond:
        return 3, {}  # 钻石不足
    mm.user.deduct_diamond(need_coin)
    refresh_time, next_time = mm.mystical_shop.get_refresh_time()
    mm.mystical_shop.next_time = int(time.mktime(time.strptime(next_time, mm.mystical_shop.FORMAT)))
    mm.mystical_shop.save()
    psl = MysticalShopLogics(mm)
    rc, data = psl.index()
    mm.user.save()
    if rc != 0:
        return rc, {}

    return 0, data


def period_index(hm):
    """ 限时商店首页

    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -1, {}

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

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -2, {}

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

    # if not mm.user.check_build(PERIOD_SHOP):
    #     return -1, {}

    psl = PeriodShopLogics(mm)
    rc, data = psl.refresh_goods()
    if rc != 0:
        return rc, {}

    return rc, data
