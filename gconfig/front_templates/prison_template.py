#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check


# 监狱主表
prison_main = {
    'uk': ('prisonId', 'int'),                              # 牢房id
    'prisonName': ('prisonName', 'unicode'),                # 牢房名
    'prisonOpen': ('prisonOpen', 'int'),                    # 开启条件
    'wanted': ('wanted', 'str'),                            # 悬赏图
    'wantedRewards': ('wantedRewards', 'list_3'),           # 悬赏奖励
    'prisoner': ('prisoner', 'int'),                        # 对应恶棍id
    'treasureId': ('treasureId', 'int'),                    # 对应宝藏
    'artifactId': ('artifactId', 'int'),                    # 对应神器
    'temptId': ('temptId', 'int'),                          # 对应诱惑道具
    'whip_rewards': ('whip_rewards', 'str'),           # 皮鞭奖励
    'tempt_rewards': ('tempt_rewards', 'str'),         # 诱惑奖励
    'wordsId1': ('wordsId1', 'int'),                        # 皮鞭文字库
    'wordsId2': ('wordsId2', 'int'),                        # 诱惑文字库
    'ArtifactGradeExp1': ('ArtifactGradeExp1', 'int'),      # 皮鞭神器经验
    'ArtifactGradeExp2': ('ArtifactGradeExp2', 'int'),      # 诱惑神器经验
    'treasureGradeExp1': ('treasureGradeExp1', 'int'),      # 皮鞭宝藏经验
    'treasureGradeExp2': ('treasureGradeExp2', 'int'),      # 诱惑宝藏经验
    'breakGradeExp': ('breakGradeExp', 'int'),              # 暴动值
    'offset': ('offset', 'int_list'),
}


# 监狱神器表
prison_artifact = {
    'uk': ('artifactId', 'int'),                             # 神器id
    'artifactName': ('artifactName', 'unicode'),             # 神器名
    'artifactDescribe': ('artifactDescribe', 'unicode'),     # 神器描述
    'artifactPicture': ('artifactPicture', 'str'),           # 神器图标
    'useItem': ('useItem', 'int_list'),                       # 升级道具
    'unlockItem': ('unlockItem', 'list_3'),                 # 解锁道具
}


# 监狱神器升级表
prison_artifact_upgrade = {
    'uk': ('ArtifactGrade', 'int'),                         # 神器等级
    'ArtifactGradeExp': ('ArtifactGradeExp', 'int'),          # 升级经验
    'Artifact': (('Artifact1', 'Artifact2', 'Artifact3', 'Artifact4', 'Artifact5',
                  'Artifact6', 'Artifact7', 'Artifact8', 'Artifact9', 'Artifact10'), ('list_2', 'mult_dict_1')),  # 神器n
    'Artifactupgrade': (('Artifactupgrade1', 'Artifactupgrade2', 'Artifactupgrade3', 'Artifactupgrade4', 'Artifactupgrade5',
                'Artifactupgrade6', 'Artifactupgrade7', 'Artifactupgrade8', 'Artifactupgrade9', 'Artifactupgrade10'), ('list_3', 'mult_dict_1')),  # 神器n
}


# 监狱宝藏表
prison_treasure = {
    'uk': ('treasureId', 'int'),
    'treasureName': ('treasureName', 'unicode'),
    'describe': ('describe', 'unicode'),
}


# 监狱宝藏升级表
prison_treasure_upgrade = {
    'uk': ('treasureGrade', 'int'),                         # 宝藏等级
    'treasureExp': ('treasureExp', 'int'),                  # 宝藏经验
    'treasure': (('treasure1', 'treasure2', 'treasure3', 'treasure4', 'treasure5',
                  'treasure6', 'treasure7', 'treasure8', 'treasure9', 'treasure10',), ('list_3', 'mult_dict_1')),  # 奖励
}


# 暴动表
prison_break = {
    'uk': ('ID', 'int'),                            # id
    'chapter': ('chapter', 'int'),               # 玩家等级范围
    'breakGrade': ('breakGrade', 'int'),            # 任务难度
    'breakExp': ('breakExp', 'int'),                # 暴动经验
    'enemy': ('enemy', 'list_2'),                 # 阵容
    'break_Rewards': ('break_Rewards', 'list_3'),   # 暴动奖励
}


# 监狱说话表
prison_words = {
    'uk': ('wordsId', 'int'),
    'Word': (('Word1', 'Word2', 'Word3', 'Word4', 'Word5',
              'Word6', 'Word7', 'Word8', 'Word9', 'Word10',), ('unicode', 'mult_dict_1')),
}

# 物品随机掉落表
random_drop = {
    'uk': ('id', 'int'),                            # id
    'award1': ('award1', 'list_3'),                 # 低级奖励
    'weight1': ('weight1', 'int'),                  # 低级权重
    'award2': ('award2', 'list_3'),                 # 高级奖励
    'weight2': ('weight2', 'int'),                  # 高级权重
    'grade': ('grade', 'int'),                      # 解锁等级
}


# 神器里程碑
prison_artifact_milestone = {
    'uk': ('id', 'int'),
    'add_str': ('add_str', 'list_2'),
    'artifact_lv': ('artifact_lv', 'int'),
}
