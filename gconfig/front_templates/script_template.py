# -*- coding: utf-8 –*-

"""
Created on 2018-08-31

@author: sm
"""

script = {
    'uk': ('id', 'int'),  # 剧本id
    'name': ('name', 'int'),  # 名字
    'type': ('type', 'int'),  # 种类0=电影 1=电视 2=综艺
    'style': ('style', 'int'),  # 关卡的剧本类型
    'rate': ('rate', 'int'),  # 随机权重
    'cost': ('cost', 'int'),  # 剧本消耗(美元)
    'paycheck_ratio': ('paycheck_ratio', 'int'),  # 片酬系数(百分之）
    'hard_rate': ('hard_rate', 'int'),  # 难度系数
    'output': ('output', 'int'),  # 票房基数(万美元)
    'star': ('star', 'int'),  # 星级1-6
    'next_id': ('next_id', 'int'),  # 续作id
    'story': ('story', 'int'),  # 说明
    'icon': ('icon', 'str'),  # 图标
    'background': ('background', 'int'),  # 拍摄场景
    'music': ('music', 'int'),  # 拍摄音乐
    'tag_script': ('tag_script', 'int_list'),  # 剧本标签
    'style_effect1': ('style_effect1', 'int_list'),  # 最佳类型
    'style_effect2': ('style_effect2', 'int_list'),  # 次佳类型
    'style_effect3': ('style_effect3', 'int_list'),  # 不适类型
    'market': (('market1', 'market2', 'market3'), ('int', 'mult_force_num_list')),  # 市场需求1-男(百分之)
    # 市场需求1-男(百分之)
    'min_attr': (('min_attr1', 'min_attr2', 'min_attr3', 'min_attr4',
                  'min_attr5', 'min_attr6'), ('int', 'mult_force_num_list')),

    'award': ('award', 'int_list'),     # 影片属性达到最低要求的奖励
    # 基准演技
    'standard_attr': (('standard_attr1', 'standard_attr2', 'standard_attr3', 'standard_attr4',
                        'standard_attr5', 'standard_attr6'), ('int', 'mult_force_num_list')),
    'role_id': ('role_id', 'int_list'),     # 角色id

}


script_style_suit = {
    'uk': ('id', 'int'),  # 适合档次
    'rate': ('rate', 'int'),  # 票房影响（万分之）
    'desc': ('desc', 'int'),  # desc

}


script_style = {
    'uk': ('id', 'int'),  # 剧本类型id
    'name': ('name', 'int'),  #
    'market': ('market', 'int'),  # 市场偏好0男1女2童

}


script_type_style = {
    'uk': ('type', 'int'),  # 种类0=电影 1=电视 2=综艺
    'name': ('name', 'int'),  # 种类名称
    'style': ('style', 'int_list'),  # 剧本类型id
    'length': ('length', 'int_list'),  # 随机时间/集数
    'length_name': ('length_name', 'int'),  # 长度单位

}


script_role = {
    'uk': ('id', 'int'),  # 角色id
    'name': ('name', 'int'),  # name
    'class': ('class', 'int'),  # 角色类型1=主角 2=配角 3=反派
    'story': ('story', 'int'),  # 角色描述
    'dialog': ('dialog', 'int'),  # 角色台词
    'tag_role': ('tag_role', 'int_list'),  # 角色标签
    'sex_type': ('sex_type', 'int'),  # 要求性别-1表示没要求
    'profession_class': ('profession_class', 'int'),  # 要求类型-1=没要求 0=偶像 1=实力
    'profession_type': ('profession_type', 'int'),  # 要求分类 0=青春 1=成熟
    'role_attr': ('role_attr', 'int_list'),  # 属性类型1=演2歌3娱4艺5气6动

}

