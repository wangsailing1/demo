#! --*-- coding: utf-8 --*--
__author__ = 'yanyunfei'

# 自己关卡模块
from gconfig import check

# avg剧情配置
avg_dialogue = {
    'uk': ('id', 'int'),
    'chapter': ('chapter', 'int'),
    'player_sex': ('player_sex', 'int'),
    # 'position': ('position', 'int'),
    'is_option': ('is_option', 'int'),
    'option_team': ('option_team', 'int_list'),
    'next': ('next', 'int'),
    'is_end': ('is_end', 'int'),
    'hero_id': ('hero_id', 'int'),
    'phone_unlock': ('phone_unlock', 'int'),
    'type': ('type', 'int'),
    # 'name': ('name', 'unicode'),
    'is_turn': ('is_turn', 'int'),
    'hero_figue': ('hero_figue', 'str'),
    'background': ('background', 'str'),
    'hero_expression': ('hero_expression', 'str'),
    'word': ('word', 'unicode'),
    'reward': ('reward', 'int_list'),
    'add_value': ('add_value', 'int_list'),
    'voice': ('voice', 'str'),
}

# 战斗内广告栏
ad = {
    'uk': ('id', 'int'),
    'jump_id': ('jump_id', 'str'),
    'sub_id': ('sub_id', 'int'),
    'ad_text': ('ad_text', 'int_list'),
}

ad_text = {
    'uk': ('id', 'int'),
    'ad_title': ('ad_title', 'unicode'),
    'ad_text': ('ad_text', 'unicode'),
}

# 战后对话文字内容
E_dialogue_words = {
    'uk': ('dialogueId', 'int'),  # 对话id
    'roleId': ('roleId', 'int'),  # 角色id
    'type': ('type', 'int'),  # 左右
    'words': ('words', 'unicode'),  # 内容
}

# 战前对话文字内容
P_dialogue_words = {
    'uk': ('dialogueId', 'int'),  # 对话id
    'roleId': ('roleId', 'int'),  # 角色id
    'type': ('type', 'int'),  # 左右
    'words': ('words', 'unicode'),  # 内容
}

# 对话关卡
dialogue_chapter = {
    'uk': ('id', 'int'),  # 关卡id
    'per_dialog': ('per_dialog', 'int'),  # 战斗前对话
    'P_dialogue': ('P_dialogue', 'int_list'),  # 对话内容
    'end_dialog': ('end_dialog', 'int'),  # 战斗后对话
    'E_dialogue': ('E_dialogue', 'int_list'),  # 对话内容
    'playbackId': ('playbackId', 'int_list'),  # 剧情回放id
}

# 对话角色头像
dialogue_role = {
    'uk': ('roleId', 'int'),  # 角色id
    'heroId': ('heroId', 'int'),  # 英雄id
    'name': ('name', 'unicode'),  # 人物名
    'image': ('image', 'str'),  # 头像
    'painting': ('painting', 'str'),  # 立绘
    'animation': ('animation', 'str'),  # 动画
}

# 动画文字内容
animation_words = {
    'uk': ('dialogueId', 'int'),  # 对话id
    'roleId': ('roleId', 'int'),  # 角色id
    'type': ('type', 'int'),  # 左右
    'words': ('words', 'unicode'),  # 内容
}

# 怪物气泡说话
monster_talk = {
    'uk': ('id', 'int'),  # 文字id
    'talk': ('talk', 'unicode'),  # 文字内容
}

# 动画关卡
animation_chapter = {
    'uk': ('operaId', 'str'),  # 剧情id
    'mapId': ('mapId', 'str'),  # 地图
}

# 英雄说话
hero_talk = {
    'uk': ('id', 'int'),  # 英雄id
    'talk': (('talk1', 'talk2', 'talk3', 'talk4', 'talk5', 'talk6', 'talk7', 'talk8', 'talk9', 'talk10',
              'talk11', 'talk12', 'talk13', 'talk14', 'talk15', 'talk16', 'talk17', 'talk18', 'talk19', 'talk20'),
             ('unicode', 'mult_dict_1'))  # 说话
}

# 剧情奖励
opera_awards = {
    'uk': ('awardId', 'str'),  # 奖励id
    'award': ('award', 'list_3'),  # 奖励内容
}

# 剧情提示
opera_click = {
    'uk': ('clickId', 'str'),  # 引导id
    'words': ('words', 'unicode'),  # 内容
}

# 剧情角色初始化
opera = {
    'uk': ('id', 'int'),  # 引导id
    'roleId': ('roleId', 'int'),  # 角色id
    'toward': ('toward', 'int'),  # 朝向
    'layer': ('layer', 'int'),  # 层
    'operaId': ('operaId', 'str'),  # 剧情id
}

# 章节剧情
chapter_words = {
    'uk': ('chapter', 'int'),  # 章节
    'chapter_num': ('chapter_num', 'unicode'),  # 第几章
    'chapter_name': ('chapter_name', 'unicode'),  # 标题
    'wordsId': ('wordsId', 'unicode'),  # 文字
}

# 新手引导对话分组
dialogue_guide_team = {
    'uk': ('id', 'int'),  # 关卡id
    'dialogueId': ('dialogueId', 'int_list'),  # 对话id
    'playbackId': ('playbackId', 'int_list'),  # 剧情回放id
    'type': ('type', 'int'),  # 触发类型
    'condition': ('condition', 'int'),  # 触发条件
}

# 新手引导对话
dialogue_guide = {
    'uk': ('dialogueId', 'int'),  # 对话id
    'roleId': ('roleId', 'int'),  # 角色id
    'type': ('type', 'int'),  # 左右
    'words': ('words', 'unicode'),  # 内容
    'eperssion': ('eperssion', 'str'),  # 控制对话框左侧表情显示
    'dialogKind': ('dialogKind', 'int'),  # 对话框
    'voice': ('voice', 'str'),
}

# 对话及动画位置
opera_location = {
    'uk': ('chapter', 'int'),  # 关卡
    'per_opera': ('per_opera', 'int_float_str'),  # 战前动画
    'in_opera': ('in_opera', 'int_float_str'),  # 战前动画
    'end_opera': ('end_opera', 'int_float_str'),  # 战后动画
}

# 掌上电脑展示
pda = {
    'uk': ('id', 'int'),  # 展示id
    'title': ('title', 'unicode'),  # 标题
    'des': ('des', 'unicode'),  # 内容
    'pic': ('pic', 'str'),  # 图片
}

avg_opera = {
    'uk': ('id', 'int'),
    'opera': ('opera', 'str'),
    'number': ('number', 'int'),
    'before': ('before', 'str_list'),
    'section': ('section', 'str_list'),
    'chapter': ('chapter', 'int'),
    'position': ('position', 'int'),
    'number_n': (('number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'number_6'), ('str_list', 'mult_list1')),
    'note': ('note', 'int'),
}

avg_note = {
    'uk': ('id', 'int'),
    'des1': ('des1', 'unicode'),
    'des2': ('des2', 'unicode'),
    'des3': ('des3', 'unicode'),
    'des4': ('des4', 'unicode'),
    'des5': ('des5', 'unicode'),
    'des6': ('des6', 'unicode'),
    'name1': ('name1', 'unicode'),
    'name2': ('name2', 'unicode'),
    'name3': ('name3', 'unicode'),
    'name4': ('name4', 'unicode'),
    'name5': ('name5', 'unicode'),
    'name6': ('name6', 'unicode'),
}

# 手机互动日常
phone_daily_dialogue = {
    'uk': ('group_id', 'int'),
    'daily_dialogue': ('daily_dialogue', 'int_list'),
    'daily_times': ('daily_times', 'int'),
}

# 手机互动剧情
phone_dialogue = {
    'uk': ('id', 'int'),
    'is_option': ('is_option', 'int'),
    'option_team': ('option_team', 'int_list'),
    'next': ('next', 'int'),
    'is_end': ('is_end', 'int'),
    'hero_id': ('hero_id', 'int'),
    'type': ('type', 'int'),
    'word': ('word', 'int'),
    'reward': ('reward', 'int_list'),
    'add_value': ('add_value', 'int_list'),
    'voice': ('voice', 'str'),
}

# 手机互动剧情触发
phone_chapter_dialogue = {
    'uk': ('id', 'int'),
    'hero_id': ('hero_id', 'int'),
    'chapter_id': ('chapter_id', 'int'),
    'dialogue_id': ('dialogue_id', 'int'),
    'dialogue_name': ('dialogue_name', 'int'),
}