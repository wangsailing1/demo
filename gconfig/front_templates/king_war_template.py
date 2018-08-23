# -*- coding: utf-8 –*-

"""
Created on 2017-11-21

@author: sm
"""

# 活动相关的配置
from gconfig import check


# 赛季配置
king_war = {
    'uk': ('id', 'int'),
    'season_id': ('season_id', 'int'),            # 赛季序号
    'season_time': ('season_time', 'str'),        # 赛季时间
    'week_time': ('week_time', 'str'),            # 每周时间
    'open_time': ('open_time', 'str'),            # 开启时间
    'open_time_bronze': ('open_time_bronze', 'str'),            # 青铜开启时间
    'sort': ('sort', 'int'),                      # 类型
    'regaular_card': ('regaular_card', 'int_list'),            # 常规卡牌
    'random_card': ('random_card', 'int_list'),            # 随机卡牌
    'season_desc': ('season_desc', 'int'),            # 赛季说明
}


# 个人排名奖励
king_war_rank_person = {
    'uk': ('id', 'int'),
    'start_rank': ('start_rank', 'int'),        # 开始名次
    'end_rank': ('end_rank', 'int'),            # 结束名次
    'per_reward': ('per_reward', 'list_3'),            # 奖励
    'title': ('title', 'int'),                      # 文字
    'description': ('description', 'int'),            # 邮件内容
}


# 积分奖励
king_war_grade = {
    'uk': ('grade_lv', 'int'),
    'grade': ('grade', 'int'),        # 积分
    'grade_lv': ('grade_lv', 'int'),        # 积分等级
    'per_reward': ('per_reward', 'list_3'),            # 奖励
    'drama': ('drama', 'unicode'),            # 段位展示
    'robot': ('robot', 'int_list'),            # 机器人积分
    'rank': ('rank', 'int'),                # 段位
    'choose': ('choose', 'int'),            # "用那种选人模式 1=自由 2=不重复"
    'total_num': ('total_num', 'int'),            # 初始可选英雄的数量
    'random_num': ('random_num', 'int'),            # 几个格子

    'grade_star': ('grade_star', 'int'),            # 最高星级
    'isstar': ('isstar', 'int'),            # 输了扣星
    'islevel': ('islevel', 'int'),            # 输了掉级 1 掉，0 不掉
    'newlevel': ('newlevel', 'int'),            # 新赛季 掉到X段位
    'name': ('name', 'unicode'),
    'grade_secondlv': ('grade_secondlv', 'int'),

}


# 活跃积分奖励
king_war_active = {
    'uk': ('id', 'int'),
    'grade': ('grade', 'int'),        # 积分
    'per_reward': ('per_reward', 'list_3'),            # 奖励
    'title': ('title', 'int'),  # 奖励邮件标题
    'des': ('description', 'int'),  # 奖励邮件内容

}


# 公会排名奖励
king_war_rank_guild = {
    'uk': ('id', 'int'),
    'start_rank': ('start_rank', 'int'),        # 开始名次
    'end_rank': ('end_rank', 'int'),            # 结束名次
    'per_reward': ('per_reward', 'list_3'),            # 奖励
    'title': ('title', 'int'),                      # 文字
    'description': ('description', 'int'),            # 邮件内容
}


# 商店
king_war_shop = {
    'uk': ('shop_id', 'int'),  # 商品编号
    'show_lv': ('show_lv', 'int'),  # 出现等级
    'pos_id': ('pos_id', 'int'),  # 出售位置
    'item': (('item_sort', 'item_id', 'item_num'), ('int', 'list_3_to_list')),  # 给予物品
    'sell_sort': ('sell_sort', 'int'),  # 售价类型
    'sell_num': ('sell_num', 'int'),  # 售价
    'sell_max': ('sell_max', 'int'),  # 限购数量
    'weight': ('weight', 'int'),  # 出现权重
    'discount': ('discount', 'list_2'),  # 折扣
    'is_hot': ('is_hot', 'int'),  # 是否热卖
    'exchange_lv': ('exchange_lv', 'int'),  # 是否热卖
}


