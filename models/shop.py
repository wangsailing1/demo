#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
import math

from lib.db import ModelBase
from lib.core.environ import ModelManager
from lib.utils import weight_choice, get_it, not_repeat_weight_choice_2
from gconfig import game_config
from tools.unlock_build import check_build, PERIOD_SHOP


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

    AUTO_REFRESH_TIME = 3600 * 2    # 商店自动刷新时间 2小时刷新一次
    STOP_REFRESH_TIME = 60          # 禁止刷新时间 商店自动刷新时间前1分钟禁止刷新
    MAX_REFRESH_TIMES = 20          # 每天最多刷新20次

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'refresh_time': 0,
            'refresh_times': 0,
            'goods': {},
            'refresh_date': '',
        }
        super(Shop, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        if not self.refresh_date or self.refresh_date != today:
            self.refresh_date = today
            self.refresh_times = 0
            self.save()

    def data_update_func_1(self):
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
        return game_config.shop_sell.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_shop_id_with_level(level)
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


class PeriodShop(Shop):
    """ 限时商店 (时空旅行商人)

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

    CONTINUED_TIMES = 2 * 3600      # 开启限时商店时间
    OPEN_RATE = 5                   # 开启概率 5 %
    # OPEN_RATE = 100                   # 开启概率 5 %

    def __init__(self, uid):
        self.uid = uid
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
        goods_weight = game_config.get_period_shop_id_with_level(level)
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
        if check_build(self.mm, PERIOD_SHOP) and get_it(self.OPEN_RATE) and not self.start_time:
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


# class DarkShop(Shop):
#     """
#     黑街商店
#     """
#     def get_shop_config(self, goods_id):
#         """
#         获取商店配置
#         :param goods_id:
#         :return:
#         """
#         return game_config.darkstreet_shop.get(goods_id)
#
#     def get_shop_id_with_level(self, level):
#         """
#         根据等级获取商品
#         :param level:
#         :return:
#         """
#         goods_weight = game_config.get_dark_shop_id_with_level(level)
#         return goods_weight


class GuildShop(Shop):
    """
    公会商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.guild_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_guild_shop_with_level(level)
        return goods_weight


class HighLadderShop(Shop):
    """
    天梯竞技场商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.arena_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_arena_shop_id_with_level(level)
        return goods_weight


class DonateShop(Shop):
    """
    荣耀商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.donate_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_donate_shop_id_with_level(level)
        return goods_weight



class RallyShop(Shop):
    """
    血尘拉力赛商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.rally_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_rally_shop_id_with_level(level)
        return goods_weight


class BoxShop(Shop):
    """
    觉醒积分商店
    """
    AUTO_REFRESH_TIME = 3600 * 48

    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.shop_box.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_box_shop_id_with_level(level)
        return goods_weight


class KingWarShop(Shop):
    """
    斗技商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.king_war_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_king_war_shop_id_with_level(level)
        return goods_weight


class WormHoleShop(Shop):
    """
    虫洞矿坑商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.tower_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_wormhole_shop_id_with_level(level)
        return goods_weight


class EquipShop(Shop):
    """
    装备商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.equip_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_equip_shop_id_with_level(level)
        return goods_weight


class ProfiteerShop(Shop):
    """
    军需商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.profiteer_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_profiteer_shop_id_with_level(level)
        return goods_weight


class HonorShop(Shop):
    """
    荣誉商店
    """
    def get_shop_config(self, goods_id):
        """
        获取商店配置
        :param goods_id:
        :return:
        """
        return game_config.honor_shop.get(goods_id)

    def get_shop_id_with_level(self, level):
        """
        根据等级获取商品
        :param level:
        :return:
        """
        goods_weight = game_config.get_honor_shop_id_with_level(level)
        return goods_weight


ModelManager.register_model('shop', Shop)
ModelManager.register_model('period_shop', PeriodShop)
# ModelManager.register_model('dark_shop', DarkShop)
ModelManager.register_model('guild_shop', GuildShop)
ModelManager.register_model('high_ladder_shop', HighLadderShop)
ModelManager.register_model('donate_shop', DonateShop)
ModelManager.register_model('rally_shop', RallyShop)
ModelManager.register_model('box_shop', BoxShop)
ModelManager.register_model('king_war_shop', KingWarShop)
ModelManager.register_model('wormhole_shop', WormHoleShop)
ModelManager.register_model('equip_shop', EquipShop)
ModelManager.register_model('profiteer_shop', ProfiteerShop)
ModelManager.register_model('honor_shop', HonorShop)
