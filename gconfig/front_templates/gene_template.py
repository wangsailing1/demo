#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 装备相关的配置
from gconfig import check

# 基因基础表
gene_basis = {
    'uk': ('id', 'int'),                # 基因id
    'name': ('name', 'unicode'),        # 基因名称
    'icon1': ('icon1', 'str'),          # 档次1图标
    'icon2': ('icon2', 'str'),          # 档次2图标
    'icon3': ('icon3', 'str'),          # 档次3图标
    'icon4': ('icon4', 'str'),          # 档次3图标
    'describe': ('describe', 'unicode'),    # 装备描述
    'sort': ('sort', 'int'),            # 类型
    'suit': ('suit', 'int'),            # 套装
    'star': ('star', 'int'),            # 初始星级
    'evo': ('evo', 'int'),              # 初始品阶
    'initial': ('initial', 'list_2'),   # 主要属性初始值
    'story': ('story', 'unicode'),      # 描述
    'story1': ('story1', 'unicode'),      # 描述
    'story2': ('story2', 'unicode'),      # 描述
    'story3': ('story3', 'unicode'),      # 描述
    'chain_show': ('chain_show', 'int_list'),   # 宿命
    'anim': ('anim', 'str'),
}


# 基因套装特效
gene_suit = {
    'uk': ('skill_id', 'int'),          # 属性id
    'suit_id': ('suit_id', 'int'),      # 套装id
    'suit_sort': ('suit_sort', 'int'),  # 二件套/四件套
    'name': ('name', 'unicode'),        # 套装名称
    'star': ('star', 'int'),            # 套装星级
    'icon': ('icon', 'str'),            # 图标
    'story': ('story', 'unicode'),      # 描述
    'suit_add': ('suit_add', 'list_2'), # 套装属性加成
    'buff_id': ('buff_id', 'int'),      # buff
}


# 基因随机属性库
gene_random = {
    'uk': ('random_id', 'int'),                                     # 随机属性id
    'random_sort': ('random_sort', 'int'),                          # 属性类型
    'weight': ('weight', 'int'),                                    # 权重
    'evo_limit': ('evo_limit', 'int'),                              # 品阶限制
    'random_range': ('random_range', 'list_3'),                     # 初始属性数值范围
    'random_range_rebuild': ('random_range_rebuild', 'list_3'),     # 洗练属性库
}


# 基因升级表
gene_lvlup = {
    'uk': ('lvl', 'int'),                # 基因等级
    'lvl_limit': ('lvl_limit', 'int_list'),   # 战队等级限制
    'lvl_rate': ('lvl_rate', 'int'),     # 基因成长系数
    'cost': ('cost', 'int'),        # 升级消耗
}


# 基因升星表
gene_starup = {
    'uk': ('star', 'int'),              # 基因星级
    'star_rate': ('star_rate', 'float'),  # 星级倍率
    'lvl_limit': ('lvl_limit', 'int'),  # 战队等级限制
    'cost': ('cost', 'int'),            # 升星花费
    'material': ('material', 'list_3'),    # 需要的材料数量
    'total_cost': ('total_cost', 'int'),    # 一键升星消耗
    'random_num': ('random_num', 'int'),    # 增加的附加属性空位
    'init_random_num': ('init_random_num', 'int'),    # 附加属性的空位
    'unlocked_num': ('unlocked_num', 'int'),    # 已经解锁生效的条目数
    're_material': ('re_material', 'list_3'),    # 分解可获得的装备碎片数
    'icon': ('icon', 'str'),
    'evo_re_material': (('evo1_re_material', 'evo2_re_material', 'evo3_re_material', 'evo4_re_material', 'evo5_re_material', 'evo6_re_material'), ('list_3', 'mult_dict_1')),    # 分解可获得的装备碎片数
}


# 基因进阶表
gene_evoup = {
    'uk': ('evo', 'int'),               # 品阶数
    'evo_rate': ('evo_rate', 'float'),    # 品阶倍数
    'lvl_limit': ('lvl_limit', 'int'),  # 战队等级限制
    'cost': ('cost', 'list_3'),         # 进阶消耗
    'baserate': (('baserate1', 'baserate2', 'baserate3', 'baserate4', 'baserate5', 'baserate6'), ('float', 'mult_dict_1')), # 基础属性上升倍率
    'lockrate': (('lockrate1', 'lockrate2', 'lockrate3', 'lockrate4', 'lockrate5', 'lockrate6'), ('float', 'mult_dict_1')), # 解锁属性上升倍率
}


piece_equip = {
    'uk': ('id', 'int'),    # 碎片id
    'num': ('num', 'int'),  # 合成需要数量
    'equip_id': ('equip_id', 'int'),    # 合成目标，special_use_item表
    'name': ('name', 'unicode'),
    'story': ('story', 'unicode'),
    'icon': ('icon', 'str'),
}
