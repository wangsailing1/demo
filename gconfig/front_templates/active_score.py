#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

# 积分活动

# 积分活动版本
active_score = {
    'uk': ('id', 'int'),                                            # 活动id
    'title_png': ('title_png', 'str'),                              # 活动标题图
    'title': ('title', 'str'),                                      # 活动副标题
    'score_icon': ('score_icon', 'str'),                            # 积分图标
    'score_txt': ('score_txt', 'str'),                              # 积分文本
    'explain_id': ('explain_id', 'int'),                            # 活动explain_id
    'des': ('des', 'str'),                                          # 活动说明
    'mission': ('mission', 'int_list'),                             # 任务组
    'award_daily': (('award_daily1', 'award_daily2', 'award_daily3'),
                   ('int_list', 'mult_force_num_list')),            # 每日奖励

    'need_daily': (('need_daily1', 'need_daily2', 'need_daily3'),
                   ('int', 'mult_force_num_list')),                 # 每日要求

    'award_total': (('award_total1', 'award_total2', 'award_total3', 'award_total4',
                 'award_total5', 'award_total6', 'award_total7', 'award_total8'),
                   ('int_list', 'mult_force_num_list')),            # 累计奖励
    'need_total': (('need_total1', 'need_total2', 'need_total3', 'need_total4',
                 'need_total5', 'need_total6', 'need_total7', 'need_total8'),
                   ('int', 'mult_force_num_list')),                 # 累计要求

    'mail_title': ('mail_title', 'str'),                            # 邮件标题
    'mail': ('mail', 'str'),                                         # 邮件内容
}

# 积分活动任务
active_score_mission = {
    'uk': ('id', 'int'),                                            # 活动id
    'des': ('des', 'str'),                                          # 活动标题图
    'sort': ('sort', 'int'),                                        # 类型
    'target': (('target1', 'target2', 'target3', 'target4', 'target5'), ('int_list_or_int2', 'mult_force_num_list')),  # 目标
    'reward': ('reward', 'int_list'),                               # 奖励
}


# 积分活动排行奖励
active_score_rank = {
    'uk': ('id', 'int'),                                            # 编号
    'rank': ('rank', 'int_list'),                                   # 排名区间
    'award': ('award', 'int_list'),                                 # 奖励道具
    'active_id': ('active_id', 'int_list'),                         # 活动id组
}