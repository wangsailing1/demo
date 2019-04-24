# -*- coding: utf-8 –*-

# 合作任务
strategy_mission = {
    'uk':               ('id',              'int'),                 # id
    'name':             ('name',            'int'),                 # 任务名称
    'describe':         ('describe',        'int'),                 # 描述
    'sort':             ('sort',            'int'),                 # 类型
    # 'target1':          ('target1',         'int'),                 # 目标1
    'target2':          ('target2',         'int'),                 # 目标2
    # 'target3':          ('target3',         'int'),                 # 目标3
    # 'target4':          ('target4',         'int'),                 # 目标4
    # 'target5':          ('target5',         'int'),                 # 目标5
    'target': (('target1', 'target2', 'target3','target4','target5',), ('int_list_or_int2', 'mult_force_num_list')),
    'reward':           ('reward',          'int_list'),            # 奖励
    'reward_a':         ('reward_a',        'float'),               # 奖励参数a
    'reward_b':         ('reward_b',        'float'),               # 奖励参数b
    'jump':             ('jump',            'int_list'),            # 跳转
    'weight':           ('weight',          'int'),                 # 权重
    'unlock_lvl':       ('unlock_lvl',      'int'),                 # 解锁等级
}


# 任务类别
strategy_gift = {
    'uk':               ('id',              'int'),                 # id
    'kind':             ('kind',            'int'),                 # 类别
    'me_spend':         ('me_spend',        'int_list'),            # 送礼花费
    'partner_street':   ('partner_street',  'int'),                 # 对方街区等级
    'partner_get':      ('partner_get',     'int_list'),            # 对方可得
}


# 任务合作等级
strategy_lv = {
    'uk':               ('level',           'int'),                 # 合作等级
    'mission_amount':   ('mission_amount',  'int'),                 # 升级所需任务数量
    'friendly':         ('friendly',        'int'),                 # 默契值
    'level_gift':       ('level_gift',      'int_list'),            # 礼包物品
}


# 任务类别
strategy_once = {
    'uk':               ('id',              'int'),                 # id
    'friendly_blank':   ('friendly_blank',  'int_list'),            # 默契值
    'big_level':        ('big_level',       'int'),                 # 最高等级
}