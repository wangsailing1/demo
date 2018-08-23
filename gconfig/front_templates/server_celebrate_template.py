#! --*-- coding: utf-8 --*--

# 活动相关的配置


# 等级排行榜活动
rank_reward_show = {
    'uk': ('id', 'int'),                            # 编号
    'sort': ('sort', 'int'),                        # sort
    'level': ('level', 'int_list'),                 # 等级
    'show_id': ('show_id', 'int'),                  # 展示顺序
    'mark': ('mark', 'int'),                        # 标记
    'show_time': ('show_time', 'str'),              # 展示时间
    'banner': ('banner', 'unicode'),                # 名字
}


# 等级排行榜活动
level_rank = {
    'uk': ('id', 'int'),                             # 编号
    'show_time': ('show_time', 'unicode'),           # 展示时间
    'start_time': ('start_time', 'str'),             # 开始时间
    'end_time': ('end_time', 'str'),                 # 结束时间
    'rank': ('rank', 'int_list'),                    # 排名
    'reward': ('reward', 'list_3'),                  # 奖励
    'mail': ('mail', 'unicode'),                     # 邮件标题
    'des': ('des', 'unicode'),                       # 邮件内容
    'story': ('story', 'unicode'),  # 邮件内容
}


# 等级排行榜奖励
level_reward = {
    'uk': ('id', 'int'),                            # id
    'level': ('level', 'int'),                      # 等级
    'gift': ('gift', 'list_3'),                     # 奖励
}


# 战力排行榜活动
combat_rank = {
    'uk': ('id', 'int'),                             # 编号
    'show_time': ('show_time', 'unicode'),           # 展示时间
    'start_time': ('start_time', 'str'),             # 开始时间
    'end_time': ('end_time', 'str'),                 # 结束时间
    'rank': ('rank', 'int_list'),                    # 排名
    'reward': ('reward', 'list_3'),                  # 奖励
    'mail': ('mail', 'unicode'),                     # 邮件标题
    'des': ('des', 'unicode'),                       # 邮件内容
    'story': ('story', 'unicode'),
}


# 战力排行榜奖励
combat_reward = {
    'uk': ('id', 'int'),                            # id
    'combat': ('combat', 'int'),                    # 战力
    'gift': ('gift', 'list_3'),                     # 奖励
}


# 监狱活动
prison_reward = {
    'uk': ('id', 'int'),                             # 编号
    'show_time': ('show_time', 'unicode'),           # 展示时间
    'start_time': ('start_time', 'str'),             # 开始时间
    'end_time': ('end_time', 'str'),                 # 结束时间
    'prisonId': ('prisonId', 'int'),                 # 监狱ID
    'gift': ('gift', 'list_3'),                      # 奖励
    'gift_rank': ('gift_rank', 'list_3'),            # 排行榜奖励
    'rank_num': ('rank_num', 'int'),                 # 排行榜数量
    'mail1': ('mail1', 'unicode'),                   # 邮件标题
    'story1': ('story1', 'unicode'),                 # 邮件内容
    'mail2': ('mail1', 'unicode'),                   # 邮件标题
    'story2': ('story1', 'unicode'),                 # 邮件内容
    'num': ('num', 'int'),                           # 人数限制
}


# 获取装备活动
get_equip = {
    'uk': ('id', 'int'),                             # 编号
    'show_time': ('show_time', 'unicode'),           # 展示时间
    'start_time': ('start_time', 'str'),             # 开始时间
    'end_time': ('end_time', 'str'),                 # 结束时间
    'evo': ('evo', 'int'),                           # 品质
    'num': ('num', 'int'),                           # 数量
    'gift': ('gift', 'list_3'),                      # 奖励
    'mail1': ('mail1', 'unicode'),                   # 邮件标题
    'story1': ('story1', 'unicode'),                 # 邮件内容
}


# 获取战队技能活动
get_skill = {
    'uk': ('id', 'int'),                             # 编号
    'show_time': ('show_time', 'unicode'),           # 展示时间
    'start_time': ('start_time', 'str'),             # 开始时间
    'end_time': ('end_time', 'str'),                 # 结束时间
    'skill_id': ('skill_id', 'int'),                 # 战队技能ID
    'gift': ('gift', 'list_3'),                      # 奖励
    'gift_rank': ('gift_rank', 'list_3'),            # 排行榜奖励
    'rank_num': ('rank_num', 'int'),                 # 排行榜数量
    'mail1': ('mail1', 'unicode'),                   # 邮件标题
    'story1': ('story1', 'unicode'),                 # 邮件内容
    'mail2': ('mail1', 'unicode'),                   # 邮件标题
    'story2': ('story1', 'unicode'),                 # 邮件内容
}


# 竞技活动
pvp_reward = {
    'uk': ('id', 'int'),                             # 编号
    'show_time': ('show_time', 'unicode'),           # 展示时间
    'start_time': ('start_time', 'str'),             # 开始时间
    'end_time': ('end_time', 'str'),                 # 结束时间
    'target1_name': ('target1_name', 'str'),         # 目标名字
    'target1_score': ('target1_score', 'int_list'),       # 目标
    'gift': ('gift', 'list_3'),                      # 奖励
    'mail1': ('mail1', 'unicode'),                   # 邮件标题
    'story1': ('story1', 'unicode'),                 # 邮件内容
    'num': ('num', 'int'),                           # 人数限制
}


# 首冲英雄升星活动
hero_star_recharge = {
    'uk': ('id', 'int'),                             # 编号
    'show_time': ('show_time', 'unicode'),           # 展示时间
    'start_time': ('start_time', 'str'),             # 开始时间
    'end_time': ('end_time', 'str'),                 # 结束时间
    'hero_id': ('hero_id', 'int'),                   # 英雄id
    'star': ('star', 'int'),                         # 星阶
    'gift': ('gift', 'list_3'),                      # 奖励
    'mail1': ('mail1', 'unicode'),                   # 邮件标题
    'story1': ('story1', 'unicode'),                 # 邮件内容
}

