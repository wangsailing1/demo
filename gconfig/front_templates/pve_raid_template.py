#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check


pve_enemy = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),    # 小怪名称
    'job': ('job', 'int'),          # 职业
    'elite': ('elite', 'int'),      # 精英
    'gender': ('gender', 'int'),    # 性别
    'icon': ('icon', 'str'),        # 图标
    'icon_fight': ('icon_fight', 'str'),        # 图标
    'act': ('act', 'str'),          # 动画
    'logic': ('logic', 'str'),      # AI脚本
    'skin': ('skin', 'int'),        # 皮肤
    'immunity': ('immunity', 'int'),    # boss免控
    'skill': (('skill1_id', 'skill2_id', 'skill3_id', 'skill4_id'), ('int', 'mult_dict_1')),  # 技能
    'hp': ('hp', 'float'),              # 生命
    'phy_atk': ('phy_atk', 'float'),    # 攻击
    'phy_def': ('phy_def', 'float'),    # 防御
    'mag_atk': ('mag_atk', 'float'),    # 魔强
    'mag_def': ('mag_def', 'float'),    # 魔抗
    'speed': ('speed', 'float'),        # 速度
    'crit_chance': ('crit_chance', 'int'),  # 暴击(%)
    'crit_atk': ('crit_atk', 'int'),        # 暴击伤害(%)
    'hit': ('hit', 'int'),                  # 效果命中(%)
    'resistance': ('resistance', 'int'),    # 效果抵抗(%)
}


pve_stagelist = {
    'uk': ('id', 'int'),            # 关卡id
    'name': ('name', 'unicode'),    # 名字
    'icon': ('icon', 'str'),        # 图标
    'description': ('description', 'unicode'),  # 描述
    'reward': ('reward', 'list_3', check.check_reward()),   # 奖励
    'enemy': (('enemy1', 'enemy2', 'enemy3', 'enemy4', 'enemy5'), ('int', 'mult_force_num_list')),  # 敌人1-5
    'limit': ('limit', 'int'),          # 狂暴时间
    'reward_show': ('reward_show', 'list_3'),     # 奖励展示
    'battle_dialogue': ('battle_dialogue', 'list_3'),
}


pve_teamskill = {
    'uk': ('id', 'int'),    # 战队技能id
    'fee': ('fee', 'int'),  # 佣金，金币
}


pve_attribute = {
    'uk': ('id', 'int'),        # id
    'sort': ('sort', 'int'),    # 1:属性,2:基因
    'name': ('name', 'unicode'),
    'description': ('description', 'unicode'),  # 描述
    'attribute': ('attribute', 'list_2'),       # 属性值
    'gene': ('gene', 'int'),                    # 基因套装id
}


pve_hero = {
    'uk': ('grade', 'int'),     # 档次
    'fee': ('fee', 'int'),      # 佣金，金币
    'list': ('list', 'int_list'),   # 英雄id列表
    'amount': ('amount', 'int'),    # 周免数量
}


pve_stagesort1 = {
    'uk': ('id', 'int'),        # id
    'difficulty': ('difficulty', 'int'),    # 难度
    # 'topic': ('topic', 'int'),              # 主题id
    'name': ('name', 'unicode'),            # 名字
    'level': ('level', 'int'),              # 等级
    'pic': ('pic', 'str'),                  # 首页banner
    'pic2': ('pic2', 'str'),                # 副本背景图
    'stagelist': ('stagelist', 'int_list'), # 关卡
    'description': ('description', 'unicode'),  # 描述
    'NPC': ('NPC', 'str'),              # 描述者
    'reward': ('reward', 'list_3', check.check_reward()),     # 通关奖励
    # 'switch': ('switch', 'int'),        # 开关
    'dialogue': ('dialogue', 'int'),
}
pve_stagesort2 = pve_stagesort1


pve_recommend = {
    'uk': ('id', 'int'),    # 英雄id
    'attribute': ('attribute', 'int_list'),     # 属性推荐
    'gene': ('gene', 'int'),    # 基因推荐
}
