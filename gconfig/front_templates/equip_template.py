#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 装备相关的配置
from gconfig import check


# 装备基础数据
equip_basis = {
    'uk': ('id', 'int'),                                                # 装备id
    'name': ('name', 'unicode'),                                        # 名字
    'icon': ('icon', 'str'),                                          # icon
    'grade': ('grade', 'int'),                                          # 档次
    'quality': (('quality1', 'quality2'), ('list_2', 'mult_dict_1')),   # 品质(颜色)(1: 正常获得, 2: 抽卡获得)
    'sort': ('sort', 'int'),                                            # 类型 装备位置：逆时针
    'suit': ('suit', 'int'),                                            # 套装
    'initial': (('initial_1', 'initial_2', 'initial_3', 'initial_4', 'initial_5', 'initial_6'),
                ('list_2', 'mult_dict_1')),                             # 主要属性初始值(1-6: 白绿蓝紫橙红)
    'story': ('story', 'unicode'),                                      # 装备描述
}


# 装备升级
equip_lvlup = {
    'uk': ('lvl', 'int'),               # 装备等级
    'rate': ('rate', 'int'),            # 装备成长系数
    'lvlup_exp': ('lvlup_exp', 'int'),  # 升到下一级需要经验
    'self_exp': ('self_exp', 'int'),    # 装备自身经验
}


# 装备属性随机库
equip_random = {
    'uk': ('random_id', 'int'),                     # 随机属性id
    'random_sort': ('random_sort', 'int'),          # 属性类型
    'weight': ('weight', 'int'),                    # 权重
    'quality': ('quality', 'int'),                  # 适用颜色
    'random_range': ('random_range', 'list_3'),     # 初始属性数值范围
    'random_range_rebuild': ('random_range_rebuild', 'list_3'),     # 洗练属性库
}


# 新版装备套装特效
equip_suit = {
    'uk': ('skill_id', 'int'),              # 属性id
    'suit_id': ('suit_id', 'int'),          # 套装id
    'suit_sort': ('suit_sort', 'int'),      # 二件套/四件套
    'name': ('name', 'unicode'),            # 套装名称
    'icon': ('icon', 'str'),                # 套装图标
    'story': ('story', 'unicode'),          # 属性描述
    'suit_add': ('suit_add', 'list_2'),     # 增加套装基础属性
    'trigger': ('trigger', 'int'),                          # 技能触发类型
    'trigger_num': ('trigger_num', 'int_list'),             # 技能触发条件
    'trigger_pro': ('trigger_pro', 'int'),                  # 技能触发概率
    'target': ('target', 'int'),                            # 目标类型
    'skill_effect_sort': ('skill_effect_sort', 'int'),      # 技能种类
    'skill_effect_value': ('skill_effect_value', 'int'),    # 技能取值
    'skill_effect': ('skill_effect', 'float'),              # 技能取值
}


# 装备品质(颜色)
equip_color = {
    'uk': ('quality', 'int'),                   # 品质(颜色)
    'lvlup_limit': ('lvlup_limit', 'int'),            # 强化次数
    'random_num': ('random_num', 'list_2'),     # 初始附加属性条数
}


# 装备档次表
equip_grade = {
    'uk': ('grade', 'int'),                 # 档次
    'lvl': ('lvl', 'list_3'),               # 等级范围([等级1, 等级2 ,权重])
    'wear_limit': ('wear_limit', 'int'),    # 穿戴等级限制
}


# 装备精炼
equip_refine = {
    'uk': ('lvl', 'int'),           # 精炼等级
    'rate': ('rate', 'int'),        # 加成系数
    'cost': ('cost', 'list_3'),     # 花费
}

