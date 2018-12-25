#! --*-- coding: utf-8 --*--



#
business = {
    'uk': ('id', 'int'),  # 事件id
    'icon': ('icon', 'str'),  # 事件icon
    'name': ('name', 'str'),  # 事件名
    'desc': ('desc', 'str'),  # 事件描述
    'select_txt': (('select_txt1', 'select_txt2', 'select_txt3'), ('str', 'mult_force_num_list')), # 选项文本
    'result_txt': (('result_txt1', 'result_txt2', 'result_txt3'), ('str', 'mult_force_num_list')), # 结果文本
    'pre_type': ('pre_type', 'int'),  # 出现条件类型
    'pre_num1': ('pre_num1', 'int'),  # 出现条件参数
    'pre_num2': ('pre_num2', 'str'),  # 出现条件参数
    'select_cost': (('select_cost1', 'select_cost2', 'select_cost3'), ('int_list', 'mult_force_num_list')), # 选项消耗
    'select_award': (('select_award1', 'select_award2', 'select_award3'), ('int_list', 'mult_force_num_list')), # 选项奖励
    'select0': ('select0', 'int'),  # 正确奖励编号
    'rate': ('rate', 'int'),  # 事件权重
}

business_times = {
    'uk': ('id', 'int'),  # id
    'cd': ('cd', 'int'),  # CD时间（分钟）
    'time': ('time', 'int_list'),  # id
}