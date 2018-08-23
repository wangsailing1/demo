#! --*-- coding: utf-8 --*--

__author__ = 'sm'


# 无尽梦靥
daily_nightmares = {
    'uk': ('id', 'int'),                        # 编号
    'name': ('name', 'unicode'),                # 名字
    'act': ('act', 'str'),                      # 显示怪物动画
    'hard': ('hard', 'int'),                    # 难度
    'unlock_type': ('unlock_type', 'int'),      # 解锁类型
    'unlock_limit': ('unlock_limit', 'int'),    # 解锁限制
    'chapterid': ('chapterid', 'int_list'),     # 关卡id
    'round': ('round', 'int'),                  # 关卡波数
    'vip_round': ('vip_round', 'int'),          # vip关卡波数
}


# 无尽梦靥奖励表
daily_rewards_nightmares = {
    'uk': ('id', 'int'),                        # 编号
    'hard': ('hard', 'int'),                    # 难度
    'section': ('section', 'int'),              # 奖励区间
    'reward1': ('reward1', 'list_3'),           # 固定奖励
    'reward2': ('reward2', 'list_4'),           # 随机奖励
}


# 战争工厂
daily_boss = {
    'uk': ('id', 'int'),                        # 编号
    'name': ('name', 'unicode'),                # 名字
    'hard': ('hard', 'int'),                    # 难度
    'round': ('round', 'int'),                  # 挑战时间(回合)
    'unlock_type': ('unlock_type', 'int'),      # 解锁类型
    'unlock_limit': ('unlock_limit', 'int'),    # 解锁限制
    'chapterid': ('chapterid', 'int_list'),     # 关卡id
    # 'blood': ('blood', 'int'),                  # boss血量上限
    # 'rate': ('rate', 'float'),                  # 银币系数
    'silver_coin': ('silver_coin', 'int'),      # 银币总数
}


# 银币活动奖励表
# daily_rewards_boss = {
#     'uk': ('section', 'int'),                   # 伤害值区间
#     'rate': ('rate', 'float'),                  # 系数
#     'value': ('value', 'int'),                  # 计算数值
# }


# 进阶副本
daily_advance = {
    'uk': ('id', 'int'),                        # 编号
    'name': ('name', 'unicode'),                # 名字
    'act': ('act', 'str'),                      # 显示怪物动画
    'sort': ('sort', 'int'),                    # 关卡类型
    'time': ('time', 'int_list'),               # 开启时间
    'hard': ('hard', 'int'),                    # 难度
    'unlock_type': ('unlock_type', 'int'),      # 解锁类型
    'unlock_limit': ('unlock_limit', 'int'),    # 解锁限制
    'chapterid': ('chapterid', 'int'),          # 关卡id
    'reward': ('reward', 'list_4'),             # 活动奖励
    'reward1': ('reward1', 'list_4'),             # 活动奖励
}


# 普通签到
sign_reward = {
    'uk': ('id', 'int'),                        # 编号
    'version': ('version', 'int'),              # 版本号
    'day': ('day', 'int'),                      # 天
    'reward': ('reward', 'list_3'),             # 奖励
    'vip': ('vip', 'int'),                      # vip
}


# 普通签到大奖
sign_final_reward = {
    'uk': ('id', 'int'),                        # 编号
    # 'month': ('month', 'int'),                  # 月
    'day': ('day', 'int'),                      # 天
    'final_reward': ('final_reward', 'list_3'), # 奖励
}


# 超值签到
sign_reward_coin = {
    'uk': ('id', 'int'),                        # 编号
    'month': ('month', 'int'),                  # 月
    'day': ('day', 'int'),                      # 天
    'pay': ('pay', 'int'),                      # 充值金额
    'icon': ('icon', 'str'),                    # 图标
    'reward': ('reward', 'list_3'),             # 奖励
    'description': ('description', 'unicode'),  # 描述
    'score': ('score', 'int'),                  # 积分
    'currency': ('currency', 'str'),                        # 币种
    'currency_name': ('currency_name', 'unicode'),          # 币种描述
}


# 普通签到大奖
sign_final_reward_coin = {
    'uk': ('id', 'int'),                        # 编号
    'month': ('month', 'int'),                  # 月
    'day': ('day', 'int'),                      # 天
    'final_reward': ('final_reward', 'list_3'), # 奖励
}


# 成长基金
growth_fund = {
    'uk': ('id', 'int'),                        # 编号
    'open_vip': ('open_vip', 'int'),            # vip等级
    'price': ('price', 'list_3'),               # 花费
}


# 成长基金奖励
growth_fund_reward = {
    'uk': ('id', 'int'),                        # 编号
    'level': ('level', 'int'),                  # 等级
    'reward': ('reward', 'list_3'),             # 奖励
}


# 日常活动显示表
daily_activity = {
    'uk': ('id', 'int'),                        # 编号
    'sort': ('sort', 'int'),                    # 标签
    'show_id': ('show_id', 'int'),              # 展示顺序
    'mark': ('mark', 'int'),                    # 标志，没用～～～
    'banner': ('banner', 'unicode'),            # 名字
}


# 全民福利奖励
growth_fund_all = {
    'uk': ('id', 'int'),                        # 编号
    'buy_number': ('buy_number', 'int'),        # 购买人数
    'reward': ('reward', 'list_3'),             # 奖励
}

# 成长基金注水
growth_fund_water = {
    'uk': ('id', 'int'),                        # 编号
    'water_number': ('water_number', 'int'),
    'water_max': ('water_max', 'int'),               # 最大注水数
    'per_time': ('per_time', 'int'),
}
