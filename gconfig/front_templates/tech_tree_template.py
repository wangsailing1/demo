#! --*-- coding: utf-8 --*--

__author__ = 'shaoqiang'

# 科技树相关的配置

# 科技树点表
tech_tree = {
    'uk': ('id', 'int'),                                    # 编号
    'gate': ('gate', 'int'),                                # 开启迷雾
    'x_y_size': ('x_y_size', 'int_list'),                   # 横纵坐标及点的大小
    'link': ('link', 'int_list'),                           # 与哪些点有连接
    'search_word': ('search_word', 'int_list'),                           # 搜索
    'icon': ('icon', 'str'),                                # icon
    'name': ('name', 'unicode'),                            # 名字
    'description': ('description', 'unicode'),              # 描述
    'battle_attr': ('battle_attr', 'list_6'),             # 前/后排、哪个职业、第几个基础属性
    'tech_buff': ('tech_buff', 'int'),  # 科技树buff
    'point': ('point', 'int'),                           # 点数
}

tech_tree_pic = {
    'uk': ('id', 'int'),                                    # 编号
    'x_y_size': ('x_y_size', 'int_list'),                   # 横纵坐标及点的大小
    'icon': ('icon', 'str'),                           # 与哪些点有连接
    'name': ('name', 'unicode'),                            # 名字
}

tech_display = {
    'uk': ('id', 'int'),                                    # 编号
    'position': ('position', 'int'),                   # 横纵坐标及点的大小
    'career': ('career', 'int'),                           # 与哪些点有连接
    'attr': ('attr', 'int'),                                # icon
    'value': ('value', 'int'),                            # 名字
}
