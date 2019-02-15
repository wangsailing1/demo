#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

director = {
    'uk':   ('id', 'int'),                      # 编号
    'name': ('name', 'unicode'),                # 名字
    'star': ('star', 'int'),                    # 星级
    'att':  ('att', 'int'),                     # 初始知道能力
    'tag':  ('tag', 'int_list'),                # 擅长标签
    'icon':  ('icon', 'str'),                   # icon
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