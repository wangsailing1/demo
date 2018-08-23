#! --*-- coding: utf-8 --*--

# 大决斗相关的配置

# 排行奖励
duel_rank_award = {
    'uk': ('id', 'int'),
    'start_rank': ('start_rank', 'int'),            # 初始排名
    'end_rank': ('end_rank', 'int'),                # 结束排名
    'per_reward': ('per_reward', 'list_3'),         # 奖励
    'title': ('title', 'unicode'),         # 奖励
    'description': ('description', 'unicode'),         # 奖励
}

# 大决斗兑换表
duel_exchange = {
    'uk': ('id', 'int'),
    'need_item': ('need_item', 'list_3'),           # 消耗物品
    'reward': ('reward', 'list_3'),                 # 奖励
    'level': ('level', 'int'),                      # 等级
}
