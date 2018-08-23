#! --*-- coding: utf-8 --*--

# 英雄相关的配置
from gconfig import check


# 主角基础数据表
main_hero = {
    'uk': ('main_hero_id', 'int'),                      # 主角id
    'act': ('act', 'str'),                              # 动画
    'icon': ('icon', 'str'),                            # 头像
    'icon_fight': ('icon_fight', 'str'),                # 战斗用头像
    'art': ('art', 'str'),                              # 原画
    'icon_arena': ('icon_arena', 'str'),                # 半身像
    'icon_arena2': ('icon_arena2', 'str'),              # 战前半身像
    'icon_arena3': ('icon_arena3', 'str'),              # 英雄背包半身像
    'painting': ('painting', 'str'),                    # 立绘
    'offset': ('offset', 'int_list'),                   # 立绘偏移值
    'show_skill': ('show_skill', 'int'),                # 获得英雄显示技能
    'show_skill_des': ('show_skill_des', 'unicode'),    # 牛逼的技能描述
    'skill1_id': ('skill1_id', 'int'),                  # 技能1
    'value_rate': ('value_rate', 'float'),              # 属性转化率
    'basic_attr': ('basic_attr', 'list_2'),             # 基础属性值
    'sound': ('sound', 'str'),                          # 详情语音
    'value_rate_add': ('value_rate_add', 'int_list'),   # 进阶转化率增加
    'sex': ('sex', 'int'),                              # 性别
    'unlock': ('unlock', 'int_float_list_or_int_float'),    # 解锁消耗
    'unlock_type': ('unlock_type', 'int'),              # 解锁类型
}


# 主角进阶表
main_hero_evo = {
    'uk': ('hero_id', 'int'),                           # 主角id
    'evo_1_cost': ('evo_1_cost', 'list_3'),             # evo1花费
    'evo_2_cost': ('evo_2_cost', 'list_3'),             # evo2花费
    'evo_3_cost': ('evo_3_cost', 'list_3'),             # evo3花费
    'evo_4_cost': ('evo_4_cost', 'list_3'),             # evo4花费
    'evo_5_cost': ('evo_5_cost', 'list_3'),             # evo5花费
    'evo_1_rate': ('evo_1_rate', 'float'),              # evo属性倍率
    'evo_2_rate': ('evo_2_rate', 'float'),              # evo属性倍率
    'evo_3_rate': ('evo_3_rate', 'float'),              # evo属性倍率
    'evo_4_rate': ('evo_4_rate', 'float'),              # evo属性倍率
    'evo_5_rate': ('evo_5_rate', 'float'),              # evo属性倍率
    'evo_6_rate': ('evo_6_rate', 'float'),              # evo属性倍率
}


# 主角基因基础属性表表
main_hero_medal = {
    'uk': ('medal_id', 'int'),                          # id
    'name': ('name', 'unicode'),                        # 名字
    'icon': ('icon', 'str'),                            # icon
    'sort': ('sort', 'int'),                            # sort
    'add_attr1': ('add_attr1', 'list_2'),               # 属性1
    'add_attr2': ('add_attr2', 'list_2'),               # 属性2
    'add_attr3': ('add_attr3', 'list_2'),               # 属性3
}


# 主角基因升级表
main_hero_medal_evo = {
    'uk': ('id', 'int'),                                # id
    'lv': ('lv', 'int'),                                # lv
    'lv_max': ('lv_max', 'int'),                        # 显示lv
    'special': ('special', 'int'),                      # 下级是否进阶
    'rate': ('rate', 'float'),                          # 属性倍率
    'quality': ('quality', 'int'),                      # 品质
    'sort_cost': ('sort_cost', 'list_3'),               # 升级或进阶花费
}


# 技能合成表
main_hero_skill_combine = {
    'uk': ('skill_lv', 'int'),                           # id
    'combine_num': ('combine_num', 'int'),               # 合成所需数量
    'combine_skill': ('combine_skill', 'int_list'),      # 合成技能库
}


# 主角技能表
main_hero_skill = {
    'uk': ('id', 'int'),                                # 技能ID
    'sort': ('sort', 'int'),                            # 子id
    'is_machine': ('is_machine', 'int'),                # 是否是坐骑技能
    'lv': ('lv', 'int'),                                # 技能等级
    'name': ('name', 'unicode'),                        # 技能名称
    'icon': ('icon', 'str'),                            # 技能图标
    'story_detail': ('story_detail', 'unicode'),        # 技能详细描述
    'script': ('script', 'str'),                        # 技能详细描述
    'skill_type': ('skill_type', 'int'),                # 技能类型
    'trigger': ('trigger', 'int'),                      # 技能触发类型
    'trigger_pro': ('trigger_pro', 'int'),              # 技能触发概率（如果有触发类型，必填）
    'trigger_data': ('trigger_data', 'int'),            # 技能触发概率（如果有触发类型，必填）
    'hit': ('hit', 'int'),                              # 是否享受效果命中
    'cost': ('cost', 'int'),                            # 消耗能量
    'cost_hp': ('cost_hp', 'int'),                      # 消耗生命（100%）
    'per_cd': ('per_cd', 'int'),                        # 冷却回合
    'cd': ('cd', 'int'),                                # 冷却回合
    'target': ('target', 'int'),                        # 目标类型
    'effect_sort': ('effect_sort', 'int'),              # 技能种类
    'add_buff': ('add_buff', 'int_list'),               # 技能附带BUFF
    'effect_value': ('effect_value', 'int'),            # 技能取值
    'effect': ('effect', 'int'),                        # 技能数值（100%）
    'mag_effect_value': ('mag_effect_value', 'int'),    # 技能数值（100%）
    'mag_effect': ('mag_effect', 'int'),                # 技能数值（100%）
    'story': ('story', 'unicode'),                      # 技能描述
    'show_lvl': ('show_lvl', 'unicode'),                # 技能等级
    'if_use': ('if_use', 'int'),
    'voice': ('voice', 'str_list'),                     # 技能喊话
    'key': ('key', 'str'),                              # 立绘偏移量
    'type': ('type', 'int'),                            # 技能性质
    'tips': ('tips', 'unicode'),                        # 玩家点击问号弹出的注释
    'protect_detail': ('protect_detail', 'unicode'),    # 觉醒增强属性的描述
    'time': ('time', 'int'),                            # 每场战斗可使用次数
    'jump': ('jump', 'int_list'),
    'unlock_id': ('unlock_id', 'int_list'),
    'from': ('from', 'unicode_list'),
    'script_play': ('script_play', 'int'),
}


# 主角里程碑
main_hero_medal_milestone = {
    'uk': ('evo_lv', 'int'),                            # id
    'add_type': ('add_type', 'int'),                    # 类型
    'add_rate1': ('add_rate1', 'int'),               # 数值增加1
    'add_rate2': ('add_rate2', 'int'),                  # 数值增加2
}


# 载具
machine = {
    'uk': ('machine_id', 'int'),                        # 载具id
    'act': ('act', 'str'),                              # 动画
    'icon': ('icon', 'str'),                            # 头像
    'icon_fight': ('icon_fight', 'str'),                # 战斗用头像
    'art': ('art', 'str'),                              # 原画
    'icon_arena': ('icon_arena', 'str'),                # 半身像
    'icon_arena2': ('icon_arena2', 'str'),              # 战前半身像
    'icon_arena3': ('icon_arena3', 'str'),              # 英雄背包半身像
    'painting': ('painting', 'str'),                    # 立绘
    'offset': ('offset', 'int_list'),                   # 立绘偏移值
    'show_skill': ('show_skill', 'int'),                # 获得英雄显示技能
    'show_skill_des': ('show_skill_des', 'unicode'),    # 牛逼的技能描述
    'skill1_id': ('skill1_id', 'int'),                  # 技能1
    'value_rate': ('value_rate', 'float'),              # 属性转化率
    'basic_attr': ('basic_attr', 'list_2'),             # 基础属性值
    'sound': ('sound', 'str'),                          # 详情语音
    'value_rate_add': ('value_rate_add', 'int_list'),   # 进阶转化率增加
    'sex': ('sex', 'int'),                              # 性别
    'unlock_type': ('unlock_type', 'int'),                  # 解锁类型
    'unlock': ('unlock', 'int_float_list_or_int_float'),    # 解锁消耗
    'show_attr_des': ('show_attr_des', 'unicode'),
    'name': ('name', 'unicode'),
}
