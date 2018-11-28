#! --*-- coding: utf-8 --*--


# 粉丝活动
fans_activity = {
    'uk': ('id', 'int'),  # 活动id
    'name': ('name', 'int'),  # 活动名字
    'groupid': ('groupid', 'int'),
    'type': ('type', 'int'),
    'next_id': ('next_id', 'int'),  # 下一级id
    'unlock_cost': ('unlock_cost', 'int'),  # 解锁消耗美元
    'time': ('time', 'int'),  # 活动时长（分钟）
    'cost': ('cost', 'int'),  # 总消耗美元
    'icon': ('icon', 'str'),  # 背景图
    'card_max': ('card_max', 'int'),  # 人数上限
    'gold_per_time': ('gold_per_time', 'int'),  # 金币产出间隔（秒）
    'gold_per_card': ('gold_per_card', 'int'),  # 每人总产出金币（5秒产一次）
    'attention_per_time': ('attention_per_time', 'int'),  # 关注度产出间隔（秒）
    'attention_per_card': ('attention_per_card', 'int'),  # 每人总产出关注度（一分钟产一次）
    'ratio_per_time': ('ratio_per_time', 'int'),  # 物品产出间隔（秒）
    'ratio_per_card': ('ratio_per_card', 'int'),  # 每人每10分钟产出物品概率（万分之）
    'item': ('item', 'int_list'),  # item
    'build_id': ('build_id', 'int'),  # 建筑id
    'card_need': ('card_need', 'int_list'),  # 艺人要求[艺人位置编号，艺人性别，艺人类型，艺人分类，演技要求，歌艺要求，气质要求，动感要求，娱乐要求，人气要求]
}
