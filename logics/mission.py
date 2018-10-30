# coding: utf-8

import time
import datetime
from gconfig import game_config

############### 任务是否完成判断函数定义 返回flag, value, need #################

GETNUMSORT = [3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


# 1 玩家等级
def target_sort1(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[1]
    value = mm.user.level
    return value >= target_value, value, target_value


# 任意卡牌达到等级
def target_sort2(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data
    num = len(reward_obj.get_count(mission_id)) if isinstance(reward_obj.get_count(mission_id),list) else 0
    return num >= target_value[1], num, target_value[1]


# 直接取数值判断
def target_sort_num(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[1]
    value = reward_obj.get_count(mission_id)
    return value >= target_value, value, target_value


# 票房
def target_sort5(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data1
    value = reward_obj.get_count(mission_id)
    return value >= target_value, value, target_value


class Mission(object):
    def __init__(self, mm):
        self.mm = mm
        self.mission = self.mm.mission

    def has_reward_by_type(self, type='daily', mission_id=''):
        mission_obj = getattr(self.mission, type)
        if mission_id:
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            if stats['status'] == 1:
                return 1
            return 0
        for mission_id, value in mission_obj.data.iteritems():
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            if stats['status'] == 1:
                return 1
        return 0

    def get_done_mission(self, type='daily', mission_id=''):
        mission_obj = getattr(self.mission, type)
        if mission_id in mission_obj.done:
            return 1
        return 0

    def mission_index(self, tp_id=0):
        data = {}
        if not tp_id:
            if self.mission.check_guide_over():
                self.mission.get_all_random_mission()
                self.mission.save()
            for tp_id, type in self.mm.mission.MISSIONMAPPING.iteritems():
                if tp_id == 2:
                    continue
                data[type] = self.get_status_by_type(type)
                data['liveness'] = self.get_status_liveness()
        else:
            type = self.mm.mission.MISSIONMAPPING[tp_id]
            data[type] = self.get_status_by_type(type)
        return data

    def get_status(self, mission_obj, mission_id, config):
        target_sort = config['sort']
        target_data = config.get('target', [])
        target_data1 = config.get('target1', [])
        if mission_id in mission_obj.done:
            status, value, need = -1, 1, 1
        else:
            if target_sort not in [1, 2, 5]:
                target_sort = '_num'
            func = globals()['target_sort%s' % target_sort]
            flag, value, need = func(self.mm, mission_obj, target_data, mission_id, target_data1)
            status = 1 if flag else 0
        return {
            'id': mission_id,
            'value': value,
            'need_value': need,
            'status': status
        }

    def get_status_liveness(self):
        # config = game_config.liveness_reward
        # data = {}
        done = self.mm.mission.live_done
        # for id, value in config.iteritems():
        #     if self.mm.mission.liveness >= value['need_liveness'] and id not in done:
        #         data[id] = [self.mm.mission.liveness,value['need_liveness'],1]
        #     elif self.mm.mission.liveness < value['need_liveness']:
        #         data[id] = [self.mm.mission.liveness,value['need_liveness'],0]
        return {'liveness':self.mm.mission.liveness,
                'done':done}


    def get_status_by_type(self, type='daily'):
        mission_obj = getattr(self.mission, type)
        result = {}
        done = mission_obj.done
        for mission_id in mission_obj.data:
            if isinstance(mission_id, (str,unicode)) and 'refresh_ts' in mission_id:
                now = int(time.time())
                end_time = mission_obj.data[mission_id] + self.mm.mission.RANDOMREFRESHTIME
                refresh_time = end_time - now if end_time - now > 0 else 0
                result[mission_id] = [refresh_time,now,0]
                continue
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            result[stats['id']] = [stats['value'], stats['need_value'], stats['status']]

        return {
            'result': result,
            'done': done
        }
