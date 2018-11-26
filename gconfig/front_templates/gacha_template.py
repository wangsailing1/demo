#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 用户相关的配置
from gconfig import check


# 金币抽卡
coin_gacha = {
    'uk': ('id', 'int'),                    # id
    'reward': ('reward', 'list_3'),         # 物品
    'unlock_lvl': ('unlock_lvl', 'int'),    # 解锁等级
    'weight': ('weight', 'int'),            # 物品权重
    'cost': ('cost', 'int'),                # 招募点赞数
    'weight_special': ('weight_special', 'int'),            # 第几次必得英雄
}


# 金币抽卡
coin_gacha_lv = {
    'uk': ('lv', 'int'),                    # 星探等级
    # 'pvp_area': ('pvp_area', 'int'),         # 升级需要街区档次
    'count': ('count', 'int'),    # 升级需要街区招募次数
    # 'cost': ('cost', 'int_list'),  # 升级消耗
    'build_id': ('build_id', 'int'),  # 建筑id
    # 'award': ('award', 'int'),            # 升级获得的钻石
}


# 金币抽卡
coin_gacha_cd = ({
    'uk': ('time', 'int'),                    # cd 出现次数
    'cd': ('cd', 'int_list'),         # cd时长（分钟）
    'cost': ('cost', 'int_list'),         # 清除当前cd消耗
    }, 'gacha_cd_config')




# 抽卡基础表配置
gacha = {
    'uk': ('gacha_id', 'int'),                  # 抽取ID
    'consume_sort': ('consume_sort', 'int'),    # 花费类型
    'value': ('value', 'int'),                  # 价格
    'cost_quan': ('cost_quan', 'int'),          # 花费券数量
    'get_num': ('get_num', 'int'),              # 抽取次数
    'image': ('image', 'str'),                  # NPC图片
    'word': ('word', 'unicode'),                # NPC对话
    # 'prize': ('prize', 'int_list'),             # 奖池
}


# 抽卡消费等级配置
gacha_vip = {
    'uk': ('vip', 'int'),                                                           # 消费级别
    'gacha_id_silver': ('gacha_id_silver', 'int_list'),                                 # 银币
    'gacha_id_silverfree': ('gacha_id_silverfree', 'int_list'),                         # 银币免费
    'gacha_id_silver10': ('gacha_id_silver10', 'int_list'),                             # 银币十连
    'gacha_id_diamond': ('gacha_id_diamond', 'int_list'),                           # 钻石
    'gacha_id_diamondfree': ('gacha_id_diamondfree', 'int_list'),                   # 钻石免费
    'gacha_id_diamond10': ('gacha_id_diamond10', 'int_list'),                       # 钻石十连
    # 'gacha_id_diamond10th': ('gacha_id_diamond10th', 'int_list'),                   # 钻石第10次
}


# 抽卡库配置
# gacha_prize = {
#     'uk': ('id', 'int'),                        # 库id
#     'prize_team': ('prize_team', 'list_3'),     # 库内容
#     'weight': ('weight', 'int')                 # 权重
# }


# # 抽卡广告板配置
# gacha_board = {
#     'uk': ('board_id', 'int'),                        # 广告ID
#     'image': ('image', 'str'),                        # 图片
#     'start_time': ('start_time', 'str'),              # 开始时间
#     'end_time': ('end_time', 'str'),                  # 结束时间
# }


# 钻石抽卡
diamond_gacha = {
    'uk': ('id', 'int'),                                # id
    'group': ('group', 'int'),                          # 分组
    'reward': ('reward', 'list_3'),                     # 物品
    'unlock_lvl': ('unlock_lvl', 'int'),                # 解锁等级
    'weight_v0': ('weight_v0', 'int'),
    'weight_integral2': ('weight_integral2', 'int'),
    # 'weight_vip': (('weight_v0', 'weight_v1', 'weight_v2', 'weight_v3', 'weight_v4', 'weight_v5',
    #                 'weight_v12', 'weight_v13', 'weight_v14', 'weight_v15', 'weight_v16', 'weight_v17',
    #                 'weight_v18', 'weight_v19', 'weight_v20',),
    #                ('int', 'mult_dict_0')),             # vipn权重
    # 'weight_first': ('weight_first', 'int'),          # 首次
    'weight_10th': ('weight_10th', 'int'),            # 10次必得英雄
    # 'weight_first_10th': ('weight_first_10th', 'int'),     # 首次10连
    # 'weight_integral': (('weight_integral1', 'weight_integral2', 'weight_integral3',
    #                      'weight_integral4'), ('int', 'mult_dict_1')),   # 100积分库，500，1000，2000
    # 'weight_server': ('weight_server', 'int'),          # 全服库
}


# 觉醒宝箱
box_gacha = {
    'uk': ('id', 'int'),                                # id
    'group': ('group', 'int'),                          # 分组
    'reward': ('reward', 'list_3'),                     # 物品
    'unlock_lvl': ('unlock_lvl', 'int'),                # 解锁等级
    'weight_v0': ('weight_v0', 'int'),
    'weight_integral2': ('weight_integral2', 'int'),
    # 'weight_vip': (('weight_v0', 'weight_v1', 'weight_v2', 'weight_v3', 'weight_v4', 'weight_v5',
    #                 'weight_v12', 'weight_v13', 'weight_v14', 'weight_v15', 'weight_v16', 'weight_v17',
    #                 'weight_v18', 'weight_v19', 'weight_v20',),
    #                ('int', 'mult_dict_0')),             # vipn权重
    # 'weight_first': ('weight_first', 'int'),          # 首次
    'weight_10th': ('weight_10th', 'int'),            # 10次必得英雄
    # 'weight_first_10th': ('weight_first_10th', 'int'),     # 首次10连
    # 'weight_integral': (('weight_integral1', 'weight_integral2', 'weight_integral3',
    #                      'weight_integral4'), ('int', 'mult_dict_1')),   # 100积分库，500，1000，2000
    # 'weight_server': ('weight_server', 'int'),          # 全服库
    'is_show': ('is_show', 'int'),
}


# # vip抽卡系数
# vip_gacha_rate = {
#     'uk': ('vip_lvl', 'int'),                                   # vip等级
#     'diamond_gacha_rate': ('diamond_gacha_rate', 'float'),      # 钻石抽卡系数
#     'box_gacha_rate': ('box_gacha_rate', 'float'),              # 觉醒宝箱系数
# }


# 钻石抽卡积分奖励
diamond_gacha_score = {
    'uk': ('score', 'int'),                 # 积分
    'group': ('group', 'int'),              # 组别
    'reward': ('reward', 'list_3'),         # 奖励库
    'if_choose': ('if_choose', 'int'),      # 是否可选
    'choose_num': ('choose_num', 'int'),    # 可选个数
}


# 觉醒宝箱积分奖励
box_gacha_score = {
    'uk': ('score', 'int'),                 # 积分
    'group': ('group', 'int'),              # 组别
    'reward': ('reward', 'list_3'),         # 奖励库
    'if_choose': ('if_choose', 'int'),      # 是否可选
    'choose_num': ('choose_num', 'int'),    # 可选个数
}
