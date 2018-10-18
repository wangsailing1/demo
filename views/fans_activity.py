#! --*-- coding: utf-8 --*--


import time
from gconfig import game_config
from logics.fans_activity import FansActivity


# 首页
def fans_index(hm):
    mm = hm
    data = {}
    config = game_config.fans_activity
    for id, value in mm.fans_activity.activity_log.iteritems():
        items = mm.fans_activity.count_produce(activity_id=id)
        config_id = config[id]
        all_time = config_id['240'] * 60
        remian_time = max(all_time + value['start_time'] - int(time.time()), 0)
        data[id] = {
            'items': items,
            'remian_time': remian_time,
            'cards': value['cards'],
        }
    data['unlocked_activity'] = mm.fans_activity.unlocked_activity
    data['can_unlock_activity'] = mm.fans_activity.can_unlock_activity
    return 0, data


# 举办活动
def event(hm):
    mm = hm.mm
    cards = hm.get_argument('cards', '')
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    if not activity_id:
        return 2, {}  # 未选活动
    if not cards:
        return 1, {}  # 没有艺人参加
    fa = FansActivity(mm)
    rc, data = fa.event(activity_id, cards)
    return rc, data
