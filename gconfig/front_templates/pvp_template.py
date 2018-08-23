#! --*-- coding: utf-8 --*--

__author__ = 'huwenchao'

# pvp用表
from gconfig import check


# 竞技场匹配表
pvp_arena = {
    'uk': ('id', 'int'),  # 分段编号
    'rank': ('rank', 'int_list'),
    'day_reward': ('day_reward', 'list_3'),
    'win_a': ('win_a', 'int'),
    'win_b': ('win_b', 'int'),
    'lose_a': ('lose_a', 'int'),
    'lose_b': ('lose_b', 'int'),
    'rank_add': ('rank_add', 'int'),
    'rank_r0': ('rank_r0', 'int'),
    'reduce': ('reduce', 'int'),
}


# 功能说明
text = {
    'uk': ('id', 'int'),
    'text': ('text', 'unicode'),    # 功能说明
}


# 机器人
# robots = {
#     'uk': ('lvl', 'int'),           # 等级
#     'hero': (('hero1', 'hero2', 'hero3', 'hero4', 'hero5'), ('list_2', 'mult_list')),  # 英雄id
#     'evo': ('evo', 'list_2'),       # 品阶权重
#     'star': ('star', 'list_2'),     # 星级权重
# }


# # 离线竞技场(黑街擂台)轮数奖励表
# darkstreet_reward_round = {
#     'uk': ('round_id', 'int'),          # 轮数id
#     'reward': ('reward', 'list_3'),     # 奖励
# }


# 离线竞技场(黑街擂台)战力匹配
darkstreet_fight = {
    'uk': ('id', 'int'),                    # id
    'round': ('round', 'int'),              # 轮数
    'grade': ('grade', 'int'),              # 档次
    # 'level': ('level', 'int'),              # 等级
    'down_limit': ('down_limit', 'float'),  # 战力下限系数
    'up_limit': ('up_limit', 'float'),      # 战力上限系数
    'reward': ('reward', 'list_3'),         # 奖励
    'reward1': ('reward1', 'list_4'),       # 战胜随机奖励库
    'hero_exp': ('hero_exp', 'int'),        # 英雄经验
}


# 离线竞技场(黑街擂台)击破奖励表
darkstreet_reward_break = {
    'uk': ('id', 'int'),                # id
    'times': (('times1', 'times2', 'times3'), ('int', 'mult_dict_1')),  # 档次1-3条件
    'reward': (('reward1', 'reward2', 'reward3'), ('list_3', 'mult_dict_1')),  # 档次1-3奖励
}


# 离线竞技场(黑街擂台)里程碑段位
darkstreet_milestone = {
    'uk': ('id', 'int'),                # id
    'title': ('title', 'unicode'),      # 称号
    'name': ('name', 'unicode'),        # 段位名称
    'name_num': ('name_num', 'int'),      # 段位段数
    'icon': ('icon', 'str'),            # 图标
    'times': ('times', 'int'),          # 累积次数
    'reward': ('reward', 'list_3'),     # 奖励
}


# 竞技场里程碑
arena_milestone_reward = {
    'uk': ('id', 'int'),
    'arena_times': ('arena_times', 'int'),
    'arena_milestone_reward': ('arena_milestone_reward', 'list_3', check.check_reward()),
    'rally_times': ('rally_times', 'int'),
    'rally_milestone_reward': ('rally_milestone_reward', 'list_3', check.check_reward()),
    'rally_day_km': ('rally_day_km', 'int'),
    'rally_day_km_reward': ('rally_day_km_reward', 'list_3', check.check_reward()),
}
