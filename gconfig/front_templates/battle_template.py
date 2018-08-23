#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 战斗相关的配置, 暂时给前端使用
from gconfig import check


# 暴击等级压制表
crit_atk_suppress = {
    'uk': ('id', 'int'),  # 分段编号
    'lvl_low_limit': ('lvl_low_limit', 'int'),  # 等级差下限
    'lvl_high_limit': ('lvl_high_limit', 'int'),  # 等级差上限
    'suppress': ('suppress', 'float'),  # 压制百分比
}


# 抗暴等级压制表
crit_def_suppress = {
    'uk': ('id', 'int'),  # 分段编号
    'lvl_low_limit': ('lvl_low_limit', 'int'),  # 等级差下限
    'lvl_high_limit': ('lvl_high_limit', 'int'),  # 等级差上限
    'suppress': ('suppress', 'float'),  # 压制百分比
}


# 伤害等级压制表
damage_suppress = {
    'uk': ('id', 'int'),  # 分段编号
    'lvl_low_limit': ('lvl_low_limit', 'int'),  # 等级差下限
    'lvl_high_limit': ('lvl_high_limit', 'int'),  # 等级差上限
    'suppress': ('suppress', 'float'),  # 压制百分比
}


# 闪避等级压制表
dodge_suppress = {
    'uk': ('id', 'int'),  # 分段编号
    'lvl_low_limit': ('lvl_low_limit', 'int'),  # 等级差下限
    'lvl_high_limit': ('lvl_high_limit', 'int'),  # 等级差上限
    'suppress': ('suppress', 'float'),  # 压制百分比
}


# 命中等级压制表
hit_suppress = {
    'uk': ('id', 'int'),  # 分段编号
    'lvl_low_limit': ('lvl_low_limit', 'int'),  # 等级差下限
    'lvl_high_limit': ('lvl_high_limit', 'int'),  # 等级差上限
    'suppress': ('suppress', 'float'),  # 压制百分比
}

# 战斗用计算公式用到的系数配置
fight = {
    'uk': ('lvl', 'int'),   # 被攻击英雄lv
    'k': ('k', 'float'),    # 系数k
    'a': ('a', 'float'),    # 系数a
    'b': ('b', 'float'),    # 系数b
}

# 援护技能升级消耗
protect_skill_cost = {
    'uk': ('id', 'int'),     # 援护技能等级
    'upgrade_cost': ('upgrade_cost', 'list_3'),  # 升级所需物品（特殊道具）
    'upgrade_herochipnum': ('upgrade_herochipnum', 'int'),      # 升级所需物品（该英雄碎片数量）
    'upgrade_gold': ('upgrade_gold', 'list_3'),    # 升级所需金币
}

# 援护技能配置
protect_skill_detail = {
    'uk': ('id', 'int'),                                # 技能ID
    'sort': ('sort', 'int'),                            # 子id
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
    'npc': ('npc', 'int'),                              # 召唤物id
    'effect_value': ('effect_value', 'int'),            # 技能取值
    'effect': ('effect', 'int'),                        # 技能数值（100%）
    'mag_effect_value': ('mag_effect_value', 'int'),    # 技能数值（100%）
    'mag_effect': ('mag_effect', 'int'),                # 技能数值（100%）
    'skill_ext': ('skill_ext', 'int_list'),
    'story': ('story', 'unicode'),                      # 技能描述
    'show_lvl': ('show_lvl', 'unicode'),                # 技能等级
    'if_use': ('if_use', 'int'),
    'voice': ('voice', 'str_list'),                     # 技能喊话
    'key': ('key', 'str'),                              # 立绘偏移量
    'type': ('type', 'int'),                            # 技能性质
    'tips': ('tips', 'unicode'),                        # 玩家点击问号弹出的注释
    'protect_detail': ('protect_detail', 'unicode'),    # 觉醒增强属性的描述
    'time': ('time', 'int'),                            # 每场战斗可使用次数
    'team_attribute': ('team_attribute', 'float'),      # 团队属性加成
    'skill_effect_sort': ('skill_effect_sort', 'int'),  # 技能性质
}

# 援护技能升级消耗
protect_skill_attr_rate = {
    'uk': ('id', 'int'),     # 援护位置
    'sort': ('sort', 'float'),  # 该位置增加团队属性
}
