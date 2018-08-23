#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check

# 英雄表
endless_march_hero = {
    'uk': ('id', 'int'),            # 英雄id
    'hero_id': ('hero_id', 'int'),  # 角色id
    'price': ('price', 'str'),      # 解锁价格
    'levelup_price': ('levelup_price', 'int'),  # 升级价格
    'levelup_rate': ('levelup_rate', 'float'),  # 每次升级提升比例
    'hero_attr': ('hero_attr', 'int'),          # 主角基础属性
    'hero_attr_rate': ('hero_attr_rate', 'float'),  # 主角基础属性增幅
    'critical_damrate': ('critical_damrate', 'int'),    # 暴击伤害
    'att_speedrate': ('att_speedrate', 'int'),  # 攻击速度
    'critical_rate': ('critical_rate', 'int'),  # 基础暴击率
    'act': ('act', 'str'),  # 动画
}

# 英雄技能表
endless_march_hero_skill = {
    'uk': ('id', 'int'),
    'skill_level': ('skill_level', 'int'),      # 技能解锁等级
    'evo_rate': ('evo_rate', 'int'),            # 解锁消耗倍率
    'att_type': ('att_type', 'int'),            # 技能效果类型
    'att_num': ('att_num', 'int'),              # 技能效果值
    'skill_name': ('skill_name', 'unicode'),    # 技能名称
    'skill_icon': ('skill_icon', 'str'),        # 技能图标
    'skill_des': ('skill_des', 'unicode'),      # 技能描述
}


# 主角表
endless_march_main = {
    'uk': ('main_hero_id', 'int'),              # 主角
    'basic_attr': ('basic_attr', 'int'),        # 主角基础属性
    'critical_damrate': ('critical_damrate', 'int'),    # 暴击伤害
    'att_speedrate': ('att_speedrate', 'int'),  # 攻击速度
    'critical_rate': ('critical_rate', 'int'),  # 基础暴击率
    'skill1_id': ('skill1_id', 'int_list'),     # 主角专属技能
    'levelup_price': ('levelup_price', 'int'),  # 升级价格
    'levelup_rate': ('levelup_rate', 'float'),  # 每次升级提升比例
    'skillup_rate': ('skillup_rate', 'float'),
}


# 主角技能表
endless_march_main_skill = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),
    'icon': ('icon', 'str'),
    'unlock_level': ('unlock_level', 'int'),
    'evo_rate': ('evo_rate', 'int'),            # 解锁消耗倍率
    'story': ('story', 'unicode'),
    'story_detail': ('story_detail', 'unicode'),
    'effect': ('effect', 'int'),
    'skill_last': ('skill_last', 'int'),
    'cd': ('cd', 'int'),
    'cdclear_price': ('cdclear_price', 'int'),  # 清除技能cd花费钻石
}

endless_march_enemy = {
    'uk': ('id', 'int'),
    'activity_enemy_id': ('activity_enemy_id', 'int'),  # 怪物id
    'is_boss': ('is_boss', 'int'),
    'hp_id': ('hp_id', 'float'),
    'reward1': ('reward1', 'list_3'),
    'reward_rate1': ('reward_rate1', 'float'),
    'reward2': ('reward2', 'list_4'),
    'reward_rate2': ('reward_rate2', 'float'),
    'size_rate': ('size_rate', 'int'),
    'big_enemy': ('big_enemy', 'int'),
}


endlesscoin_exchange = {
    'uk': ('id', 'int'),
    'level': ('level', 'int'),
    'cost': ('cost', 'int_list'),
    'coin': ('coin', 'int'),
    'weight1': ('weight1', 'list_2'),
    'weight2': ('weight2', 'list_2'),
    'times': ('times', 'int'),
}


endless_breakreward = {
    'uk': ('id', 'int'),
    'times': ('times', 'int'),
    'reward': ('reward', 'list_3', check.check_reward()),
}


endless_lucky = {
    'uk': ('id', 'int'),
    'type': ('type', 'int'),
    'type_des': ('type_des', 'unicode'),
    'effect': ('effect', 'int_float_list_or_int_float'),
    'effect_content': ('effect_content', 'list_3'),
    'apper_time': ('apper_time', 'int_list'),
}


endless_artifact = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),
    'pic': ('pic', 'str'),
    'des': ('des', 'unicode'),
    'att_num': ('att_num', 'int'),
    'att_type': ('att_type', 'int'),
    'price': ('price', 'int'),
    'art_size': ('art_size', 'float'),
    'art_quality': ('art_quality', 'int'),
}


endless_bg = {
    'uk': ('id', 'int'),
    'pic_id': ('pic_id', 'str'),
}
