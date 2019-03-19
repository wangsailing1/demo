# -*- coding: utf-8 –*-

egg_item = {
    'uk': ('version', 'int'),  # 版本
    'start_time': ('start_time', 'str'),  # 起始时间
    'end_time': ('end_time', 'str'),  # 结束时间
    'type': ('type', 'int'),  # 活动类型
    'need_sort': ('need_sort', 'int'),  # 花费项目
    'need_recharge': ('need_recharge', 'int'),  # 花费量
    'number': ('number', 'int'),  # 数量
    'reward_1': ('reward_1', 'int_list'),  # 奖池1
    'reward_2': ('reward_2', 'int_list'),  # 奖池2
    'reward_3': ('reward_3', 'int_list'),  # 奖池3
    'reward_chance': ('reward_chance', 'int_list'),  # 随机权重
    'refresh_price': ('refresh_price', 'int'),  # 刷新花费钻石
    'notice': ('notice', 'int'),  # 说明
    'best_reward': ('best_reward', 'int_list'),  # 最好奖励
}

egg_diamond = {
    'uk': ('version', 'int'),  # 版本
    'type': ('type', 'int'),  # 活动类型
    'need_sort': ('need_sort', 'int'),  # 花费项目
    'need_recharge': ('need_recharge', 'int'),  # 花费项目
    'super_item_higher': ('super_item_higher', 'int_list'),  # 大奖
    'number': ('number', 'int'),  # 数量
    'reward_1': ('reward_1', 'int_list'),  # 奖池1
    'reward_2': ('reward_2', 'int_list'),  # 奖池2
    'reward_3': ('reward_3', 'int_list'),  # 奖池3
    'reward_chance': ('reward_chance', 'int_list'),  # 随机权重
    'refresh_price': ('refresh_price', 'int'),  # 刷新花费钻石
    'notice': ('notice', 'int'),  # 说明
    'best_reward': ('best_reward', 'int_list'),  # 最好奖励
}