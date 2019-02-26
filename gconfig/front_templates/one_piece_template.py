#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

# 藏宝图配置
from gconfig import check


# 藏宝图
one_piece = {
    'uk': ('version', 'int'),              # 活动编号
    'id': ('id', 'int'),            # 编号
    'free_reward': ('free_reward', 'int_list'),        # 免费探索奖励
    'animation': ('animation', 'str'),      # 装备动画
    'one_coin': ('one_coin', 'int'),            # 单次消耗钻石
    'icon': ('icon', 'str'),                # 装备icon图片
    'sort': ('sort', 'int'),                # 装备类型/位置
    'quality_new': ('quality_new', 'int'),  # 初始品质框颜色
    'awake_item': ('awake_item', 'int'),    # 觉醒专属道具编号
    'add_attr': (('add_attr1', 'add_attr2', 'add_attr3'), ('list_2', 'mult_dict_1')),   # 属性基础值
    'awake': (('awake1', 'awake2', 'awake3', 'awake4', 'awake5'), ('int_float_list_or_int_float', 'mult_dict_1')),  # 觉醒等级效果
}