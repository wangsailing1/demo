#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 道具相关的配置
from gconfig import check


# 战斗道具释放配置
battle_item_skill = {
    'uk': ('id', 'int'),  # 技能id
    'name': ('name', 'unicode'),  # 名字
    'cost': ('cost', 'int'),  # 消耗能量
    'icon': ('icon', 'str'),  # 图标
    'key': ('key', 'str_list'),  # 作用关键字, 前端变量
    'value': ('value', 'int_list'),  # 作用关键值, 前端变量
    'ready_time': ('ready_time', 'float'),  # 前摇时间
    'special_effects_hero1': ('special_effects_hero1', 'str'),  # 施法人特效
    'special_effects_skill': ('special_effects_skill', 'str'),  # 技能特效
    'special_effects_hero2': ('special_effects_hero2', 'str'),  # 被攻击特效
    'special_effects_skill_down': ('special_effects_skill_down', 'str'),  # 飞行特效(人下面)
    'continuous_effect_up': ('continuous_effect_up', 'str'),  # 持续特效(人上面)
    'continuous_effect_down': ('continuous_effect_down', 'str'),  # 持续特效(人下面)
    'effects_hero2_num': ('effects_hero2_num', 'int'),  # 被攻击特效播放个数
    'special_effects_skill_time': ('special_effects_skill_time', 'float'),  # 被攻击动画保留时间
    'sign': ('sign', 'str'),  # 施法区域标记
    'sign_enemy': ('sign_enemy', 'str'),  # 施法区域标记（敌方）
    'npc_id': ('npc_id', 'int'),  # 召唤英雄id
    'npc_lvl': ('npc_lvl', 'int'),      # 召唤英雄等级
    'cd': ('cd', 'float'),  # CD
    'skill_type': ('skill_type', 'int'),  # 技能类型
    'target': ('target', 'int'),  # 目标
    'radius': ('radius', 'float'),  # 半径
    'add_buff': ('add_buff', 'int'),  # 特效类型
    'buff_pro': ('buff_pro', 'int'),  # 特效概率
    'buff_effect': ('buff_effect', 'int'),  # buff每秒恢复/dot数值
    'buff_time': ('buff_time', 'int'),  # 特效保留时间
    'skill_effect': ('skill_effect', 'float'),  # 技能效果基础数值
    'ext_sign': ('ext_sign', 'str'),  # 额外动画播放(己方)
    'ext_sign_enemy': ('ext_sign_enemy', 'str'),  # 额外动画播放(敌方)
    'ext_sign_pos': ('ext_sign_pos', 'int'),  # 额外动画位置(不填跟随, 填固定)
    'story': ('story', 'unicode'),      # 道具说明
}


# 战斗道具属性表
# battle_item_pro = {
#     'uk': ('id', 'int'),                              # 道具id
#     'name': ('name', 'unicode'),                      # 道具名称
#     'icon': ('icon', 'str'),                          # 图标
#     'life': ('life', 'int_float_str'),                # 生命值
#     'life_fall': ('life_fall', 'int_float_str'),      # 生命衰减
#     'damage': ('damage', 'int_float_str'),            # 伤害
#     'atk_speed': ('atk_speed', 'int_float_str'),      # 攻击速度
#     'damage_type': ('damage_type', 'int_float_str'),  # 伤害类型
#     'range': ('range', 'int_float_str'),              # 攻击距离
#     'object': ('object', 'int_float_str'),            # 作用对象
#     'radius': ('radius', 'int_float_str'),            # 作用范围
#     'buff_time': ('buff_time', 'int_float_str'),      # 持续时间
#     'treat': ('treat', 'unicode'),                    # 治疗效果
#     'effect_lvl': ('effect_lvl', 'int_float_str'),    # 最大作用等级
#     'story': ('story', 'unicode'),                    # 技能说明
#     'cost': ('cost', 'int_float_str'),                # 费用
# }



# 对应点数
battle_item_layer = {
    'uk': ('layer', 'int'),         # 层级
    'quality': ('quality', 'int'),  # 对应品阶
    'ring': (('ring1', 'ring2', 'ring3'), ('int', 'mult_dict_1')),      # 1环结点数, 2环结点数, 3环结点数
}


# 战斗道具属性库
battle_item_bank = ({
    'uk': ('id', 'int'),                # 库id
    'layer': ('layer', 'int'),          # 所在层级
    'quality': ('quality', 'int'),      # 对应品阶
    'item_id': ('item_id', 'int'),      # 道具id
    'sort': ('sort', 'int'),            # 属性类型
    'value1': (('value11', 'value12'), ('float', 'mult_list')),    # 一环[数值1, 数值2]
    'value2': (('value21', 'value22'), ('float', 'mult_list')),    # 二环[数值1, 数值2]
    'value3': (('value31', 'value32'), ('float', 'mult_list')),    # 三环[数值1, 数值2]
    'cost': (('cost1', 'cost2', 'cost3'), ('int_list', 'mult_dict_1')),    # 激活花费
}, 'battle_item_bank')


# 战斗道具属性上限
battle_item_limit = ({
    'uk': ('item_id', 'int'),                   # 道具id
    'quality': ('quality', 'int'),              # 对应品阶
    'sort': ('sort', 'int'),                    # 属性类型
    'quality_item': ('quality_item', 'float'),  # 该品阶限制值
}, 'battle_item_limit')


# 对立道具和亲近道具
battle_item_oppo = {
    'uk': ('ID', 'int'),                   # 道具id
    'oppo_id': ('oppo_id', 'int_list'),    # 对立id库
    'match_id': ('match_id', 'int_list'),  # 亲近id库
}


# 解锁道具表
add_battle_item = ({
    'uk': ('layer', 'int'),                   # 层数
    'ring': ('ring', 'int'),                  # 环数
    'battle_id': ('battle_id', 'int'),        # 道具id
    'cost': ('cost', 'int_list'),    # 激活花费
}, 'add_battle_item')
