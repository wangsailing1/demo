#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

# 七日盛典主表
sevenday = {
    'uk': ('id', 'int'),    # 七日盛典第几天
    'act_name': (('act1_name', 'act2_name', 'act3_name', 'act4_name', 'act5_name'), ('unicode', 'mult_dict_1')),  # 1,2,3活动页签名
    'act_id': (('act1_id', 'act2_id', 'act3_id', 'act4_id', 'act5_id'), ('int_list', 'mult_dict_1')),         # 1,2,3活动对应目标信息表中的id序列
    'reward_show': ('reward_show', 'list_3'),
}


# 七日盛典目标信息表
sevenday_info = {
    'uk': ('id', 'int'),                        # 目标的id
    'sort': ('sort', 'int'),                    # 目标的类型
    'condition1': ('condition1', 'int'),        # 目标条件1
    'condition2': ('condition2', 'int'),        # 目标条件2
    'is_count': ('is_count', 'int'),            # 是否显示计数器
    'reward': ('reward', 'list_3'),             # 该目标达成后的奖励
    'des': ('des', 'unicode'),                  # 该目标的描述文字
    'jump': ('jump', 'int'),
}


# 七日盛典抢购信息表
sevenday_shop = {
    'uk': ('id', 'int'),                    # 序号
    'reward': ('reward', 'list_3'),         # 购买的物品
    'name': ('name', 'unicode'),            # 物品名称展示
    'price_off': ('price_off', 'int'),      # 原价
    'price_real': ('price_real', 'int'),    # 现价
    # 'total_num': ('total_num', 'int'),      # 全服限购数量
}

