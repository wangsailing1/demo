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
    'target': (('target1', 'target2', 'target3', 'target4', 'target5'), ('int_list_or_int2', 'mult_force_num_list')),  # 目标
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
    'target': (('target1', 'target2', 'target3', 'target4', 'target5'), ('int_list_or_int2', 'mult_force_num_list')),  # 目标
    'reward': ('reward', 'int_list'),  # 奖励
    'jump': ('jump', 'int_list'),  # 跳转
    'weight': ('weight', 'int'),  # 权重
    'unlock_lvl': ('unlock_lvl', 'int'),  # 解锁等级
    'name': ('name', 'str'),  # 名字
}

# 成就任务
achieve_mission = {
    'uk': ('id', 'int'),
    'mission_name': ('mission_name', 'str'),  # 任务名
    'describe': ('describe', 'str'),  # 描述
    'group': ('group', 'int'),  # 任务组
    'next_id': ('next_id', 'int'),  # 下个任务
    'sort': ('sort', 'int'),  # 类型
    'target': (('target1', 'target2', 'target3', 'target4', 'target5'), ('int_list_or_int2', 'mult_force_num_list')),  # 目标
    'reward': ('reward', 'int_list'),  # 奖励
    'achieve_point': ('achieve_point', 'int'),  # 成就点
    'jump': ('jump', 'int_list'),  # 跳转
    'unlock_lvl': ('unlock_lvl', 'int'),  # 解锁等级
}
