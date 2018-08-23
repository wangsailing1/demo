#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 用户相关的配置
from gconfig import check


# 好友加油
friend_cheer = {
    'uk': ('item_level', 'int'),            # 生产物等级
    'time_reduce': ('time_reduce', 'int'),  # 缩减时间（秒）
    'friend': ('friend', 'int'),            # 友好度增加值
}


# 好友打扫
friend_clean = {
    'uk': ('id', 'int'),                            # 扫除奖励ID
    'player_level': ('player_level', 'int_list'),   # 打扫者等级
    'reward': ('reward', 'list_3'),                 # 奖励内容
    'friend': ('friend', 'int'),                    # 友好度增加值
}


# 红包
redpacket = {
    'uk': ('id', 'int'),
    'level': ('level', 'int_list'),     # 等级
    'money': ('money', 'int'),      # 总额
    'sort': ('sort', 'int'),        # 币种
    'number': ('number', 'int'),    # 人数
    'money1': ('money1', 'int'),    # 生成获得
    'money2': ('money2', 'int'),    # 被领获得
}


# 好友度等级
friend_point = {
    'uk': ('friend_lv', 'int'),             # 友情等级
    'need_point': ('need_point', 'int'),    # 需要经验
    'des': ('des', 'unicode'),              # 等级名称
    'reward': ('reward', 'list_3'),         # 奖励
}
