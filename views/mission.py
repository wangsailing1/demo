#! --*-- coding: utf-8 --*--

from logics.mission import Mission
from tools.gift import add_mult_gift
from gconfig import game_config


def mission_index(hm):
    mm = hm.mm
    tp_id = hm.get_argument('tp_id', 0, is_int=True)
    mission = Mission(mm)
    data = mission.mission_index(tp_id)
    return 0, data


def get_reward(hm):
    mm = hm.mm
    mission = Mission(mm)
    tp_id = hm.get_argument('tp_id', 0, is_int=True)
    mission_id = hm.get_argument('mission_id', 0, is_int=True)

    if tp_id == 5:
        config = game_config.liveness_reward[mission_id]
        if mission_id in mm.mission.live_done:
            return 3, {}  #已领
        if  mission.get_status_liveness()['liveness'] < config['need_liveness']:
            return 4, {}  #未完成
        gift = config['reward']
        reward = add_mult_gift(mm,gift)
        mm.mission.live_done.append(mission_id)
        mm.mission.save()
        data = mission.mission_index()
        data['reward'] = reward
        return 0,data
    m_type = mm.mission.MISSIONMAPPING[tp_id]
    if not tp_id or not mission_id:
        return 1, {}  # 参数错误
    if not mission.has_reward_by_type(m_type, mission_id):
        return 2, {}  # 未完成
    if mission.get_done_mission(m_type, mission_id):
        return 3, {}  # 已领
    mm_obj = getattr(mm.mission, m_type)
    mm_obj.done_task(mission_id)
    gift = mm_obj.config[mission_id]['reward']
    if tp_id == 1:
        mm.mission.liveness += mm_obj.config[mission_id]['liveness']
    if tp_id == 3:
        if mm.mission.check_guide_over():
            mm.mission.get_all_random_mission()
        else:
            mm.mission.get_guide_mission()
    reward = add_mult_gift(mm,gift)
    mm.mission.save()
    data = mission.mission_index()
    data['reward'] = reward
    return 0, data

def refresh_mission(hm):
    mm = hm.mm
    mission = Mission(mm)
    mission_id = hm.get_argument('mission_id', 0, is_int=True)
    mm.mission.refresh_random_misstion(mission_id)
    mm.mission.save()
    data = mission.mission_index()
    return 0, data



