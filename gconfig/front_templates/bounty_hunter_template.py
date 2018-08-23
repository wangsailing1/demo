#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'


# 末日狩猎-组队玩法
doomsday_hunt_main = {
    'uk': ('sort', 'int'),                      # 类型
    'name': ('name', 'unicode'),                # 名字
    'boss_image': ('boss_image', 'str'),        # 图标
    'open_time': ('open_time', 'int_list'),     # 开启时间
    'boss_act': ('boss_act', 'unicode'),        # 动画
    'chapter': ('chapter', 'int_list'),       # 对应副本id
    # 'chapter': ('chapter', 'int_list'),       # 对应副本id
    'reward_show': ('reward_show', 'list_3'),   # 展示奖励
}
doomsday_hunt = {
    'uk': ('id', 'int'),                            # id
    'hard': ('hard', 'int'),                        # 难度
    'sort': ('sort', 'int'),                        # 类型
    # 'unlock_limit': ('unlock_limit', 'int_list'),   # 解锁限制
    'chapterid': ('chapterid', 'int_list'),         # 关卡id
    'first_reward': ('first_reward', 'list_4'),     # 首次奖励
    'reward': ('reward', 'list_3'),                 # 固定奖励
    'reward_base': ('reward_base', 'list_4'),     # 随机奖励
    'random': (('random_reward1', 'random_num1'), ('', 'chapter_stage')),  # 随机奖励库
    'goldin': ('goldin', 'list_3'),                 # 固定奖励
    'goldout': ('goldout', 'list_3'),                 # 固定奖励
    'boss_num_weight': ('boss_num_weight', 'int_list'),         # 根据BOSS数量决定装备掉落权重
    'color_weight': ('color_weight', 'int_list'),               # evo权重
    'star_weight': ('star_weight', 'int_list'),                 # star权重
    'reward_show': ('reward_show', 'list_4'),       # 奖励展示
}

# reward_set = {
#     'uk': ('id', 'int'),        # 奖励id
#     'reward': ('reward', 'list_5'),     # 基因奖励
#     'reward_num': ('reward_num', 'int'),    # 随机数量
# }


# 赏金猎人-克隆人
clone = {
    'uk': ('id', 'int'),                        # 难度
    'unlock_type': ('unlock_type', 'int'),      # 解锁类型
    'unlock_limit': ('unlock_limit', 'int'),    # 解锁限制
    # 'enemy_lvl': ('enemy_lvl', 'int'),          # 怪物等级
    # 'reward_rate': ('reward_rate', 'int_list'),      # 灵魂石奖励权重系数加成%
    'reward': ('reward', 'list_3'),             # 固定奖励
    # 'random': (('random_reward1', 'random_num1'), ('', 'chapter_stage')),  # 随机奖励库
}
clone_bank = {
    'uk': ('id', 'int'),                        # 副本id
    'hero_id': ('hero_id', 'int'),              # 英雄id
    'grade': ('grade', 'int'),                  # 英雄资质
    'chapter_id': ('chapter_id', 'int_list'),   # 怪物阵容
    'hero_stone': ('hero_stone', 'list_3'),     # 固定灵魂石
    # 'random_hero_stone': ('random_hero_stone', 'list_4'),   # 随机灵魂石
    # 'weight': ('weight', 'int'),                # 权重
    'image': ('image', 'str'),                  # 图标
    'xy': ('xy', 'int_list'),                   # 偏移值
}


# 猛兽通缉令地图
hunt_map = {
    'uk': ('id', 'int'),                                # id
    'level': ('level', 'int'),                          # 难度
    'map_name': ('map_name', 'unicode'),                # 地图名称
    # 'map_des': ('map_des', 'unicode'),                  # 地图描述g
    'size': ('size', 'int_list'),                       # 地图边长
    # 'buffword': ('buffword', 'int_list'),               # 地图词缀池子
    # 'buffword_num': ('buffword_num', 'int_list'),            # 地图词缀数量
    'obstacle_num': ('obstacle_num', 'int_list'),            # 障碍物
    'boss_num': ('boss_num', 'int_list'),               # Boss数量
    'monster': ('monster', 'int_list'),                 # 小怪
    'monster_num': ('monster_num', 'int_list'),         # 小怪数量
    'bossmonster': ('bossmonster', 'int_list'),         # 乱入怪
    'bossmonster_num': ('bossmonster_num', 'int_list'), # 乱入怪数量
    'item1': ('item1', 'list_4'),                       # 物品池子
    'item1_num': ('item1_num', 'int_list'),             # 物品数量
    'item2': ('item2', 'list_4'),
    'item2_num': ('item2_num', 'int_list'),
    'item3': ('item3', 'list_4'),
    'item3_num': ('item3_num', 'int_list'),
    'item4': ('item4', 'list_4'),
    'item4_num': ('item4_num', 'int_list'),
    'item5': ('item5', 'list_4'),
    'item5_num': ('item5_num', 'int_list'),
    'item6': ('item6', 'list_4'),
    'item6_num': ('item6_num', 'int_list'),
    'item7': ('item7', 'list_4'),
    'item7_num': ('item7_num', 'int_list'),
    'left': ('left', 'str'),                            # 剩下的格子内容
    'left_num': ('left_num', 'float'),                  # 除此之外有多少是空格子
    'background_pic': ('background_pic', 'str'),        # 背景
    'capacity_min': ('capacity_min', 'int'),            # 占领最低战斗力
    'monster_reward': ('monster_reward', 'list_4'),     # 小怪奖励
    'monster_reward_num': ('monster_reward_num', 'int'),  # 小怪奖励数量
    'map_reward': ('map_reward', 'list_3'),  # 全清奖励
    'first_reward': ('first_reward', 'list_3'),         # 首通奖励
    'boss_pot': ('boss_pot', 'int_list'),           # boss池
    'sweep_reward': ('sweep_reward', 'list_3'),
    'sweep_extra': ('sweep_extra', 'list_3'),
}

# # 词缀属性
# bufword = {
#     'uk': ('id', 'int'),                    # id
#     'type': ('type', 'int'),                # 生效类型
#     'ispercent': ('ispercent', 'int'),      # 是否为成算
#     'value': ('value', 'float'),            # 效果值
#     'quality': ('quality', 'float'),        # 增加权重
# }
#
#
# # 词缀属性
# bufwordmap = {
#     'uk': ('id', 'int'),                            # id
#     'buffwordlist': ('buffwordlist', 'int_list'),   # 词缀效果
#     'nameid': ('nameid', 'unicode'),                # 名称
#     'desid': ('desid', 'unicode'),                  # 描述
#     'quality': ('quality', 'float'),                # 增加权重
# }
