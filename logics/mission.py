# coding: utf-8

import time
import datetime
from gconfig import game_config

############### 任务是否完成判断函数定义 返回flag, value, need #################

GETNUMSORT = [3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


# 1 玩家等级
def target_sort1(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[0]
    value = mm.user.level
    return value >= target_value, value, target_value


# 任意卡牌达到等级
def target_sort2(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data
    num = len(reward_obj.get_count(mission_id))
    return num >= target_value[1], num, target_value[1]


# 直接取数值判断
def target_sort_num(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[1]
    value = reward_obj.get_count(mission_id)
    return value >= target_value, value, target_value


# 票房
def target_sort5(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[1]
    value = reward_obj.get_count(mission_id)
    return value >= target_value, value, target_value

class Mission(object):

    def __init__(self,mm):
        self.mm = mm
        self.mission = mm.mission

    def has_reward_daily(self):
        reward_obj = self.mission.daily
        for mission_id,value in self.mission.daily.iteritems():
            config = game_config.liveness
            status = self.get_status(reward_obj, mission_id, config)

    def get_status(self):
        pass

