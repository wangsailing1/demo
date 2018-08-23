#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 公会相关的配置
from gconfig import check


# 公会BOSS血量变化
worldboss_boss = {
    'uk': ('id', 'str'),                # id
    'boss_id': ('boss_id', 'int'),      # boss_id
    'open_time': ('open_time', 'str'),  # 开启时间
    'show_time': ('show_time', 'str'),  # 展示时间
    'cold_time': ('cold_time', 'int'),      # 冷却时间
    'round': ('round', 'int'),          # 回合上限
    'hp_basis': ('hp_basis', 'int'),          # BOSS初始血量、最低血量

    'time_condition1': ('time_condition1', 'int_list'),  # 条件
    'time_condition2': ('time_condition2', 'int_list'),  # 条件
    'time_condition3': ('time_condition3', 'int_list'),  # 条件
    'lefthp_condition1': ('lefthp_condition1', 'int_list'),  # 条件
    'lefthp_condition2': ('lefthp_condition2', 'int_list'),  # 条件
    'lefthp_condition3': ('lefthp_condition3', 'int_list'),  # 条件
    'kill_time1': ('kill_time1', 'float'),  # 血量变化
    'kill_time2': ('kill_time2', 'float'),  # 血量变化
    'kill_time3': ('kill_time3', 'float'),  # 血量变化
    'kill_time4': ('kill_time4', 'float'),  # 血量变化
    'kill_time5': ('kill_time5', 'float'),  # 血量变化
    'kill_time6': ('kill_time6', 'float'),  # 血量变化

    'worldboss_bg': ('worldboss_bg', 'str'),  # 背景图
    'killreward_show': ('killreward_show', 'list_3'),  # 击败boss奖励展示
    'killreward': ('killreward', 'list_3'),  # 击杀boss奖励展示
    'title': ('title', 'int'),  # 奖励邮件标题
    'des': ('des', 'int'),  # 奖励邮件内容
    'des': ('des', 'int'),  # 奖励邮件内容
    'killreward_msg': ('killreward_msg', 'int'),  # 击杀奖励邮件内容
    'refresh_cost': ('refresh_cost', 'int'),  # 刷新所需钻石
    'bossbattle_bg': ('bossbattle_bg', 'str'),  # 战斗背景
    'boss_data_id': ('boss_data_id', 'str'),  # boss编号
}


# 伤害区间奖励
worldboss_streward = {
    'uk': ('id', 'int'),                # id
    'damage': ('damage', 'int_list'),   # 伤害区间
    'reward': ('reward', 'list_3'),     # 伤害区间奖励
}

# 英雄头像展示
worldboss_heroact = {
    'uk': ('id', 'int'),                # id
    'id': ('id', 'int'),
}


# 排名奖励
worldboss_topreward = {
    'uk': ('id', 'int'),                # id
    'rank': ('rank', 'int_list'),     # 奖励
    'rank_reward': ('rank_reward', 'list_3'),  # 奖励
    'title': ('title', 'unicode'),      # 邮件标题
    'des': ('des', 'unicode'),          # 公会邮件内容
}

# 公会排名奖励
worldboss_guild = {
    'uk': ('id', 'int'),                # id
    'rank': ('rank', 'int_list'),     # 奖励
    'rank_reward': ('rank_reward', 'list_3'),  # 奖励
    'title': ('title', 'unicode'),      # 邮件标题
    'des': ('des', 'unicode'),          # 公会邮件内容
}


# 积分奖励
worldboss_pointreward = {
    'uk': ('id', 'int'),                # id
    'bosspoint': ('bosspoint', 'int'),     # 奖励
    'point_reward': ('point_reward', 'list_3'),  # 奖励
    'title': ('title', 'unicode'),      # 邮件标题
    'des': ('des', 'unicode'),          # 公会邮件内容
}

