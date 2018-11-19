#! --*-- coding: utf-8 --*--


guide = {
    'uk': ('id', 'int'),  # id
    'sort': ('sort', 'int'),  # 组
    'aim': ('aim', 'int'),  # 结束步
    'level': ('level', 'int'),  # 跳过
    'key': ('key', 'str'),  # 页面名
    'action': ('action', 'int'),  # 执行
    'trigger': ('trigger', 'int'),  # 触发
    'delay': ('delay', 'int'),  # 延迟
    'target': ('target', 'int'),  # 显示
    'next': ('next', 'int'),  # 下一步
    'drama': ('drama', 'int'),  # 触发对话
    'des': ('des', 'unicode'),  # 说明文档
}


guide_team = {
    'uk': ('id', 'int'),  # 引导组id
    'start_id': ('start_id', 'int'),  # 起始id
    'open_level': ('open_level', 'int'),  # 激活等级
    'sort': ('sort', 'int'),  # 引导分组
    'type': ('type', 'int'),  # 引导类型
    'is_open': ('is_open', 'int'),  # 是否开启
    'is_done': ('is_done', 'int'),  # 完成条件
}


dialogue_guide_team = {
    'uk': ('id', 'int'),  # id
    'dialogueId': ('dialogueId', 'int_list'),  # 对话id
}