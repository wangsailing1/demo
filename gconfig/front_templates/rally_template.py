#! --*-- coding: utf-8 --*--

__author__ = 'sm'


# 血尘拉力赛 - 赛道
rally_main = {
    'uk': ('rally_id', 'int'),          # 赛道ID
    'name': ('name', 'unicode'),        # 名字
    'banner': ('banner', 'str'),        # 图片
    'story': ('story', 'unicode'),      # 描述
    'need_lv': ('need_lv', 'int_list'), # 开放等级
    'point_id': ('point_id', 'int_list'),    # 血沉地图点
    'reward': ('reward', 'list_3'),     # 通关奖励
    'difficulty': ('difficulty', 'int'),
}


# 事件表
rally_event = {
    'uk': ('id', 'int'),                        # 事件id
    'des': ('des', 'unicode'),                  # 事件文字
    'icon': ('icon', 'str'),
    'condition': ('condition', 'int_list'),     # "事件开启条件前置事件--道德值"
    'option': (('option1', 'option2', 'option3'), ('unicode', 'mult_dict_1')),  # 选项1文字描述
    'option_result_word': (('option1_result_word', 'option2_result_word', 'option3_result_word'), ('unicode', 'mult_dict_1')),   # 选项1文字结果
    'option_result_reward': (('option1_result_reward', 'option2_result_reward', 'option3_result_reward'), ('list_3', 'mult_dict_1')),   # 选项1奖励结果
    'option_result_buff': (('option1_result_buff', 'option2_result_buff', 'option3_result_buff'), ('int_list', 'mult_dict_1')),     # 选项1buff结果
    'option_result_value': (('option1_result_value', 'option2_result_value', 'option3_result_value'), ('int_list', 'mult_dict_1')),   # 选项1道德值结果
}


# 血沉地图表
rally_map = {
    'uk': ('id', 'int'),                            # 编号
    'map_id': ('map_id', 'int'),                    # 属于哪个地图
    'xy': ('xy', 'int_list'),                       # 点的坐标
    'stage': ('stage', 'int'),                      # 展示km数就是关卡数
    'prev_id': ('prev_id', 'int_list'),             # 该点前一个点
    'next_id': ('next_id', 'int_list'),             # 该点后一个点
    'event_type': ('event_type', 'int'),            # 该点的类型 0=不固定类型 1=玩家敌人 2=怪物 3=奖励 4=buff 5=特殊事件 6=每X关大宝箱 7=分叉点
    'event_weight': ('event_weight', 'int_list'),   # 不同类型权重
    'level': ('level', 'int_list'),                 # 等级范围
    'monster': ('monster', 'int_list'),             # 怪物池子
    'reward': ('reward', 'list_4'),                 # 奖励池子
    'buff': ('buff', 'int_list'),                   # buff池子
    'event': ('event', 'list_2'),                   # 事件池子
}

#
# # 血尘拉力赛 - 关卡配置
# rally_stage = {
#     'uk': ('stage_id', 'int'),                        # 层数
#     'enemy_level_1': ('enemy_level_1', 'int'),        # 赛道1的小怪等级
#     'enemy_level_2': ('enemy_level_2', 'int'),        # 赛道2的小怪等级
#     'enemy_level_3': ('enemy_level_3', 'int'),        # 赛道3的小怪等级
#     'enemy_level_4': ('enemy_level_4', 'int'),        # 赛道4的小怪等级
#     'enemy_level_5': ('enemy_level_5', 'int'),        # 赛道5的小怪等级
#     'reward_1': ('reward_1', 'list_3'),               # 赛道1的奖励
#     'reward_2': ('reward_2', 'list_3'),               # 赛道2的奖励
#     'reward_3': ('reward_3', 'list_3'),               # 赛道3的奖励
#     'reward_4': ('reward_4', 'list_3'),               # 赛道4的奖励
#     'reward_5': ('reward_5', 'list_3'),               # 赛道5的奖励
# }


# 玩家状态奖励
rally_buff = {
    'uk': ('id', 'int'),                    # 词缀id
    'type': ('type', 'int'),                # 生效类型
    'ispercent': ('ispercent', 'int'),      # 1为百分比乘法计算，0为固定值加法计算
    'value': ('value', 'float'),            # 效果值
    'icon': ('icon', 'str'),                # 图标
    'des': ('des', 'unicode'),              # 文字描述
}


# # 血尘拉力赛 - 关卡配置
# rally_stage_detail = {
#     'uk': ('stage_type', 'int'),                        # 关卡类型id
#     'name': ('name', 'unicode'),                # 关卡名称
#     'word': ('word', 'unicode'),                # 关卡描述
# }
#
#
# # 购买宝箱
# rally_box = {
#     'uk': ('id', 'int'),
#     'stage_id': ('stage_id', 'int'),
#     'rally_id': ('rally_id', 'int'),
#     'reward': ('reward', 'int'),
#     'random_reward': ('random_reward', 'list_4'),   # 随机奖励
#     'reward_num': ('reward_num', 'int'),            # 随机奖励数量
# }
