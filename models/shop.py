#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
import math

from lib.db import ModelBase
from lib.core.environ import ModelManager
from lib.utils import weight_choice, get_it, not_repeat_weight_choice_2
from gconfig import game_config
from tools.unlock_build import check_build


class Shop(ModelBase):
    """
    商店
    :var refresh_time: 1449025282   # 刷新时间
    :var refresh_times: 0           # 刷新次数
    :var goods: {            # 普通商品
        id: {
            shop_id: 0,
            times: 0,
            sell_num: 0,
        },
    }
    """
    FORMAT = '%Y-%m-%d %H:%M:%S'
    AUTO_REFRESH_TIME = 3600 * 2  # 商店自动刷新时间 2小时刷新一次
    STOP_REFRESH_TIME = 60  # 禁止刷新时间 商店自动刷新时间前1分钟禁止刷新
    MAX_REFRESH_TIMES = 20  # 每天最多刷新20次

    def __init__(self, uid, shop_id=1):
        self.uid = uid
        self.shop_id = shop_id
        self._attrs = {
            'refresh_time': 0,
            'refresh_times': 0,
            'goods': {},
            'refresh_date': '',
            'next_time': 0
        }
        super(Shop, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        if not self.refresh_date or self.refresh_date != today:
            self.refresh_date = today
            self.refresh_times = 0
            # self.save()
        if not self.goods:
            self.refresh_goods(is_save=True)

    def refresh_goods(self, is_save=False):
        if self.goods:
            self.goods = {}
        level = self.mm.user.level
        goods_weight = self.get_shop_id_with_level(level)
        if not goods_weight:
            return
        for i, j in goods_weight.iteritems():
            if not j:
                continue
            goods_id = weight_choice(j)[0]
            sell_config = self.get_shop_config(goods_id)
            if not sell_config:
                continue
            sell_num = sell_config.get('sell_num', 0)
            discount, price = self.get_price(sell_num, sell_config)
            self.goods[i] = {'shop_id': goods_id, 'times': 0, 'sell_num': price, 'discount': discount}
        if is_save:
            self.save()

    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.shop_goods.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_shop_id_with_level(self.shop_id, level)
        return goods_weight

    def get_price(self, price, shop_config):
        """
        实际价格
        :param price:
        :param shop_config:
        :return:
        """
        discount = weight_choice(shop_config.get('discount', [10, 1]))[0]

        return discount, int(math.ceil(round(price * 0.1 * discount, 2)))


# 神秘商店
class MysticalShop(Shop):
    FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, uid, shop_id=4):
        self.uid = uid
        self.shop_id = shop_id
        self._attrs = {
            'show_times': 0,
            'start_time': 0,
            'refresh_time': 0,
            'refresh_times': 0,
            'next_time': 0,
            'refresh_date': '',
            'goods': {},
        }
        super(Shop, self).__init__(self.uid)

    def pre_use(self):
        refresh_time, next_time = self.get_refresh_time()
        now = time.strftime(self.FORMAT)
        save = self.mysticalrefresh_times()
        self.mysticalrefresh_times()
        if self.refresh_time < refresh_time and now > refresh_time:
            self.refresh_goods()
            self.refresh_time = refresh_time
            self.next_time = int(time.mktime(time.strptime(next_time, self.FORMAT)))
            save = True
        if save:
            self.save()

    def mysticalrefresh_times(self):
        today = time.strftime('%F')
        if self.refresh_date != today:
            self.refresh_date = today
            self.refresh_times = 0
            return True
        return False

    def refresh_goods(self, is_save=False, is_manual=False):

        if self.goods:
            self.goods = {}
        level = self.mm.user.level
        goods_weight = self.get_shop_id_with_level(level)
        if not goods_weight:
            return
        for i, j in goods_weight.iteritems():
            if not j:
                continue
            goods_id = weight_choice(j)[0]
            sell_config = self.get_shop_config(goods_id)
            if not sell_config:
                continue
            sell_num = sell_config.get('sell_num', 0)
            discount, price = self.get_price(sell_num, sell_config)
            self.goods[i] = {'shop_id': goods_id, 'times': 0, 'sell_num': price, 'discount': discount}
        if is_save:
            self.save()

    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.shop_goods.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_shop_id_with_level(self.shop_id, level)
        return goods_weight

    def get_refresh_time(self):
        config = game_config.mystical_store_cd
        now = time.strftime(self.FORMAT)
        yes = time.strftime(self.FORMAT, time.localtime(time.time() - 3600 * 24))
        tom = time.strftime(self.FORMAT, time.localtime(time.time() + 3600 * 24))
        tom_date, tom_tm = tom.split(' ')
        yes_date, yes_tm = yes.split(' ')
        date, tm = now.split(' ')
        refresh_time = sorted([i['cd_time'] for i in config.values()])
        for k, t in enumerate(refresh_time):
            if k == 0 and tm < t:
                return yes_date + ' ' + refresh_time[-1], date + ' ' + refresh_time[k]
            elif k == len(refresh_time) - 1 and tm >= t:
                return date + ' ' + refresh_time[k], tom_date + ' ' + refresh_time[0]
            elif t <= tm < refresh_time[k + 1]:
                return date + ' ' + refresh_time[k], date + ' ' + refresh_time[k + 1]


# 礼包
class GiftShop(Shop):
    def __init__(self, uid, shop_id=3):
        self.uid = uid
        self.shop_id = shop_id
        self._attrs = {
            'show_times': 0,
            'start_time': 0,
            'refresh_time': 0,
            'refresh_times': 0,
            'goods': {},
            'next_time': 0,
            'refresh_date': '',
        }
        super(Shop, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        save = False
        if self.refresh_date != today:
            self.refresh_date = today
            self.refresh_goods()
            self.refresh_time = time.strftime(self.FORMAT)
            save = True
        if not self.goods and not self.refresh_time:
            self.refresh_goods()
            self.refresh_time = time.strftime(self.FORMAT)
            save = True
        if save:
            self.save()

    def refresh_goods(self, is_save=False):
        if self.goods:
            self.goods = {}
        level = self.mm.user.level
        goods_weight = self.get_shop_id_with_level(level)
        if not goods_weight:
            return
        for i, j in goods_weight.iteritems():
            if not j:
                continue
            goods_id = weight_choice(j)[0]
            sell_config = self.get_shop_config(goods_id)
            if not sell_config:
                continue
            sell_num = sell_config.get('sell_num', 0)
            discount, price = self.get_price(sell_num, sell_config)
            self.goods[i] = {'shop_id': goods_id, 'times': 0, 'sell_num': price, 'discount': discount}
        if is_save:
            self.save()

    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.shop_goods.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_shop_id_with_level(self.shop_id, level)
        return goods_weight


# 资源
class ResourceShop(Shop):
    def __init__(self, uid, shop_id=2):
        self.uid = uid
        self.shop_id = shop_id
        self._attrs = {
            'show_times': 0,
            'start_time': 0,
            'refresh_time': 0,
            'refresh_times': 0,
            'goods': {},
            'next_time': 0,
            'refresh_date': '',
        }
        super(Shop, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        save = False
        if self.refresh_date != today:
            self.refresh_date = today
            self.refresh_goods()
            self.refresh_time = time.strftime(self.FORMAT)
            save = True
        if not self.goods and not self.refresh_time:
            self.refresh_goods()
            self.refresh_time = time.strftime(self.FORMAT)
            save = True
        if save:
            self.save()

    def refresh_goods(self, is_save=False):

        if self.goods:
            self.goods = {}
        level = self.mm.user.level
        goods_weight = self.get_shop_id_with_level(level)
        if not goods_weight:
            return
        for i, j in goods_weight.iteritems():
            if not j:
                continue
            goods_id = weight_choice(j)[0]
            sell_config = self.get_shop_config(goods_id)
            if not sell_config:
                continue
            sell_num = sell_config.get('sell_num', 0)
            discount, price = self.get_price(sell_num, sell_config)
            self.goods[i] = {'shop_id': goods_id, 'times': 0, 'sell_num': price, 'discount': discount}
        if is_save:
            self.save()

    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.shop_goods.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_shop_id_with_level(self.shop_id, level)
        return goods_weight


class PeriodShop(Shop):
    """ 神秘商店 

    :var show_times: 0              # 出现限时商店次数
    :var start_time: 1449025282     # 开始时间
    :var refresh_times: 0           # 刷新次数
    :var goods: {                   # 普通商品
        id: {
            shop_id: 0,
            times: 0,
            sell_num: 0,
        },
    }
    """

    CONTINUED_TIMES = 2 * 3600  # 开启限时商店时间
    OPEN_RATE = 5  # 开启概率 5 %

    # OPEN_RATE = 100                   # 开启概率 5 %

    def __init__(self, uid, shop_id=4):
        self.uid = uid
        self.shop_id = shop_id
        self._attrs = {
            'show_times': 0,
            'start_time': 0,
            'refresh_times': 0,
            'goods': {},
        }
        super(Shop, self).__init__(self.uid)

    def pre_use(self):
        """
        商店自动刷新
        :return:
        """
        if self.get_refresh_time() <= 0 and self.start_time:
            self.start_time = 0
            self.refresh_times = 0
            self.goods = {}
            self.save()

    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.period_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_shop_id_with_level(self.shop_id, level)
        return goods_weight

    def get_refresh_time(self):
        """
        获取剩余刷新时间
        :return:
        """
        if not self.start_time:
            return 0
        return max(self.start_time + self.CONTINUED_TIMES - int(time.time()), 0)

    def open_shop(self):
        """ 开启限时商店

        :return:
        """
        if  get_it(self.OPEN_RATE) and not self.start_time:
            self.start_time = int(time.time())
            self.show_times += 1
            self.refresh_times = 0
            self.refresh_goods(is_save=True)
            return self.show_times
        return 0

    def is_show(self):
        """ 是否展示

        :return:
        """
        return 1 if self.get_refresh_time() > 0 else 0


ModelManager.register_model('shop', Shop)
# ModelManager.register_model('period_shop', PeriodShop)
ModelManager.register_model('mystical_shop', MysticalShop)
ModelManager.register_model('gift_shop', GiftShop)
ModelManager.register_model('resource_shop', ResourceShop)
