#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 战斗相关的配置, 暂时给前端使用
from gconfig import check


# 地块掉落奖励
slg_block_reward = {
    'uk': ('id', 'int'),  #
    'range': ('range', 'list_2'),
    'reward': ('reward', 'int_list'),
}
