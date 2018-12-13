#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check

# 主城主线任务
mission_main = {
    'uk': ('id', 'int'),                                    # 编号
    'name': ('name', 'unicode'),                            # 名字
    'get_drama': ('get_drama', 'str'),                      # 领取任务对话id
    'get_board': ('get_board', 'unicode'),                  # 领取任务说明
    'start_npc': ('start_npc', 'int'),                      # 领取任务npc编号
    'start_drama': ('start_drama', 'str'),                  # 领取任务对话编号
    'sort': ('sort', 'int'),                                # 任务类型
    'target1': ('target1', 'int_list_or_int2'),             # 规则1
    'target2': ('target2', 'int'),                          # 规则2
    'finish_board': ('finish_board', 'unicode'),            # 完成任务显示说明
    'finish_npc': ('finish_npc', 'int'),                    # 完成任务npc编号
    'finish_drama': ('finish_drama', 'int'),                # 完成对话编号
    'reward': ('reward', 'list_3'),                         # 奖励
    'next_id': ('next_id', 'int'),                          # 下一个任务
    # 'mission_side': ('mission_side', 'int'),                # 开启直线任务id
    'icon': ('icon', 'str'),                                # 图标
    'mission_chapter': ('mission_chapter', 'int_list'),
}
# 支线任务
mission_side = {
    'uk': ('id', 'int'),                            # id
    'icon': ('icon', 'str'),                        # 图标
    'name': ('name', 'unicode'),                    # 任务名
    'des': ('des', 'unicode'),                      # 任务描述
    'finish_board': ('finish_board', 'unicode'),    # 完成任务显示说明
    'sort': ('sort', 'int'),                        # 任务类型
    'target1': ('target1', 'int_list_or_int2'),                  # 目标1
    'target2': ('target2', 'int'),                  # 目标2
    'reward': ('reward', 'list_3'),                 # 奖励
    'jump': ('jump', 'int_list'),                        # 跳转
    # 'next_id': ('next_id', 'ibox_gachant'),                  # 下一个任务id
    'open_id': ('open_id', 'int'),                  # 开启条件（需要完成主线任务）
    'lvl_limit': ('lvl_limit', 'int'),                  # 开启条件（需要完成主线任务）
    'side_npc': ('side_npc', 'int'),
    'start_dialogue': ('start_dialogue', 'unicode'),
    'start_des': ('start_des', 'unicode'),
}

mission_record = {
    'uk': ('mission_sort', 'int'),
    'mission_record': ('mission_record', 'int'),
}


slg_task_daily = {
    'uk': ('id', 'int'),
    'des': ('des', 'unicode'),
    'sort': ('sort', 'int'),
    'target1': ('target1', 'int'),
    'target2': ('target2', 'int'),
    'reward': ('reward', 'list_3'),
}


slg_rank_reward = {
    'uk': ('id', 'int'),
    'min': ('min', 'int'),
    'max': ('max', 'int'),
    'per_reward': ('per_reward', 'list_3'),
}


# 登录礼包
log_reward = {
    'uk': ('day', 'int'),               # 天数
    'reward': ('reward', 'list_3'),     # 奖励
    'mail': ('mail', 'unicode'),        # 邮件标题
    'mail_des': ('mail_des', 'unicode'),    # 邮件内容
    'name': ('name', 'unicode'),        # 显示
}


# 公会boss降临活动
guild_task = {
    'uk': ('id', 'int'),                # 任务id
    'des': ('des', 'unicode'),          # 描述
    'sort': ('sort', 'int'),            # 任务类型
    'target1': ('target1', 'int'),      # 目标1
    'target2': ('target2', 'int'),      # 目标2
    'get_item': ('get_item', 'int'),    # 获得的道具
    'num': ('num', 'int'),              # 获得的数量
    'reward': ('reward', 'list_3'),     # 额外奖励
    'jump': ('jump', 'int'),            # 跳转
}
person_task = {
    'uk': ('id', 'int'),                # 任务id
    'des': ('des', 'unicode'),          # 描述
    'sort': ('sort', 'int'),            # 任务类型
    'target1': ('target1', 'int'),      # 目标1
    'target2': ('target2', 'int'),      # 目标2
    'get_item': ('get_item', 'int'),    # 获得的道具
    'num': ('num', 'int'),              # 获得的数量
    'reward': ('reward', 'list_3'),     # 额外奖励
    'jump': ('jump', 'int'),            # 跳转
}
score_reward = {
    'uk': ('id', 'int'),                    # id
    'version': ('version', 'int'),          # 版本
    'start_time': ('start_time', 'str'),    # 开始时间
    'end_time': ('end_time', 'str'),        # 结束时间
    'rank': ('rank', 'int'),                # 积分档次
    'score': ('score', 'int'),              # 积分
    'reward': ('reward', 'int_list'),       # 奖励
    'show_card': ('show_card', 'list_3'),   # 主页展示的卡
    'notice': ('notice', 'unicode'),        #
    'server_id': ('server_id', 'int_list'), # 服id
}
rank_reward = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'rank': ('rank', 'int_list'),               # 排名
    'least_score': ('least_score', 'int'),      # 最低积分
    'reward_time': ('reward_time', 'str'),      # 发奖时间
    'reward': ('reward', 'list_3'),           # 奖励
    # 'mail_title': ('mail_title', 'unicode'),    # 邮件title
    # 'mail': ('mail', 'unicode'),                # 邮件内容
    'last_rank': ('last_rank', 'int'),          #
}
# score_reward_pool = {
#     'uk': ('id', 'int'),                # id
#     'reward': ('reward', 'list_3',),   # 奖励
#     'num': ('num', 'int'),              # 奖励数量
# }


# 主线任务
task_main = {
    'uk': ('id', 'int'),
    'icon': ('icon', 'str'),            # 图标
    'name': ('name', 'unicode'),        # 任务名
    'des': ('des', 'unicode'),          # 任务描述
    'task': ('task', 'int_list'),       # 目标子任务
    'reward': ('reward', 'list_3'),     # 获得奖励
}


# 主线任务描述
task_main_detail = {
    'uk': ('id', 'int'),
    'des': ('des', 'unicode'),      # 任务描述
    'sort': ('sort', 'int'),        # 任务类型
    'target1': ('target1', 'int'),  # 需求目标1
    'target2': ('target2', 'int'),  # 需求目标2
    'jump': ('jump', 'int_list_or_int'),   # 跳转
}


# 宇宙最强
super_all = {
    'uk': ('version', 'int'),
    'start_time': ('start_time', 'str'),
    'end_time': ('end_time', 'str'),
    'end_time_show': ('end_time_show', 'str'),
    'server_id': ('server_id', 'int_list'),
    'score': ('score', 'mult_dict_1'),
    'base': ('base', 'int'),
    'reward': ('reward', 'mult_dict_1'),
    'show_reward': ('show_reward', 'list_3'),
    'shop_id': ('shop_id', 'int'),
    'shop_price': ('shop_price', 'int'),
    'item_id': ('item_id', 'int'),
    'show': ('show', 'unicode'),
    'notice': ('notice', 'unicode'),
    'des': ('des', 'unicode'),
    'mail': ('mail', 'unicode'),
    'mail_des': ('mail_des', 'unicode'),
}
super_rich = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'rank': ('rank', 'int_list'),
    'start_time': ('start_time', 'str'),
    'end_time': ('end_time', 'str'),
    'reward_12': ('reward_12', 'list_3'),
    'reward_21': ('reward_21', 'list_3'),
    'reward_23': ('reward_23', 'list_3'),
    'notice': ('notice', 'unicode'),
    'des': ('des', 'unicode'),
    'mail': ('mail', 'unicode'),
    'mail_des': ('mail_des', 'unicode'),
}


# 运营活动弹板
shoot_plank = {
    'uk': ('id', 'int'),
    'show_id': ('show_id', 'int'),
    'vip': ('vip', 'int_list'),
}


server_shoot_plank = shoot_plank


# 随机任务
task_random = {
    'uk': ('id', 'int'),
    'icon': ('icon', 'str'),            # 图标
    'name': ('name', 'unicode'),        # 任务名
    'des': ('des', 'unicode'),          # 任务描述
    'rate': ('rate', 'int'),            # 权重
    'quality': ('quality', 'int'),      # 任务级别
    'open_sort': ('open_sort', 'int'),  # 开启类型
    'open_data': ('open_data', 'int'),  # 开启条件
    'sort': ('sort', 'int'),            # 任务类型
    'target1': ('target1', 'int'),      # 达成目标1
    'target2': ('target2', 'int'),      # 达成目标2
    'reward': ('reward', 'list_3'),     # 获得奖励
    'jump': ('jump', 'int_list'),       # 跳转
}


# 阶段成就
achievement = {
    'uk': ('id', 'int'),
    'start_id': ('start_id', 'int'),    # 起始
    'next_id': ('next_id', 'int'),      # 下一步对应
    'icon': ('icon', 'str'),            # 图标
    'name': ('name', 'unicode'),        # 成就名
    'des': ('des', 'unicode'),          # 成就描述
    'sort': ('sort', 'int'),            # 成就类型
    'target1': ('target1', 'int'),      # 成就需求1
    'target2': ('target2', 'int'),      # 成就需求2
    'reward': ('reward', 'list_3'),     # 获得奖励
    'jump': ('jump', 'int_list'),       # 跳转
    'building_id': ('building_id', 'int'),     # 建筑功能id
}


# 收集功能
achievement_collection = {
    'uk': ('id', 'int'),
    'tag': ('tag', 'int'),              # 分类
    'show': ('show', 'int'),            # 显示顺序
    'name': ('name', 'unicode'),        # 收集名
    'need': ('need', 'int_list'),       # 收集内容
    'reward': ('reward', 'list_3'),     # 获得奖励
    'jump': ('jump', 'int_list'),       # 跳转
}


# 每日任务
task_daily = {
    'uk': ('id', 'int'),            # 任务编号
    'icon': ('icon', 'str'),        # 图标
    'name': ('name', 'unicode'),    # 任务名
    'des': ('des', 'unicode'),      # 任务描述
    'quality': ('quality', 'int'),  # 任务级别
    'level': ('level', 'int'),
    'sort': ('sort', 'int'),        # 成就类型
    'target1': ('target1', 'int'),  # 成就需求1
    'target2': ('target2', 'int'),  # 成就需求2
    'first_reward': ('first_reward', 'list_3'),  # 首日奖励
    'reward': ('reward', 'list_3'),  # 获得奖励
    'point': ('point', 'int'),      # 活跃度
    'jump': ('jump', 'int_list'),  # 跳转
}


# 每日任务奖励
task_daily_reward = {
    'uk': ('id', 'int'),                   # 奖励编号
    'need_point': ('need_point', 'int'),   # 需要活跃度
    'reward': ('reward', 'list_3'),        # 奖励
    'isday': ('isday', 'int'),              # 0：日活跃，1：周活跃
}


# 招财猫
diamond_get = {
    'uk': ('id', 'int'),                 # 活动id
    'version': ('version', 'int'),              # 活动版本号
    'start_time': ('start_time', 'str'),        # 活动开始时间
    'end_time': ('end_time', 'str'),            # 活动结束时间
    'id': ('id', 'int'),                        # 档位的id
    'coin': ('coin', 'int'),                    # 需要的钻石
    'get_coin_max': ('get_coin_max', 'int'),    # 最高可获得的钻石
    # 'get_coin': ('get_coin', 'list_3'),       # 获得钻石范围
    'vip': ('vip', 'int'),                      # 需要的vip等级
    'show_time': ('show_time', 'unicode'),        # 展示时间
    'server': ('server', 'int_list'),           # 不填是新老服都开，2是只有老服开
    'channel_id': ('channel_id', 'int_list'),   # 填渠道id，填谁谁开，不填全开
    'no_server_id': ('no_server_id', 'int_list'),     # 写谁谁不开
}


# 新服招财猫
server_diamond_get = {
    'uk': ('id', 'int'),                 # 活动id
    'version': ('version', 'int'),              # 活动版本号
    'start_time': ('start_time', 'str'),        # 活动开始时间
    'end_time': ('end_time', 'str'),            # 活动结束时间
    'id': ('id', 'int'),                        # 档位的id
    'coin': ('coin', 'int'),                    # 需要的钻石
    'get_coin_max': ('get_coin_max', 'int'),    # 最高可获得的钻石
    # 'get_coin': ('get_coin', 'list_3'),       # 获得钻石范围
    'vip': ('vip', 'int'),                      # 需要的vip等级
    'show_time': ('show_time', 'unicode'),        # 展示时间
    'server_id': ('server_id', 'int_list'),     # 新老服
}


# 零用钱银行
invest = {
    'uk': ('version', 'int'),                  # 版本号
    'start_time': ('start_time', 'str'),            # 开始时间
    'end_time': ('end_time', 'str'),                # 结束时间
    'free_times': ('free_times', 'int'),            # 免费次数
    'need_item': ('need_item', 'int'),              # 需要道具id
    'charge_reward1': ('charge_reward1', 'list_3'),    # 第一级奖励
    'charge_reward2': ('charge_reward2', 'list_3'),    # 第二级奖励
    'charge_reward3': ('charge_reward3', 'list_3'),    # 第三级奖励
    'charge_reward4': ('charge_reward4', 'list_3'),    # 第四级奖励
    'max_coin': ('max_coin', 'int'),                # 最终需要的积分总数
    'step_coin': ('step_coin', 'int'),              # 每一级需要的积分数
    'time1': ('time1', 'int'),                      # 对应期限（h）
    'time2': ('time2', 'int'),                      # 对应期限（h）
    'time3': ('time3', 'int'),                      # 对应期限（h）
    'coin_point1': ('coin_point1', 'int_list'),          # 回报率百分比，区间
    'coin_point2': ('coin_point2', 'int_list'),          # 回报率百分比，区间
    'coin_point3': ('coin_point3', 'int_list'),          # 回报率百分比，区间
    'quickly_point': ('quickly_point', 'int'),      # 快速领取时，扣掉的钻石的比率
    'des1': ('des1', 'unicode'),                        # 文字
    'refresh_coin': ('refresh_coin', 'int_list'),        # 刷新需要的钻石数，单个的数值
    'show_time': ('show_time', 'unicode'),        # 展示时间
}
invest_rate = {
    'uk': ('active_id', 'int'),                  # 活动id
    'version': ('version', 'int'),                      # 版本号
    'id': ('id', 'int'),                                # 钻石的档位序号
    'limit': ('limit', 'int'),                          # 刷新时玩家身上钻石与该值比较
    'coin_down': ('coin_down', 'list_3'),                  # 玩家钻石小于limit
    'refresh_rate_down': ('refresh_rate_down', 'list_3'),  # 小于limit回报率
    'coin_up': ('coin_up', 'list_3'),                      # 玩家钻石大于limit
    'refresh_rate_up': ('refresh_rate_up', 'list_3'),      # 玩家钻石大于limit
}


# 零用钱银行
server_invest = {
    'uk': ('version', 'int'),                  # 版本号
    'start_time': ('start_time', 'str'),            # 开始时间
    'end_time': ('end_time', 'str'),                # 结束时间
    'free_times': ('free_times', 'int'),            # 免费次数
    'need_item': ('need_item', 'int'),              # 需要道具id
    'charge_reward1': ('charge_reward1', 'list_3'),    # 第一级奖励
    'charge_reward2': ('charge_reward2', 'list_3'),    # 第二级奖励
    'charge_reward3': ('charge_reward3', 'list_3'),    # 第三级奖励
    'charge_reward4': ('charge_reward4', 'list_3'),    # 第四级奖励
    'max_coin': ('max_coin', 'int'),                # 最终需要的积分总数
    'step_coin': ('step_coin', 'int'),              # 每一级需要的积分数
    'time1': ('time1', 'int'),                      # 对应期限（h）
    'time2': ('time2', 'int'),                      # 对应期限（h）
    'time3': ('time3', 'int'),                      # 对应期限（h）
    'coin_point1': ('coin_point1', 'int_list'),          # 回报率百分比，区间
    'coin_point2': ('coin_point2', 'int_list'),          # 回报率百分比，区间
    'coin_point3': ('coin_point3', 'int_list'),          # 回报率百分比，区间
    'quickly_point': ('quickly_point', 'int'),      # 快速领取时，扣掉的钻石的比率
    'des1': ('des1', 'unicode'),                        # 文字
    'refresh_coin': ('refresh_coin', 'int_list'),        # 刷新需要的钻石数，单个的数值
    'show_time': ('show_time', 'unicode'),        # 展示时间
    'server_id': ('server_id', 'int_list'),
}
server_invest_rate = {
    'uk': ('active_id', 'int'),                  # 活动id
    'version': ('version', 'int'),                      # 版本号
    'id': ('id', 'int'),                                # 钻石的档位序号
    'limit': ('limit', 'int'),                          # 刷新时玩家身上钻石与该值比较
    'coin_down': ('coin_down', 'list_3'),                  # 玩家钻石小于limit
    'refresh_rate_down': ('refresh_rate_down', 'list_3'),  # 小于limit回报率
    'coin_up': ('coin_up', 'list_3'),                      # 玩家钻石大于limit
    'refresh_rate_up': ('refresh_rate_up', 'list_3'),      # 玩家钻石大于limit
}


# 每日礼包
daily_reward = {
    'uk': ('week', 'int'),                      # 周一到周日，1-7
    'reward': ('reward', 'list_3'),             # 奖励
    'des': ('des', 'unicode'),                  # 奖励描述
    # 'server_id1': ('server_id1', 'int_list'),   # 服务器id，区间表示
    # 'server_id2': ('server_id2', 'int_list'),   # 服务器id，个数表示
}
# buy_reward = {
#     'uk': ('id', 'int'),                    # id
#     'show_id': ('show_id', 'int'),          # 上一个页签对应的礼包类型
#     'demand': ('demand', 'int'),            # 购买需求，1是充值，2是花费钻石
#     'level': ('level', 'int_list'),         # 指玩家等级区间，格式1,40
#     'reward': ('reward', 'list_4'),         # 奖励
#     'reward_num': ('reward_num', 'int'),    # 随机数量
# }


# 首充
first_recharge = {
    'uk': ('id', 'int'),            # 充值id
    'price_CN': ('price_CN', 'int'),      # 所需rmb
    'price_TW': ('price_TW', 'float'),    # 所需美元
    'name': ('name', 'unicode'),    # 名字
    'time': ('time', 'int'),        # 领取倒计时
    'gift': ('gift', 'list_3'),     # 领取奖励
    'story': ('story', 'unicode'),  # 描述
    # 'type': ('type', 'int'),      # 类型 0是任意金额，1是累计的，2是单笔的
}


# 星芒法阵
points_exchange = {
    'uk': ('id', 'int'),                    # id
    'version': ('version', 'int'),          # 版本号
    'start_time': ('start_time', 'str'),    # 开始时间
    'end_time': ('end_time', 'str'),        # 结束时间
    'cost_points': ('cost_points', 'int'),  # 花费积分
    'reward': ('reward', 'list_3'),         # 获得奖励
    'final_reward': ('final_reward', 'list_3'),     # 终极大奖
}
star_task = {
    'uk': ('id', 'int'),            # 任务id
    'des': ('des', 'unicode'),      # 任务描述
    'sort': ('sort', 'int'),        # 任务类型
    'target1': ('target1', 'int'),  # 任务目标1
    'target2': ('target2', 'int'),  # 任务目标2
    'points': ('points', 'int'),    # 获得积分
    'reward': ('reward', 'list_3', check.check_reward()),   # 额外奖励
    'jump': ('jump', 'int'),        # 跳转
}


# 新服星芒法阵
server_points_exchange = {
    'uk': ('id', 'int'),                    # id
    'version': ('version', 'int'),          # 版本号
    'start_time': ('start_time', 'str'),    # 开始时间
    'end_time': ('end_time', 'str'),        # 结束时间
    'cost_points': ('cost_points', 'int'),  # 花费积分
    'reward': ('reward', 'list_3'),         # 获得奖励
    'final_reward': ('final_reward', 'list_3'),     # 终极大奖
}
server_star_task = {
    'uk': ('id', 'int'),            # 任务id
    # 'des': ('des', 'unicode'),      # 任务描述
    'sort': ('sort', 'int'),        # 任务类型
    'target1': ('target1', 'int'),  # 任务目标1
    'target2': ('target2', 'int'),  # 任务目标2
    'points': ('points', 'int'),    # 获得积分
    'reward': ('reward', 'list_3', check.check_reward()),   # 额外奖励
    # 'jump': ('jump', 'int'),        # 跳转
}

# 累计消耗
active_consume = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),      # 展示时间
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),        # 开始时间
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),            # 结束时间
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
active_daily_consume = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),      # 展示时间
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),        # 开始时间
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),            # 结束时间
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
active_recharge = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),      # 展示时间
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),        # 开始时间
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),            # 结束时间
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

# 每日充值活动
active_daily_recharge = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'show_time': ('show_time', 'unicode'),      # 展示时间
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),        # 开始时间
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),            # 结束时间
    'num': ('num', 'float'),                      # 数值
    'reward_show': ('reward_show', 'list_3', check.check_reward(),),   # 奖品
    'level': ('level', 'int_list'),             # 展示大奖
    'reward': ('reward', 'list_3', check.check_reward(),),             # 等级
    'server_id': ('server_id', 'int_list'),     # 服务器id
    'mail_title': ('mail_title', 'unicode'),    # 邮件名
    'des': ('des', 'unicode'),                  # 邮件内容描述
    'num_type': ('num_type', 'int'),            # 计数类型
    'currency': ('currency', 'str'),            # 币种
    'currency_name': ('currency_name', 'unicode'),     # 种名
    'daily_reward': ('daily_reward', 'list_3', check.check_reward()),     # 累充（单充）补给奖励
    'show_des': ('show_des', 'unicode'),
}

# 常规兑换活动
normal_exchange = {
    'uk': ('id', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'version': ('version', 'int'),              # version
    'show_time': ('show_time', 'unicode'),       # 展示时间
    'type': ('type', 'int'),                    # 兑换类型
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),        # 开始时间
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),            # 结束时间
    'exchange_num': ('exchange_num', 'int'),    # 可兑换次数
    'need_item': ('need_item', 'list_3', check.check_reward(),),       # 兑换道具
    'out_item': ('out_item', 'list_3', check.check_reward(),),         # 兑换得到的奖品
    'show_des': ('show_des', 'unicode'),
}

# 限时兑换活动
omni_exchange = {
    'uk': ('id', 'int'),
    'show_id': ('show_id', 'int'),              # 展示id
    'version': ('version', 'int'),              # version
    'show_time': ('show_time', 'unicode'),       # 展示时间
    'exchange_type': ('exchange_type', 'int'),  # 兑换类型
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),        # 开始时间
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),            # 结束时间
    'exchange_num': ('exchange_num', 'int'),    # 可兑换次数
    'need_item': ('need_item', 'list_3', check.check_reward(),),       # 兑换道具
    'out_item': ('out_item', 'list_3', check.check_reward(),),         # 兑换得到的奖品
    'reward_show': ('reward_show', 'list_3', check.check_reward(),),   # 大奖
    'show_des': ('show_des', 'unicode'),
}

# 限时兑换活动
sign_daily_charge = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),               # 版本号
    'show_time': ('show_time', 'unicode'),       # 展示时间
    'start_time': ('start_time', 'str'),         # 开始时间
    'end_time': ('end_time', 'str'),             # 结束时间
    'day': ('day', 'int'),                       # 天数
    'reward': ('reward', 'list_3'),              # 奖励
    'show_reward': ('show_reward', 'list_3'),    # 展示的奖励
    'pay': ('pay', 'int'),                       # 签到所需金额
    'pay_sort': ('pay_sort', 'int'),             # 记录支付的种类
    'final_reward': ('final_reward', 'list_3'),  # 最终大奖
    'des': ('des', 'unicode'),                   # 大奖描述
}


# 每日礼包
gift_show = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),               # 版本号
    'show': ('show', 'int'),    # 是否展示
    'show_id': ('show_id', 'int'),    # 展示顺序
    'time_show': ('time_show', 'str'),    # 展示时间
    'start_time': ('start_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),         # 开始时间
    'end_time': ('end_time', 'str', check.check_time(tformat="%Y-%m-%d %H:%M:%S"),),             # 结束时间
    'name': ('name', 'unicode'),    # 标签名字
    'reward': ('reward', 'list_3', check.check_reward(),),              # 奖励
    'daily_reward': ('daily_reward', 'list_3', check.check_reward()),  # 今日福利
    'charge': ('charge', 'int'),    # 充值对应项
    'show_des': ('show_des', 'unicode'),  # 大奖描述
}

# 活动展示
active_show = {
    'uk': ('id', 'int'),
    'sort': ('sort', 'int'),                    # 标签id
    'level': ('level', 'int_list'),             # 等级
    'show_time': ('show_time', 'str'),        # 开始时间
    'server_id': ('server_id', 'int_list'),     # 服务器id
    'show_id': ('show_id', 'int'),              # 展示顺序
    'mark': ('mark', 'int'),                    # 标志
    'banner': ('banner', 'unicode'),            # 名字
}

# 招募活动
gacha_reward_hero = {
    'uk': ('id', 'int'),
    'hero_id': ('hero_id', 'int'),       # 英雄id
    'name': ('name', 'unicode'),         # 英雄名字
    'reward': ('reward', 'list_3'),      # 奖励
    'days': ('days', 'int'),             # 持续时间
}

# 抽卡活动
gacha_reward = {
    'uk': ('id', 'int'),
    'type': ('type', 'int'),             # 抽卡种类
    'num': ('num', 'int'),               # 次数
    'reward': ('reward', 'list_3'),      # 奖励
    'days': ('days', 'int'),             # 持续时间
}

# 季卡月卡活动
month_card = {
    'uk': ('card_type', 'int'),
    'card_name': ('card_name', 'unicode'),             # 抽卡种类
    'price_CN': ('price_CN', 'float'),               # 价格，前端用
    'price_TW': ('price_TW', 'float'),               # 价格，前端用
    'daily_rebate': ('daily_rebate', 'list_3'),      # 奖励
    'price_show': ('price_show', 'int'),             # 持续时间
    'effective_days': ('effective_days', 'int'),
    'reward_show': ('reward_show', 'int'),
    'immediate_rebate': ('immediate_rebate', 'list_3'),
    'mail_title_immediate': ('mail_title_immediate', 'unicode'),
    'mail_immediate': ('mail_immediate', 'unicode'),
}


# 运营活动开关
active_inreview = {
    'uk': ('id', 'int'),                        # 对应入口
    'is_open': ('is_open', 'int'),              # 是否开启
    'show_lv': ('show_lv', 'int'),              # 开启等级
    # 'server_id': ('server_id', 'int_list'),     # 开启服务器
    'server_new': ('server_new', 'int'),        # 新老服开启服务器
    'show_time': ('show_time', 'str'),          # 开启时间
}


# 限时武器之魂
limit_weapon = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'start_time': ('start_time', 'str'),        # 开始时间
    'end_time': ('end_time', 'str'),            # 结束时间
    'reward_show': ('reward_show', 'list_3'),   # 大奖展示
    'reward': ('reward', 'list_4'),             # 奖励
    'num': ('num', 'int'),                      # 数量
    'show_card': ('show_card', 'str'),          # banner
    'server_id': ('server_id', 'int_list'),     # 开启服务器
    'server': ('server', 'int_list'),           # 新老服
    'one_time': ('one_time', 'int'),            # 单次抽卡花费
    'five_times': ('five_times', 'int'),        # 五次抽卡花费
}

# 限时武器之魂伪概率奖励
limit_box_reward = {
    'uk': ('ID', 'int'),                        # id
    'reward': ('reward', 'list_3'),             # 奖励
    'num': ('num', 'int_list'),                 # 开箱次数
    'version': ('version', 'int'),              # 版本号
}


limit_box_shop = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'need_item': ('need_item', 'list_3', check.check_reward()),
    'out_item': ('out_item', 'list_3', check.check_reward()),
    'times': ('times', 'int'),
}

# 限时武器之魂
limit_hero_score = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'start_time': ('start_time', 'str'),        # 开始时间
    'end_time': ('end_time', 'str'),            # 结束时间
    'end_time_show': ('end_time_show', 'str'),  # 展示用结束时间
    'rank': ('rank', 'int'),                    # 排名
    'score': ('score', 'int'),                  # 积分
    'one_time': ('one_time', 'int'),                    # 一次花费
    'ten_times': ('ten_times', 'int'),                  # 十次花费
    'reward': ('reward', 'list_3'),             # 奖励
    'banner_notice': ('banner_notice', 'unicode'),  # 按钮上的话
    'show_card': ('show_card', 'list_3'),       # 奖励
    'notice': ('notice', 'unicode'),            # 活动规则
    'mail_title': ('mail_title', 'unicode'),    # 单次抽卡花费
    'mail': ('mail', 'unicode'),                # 五次抽卡花费
    'server': ('server', 'int_list'),           # 不填是新老服都开，2是只有老服开
    'channel_id': ('channel_id', 'int_list'),   # 填渠道id，填谁谁开，不填全开
    'no_server_id': ('no_server_id', 'int_list'),     # 写谁谁不开
}

# 限时英雄积分排行奖励
limit_hero_rank = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'rank': ('rank', 'int_list'),                    # 排名
    'least_score': ('least_score', 'int'),      # 积分
    'vip': ('vip', 'int'),                      # 排名
    'last_rank': ('last_rank', 'int'),                      # 排名
    'power': ('power', 'int'),                  # 排名
    'reward_time': ('reward_time', 'str'),      # 发奖时间
    'reward': ('reward', 'list_3'),             # 奖励
    'mail_title': ('mail_title', 'unicode'),    # 邮件标题
    'mail': ('mail', 'unicode'),                # 邮件内容
}

# 限时英雄十连额外奖励
limit_card_chip = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'num': ('num', 'int'),                      # 排名
    'chip_reward': ('chip_reward', 'list_4'),   # 奖励
}

# 限时英雄抽卡池
limit_diamond_gacha = {
    'uk': ('id', 'int'),                                # id
    'reward': ('reward', 'list_3'),                     # 物品
    'unlock_lvl': ('unlock_lvl', 'int'),                # 解锁等级
    'weight_vip': (('weight_v0', 'weight_v1', 'weight_v2', 'weight_v3', 'weight_v4', 'weight_v5',
                    'weight_v6', 'weight_v7', 'weight_v8', 'weight_v9', 'weight_v10', 'weight_v11',
                    'weight_v12', 'weight_v13', 'weight_v14', 'weight_v15'),
                   ('int', 'mult_dict_0')),             # vipn权重
    'weight_10th': ('weight_10th', 'int'),            # 10次必得英雄
}

# 魂匣
limit_gacha = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'type': ('type', 'int'),                    # 单英雄或爽英雄标识
    'start_time': ('start_time', 'str'),        # 开始时间
    'end_time': ('end_time', 'str'),            # 结束时间
    'normal_hero': ('normal_hero', 'list_3'),   # 奖励
    'reward_hero': ('reward_hero', 'list_3'),   # 大奖展示
    'reward': ('reward', 'list_4'),             # 奖池
    'num': ('num', 'int'),                      # 数量
    'server_id': ('server_id', 'int_list'),     # 开启服务器
    'server': ('server', 'int_list'),           # 新老服
    'one_time': ('one_time', 'int'),            # 单次抽卡花费
    'five_times': ('five_times', 'int'),        # 五次抽卡花费
    'reward_show': ('reward_show', 'str'),      # 五次抽卡花费
    'vip': ('vip', 'int'),                      # VIP等级
    'level': ('level', 'int'),                  # 等级
    'background': ('background', 'str'),
}

# 魂匣伪概率奖励
extra_hero = {
    'uk': ('ID', 'int'),                        # id
    'reward': ('reward', 'list_3'),             # 奖励
    'num': ('num', 'int_list'),                 # 开箱次数
    'version': ('version', 'int'),              # 版本号
    'hot': ('hot', 'int'),                      # 大奖英雄标识
}

# 前段用
hero_description = {
    'uk': ('ID', 'int'),                        # id
    'hero_id': ('hero_id', 'list_3'),             # 奖励
    'position': ('position', 'unicode'),                 # 开箱次数
    'introduction': ('introduction', 'unicode'),              # 版本号
}

# 限时武器之魂
server_limit_weapon = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'start_time': ('start_time', 'str'),        # 开始时间
    'end_time': ('end_time', 'str'),            # 结束时间
    'reward_show': ('reward_show', 'list_3'),   # 大奖展示
    'reward': ('reward', 'list_4'),             # 奖励
    'num': ('num', 'int'),                      # 数量
    'show_card': ('show_card', 'str'),          # banner
    # 'server_id': ('server_id', 'int_list'),     # 开启服务器
    # 'server': ('server', 'int_list'),           # 新老服
    'one_time': ('one_time', 'int'),            # 单次抽卡花费
    'five_times': ('five_times', 'int'),        # 五次抽卡花费
}

# 限时武器之魂伪概率奖励
server_limit_box_reward = {
    'uk': ('ID', 'int'),                        # id
    'reward': ('reward', 'list_3'),             # 奖励
    'num': ('num', 'int_list'),                 # 开箱次数
    'version': ('version', 'int'),              # 版本号
}


server_limit_box_shop = limit_box_shop

# 限时武器之魂
server_limit_hero_score = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'start_time': ('start_time', 'str'),        # 开始时间
    'end_time': ('end_time', 'str'),            # 结束时间
    'end_time_show': ('end_time_show', 'str'),  # 展示用结束时间
    'rank': ('rank', 'int'),                    # 排名
    'score': ('score', 'int'),                  # 积分
    'one_time': ('one_time', 'int'),                    # 一次花费
    'ten_times': ('ten_times', 'int'),                  # 十次花费
    'reward': ('reward', 'list_3'),             # 奖励
    'banner_notice': ('banner_notice', 'unicode'),  # 按钮上的话
    'show_card': ('show_card', 'list_3'),       # 奖励
    'notice': ('notice', 'unicode'),            # 活动规则
    # 'server_id': ('server_id', 'int_list'),     # 开启服务器
    # 'server': ('server', 'int_list'),           # 新老服
    'mail_title': ('mail_title', 'unicode'),    # 单次抽卡花费
    'mail': ('mail', 'unicode'),                # 五次抽卡花费
}

# 限时英雄积分排行奖励
server_limit_hero_rank = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'rank': ('rank', 'int_list'),                    # 排名
    'least_score': ('least_score', 'int'),      # 积分
    'vip': ('vip', 'int'),                      # 排名
    'last_rank': ('last_rank', 'int'),                      # 排名
    'power': ('power', 'int'),                  # 排名
    'reward_time': ('reward_time', 'str'),      # 发奖时间
    'reward': ('reward', 'list_3'),             # 奖励
    # 'mail_title': ('mail_title', 'unicode'),    # 邮件标题
    # 'mail': ('mail', 'unicode'),                # 邮件内容
}

# 限时英雄十连额外奖励
server_limit_card_chip = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'num': ('num', 'int'),                      # 排名
    'chip_reward': ('chip_reward', 'list_4'),   # 奖励
}

# 限时英雄抽卡池
server_limit_diamond_gacha = {
    'uk': ('id', 'int'),                                # id
    'reward': ('reward', 'list_3'),                     # 物品
    'unlock_lvl': ('unlock_lvl', 'int'),                # 解锁等级
    'weight_vip': (('weight_v0', 'weight_v1', 'weight_v2', 'weight_v3', 'weight_v4', 'weight_v5',
                    'weight_v6', 'weight_v7', 'weight_v8', 'weight_v9', 'weight_v10', 'weight_v11',
                    'weight_v12', 'weight_v13', 'weight_v14', 'weight_v15'),
                   ('int', 'mult_dict_0')),             # vipn权重
    'weight_10th': ('weight_10th', 'int'),            # 10次必得英雄
}

# 魂匣
server_limit_gacha = {
    'uk': ('id', 'int'),                        # id
    'version': ('version', 'int'),              # 版本
    'type': ('type', 'int'),                    # 单英雄或爽英雄标识
    'start_time': ('start_time', 'str'),        # 开始时间
    'end_time': ('end_time', 'str'),            # 结束时间
    'normal_hero': ('normal_hero', 'list_3'),   # 奖励
    'reward_hero': ('reward_hero', 'list_3'),   # 大奖展示
    'reward': ('reward', 'list_4'),             # 奖池
    'num': ('num', 'int'),                      # 数量
    # 'server_id': ('server_id', 'int_list'),     # 开启服务器
    # 'server': ('server', 'int_list'),           # 新老服
    'one_time': ('one_time', 'int'),            # 单次抽卡花费
    'five_times': ('five_times', 'int'),        # 五次抽卡花费
    'reward_show': ('reward_show', 'str'),        # 五次抽卡花费
    'vip': ('vip', 'int'),                      # VIP等级
    'level': ('level', 'int'),                  # 等级
    'background': ('background', 'str'),
}

# 魂匣伪概率奖励
server_extra_hero = {
    'uk': ('ID', 'int'),                        # id
    'reward': ('reward', 'list_3'),             # 奖励
    'num': ('num', 'int_list'),                 # 开箱次数
    'version': ('version', 'int'),              # 版本号
    'hot': ('hot', 'int'),                      # 大奖英雄标识
}


# 前段用
server_hero_description = {
    'uk': ('ID', 'int'),                        # id
    'hero_id': ('hero_id', 'list_3'),             # 奖励
    'position': ('position', 'unicode'),                 # 开箱次数
    'introduction': ('introduction', 'unicode'),              # 版本号
}


ban_ip = {
    'uk': ('ip', 'str'),
    'expire': ('expire', 'str'),
    'reason': ('reason', 'unicode'),
}

honor_shop_new = {
    'uk': ('shop_id', 'int'),
    'page': ('page', 'int'),                 # 标签页
    'pagetitle': ('pagetitle', 'unicode'),   # 标签页文字
    'pos_id': ('pos_id', 'int'),             # 出售位置
    'show_lv': ('show_lv', 'int'),           # 出现等级
    'sell_max': ('sell_max', 'int'),         # 每日限购次数
    'need_item': ('need_item', 'list_3'),    # 兑换道具
    'out_item': ('out_item', 'list_3'),      # 兑换得到的奖品
}


# 新人首周签到
sign_first_week = {
    'uk': ('day', 'int'),               # 日
    'reward': ('reward', 'list_3'),     # 奖励
    'des': ('des', 'unicode'),          # 描述
}


# 每月签到
sign_daily_normal = {
    'uk': ('day', 'int'),               # 每月签到日期
    'reward': ('reward', 'list_3'),     # 每月签到奖励
    'extra_reward': ('extra_reward', 'list_3'),     # 每月签到奖励
}

# 活动时间配置
active = {
    'uk':               ('id',              'int'),     # 序号
    'active_version':   ('active_version',  'int'),     # 版本号
    'start_time':       ('start_time',      'str'),     # 开始时间
    'end_time':         ('end_time',        'str'),     # 结束时间
    'active_type':      ('active_type',     'int'),     # 活动类型
    'param1':           ('param1',          'int'),     # 参数1
    'param2':           ('param2',          'int'),     # 参数2
    'param3':           ('param3',          'int'),     # 参数3
}