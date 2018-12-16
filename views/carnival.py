# -*- coding: utf-8 –*-

from logics.carnival import Carnival


def index(hm):
    mm = hm.mm
    tp = hm.get_argument('carvical_type', 1, is_int=True)
    carvical_open = mm.carnival.server_carvical_open(tp=tp)
    if not carvical_open:
        return 1, {}  # 活动已关闭
    carnival = Carnival(mm)
    rc, data = carnival.index(tp=tp)
    return rc, data


def dice(hm):
    mm = hm.mm
    tp = hm.get_argument('carvical_type', 1, is_int=True)
    carvical_open = mm.carnival.server_carvical_open(tp=tp)
    if not carvical_open:
        return 1, {}  # 活动已结束
    pre_str = mm.carnival.CONFIGMAPPING[tp]
    dice_num = getattr(mm.carnival, '%s%s' % (pre_str, 'dice_num'))
    if not dice_num:
        return 2, {}  # 骰子不足
    carnival = Carnival(mm)
    rc, data = carnival.dice(tp=tp)
    return rc, data


def get_dice(hm):
    mm = hm.mm
    tp = hm.get_argument('carvical_type', 1, is_int=True)
    m_id = hm.get_argument('mission_id', 0, is_int=True)
    carvical_open = mm.carnival.server_carvical_open(tp=tp)
    if not carvical_open:
        return 1, {}  # 活动已结束
    carnival = Carnival(mm)
    done = carnival.get_done_mission(tp=tp, mission_id=m_id)
    if done:
        return 2, {}  # 已领
    status = carnival.has_reward_by_type(tp=tp, mission_id=m_id)
    if not status:
        return 3, {}  # 未完成
    rc, data = carnival.get_reward(tp=tp, mission_id=m_id)
    return rc, data
