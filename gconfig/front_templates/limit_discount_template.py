#! --*-- coding: utf-8 --*--

# 活动相关的配置
from gconfig import check

# 限时特惠
limit_discount = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'name': ('name', 'unicode'),
    'rebate': ('rebate', 'str'),
    'buy_num': ('buy_num', 'int'),
    'charge': ('charge', 'int'),
    'hero_show': ('hero_show', 'list_3'),
    'reward': ('reward', 'list_3'),
    'show_des1': ('show_des1', 'unicode'),
    'show_des2': ('show_des2', 'unicode'),
    'show_price': ('show_price', 'unicode'),
    'plank_des': ('plank_des', 'unicode'),
}


server_limit_discount = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str'),
    'end_time': ('end_time', 'str'),
    'name': ('name', 'unicode'),
    'rebate': ('rebate', 'str'),
    'buy_num': ('buy_num', 'int'),
    'charge': ('charge', 'int'),
    'hero_show': ('hero_show', 'list_3'),
    'reward': ('reward', 'list_3'),
    'show_des1': ('show_des1', 'unicode'),
    'show_des2': ('show_des2', 'unicode'),
    'show_price': ('show_price', 'unicode'),
    'plank_des': ('plank_des', 'unicode'),
}


# 天降红包
red_bag = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S")),
    'times': ('times', 'int'),
    'refresh': ('refresh', 'int'),
    'type1': ('type1', 'int'),
    'num1': ('num1', 'int'),
    'type2': ('type2', 'int'),
    'num2': ('num2', 'int'),
    'quantity': ('quantity', 'int'),
    'min': ('min', 'int'),
    'max': ('max', 'int'),
    'instruction': ('instruction', 'unicode'),
}
server_red_bag = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'start_time': ('start_time', 'str'),
    'end_time': ('end_time', 'str'),
    'times': ('times', 'int'),
    'refresh': ('refresh', 'int'),
    'type1': ('type1', 'int'),
    'num1': ('num1', 'int'),
    'type2': ('type2', 'int'),
    'num2': ('num2', 'int'),
    'quantity': ('quantity', 'int'),
    'min': ('min', 'int'),
    'max': ('max', 'int'),
    'instruction': ('instruction', 'unicode'),
}
