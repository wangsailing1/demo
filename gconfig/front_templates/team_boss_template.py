#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'


# 组队boss-组队玩法
team_boss = {
    'uk': ('id', 'int'),                            # 关卡id
    'name': ('name', 'unicode'),                    # 名称
    'des': ('des', 'unicode'),                      # 描述
    'skill_name': ('skill_name', 'unicode'),        # 技能名字
    'skill_des': ('skill_des', 'unicode'),          # 技能描述
    'sort': ('sort', 'int'),                        # 类型
    'unlock_lvl': ('unlock_lvl', 'int_list'),       # 难度解锁等级
    'lvl': ('lvl', 'int'),                          # 关卡难度等级
    'team_lvl': ('team_lvl', 'int'),                # 队伍等级
    'team_evo': ('team_evo', 'int'),                # 队伍品阶
    'team_star': ('team_star', 'int'),              # 队伍星级
    'enemy': ('enemy', 'int_list'),                 # 怪物阵容
    'cost': ('cost', 'int'),                        # 单人体力消耗
    'team_cost': ('team_cost', 'int'),              # 2人组队体力消耗
    'team_cost2': ('team_cost2', 'int'),            # 3人组队体力消耗
    'reward': ('reward', 'list_4'),                 # 随机奖励
    'hero_reward': (('hero5_reward', 'hero1_reward', 'hero2_reward', 'hero3_reward'),
                    ('list_2', 'mult_dict_0')),     # 单人挑战奖励, 组队挑战上1-3人奖励
}
