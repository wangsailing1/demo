#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 英雄相关的配置
from gconfig import check


# 英雄基础数据表
hero_basis = {
    'uk': ('hero_id', 'int'),                   # 英雄id
    'sublevel_id': ('sublevel_id', 'int'),      # 子级id
    'father_id': ('father_id', 'int'),          # 父级id
    'name': ('name', 'unicode'),                # 英雄名字
    'phy_or_mag': ('phy_or_mag', 'int'),        # 物理or魔法
    'title': ('title', 'unicode'),              # 英雄称号
    'story': ('story', 'unicode'),              # 英雄描述
    'job': ('job', 'int'),                      # 职业定义
    'camp': ('camp', 'int'),                    # 阵营
    'personality': ('personality', 'int_list'), # 性格
    'crace': ('crace', 'int'),                  # 种族
    'gender': ('gender', 'int'),                # 性别
    'leader': ('leader', 'int'),                # 主角  0 不是主角  1 是主角
    'icon': ('icon', 'str'),                    # 头像
    'icon1': ('icon1', 'str'),                  # 临时头像
    'icon_fight': ('icon_fight', 'str'),        # 战斗用头像
    'art': ('art', 'str'),                      # 原画
    'icon_arena': ('icon_arena', 'str'),        # 竞技场头像
    'act': ('act', 'str'),                      # 动画
    'grade': ('grade', 'int'),                  # 档次,类型, 1: D 2: C 3: B 4: A 5: S 6: SS 7: SSS
    'grade_red': ('grade_red', 'int'),          # 是否红ssr
    'skin': ('skin', 'str'),                    # 皮肤
    'if_show': ('if_show', 'int'),              # 是否在完整表展示
    'show_skill': ('show_skill', 'int'),        # 获得英雄时显示的nb的技能
    'show_skill_des': ('show_skill_des', 'unicode'),    # nb的技能描述

    'init_star': ('init_star', 'int'),          # 初始星级
    'phy_atk': ('phy_atk', 'float'),            # 攻击
    'hp': ('hp', 'float'),                      # 生命
    'phy_def': ('phy_def', 'float'),            # 防御
    'speed': ('speed', 'float'),                # 速度
    'mag_atk': ('mag_atk', 'float'),            # 魔强
    'mag_def': ('mag_def', 'float'),            # 魔抗

    'crit_chance': ('crit_chance', 'int'),      # 暴击(%)
    'crit_atk': ('crit_atk', 'int'),            # 暴击伤害(%)
    'hit': ('hit', 'int'),                      # 效果命中(%)
    'resistance': ('resistance', 'int'),        # 效果抵抗(%)

    # 'star_rate': (('star1', 'star2', 'star3', 'star4', 'star5', 'star6', 'star7'),
    #               ('float', 'mult_dict_1')),  # 星级成长倍率

    'skill': (('skill1_id', 'skill2_id', 'skill3_id', 'skill4_id'), ('int', 'mult_dict_1')),  # 技能

    'extra_skill': (('extra_skill1_id', 'extra_skill2_id'), ('int', 'mult_dict_1')),    # 附加技

    # 'star_stone': (('star1_stone', 'star2_stone', 'star3_stone', 'star4_stone', 'star5_stone',
    #                 'star6_stone', 'star7_stone'), ('int', 'mult_dict_1')),  # 召唤所需灵魂石

    # 'star_cost': (('star2_cost', 'star3_cost', 'star4_cost', 'star5_cost',
    #                'star6_cost', 'star7_cost'), ('int', 'mult_dict_2')),  # 召回所需话费金钱

    'stone': ('stone', 'int'),                  # 对应灵魂石
    'awaken_material': ('awaken_material', 'list_3'),   # 觉醒消耗材料
    'awaken_skill': ('awaken_skill', 'int_list'),   # 觉醒技能
    'awaken_skill_story': ('awaken_skill_story', 'unicode'),   # 觉醒技能描述
    'prototype': ('prototype', 'unicode'),   # 致敬原型
    'painting': ('painting', 'str'),        # 立绘
    'chain_show': ('chain_show', 'int_list'),   # 宿命
    'sound': ('sound', 'str_list'),             # 声音
    'job_sort': ('job_sort', 'int'),            # 英雄定位
    'offset': ('offset', 'int_list'),           # 获得英雄立绘偏移值
    'equip_id': ('equip_id', 'int_list'),       # 穿戴装备id
    'icon_arena2': ('icon_arena2', 'str'),        # 竞技场头像
    'icon_arena3': ('icon_arena3', 'str'),        # 竞技场头像
    'icon_arena5': ('icon_arena5', 'str'),        # 竞技场头像
    'logic': ('logic', 'str'),                  # AI
    'position': ('position', 'int'),            # 推荐站位
    'combine': ('combine', 'int'),            # 合成碎片数
    'is_have': ('is_have', 'int'),            # 转成碎片数
    'protect_skill1_id': ('protect_skill1_id', 'int'),  # 援护技能id
    'pve_switch': ('pve_switch', 'int'),
    'painting_turninbs_player1': ('painting_turninbs_player1', 'int'),      # 黑街擂台中我方立绘是否需要翻转
    'painting_turninbs_player2': ('painting_turninbs_player2', 'int'),      # 黑街擂台中敌方立绘是否需要翻转
    'speciality': ('speciality', 'int'),
    'quality': ('quality', 'int'),  # 资质
    'character': ('character', 'int_list'), # 特性
    'character_value': ('character_value', 'int_or_float_list'),
    'painting_action': ('painting_action', 'str'),
}


# 英雄星级系数
hero_star_rate = {
    'uk': ('star', 'int'),
    'hero_star_rate': (('hero1_star_rate', 'hero2_star_rate', 'hero3_star_rate', 'hero4_star_rate',
                        'hero5_star_rate', 'hero6_star_rate'),
                       ('float', 'mult_dict_1')),    # 资质12-15英雄升星系数
    'hero_awaken_star': (('hero1_awaken_star_rate', 'hero2_awaken_star_rate', 'hero3_awaken_star_rate',
                          'hero4_awaken_star_rate', 'hero5_awaken_star_rate', 'hero6_awaken_star_rate'),
                         ('float', 'mult_dict_1')),  # 资质12-15英雄觉醒系数
}


# 英雄升星被动
hero_star_passive = {
    'uk': ('id', 'int'),                            # id
    'star': ('star', 'int'),                        # 星级
    'hero_passive': (('hero1_passive', 'hero2_passive', 'hero3_passive', 'hero4_passive', 'hero5_passive', 'hero6_passive'),
                     ('list_2', 'mult_dict_1')),      # 资质12-15被动
    'hero_passive_team': ('hero_passive_team', 'list_2'),  # 增加上阵英雄全员属性
}


# 升星数据
hero_star = {
    'uk': ('star', 'int'),                          # 星级
    'hero_stone': (('hero1_stone', 'hero2_stone', 'hero3_stone', 'hero4_stone', 'hero5_stone', 'hero6_stone'),
                   ('int', 'mult_dict_1')),        # 资质12-15需要的灵魂石
    'hero_cost': (('hero1_cost', 'hero2_cost', 'hero3_cost', 'hero4_cost', 'hero5_cost', 'hero6_cost'),
                   ('int', 'mult_dict_1')),        # 资质12-15升星花费
}


# 觉醒材料
awaken_material = {
    'uk': ('id', 'int'),            # 材料id
    'name': ('name', 'unicode'),    # 名称
    'icon': ('icon', 'str'),        # 图标
    'story': ('story', 'unicode'),  # 描述
    'quality': ('quality', 'int'),  # 品质框
    'sort': ('sort', 'int'),        # 类型
    'level': ('level', 'int'),      # 等级
    'cost': ('cost', 'list_3'),     # 合成消耗
}


# 英雄成长系数表
# hero_growth_rate = {
#     'uk': ('lvl', 'int'),       # 等级
#     'rate': ('rate', 'int'),    # 系数
#     'job': ((('warrior', 1),('assassin', 2), ('archer', 3), ('mage', 4), ('these', 5), ('special_hero', 100),
#              ('enemy', 200), ('boss', 300), ('npc', 400), ('player', 6)),  # 战士\刺客\弓手\法师\牧师\特殊英雄\小怪\boss\npc\主角
#             ('int', 'mult_key_dict')),
# }
hero_growth_rate = {
    'uk': ('lvl', 'int'),                               # 等级
    'hero_lvl_rate': (('hero1_lvl_rate', 'hero2_lvl_rate', 'hero3_lvl_rate', 'hero4_lvl_rate', 'hero5_lvl_rate', 'hero6_lvl_rate'),
                      ('int', 'mult_dict_1')),         # 资质12-15英雄
    'main_hero': ('main_hero', 'int'),                  # 主角基础
    'enemy': ('enemy', 'int'),                          # 小怪
}


# 英雄升级经验表
hero_exp = {
    'uk': ('lv', 'int'),    # 等级
    'hero_exp': (('hero1_exp', 'hero2_exp', 'hero3_exp', 'hero4_exp', 'hero5_exp', 'hero6_exp'),
                 ('int', 'mult_dict_1')),  # 英雄资质12-15所需经验
    'player_exp': ('player_exp', 'int'),  # 战队所需经验
    'give_power': ('give_power', 'int'),  # 升级赠送体力
    'give_whip': ('give_whip', 'int'),    # 升级获得皮鞭
    'gifts': ('gifts', 'list_3', check.check_reward()),     # 升级道具发背包
}


# 英雄等级上限
hero_lvl_limit = {
    'uk': ('player_lvl', 'int'),        # 战队等级
    'hero_lvl': ('hero_lvl', 'int'),    # 英雄等级
    'equip_lvl': ('equip_lvl', 'int'),  # 装备强化上限
}


# 英雄灵魂石
hero_stone = {
    'uk': ('id', 'int'),   # 灵魂石id
    'name': ('name', 'unicode'),  # 灵魂石名字
    'story': ('story', 'unicode'),  # 灵魂石描述
    'icon': ('icon', 'str_list'),  # 灵魂石icon
    'price': ('price', 'int'),  # 灵魂石出售价格
    'guide': ('guide', 'list_int_list'),  # 掉落指引
    'jump': ('jump', 'int'),            # 玩法跳转
    'unlock_id': ('unlock_id', 'int'),  # 解锁id
    'from': ('from', 'unicode'),        # 掉落描述
    'grade': ('grade', 'int'),          # 档次
    'quality': ('quality', 'int'),      # 品质边框
    'grade_red': ('grade_red', 'int'),  # 红品质
}


# 英雄属性品质
hero_quanlity = {
    'uk': ('id', 'int'),                    # 属性id
    'sort': ('sort', 'int'),                # 属性类型
    'quality': ('quality', 'list_3'),     # 属性品质库
}


# 英雄进阶徽章
# {
#     1: {  职业
#         1: {  档次
#             1: [],  品质: 需要的徽章
#         }
#     }
# }
grade_lvlup_badge = ({
    'uk': ('job', 'int'),  # 职业
    'grade': ('grade', 'int'),  # 档次
    'cost': ('cost', 'list_3'),     # 花费
    'lvl': ('lvl', 'int'),          # 等级限制
    'evolution': ('evolution', 'int'),  # 徽章品质
    'badge': (('badge1', 'num1', 'badge2', 'num2', 'badge3', 'num3',  # 需要的徽章
               'badge4', 'num4', 'badge5', 'num5', 'badge6', 'num6',
               'badge7', 'num7', 'badge8', 'num8', 'badge9', 'num9',
               'badge10', 'num10', 'badge11', 'num11', 'badge12', 'num12',
               'badge13', 'num13', 'badge14', 'num14', 'badge15', 'num15'), ('int', 'list_2_to_dict')),
}, 'grade_lvlup_badge')


# 英雄进阶奖励
# {
#     1: {  职业
#         1: {  档次
#             1: [],  品质: 效果
#         }
#     }
# }
grade_lvlup_reward = ({
    'uk': ('job', 'int'),  # 职业
    'grade': ('grade', 'int'),  # 档次
    'evolution': ('evolution', 'int'),  # 徽章品质
    'effect': ((('hp', 'hp'),  # 徽章效果
              ('phy_atk', 'phy_atk'),
              ('phy_def', 'phy_def'),
              ('mag_atk', 'mag_atk'),
              ('mag_def', 'mag_def')), ('float', 'mult_key_dict')),
}, 'grade_lvlup_reward')


grade_lvlup_reward_new = {
    'uk': ('evolution', 'int'),
    'evo_rate': ('evo_rate', 'float'),
}


hero_attribute = {
    'uk': ('hero_id', 'int'),
    'lvl_hp': ('lvl_hp', 'float'),
    'lvl_phy_atk': ('lvl_phy_atk', 'float'),
    'lvl_phy_def': ('lvl_phy_def', 'float'),
    'lvl_mag_atk': ('lvl_mag_atk', 'float'),
    'lvl_mag_def': ('lvl_mag_def', 'float'),
    'lvl_speed': ('lvl_speed', 'float'),
    'lvl_crit_chance': ('lvl_crit_chance', 'float'),
    'lvl_crit_atk': ('lvl_crit_atk', 'float'),
    'lvl_hit': ('lvl_hit', 'float'),
    'lvl_resistance': ('lvl_resistance', 'float'),
    'growth_hp': ('growth_hp', 'float'),
    'growth_phy_atk': ('growth_phy_atk', 'float'),
    'growth_phy_def': ('growth_phy_def', 'float'),
    'growth_mag_atk': ('growth_mag_atk', 'float'),
    'growth_mag_def': ('growth_mag_def', 'float'),
    'growth_speed': ('growth_speed', 'float'),
    'growth_crit_chance': ('growth_crit_chance', 'float'),
    'growth_crit_atk': ('growth_crit_atk', 'float'),
    'growth_hit': ('growth_hit', 'float'),
    'growth_resistance': ('growth_resistance', 'float'),
    'star_hp': ('star_hp', 'float'),
    'star_phy_atk': ('star_phy_atk', 'float'),
    'star_phy_def': ('star_phy_def', 'float'),
    'star_mag_atk': ('star_mag_atk', 'float'),
    'star_mag_def': ('star_mag_def', 'float'),
    'star_speed': ('star_speed', 'float'),
    'star_crit_chance': ('star_crit_chance', 'float'),
    'star_crit_atk': ('star_crit_atk', 'float'),
    'star_hit': ('star_hit', 'float'),
    'star_resistance': ('star_resistance', 'float'),
}


# 英雄进阶成长系数
hero_grade_rate = {
    'uk': ('grade', 'int'),  # 英雄品阶
    'trade_num_rate': ('trade_num_rate', 'float'),  # 公会贸易每十分钟英雄采集数量的成长系数
}


# 战斗技能升级
skill_detail_upgrade = {
    'uk': ('id', 'int'),        # 英雄id
    'grade_skill': (('grade1_skill', 'grade2_skill', 'grade3_skill', 'grade4_skill', 'grade5_skill',    # 品阶n拥有技能
                     'grade6_skill', 'grade7_skill', 'grade8_skill', 'grade9_skill', 'grade10_skill',
                     'grade11_skill', 'grade12_skill', 'grade13_skill', 'grade14_skill', 'grade15_skill',
                     'grade16_skill', 'grade17_skill', 'grade18_skill', 'grade19_skill', 'grade20_skill',
                     'grade21_skill', 'grade22_skill', 'grade23_skill', 'grade24_skill', 'grade25_skill',
                     'grade26_skill', 'grade27_skill', 'grade28_skill', 'grade29_skill', 'grade30_skill'),
                    ('int_list', 'mult_dict_1'))
}


# 英雄技能升级表
skill_lvlup_cost = {
    'uk': ('lvl', 'int'),  # 技能等级
    'normal_skill_cost': ('normal_skill_cost', 'int'),  # 小技能花费
}


# 技能成长系数
skill_growth_rate = {
    'uk': ('lvl', 'int'),  # 等级
    'rate': ('rate', 'int'),  # 系数
    'npc_lvl_rate': ('npc_lvl_rate', 'int'),    # 召唤npc等级系数
    'passive_rate': ('passive_rate', 'int'),  # 被动技
}


# 附加技能升级表
extra_skill_exp = {
    'uk': ('lvl', 'int'),   # 等级
    'dab_exp': ('dab_exp', 'int'),   # 能手技能经验
    'expert_exp': ('expert_exp', 'int'),   # 专精技能经验
    'fan_exp': ('fan_exp', 'int'),   # 爱好者技能经验
    'master_exp': ('master_exp', 'int'),   # 大师技能经验
}


# 附加技能成长
extra_skill_growth = {
    'uk': ('lvl', 'int'),   # 等级
    'dab_effect': ('dab_effect', 'int'),   # 增加能力值(能手)
    'expert_effect': ('expert_effect', 'int'),   # 增加珍惜装备权重100%(专精)
    'master_effect': ('master_effect', 'int'),   # 增加能力值(大师)
    'fan_effect': ('fan_effect', 'int'),   # 增加权重100%(爱好者)
}


# 英雄小技能基础数据
skill_normal_basis = {
    'uk': ('id', 'int'),  # 技能id
    'name': ('name', 'unicode'),  # 名字
    'story': ('story', 'unicode'),  # 描述
    'icon': ('icon', 'str'),  # 图标
    'act_hero': ('act_hero', 'str'),  # 人物动作
    'special_effects_hero1': ('special_effects_hero1', 'str'),  # 施法人特效
    'special_effects_skill': ('special_effects_skill', 'str'),  # 技能特效
    'skill_ready_time': ('skill_ready_time', 'float'),  # 法球出手延迟时间
    'special_effects_hero2': ('special_effects_hero2', 'str'),  # 被攻击特效
    'effect_rotation': ('effect_rotation', 'int'),  # 被攻击特效转向
    'effect_down': ('effect_down', 'int'),  # 被攻击特效层级
    'attacked_hero': ('attacked_hero', 'str'),  # 被攻击人动作
    'sign': ('sign', 'str'),  # 施法区域标记
    'npc_id': ('npc_id', 'int'),  # 召唤npc的id
    'npc_life': ('npc_life', 'float'),  # npc存在时间
    'act_ready': ('act_ready', 'str'),  # 施法前摇
    'act_ready_time': ('act_ready_time', 'float'),  # 施法前摇时间
    'ready_time': ('ready_time', 'float'),  # 前摇时间
    'blood_time': ('blood_time', 'int_or_float_list'),  # 掉血次数及频率
    'trigger': ('trigger', 'int'),  # 触发器类型
    'trigger_num': ('trigger_num', 'int'),  # 触发条件
    'use_num': ('use_num', 'int'),  # 最大使用次数
    'cd': ('cd', 'float'),  # CD
    'skill_type': ('skill_type', 'int'),  # 技能类型
    'target': ('target', 'int'),  # 目标
    'scope': ('scope', 'int'),  # 释放范围
    'radius': ('radius', 'int'),  # 半径
    'release_type': ('release_type', 'int'),  # 施法类型
    'release_time': ('release_time', 'int'),  # 持续施法时间
    'add_buff': ('add_buff', 'int'),  # 特效类型
    'buff_pro': ('buff_pro', 'int'),  # 特效概率
    'buff_time': ('buff_time', 'int'),  # 特效保留时间
    'skill_effect': ('skill_effect', 'float'),  # 技能效果
    'buff_effect': ('buff_effect', 'float'),  # buff效果
    'lvup_type': ('lvup_type', 'int'),  # 升级成长类型buff成长还是伤害数值成长
    'skill_effect_fix': ('skill_effect_fix', 'float'),  # 技能修正系数
    'effects_hero2_num': ('effects_hero2_num', 'int'),  # 被攻击特效播放个数
    'id_id': ('id_id', 'int'),  # 前端测试用
}


# 英雄被动技能
passive_skill = {
    'uk': ('id', 'int'),  # 技能id
    'name': ('name', 'unicode'),  # 名字
    'story': ('story', 'unicode'),  # 描述
    'icon': ('icon', 'str'),  # 图标
    'skill_type': ('skill_type', 'int'),  # 技能类型
    'target': ('target', 'int'),  # 目标类型
    'target_id': ('target_id', 'int'),  # 目标id
    'skill_effect': ('skill_effect', 'float'),  # 技能效果
}


# 附加技能
extra_skill = {
    'uk': ('skill_id', 'int'),  # 技能id
    'name': ('name', 'unicode'),  # 名字
    'icon': ('icon', 'str'),  # 图标
    'sort': ('sort', 'int'),  # 类型
    'type': ('type', 'int'),  # 值
    'story': ('story', 'unicode'),  # 描述
}


# 技能特效表
skill_buff = {
    'uk': ('id', 'int'),                                        # 特效id
    'add_buff_trigger': ('add_buff_trigger', 'int'),            # 技能附带特效触发类型
    'add_buff_trigger_num': ('add_buff_trigger_num', 'int'),    # 技能附带特效触发条件
    'add_buff_pro': ('add_buff_pro', 'int'),                    # 技能附带特效触发（100%）
    'hit': ('hit', 'int'),                                      # 是否享受效果命中
    'add_buff': ('add_buff', 'int'),                            # 技能附带BUFF
    'buff_max_type': ('buff_max_type', 'int'),                  # 特效叠加类型
    'buff_max_num': ('buff_max_num', 'int'),                    # 特效最大叠加层数
    'buff_time': ('buff_time', 'int'),                          # 特效持续回合数
    'buff_target': ('buff_target', 'int'),                      # 特效作用目标
    'buff_effect_value': ('buff_effect_value', 'int'),          # 特效数值取值
    'buff_effect': ('buff_effect', 'int'),                      # 特效数值
    'buff_off': ('buff_off', 'int'),                            # 特效强制结束
    'buff_end': ('buff_end', 'int_list'),                       # 驱散buff
    'buff_trigger': ('buff_trigger', 'int'),                    # 特效触发类型
    'add_buff_ext': ('add_buff_ext', 'int_list'),               # 特效扩展
    'name': ('name', 'unicode'),                                # 标题
    'sort': ('sort', 'int'),                                    # 类型
    'show': ('show', 'int'),                                    # buff icon展现位置
    'buff_effect_ext': ('buff_effect_ext', 'int'),              #
    'protect': ('protect', 'int'),                              # 免疫净化
    'type': ('type', 'int'),
    'description': ('description', 'unicode'),
    'buff_num': ('buff_num', 'int'),
}

# 技能效果播放
# skill_effect = {
#     'uk': ('id', 'int'),                                                # 技能id
#     'hero_location': ('hero_location', 'int'),                          # 技能释放人物位置
#     'act_hero1': ('act_hero1', 'str'),                                  # 攻击动作
#     'act_hero2': ('act_hero2', 'str'),                                  # 被攻击动作
#     'skill_ball': ('skill_ball', 'str'),                                # 法球
#     'ball_start_location': ('ball_start_location', 'int_list'),         # 法球出手位置
#     'ready_effect': ('ready_effect', 'str'),                            # 施法特效
#     'ready_effect_type': ('ready_effect_type', 'int'),                  # 施法特效播放逻辑
#     'ball_time': ('ball_time', 'float'),                                # 法球飞行时间
#     'effect_bao': ('effect_bao', 'int'),                                # 暴血点特效读取
#     'special_effect1': ('special_effect1', 'str'),                      # 特效名称1
#     'special_effect1_location': ('special_effect1_location', 'int'),    # 特效1播放位置
#     'special_effect1_down': ('special_effect1_down', 'int'),            # 特效1播放层级
#     'special_effect1_num': ('special_effect1_num', 'int'),              # 是否播放多个攻击特效1
#     'special_effect2': ('special_effect2', 'str'),                      # 特效名称2
#     'special_effect2_location': ('special_effect2_location', 'int'),    # 特效2播放位置
#     'special_effect2_num': ('special_effect2_num', 'int'),              # 是否播放多个攻击特效2
#     'special_effect2_down': ('special_effect2_down', 'int'),            # 特效2播放层级
# }

# npc基础数据表
npc = {
    'uk': ('npc_id', 'int'),                # id
    'name': ('name', 'unicode'),            # npc名称
    'act': ('act', 'str'),                  # 动画
    'can_choose': ('can_choose', 'int'),    # 能否被作为选中目标
    'phy_or_mag': ('phy_or_mag', 'int'),    # 物理还是魔法
    'skill': (('skill1_id', 'skill2_id', 'skill3_id'), ('int', 'mult_dict_1')),  # 技能
    'speed': ('speed', 'float'),            # 速度
    'hp': ('hp', 'float'),                  # 生命继承
    'phy_atk': ('phy_atk', 'float'),        # 攻击继承
    'phy_def': ('phy_def', 'float'),        # 防御继承
    'mag_atk': ('mag_atk', 'float'),        # 魔强继承
    'mag_def': ('mag_def', 'float'),        # 魔抗继承
    'round': ('round', 'int'),              # 生存回合
}


# 展示用npc
npc_show = {
    'uk': ('id', 'int'),                # id
    'painting': ('painting', 'str'),    # 动画配置
}


# 图鉴功能
pokedex = {
    'uk': ('id', 'int'),                    # 图鉴id
    'name': ('name', 'unicode'),            # 图鉴名称
    'hero_id': ('hero_id', 'int_list'),     # 图鉴包括英雄
    'extra': (('extra1', 'extra2', 'extra3', 'extra4', 'extra5'), ('list_2', 'mult_dict_1')),     # 全部激活属性(默认1星)
}


# 英雄图鉴属性
pokedex_hero = {
    'uk': ('hero_id', 'int'),               # 英雄id
    'pokedex_id': ('pokedex_id', 'int'),    # 所在图鉴id
    'attribute': ('attribute', 'list_2'),   # 增加属性
}


# 英雄里程碑
hero_milestone = {
    'uk': ('hero_id', 'int'),
    'task': (('task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7', 'task8', 'task9', 'task10'),
             ('int', 'mult_dict_1')),
    'task_reward': (('task1_reward', 'task2_reward', 'task3_reward', 'task4_reward', 'task5_reward',
                     'task6_reward', 'task7_reward', 'task8_reward', 'task9_reward', 'task10_reward',),
                    ('list_2', 'mult_dict_1'))
}


# 里程碑任务
milestone = {
    'uk': ('milestone_task_id', 'int'),     # 里程碑任务id
    'name': ('name', 'unicode'),            # 任务名
    'des': ('des', 'unicode'),              # 任务描述
    'icon': ('icon', 'str'),                # 任务图标
    'sort': ('sort', 'int'),                # 任务类型
    'type1': ('type1', 'int'),              # 类型1
    'type2': ('type2', 'int'),              # 类型2
    'target': (('target1', 'target2', 'target3', 'target4', 'target5',
                'target6', 'target7', 'target8', 'target9', 'target10'),
               ('int', 'mult_dict_1')),     # 目标
    'jump': ('jump', 'int'),                # 跳转
    'building_id': ('building_id', 'int'),  # 建筑功能id
}


# 英雄传记表
hero_story = {
    'uk': ('id', 'int'),    # 英雄id
    'story': (('story1', 'story2', 'story3', 'story4'), ('unicode', 'mult_dict_1')),    # 章节
    'story_name': (('story1_name', 'story2_name', 'story3_name', 'story4_name'), ('unicode', 'mult_dict_1')),   # 章节名称
    'story_reward': (('story1_reward', 'story2_reward', 'story3_reward', 'story4_reward'), ('list_3', 'mult_dict_1')),  # 章节解锁奖励
    'story_star': (('story1_star', 'story2_star', 'story3_star', 'story4_star'), ('int_list', 'mult_dict_1')),
}


# 助战英雄
assistant_hero = {
    'uk': ('id', 'int'),                # 助战id
    'hero_id': ('hero_id', 'int'),      # 英雄id
    'hp': ('hp', 'float'),              # 生命
    'phy_atk': ('phy_atk', 'float'),    # 攻击
    'phy_def': ('phy_def', 'float'),    # 防御
    'mag_atk': ('mag_atk', 'float'),    # 魔强
    'mag_def': ('mag_def', 'float'),    # 魔抗
    'speed': ('speed', 'float'),        # 速度
    'lv': ('lv', 'int'),                # 等级
}


# 缘分
chain = {
    'uk': ('chain_id', 'int'),                      # 宿命序号
    'name': ('name', 'unicode'),                    # 宿命名称
    'condition_sort': ('condition_sort', 'int'),    # 宿命达成类型（1：拥有卡牌，2：穿戴装备）
    'des': ('des', 'unicode'),                      # 宿命文字描述
    'data': (('data', 'data2', 'data3', 'data4'), ('int_list', 'mult_dict_1')),     # 宿命关联卡牌、装备id
    'effect': (('effect', 'effect2', 'effect3', 'effect4'), ('list_2', 'mult_dict_1')),     # 宿命属性加成
}


# 技能配置
skill_detail = {
    'uk': ('id', 'int'),                                # 技能ID
    'sort': ('sort', 'int'),                            # 子id
    'name': ('name', 'unicode'),                        # 技能名称
    'icon': ('icon', 'str'),                            # 技能图标
    'story_detail': ('story_detail', 'unicode'),        # 技能详细描述
    'script': ('script', 'str'),                        # 技能详细描述
    'skill_type': ('skill_type', 'int'),                # 技能类型
    'trigger': ('trigger', 'int'),                      # 技能触发类型
    'trigger_pro': ('trigger_pro', 'int'),              # 技能触发概率（如果有触发类型，必填）
    'trigger_data': ('trigger_data', 'int'),            # 技能触发概率（如果有触发类型，必填）
    'hit': ('hit', 'int'),                              # 是否享受效果命中
    'cost': ('cost', 'int'),                            # 消耗能量
    'cost_hp': ('cost_hp', 'int'),                      # 消耗生命（100%）
    'per_cd': ('per_cd', 'int'),                        # 冷却回合
    'cd': ('cd', 'int'),                                # 冷却回合
    'target': ('target', 'int'),                        # 目标类型
    'effect_sort': ('effect_sort', 'int'),              # 技能种类
    'add_buff': ('add_buff', 'int_list'),               # 技能附带BUFF
    'npc': ('npc', 'int'),                              # 召唤物id
    'effect_value': ('effect_value', 'int'),            # 技能取值
    'effect': ('effect', 'int'),                        # 技能数值（100%）
    'mag_effect_value': ('mag_effect_value', 'int'),    # 技能数值（100%）
    'mag_effect': ('mag_effect', 'int'),                # 技能数值（100%）
    'skill_ext': ('skill_ext', 'int_list'),
    'story': ('story', 'unicode'),                      # 技能描述
    'show_lvl': ('show_lvl', 'unicode'),                # 技能等级
    'if_use': ('if_use', 'int'),
    'voice': ('voice', 'str_list'),                     # 技能喊话
    'voice_percent': ('voice_percent', 'str_list'),     # 播放频率
    'key': ('key', 'str'),                              # 立绘偏移量
    'type': ('type', 'int'),                            # 技能性质
    'tips': ('tips', 'unicode'),                        # 玩家点击问号弹出的注释
}



# 小怪技能
skill_enemy = {
'uk': ('id', 'int'),                                # 技能ID
    'sort': ('sort', 'int'),                            # 子id
    'name': ('name', 'unicode'),                        # 技能名称
    'icon': ('icon', 'str'),                            # 技能图标
    'story_detail': ('story_detail', 'unicode'),        # 技能详细描述
    'script': ('script', 'str'),                        # 技能详细描述
    'skill_type': ('skill_type', 'int'),                # 技能类型
    'trigger': ('trigger', 'int'),                      # 技能触发类型
    'trigger_pro': ('trigger_pro', 'int'),              # 技能触发概率（如果有触发类型，必填）
    'trigger_data': ('trigger_data', 'int'),            # 技能触发概率（如果有触发类型，必填）
    'hit': ('hit', 'int'),                              # 是否享受效果命中
    'cost': ('cost', 'int'),                            # 消耗能量
    'cost_hp': ('cost_hp', 'int'),                      # 消耗生命（100%）
    'per_cd': ('per_cd', 'int'),                        # 冷却回合
    'cd': ('cd', 'int'),                                # 冷却回合
    'target': ('target', 'int'),                        # 目标类型
    'effect_sort': ('effect_sort', 'int'),              # 技能种类
    'add_buff': ('add_buff', 'int_list'),               # 技能附带BUFF
    'npc': ('npc', 'int'),                              # 召唤物id
    'effect_value': ('effect_value', 'int'),            # 技能取值
    'effect': ('effect', 'int'),                        # 技能数值（100%）
    'mag_effect_value': ('mag_effect_value', 'int'),    # 技能数值（100%）
    'mag_effect': ('mag_effect', 'int'),                # 技能数值（100%）
    'skill_ext': ('skill_ext', 'int_list'),
    'voice': ('voice', 'str_list'),                          # 技能喊话
    'key': ('key', 'str'),                              # 立绘偏移量
}


# 好感度
hero_favor = {
    'uk': ('hero_id', 'int'),                           # 英雄父id
    'talk': ('talk', 'unicode'),                        # 说话
    'main_attr': ('main_attr', 'list_2'),
    'sec_attr': ('sec_attr', 'list_2'),
    'attr_award_base': ('attr_award_base', 'list_2'),   # 基础属性加成
    'food_item': ('food_item', 'int_list'),
    'ex_attr': (('ex_attr1', 'ex_attr2', 'ex_attr3', 'ex_attr4', 'ex_attr5',
                 'ex_attr6', 'ex_attr7', 'ex_attr8', 'ex_attr9', 'ex_attr10'),
                 ('list_2', 'mult_dict_1')),                    # 每十级额外属性
    'teamattr_level': ('teamattr_level', 'int_list'),   # 全队加成对应等级
    'voice_unlock': ('voice_unlock', 'int_list'),       # 语音解锁等级

}
hero_favor_grade = {
    'uk': ('lv', 'int'),            # 等级
    'exp': ('exp', 'int'),          # 经验
    'rate': ('rate', 'int_list'),   # 属性几提升倍率
    # 'main_rate': ('main_rate', 'int'),    # 主要属性几提升倍率
    # 'sec_rate': ('sec_rate', 'int'),      # 阵营属性几提升倍率
    'title': ('title', 'str'),      # 好感度称号动画
    'item_levelup': ('item_levelup', 'list_3'), # 升级道具
    'is_break': ('is_break', 'int')         # 是否突破
}

personality = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),                    # 名称
    'description': ('description', 'unicode'),      # 描述
}


hero_character = {
    'uk': ('id', 'int'),
    'icon': ('icon', 'str'),
    'name': ('name', 'unicode'),
    'describe': ('describe', 'unicode'),
    'quality': ('quality', 'int'),
    'type': ('type', 'int'),
    'property': ('property', 'int'),
    'value': ('value', 'int'),
    'unit': ('unit', 'str'),
}
