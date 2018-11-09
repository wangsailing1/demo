#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 装备相关的配置
from gconfig import check

# 激活码
code = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),
    'open': ('open', 'int_float_str'),
    'type': ('type', 'int'),
    # 'vip': ('vip', 'int'),
    'close': ('close', 'int_float_str'),
    # 'server': ('server', 'str'),
    'refresh': ('refresh', 'int'),
    'reward_des': ('reward_des', 'unicode'),
    'reward': ('reward', 'list_3'),
    'icon': ('icon', 'str'),
}
