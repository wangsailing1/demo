#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 采集相关的配置
from gconfig import check


# 生产表
manufacture = {
    'uk': ('id', 'int'),                    # 产物ID
    'name': ('name', 'unicode'),            # 名字
    'random': ('random', 'int'),            # 随机
    'sort': ('sort', 'int'),                # 类型
    'job': ('job', 'int'),                  # 生产所需JOB
    'value': ('value', 'int'),              # 需要生产能力
    'evolution': ('evolution', 'int'),      # 需求品质
    'grade': ('grade', 'int'),              # 档次
    'lvl_unlock': ('lvl_unlock', 'int'),    # 解锁等级
    'material': (('material1', 'num1',      # 生产需要的材料和数量
                  'material2', 'num2',
                  'material3', 'num3',
                  'material4', 'num4',
                  'material5', 'num5',), ('int', 'list_2_to_list')),
    'get_num': ('get_num', 'int'),          # 获取数量
    'equip_id': ('equip_id', 'int'),       # 获得物品
    'quality': (('quality', 'quality1', 'quality2', 'quality3', 'quality4'),
                ('list_2', 'mult_dict_0')),  # 品质,颜色,使用0-4个材料库
}


# 生产英雄体力与能力计算
manufacture_weary = ({
    'uk': ('weary', 'int'),  # 体力
    'percent': ('percent', 'int'),  # 采集能力100%
}, 'manufacture_weary')


# 生产星级决定提升下限百分比
# manufacture_star = {
#     'uk': ('star', 'int'),  # 星星数量
#     'percent': ('percent', 'float'),  # 提升下限百分比
# }


# 生产精石
manufacture_stone = {
    'uk': ('id', 'int'),                                # 配方id
    'combination': ('combination', 'list_2'),           # 稀有资源组合
    'extra_attribute': ('extra_attribute', 'list_2'),   # 额外附加属性
}


# 采集生产随机经验块
# collection_manufacture = {
#     'uk': ('id', 'int'),                # id
#     'sort': ('sort', 'int'),            # 类型, 1:采集, 2:生产
#     'time': ('time', 'int'),            # 花费时间(h)
#     'reward': ('reward', 'list_4'),     # 奖励
# }
