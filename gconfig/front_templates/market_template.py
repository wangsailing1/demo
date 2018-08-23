#! --*-- coding: utf-8 --*--

__author__ = 'sm'


# 采集相关的配置
from gconfig import check


# 集市
market = {
    'uk': ('id', 'int'),  # ID
    'name': ('name', 'unicode'),  # 名称
    'quality': ('quality', 'int'),  # 品阶(颜色)
    'base_price': ('base_price', 'int'),  # 初始定价
    'type': ('type', 'int'),  # 商品类型
    'in_shop': ('in_shop', 'int'),  # 是否出售
    'treasure': ('treasure', 'int'),  # 是否珍品
    'treasure_base_limit': ('treasure_base_limit', 'int'),  # 装备珍品基础属性及格线
    'treasure_random_limit': ('treasure_random_limit', 'int'),  # 装备珍品附加属性及格线
    'rate': ('rate', 'int'),  # 税率
    'booth_fee': (('booth_fee_1day', 'booth_fee_2day', 'booth_fee_3day'), ('int', 'mult_dict_1')),  # 1,2,3天摊位费
    'cd': ('cd', 'int'),  # 冷冻期时长（h）
    'down_limit': ('down_limit', 'int'),  # 定价下限百分比
    'up_limit': ('up_limit', 'int'),  # 定价上限百分比
    'heart': ('heart', 'int'),  # 关注一次桃心占比
}


# 集市筛选分类
market_type = {
    'uk': ('id', 'int'),  # id
    'type': ('type', 'int'),  # 筛选名称
    'name': ('name', 'unicode'),  # 筛选名称
    'icon': ('icon', 'unicode'),  # 筛选图标
    'treasure': ('treasure', 'int'),  # 是否在珍品里显示
    'sort': ('sort', 'int'),  # 装备部位
    'job': ('job', 'int'),  # 装备职业
}
