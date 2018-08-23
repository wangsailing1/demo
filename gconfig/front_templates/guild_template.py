#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 公会相关的配置
from gconfig import check


# 公会基础表
guild_build = ({
    'uk': ('lv', 'int'),                        # 创建公会等级
    'cost': ('cost', 'list_3'),                 # 所需金钱
    'applymax': ('applymax', 'int'),            # 申请限制
    'change_name': ('change_name', 'list_3'),   # 改名花费
    'per_applymax': ('per_applymax', 'int'),    # 玩家最多同时申请公会个数
    'lvl_limit': ('lvl_limit', 'int_list'),     # 加入等级显示
}, 'grade_guild_build')


# 公会经验
guild_info = {
    'uk': ('lv', 'int'),  # 公会等级
    'exp': ('exp', 'int'),  # 公会升级所需经验（累计经验）
    'maxmember': ('maxmember', 'int'),  # 公会的人数上限
    'protect_num': ('protect_num', 'int'),  # 公会护卫人数
    'reward_percent': ('reward_percent', 'int'),  # 公会护卫雇佣获得金钱百分比
    'technology_limit': ('technology_limit', 'int'),  # 公会科技等级上限
}

# 护卫挂机雇佣金钱结算
guild_protect_money = ({
    'uk': ('hire_basis', 'int'),  # 雇佣基础花费
    'hire_effective': ('hire_effective', 'int'),  # 雇佣战斗力花费系数
    'protect_basis': ('protect_basis', 'int'),  # 挂机基础收益（30分钟）
    'protect_effective': ('protect_effective', 'int'),  # 挂机战斗力收益系数（30分钟）
}, 'guild_protect_money')

# 公会科技升级表
guild_technology_lvlup = {
    'uk': ('lvl', 'int'),       # 科技等级
    'exp': ('exp', 'int'),      # 升级所需经验
}

# 公会科技
guild_technology = {
    'uk': ('id', 'int'),                        # 科技id
    'icon': ('icon', 'str'),                    # 科技图标
    'name': ('name', 'unicode'),                # 科技名称
    'sort': ('sort', 'int'),                    # 科技加成类型
    'attr': ('attr', 'int'),                    # 属性类型
    'attribute': ('attribute', 'int_list'),     # 属性值
    'cost': (('cost1', 'cost2', 'cost3'), ('list_4', 'mult_dict_1')),   # 捐献消耗
    'guild_limit': ('guild_limit', 'int'),      # 解锁公会等级
    'des': ('des', 'unicode'),  # 描述
}


# 公会战主题
guild_war_theme = {
    'uk': ('id', 'int'),            # 主题id
    'name': ('name', 'unicode'),    # 主题名称
    'banner': ('banner', 'str'),    # banner图
    'hero_limit': ('hero_limit', 'int_list'),   # 英雄限制
    # 'weight': ('weight', 'int'),    # 权重
}


# 公会战配置
guild_war = ({
    'uk': ('num_limit', 'int'),                             # 开公会战最低要求人数
    'sign_up_time': ('sign_up_time', 'str_list'),           # 公会战报名时间
    'attack_time': ('attack_time', 'str_list'),             # 本服公会战攻打时间
    'prepare_time': ('prepare_time', 'str_list'),           # 全服公会战准备时间
    'all_attack_time': ('all_attack_time', 'str_list'),     # 全服公会战攻打时间
}, 'guild_war')


# 公会战精力配置
guild_war_reward = {
    'uk': ('id', 'int'),        # 奖励id
    'per_reward': (('per_reward', 'per_reward1'), ('list_3', 'mult_dict_0')),               # 个人奖励(0:战胜,1:战败)
    'guild_integral': (('guild_integral', 'guild_integral1'), ('int', 'mult_dict_0')),      # 公会积分(0:战胜,1:战败)
}


# 公会战排名奖励配置
guild_war_rank_reward = {
    'uk': ('id', 'int'),        # 奖励id
    # 'rank_guild_reward': (('rank_guild_reward', 'rank_guild_reward2'), ('int', 'mult_dict_0')),  # 公会奖励(0:本服,1:全服)
    'rank_per_reward': (('rank_per_reward', 'rank_per_reward2'), ('list_3', 'mult_dict_0')),        # 个人奖励(0:本服,1:全服)
}


# 公会图标
guild_icon = {
    'uk': ('id', 'int'),        # 图标id
    'icon': ('icon', 'str'),    # 图标
}


# # 公会副本奖励配置
# guild_boss_reward = {
#     'uk': ('id', 'int'),                # 奖励id
#     'reward': ('reward', 'list_3'),     # 奖励
#     'num': ('num', 'int'),              # 奖励的数量
# }


# 公会金币副本配置
guild_boss_coin = {
    'uk': ('id', 'int'),                            # 据点id
    'name': ('name', 'unicode'),                    # 据点名称
    'icon': ('icon', 'str'),                        # icon
    'guild_lvl': ('guild_lvl', 'int'),              # 公会等级限制
    'boss_id': ('boss_id', 'int_list'),             # 怪物配置
    # 'damage_rate': ('damage_rate', 'float'),        # 单位伤害金币系数
    'round': ('round', 'int'),                      # 单次挑战回合上限
    # 'single_reward_limit': ('single_reward_limit', 'int'),   # 个人挑战金币奖励上限
    'chest_reward': ('chest_reward', 'int_list'),   # 宝箱奖励
    'kill_reward': ('kill_reward', 'list_3'),       # 击杀奖励
}


# 公会经验副本配置
guild_boss_exp = {
    'uk': ('id', 'int'),                            # 据点id
    'name': ('name', 'unicode'),                    # 据点名称
    'guild_lvl': ('guild_lvl', 'int'),              # 公会等级限制
    'boss_id': ('boss_id', 'int_list'),             # 怪物配置
    # 'damage_rate': ('damage_rate', 'float'),        # 单位伤害金币系数
    'exp_id': ('exp_id', 'list_3'),                 # 奖励物品id
    'round': ('round', 'int'),                      # 单次挑战回合上限
    # 'single_reward_limit': ('single_reward_limit', 'int'),   # 个人挑战金币奖励上限
    'chest_reward': ('chest_reward', 'int_list'),   # 宝箱奖励
    'kill_reward': ('kill_reward', 'list_3'),       # 击杀奖励
}


# 捐献
guild_donate = {
    'uk': ('donate_id', 'int'),         # 档次
    'tech_exp': ('tech_exp', 'int'),    # 获得经验
    'honor': ('honor', 'int'),          # 获得荣耀
    'rate2': ('rate2', 'int'),          # 开启档次2捐献概率
    'rate3': ('rate3', 'int'),          # 开启档次3捐献概率
}

#
# # 公会吧台英雄
# guild_barhero = {
#     'uk': ('hero_id', 'int'),  # 吧台英雄id
#     'deck_id': ('deck_id', 'int'),  # 英雄昆特牌牌组
#     'game_win': ('game_win', 'list_3'),  # 玩家小游戏胜利
#     'game_lose': ('game_lose', 'list_3'),  # 玩家小游戏失败
#     'chat': ('chat', 'int_list'),  # 聊天事件
#     'hero_icon': ('hero_icon', 'str'),  # 英雄立绘
#     'gift_like': ('gift_like', ('list_2', 'dict')),  # 英雄礼品偏好
#     'story': (('story1', 'story2', 'story3', 'story4', 'story5', 'story6', 'story7'),
#               ('unicode', 'mult_dict_1')),  # 显示内容
#     'heroevent_id': ('heroevent_id', 'int_list'),  # 触发的邀约事件
# }
#
#
# # 吧台英雄闲聊
# guild_barchat = {
#     'uk': ('id', 'int'),  # 聊天事件id
#     'chat1': ('chat1', 'mix_list_unicode_list'),  # 对话内容1
#     'choose': ('choose', 'mix_list_unicode_list'),  # 选择内容
#     'choose1': ('choose1', 'mix_list_unicode_list'),  # 选择以后的对话内容1
#     'choose2': ('choose2', 'mix_list_unicode_list'),  # 选择以后的对话内容2
#     'choose3': ('choose3', 'mix_list_unicode_list'),  # 选择以后的对话内容3
#     'reward': ('reward', 'list_3'),  # 奖励物品
# }
#
#
# # 吧台英雄邀约
# guild_heroevent = {
#     'uk': ('id', 'int'),  # 邀约事件id
#     'name': ('name', 'unicode'),  # 邀约事件名称
#     'favor_limit': ('favor_limit', 'int'),  # 好感度等级限制
#     'order': ('order', 'int'),  # 显示排列顺序
#     'chat1': ('chat1', 'mix_list_unicode_list'),  # 对话内容1
#     'choose': ('choose', 'mix_list_unicode_list'),  # 选择内容
#     'choose1': ('choose1', 'mix_list_unicode_list'),  # 选择以后的对话内容1
#     'choose2': ('choose2', 'mix_list_unicode_list'),  # 选择以后的对话内容2
#     'choose3': ('choose3', 'mix_list_unicode_list'),  # 选择以后的对话内容3
#     'backdrop': ('backdrop', 'str'),  # 背景图片
#     'reward': ('reward', 'list_3'),  # 奖励物品
# }
#
#
# # 公会英雄好感度
# guild_herofavor = {
#     'uk': ('lv', 'int'),  # 好感度等级
#     'exp': ('exp', 'int'),  # 好感度升级所需经验
#     'reward': ('reward', 'list_3'),  # 升级时会获得物品奖励
# }
#
#
# # 吧台英雄礼品
# guild_herogift = {
#     'uk': ('id', 'int'),  # 礼品ID
#     'name': ('name', 'unicode'),  # 物品名
#     'favor': ('favor', 'int'),  # 增加好感度的值
#     'cost': ('cost', 'int'),  # 购买一次该礼品花费的钻石
#     'icon': ('icon', 'str'),  # 物品图标
# }
#
#
# # 昆特牌配置
# card_detail = {
#     'uk': ('id', 'int'),                  # 卡牌id
#     'name': ('name', 'unicode'),          # 卡牌名称
#     'type': ('type', 'int'),              # 卡牌的类型
#     'OCC': ('OCC', 'int'),                # 卡牌职业id
#     'country': ('country', 'int'),        # 卡牌种族id
#     'star': ('star', 'int'),              # 卡牌稀有度
#     'atk': ('atk', 'int'),                # 卡牌战斗力
#     'image': ('image', 'str'),            # 卡牌的大图
#     'icon': ('icon', 'str'),              # 卡牌的小头像
#     'samename': ('samename', 'str'),      # 判别同名
#     'skill': (('skill1', 'skill2', 'skill3'), ('int', 'mult_list')),  # 技能
# }
#
#
# # 昆特牌技能配置
# gwentcard_skill = {
#     'uk': ('id', 'int'),                # 技能id
#     'sort': ('sort', 'int'),            # 技能类型
#     'name': ('name', 'unicode'),        # 技能名称
#     'value1': ('value1', 'int'),        # 技能效果1
#     'value2': ('value2', 'int'),        # 技能效果2
#     'icon': ('icon', 'str'),            # 技能图标
#     'des': ('des', 'unicode'),          # 技能描述
# }
#
#
# # 昆特牌卡牌牌组
# gwentcard_deck = {
#     'uk': ('id', 'int'),                # 牌组id
#     'deck_hero': ('deck_hero', 'int'),  # 昆特牌领导
#     'deck': ('deck', 'int_list'),       # 牌组
# }
#
#
# # 昆特牌领导牌
# gwentcard_hero = {
#     'uk': ('id', 'int'),                    # 领导id
#     'name': ('name', 'unicode'),            # 领导姓名
#     'icon': ('icon', 'str'),                # 领导头像
#     'country': ('country', 'int'),          # 领导阵营
#     'skill': ('skill', 'int'),              # 领导技能
#     'skill_des': ('skill_des', 'unicode'),  # 技能描述
#     'deck': ('deck', 'int_list'),           # 默认牌组
# }
#
#
# # 昆特牌匹配机器人
# pvp_gwentrobot = {
#     'uk': ('id', 'int'),            # 机器人id
#     'rank': ('rank', 'int_list'),   # 机器人rank值
#     'name': ('name', 'unicode'),    # 机器人名字
#     'deck_id': ('deck_id', 'int'),  # 机器人昆特牌牌组
# }
#
#
# # 昆特牌rank值匹配
# pvp_gwentcard = {
#     'uk': ('id', 'int'),                # 段位id
#     'rank': ('rank', 'int_list'),       # rank值范围
#     'win_a': ('win_a', 'int'),          # 胜利常数a的值
#     'win_b': ('win_b', 'int'),          # 胜利常数b的值
#     'lose_a': ('lose_a', 'int'),        # 失败常数a的值
#     'lose_b': ('lose_b', 'int'),        # 失败常数b的值
#     'rank_add': ('rank_add', 'int'),    # 匹配离线玩家或电脑时，要加的参数
# }
#
# # 公会交易
# guild_trade = {
#     'uk': ('id', 'int'),  # 订单编号
#     'sort': ('sort', 'int'),  # 订单类型
#     'name': ('name', 'unicode'),  # 订单名称
#     'item_name': ('item_name', 'unicode'),  # 要求物品名
#     'item_icon': ('item_icon', 'str'),  # 要求物品图标
#     'item_num': ('item_num', 'int'),  # 需求数量
#     'reward': ('reward', 'list_3'),  # 单位进度物品数值奖励
#     'reward_num': ('reward_num', 'int'),  # 单位进度
#     'player_exp': ('player_exp', 'int'),  # 单位进度物品经验奖励
#     'story': ('story', 'unicode'),  # 订单描述
#     'exp': ('exp', 'int'),  # 单位进度订单后获得的公会经验
# }
#
#
# # 公会任务
# guild_task = {
#     'uk': ('id', 'int'),  # 任务编号
#     'sort': ('sort', 'int'),  # 任务类型
#     'name': ('name', 'unicode'),  # 任务名
#     'value': ('value', 'int_list_or_int'),  # 任务完成条件
#     'reward': ('reward', 'list_3'),  # 任务奖励
#     'story': ('story', 'int'),  # 任务描述
#     'icon': ('icon', 'int'),  # 任务图标
#     'exp': ('exp', 'int'),  # 公会经验
# }

# 德州扑克牌信息
guild_texas = {
    'uk': ('id', 'int'),                            # id
    'colour': ('colour', 'str'),                    # 花色
    'number': ('number', 'int'),                    # 数字
    'card_icon': ('card_icon', 'str'),              # 图案
}

# 德州扑克奖励配置
guild_texas_reward = {
    'uk': ('id', 'int'),                            # id
    'reward': ('reward', 'list_3'),                 # 奖励
    'point': ('point', 'int'),                      # 点数
    'name': ('name', 'unicode'),                    # 牌型名
    'des': ('des', 'unicode'),                      # 描述
}

# 德州扑克奖励配置
guild_texas_point_reward = {
    'uk': ('id', 'int'),                            # id
    'reward_guild': ('reward_guild', 'list_3'),     # 公会积分奖
    'reward_all': ('reward_all', 'list_3'),         # 本服积分奖
    'mail_title': ('mail_title', 'unicode'),         # 邮件标题
    'mail_guild': ('mail_guild', 'unicode'),         # 公会邮件内容
    'mail_all': ('mail_all', 'unicode'),             # 本服邮件内容
}


# 公会副本奖励配置
guild_boss_reward = {
    'uk': ('id', 'int'),                            # 据点id
    'damage': ('damage', 'int_list'),               # 伤害
    'coin_ratio': ('coin_ratio', 'float'),          # 单位金币价值
    'exp_ratio': ('exp_ratio', 'float'),            # 单位经验价值
}


# 公会副本击杀奖励
guild_boss_killreward = {
    'uk': ('id', 'int'),                            # id
    'guild_boss_killreward': ('guild_boss_killreward', 'list_3'),  # 奖励
    'guild_boss_allreward': ('guild_boss_allreward', 'list_3'),   # 全员奖励
    # 'title': ('title', 'unicode'),  # 邮件标题
    # 'des': ('des', 'unicode'),      # 邮件内容
}

# 公会副本里程碑奖励
guild_boss_breakreward = {
    'uk': ('id', 'int'),                            # id
    'times': ('times', 'int'),                      # 次数
    'reward': ('reward', 'list_3'),                 # 奖励
}

# 公会排名奖励
guild_boss_rankreward = {
    'uk': ('id', 'int'),                # id
    'rank': ('rank', 'int_list'),     # 奖励
    'reward1': ('reward1', 'list_3'),  # 奖励
    'reward2': ('reward2', 'list_3'),  # 奖励
    'reward3': ('reward3', 'list_3'),  # 奖励
    'reward4': ('reward4', 'list_3'),  # 奖励
    'title': ('title', 'unicode'),      # 邮件标题
    'des': ('des', 'unicode'),          # 公会邮件内容
}

# 公会BOSS血量变化
guild_boss_hp = {
    'uk': ('id', 'int'),                # id
    'boss_id': ('boss_id', 'int'),      # boss_id
    'round': ('round', 'int'),          # 回合上限
    'open_time': ('open_time', 'str'),  # 开启时间
    'boss_hp_basis': ('boss_hp_basis', 'int'),          # BOSS初始血量、最低血量
    'time_condition1': ('time_condition1', 'int_list'),  # 条件
    'time_condition2': ('time_condition2', 'int_list'),  # 条件
    'time_condition3': ('time_condition3', 'int_list'),  # 条件
    'lefthp_condition1': ('lefthp_condition1', 'int_list'),  # 条件
    'lefthp_condition2': ('lefthp_condition2', 'int_list'),  # 条件
    'lefthp_condition3': ('lefthp_condition3', 'int_list'),  # 条件
    'kill_time1': ('kill_time1', 'float'),  # 血量变化
    'kill_time2': ('kill_time2', 'float'),  # 血量变化
    'kill_time3': ('kill_time3', 'float'),  # 血量变化
    'kill_time4': ('kill_time4', 'float'),  # 血量变化
    'kill_time5': ('kill_time5', 'float'),  # 血量变化
    'kill_time6': ('kill_time6', 'float'),  # 血量变化
}
