#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time

# 检查配置项是否正确


REWARD_CHECK_MAPPING = {
    # sort:{'num':限制数量, 'msg': 返回信息}
    1: {'num': 999999, 'msg': 'coin'},                  # 银币大于999999
    2: {'num': 2888, 'msg': 'diamond'},                  # 钻石大于500
    3: {'num': 100, 'msg': 'item'},                     # 道具大于100
    # 4: {'num': 150, 'msg': 'soul stone'},               # 灵魂石大于150
    5: {'num': 50, 'msg': 'collection item'},           # 采集物大于50
    6: {'num': 50, 'msg': 'gene'},                      # 基因大于50
    # 7: {'num': 299, 'msg': 'evo item'},                 # 进阶材料大于299
    8: {'num': 999, 'msg': 'hero exp'},                 # 英雄经验大于999
    # 9: {'num': 9, 'msg': 'hero'},                       # 英雄大于9
    10: {'num': 99, 'msg': 'guild exp'},                # 公会经验大于99
    11: {'num': 99, 'msg': 'guild gift'},               # 公会礼物道具大于99
    12: {'num': 49, 'msg': 'awaken item'},              # 觉醒材料大于49
    13: {'num': 99, 'msg': 'gold coin'},                # 金币大于99
    14: {'num': 99, 'msg': 'production formula'},       # 生产配方大于99
    15: {'num': 99, 'msg': 'defense item'},             # 防守道具大于99
    16: {'num': 99, 'msg': 'quinter card'},             # 昆特牌大于99
    17: {'num': 99, 'msg': 'battle exp'},               # 战斗经验大于99
    18: {'num': 299, 'msg': 'challenge exp'},           # 挑战卡大于299
    19: {'num': 99, 'msg': 'energy'},                   # 能量, 战斗道具大于99
    20: {'num': 299, 'msg': 'power'},                   # 体力大于299
    21: {'num': 299, 'msg': 'dark street coin'},        # 黑街货币大于299
    22: {'num': 99, 'msg': 'battle skill fragment'},    # 战队技能碎片大于99
    23: {'num': 299, 'msg': 'guild coin'},              # 公会币大于299
    24: {'num': 99, 'msg': 'common plane ticket'},      # 普通飞机票大于99
    25: {'num': 99, 'msg': 'senior plane ticket'},      # 高级飞机票大于99
    26: {'num': 99, 'msg': 'special item'},             # 觉醒宝箱碎片大于99
    27: {'num': 299, 'msg': 'peak coin'},               # 巅峰币大于299
    28: {'num': 999, 'msg': 'vip exp'},                 # vip经验大于999
    29: {'num': 99, 'msg': 'awaken box fragment'},      # 觉醒宝箱碎片大于99
    30: {'num': 299, 'msg': 'honor coin'},              # 荣耀币大于299
    31: {'num': 49, 'msg': 'awaken box key'},           # 觉醒宝箱钥匙大于49
    106: {'num': 99, 'msg': 'equip'},                   # 通过装备属性增加装备大于99
}


def test():
    print 'hehe'


# 时间格式检查
def check_time(tformat="%Y-%m-%d %H:%M:%S"):
    def trans(x):
        message = None
        try:
            time.strptime(x, tformat)
        except:
            message = 'wrong time format!!!'

        return message

    return trans


# 检查数据列表格式
def check_int_list(num):
    def trans(x):
        message = None
        for reward in x:
            try:
                if len(reward) != num:
                    message = 'the format is wrong!!!'
                    return message
            except:
                message = 'the format is wrong!!!'
                return message
        return message

    return trans


# 检查数据列表格式
def check_int():
    def trans(x):
        message = None
        try:
            if not isinstance(x, float):
                message = 'the format is wrong!!!'
                return message
        except:
            message = 'the format is wrong!!!'
            return message
        return message

    return trans


# 检查数据条目是否为空
def check_empty():
    def trans(x):
        if x:
            return None
        return 'this column can\'t be empty.'

    return trans


# 检查数据小于等于num
def check_below(num):
    def trans(x):
        if x > num:
            return 'the number is too large.'
        return None

    return trans


# 检查奖励
def check_reward(lens=3, is_random=False):
    def trans(x):
        from gconfig import game_config
        message = None
        try:
            # 格式检查
            if not isinstance(x, list):
                message = 'the reward format is wrong!!!'
                return message
            for i in x:
                if not isinstance(i, list) or len(i) != lens:
                    message = 'the reward format is wrong!!!'
                    return message
                for j in i:
                    if not isinstance(j, int):
                        message = 'the reward format is wrong!!!'
                        return message
            # 奖励存在检查
            for reward in x:
                if is_random:
                    if len(reward) == lens:
                        sort, tid, ran, num = reward
                    else:
                        sort, tid, ran, num, lv = reward
                else:
                    if len(reward) == lens:
                        sort, tid, num = reward
                    else:
                        sort, tid, num, lv = reward
                sort = int(sort)

                if sort in (1, 2, 3, 4, 7, 11, 12, 13, 14, 18, 20, 21, 23, 24, 25, 27, 28, 29, 30):  # 货币挑战券之类
                    num = int(num)
                    if num <= 0:
                        message = 'wrong number of reward!!!'
                        return message
                elif sort == 5:  # 道具
                    num = int(num)
                    if num <= 0:
                        message = 'wrong number of reward!!!'
                        return message
                    tid = int(tid)
                    if tid not in game_config.use_item.keys():
                        message = 'No reward in config!!!'
                        return message
                #
                # elif sort == 4:  # 美元
                #     num = int(num)
                #     if num <= 0:
                #         message = 'wrong number of reward!!!'
                #         return message
                    # tid = int(tid)
                    # if tid not in game_config.hero_stone.keys():
                    #     message = 'No reward in config!!!'
                    #     return message
                # elif sort == 5:  # 采集物
                #     pass
                # elif sort == 6:  # 装备
                #     return False
                elif sort == 6:  # 装备
                    num = int(num)
                    if num <= 0:
                        message = 'wrong number of reward!!!'
                        return message
                    tid = int(tid)
                    if tid not in game_config.equip.keys():
                        message = 'No reward in config!!!'
                        return message

                # elif sort == 7:  # 进阶材料
                #     num = int(num)
                #     if num <= 0:
                #         message = 'wrong number of reward!!!'
                #         return message
                #     tid = int(tid)
                #     if tid not in game_config.grade_lvlup_item.keys():
                #         message = 'No reward in config!!!'
                #         return message
                # elif sort == 8:  # 增加英雄经验, 需要在调用地方单独加
                #     pass

                elif sort == 8:  # 艺人
                    num = int(num)
                    if num <= 0:
                        message = 'wrong number of reward!!!'
                        return message
                    tid = int(tid)
                    if tid not in game_config.card_basis.keys():
                        message = 'No reward in config!!!'
                        return message

                elif sort == 9:  # 艺人碎片
                    num = int(num)
                    if num <= 0:
                        message = 'wrong number of reward!!!'
                        return message
                    tid = int(tid)
                    if tid not in game_config.card_piece.keys():
                        message = 'No reward in config!!!'
                        return message
                elif sort == 10:  # 装备碎片
                    num = int(num)
                    if num <= 0:
                        message = 'wrong number of reward!!!'
                        return message
                    tid = int(tid)
                    if tid not in game_config.equip_piece.keys():
                        message = 'No reward in config!!!'
                        return message
                #
                # elif sort == 11:  # 公会礼物道具
                #     pass
                elif sort == 12:  # 觉醒材料
                    num = int(num)
                    if num <= 0:
                        message = 'wrong number of reward!!!'
                        return message
                    tid = int(tid)
                    if tid not in game_config.awaken_material.keys():
                        message = 'No reward in config!!!'
                        return message
                elif sort == 14:  # 生产配方
                    continue

                elif sort == 15:  # 防守道具
                    continue

                elif sort == 16:  # 昆特牌
                    message = 'error reward sort!!!'
                    return message

                elif sort == 17:  # 战斗经验
                    continue
                elif sort == 19:  # 能量, 战斗道具
                    continue
                elif sort == 22:  # 战队技能碎片
                    continue
                elif sort == 26:  # 特殊类道具
                    continue

                elif sort == 31:  # 觉醒宝箱钥匙
                    continue
                elif sort == 106:  # 通过装备属性增加装备
                    continue
                else:
                    message = 'No reward in config!!!'
                    return message
        except:
            message = 'the format is wrong!!!'
            return message
        return message
    return trans


# 检查奖励
def check_reward_counts(x):
    message = None
    # 奖励存在检查
    for reward in x:
        if len(reward) == 3:
            sort, tid, num = reward
        else:
            sort, tid, num, lv = reward
        sort = int(sort)
        num = int(num)
        if sort in REWARD_CHECK_MAPPING.keys():
            if num > REWARD_CHECK_MAPPING[sort]['num']:
                return 'the %s(sort is %s) nums out of range!!!' % (REWARD_CHECK_MAPPING[sort]['msg'], sort)
            else:
                return message
        else:
            return message
    return message
