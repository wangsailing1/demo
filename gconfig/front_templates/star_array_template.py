#! --*-- coding: utf-8 --*--


# 星座图
star_array = {
    'uk': ('id', 'int'),                # id
    'star': ('star', 'int'),            # 所属那个星座的那个图
    'xy': ('xy', 'int_list'),           # 坐标
    'attr': ('attr', 'int'),            # 加成属性
    'value': ('value', 'int'),          # 属性数值
    'price': ('price', 'int'),          # 需要点数
    'reward': ('reward', 'list_3'),     # 属性描述
}

# 星座图奖励
star_array_reward = {
    'uk': ('id', 'int'),                # id
    'num': ('num', 'int'),              # 所需点数
    'reward': ('reward', 'list_3'),     # 奖励
}


# 星座图背景
star_pic = {
    'uk': ('id', 'int'),                # id
    'button': ('button', 'str'),        # 按钮图
    'pic': ('pic', 'str'),              # 背景图
    'line1': ('line1', 'str'),          # 未点亮时连线
    'line2': ('line2', 'str'),          # 点亮时连线
    'point': ('point', 'int_list'),     # 图里的点
    'button1': ('button1', 'str'),        # 按钮图
    'name': ('name', 'unicode'),        # 名称
}
