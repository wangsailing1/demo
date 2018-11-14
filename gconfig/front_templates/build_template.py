#! --*-- coding: utf-8 --*--



#
card_building = {
    'uk': ('lv', 'int'),  # 等级
    'build_id': ('build_id', 'int'),  # 解锁等级
    'player_lv': ('player_lv', 'int'),  # 解锁等级
    'card_limit': ('card_limit', 'int'),  # 艺人上限
    'cost': ('cost', 'int_list'),  # 消耗
}

building = {
    'uk': ('build_id', 'int'),  # 建筑id
    'group': ('group', 'int'),  # 组别
    'next_id': ('next_id', 'int'),  # 下级建筑
    'icon': ('icon', 'str'),  # 图标
    'sort': ('sort', 'int'),  # 类型
    'name': ('name', 'str'),  # 名称
    'default': ('default', 'int'),  # 默认存在
    'unlock_lv': ('unlock_lv', 'int'),  # 解锁等级
}