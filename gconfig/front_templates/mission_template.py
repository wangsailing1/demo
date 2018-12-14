#! --*-- coding: utf-8 --*--


# 活跃度
liveness_reward = {
    'uk': ('id', 'int'),
    'need_liveness': ('need_liveness', 'int'),  # 所需活跃度
    'reward': ('reward', 'int_list'),  # 奖励
}

# 活跃度
liveness = {
    'uk': ('id', 'int'),
    'describe': ('describe', 'int'),  # 任务描述
    'liveness': ('liveness', 'int'),  # 活跃度
    'sort': ('sort', 'int'),  # 类型
    'target': (('target1', 'target2', 'target3',), ('int', 'mult_force_num_list')),  # 目标
    'reward': ('reward', 'int_list'),  # 奖励
    'jump': ('jump', 'int_list'),  # 跳转
    'unlock_level': ('unlock_level', 'int_list'),  # 解锁等级
}

# 档期任务
box_office = {
    'uk': ('id', 'int'),
    'describe': ('describe', 'int'),  # 任务描述
    'level': ('level', 'int'),  # 等级
    'sort': ('sort', 'int'),  # 类型
    'target1': ('target1', 'int'),  # 目标
    'reward': ('reward', 'int_list'),  # 奖励
    'next_id': ('next_id', 'int'),  # 下个任务
}

# 新手任务
guide_mission = {
    'uk': ('id', 'int'),
    'describe': ('describe', 'int'),  # 任务描述
    'sort': ('sort', 'int'),  # 类型
    'target': (('target1', 'target2', 'target3',), ('int', 'mult_force_num_list')),  # 目标
    'reward': ('reward', 'int_list'),  # 奖励
    'jump': ('jump', 'int_list'),  # 跳转
}

# 随机任务
random_mission = {
    'uk': ('id', 'int'),
    'describe': ('describe', 'int'),  # 任务描述
    'sort': ('sort', 'int'),  # 类型
    'target': (('target1', 'target2', 'target3',), ('int', 'mult_force_num_list')),  # 目标
    'reward': ('reward', 'int_list'),  # 奖励
    'jump': ('jump', 'int_list'),  # 跳转
    'weight': ('weight', 'int'),  # 解锁等级
    'name': ('name', 'str'),  # 名字
}
