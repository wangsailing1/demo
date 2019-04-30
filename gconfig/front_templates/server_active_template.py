#! --*-- coding: utf-8 --*--

# 活动相关的配置
from gconfig import check


# 累计消耗
server_consume = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),      # 展示时间
    'server_start_time': ('server_start_time', 'str'),        # 开始时间
    'server_end_time': ('server_end_time', 'str'),            # 结束时间
    'num': ('num', 'int'),                      # 数值
    'reward_show': ('reward_show', 'list_3', check.check_reward(),),   # 奖品
    'level': ('level', 'int_list'),             # 展示大奖
    'reward': ('reward', 'list_3', check.check_reward(),),             # 等级
    'server_id': ('server_id', 'int_list'),     # 服务器id
    'mail_title': ('mail_title', 'unicode'),    # 邮件名
    'des': ('des', 'unicode'),                  # 邮件内容描述
    'daily_reward': ('daily_reward', 'list_3', check.check_reward()),     # 累充（单充）补给奖励
    'show_des': ('show_des', 'unicode'),
}

# 每日消耗
server_daily_consume = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),      # 展示时间
    'server_start_time': ('server_start_time', 'str'),        # 开始时间
    'server_end_time': ('server_end_time', 'str'),            # 结束时间
    'num': ('num', 'int'),                      # 数值
    'reward_show': ('reward_show', 'list_3', check.check_reward(),),   # 奖品
    'level': ('level', 'int_list'),             # 展示大奖
    'reward': ('reward', 'list_3', check.check_reward(),),             # 等级
    'server_id': ('server_id', 'int_list'),     # 服务器id
    'mail_title': ('mail_title', 'unicode'),    # 邮件名
    'des': ('des', 'unicode'),                  # 邮件内容描述
    'daily_reward': ('daily_reward', 'list_3', check.check_reward()),     # 累充（单充）补给奖励
    'show_des': ('show_des', 'unicode'),
}

# 充值活动
server_recharge = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),      # 展示时间
    'server_start_time': ('server_start_time', 'str'),        # 开始时间
    'server_end_time': ('server_end_time', 'str'),            # 结束时间
    'num': ('num', 'float'),                      # 数值
    'limit_num': ('limit_num', 'int'),          # 限制次數
    'reward_show': ('reward_show', 'list_3', check.check_reward()),   # 奖品
    'level': ('level', 'int_list'),             # 展示大奖
    'reward': ('reward', 'list_3', check.check_reward()),             # 等级
    'server_id': ('server_id', 'int_list'),     # 服务器id
    'mail_title': ('mail_title', 'unicode'),    # 邮件名
    'des': ('des', 'unicode'),                  # 邮件内容描述
    'charge_type': ('charge_type', 'int'),      # 充值类型
    'num_type': ('num_type', 'int'),            # 计数类型
    'charge_id': ('charge_id', 'int'),          # 充值项
    'currency': ('currency', 'str'),            # 币种
    'currency_name': ('currency_name', 'unicode'),     # 种名
    'daily_reward': ('daily_reward', 'list_3', check.check_reward()),     # 累充（单充）补给奖励
    'show_des': ('show_des', 'unicode'),
    'card_show': ('card_show', 'list_3'),
    'plank_des1': ('plank_des1', 'unicode'),
    'plank_des2': ('plank_des2', 'unicode'),
    'is_open': ('is_open', 'int'),
}

# # 每日充值活动
# server_daily_recharge = {
#     'uk': ('id', 'int'),
#     'version': ('version', 'int'),
#     'show_id': ('show_id', 'int'),              # 展示id
#     'show_time': ('show_time', 'unicode'),      # 展示时间
#     'server_start_time': ('server_start_time', 'str'),        # 开始时间
#     'server_end_time': ('server_end_time', 'str'),            # 结束时间
#     'num': ('num', 'float'),                      # 数值
#     'reward_show': ('reward_show', 'list_3', check.check_reward(),),   # 奖品
#     'level': ('level', 'int_list'),             # 展示大奖
#     'reward': ('reward', 'list_3', check.check_reward(),),             # 等级
#     'server_id': ('server_id', 'int_list'),     # 服务器id
#     'mail_title': ('mail_title', 'unicode'),    # 邮件名
#     'des': ('des', 'unicode'),                  # 邮件内容描述
#     'num_type': ('num_type', 'int'),            # 计数类型
#     'currency': ('currency', 'str'),            # 币种
#     'currency_name': ('currency_name', 'unicode'),     # 种名
#     'daily_reward': ('daily_reward', 'list_3', check.check_reward()),     # 累充（单充）补给奖励
#     'show_des': ('show_des', 'unicode'),
# }

# 常规兑换活动
server_normal_exchange = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),       # 展示时间
    'type': ('type', 'int'),                    # 兑换类型
    'server_start_time': ('server_start_time', 'str'),        # 开始时间
    'server_end_time': ('server_end_time', 'str'),            # 结束时间
    'exchange_num': ('exchange_num', 'int'),    # 可兑换次数
    'need_item': ('need_item', 'list_3'),       # 兑换道具
    'out_item': ('out_item', 'list_3'),         # 兑换得到的奖品
    'show_des': ('show_des', 'unicode'),
}

# 限时兑换活动
# server_omni_exchange = {
#     'uk': ('id', 'int'),
#     'version': ('version', 'int'),
#     'show_id': ('show_id', 'int'),              # 展示id
#     'show_time': ('show_time', 'unicode'),       # 展示时间
#     'exchange_type': ('exchange_type', 'int'),  # 兑换类型
#     'server_start_time': ('server_start_time', 'str'),        # 开始时间
#     'server_end_time': ('server_end_time', 'str'),            # 结束时间
#     'exchange_num': ('exchange_num', 'int'),    # 可兑换次数
#     'need_item': ('need_item', 'list_3'),       # 兑换道具
#     'out_item': ('out_item', 'list_3'),         # 兑换得到的奖品
#     'reward_show': ('reward_show', 'list_3'),   # 大奖
#     'show_des': ('show_des', 'unicode'),
# }

# 豪华签到
server_sign_daily_charge = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),               # 版本号
    'show_time': ('show_time', 'unicode'),       # 展示时间
    'server_start_time': ('server_start_time', 'str'),         # 开始时间
    'server_end_time': ('server_end_time', 'str'),             # 结束时间
    'day': ('day', 'int'),                       # 天数
    'reward': ('reward', 'list_3', check.check_reward(),),              # 奖励
    'show_reward': ('show_reward', 'list_3', check.check_reward(),),    # 展示的奖励
    'pay': ('pay', 'int'),                       # 签到所需金额
    'pay_sort': ('pay_sort', 'int'),             # 记录支付的种类
    'final_reward': ('final_reward', 'list_3', check.check_reward(),),  # 最终大奖
    'des': ('des', 'unicode'),                   # 大奖描述
}

# 活动展示
server_active_show = {
    'uk': ('id', 'int'),
    'sort': ('sort', 'int'),                    # 标签id
    'level': ('level', 'int_list'),             # 等级
    'show_time': ('show_time', 'str'),        # 开始时间
    'server_id': ('server_id', 'int_list'),     # 服务器id
    'show_id': ('show_id', 'int'),              # 展示顺序
    'mark': ('mark', 'int'),                    # 标志
    'banner': ('banner', 'unicode'),            # 名字
}

# 每日礼包
server_daily_reward = {
    'uk': ('week', 'int'),                      # 周一到周日，1-7
    'reward': ('reward', 'list_3', check.check_reward(),),             # 奖励
    'des': ('des', 'unicode'),                  # 奖励描述
}
server_gift_show = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),               # 版本号
    'show': ('show', 'int'),    # 是否展示
    'show_id': ('show_id', 'int'),    # 展示顺序
    'time_show': ('time_show', 'str'),    # 展示时间
    'start_time': ('start_time', 'str'),         # 开始时间
    'end_time': ('end_time', 'str'),             # 结束时间
    'name': ('name', 'unicode'),    # 标签名字
    'reward': ('reward', 'list_3', check.check_reward(),),              # 奖励
    'daily_reward': ('daily_reward', 'list_3', check.check_reward()),  # 今日福利
    'charge': ('charge', 'int'),    # 充值对应项
    'show_des': ('show_des', 'unicode'),  # 大奖描述
}
server_buy_reward = {
    'uk': ('id', 'int'),                    # id
    'show_id': ('show_id', 'int'),          # 上一个页签对应的礼包类型
    'demand': ('demand', 'int'),            # 购买需求，1是充值，2是花费钻石
    'level': ('level', 'int_list'),         # 指玩家等级区间，格式1,40
    'reward': ('reward', 'list_4'),         # 奖励
    'reward_num': ('reward_num', 'int'),    # 随机数量
}
