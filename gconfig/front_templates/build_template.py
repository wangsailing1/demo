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
    'cost': ('cost', 'int_list'),  # 消耗
    'lv': ('lv', 'int'),  # 消耗
    'button': ('button', 'int_list'),  # 按钮
    'anim': ('anim', 'str'),  # 动画
    'open_anim': ('open_anim', 'str'),  # 解锁动画
    'field_id': ('field_id', 'int'),  # 地块id
    'lvlup_des': ('lvlup_des', 'str'),  # 升级描述
    'lvlup_condition': ('lvlup_condition', 'str'),  # 升级条件
}

field = {
    'uk': ('field_id', 'int'),  # 地块id
    'order': ('order', 'int'),  # 顺序
    'can_build': ('can_build', 'int_list'),    # 可建建筑
    'sort': ('sort', 'int'),    #
    'scaling': ('scaling', 'float'),    #
}
