#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 用户相关的配置
from gconfig import check


# 商品出售配置
shop_goods = {
    'uk':           ('id',              'int'),                                         # 商品编号
    'shop_id':      ('shop_id',         'int'),                                         # 出售位置
    'show_lv':      ('show_lv',         'int'),                                         # 出现等级
    'exchange_lv':  ('exchange_lv',     'int'),                                         # 出现等级
    'pos_id':       ('pos_id',          'int'),                                         # 出售位置
    'item':         (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 给予物品
    'sell_sort':    ('sell_sort',       'int'),                                         # 售价类型
    'sell_num':     ('sell_num',        'int'),                                         # 售价
    'sell_max':     ('sell_max',        'int'),                                         # 限购数量
    'weight':       ('weight',          'int'),                                         # 出现权重
    'discount':     ('discount',        'list_2'),                                      # 折扣
    'is_hot':       ('is_hot',          'int'),                                         # 热卖标签
}


# 限时商店
# period_shop = {
#     'uk': ('id', 'int'),                                                        # 商品编号
#     'use_lv': ('use_lv', 'int'),                                                # 出现等级
#     'item': (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 给予物品
#     'sell_sort': ('sell_sort', 'int'),                                          # 售价类型
#     'sell_num': ('sell_num', 'int'),                                            # 售价
#     'weight': ('weight', 'int'),                                                # 出现权重
# }


# 黑街商店
# darkstreet_shop = {
#     'uk': ('shop_id', 'int'),                                                   # 商品编号
#     'show_lv': ('show_lv', 'int'),                                              # 出现等级
#     'item': (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 给予物品
#     'sell_sort': ('sell_sort', 'int'),                                          # 售价类型
#     'sell_num': ('sell_num', 'int'),                                            # 售价
#     'sell_max': ('sell_max', 'int'),                                            # 限购数量
#     'weight': ('weight', 'int'),                                                # 出现权重
# }


# # 公会商店
# guild_shop = {
#     'uk': ('shop_id', 'int'),                                                   # 商品编号
#     'show_lv': ('show_lv', 'int'),                                              # 出现等级
#     'item': (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 给予物品
#     'sell_sort': ('sell_sort', 'int'),                                          # 售价类型
#     'sell_num': ('sell_num', 'int'),                                            # 售价
#     'sell_max': ('sell_max', 'int'),                                            # 限购数量
#     'weight': ('weight', 'int'),                                                # 出现权重
# }


# # 天梯竞技场商店
# arena_shop = {
#     'uk': ('shop_id', 'int'),                                                   # 商品编号
#     'show_lv': ('show_lv', 'int'),                                              # 出现等级
#     'item': (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 给予物品
#     'sell_sort': ('sell_sort', 'int'),                                          # 售价类型
#     'sell_num': ('sell_num', 'int'),                                            # 售价
#     'sell_max': ('sell_max', 'int'),                                            # 限购数量
#     'weight': ('weight', 'int'),                                                # 出现权重
# }

# # 荣耀商店
# donate_shop = {
#     'uk': ('shop_id', 'int'),                                                   # 商品编号
#     'show_lv': ('show_lv', 'int'),                                              # 出现等级
#     'item': (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 给予物品
#     'sell_sort': ('sell_sort', 'int'),                                          # 售价类型
#     'sell_num': ('sell_num', 'int'),                                            # 售价
#     'sell_max': ('sell_max', 'int'),                                            # 限购数量
#     'weight': ('weight', 'int'),                                                # 出现权重
# }

# 血尘拉力赛 - 游骑兵黑市
# rally_shop = {
#     'uk': ('shop_id', 'int'),                        # 黑市商品ID
#     'show_lv': ('show_lv', 'int'),                   # 需要等级
#     'item': (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 物品
#     'sell_max': ('sell_max', 'int'),                 # 限购数量
#     'sell_sort': ('sell_sort', 'int'),               # 货币类型
#     'sell_num': ('sell_num', 'int'),                 # 价格
#     'weight': ('weight', 'int'),                     # 权重
# }
