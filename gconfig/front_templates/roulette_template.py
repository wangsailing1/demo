#! --*-- coding: utf-8 --*--

# 活动相关的配置
from gconfig import check

# 轮盘
roulette = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'price': ('price', 'int'),
    'price_10': ('price_10', 'int'),
    'reward1': ('reward1', 'list_4'),
    'reward2': ('reward2', 'list_4'),
    'reward_show': ('reward_show', 'list_3'),
    'notice': ('notice', 'unicode'),
}


achieve_reward = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'time': ('time', 'int_list'),
    'reward': ('reward', 'list_3'),
}


# 新服轮盘
server_roulette = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str'),
    'end_time': ('end_time', 'str'),
    'price': ('price', 'int'),
    'price_10': ('price_10', 'int'),
    'reward1': ('reward1', 'list_4'),
    'reward2': ('reward2', 'list_4'),
    'reward_show': ('reward_show', 'list_3'),
    'notice': ('notice', 'unicode'),
}


server_achieve_reward = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'time': ('time', 'int_list'),
    'reward': ('reward', 'list_3'),
}


# 许愿池
charge_roulette = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'need_sort': ('need_sort', 'int'),
    'price': ('price', 'int'),
    'need_item': ('need_item', 'int_list'),
    'reward1': ('reward1', 'list_4'),
    'reward2': ('reward2', 'list_4'),
    'reward_show': ('reward_show', 'list_3'),
    'notice': ('notice', 'unicode'),
    'currency': ('currency', 'str'),
    'currency_name': ('currency', 'unicode'),
}


server_charge_roulette = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str'),
    'end_time': ('end_time', 'str'),
    'need_sort': ('need_sort', 'int'),
    'price': ('price', 'int'),
    'need_item': ('need_item', 'int_list'),
    'reward1': ('reward1', 'list_4'),
    'reward2': ('reward2', 'list_4'),
    'reward_show': ('reward_show', 'list_3'),
    'notice': ('notice', 'unicode'),
    'currency': ('currency', 'str'),
    'currency_name': ('currency', 'unicode'),
}
