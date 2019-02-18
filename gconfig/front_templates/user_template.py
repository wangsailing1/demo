#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 用户相关的配置
from gconfig import check

common = ({
              'uk': ('id', 'int'),
              'value': ('value', 'int_float_list_or_int_float')
          }, 'common_config')

player_level = {
    'uk': ('lv_addition', 'int'),  # 等级
    'exp': ('exp', 'int'),  # 等级
    'card_limit': ('card_limit', 'int'),  # 艺人上线
    'award': ('award', 'int_list')  # 艺人上线

}

common_attention = {
    'uk': ('id', 'int'),  # 等级
    'name': ('name', 'int'),  # 等级
}

main_hero = {
    'uk': ('id', 'int'),  # id
    'sex': ('sex', 'int'),  # 性别
    'painting': ('painting', 'str'),  # 立绘
    'icon': ('icon', 'str'),  # 初始头像
    'half_painting': ('half_painting', 'str'),  # 半身像
    'price': ('price', 'int')  # 钻石价格
}

# 动作可获得的经验
action_exp = {
    'uk': ('id', 'int'),  # 动作id
    'action_exp': ('action_exp', 'int'),  # 经验
    'action_coin': ('action_coin', 'int'),  # 金币
}

# 标签
tag = {
    'uk': ('id', 'int'),  # 动作id
    'type': ('type', 'int'),  # 标签类型
    'name': ('name', 'int'),  # 标签文本
}

# 标签
tag_score = {
    'uk': ('quality', 'int'),  # 品质
    'score': ('score', 'int'),  # 得分
    'icon': ('icon', 'str'),  # 得分
}

# 测试服初始账号配置
initial_account = ({
                       'uk': ('level', 'int'),  # 等级
                       'good': ('good', 'list_3'),  # 道具
                       'card': ('card', 'list_4'),  # 英雄
                   }, 'initial_account')

# vip_company
vip_company = {
    'uk': ('vip_company', 'int'),  # VIP等级
    'exp': ('exp', 'int'),  # 升至下级所需经验
    'name': ('name', 'int'),
    'icon': ('icon', 'str'),    # Vip等级图标
    'des': ('des', 'int'),      # 特权描述
    'vip_gift_icon': ('vip_gift_icon', 'str_list'),      # vip礼包为空时显示的图标
    'vip_gift_des': ('vip_gift_des', 'str_list'),        # vip礼包为空时显示的图标tips
    'reward': ('reward', 'int_list'),               # Vip特权奖励礼包（免费送）
    'vip_coin_gacha_count': ('vip_coin_gacha_count', 'int'),      # 免费招募次数积累上限
    'buy_point': ('buy_point', 'int'),                              # 购买体力次数上限
    'if_catcher': ('if_catcher', 'int'),                              # 是否解锁娃娃机
    'if_super_catcher': ('if_super_catcher', 'int'),                  # 是否解锁超级娃娃机
    'bussiness_gold': ('bussiness_gold', 'int'),                              # 明星活动金币收益+N%
    # 'bussiness_exp': ('bussiness_exp', 'int'),                              # 明星活动公司经验收益+M%
    'task_cd': ('task_cd', 'int'),                              # 随机任务刷新时间变快N分钟
    # 'buy_gold': ('buy_gold', 'int'),                              # 兑换金币次数+N
    'shop_num': ('shop_num', 'int_list'),                              # 商店限购物品个数+N
    'if_skip_story': ('if_skip_story', 'int'),                              # 可使用跳过剧情功能
    'if_skip_battle': ('if_skip_battle', 'int'),                              # 可使用跳过票房功能
    'card_max': ('card_max', 'int'),                              # 可拥有艺人上限数量+N
    'extra_script': ('extra_script', 'int'),                              # 续作拍摄上限+N档
    'more_license': ('more_license', 'int'),                              # 秘书每天申请许可证数量+L
    'buy_pvp': ('buy_pvp', 'int'),                              # 谁是歌手每日购买次数上限
    'scriptgacha_maxnum': ('scriptgacha_maxnum', 'int'),                              # 抽剧本可积攒的次数上限
    'chapterstage_fastten': ('chapterstage_fastten', 'int'),                              # 快速工作10场
    'script_reselectiontimes': ('script_reselectiontimes', 'int'),                              # 重新选择自制拍摄剧本次数
    'avgdatetimes': ('avgdatetimes', 'int'),                              # 约会次数
    'phonecalltimes': ('phonecalltimes', 'int'),                              # 手机聊天次数
    'title': ('title', 'str'),                             # 标题
    'half': ('half', 'str'),                             # 

}

# VIP
vip = {
    'uk': ('vip', 'int'),  # VIP等级
    'exp': ('exp', 'int'),  # 升至下级所需钻石
    'vip_coin_gacha_count': ('vip_coin_gacha_count', 'int'),  # 免费招募次数积累上限
    'buy_point': ('buy_point', 'int'),  # 购买体力次数上限

    # 'des': ('des', 'unicode'),  # 特权描述
    # 'vip_buy_reward': ('vip_buy_reward', 'list_3'),  # vip特权礼包
    # 'price_off': ('price_off', 'int'),  # 特权礼包购买原价
    # 'price_real': ('price_real', 'int'),  # 特权礼包购买现价
    # 'icon': ('icon', 'str'),  # 本级特权图片
    # 'market_num': ('market_num', 'int'),  # 摊位数量
    # 'hunt_box_times': ('hunt_box_times', 'int'),    # 猛兽宝箱开启次数
    # 'whip_times': ('whip_times', 'int'),    # 皮鞭购买次数上限
    # 'tempt_times': ('tempt_times', 'int'),  # 诱惑购买次数上限
    # 'buy_point': ('buy_point', 'int'),  # 购买体力次数
    # 'arena_buy_times': ('arena_buy_times', 'int'),  # 竞技场购买次数
    # 'arena_refresh_times': ('arena_refresh_times', 'int'),  # 竞技场刷新敌人次数
    # 'guild_technology_cd': ('guild_technology_cd', 'int'),  # 公会科技捐献冷却
    # 'guild_fuben_num': ('guild_fuben_num', 'int'),  # 公会副本次数
    # 'clone_times': ('clone_times', 'int'),  # 克隆玩法次数
    # 'biography_num': ('biography_num', 'int'),  # 传记副本每日可选数
    # 'dark_point': ('dark_point', 'int'),  # 黑街擂台挑战券上限
    # 'vip_daily_reward': ('vip_daily_reward', 'list_3'),     # 每日奖励
    # 'show_type': ('show_type', 'int'),  # 展示类型
    # 'rally_km': ('rally_km', 'int_list'),   # 一键通关层数
    # 'guild_Texas_change_times': ('guild_Texas_change_times', 'int'),     # 德州扑克
    # 'guild_Texas_times': ('guild_Texas_times', 'int'),   # 德州扑克
    # 'duel_auto_enroll': ('duel_auto_enroll', 'int'),  # 大对决自动报名
    # 'gold_exchange_times': ('gold_exchange_times', 'int'),  # 可购买金币次数
    # 'endlesscoin_exchange_times': ('endlesscoin_exchange_times', 'int'),  # 可购买无尽币次数
    # 'whip_num': ('whip_num', 'int'),                # 特权1，监狱皮鞭
    # 'friend_num': ('friend_num', 'int'),            # 好友数量
    # 'reset_dungeon': ('reset_dungeon', 'int'),      # 地城刷新次数
    # 'ten_times': ('ten_times', 'int'),                  # 扫荡10次功能
    # 'dan_color': ('dan_color', 'int'),                  # 弹幕可用颜色数量
    # 'hunt_times': ('hunt_times', 'int'),  # 猛兽通缉令每日挑战次数
    # 'team_skill': ('team_skill', 'int'),  # 游骑兵购买挑战次数上限
    # 'rest_times': ('rest_times', 'int'),  # 关卡每日挑战次数
    # 'dragon_times': ('dragon_times', 'int'),  # 巨龙可购买次数
    # 'buy_slgpoint': ('buy_slgpoint', 'int'),  #购买slg行动力次数
    # 'dark_num': ('dark_num', 'int'),    # 黑街购买次数限制
    # 'ulchallenge_times': ('ulchallenge_times', 'int'),    # 极限挑战每日次数
}

# 主场景配置
city_inside = {
    'uk': ('city_id', 'int'),  # 城市id
    'npc_id': ('npc_id', 'int_list'),  # npc id
}
city_pos = {
    'uk': ('npc', 'int'),  # npc id
    'pos': ('pos', 'int_list'),  # 对应位置
    'face': ('face', 'int'),  # 对应方向
    'oppos': ('oppos', 'int_list'),  # 主角对话的NPC对面的位置
    'opface': ('opface', 'int'),  # 主角对话的NPC对面的方向
    'npc_animation': ('npc_animation', 'str'),  # 动画
    'NPC_drama': ('NPC_drama', 'unicode'),  # 点击触发的对话
    'jump': ('jump', 'str'),  # 跳转到的功能
    'is_animation': ('is_animation', 'str'),  # 是否展示动画
    'is_name': ('is_name', 'str'),  # 是否展示名字
    'is_icon': ('is_icon', 'str'),  # icon
    'block': ('block', 'int'),
}

# 花费钻石配置
vip_pay = {
    'uk': ('pay_id', 'int'),  # 功能id
    'diamond': ('diamond', 'int_list'),  # 消费
}

# 支付表
# charge = {
#     'uk': ('buy_id', 'int'),  # 充值ID
#     'diamond': ('diamond', 'int'),  # 给予钻石数量
#     'gift_diamond': ('gift_diamond', 'int'),  # 赠送钻石数
#     'buy_times': ('buy_times', 'int'),  # 购买限制，1:限购1次，每周刷新，2:限购1次，每月刷新，3:限购1次，永不刷新
#     'is_double': ('is_double', 'int'),  # 是否首次双倍
#     'goodsId': ('goodsId', 'int'),
#     'cost': ('cost', 'str'),  # 商品id
#     'name': ('name', 'unicode'),  # 名字
#     'des': ('des', 'unicode'),  # 描述
#     'icon': ('icon', 'str'),  # ICON
#     'open_gift': ('open_gift', 'int'),  # 购买后开启奖励，0：不开启，1：月卡，2：季卡，3：充值限时礼包
#     'is_show': ('is_show', 'int'),  # 是否显示充值项
#     'gift_reward_id': ('gift_reward_id', 'int'),  # 限时礼包奖励
#     'charge_reward': ('charge_reward', 'list_3'),  # 充值项奖励
#     'charge_anim': ('charge_anim', 'str'),  # 充值项奖励的图或动画
#     'charge_icon': ('charge_icon', 'str'),
#     'price_CN': ('price_CN', 'float'),  # 所需金额
#     'price_TW': ('price_TW', 'float'),  # 所需金额
#     'price_TWD': ('price_TWD', 'float'),  # 所需金额
#     'charge_condition': ('charge_condition', 'int_list'),  # 充值限制（写谁，该充值项不算谁1累充，2.首充）
# }

charge = {
    'uk': ('buy_id', 'int'),  # id
    'sort': ('sort', 'int'),  # 购买类型
    'diamond': ('diamond', 'int'),  # 给予钻石数量
    'gift_diamond': ('gift_diamond', 'int'),  # 赠送钻石数
    'is_double': ('is_double', 'int'),  # 是否首次双倍
    'vip_exp': ('vip_exp', 'int'),  # vip经验
    'price_rmb': ('price_rmb', 'int'),  # 所需RMB
    'price_dollar': ('price_dollar', 'float'),  # 所需美元
    'name': ('name', 'int'),  # 名字
    'icon': ('icon', 'str'),  # 图
    'charge_condition': ('charge_condition', 'str'),  #
    'gift': ('gift', 'int_list'),  #
}

month_privilege = {
    'uk': ('card_type', 'int'),  # id
    'price': ('price', 'int'),  # 所需RMB
    'effective_days': ('effective_days', 'int'),  # 持续天数
    'daily_rebate': ('daily_rebate', 'int_list'),  # 每日奖励
    'des': ('des', 'int'),  # 每日奖励
}

charge_ios = {
    'uk': ('suit_id', 'str'),
    'goods_id': ('goods_id', 'str'),
}

# 采集、生产加速花费配置
speed_up_cost = {
    'uk': ('time', 'int'),  # 时间段(s)
    'cost_1s': ('cost_1s', 'float'),  # 单位时间花费
    'sum_cost': ('sum_cost', 'float'),  # 累计花费
}

# 建造功能解锁
building_unlock = {
    'uk': ('id', 'int'),  # id
    'name': ('name', 'unicode'),  # 名字
    'icon': ('icon', 'str'),  # 图标
    'unlock_type': ('unlock_type', 'int'),  # 解锁类型
    'unlock_look': ('unlock_look', 'int'),  # 可见条件
    'unlock_limit': ('unlock_limit', 'int'),  # 解锁限制
}

# 币种固定比例兑换
currency_exchange = {
    'uk': ('id', 'int'),  # id
    'exchange_cost': ('exchange_cost', 'int'),  # 兑换币种类型
    'exchange_get': ('exchange_get', 'int'),  # 获得币种类型
    'proportion': ('proportion', 'int'),  # 兑换比例（获得币种/花费币种，c/b）
    'limit_up': ('limit_up', 'int'),  # 单次兑换获得币种上限
}

# value参数
value = {
    'uk': ('id', 'int'),  # id
    'value': ('value', 'int_float_list_or_int_float'),  # 值
}

# 特权类型
privilege = {
    'uk': ('id', 'int'),  # 编号
    'icon': ('icon', 'str'),  # 图片
    'story': ('story', 'unicode'),  # 说明
    'order': ('order', 'int'),  # 排序
}

# 特权礼包
charge_privilege = {
    'uk': ('buy_id', 'int'),  # 购买的ID
    'order': ('order', 'int'),  # 排列顺序
    'type': ('type', 'int'),  # 所需币种 1: 人民币 2: 钻石  3: 金币
    'price': ('price', 'int'),  # 所需价格
    'name': ('name', 'unicode'),  # 名称
    'time': ('time', 'int'),  # 特权有效时间, 单位分钟
    'icon': ('icon', 'str'),  # 特权图标
    'privilege': (('privilege1', 'value1', 'privilege2', 'value2', 'privilege3', 'value3',  # 特权礼包
                   'privilege4', 'value4', 'privilege5', 'value5', 'privilege6', 'value6',
                   'privilege7', 'value7', 'privilege8', 'value8', 'privilege9', 'value9',
                   'privilege10', 'value10', 'privilege11', 'value11', 'privilege12', 'value12',
                   'privilege13', 'value13', 'privilege14', 'value14', 'privilege15', 'value15',
                   'privilege16', 'value16', 'privilege17', 'value17', 'privilege18', 'value18',
                   'privilege19', 'value19', 'privilege20', 'value20'),
                  ('int_list_or_int', 'list_2_to_list')),  # 购买的ID
}
#
# # 新手引导
# guide = {
#     'uk': ('id', 'int'),  # 引导id
#     'sort': ('sort', 'int'),  # 类型
#     'aim': ('aim', 'int'),  # 目标步骤
#     'level': ('level', 'int'),  # 关健步
#     'key': ('key', 'str'),  # 关键字
#     'action': ('action', 'int'),  # 动作
#     'trigger': ('trigger', 'int_list'),  # 条件
#     'delay': ('delay', 'float'),  # 延迟
#     'target': ('target', 'int_list'),  # 动作目标
#     'target_data': ('target_data', 'int_list'),  # 动作参数
#     'next': ('next', 'int'),  # 下一步
#     'drama': ('drama', 'int'),  # 剧情id
#     'skip': ('skip', 'int'),  # 跳过按钮的位置
#     'free': ('free', 'int'),
#     'des': ('des', 'unicode'),
# }

mission_guide = {
    'uk': ('id', 'int'),  # id
    'icon': ('icon', 'str'),  # 图标
    'name': ('name', 'unicode'),  # 任务名
    'des': ('des', 'unicode'),  # 任务描述
    'finish_board': ('finish_board', 'unicode'),  # 完成任务显示说明
    'reward_show': ('reward_show', 'list_3'),  # 奖励展示
}

# 引导组
# guide_team = {
#     'uk': ('id', 'int'),  # 引导组id
#     'start_id': ('start_id', 'int'),  # 起始id
#     'open_level': ('open_level', 'int'),  # 激活等级
#     'type': ('type', 'int'),  # 引导类型
#     'sort': ('sort', 'int'),  # 引导分组
#     'is_open': ('is_open', 'int'),  # 是否开启
#     'is_done': ('is_done', 'int_list'),  # 是否完成
# }

# 初始数据
# initial_data = {
#     'uk': ('id', 'int'),                            # id
#     'reward': ('reward', 'int_list_or_int'),        # 初始物品
#     'sort': ('sort', 'int'),                        # 类型
# }


# 主角姓名随机
first_random_name = ({
                         'uk': ('first_name', 'unicode'),  # 名字
                     }, 'first_random_name')

# 主角姓名随机
last_random_name = ({
                        'uk': ('last_name', 'unicode'),  # 名字
                        'gender': ('gender', 'int'),  # 类型
                    }, 'last_random_name')

# 剧情对话
drama = {
    'uk': ('dramaID', 'int'),  # 对话id
    'start_sort': ('start_sort', 'int'),  # 类型
    'drama_detail': ('drama_detail', 'mix_list_unicode_list'),  # 对话内容
}

# runtimer测试
test_config = {
    'uk': ('id', 'int'),
    'version': ('version', 'int'),
    'reward_time': ('reward_time', 'str'),
}

# 版本强制更新表
version = {
    'uk': ('platform', 'str'),
    'version': ('version', 'str'),
    'url': ('url', 'str'),
    'msg': ('msg', 'unicode'),
}


# 战队技能表
team_skill = {
    'uk': ('skill_id', 'int'),  # 技能id
    'next_id': ('next_id', 'int'),  # 子id
    'skill_sort': ('skill_sort', 'int'),  # 技能大id
    'lvl': ('lvl', 'int'),  # 技能等级
    'name': ('name', 'unicode'),  # 技能名称
    'icon': ('icon', 'str'),  # 技能图标
    'story': ('story', 'unicode'),  # 技能描述
    'script': ('script', 'str'),  # 技能脚本
    'unlock_level': ('unlock_level', 'int'),  # 解锁等级
    'stone_cost': ('stone_cost', 'int'),  # 升级消耗(技能碎片)
    'lvl_up': ('lvl_up', 'int'),  # 升级消耗（银币）
    'skill_type': ('skill_type', 'int'),  # 技能类型
    'skill_attribute': ('skill_attribute', 'list_2'),  # 升级提升属性
    'target': ('target', 'int'),  # 目标类型
    'skill_effect_sort': ('skill_effect_sort', 'int'),  # 技能种类
    'effect_value': ('effect_value', 'int'),  # 技能取值
    'skill_effect': ('skill_effect', 'float'),  # 技能数值
    'add_buff': ('add_buff', 'int_list'),  # 附带特效id
    'skill_max': ('skill_max', 'int'),  # 最大技能
    'if_teamskill': ('if_teamskill', 'int'),
    'pre_cd': ('pre_cd', 'int'),  #
}

# 战队技能碎片
skill_stone = {
    'uk': ('id', 'int'),  # 编号
    'name': ('name', 'unicode'),  # 名称
    'icon': ('icon', 'str'),  # 图标
    'price': ('price', 'int'),  # 出售价格
    'skill_sort': ('skill_sort', 'int'),  # 对应战队技能大id
    'guide': ('guide', 'list_int_list'),  # 掉落指引
    'story': ('story', 'unicode'),  # 描述
}

# 战队技能熟练度
team_skill_mastery = {
    'uk': ('skill_id', 'int'),  # 技能id
    'value': ('value', 'int_or_float_list'),  # 百分比
}
team_skill_mastery_up = {
    'uk': ('lvl', 'int'),  # 等级
    'exp': ('exp', 'int'),  # 升级经验
}
team_skill_lvl_up = {
    'uk': ('team_skill_lvl', 'int'),  # 等级
    'exp': ('exp', 'int'),  # 升级经验
    'attribute': ('attribute', 'list_2'),  # 团队属性加成
}

team_skill_unlock = {
    'uk': ('skill_id', 'int'),  # 技能id
    'team_skill_lvl': ('team_skill_lvl', 'int'),  # 需要的战队技能等级
}

# 玩家头像
player_icon = {
    'uk': ('id', 'int'),  # 头像编号
    'icon': ('icon', 'str'),  # 图标
    'des': ('des', 'unicode'),  # 解锁描述
    'sort': ('sort', 'int'),  # 解锁类型
    'value': ('value', 'int'),  # 解锁类型
}

# 敏感词
dirtyword_ch = ({
                    'uk': ('dirtyword', 'unicode'),
                }, 'dirtyword')

# 主页按钮配置
# homepage_button = {
#     'uk': ('id', 'int'),  # 按钮id
#     'build': ('build', 'int'),  # 建筑位置
#     'sort': ('sort', 'int'),  # 按钮类型
#     'name': ('name', 'unicode'),  # 名字
#     'unlock_lvl': ('unlock_lvl', 'int'),  # 解锁等级
#     'icon': ('icon', 'str'),  # icon
#     'jump': ('jump', 'str'),  # 跳转
#     'button': (('button1', 'button2', 'button3', 'button4', 'button5',
#                 'button6', 'button7', 'button8', 'button9', 'button10',
#                 'button11', 'button12', 'button13', 'button14', 'button15'), ('int', 'mult_list')),  # 按钮子按钮1-10
#     'father': ('father', 'int'),  # 父按钮
#     'msg': ('msg', 'unicode'),  # 功能描述
#     'order': ('order', 'int'),  # 前端显示
#     'reward_info': ('reward_info', 'unicode'),  # 奖励说明
# }

homepage_button = {
    'uk': ('id', 'int'),
    'order': ('order', 'int'),
    'group': ('group', 'int'),
    'sort': ('sort', 'int'),
    'unlock_lvl': ('unlock_lvl', 'int'),
    'unlock_guide_team': ('unlock_guide_team', 'int'),
    'icon': ('icon', 'str'),
    'jump': ('jump', 'int'),
    'button': (('button1', 'button2', 'button3', 'button4', 'button5'), ('int', 'mult_list')),
    'direction': ('direction', 'int'),
    'name': ('name', 'int'),
    'red_point': ('red_point', 'int'),
    'quick_jump': ('quick_jump', 'int'),
}

# 跑马灯配置
message = {
    'uk': ('id', 'int'),  # 条件id
    'sort': ('sort', 'int'),  # 条件类型
    'target1': ('target1', 'int_list_or_int2'),  # 条件目标
    'target2': ('target2', 'int'),  # 条件目标
    'des': ('des', 'unicode_list'),  # 信息内容
    'is_show': ('is_show', 'int'),  # 开关
}

# 提示系统功能
play_help = {
    'uk': ('id', 'int'),  # id
    'name': ('name', 'unicode'),  # 名称
    'name2': ('name2', 'unicode'),  # 名称
    'icon': ('icon', 'str'),  # icon
    'sort': ('sort', 'int'),  # 类型
    'show_lvl': ('show_lvl', 'int_list'),  # 显示等级
    'des': ('des', 'unicode'),  # 描述
    # 'show_sort': ('show_sort', 'int'),      # 显示额外条件
    'jump': ('jump', 'int'),  # 前往
    # 'priority': ('priority', 'int'),        # 优先级
    'unlock_lv': ('unlock_lv', 'int'),  # 解锁等级
}

# 推送消息
push_message = {
    'uk': ('id', 'int'),  # 推送id
    'push_sort': ('push_sort', 'int'),  # 推送类型
    'push_condition': ('push_condition', 'int'),  # 推送条件
    'title': ('title', 'unicode'),  # 标题
    'message': ('message', 'unicode'),  # 信息内容
    'time_sort': ('time_sort', 'int'),
    'time': ('time', 'int'),
    'loop': ('loop', 'int'),
}

# # 等级邮件
level_mail = {
    'uk': ('id', 'int'),  # id
    'level': ('level', 'int'),  # 等级
    'name': ('name', 'unicode'),  # 标题
    'des': ('des', 'unicode'),  # 描述
    'reward': ('reward', 'list_3'),  # 奖励
}

# 等级限时礼包
level_gift = {
    'uk': ('level', 'int'),  # 等级
    'reward': ('reward', 'list_3'),  # 奖励
    'coin': ('coin', 'int'),  # 钻石购买
    'buy': ('buy', 'int'),  # 充值id
    'des': ('des', 'unicode'),  # 描述
    'des2': ('des2', 'unicode'),  # 描述
}

# 新服活动时间配置
server_inreview = {
    'uk': ('ID', 'int'),
    'banner': ('banner', 'str'),
    'is_open': ('is_open', 'int'),
    # 'show_id': ('show_id', 'int'),
    # 'mark': ('mark', 'int'),
    'name': ('name', 'str'),
    # 'story': ('story', 'unicode'),
    # 'default': ('default', 'unicode'),
    'show_lv': ('show_lv', 'int'),
    # 'sort': ('sort', 'int'),
}

# 称号
title = {
    'uk': ('id', 'int'),
    'series': ('series', 'int'),
    'icon': ('icon', 'str'),
    'name': ('name', 'unicode'),
    'des': ('des', 'unicode'),
    'quality': ('quality', 'int'),
    'sort': ('sort', 'int'),
    'target1': ('target1', 'int'),
    'target2': ('target2', 'int'),
    'first_reward': ('first_reward', 'int_list'),
    'reward': ('reward', 'int_or_float_list'),
    'des1': ('des1', 'unicode'),
    'des2': ('des2', 'unicode'),
    'grade': ('grade', 'str'),
}

# 点金手
# gold_exchange = ({
#     'uk': ('id', 'int'),
#     'coin': ('coin', 'int_list'),           # 每次兑换活动的金币
#     'cost': ('cost', 'int_list'),       # 花费
#     # 'weight1': ('weight1', 'list_2'),   # 暴击权重
#     # 'times': ('times', 'int'),          # 每xx次必定暴击
#     # 'weight2': ('weight2', 'list_2'),   # 必定暴击权重
# }, 'buy_silver')
gold_exchange = {
    'uk': ('id', 'int'),
    'level': ('level', 'int'),
    'coin': ('coin', 'int_list'),  # 每次兑换活动的金币
    'cost': ('cost', 'int_list'),  # 花费
    # 'weight1': ('weight1', 'list_2'),   # 暴击权重
    # 'times': ('times', 'int'),          # 每xx次必定暴击
    # 'weight2': ('weight2', 'list_2'),   # 必定暴击权重
}

# longing界面
loading_des = {
    'uk': ('id', 'int'),
    'loading_icon': ('loading_icon', 'str'),
    'hero_id': ('hero_id', 'int'),
    'skill_id': ('skill_id', 'int'),
    'loading_des': ('loading_des', 'unicode'),
    'color': ('color', 'int_list'),
    'color2': ('color2', 'int_list'),
    'pro': ('pro', 'str'),
}

loading_gif = {
    'uk': ('id', 'int'),
    'loading_icon': ('loading_icon', 'str'),
    'loading_des': ('loading_des', 'unicode_list'),
}

# 功能说明
help = {
    'uk': ('jump_id', 'str'),
    'text_pic': ('text_pic', 'str'),
    'text_picnum': ('text_picnum', 'int'),
}

# 升级解锁功能引导
guide_unlock = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),
    'icon': ('icon', 'str'),
    'desc': ('desc', 'unicode'),
    'unlock_limit': ('unlock_limit', 'int'),
    'index': ('index', 'str'),
}

jump = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),
    'des': ('des', 'unicode'),
    'target': ('target', 'int_list'),
    'unlock': ('unlock', 'int'),
    'icon': ('icon', 'str'),
    'button_id': ('button_id', 'int'),
    'close_under': ('close_under', 'int'),
}

item_coin = {
    'uk': ('id', 'int'),
    'name': ('name', 'unicode'),
    'icon': ('icon', 'str'),
    'story': ('story', 'str'),
    'quality': ('quality', 'int'),
    'guide': ('guide', '2int_list'),
}

login_reward_id = {
    'uk': ('id', 'int'),
    'title': ('title', 'unicode'),
    'time_format': ('time_format', 'int'),
    'open': ('open', 'str'),
    'close': ('close', 'str'),
    'reward': ('reward', 'int_list'),
    'des': ('des', 'unicode'),
    'level': ('level', 'int_list'),
    'vip': ('vip', 'int_list'),
    'server': ('server', 'str_list'),
    'uid_list': ('uid_list', 'str_list'),
    'url': ('url', 'str'),
}

money_guide = {
    'uk': ('id', 'int'),
    'guide': ('guide', 'int_list'),
    'des': ('des', 'unicode'),
}

server_type = {
    'uk': ('server_id', 'int'),
    'time': ('time', 'str'),
    'type': ('type', 'int'),
}
