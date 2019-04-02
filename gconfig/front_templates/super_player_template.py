#! --*-- coding: utf-8 --*--

__author__ = 'ljm'



player = {
    'uk':           ('version', 'int'),          # 活动版本
    'recharge':     ('recharge', 'int'),    # 充值额度
    'consume':      ('consume', 'int'),     # 消费额度
    'donate':       ('donate', 'int'),      # 红包钻石
    'instruction':  ('instruction', 'str'), # 说明
}

play_redbag = {
    'uk':       ('id', 'int'),          # id
    'version':  ('version', 'int'),     # 活动版本
    'quantity': ('quantity', 'int'),    # 红包数量
    'donate':   ('donate', 'int'),      # 赠礼总额
    'min':      ('min', 'int'),         # 最小红包
    'max':      ('max', 'int'),         # 最大红包
}

play_shop = {
    'uk':           ('id', 'int'),              # id
    'version':      ('version', 'int'),         # 活动版本
    'reward':       ('reward', 'int_list'),     # 奖励
    'sort':         ('sort', 'int'),            # 类型
    'limit_type':   ('limit_type', 'int'),      # 限制类型
    'limit_num':    ('limit_num', 'int'),       # 限购数量
    'player_limit': ('player_limit', 'int'),    # 单个玩家限购次数
    'cost_coin':    ('cost_coin', 'int'),       # 钻石价格
    'time':         ('time', 'int'),            # 时间
}

play_rankreward = {
    'uk':           ('id', 'int'),                  # id
    'version':      ('version', 'int'),             # 版本编号
    'rank':         ('rank', 'int_list'),           # 排行
    'rank_reward':  ('rank_reward', 'int_list'),    # 奖励
}

play_points = {
    'uk':       ('id', 'int'),          # id
    'version':  ('version', 'int'),     # 版本编号
    'point':    ('point', 'int'),       # 购买次数
    'reward':   ('reward', 'int_list'), # 奖励
}


server_player = {
    'uk':           ('version', 'int'),          # 活动版本
    'recharge':     ('recharge', 'int'),    # 充值额度
    'consume':      ('consume', 'int'),     # 消费额度
    'donate':       ('donate', 'int'),      # 红包钻石
    'instruction':  ('instruction', 'str'), # 说明
}

server_play_redbag = {
    'uk':       ('id', 'int'),          # id
    'version':  ('version', 'int'),     # 活动版本
    'quantity': ('quantity', 'int'),    # 红包数量
    'donate':   ('donate', 'int'),      # 赠礼总额
    'min':      ('min', 'int'),         # 最小红包
    'max':      ('max', 'int'),         # 最大红包
}

server_play_shop = {
    'uk':           ('id', 'int'),              # id
    'version':      ('version', 'int'),         # 活动版本
    'reward':       ('reward', 'int_list'),     # 奖励
    'sort':         ('sort', 'int'),            # 类型
    'limit_type':   ('limit_type', 'int'),      # 限制类型
    'limit_num':    ('limit_num', 'int'),       # 限购数量
    'player_limit': ('player_limit', 'int'),    # 单个玩家限购次数
    'cost_coin':    ('cost_coin', 'int'),       # 钻石价格
    'time':         ('time', 'int'),            # 时间
}

server_play_rankreward = {
    'uk':           ('id', 'int'),                  # id
    'version':      ('version', 'int'),             # 版本编号
    'rank':         ('rank', 'int_list'),           # 排行
    'rank_reward':  ('rank_reward', 'int_list'),    # 奖励
}

server_play_points = {
    'uk':       ('id', 'int'),          # id
    'version':  ('version', 'int'),     # 版本编号
    'point':    ('point', 'int'),       # 购买次数
    'reward':   ('reward', 'int_list'), # 奖励
}