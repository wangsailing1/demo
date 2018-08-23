#! --*-- coding: utf-8 --*--


# 虫洞矿坑
wormhole_detail = {
    'uk': ('id', 'int'),                            # id
    'position_nums': ('position_nums', 'int'),      # 每层的位置数
    'reward': ('reward', 'list_3'),                 # 每日结算奖励
    'reward_seized': ('reward_seized', 'list_3'),   # 占领奖励
    'reward_seized2': ('reward_seized2', 'list_3'),   # 金币奖励奖励，半小时算一次
    'is_pass': ('is_pass', 'int'),                  # 是否是通道
    'enemy_id_rage': ('enemy_id_rage', 'int_list'), # 每层的位置数
    'weight': ('weight', 'int'),                    # 权重
    'lucky_site': ('lucky_site', 'int_list'),       # 幸运位置随机
    'final_reward1': ('final_reward1', 'list_3'),   # 每期固定奖励
    'final_reward2': ('final_reward2', 'list_4'),   # 每期随机奖励1
    'final_reward3': ('final_reward3', 'list_4'),   # 每期随机奖励2
    'final_reward_mail': ('final_reward_mail', 'unicode'),  # 奖励邮件内容
    'final_reward_mail_title': ('final_reward_mail_title', 'unicode'),  # 奖励邮件标题

    'enemy_level': ('enemy_level', 'int'),          # 机器人的等级
    'channel_enemy_level': ('channel_enemy_level', 'int'),          # 通道机器人的等级
}

# 虫洞矿坑主题信息
wormhole_theme = {
    'uk': ('id', 'int'),                            # id
    'name': ('name', 'unicode'),                    # 主题名字
    'banner': ('banner', 'str'),                    # 主题图标
    'group_id': ('group_id', 'int_list'),             # 可用英雄
}

# 虫洞矿坑全局控制
wormhole = {
    'uk': ('id', 'int'),                                # id
    'fight_nums': ('fight_nums', 'int'),                # 每日挑战次数
    'fight_cost': ('fight_cost', 'list_4'),             # 购买体力价格
    'fight_buy_limit': ('fight_buy_limit', 'int'),      # 购买上限
    'morale_cost': ('morale_cost', 'list_3'),           # 恢复士气价格
    'morale_speed': ('morale_speed', 'int'),            # 士气恢复速度
    'lucky_nums': ('lucky_nums', 'int'),                # 幸运位置数量
    'lucky_reward': ('lucky_reward', 'list_3'),         # 幸运位置奖励
    'lucky_refresh': ('lucky_refresh', 'str'),          # 幸运位置刷新时间
    'lucky_time': ('lucky_time', 'str'),                # 幸运位置发奖时间
    'reward_time': ('reward_time', 'str'),              # 常规奖励结算时间
    'advance_cost': ('advance_cost', 'int'),            # 突进价格
    'turn_time': ('turn_time', 'int_list'),               # 轮次时间
    'per_time': ('per_time', 'int'),                    # 每多少分钟结算一次奖励
}

# 虫洞矿坑每日攻打次数奖励
wormhole_reward_break = {
    'uk': ('id', 'int'),                # id
    'times': ('times', 'int'),          # 每日挑战次数
    'reward': ('reward', 'list_3'),     # 奖励
}
