# -*- coding: utf-8 –*-

"""
Created on 2018-08-31

@author: sm
"""

script = {
    'uk': ('id', 'int'),  # 剧本id
    'name': ('name', 'int'),  # 名字
    'first_script': ('first_script', 'int'),  # 是否首次剧本
    'type': ('type', 'int'),  # 种类1=电影 2=电视 3=综艺
    'style': ('style', 'int'),  # 关卡的剧本类型
    'rate': ('rate', 'int'),  # 随机权重
    'performance': ('performance', 'int'),  # 战斗表现
    'cost': ('cost', 'int'),  # 剧本消耗(美元)
    'paycheck_ratio': ('paycheck_ratio', 'int'),  # 片酬系数(百分之）
    'sequel_count': ('sequel_count', 'int'),  # 续作编号
    'hard_rate': ('hard_rate', 'int'),  # 难度系数
    'output': ('output', 'int'),  # 票房基数(万美元)
    'standard_popularity': ('standard_popularity', 'int'),  # 人气要求
    'star': ('star', 'int'),  # 星级1-6
    'next_id': ('next_id', 'int'),  # 续作id
    'group': ('group', 'int'),  # 组id
    'story': ('story', 'int'),  # 说明
    'icon': ('icon', 'str'),  # 图标
    'background': ('background', 'str'),  # 拍摄场景
    'music': ('music', 'str'),  # 拍摄音乐
    'tag_script': ('tag_script', 'int_list'),  # 剧本标签
    'style_effect': ('style_effect', 'int_list'),  # 最佳类型
    # 市场需求1-男(百分之)  2：女 3：儿童
    'market': (('market1', 'market2', 'market3'), ('int', 'mult_force_num_list')),
    'min_attr': (('min_attr1', 'min_attr2', 'min_attr3', 'min_attr4',
                  'min_attr5', 'min_attr6'), ('int', 'mult_force_num_list')),

    'award': ('award', 'int_list'),     # 影片属性达到3最低要求的奖励
    # 基准演技
    'standard_attr': (('standard_attr1', 'standard_attr2', 'standard_attr3', 'standard_attr4',
                        'standard_attr5', 'standard_attr6'), ('int', 'mult_force_num_list')),
    'ticket_line': ('ticket_line', 'int'),     # 结算票房标准
    # 同档演技
    'good_attr': (('good_attr1', 'good_attr2', 'good_attr3', 'good_attr4',
                       'good_attr5', 'good_attr6'), ('int', 'mult_force_num_list')),
    'random_reward1': ('random_reward1', 'int_list'),       # 随机奖励库1
    'random_num1': ('random_num1', 'int'),       # 随机奖励数量1
    'random_reward2': ('random_reward2', 'int_list'),       # 随机奖励库2
    'random_num2': ('random_num2', 'int'),       # 随机奖励数量2
    'player_exp': ('player_exp', 'int'),       # 公司经验
    'fight_exp': ('fight_exp', 'int'),       # 类型经验
    'stage_score': ('stage_score', 'int_list'),       # 推图分数

    'role_id': ('role_id', 'int_list'),     # 角色id
    'directing_policy': ('directing_policy', 'int_list'),     # 执导方针

}


script_style_suit = {
    'uk': ('id', 'int'),  # 适合档次
    'rate': ('rate', 'int'),  # 评分增量（十分之）
    'attention': ('attention', 'int'),  # 市场关注度影响
    'desc1': ('desc1', 'int'),  # desc
    'desc2': ('desc2', 'int'),  # desc
    'icon': ('icon', 'str'),  # icon
    'icon2': ('icon2', 'str_list'),  # icon

}


script_style = {
    'uk': ('id', 'int'),  # 剧本类型id
    'name': ('name', 'int'),  #
    'market': ('market', 'int'),  # 市场偏好2男1女3童
    'market_num': ('market_num', 'int'),  # 市场偏好2男1女3童
    'icon': ('icon', 'str'),

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
    'class': ('class', 'str'),  # 角色类型1=主角 2=配角 3=反派
    'story': ('story', 'int'),  # 角色描述
    'dialog': ('dialog', 'int'),  # 角色台词
    'tag_role': ('tag_role', 'int_list'),  # 角色标签
    'sex_type': ('sex_type', 'int'),  # 要求性别-1表示没要求
    'profession_class': ('profession_class', 'int'),  # 要求类型-1=没要求 0=偶像 1=实力
    'profession_type': ('profession_type', 'int'),  # 要求分类 0=青春 1=成熟
    'role_attr': ('role_attr', 'int_list'),  # 属性类型1=演2歌3娱4艺5气6动
    'role_help': ('role_help', 'int'),  # 推荐艺人

}

# 结束档次
script_end_level = {
    'uk': ('level', 'int'),  #
    'name': ('name', 'int'),  # name
    'icon': ('icon', 'str'),  # name
    'line': ('line', 'int'),  # 占结算线比重（万分之)
    'continued_level': ('continued_level', 'int'),  # 下映后关注度等级
    'if_next_script': ('if_next_script', 'int'),  # 是否激活续作
    'next_attention': ('next_attention', 'int'),
    'level_sequel_count': ('level_sequel_count', 'int'),    # 可获取该档次的续作编号
    'icon_background': ('icon_background', 'str_list'),    # 背景图

}

# 持续收益等级
script_continued_level = {
    'uk': ('level', 'int'),  #
    'upgrade_cost': ('upgrade_cost', 'int_list'),  # 升级需要宣传册数量
    'parm': ('parm', 'int'),  # 总收益倍数(2小时的总收益系数）
}


# 市场需求
script_market = {
    'uk': ('id', 'int'),  #
    'rate': ('rate', 'int'),  # 权重
    'market': (('market1', 'market2', 'market3'), ('int', 'mult_force_num_list')),  # 市场需求1-男(百分之)

}

# 曲线参数范围区间
script_curve = {
    'uk': ('id', 'int'),  #
    'name': ('name', 'int'),  # 曲线名
    'weeks': ('weeks', 'int'),  # 上映周数
    'curve_rate': ('curve_rate', 'int_list'),  # 曲线变化
    'icon': ('icon', 'str'),  # 曲线变化
}

# 许可证恢复
script_license = ({
    'uk': ('num', 'int'),  # 今日恢复数量
    'cd': ('cd', 'int_list'),  # 冷却时间（分钟）
    'cost': ('cost', 'int_list'),  # 许可证消耗
}, 'script_licence_config')


# 抽剧本
script_gacha = {
    'uk': ('id', 'int'),  #
    'script_id': ('script_id', 'int'),  #
    'gifts_id': ('gifts_id', 'int_list'),  #
    'weight': ('weight', 'int'),  #
    'weight_special': ('weight_special', 'int'),  #

}


# 抽剧本
diamond_script_gacha = {
    'uk': ('id', 'int'),  #
    'script_id': ('script_id', 'int'),  #
    'gifts_id': ('gifts_id', 'int_list'),  #
    'weight': ('weight', 'int'),  #
    'weight_special': ('weight_special', 'int'),  #

}

# 抽剧本cd
script_gacha_cd = ({
                    'uk': ('time', 'int'),  #
                    'cd': ('cd', 'int_list'),  #
                    }, 'gacha_cd_config')


# 抽剧本cost
script_gacha_cost = {
    'uk': ('type', 'int'),  #
    'cost': ('cost', 'int_list'),  #

}


# 关注度等级
attention_level = {
    'uk': ('level', 'int'),  #
    'name': ('name', 'str'),  #
    'min_attention': ('min_attention', 'int'),  #
    'max_attention': ('max_attention', 'int'),  #
    'name_trans': ('name_trans', 'str'),  #
    'icon': ('icon', 'str'),  #
    'color': ('color', 'int_list'),  #

}


# 难度等级
difficulty_level = {
    'uk': ('level', 'int'),  #
    'name': ('name', 'int'),  #
    'min_completely': ('min_completely', 'int'),  #
    'max_completely': ('max_completely', 'int'),  #

}


# 随机观众评价选择
audi_comment_choice = {
    'uk': ('id', 'int'),
    'audi_grade_range': ('audi_grade_range', 'int_list'),   # 观众评价区间
    'grade_weight': ('grade_weight', 'int_list'),           # 评分权重[观众评论星级，权重]
    'barrage_weight': ('barrage_weight', 'int_list'),       # 弹幕区间[弹幕星级，区间下限，区间上限]
}


# 媒体评价
media_comment = {
    'uk': ('id', 'int'),
    'name': ('name', 'int'),   # 媒体评论
    'pos_id': ('pos_id', 'int'),           # 出现位置
    'grade_range': ('grade_range', 'int_list'),       # 对应评分区间(0~10)
    'grade_wave_range': ('grade_wave_range', 'int_list'),       # 显示评分波动范围(已放大100倍）
    'type': ('type', 'int'),
}


# 观众评价
audi_comment = {
    'uk': ('id', 'int'),
    'name': ('name', 'int'),   # 观众评论
    'star': ('star', 'int'),           # 评论星级
    'grade_range': ('grade_range', 'int_list'),       # 对应评分区间(0~10)
    'type': ('type', 'int'),
}


# 弹幕
barrage = {
    'uk': ('id', 'int'),
    'name': ('name', 'int'),   # 观众评论
    'star': ('star', 'int'),           # 评论星级
    'type': ('type', 'int'),
}


# 市场随机事件
random_event = {
    'uk': ('id', 'int'),
    'des': ('des', 'str'),  # 描述
    'effect': ('effect', 'int_list'),  # 影响 [type, style, buff_percent]
    'weight': ('weight', 'int'),  # 权重
    'des1': ('des1', 'str'),  # 描述
    'des2': ('des2', 'str'),  # 描述
}


# 全球市场事件
global_market = random_event
