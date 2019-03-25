# -*- coding: utf-8 –*-


# 街区配置
dan_grading_list = {
    'uk': ('id', 'int'),
    'name': ('name', 'int'),
    'daily_rewards': ('daily_rewards', 'int_list'),
    'reach_rewards': ('reach_rewards', 'int_list'),
    'promotion_cup_num': ('promotion_cup_num', 'int'),
    'people_num': ('people_num', 'int'),
    'standard_box': ('standard_box', 'float'),
    'privilage': ('privilage', 'int_list'),
    'icon': ('icon', 'str'),

}

# 票房排行奖励
rank_reward_list = {
    'uk': ('id', 'int'),
    'rank': ('rank', 'int_list'),
    'daily_reward': ('daily_reward', 'int_list'),
}

# 奖杯设置
cup_num = {
    'uk': ('id', 'int'),
    'award_name': ('award_name', 'int'),
    'win_cup_num': ('win_cup_num', 'int'),
    'nomi_cup_num': ('nomi_cup_num', 'int'),
    'like_num': ('like_num', 'int_list'),
    'first_lines': ('first_lines', 'int_list'),
    'mid_lines': ('mid_lines', 'int'),
    'last_lines': ('last_lines', 'int'),
    'sort': ('sort', 'int'),
    'icon': ('icon', 'str'),
    'des': ('des', 'str'),
}

# #颁奖设置
# compere_lines = {
#     'uk': ('id', 'int'),
#     'first_lines': ('first_lines', 'int'),
#     'mid_lines': ('mid_lines', 'int'),
#     'last_lines': ('last_lines', 'int'),
# }


# 颁奖设置
dan_grading_privilage = {
    'uk': ('id', 'int'),
    'disc': ('disc', 'str'),
}
