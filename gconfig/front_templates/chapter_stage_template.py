# -*- coding: utf-8 –*-


chapter_stage = {
    'uk': ('stage_id', 'int'),  # id
    'script_id': ('script_id', 'int'),  # 关卡剧本id
    'fans_activity': ('fans_activity', 'int'),  # 解锁的粉丝活动id
    'show_reward': ('show_reward', 'int_list'),  # 显示用奖励
    'player_exp': ('player_exp', 'int'),  # 公司经验
    'fight_exp': ('fight_exp', 'int'),  # 类型经验
    'fight_reward': ('fight_reward', 'int_list'),  # 战斗奖励金币
    'first_reward': ('first_reward', 'int_list'),  # 首次奖励
    'random_reward1': ('random_reward1', 'int_list'),  # 艺人合同奖励
    'random_num1': ('random_num1', 'int'),  # 合同奖励数量1
    'random_reward2': ('random_reward2', 'int_list'),  # 随机奖励库2
    'random_num2': ('random_num2', 'int'),  # 随机奖励数量2
    'random_reward3': ('random_reward3', 'int_list'),  # 随机奖励库3
    'random_num3': ('random_num3', 'int'),  # 随机奖励数量3
    'chapter_enemy': ('chapter_enemy', 'int_list'),  # 关卡预约艺人【剧本角色role_id,怪物npc_id】
    'challenge_limit': ('challenge_limit', 'int'),  # 每日限制次数
    'lv_unlocked': ('lv_unlocked', 'int'),  # 等级限制
    'start_cost': ('start_cost', 'int'),  # 进入前扣除体力
    'end_cost': ('end_cost', 'int'),  # 结算时扣除体力
    'type': ('type', 'int'),  # 关卡表现类型
    'name': ('name', 'str'),  # 关卡名
    'story': ('story', 'str'),  # 关卡描述
    'background': ('background', 'str'),  # 背景图
    'card_need': ('card_need', 'int_list'),  # 艺人要求
    'music': ('music', 'str'),  # 拍摄音乐
    'name1': ('name1', 'str'),  # 角色名
    'dialog1': ('dialog1', 'str'),  # 角色台词
    'name2': ('name2', 'str'),  # 角色名
    'dialog2': ('dialog2', 'str'),  # 角色台词
    'icon': ('icon', 'str'),  # 剧本图标
    'tag': ('tag', 'str'),  # 标签


}

chapter = {
    'uk': ('chapter_id', 'int'),  # id
    'chapter_name': ('chapter_name', 'int'),  # 章节名
    'next_chapter': ('next_chapter', 'int_list'),  # 解锁章节
    'num': ('num', 'int'),  # 章节序号
    'hard_type': ('hard_type', 'int'),  # 难度类型0=普通 1=精英
    'background': ('background', 'str'),  # 关卡地图背景
    'music': ('music', 'int'),  # 地图背景音乐
    'script_end_level': ('script_end_level', 'int'),  # 几星扫荡
    'stage_id': (('stage_id1', 'stage_id2', 'stage_id3', 'stage_id4', 'stage_id5',
                  'stage_id6', 'stage_id7', 'stage_id8', 'stage_id9', 'stage_id10', 'stage_id11', 'stage_id12',
                  ), ('int', 'mult_force_num_list')),
    # 关卡
    'dialogue_id': (('dialogue_id1', 'dialogue_id2', 'dialogue_id3', 'dialogue_id4', 'dialogue_id5',
                     'dialogue_id6', 'dialogue_id7', 'dialogue_id8', 'dialogue_id9', 'dialogue_id10', 'dialogue_id11',
                     'dialogue_id12'), ('int', 'mult_force_num_list')),
    # 剧情关卡
    'fight_reward1': ('fight_reward1', 'int_list'),  # 星级奖励1
    'star_num1': ('star_num1', 'int'),  # 奖励1需求星数
    'fight_reward2': ('fight_reward2', 'int_list'),  # 星级奖励2
    'star_num2': ('star_num2', 'int'),  # 奖励2需求星数
    'fight_reward3': ('fight_reward3', 'int_list'),  # 星级奖励3
    'star_num3': ('star_num3', 'int'),  # 奖励3需求星数
    'chapter_icon': ('chapter_icon', 'str'),  # 章节图标
    'preincome': ('preincome', 'int'),  # 章节进入前提-最高票房
    'prelv': ('prelv', 'int'),  # 章节进入前提-等级

}

chapter_enemy = {
    'uk': ('id', 'int'),  # id
    'card_id': ('card_id', 'int'),  # 对应卡牌id
    'charpro': (('charpro1', 'charpro2', 'charpro3', 'charpro4', 'charpro5',
                 'charpro6'), ('int', 'mult_force_num_list')),  # 演技，歌艺，气质，动感，娱乐，艺术
    'dps_rate': ('dps_rate', 'int_list'),  # 伤害输出系数区间值（万分之）
    'ex_special_rate': ('ex_special_rate', 'int'),  # 额外触发概率( 万分比）
    'special_quality': ('special_quality', 'int_list'),  # 艺术/娱乐触发权重
    'crit_rate_base': ('crit_rate_base', 'int'),  # 基础暴击率(万分之)

}
