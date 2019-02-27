#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

# 藏宝图配置
from gconfig import check


# 藏宝图
one_piece = {
    'uk':           ('version', 'int'),                 # 活动编号
    'id':           ('id', 'int'),                      # 编号
    'free_reward':  ('free_reward', 'int_list'),        # 免费探索奖励
    'one_coin':     ('one_coin', 'int'),                # 单次消耗钻石
    'ten_coin':     ('ten_coin', 'int'),                # 十连消耗钻石
    'max_score':    ('max_score', 'int'),               # 最高积分
    'max_rate':     ('max_rate', 'int'),                # 概率
    'vip_limit':    ('vip_limit', 'int'),               # vip等级限制
    'server_score': ('server_score', 'int_list'),       # 服务器加分人次
    'score':        (('score_1','score_2','score_3'), ('int', 'mult_force_num_list')),    # 阶段积分
    'reward':       (('reward_1','reward_2','reward_3'), ('int_list', 'mult_force_num_list')),    # 奖励内容
    'show_ranking': ('show_ranking', 'int'),            # 是否显示排名（1：显示，0：不显示）
    'notice':       ('notice', 'str'),                  # 说明
}

one_piece_rate = {
    'uk':           ('active_id', 'int'),               # 编号
    'version':      ('version', 'int'),                 # 对应one_piece编号
    'id':           ('id', 'int'),                      # 免费探索奖励
    'show_id':      ('show_id', 'int'),                 # 展示顺序
    'reward':       ('reward', 'int_list'),             # 奖励
    'score':        ('score', 'int'),                   # 积分
    'rate':         ('rate', 'int'),                    # 不走积分概率
    'has_reduce':   ('has_reduce', 'int'),              # 积分是否衰减 1：是 2：否
}

one_piece_exchange = {
    'uk':           ('id', 'int'),                  # 编号
    'version':      ('version', 'int'),             # 对应one_piece编号
    'sort':         ('sort', 'int'),                # 免费探索奖励
    'reward':       ('reward', 'int_list'),         # 奖励
    'limit_num':    ('limit_num', 'int'),           # 积分
    'need_key_num': ('need_key_num', 'int'),        # 不走积分概率
    'player_limit': ('player_limit', 'int'),        # 积分是否衰减 1：是 2：否
}

one_piece_rank_reward = {
    'uk':           ('id', 'int'),                  # 编号
    'version':      ('version', 'int'),             # 对应one_piece编号
    'reward_time':  ('reward_time', 'str'),         # 奖励时间
    'rank':         ('rank', 'int_list'),           # 排名[上限，下限]
    'rank_reward':  ('rank_reward', 'int_list'),    # 奖励内容
    'mail':         ('mail', 'str'),                # 邮件内容
}

one_piece_reduce = {
    'uk':           ('id', 'int'),                  # vip等级
    'day_1':        ('day_1', 'int'),               # 第一天衰减
    'day_2':        ('day_2', 'int'),               # 第二天衰减
    'day_3':        ('day_3', 'int'),               # 第三天衰减
}