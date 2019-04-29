#! --*-- coding: utf-8 --*--


guide = {
    'uk': ('id', 'int'),  # id
    'sort': ('sort', 'int'),  # 组
    'aim': ('aim', 'int'),  # 结束步
    'level': ('level', 'int'),  # 跳过
    'key': ('key', 'str'),  # 页面名
    'action': ('action', 'int'),  # 执行
    'trigger': ('trigger', 'int_list'),  # 触发
    'delay': ('delay', 'float'),  # 延迟
    'target': ('target', 'int_list'),  # 显示
    'next': ('next', 'int'),  # 下一步
    'drama': ('drama', 'int_list'),  # 触发对话
    'des': ('des', 'unicode'),  # 说明文档
    'jump': ('jump', 'int'),  # 跳转
}

guide_team = {
    'uk': ('id', 'int'),  # 引导组id
    'start_id': ('start_id', 'int'),  # 起始id
    'open_level': ('open_level', 'int'),  # 激活等级
    'sort': ('sort', 'int'),  # 引导分组
    'type': ('type', 'int'),  # 引导类型
    'is_open': ('is_open', 'int'),  # 是否开启
    'is_done': ('is_done', 'int_list'),  # 完成条件
}

dialogue_guide_team = {
    'uk': ('id', 'int'),  # id
    'dialogueId': ('dialogueId', 'int_list'),  # 对话id
}

dialogue_guide = {
    'uk': ('dialogueid', 'int'),  # id
    'roleid': ('roleid', 'int'),  # 角色id
    'dialogkind': ('dialogkind', 'int'),  # 对话框种类
    'type': ('type', 'int'),  # 类型
    'words': ('words', 'str'),  # 对话
    'voice': ('voice', 'str'),  # 配音
}
