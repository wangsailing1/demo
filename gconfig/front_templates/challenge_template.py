#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check

# 极限挑战
challenge_theme = {
    'uk': ('id', 'int'),
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'theme_name': ('theme_name', 'unicode'),
    'theme_detail': ('theme_detail', 'unicode'),
    'hero_up': ('hero_up', 'int_list'),
    'boss_id': ('boss_id', 'int'),
    'boss_display': ('boss_display', 'int'),
    'reward_show': ('reward_show', 'list_3'),
    'turn': ('turn', 'int'),
    'battle_bg': ('battle_bg', 'str'),
    'server': ('server', 'int_list'),           # 不填是新老服都开，2是只有老服开
    'channel_id': ('channel_id', 'int_list'),   # 填渠道id，填谁谁开，不填全开
    'no_server_id': ('no_server_id', 'int_list'),     # 写谁谁不开
    'stone_reward': ('stone_reward', 'int_list'),       # 奖励灵魂石
}

battle_reward = {
    'uk': ('id', 'int'),
    'damage': ('damage', 'int_list'),
    'damage_reward': ('damage_reward', 'list_3', check.check_reward()),
}


rank_reward_daily = {
    'uk': ('id', 'int'),
    'rank_daily': ('rank_daily', 'int_list'),
    'rank_reward_daily': ('rank_reward_daily', 'list_3', check.check_reward()),
    'stone_num_daily': ('stone_num_daily', 'int'),
}


uc_rank_reward = {
    'uk': ('id', 'int'),
    'rank': ('rank', 'int_list'),
    'rank_reward': ('rank_reward', 'list_3', check.check_reward()),
    'stone_num': ('stone_num', 'int'),
}
