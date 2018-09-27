#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
import copy
import math

from gconfig import game_config
from tools.pay import (
    get_shop_refresh_need_diamond,
    get_period_shop_refresh_need_diamond,
    get_guild_shop_refresh_need_guild_coin,
    get_dark_shop_refresh_need_dark_coin,
    get_ladder_shop_refresh_need_ladder_coin,
    get_donate_shop_refresh_need_coin,
    get_rally_shop_refresh_need_rally_coin,
    get_king_war_shop_refresh_need_score,
    get_wormhole_shop_refresh_need_wormhole_coin,
    get_equip_shop_refresh_need_equip_coin,
    get_profiteer_shop_refresh_need_coin,
    get_honor_shop_refresh_need_coin,
)
from tools.gift import add_mult_gift, del_mult_goods, add_gift
from tools.unlock_build import check_build, GUILD_SHOP_SORT, DARK_STREET, DAILY_RALLY, AREA_SORT, DONATE_SHOP, \
    OUTLAND_PYRAMID, EQUIP_SHOP, HONOR_SHOP


class AllShopLogics(object):
    """
    商店统一接口
    """

    def __init__(self, mm):
        self.mm = mm

    def all_shop(self):
        """
        商店总界面需要返的数据
        :return:
        """
        data = {
            # 'period_shop_open': True if self.period_shop.get_refresh_time() else False,     # 限时商店是否开启
            'guild_shop_open': True if self.mm.user.guild_id else False,  # 公会商店是否开启
            'dark_shop_open': self.mm.user.check_build(DARK_STREET),  # 黑街商店是否开启
            'rally_shop_open': self.mm.user.check_build(DAILY_RALLY),  # 游骑兵黑市是否开启
            'arena_shop_open': self.mm.user.check_build(AREA_SORT),  # 竞技场商店是否开启
            'donate_shop_open': self.mm.user.check_build(DONATE_SHOP),  # 荣耀商店是否开启
            'wormhole_shop_open': False and self.mm.user.check_build(OUTLAND_PYRAMID),  # 虫洞商店是否开启
            'equip_shop_open': self.mm.user.check_build(EQUIP_SHOP),  # 装备商店是否开启
            'honor_shop_open': False and self.mm.user.check_build(HONOR_SHOP),  # 荣耀商店是否开启
        }

        return 0, data


class ShopLogics(object):
    def __init__(self, mm):
        self.mm = mm
        self.shop = self.mm.shop
        # self.refresh()
        self.sort = 1

    def index(self):
        goods = self.shop.goods

        goods = copy.deepcopy(goods)
        for k, v in goods.iteritems():
            sell_config = self.shop.get_shop_config(v['shop_id'])
            if not sell_config:
                return 2, {}  # 没有配置

            item = sell_config.get('item', [])
            v['item'] = item
            v['sell_sort'] = sell_config.get('sell_sort', 0)
            v['max_buy_times'] = sell_config['sell_max']
            v['is_hot'] = sell_config.get('is_hot', 0)
            v['exchange_lv'] = sell_config.get('exchange_lv', 0)

        cur_times = self.shop.refresh_times
        _, remain = self.get_remain_refresh_time()

        data = {
            'goods': goods,
            'refresh_times': cur_times,
            'remain': remain,
            'refresh_time': self.shop.refresh_time
        }

        return 0, data

    def refresh_goods(self):
        if self.is_stop_refresh():
            return 1, {}  # 我们正在准备进货，请耐心等待

        if self.shop.refresh_times >= self.shop.MAX_REFRESH_TIMES:
            return 2, {}  # 刷新次数不足

        need_diamond = get_shop_refresh_need_diamond(self.mm)
        if not self.mm.user.is_diamond_enough(need_diamond):
            return 'error_diamond', {}

        self.mm.user.deduct_diamond(need_diamond)
        self.shop.refresh_goods()
        self.shop.refresh_times += 1

        self.mm.user.save()
        self.shop.save()

        # 商城刷新
        # task_event_dispatch = self.mm.get_event('task_event_dispatch')
        # task_event_dispatch.call_method('shop_refresh', shop_sort=self.sort)

        return self.index()

    def refresh(self):
        """
        商店自动刷新
        :return:
        """
        div, remain_time = self.get_remain_refresh_time()
        now = int(time.time())

        if (div == 0 and remain_time == 0) or div:

            if div and remain_time:
                refresh_time = now + remain_time - self.shop.AUTO_REFRESH_TIME
            else:
                refresh_time = now

            self.shop.refresh_time = refresh_time
            self.shop.refresh_goods()
            self.shop.save()

    def get_remain_refresh_time(self):

        now = int(time.time())
        div = 0
        if self.shop.next_time == 0 or self.shop.next_time <= now:
            remain = 0
        else:
            remain = self.shop.next_time - now
        return div, remain

    def is_stop_refresh(self):
        """
        判断是否在禁止刷新时间内
        :return:
        """
        now = int(time.time())
        next_refresh = self.shop.refresh_time + self.shop.AUTO_REFRESH_TIME

        if next_refresh - self.shop.STOP_REFRESH_TIME <= now <= next_refresh:
            return True
        else:
            return False

    def buy(self, good_id, num):
        """
        购买商品
        :param good_id:
        :param shop_id:
        :return:
        """
        normal_goods = self.shop.goods
        goods = normal_goods.get(good_id, {})

        if not goods:
            return 2, {}

        shop_id = goods['shop_id']
        shop_config = self.shop.get_shop_config(shop_id)
        if not shop_config:
            return 3, {}

        if self.mm.user.level < shop_config.get('exchange_lv', 0):
            return 'error_shop_buy', {}
        if goods['times'] + num > shop_config['sell_max'] and shop_config['sell_max'] != -1:
            print goods
            return 4, {}

        sell_sort = shop_config['sell_sort']
        sell_num = goods['sell_num'] * num
        # self.shop.print_log(11111, [[sell_sort, 0, sell_num]])
        cost = [[sell_sort, 0, sell_num]]
        rc, _ = del_mult_goods(self.mm, cost)
        if rc != 0:
            return rc, {}

        goods['times'] += num
        gift_config = shop_config['item'] * num
        reward = add_mult_gift(self.mm, gift_config)
        rc, data = self.index()
        data['reward'] = reward

        # 记录累积商城购买次数
        # self.mm.task_data.add_task_data('shop', self.sort)
        # 触发商城购买任务
        # task_event_dispatch = self.mm.get_event('task_event_dispatch')
        # task_event_dispatch.call_method('shop_buy', self.sort)

        self.mm.user.save()
        self.shop.save()

        # 给bdc eventinfo用
        data["_bdc_event_info"] = {'cost': cost, 'goods_id': good_id, 'num': 1}
        return rc, data

    def sell(self, items):
        """
        物品回收
        :param items:
        :return:
        """
        new_items = []
        for sort, item_id, num in items:
            if sort not in [3, 4, 5, 6, 7]:
                continue
            if sort != 6:
                item_id = int(item_id)
            new_items.append([sort, item_id, num])

        if not new_items:
            return 2, {}

        rc, silvers = del_mult_goods(self.mm, new_items)
        if rc != 0:
            return rc, 0

        reward = add_gift(self.mm, 1, [[0, silvers]])

        result = {'reward': reward}

        return 0, result


class GiftShopLogics(ShopLogics):
    def __init__(self, mm):
        self.mm = mm
        self.shop = self.mm.gift_shop

    def buy(self, good_id, num):
        rc, data = super(GiftShopLogics, self).buy(good_id, num)
        if rc != 0:
            return rc, {}

        return rc, data


class ResourceShopLogics(ShopLogics):
    def __init__(self, mm):
        self.mm = mm
        self.shop = self.mm.resource_shop

    def buy(self, good_id, num):
        rc, data = super(ResourceShopLogics, self).buy(good_id, num)
        if rc != 0:
            return rc, {}

        return rc, data


class MysticalShopLogics(ShopLogics):
    def __init__(self, mm):
        self.mm = mm
        self.shop = self.mm.mystical_shop

    def buy(self, good_id, num):
        rc, data = super(MysticalShopLogics, self).buy(good_id, num)
        if rc != 0:
            return rc, {}

        return rc, data

    def refresh(self):
        self.shop.refresh_goods(is_save=True)


class PeriodShopLogics(ShopLogics):
    def __init__(self, mm):
        self.mm = mm
        self.shop = self.mm.period_shop
        self.sort = 0

    def refresh_goods(self):
        if not self.shop.start_time:
            return 1, {}

        need_diamond = get_period_shop_refresh_need_diamond(self.mm)
        if not self.mm.user.is_diamond_enough(need_diamond):
            return 'error_diamond', {}

        self.mm.user.deduct_diamond(need_diamond)
        self.shop.refresh_goods()
        self.shop.refresh_times += 1

        self.mm.user.save()
        self.shop.save()

        # 商城刷新
        # task_event_dispatch = self.mm.get_event('task_event_dispatch')
        # task_event_dispatch.call_method('shop_refresh', shop_sort=self.sort)

        return self.index()

    def buy(self, good_id):
        """
        购买商品
        :param good_id:
        :return:
        """
        if not self.shop.start_time:
            return 1, {}

        rc, data = super(PeriodShopLogics, self).buy(good_id)
        if rc != 0:
            return rc, {}

        return rc, data
