#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check


# 传记副本详情
biography_detail = {
    'uk': ('id', 'int'),                        # 序号
    'name': ('name', 'unicode'),                # 传记名称
    'icon': ('icon', 'str_list'),               # 传记相关任务
    'banner': ('banner', 'str'),                # 传记大图
    # 'lock': ('lock', 'int'),                    # 解锁条件（等级）
    'des': ('des', 'unicode'),                  # 故事梗概
    'chapter_id': ('chapter_id', 'int_list'),   # 传记中的关卡
    'swap_reward': ('swap_reward', 'list_3'),   # 扫荡奖励
}


# 匹配敌人
biography_chapter = {
    'uk': ('id', 'int'),                        # 传记关卡id
    'name': ('name', 'unicode'),                # 关卡名称
    'icon': ('icon', 'str'),                    # 关卡图标
    'chapter_reward': ('chapter_reward', 'list_3'),    # 关卡完成奖励
    'start_drama': ('start_drama', 'int'),             # 战前剧情对话
    'end_drama': ('end_drama', 'int'),                 # 战后对话
    'enemy_id': ('enemy_id', 'int'),              # 难度1-6敌人阵容
    'hero_id': (('hero1_id', 'hero2_id', 'hero3_id', 'hero4_id', 'hero5_id'), ('int', 'mult_force_num_list')),    # 1-5号位助战英雄
    'hero_lv': (('hero1_lv', 'hero2_lv', 'hero3_lv', 'hero4_lv', 'hero5_lv'), ('int', 'mult_force_num_list')),    # 1-5号位助战英雄等级
    'hero_star': ('hero_star', 'int'),             # 1-5号位助战英雄星级
    'hero_grade': ('hero_grade', 'int'),           # 1-5号位助战英雄品阶
}
