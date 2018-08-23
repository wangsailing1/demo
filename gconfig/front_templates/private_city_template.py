#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 自己关卡模块
from gconfig import check


# 章节
chapter = {
    'uk': ('chapter_id', 'int'),  # 章节ID
    'chapter_name': ('chapter_name', 'unicode'),  # 章节名
    'resource': ('resource', 'str'),  # 背景图
    'building': ('building', 'unicode'),    # 标准建筑
    'banner': ('banner', 'str'),    # 横幅
    'music': ('music', 'str'),      # 背景音乐
    'stage': (('stage_id1', 'stage_id2', 'stage_id3', 'stage_id4', 'stage_id5',
               'stage_id6', 'stage_id7', 'stage_id8', 'stage_id9', 'stage_id10',), ('int', 'mult_list')),  # 关卡组
    'dungeon': (('dungeon1', 'dungeon2', 'dungeon3'), ('int', 'mult_list')),  # 地城
    'fight_reward': (('fight_reward1', 'fight_reward2', 'fight_reward3'), ('list_3', 'mult_dict_1')),  # 星级奖励
    'star_num': (('star_num1', 'star_num2', 'star_num3'), ('int', 'mult_dict_1')),                     # 奖励需要的星数
    'difficulty_star_reward': ('difficulty_star_reward', 'list_3'),     # 困难星级奖励
    'hell_star_reward': ('hell_star_reward', 'list_3'),                 # 地狱星级奖励
    'difficulty_star_num': ('difficulty_star_num', 'int'),              # 困难星级数
    'hell_star_num': ('hell_star_num', 'int'),                          # 地狱星级数

    'chapter_clear_time': (('chapter_clear_time1', 'chapter_clear_time2', 'chapter_clear_time3'),
                           ('int', 'mult_dict_1')),  # 50% 70% 100%探索所需时间
    'chapter_clear_reward': (('chapter_clear_reward1', 'chapter_clear_reward2', 'chapter_clear_reward3'),
                             ('list_3', 'mult_dict_1')),  # 50% 70% 100%探索奖励

    'dungeon_clear_reward': (('dungeon_clear_reward1', 'dungeon_clear_reward2', 'dungeon_clear_reward3'),
                             ('list_3', 'mult_dict_1')),  # 地城全通奖励
    'explore_lv': ('explore_lv', 'int'),  # 探险最低等级
    'explore_time': ('explore_time', 'int'),  # 探险周期
    'explore_exp': ('explore_exp', 'int'),  # 单个英雄探险单位时间获取的经验, 1分钟
    'explore_reward': ('explore_reward', 'list_4'),  # 探险随机奖励库
    'fix_reward': ('fix_reward', 'list_3'),  # 挂机固定可得
    'explore_num': ('explore_num', 'int'),  # 最大探索上限
    'story_title': ('story_title', 'int'),  # 下章节内容标题
    'story': ('story', 'int'),              # 下章节内容
    'icon': ('icon', 'str'),                # 挂机icon
    'map': ('map', 'str'),                # 关卡选择地图
    'chapter': ('chapter', 'str'),        # 章节选择地图
    'speed_1': ('speed_1', 'float'),        # 普通难度每一章的敌方单位速度增加量
    'speed_2': ('speed_2', 'float'),        # 困难难度每一章的敌方单位速度增加量
    'speed_3': ('speed_3', 'float'),        # 地狱难度每一章的敌方单位速度增加量
    'chapter_title': ('chapter_title', 'unicode'),
    'map_bg': ('map_bg', 'str'),    # 关卡背景
    'map_bgwg': ('map_bgwg', 'str'),    # 背景网格
    'map_bgdz': ('map_bgdz', 'str'),
    'fate_chest': ('fate_chest', 'list_3'),
}


# 章节对应关卡组
chapter_to_stage = {
    'uk': ('stage_id', 'int'),  # 关卡ID
    'stage_num': ('stage_num', 'str'),  # 几章几关
    'stage_name': ('stage_name', 'unicode'),  # 关卡名
    'story': ('story', 'unicode'),  # 描述
    'stage_sort': ('stage_sort', 'int'),    # 关卡类型
    'easy': ('easy', 'int'),    # 简单ID
    'hard': ('hard', 'int'),    # 困难ID
    'hell': ('hell', 'int'),    # 地狱ID
    'resource': ('resource', 'str'),  # 关卡图
}


# 关卡
chapter_stage = {
    'uk': ('stage_id', 'int'),  # 关卡ID
    'lv_unlocked': ('lv_unlocked', 'int'),
    'power': ('power', 'int'),  # 推荐战斗力
    'fight_exp': ('fight_exp', 'int'),  # 战斗经验
    'fight_reward': ('fight_reward', 'list_3'),  # 战斗奖励库
    'random': (('random_reward', 'random_num',
                'random_reward1', 'random_num1',
                'random_reward2', 'random_num2',
                'random_reward3', 'random_num3',
                'random_reward4', 'random_num4',
                'random_reward5', 'random_num5',
                'random_reward6', 'random_num6',
                'random_reward7', 'random_num7',
                'random_reward8', 'random_num8'), ('', 'chapter_stage')),  # 随机奖励库
    'stage_enemy': ('stage_enemy', 'int_list'),  # 展示敌人
    'stage_boss': ('stage_boss', 'int_list'),  # 关卡BOSS
    'chapter_star': ('chapter_star', 'int_list'),     # 星级条件, 对应星级表chapter_star
    'chapter_lose': ('chapter_lose', 'int_list'),     # 失败条件, 对应星级表chapter_lose
    'win_time': ('win_time', 'int_list'),           # 胜利条件
    'first_reward': ('first_reward', 'list_3'),     # 首次奖励
    'free_item': ('free_item', 'list_3'),           # 赠送战斗道具卡组
    # 'draught1': ('draught1', 'list_3'),                # 扫荡一次获得药水
    # 'draught2': ('draught2', 'list_3'),                # 扫荡十次获得药水
    'start_cost': ('start_cost', 'int'),            # 进入前扣除体力
    'end_cost': ('end_cost', 'int'),                # 结算时扣除体力
    'player_exp': ('player_exp', 'int'),            # 战队经验
    'chapter_enemy': ('chapter_enemy', 'int_list'),  # 怪物阵容id
    'show_reward': ('show_reward', 'list_3'),  # 奖励展示
    'rank_limit_grade': ('rank_limit_grade', 'int'),  # 排名限制等级
    'show_reward_2': ('show_reward_2', 'list_3'),  # 奖励展示(二)
    'first_mission_reward': ('first_mission_reward', 'list_3'),  # 主线任务奖励
    'challenge_limit': ('challenge_limit', 'int'),  # 普通副本挑战次数限制
    'stage_pic': ('stage_pic', 'str'),  # 普通副本挑战次数限制
    'stage_picbig': ('stage_picbig', 'int'),    # 是不是放大图
}


# 星级评定
chapter_star = {
    'uk': ('id', 'int'),
    'sort': ('sort', 'int'),      # 评星类型
    'value': ('value', 'int'),    # 评星条件
    'star_num': ('star_num', 'int'),    # 得星
    'story': ('story', 'unicode'),          # 描述
}


# 失败条件
chapter_lose = {
    'uk': ('id', 'int'),
    'sort': ('sort', 'int'),      # 评星类型
    'value': ('value', 'int'),    # 评星条件
    'story': ('story', 'unicode'),          # 描述
}


# 小怪基础数据表
enemy_basis = {
    'uk': ('hero_id', 'int'),                   # id
    'name': ('name', 'unicode'),                # 英雄名字
    'job': ('job', 'int'),                      # 职业定义
    'camp': ('camp', 'int'),                    # 阵营
    'crace': ('crace', 'int'),                  # 种族
    'gender': ('gender', 'int'),                # 性别
    'icon': ('icon', 'str'),                    # 头像
    'icon1': ('icon1', 'str'),                    # 头像
    'icon_fight': ('icon_fight', 'str'),        # 战斗用头像
    'art': ('art', 'str'),                      # 动画
    'act': ('act', 'str'),                      # 动画
    'grade': ('grade', 'int'),                  # 档次,类型, 1: D 2: C 3: B 4: A 5: S 6: SS 7: SSS
    'skin': ('skin', 'str'),                    # 皮肤
    'init_star': ('init_star', 'int'),          # 初始星级
    'skill': (('skill1_id', 'skill2_id', 'skill3_id', 'skill4_id'), ('int', 'mult_dict_1')),  # 技能
    'hp': ('hp', 'float'),                        # 生命
    'phy_atk': ('phy_atk', 'float'),              # 攻击
    'phy_def': ('phy_def', 'float'),              # 防御
    'mag_atk': ('mag_atk', 'float'),              # 攻击
    'mag_def': ('mag_def', 'float'),              # 防御
    'speed': ('speed', 'float'),                  # 速度
    'crit_chance': ('crit_chance', 'int'),      # 暴击(%)
    'crit_atk': ('crit_atk', 'int'),            # 暴击伤害(%)
    'hit': ('hit', 'int'),                      # 效果命中(%)
    'resistance': ('resistance', 'int'),        # 效果抵抗(%)
    # 'star_rate': (('star1', 'star2', 'star3', 'star4', 'star5'), ('float', 'mult_dict_1')),  # 星级成长倍率
    'story': ('story', 'unicode'),              # 描述
    'job_sort': ('job_sort', 'int'),            # 英雄定位
    'phy_or_mag': ('phy_or_mag', 'int'),        # 物理or魔法
    'elite': ('elite', 'int'),                  # 精英
    'logic': ('logic', 'str'),                  # AI
    'immunity': ('immunity', 'int'),
    'herobase_id': ('herobase_id', 'int'),
}


# # boss基础数据表
# boss = {
#     'uk': ('boss_id', 'int'),                   # id
#     'name': ('name', 'unicode'),                # 英雄名字
#     'job': ('job', 'int'),                      # 职业定义
#     'icon': ('icon', 'str'),                    # 头像
#     'act': ('act', 'str'),                      # 动画
#     'grade': ('grade', 'int'),                  # 档次,类型, 1: D 2: C 3: B 4: A 5: S 6: SS 7: SSS
#     'special_effects_atk': ('special_effects_atk', 'str'),   # 发球动画
#     'atk_ready_time': ('atk_ready_time', 'int_or_float_list'),      # 掉血延迟
#     'special_effects_atk_hero2': ('special_effects_atk_hero2', 'str'),   # 动画特效
#     'init_star': ('init_star', 'int'),          # 初始星级
#     'phormg': ('phormg', 'int'),                # 伤害类型
#     'search': ('search', 'int'),                # 感知范围
#     'collision': ('collision', 'int'),          # 碰撞范围
#     'range': ('range', 'float'),                # 攻击距离
#     'speed': ('speed', 'int'),                  # 初始移动/单位时间1s移动距离
#     'atkspeed': ('atkspeed', 'float'),          # 初始攻速/单位时间攻击次数
#     'crit_atk': ('crit_atk', 'int'),            # 初始暴击
#     'crit_def': ('crit_def', 'int'),            # 初始抗暴
#     'dodge': ('dodge', 'int'),                  # 初始闪避
#     'hit': ('hit', 'int'),                      # 初始命中
#     'suck': ('suck', 'int'),                    # 初始吸血
#     'skill': (('skill1_id', 'skill2_id', 'skill3_id', 'skill4_id'), ('int', 'mult_dict_1')),  # 技能
#     'grow': ((('hp_grow', 'hp'),
#               ('phy_atk_grow', 'phy_atk'),
#               ('phy_def_grow', 'phy_def'),
#               ('mag_atk_grow', 'mag_atk'),
#               ('mag_def_grow', 'mag_def')), ('float', 'mult_key_dict')),  # 成长
#     'star_rate': (('star2', 'star3', 'star4', 'star5'), ('float', 'mult_dict_2')),  # 星级成长倍率
#     'description': ('description', 'unicode'),  # 怪物描述
# }


# 羁绊故事大章节
chain_story = {
    'uk': ('id', 'int'),                                # 大章节id
    'name': ('name', 'unicode'),                        # 大章节名
    'need_hero': ('need_hero', 'int_list'),             # 开启章节所需英雄
    'story_content': ('story_content', 'int_list'),     # 包含小章节
    'description1': ('description1', 'unicode'),        # 关系描述1
    'description2': ('description2', 'unicode'),        # 关系描述2
    'description3': ('description3', 'unicode'),        # 关系描述3
    'description4': ('description4', 'unicode'),        # 关系描述4
    'image': ('image', 'str'),                          # 封面模板
}


# 羁绊故事小章节
chain_story_content = {
    'uk': ('id', 'int'),                        # 章节id
    'name': ('name', 'unicode'),                # 章节名
    'loot': ('loot', 'list_3'),                 # 首次通关可得
    'content': ('content', 'str'),              # 章节脚本
    'image': ('image', 'str'),                  # 背景图片
}


# 关卡怪物配置表
chapter_enemy = {
    'uk': ('id', 'int'),
    'sort': ('sort', 'int'),
    'hero_id': ('hero_id', 'int'),
    'boss_place': ('boss_place', 'int'),    # 几号位是boss
    'enemy': ((('enemy1_id', 'id'), ('enemy1_lv', 'lv'), ('enemy1_star', 'star'), ('enemy1_grade', 'grade'), ('enemy1_evo', 'evo'), ('skill1_power', 'skill_power'),
               ('enemy2_id', 'id'), ('enemy2_lv', 'lv'), ('enemy2_star', 'star'), ('enemy2_grade', 'grade'), ('enemy2_evo', 'evo'), ('skill2_power', 'skill_power'),
               ('enemy3_id', 'id'), ('enemy3_lv', 'lv'), ('enemy3_star', 'star'), ('enemy3_grade', 'grade'), ('enemy3_evo', 'evo'), ('skill3_power', 'skill_power'),
               ('enemy4_id', 'id'), ('enemy4_lv', 'lv'), ('enemy4_star', 'star'), ('enemy4_grade', 'grade'), ('enemy4_evo', 'evo'), ('skill4_power', 'skill_power'),
               ('enemy5_id', 'id'), ('enemy5_lv', 'lv'), ('enemy5_star', 'star'), ('enemy5_grade', 'grade'), ('enemy5_evo', 'evo'), ('skill5_power', 'skill_power'),),
              ('int', 'chapter_enemy'))
}


# 其他副本怪物配置
activity_enemy = chapter_enemy


# # 副本邮件
# chapter_single_mail = {
#     'uk': ('day', 'str'),               # 日期
#     'chapter': ('chapter', 'int'),      # 章节
#     'time': ('time', 'int'),            # 次数
#     'name': ('name', 'unicode'),        # 邮件标题
#     'des': ('des', 'unicode'),          # 邮件内容
#     'reward': ('reward', 'list_3'),     # 邮件奖励
# }
#
#
# chapter_double_mail = {
# 'uk': ('day', 'str'),                   # 日期
#     'chapter': ('chapter', 'int_list'), # 章节
#     'name': ('name', 'unicode'),        # 邮件标题
#     'des': ('des', 'unicode'),          # 邮件内容
#     'reward': ('reward', 'list_3'),     # 邮件奖励
# }


battle_story = {
    'uk': ('id', 'int'),
    'section_id': ('section_id', 'str'),
    'trigger_pos': ('trigger_pos', 'str'),
    'action_type': ('action_type', 'str'),
    'param': (('param1', 'param2', 'param3', 'param4', 'param5', 'param6', 'param7', 'param8', 'param9', 'param10',
               'param11', 'param12', 'param13', 'param14', 'param15', 'param16', 'param17', 'param18', 'param19', 'param20'),
              ('battle_story_param', 'mult_list1')),
}
