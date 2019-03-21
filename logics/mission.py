# coding: utf-8

import time
import datetime
from gconfig import game_config
from models.vip_company import task_cd

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
    num = len(reward_obj.get_count(mission_id)) if isinstance(reward_obj.get_count(mission_id), list) else 0
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


# 星级艺人总数
def target_sort15(mm, reward_obj, target_data, mission_id, target_data1):
    star, target_value = target_data[:2]
    value = 0
    for k, v in mm.card.cards.iteritems():
        if v['star'] >= star:
            value += 1
    return value >= target_value, value, target_value


# 星级剧本总数
def target_sort16(mm, reward_obj, target_data, mission_id, target_data1):
    star, target_value = target_data[:2]
    value = 0
    for script_id in mm.script.own_script:
        script_config = game_config.script[script_id]
        if script_config['star'] >= star:
            value += 1
    return value >= target_value, value, target_value


# # 累计成就点 todo
# def target_sort21(mm, reward_obj, target_data, mission_id, target_data1):
#     pass


# 艺人好感度  [好感度love数值， 达到要求好感度的卡牌数 ]
def target_sort23(mm, reward_obj, target_data, mission_id, target_data1):
    love_exp, target_value = target_data[:2]
    value = 0
    for k, v in mm.card.cards.iteritems():
        if v['love_exp'] >= love_exp:
            value += 1
    return value >= target_value, value, target_value


# 是否建造建筑,target对应的建筑groupID是否存在，若存在，则任务完成
def target_sort26(mm, reward_obj, target_data, mission_id, target_data1):
    group_id = target_data[0]
    value = 1 if group_id in mm.user.group_ids else 0
    target_value = target_data[1]
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
            if isinstance(mission_id, basestring) and 'time' in mission_id:
                continue
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            if stats['status'] == 1:
                return 1
        return 0

    def get_done_mission(self, type='daily', mission_id=''):
        mission_obj = getattr(self.mission, type)
        if mission_id in mission_obj.done:
            return 1
        return 0

    def mission_red_dot(self,type = 'daily', m_id=None):
        mission_obj = getattr(self.mission, type)
        for mission_id in mission_obj.data:
            if m_id and mission_id != m_id:
                continue
            if isinstance(mission_id, basestring) and ('time' in mission_id or 'refresh_ts' in mission_id):
                continue
            has_reward = self.has_reward_by_type(type=type, mission_id=mission_id)
            done = self.get_done_mission(type=type, mission_id=mission_id)
            if has_reward and not done:
                return True
        return False

    def mission_index(self, tp_id=0, is_save=True):
        data = {}
        data['remain_refresh_times'] = game_config.common.get(42, 2) - self.mission.refresh_times
        if not tp_id:
            # if self.mission.check_guide_over():
            #     self.mission.get_all_random_mission()
            #     if is_save:
            #         self.mission.save()
            for tp_id, type in self.mm.mission.MISSIONMAPPING.iteritems():
                if tp_id == 2:
                    continue
                #todo 新手引导任务暂时屏蔽
                if tp_id == 3:
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
        if mission_id in mission_obj.done and mission_id not in mission_obj.data:
            status, value, need = -1, 1, 1
        else:
            func = globals().get('target_sort%s' % target_sort)
            if not func:
                target_sort = '_num'
                func = globals()['target_sort%s' % target_sort]

            # if target_sort not in [1, 2, 5]:
            #     target_sort = '_num'
            # func = globals()['target_sort%s' % target_sort]
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
        return {'liveness': self.mm.mission.liveness,
                'done': done}

    def get_status_by_type(self, type='daily'):
        mission_obj = getattr(self.mission, type)
        result = {}
        done = mission_obj.done
        for mission_id in mission_obj.data:
            if isinstance(mission_id, (str, unicode)) and 'time' in mission_id:
                continue
            if isinstance(mission_id, (str, unicode)) and 'refresh_ts' in mission_id:
                now = int(time.time())
                end_time = mission_obj.data[mission_id] + self.mm.mission.RANDOMREFRESHTIME - task_cd(self.mm.user) * 60
                refresh_time = end_time - now if end_time - now > 0 else 0
                result[mission_id] = [refresh_time, now, 0]
                continue
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            result[stats['id']] = [stats['value'], stats['need_value'], stats['status']]
        time_data = {}
        if type == 'box_office':
            time_data = mission_obj.data
        return {
            'result': result,
            'done': done,
            'cur_task': time_data
        }
