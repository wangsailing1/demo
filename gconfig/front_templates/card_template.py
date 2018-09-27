# -*- coding: utf-8 –*-

"""
Created on 2018-08-27

@author: sm
"""

card_basis = {
    'uk': ('id', 'int'),  # id
    'name': ('name', 'int'),  # 名字
    'paycheck_base': ('paycheck_base', 'int'),  # 片酬基数
    'sex_type': ('sex_type', 'int'),  # 性别
    'profession_class': ('profession_class', 'int'),  # 艺人类型0=偶像 1=实力
    'profession_type': ('profession_type', 'int'),  # 艺人分类 0=青春 1=成熟
    'head_portrait': ('head_portrait', 'str'),  # 艺人头像
    'half_portrait': ('half_portrait', 'str'),  # 艺人半身像
    'small_portrait': ('small_portrait', 'str'),  # 艺人半身像
    'hero_talk': ('hero_talk', 'int'),  # 艺人人口号
    'hero_title': ('hero_title', 'int'),  # 艺人称号
    'hero_design': ('hero_design', 'int'),  # 艺人描述
    'star_level': ('star_level', 'int'),  # 艺人星级1~6星

    'piece_id': ('piece_id', 'int'),  # 艺人碎片
    'star_cost': ('star_cost', 'int'),  # 艺人碎片-需要
    'star_giveback': ('star_giveback', 'int'),  # 艺人碎片-返还

    'qualityid': ('qualityid', 'int'),  # 艺人格调0~6
    'nextid': ('nextid', 'int'),  # 下一格调ID
    'lvmin': ('lvmin', 'int'),  # 觉醒等级限制
    'group': ('group', 'int'),  # 艺人组
    # 格调升档消耗
    'quality_cost': ('quality_cost', 'int_list'),
    # 初始演技、歌艺、娱乐、艺术、气质、动感
    'char_pro': (('charpro1', 'charpro2', 'charpro3', 'charpro4',
                     'charpro5', 'charpro6'), ('int', 'mult_force_num_list')),
    'lv_growid': ('lv_growid', 'int'),    # 升级属性成长ID

    'train_grow': ('train_grow', 'int_list'),    # 培养成长率 [成长，次数]

    'love_gift_type': ('love_gift_type', 'int_list'),  # 好感食物
    'love_growid': ('lovegrowid', 'int'),  # 羁绊属性成长ID

    # # 擅长剧本标签 擅长剧本标签品质
    'tag_script': ('tag_script', 'int_list'),

    # 擅长角色标签
    'tag_role': ('tag_role', 'int_list'),
    'phone_card': ('phone_card', 'int'),

}


card_level = {
    'uk': ('card_level', 'int'),    # 等级
    'exp': ('exp', 'int'),          # 升级所需经验
    'level_gold': ('level_gold', 'int'),          # 升级所需金币
}


card_script_exp = {
    'uk': ('card_script_level', 'int'),    # 等级
    'exp': ('exp', 'int'),          # 升级所需经验
    'lv_addition': ('lv_addition', 'int'),          # 类型结算属性加成
}


card_level_grow = {
    'uk': ('id', 'int'),    # 等级
    # 奇数级 升级 演技、歌艺、娱乐、艺术、气质、动感
    'pro_grow_odd': (('pro_grow_odd1', 'pro_grow_odd2', 'pro_grow_odd3', 'pro_grow_odd4',
                  'pro_grow_odd5', 'pro_grow_odd6'), ('int', 'mult_force_num_list')),
    # 偶数级 升级 演技、歌艺、娱乐、艺术、气质、动感
    'pro_grow_even': (('pro_grow_even1', 'pro_grow_even2', 'pro_grow_even3', 'pro_grow_even4',
                  'pro_grow_even5', 'pro_grow_even6'), ('int', 'mult_force_num_list')),

}


# 羁绊等级
card_love_level = {
    'uk': ('card_love_level', 'int'),    # 等级
    'exp': ('exp', 'int'),          # 升级所需经验
    'gift_max': ('gift_max', 'int'),          # 礼物赠送最大数量上限
    # 羁绊晋级需要碎片数量1星卡
    'star_cost': ('star_cost', 'list_2'),
    'train_count': ('train_count', 'int'),        # 培养次数上限

}


# 羁绊等级加成
card_love_grow = {
    'uk': ('id', 'int'),    # 卡片 星级
    # 羁绊升级所有属性加成比(万)[升到等级，加成比]
    'grow_love': ('grow_love', 'int_list'),
}


# 羁绊送礼等级
card_love_gift = {
    'uk': ('gift_lv', 'int'),    # 送礼升级属性的次数
    'gift_exp': ('gift_exp', 'int'),       # 升属性需要的礼物点数
}


# 羁绊礼物id属性隐射
card_love_gift_taste = {
    'uk': ('id', 'int'),    # id
    'name': ('name', 'unicode'),       # 味道名称
    'attr': ('attr', 'int'),       # 对应属性
    'item_id': ('item_id', 'int_list'),       # 对应食物
}


# 卡牌培养消耗
card_train_cost = {
    'uk': ('train_time', 'int'),    # 培养次数
    'cost': ('cost', 'list_3'),       # 消耗
    'diamond_cost': ('diamond_cost', 'int'),       # 钻石消耗
}


# 卡牌培养加成
card_train_grow = {
    'uk': ('id', 'int'),    # 成长id
    # 培养成长随机区间 演技、歌艺、娱乐、艺术、气质、动感
    'pro_grow_train': (('pro_grow_train1', 'pro_grow_train2', 'pro_grow_train3', 'pro_grow_train4',
                  'pro_grow_train5', 'pro_grow_train6'), ('int_list', 'mult_force_num_list')),
}


# 卡牌培养名字
card_train_type = {
    'uk': ('id', 'int'),    #
    'name': ('name', 'int'),
    'icon': ('icon', 'str'),
}


# 卡牌碎片
card_piece = {
    'uk': ('id', 'int'),    #
    'name': ('name', 'int'),        # 名字
    'story': ('story', 'int'),      # 说明
    'icon': ('icon', 'str'),
    'quality': ('quality', 'int'),      # 品质
    'star': ('star', 'int'),            # 星级
    'use_num': ('use_num', 'int'),      # 碎片合成数量
    'card_id': ('card_id', 'int'),      # 对应艺人
    'guide': ('guide', 'list_int_list'),  # 掉落指引
}


# 卡牌品质
card_quality = {
    'uk': ('level', 'int'),    #
    'name': ('name', 'int'),        # 名字
    'color': ('color', 'str'),
}


# 卡牌取消雪藏消耗
card_repick = {
    'uk': ('star', 'int'),    #
    'cost': ('cost', 'int'),        # 消耗的点赞数
}
