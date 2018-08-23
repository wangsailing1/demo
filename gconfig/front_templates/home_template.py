#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check


# 家园房间
home_main = {
    'uk': ('id', 'int'),                # 房间id
    'name': ('name', 'unicode'),        # 房间名/阵营
    'hero': ('hero', 'int_list'),       # 房间英雄(多个)
    'picture': ('picture', 'str'),      # 房间背景图
    'dressup_sort': ('dressup_sort', 'int_list'),   # 房间的装扮项
}


# 装扮项
home_dressup_sort = {
    'uk': ('id', 'int'),                # 序号
    'icon': ('icon', 'str'),            # 装扮项图标
    'condition': ('condition', 'int'),  # 解锁条件(等级)
    'need_card': ('need_card', 'int_list'),  # 解锁所需英雄
    'dressup_id': ('dressup_id', 'int_list'),   # 装扮项包含的装扮
}


# 装扮详情
home_dressup_detail = {
    'uk': ('id', 'int'),                    # 序号
    'name': ('name', 'unicode'),            # 装扮名称
    'anim': ('anim', 'str'),                # 装扮图或动画
    'value': ('value', 'int'),              # 装扮值
    'cost': ('cost', 'list_3'),             # 解锁花费
    'need_card': ('need_card', 'int_list'),           # 解锁所需英雄
    'position': ('position', 'int_list'),   # 装扮安放的坐标
    'attr': ('attr', 'list_2'),             # 装扮使用的属性
    'icon': ('icon', 'str'),
    'need_level': ('need_level', 'int'),    # 等级解锁
}

home_flower_reward = {
    'uk': ('id', 'int'),                # 收到的花朵数
    'reward': ('reward', 'list_3'),     # 奖励
}

home_flsend_reward = home_flower_reward

