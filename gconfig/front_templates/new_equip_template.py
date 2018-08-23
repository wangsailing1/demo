#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 装备相关的配置
from gconfig import check


# 装备详情
new_equip_detail = {
    'uk': ('equip_id', 'int'),              # 装备id
    'name': ('name', 'unicode'),            # 名称
    'awake_id': ('awake_id', 'int'),        # 觉醒可能更换id，若为空则只升星
    'animation': ('animation', 'str'),      # 装备动画
    'effect': ('effect', 'str'),            # 底板动画
    'icon': ('icon', 'str'),                # 装备icon图片
    'sort': ('sort', 'int'),                # 装备类型/位置
    'quality_new': ('quality_new', 'int'),  # 初始品质框颜色
    'awake_item': ('awake_item', 'int'),    # 觉醒专属道具编号
    'add_attr': (('add_attr1', 'add_attr2', 'add_attr3'), ('list_2', 'mult_dict_1')),   # 属性基础值
    'awake': (('awake1', 'awake2', 'awake3', 'awake4', 'awake5'), ('int_float_list_or_int_float', 'mult_dict_1')),  # 觉醒等级效果
}


# 升级、升品倍率、消耗
new_equip_grade = {
    'uk': ('id', 'int'),                    # id
    'lv': ('lv', 'int'),                    # 等级
    'special': ('special', 'int'),          # 是否为升品
    'rate': ('rate', 'float'),                # 升级倍率
    'lvlup_exp': ('lvlup_exp', 'int'),      # 升级所需经验
    'quality': ('quality', 'int'),          # 当前等级品质
    'sort_cost': (('sort1_cost', 'sort2_cost', 'sort3_cost', 'sort4_cost', 'sort5_cost', 'sort6_cost', 'sort7_cost'),
                  ('list_3', 'mult_dict_1')),   # 消耗
    'lv_max': ('lv_max', 'int'),            # 最大等级
}


# 觉醒倍率、消耗
new_equip_awake = {
    'uk': ('awake_id', 'int'),      # 觉醒星级数
    'rate': ('rate', 'float'),        # 提升倍率
    'sort_cost': (('sort1_cost', 'sort2_cost', 'sort3_cost', 'sort4_cost', 'sort5_cost', 'sort6_cost', 'sort7_cost'),
                  ('list_3', 'mult_dict_1')),   # 消耗
    'awake_item_num': ('awake_item_num', 'int'),    # 觉醒专属道具消耗数量
}
