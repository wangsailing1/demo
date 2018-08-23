#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 暂时给前端使用
from gconfig import check


# 统率
commander = {
    'uk': ('id', 'int'),            # 统率id
    'name': ('name', 'unicode'),    # 统率名称
    'icon': ('icon', 'str'),        # 图标
    'lvl': ('lvl', 'int'),          # 初始等级
    'exp': ('exp', 'int'),          # 初始经验
    'story': ('story', 'unicode'),  # 属性描述
}

# 统帅碎片
commander_part = {
    'uk': ('part_id', 'int'),     # 碎片id
    'name': ('name', 'unicode'),  # 碎片名称
    'icon': ('icon', 'str'),        # 图标
    'recipe': ('recipe', 'int'),  # 所属配方
    'des': ('des', 'unicode'),    # 描述
}


# 统帅属性
commander_type = {
    'uk': ('level', 'int'),     # 统帅等级
    'exp': ('exp', 'int'),              # 经验
    'hp': ('hp', 'float'),        # 增加生命
    'phy_atk': ('phy_atk', 'float'),    # 增加物攻
    'phy_def': ('phy_def', 'float'),    # 增加物防
    'mag_atk': ('mag_atk', 'float'),    # 增加魔攻
    'mag_def': ('mag_def', 'float'),    # 增加魔防
}


# 统帅配方
commander_recipe = {
    'uk': ('recipe_ID', 'int'),                 # 配方ID
    'name': ('name', 'unicode'),                # 名称
    'part': ('part', 'int_list'),               # 碎片
    'rate1': ('rate1', 'int'),                  # 简单概率
    'rate2': ('rate2', 'int'),                  # 普通概率
    'rate3': ('rate3', 'int'),                  # 困难概率
    'exp': ('exp', 'int'),                      # 增加经验
    'sort': ('sort', 'int'),                    # 属性类型
    'is_show': ('is_show', 'int'),              # 是否展示
    'icon': ('icon', 'str'),                    # 图标
    'quality': ('quality', 'int'),              # 品质
    # 'rate_win': (('rate_easy', 'rate_nomal', 'rate_hard'), ('int', 'mult_dict_1')),   # 胜利概率(简单,正常,困难)
}


# 统帅合成额外奖励库
# commander_reward = {
#     'uk': ('id', 'int'),                # 奖励id
#     'des': ('des', 'unicode'),          # 描述
#     'use_lvl': ('use_lvl', 'int'),      # 战队等级限制
#     'reward': ('reward', 'list_3'),     # 奖励
#     'weight': ('weight', 'int'),        # 出现权重
# }
