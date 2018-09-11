# -*- coding: utf-8 –*-


card_book = {
    'uk':               ('id',          'int'),         # id
    'name':             ('name',        'int'),         # 组合名称
    'intro':            ('intro',       'int'),         # 组合描述
    'card':             ('card',        'int_list'),    # 角色
    'award':            ('award',       'int_list'),    # 奖励

}

script_book = {
    'uk':               ('id',          'int'),          # id
    'name':             ('name',        'int'),         # 组合名称
    'intro':            ('intro',       'int'),         # 组合描述
    'script':           ('script',      'int_list'),    # 剧本
    'award':            ('award',       'int_list'),    # 奖励
}

script_group_object = {
    'uk':               ('id',              'int'),         # id
    'group_target':     ('group_target',    'int_list'),         # 组目标
    'award':            ('award',           'int_list'),    # 奖励
}