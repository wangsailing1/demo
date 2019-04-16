#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 采集相关的配置
from gconfig import check


# 福利中心总表
gift_center = {
    'uk': ('id', 'int'),  # 编号
    'show_id': ('show_id', 'int'),  # 排序
    'type': ('type', 'int'),  # 类型
    'title': ('title', 'unicode'),  # 标题
    'banner': ('banner', 'str'),  # 活动图片
    'story': ('story', 'unicode'),  # 文字描述
    'start_time': ('start_time', 'str'),  # 活动开始时间, 不配置为永远
    'end_time': ('end_time', 'str'),  # 活动结束时间, 不配置为永远
    'show_lv': ('show_lv', 'int_list'),  # 展示等级
    'is_show': ('is_show', 'int'),  # 显示开关
}

welfare = {
    'uk': ('id', 'int'),                    # 活动id
    'name': ('name', 'unicode'),            # 活动名称
    'sort': ('sort', 'int'),                # 排序
    'is_show': ('is_show', 'int'),          # 是否显示
    'level': ('level', 'int'),              # 开启登陆
    'time_sort': ('time_sort', 'int'),      # 时间类型
    'start_time': ('start_time', 'str'),    # 开启时间
    'end_time': ('end_time', 'str'),        # 结束时间
}


# 每月签到
welfare_sign = {
    'uk': ('id', 'int'),   # 每月签到日期
    'reward': ('reward', 'list_3'),   # 每月签到奖励
}


# 豪华签到
# sign_daily_charge = ({
#     'uk': ('version', 'int'),   # 版本号
#     'day': ('day', 'int'),   # 天数
#     'reward': ('reward', 'list_3'),   # 奖励
#     'pay': ('pay', 'int'),   # 需要充值
#     'pay_sort': ('pay_sort', 'int'),   # 充值类型
#     'pay_icon': ('pay_icon', 'str'),   # 标签图标
# }, 'sign_daily_charge')


# # 新人首周签到
# sign_first_week = {
#     'uk': ('day', 'int'),   # 日
#     'reward': ('reward', 'list_3'),   # 奖励
#     'des': ('des', 'unicode'),   # 描述
# }


# # 首充奖励
# first_charge_reward = {
#     'uk': ('need_charge', 'int'),   # 需要充值金额
#     'reward': ('reward', 'list_3'),  # 奖励
#     'des': ('des', 'unicode'),  # 描述
# }


# 领取体力配置
welfare_energy = {
    'uk': ('id', 'int'),                            # 赠送体力id
    'time_rage': ('time_rage', 'str_list'),         # 补充体力的时间范围
    'power': ('power', 'int'),                   # 增加的体力值
    # 'extra_reward': ('extra_reward', 'list_3'),     # 额外奖励
}


# 累积登陆
welfare_login = {
    'uk': ('id', 'int'),                    # id
    'login_days': ('login_days', 'int'),    # 累积登陆天数
    'reward': ('reward', 'list_3'),         # 奖励
    'des': ('des', 'unicode'),              # 描述
    'vip': ('vip', 'int'),              # 获得的vip
    'reward_show': ('reward_show', 'list_3'), # 展示奖励
}


# # 登陆翻牌
welfare_card_login = {
    'uk': ('id', 'int'),                            # 累积登陆天数
    'card_times': ('card_times', 'int'),            # 可获得的翻牌次数
    # 'reward_total': ('reward_total', 'list_4'),     # 奖励库
}


# 三顾茅庐
welfare_3days = {
    'uk': ('id', 'int'),    # 连续登陆的天数
    'day_reward': (('day1_reward', 'day2_reward', 'day3_reward'), ('list_3', 'mult_dict_1'))    # 第n天奖励
}


# 累计在线
welfare_online = {
    'uk': ('id', 'int'),                    # 奖励序列
    'reward': ('reward', 'list_3'),         # 奖励
    'online_time': ('online_time', 'int'),  # 在线时长s
}


# 等级奖励
welfare_level = {
    'uk': ('id', 'int'),                # 奖励序列
    'reward': ('reward', 'list_3'),     # 奖励
    'level': ('level', 'int'),           # 等级要求
    'reward_show': ('reward_show', 'list_3')    # 奖励展示
}


# 公告
welfare_notice = {
    'uk': ('id', 'int'),                    # 公告id
    'name': ('name', 'unicode'),            # 公告名称
    'des': ('des', 'unicode'),              # 公告内容
    'is_show': ('is_show', 'int'),          # 是否显示
    'time_sort': ('time_sort', 'int'),      # 时间类型
    'start_time': ('start_time', 'str'),    # 开始时间
    'end_time': ('end_time', 'str'),        # 结束时间
    'mark': ('mark', 'int_list'),
    'show_time': ('show_time', 'unicode'),
    'order': ('order', 'int'),
}

server_notice = {
    'uk': ('id', 'int'),                    # 公告id
    'name': ('name', 'unicode'),            # 公告名称
    'des': ('des', 'unicode'),              # 公告内容
    'is_show': ('is_show', 'int'),          # 是否显示
    'time_sort': ('time_sort', 'int'),      # 时间类型
    'start_time': ('start_time', 'str'),    # 开始时间
    'end_time': ('end_time', 'str'),        # 结束时间
    'mark': ('mark', 'int_list'),
    'show_time': ('show_time', 'unicode'),
}

scroll_bar = {
    'uk': ('id', 'int'),                    # 公告id
    'msg': ('msg', 'unicode'),            # 公告名称
}
