# -*- coding: utf-8 -*-

"""
Create on 2019-02-15

@author: cj
"""

card_skill_unlock = {
    'uk': ('id', 'int'),  # id
    'lv': ('lv', 'int'),  # 解锁需要艺人等级
}

card_skill_level = {
    'uk': ('skill_level', 'int'),  # 技能等级
    'exp': (('exp1', 'exp2', 'exp3', 'exp4', 'exp5', 'exp6',), ('int', 'mult_force_num_list')),  # 不同技能品质所需技能经验
}

card_skill = {
    'uk': ('id', 'int'),  # 技能id
    'name': ('name', 'str'),  # 技能名称
    'des': ('des', 'str'),  # 技能描述
    'quality': ('quality', 'int'),  # 技能品质
    'triggersystem': ('triggersystem', 'int'),  # 触发系统
    'triggercondition': ('triggercondition', 'int_list'),  # 技能触发条件
    'triggercondition_logic': ('triggercondition_logic', 'int'),  # 技能触发条件逻辑
    'skilltype': ('skilltype', 'int'),  # 技能效果类型
    'skilltarget_type': ('skilltarget_type', 'int'),  # 技能受众类型
    'skilltarget_id': ('skilltarget_id', 'int_list'),  # 技能受众id
    'computing_method': ('computing_method', 'int'),  # 效果计算方式
    'skilllevel_value': ('skilllevel_value', 'int_list'),  # 技能各级效果数值
}
