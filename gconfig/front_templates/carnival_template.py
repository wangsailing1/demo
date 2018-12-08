#! --*-- coding: utf-8 --*--


carnival_mission = {
    'uk': ('id', 'int'),  # 任务ID
    'describe': ('describe', 'str'),  # 描述
    'sort': ('sort', 'int'),  # 类型
    'target': (('target1', 'target2', 'target3','target4','target5',), ('int_list_or_int2', 'mult_force_num_list')),
    'reward': ('reward', 'int'),  # 奖励骰子数量
    'jump': ('jump', 'int'),  # 跳转
    'if_reuse': ('if_reuse', 'int'),  # 可否重复完成
    'days_new': ('days_new', 'int'),  # 新服嘉年华天数
    'days_old': ('days_old', 'int'),  # 普通嘉年华天数
}


carnival_new_reward = {
    'uk': ('id', 'int'),  # 格子id
    'num': ('num', 'int'),  # 描述
    'icon': ('icon', 'str'),  # 类型
    'reward': ('reward', 'int_list'),  # 奖励
    'unlock_day': ('unlock_day', 'int'),  # 跳转
}

carnival_old_reward = {
    'uk': ('id', 'int'),  # 格子id
    'num': ('num', 'int'),  # 描述
    'icon': ('icon', 'str'),  # 类型
    'reward': ('reward', 'int_list'),  # 奖励
    'unlock_day': ('unlock_day', 'int'),  # 跳转
}

carnival_days = {
    'uk': ('id', 'int'),  # ID
    'time_format': ('time_format', 'int'),  # 时间格式，1是新服嘉年华，2是普通嘉年华
    'open': ('open', 'str'),  # 开启时间
    'close': ('close', 'str'),  # 结束时间
}

carnival_random = {
    'uk': ('id', 'int'),  # 色子id
    'ratio': ('ratio', 'int'),  # 色子概率
}