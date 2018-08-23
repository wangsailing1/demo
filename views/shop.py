#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from logics.shop import (
    AllShopLogics,
    ShopLogics,
    PeriodShopLogics,
    # DarkShopLogics,
    GuildShopLogics,
    HighLadderShopLogics,
    DonateShopLogic,
    RallyShopLogic,
    BoxShopLogic,
    KingWarShopLogics,
    WormHoleShopLogics,
    EquipShopLogics,
    ProfiteerShopLogics,
    HonorShopLogics,
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


# def dark_shop(hm):
#     """
#     黑街商店
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     if not mm.user.check_build(DARK_STREET):
#         return 'error_unlock', {}
#
#     dsl = DarkShopLogics(mm)
#     rc, data = dsl.index()
#     if rc != 0:
#         return rc, {}
#
#     return 0, data
#
#
# def dark_buy(hm):
#     """
#     黑街商店购买
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     if not mm.user.check_build(DARK_STREET):
#         return 'error_unlock', {}
#
#     goods_id = hm.get_argument('goods_id', is_int=True)
#
#     if not goods_id:
#         return 'error_100', {}
#
#     dsl = DarkShopLogics(mm)
#     rc, data = dsl.buy(goods_id)
#     if rc != 0:
#         return rc, {}
#     # # 触发商城购买任务
#     # task_event_dispatch = mm.get_event('task_event_dispatch')
#     # task_event_dispatch.call_method('shop_buy', 3)
#     return 0, data
#
#
# def dark_refresh(hm):
#     """
#     黑街商店手动刷新
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     if not mm.user.check_build(DARK_STREET):
#         return 'error_unlock', {}
#
#     dsl = DarkShopLogics(mm)
#     rc, data = dsl.dark_refresh()
#     if rc != 0:
#         return rc, {}
#
#     return 0, data


def guild_shop_index(hm):
    """
    公会商店首页
    :param hm:
    :return:
    """
    mm = hm.mm

    if not check_build(mm, GUILD_SHOP_SORT):
        return 'error_unlock', {}

    gsl = GuildShopLogics(mm)
    rc, data = gsl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def guild_shop_buy(hm):
    """
    公会商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    if not check_build(mm, GUILD_SHOP_SORT):
        return 'error_unlock', {}

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    gsl = GuildShopLogics(mm)
    rc, data = gsl.buy(goods_id)
    if rc != 0:
        return rc, {}

    return 0, data


def guild_shop_refresh(hm):
    """
    公会商店刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    if not check_build(mm, GUILD_SHOP_SORT):
        return 'error_unlock', {}

    gsl = GuildShopLogics(mm)
    rc, data = gsl.refresh_goods()
    if rc != 0:
        return rc, {}

    return 0, data


def high_ladder(hm):
    """
    天梯竞技场商店
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(DARK_STREET):
    #     return 'error_unlock', {}

    hls = HighLadderShopLogics(mm)
    rc, data = hls.index()
    if rc != 0:
        return rc, {}

    return 0, data


def high_ladder_buy(hm):
    """
    天梯竞技场商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(DARK_STREET):
    #     return 'error_unlock', {}

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    hls = HighLadderShopLogics(mm)
    rc, data = hls.buy(goods_id)
    if rc != 0:
        return rc, {}
    # # 触发商城购买任务
    # task_event_dispatch = mm.get_event('task_event_dispatch')
    # task_event_dispatch.call_method('shop_buy', 2)
    return 0, data


def high_ladder_refresh(hm):
    """
    天梯竞技场商店手动刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    # if not mm.user.check_build(DARK_STREET):
    #     return 'error_unlock', {}

    hls = HighLadderShopLogics(mm)
    rc, data = hls.high_ladder_refresh()
    if rc != 0:
        return rc, {}

    return 0, data


def donate(hm):
    """
    荣耀商店
    :param hm:
    :return:
    """
    mm = hm.mm

    dl = DonateShopLogic(mm)
    rc, data = dl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def donate_buy(hm):
    """
    荣耀商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    dl = DonateShopLogic(mm)
    rc, data = dl.buy(goods_id)
    if rc != 0:
        return rc, {}

    return 0, data


def donate_refresh(hm):
    """
    荣耀商店手动刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    dl = DonateShopLogic(mm)
    rc, data = dl.donate_refresh()
    if rc != 0:
        return rc, {}

    return 0, data


def rally(hm):
    """
    血沉商店
    :param hm:
    :return:
    """
    mm = hm.mm

    rsl = RallyShopLogic(mm)
    rc, data = rsl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def rally_buy(hm):
    """
    血沉商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    rsl = RallyShopLogic(mm)
    rc, data = rsl.buy(goods_id)
    if rc != 0:
        return rc, {}

    return 0, data


def rally_refresh(hm):
    """
    血沉商店手动刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    rsl = RallyShopLogic(mm)
    rc, data = rsl.refresh_shop()
    if rc != 0:
        return rc, {}

    return 0, data


def box_shop(hm):
    """
    觉醒积分商店
    :param hm:
    :return:
    """
    mm = hm.mm

    bsl = BoxShopLogic(mm)
    rc, data = bsl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def box_shop_buy(hm):
    """
    觉醒积分商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    bsl = BoxShopLogic(mm)
    rc, data = bsl.buy(goods_id)
    if rc != 0:
        return rc, {}

    return 0, data


@check_close
def king_war_index(hm):
    """
    商店入口
    :param hm:
    :return:
    """
    mm = hm.mm

    sl = KingWarShopLogics(mm)
    rc, data = sl.index()
    if rc != 0:
        return rc, {}

    return rc, data


@check_close
def king_war_buy(hm):
    """
    购买商品
    :param hm:
    :return:
    """
    mm = hm.mm
    good_id = hm.get_argument('goods_id', is_int=True)

    if not id:
        return 'error_100', {}

    sl = KingWarShopLogics(mm)
    rc, data = sl.buy(good_id)
    if rc != 0:
        return rc, {}
    # # 触发商城购买任务
    # task_event_dispatch = mm.get_event('task_event_dispatch')
    # task_event_dispatch.call_method('shop_buy', 1)
    return 0, data


@check_close
def king_war_refresh(hm):
    """
    刷新商店普通物品
    :param hm:
    :return:
    """
    mm = hm.mm

    shop_logics = KingWarShopLogics(mm)
    rc, data = shop_logics.refresh_goods()
    if rc != 0:
        return rc, {}

    return rc, data


@check_close
def wormhole(hm):
    """
    虫洞矿坑商店
    :param hm:
    :return:
    """
    mm = hm.mm

    whls = WormHoleShopLogics(mm)
    rc, data = whls.index()
    if rc != 0:
        return rc, {}

    return 0, data


@check_close
def wormhole_buy(hm):
    """
    虫洞矿坑商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    whls = WormHoleShopLogics(mm)
    rc, data = whls.buy(goods_id)
    if rc != 0:
        return rc, {}
    return 0, data


@check_close
def wormhole_refresh(hm):
    """
    虫洞矿坑商店手动刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    whls = WormHoleShopLogics(mm)
    rc, data = whls.wormhole_refresh()
    if rc != 0:
        return rc, {}

    return 0, data


def equip(hm):
    """
    装备商店
    :param hm:
    :return:
    """
    mm = hm.mm

    esl = EquipShopLogics(mm)
    rc, data = esl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def equip_buy(hm):
    """
    装备商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    esl = EquipShopLogics(mm)
    rc, data = esl.buy(goods_id)
    if rc != 0:
        return rc, {}
    return 0, data


def equip_refresh(hm):
    """
    装备商店手动刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    esl = EquipShopLogics(mm)
    rc, data = esl.equip_refresh()
    if rc != 0:
        return rc, {}

    return 0, data


def profiteer(hm):
    """
    军需商店
    :param hm:
    :return:
    """
    mm = hm.mm

    if not check_build(mm, PROFITEER_SHOP):
        return 'error_unlock', {}   # 未解锁

    psl = ProfiteerShopLogics(mm)
    rc, data = psl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def profiteer_buy(hm):
    """
    军需商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    psl = ProfiteerShopLogics(mm)
    rc, data = psl.buy(goods_id)
    if rc != 0:
        return rc, {}
    return 0, data


def profiteer_refresh(hm):
    """
    军需商店手动刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    psl = ProfiteerShopLogics(mm)
    rc, data = psl.profiteer_refresh()
    if rc != 0:
        return rc, {}

    return 0, data


def honor(hm):
    """
    荣誉商店
    :param hm:
    :return:
    """
    mm = hm.mm

    if not check_build(mm, HONOR_SHOP):
        return 'error_unlock', {}   # 未解锁

    hsl = HonorShopLogics(mm)
    rc, data = hsl.index()
    if rc != 0:
        return rc, {}

    return 0, data


def honor_buy(hm):
    """
    荣誉商店购买
    :param hm:
    :return:
    """
    mm = hm.mm

    goods_id = hm.get_argument('goods_id', is_int=True)

    if not goods_id:
        return 'error_100', {}

    hsl = HonorShopLogics(mm)
    rc, data = hsl.buy(goods_id)
    if rc != 0:
        return rc, {}
    return 0, data


def honor_refresh(hm):
    """
    荣誉商店手动刷新
    :param hm:
    :return:
    """
    mm = hm.mm

    hsl = HonorShopLogics(mm)
    rc, data = hsl.honor_refresh()
    if rc != 0:
        return rc, {}

    return 0, data
