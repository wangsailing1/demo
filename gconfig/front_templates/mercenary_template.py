#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check


# 雇佣系统
mercenary = {
    'uk': ('times', 'int'),     # 雇佣次数
    'cost': ('cost', 'int'),    # 雇佣花费（金币）
}


# 雇佣系数
mercenary_value = {
    'uk': ('grade', 'int'),     # 英雄资质
    'value_basis': ('value_basis', 'int'),  # 基础
    'fate_rate': ('fate_rate', 'int'),      # 缘分系数
    'gene_rate1': ('gene_rate1', 'int'),    # 2件套
    'gene_rate2': ('gene_rate2', 'int'),    # 4件套
}


#
mercenary_select = {
    'uk': ('job', 'int'),                   # 英雄职业下拉
    'grade': ('grade', 'int'),              # 英雄资质下拉
    'cost_down': ('cost_down', 'int'),      # 雇佣花费下限
    'cost_up': ('cost_up', 'int'),          # 雇佣花费上限
}


# 战队技能碎片副本配置
team_skill_fuben = {
    'uk': ('id', 'int'),                            # 副本id(难度)
    'lvl_limit': ('lvl_limit', 'int'),              # 解锁等级
    'chapter_id1': ('chapter_id1', 'int'),          # 第一关怪
    'force1': ('force1', 'int'),                    # 战力
    'side_set1': ('side_set1', 'int_list'),         # 第一关锁定位置
    'chapter_id2': ('chapter_id2', 'int'),          # 第二关怪
    'force2': ('force2', 'int'),                    # 战力
    'side_set2': ('side_set2', 'int_list'),         # 第二关锁定位置
    'reward_show': ('reward_show', 'list_3'),       # 奖励展示/当前掉落展示
    'reward_base': ('reward_base', 'int_list'),     # 随机奖励库
    'first_reward': ('first_reward', 'list_3'),     # 首次必得
    'reward': ('reward', 'list_3'),                 # 固定奖励
    'extra_reward': ('extra_reward', 'list_3'),     # vip3以上额外固定奖励
    'random': (('random_reward1', 'random_num1'), ('', 'chapter_stage')),  # 随机奖励库
}


# team_skill_reward_set = {
#     'uk': ('id', 'int'),        # 奖励id
#     'reward': ('reward', 'list_4'),     # 基因奖励
#     'reward_num': ('reward_num', 'int'),    # 随机数量
# }


team_skill_cost = {
    'uk': ('times_id', 'int'),                      # 挑战次数
    'cost': ('cost', 'list_3'),                        # 挑战花费
    'strength_rate': ('strength_rate', 'float'),      # 怪物实力加成
}


team_skill_milestone = {
    'uk': ('id', 'int'),                 # id
    'times': ('times', 'int'),           # 挑战花费
    'reward': ('reward', 'list_3'),      # 宝箱奖励
}


# 觉醒副本配置
awaken_chapter = {
    'uk': ('id', 'int'),                            # 编号
    'lv_unlocked': ('lv_unlocked', 'int'),          # 开启等级
    'player_lvl': ('player_lvl', 'int'),          # 玩家等级限制
    'name': ('name', 'unicode'),                    # 名字
    'picture': ('picture', 'str'),                  # 背景图
    'hard': ('hard', 'int'),                        # 难度
    'sort': ('sort', 'int'),                        # 类型
    'picture_boss': ('picture_boss', 'str'),    # 类型
    'first_reward': ('first_reward', 'list_3'),     # 首次奖励
    # 'chapter_id': (('chapter_id1', 'chapter_id2', 'chapter_id3',), ('int_list', 'mult_dict_1')),    # 多波怪关卡id
    'reward_show': ('reward_show', 'list_3'),       # 奖励展示
    # 'hero_exp': ('hero_exp', 'int'),                # 英雄经验
    # 'reward': ('reward', 'list_3'),                 # 固定奖励
    # 'failed_rate': ('failed_rate', 'float'),          # 失败随机奖励系数
    # 'random': (('random_reward1', 'random_num1',
    #             'random_reward2', 'random_num2',
    #             'random_reward3', 'random_num3',
    #             'random_reward4', 'random_num4'), ('', 'chapter_stage')),  # 随机奖励库
}


awaken_chapter_cost = {
    'uk': ('times_id', 'int'),                      # 挑战次数
    'cost': ('cost', 'list_3'),                        # 挑战花费
    'strength_rate': ('strength_rate', 'int'),      # 怪物实力加成
}


awaken_chapter_milestone = {
    'uk': ('id', 'int'),                 # id
    'times': ('times', 'int'),           # 挑战花费
    'reward': ('reward', 'list_3'),      # 宝箱奖励
}


# 觉醒副本配置
awaken_group = {
    'uk': ('id', 'int'),                            # 编号
    'hero_id': ('hero_id', 'int_list'),             # 可用阵营
    'debuff': ('debuff', 'int'),                    # debuff
}


awaken_history = {
    'uk': ('id', 'int'),                 # id
    'times_id': ('times_id', 'int'),           # 挑战花费
    'history_reward': ('history_reward', 'list_3'),      # 宝箱奖励
}
