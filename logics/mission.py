# coding: utf-8

import time
import datetime
from gconfig import game_config



############### 任务是否完成判断函数定义 返回flag, value, need #################
#1 玩家等级
def target_sort1(mm,reward_obj,target_data,target_data1,award_id):

    target_value = target_data[0]
    value = mm.user.level
    return value >= target_value,value,target_value

#任意卡牌达到等级
def target_sort2(mm,reward_obj,target_data,target_data1,award_id):
    target_value = target_data
    value = [v['lv'] for v in mm.card.cards.values()]
    num = 0
    for i in value:
        if i >= target_value[0]:
            num += 1
    return  num >= target_value[1],num,target_value[1]

#抽取艺人
def target_sort3(mm,reward_obj,target_data,target_data1,award_id):
    target_value = target_data[1]
    value = reward_obj.get_count(award_id)
    return value >= target_value,value,target_value

#抽取剧本
def target_sort4(mm,reward_obj,target_data,target_data1,award_id):
    target_value = target_data[1]
    value = reward_obj.get_count(award_id)
    return value >= target_value,value,target_value


