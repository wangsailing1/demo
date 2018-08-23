# -*- coding: utf-8 –*-

"""
Created on 2018-08-27

@author: sm
"""

equip = {
    'uk': ('id', 'int'),  # 道具id
    'name': ('name', 'int'),  # 名字
    'quality': ('quality', 'int'),  # 品质
    'star': ('star', 'int'),  # 星级
    'icon': ('icon', 'str'),  # icon
    'story': ('story', 'int'),  # 说明
    # 'add_attr': (('add_attr1', 'add_attr2', 'add_attr3', 'add_attr4',
    #                'add_attr5', 'add_attr6', ('int', 'mult_force_num_list'))),  # 说明
}


# 卡牌碎片
equip_piece = {
    'uk': ('piece_id', 'int'),    #
    'name': ('name', 'int'),        # 名字
    'story': ('story', 'int'),      # 说明
    'icon': ('icon', 'str'),
    'quality': ('quality', 'int'),      # 品质
    'star': ('star', 'int'),            # 星级
    'use_num': ('use_num', 'int'),      # 碎片合成数量
    'equip_id': ('equip_id', 'int'),      # 对应装备
    'guide': ('guide', 'list_int_list'),  # 掉落指引
}
