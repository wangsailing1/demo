#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

director = {
    'uk':   ('id', 'int'),                      # 编号
    'name': ('name', 'unicode'),                # 名字
    'star': ('star', 'int'),                    # 星级
    'att':  ('att', 'int'),                     # 初始指导能力
    'tag':  ('tag', 'int_list'),                # 擅长标签
    'icon':  ('icon', 'str'),                   # 初始消耗美元
    'cost':  ('cost', 'str'),                   # icon
    'pro':  (('pro1', 'pro2','pro3','pro4','pro5','pro6',), ('int', 'mult_force_num_list')),    # 属性加成
}

director_gacha = {
    'uk':       ('id', 'int'),                          # 编号
    'director': ('director', 'int_list'),               # 导演id
    'weight':   ('weight', 'int'),                      # 权重
    'cost':     ('cost', 'int_list'),                   # 招聘书消耗
    'gacha_id': ('gacha_id', 'int'),                    # 招聘库id
}

director_gacha_cost = {
    'uk':       ('id', 'int'),                          # 编号
    'cost':     ('cost', 'int_list'),                   # 招聘消耗
    'cd':       ('cd', 'int_list'),                     # 冷却时间
}

director_lv = {
    'uk':               ('lv', 'int'),                              # 导演等级
    'att_param':        ('att_param', 'int'),                       # 执导能力加成万分比
    'cost_param':       ('cost_param', 'int'),                      # 消耗美元加成万分比
    'level_cost':       ('level_cost', 'int_list'),                 # 升级花费
    'pro_param':        ('pro_param', 'int'),                       # 属性加成万分比
}


director_skill = {
    'uk':               ('id', 'int'),                          # 导演等级
    'skill_type':       ('skill_type', 'int'),                  # 技能类型
    'value':            ('value', 'int'),                       # 技能效果
    'dskill_param':     ('dskill_param', 'int'),                # 导演技能系数
    'des':              ('des', 'str'),                         # 属性加成万分比
}


directing_policy  = {
    'uk':                       ('id', 'int'),                          # 导演等级
    'director_skillid':         ('director_skillid', 'int_list'),       # 技能类型
    'name':                     ('name', 'str'),                        # 技能名
    'des':                      ('des', 'str'),                         # 属性加成万分比
}