#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check


# 排名奖励
arena_award = {
    'uk': ('id', 'int'),                        # id
    'start_rank': ('start_rank', 'int'),        # 初始排名
    'end_rank': ('end_rank', 'int'),            # 结束排名
    'per_reward': ('per_reward', 'list_3'),     # 奖励
}


# 最高排名奖励
arena_once_reward = {
    'uk': ('id', 'int'),                        # id
    'rank': ('rank', 'int'),                    # 目标排名
    'once_reward': ('once_reward', 'list_3'),   # 奖励
}


# 每日奖励
arena_daily_reward = {
    'uk': ('id', 'int'),                            # 场次
    'daily_reward': ('daily_reward', 'list_3'),     # 奖励
}


# # 匹配敌人
# arena_enemy = {
#     'uk': ('id', 'int'),                        # id
#     'start_rank': ('start_rank', 'int'),        # 初始排名
#     'end_rank': ('end_rank', 'int'),            # 结束排名
#     'step': ('step', 'int_list'),               # 1-2匹配敌人
#     'step_next': ('step_next', 'int_list'),     # 3匹配敌人
#     'step_last': ('step_last', 'int_list'),     # 末匹配敌人
# }
#
#
# # 匹配机器人
# arena_robot = {
#     'uk': ('id', 'int'),                        # id
#     'rank_list': ('rank_list', 'int_list'),     # 机器人名次区间
#     'enemy_id': ('enemy_id', 'int_list'),       # 机器人编号
# }
