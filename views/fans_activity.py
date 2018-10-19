#! --*-- coding: utf-8 --*--


import time
from gconfig import game_config
from logics.fans_activity import FansActivity
from tools.gift import add_mult_gift

# 首页
def fans_index(hm):
    mm = hm
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    data = {}
    config = game_config.fans_activity
    if activity_id and activity_id not in mm.fans_activity.activity_log:
        return 1, {} #活动错误
    if activity_id:
        value = mm.fans_activity.activity_log[activity_id]
        items = mm.fans_activity.count_produce(activity_id=activity_id)
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

#解锁活动
def unlock_event(hm):
    mm = hm.mm
    event_id = hm.get_argument('event_id',0,is_int=True)
    config = game_config.fans_activity[event_id]
    cost = config['unlock_cost']
    if mm.user.dollar < cost:
        return 3, {}  #美元不足
    if not event_id:
        return 1, {}  #没有活动
    if event_id not in mm.fans_activity.can_unlock_activity:
        return 2, {}  #该活动尚不能解锁
    mm.fans_activity.activity_log[event_id] = {}
    mm.fans_activity.unlocked_activity.append(event_id)
    mm.user.dollar -= cost
    mm.user.save()
    mm.fans_activity.save()
    return 0, {}

#升级活动
def up_event(hm):
    mm = hm.mm
    event_id = hm.get_argument('event_id', 0, is_int=True)
    config = game_config.fans_activity[event_id]
    next_id = config['next_id']
    if next_id == -1:
        return 1, {}  #活动等级已经最大
    if next_id not in mm.fans_activity.can_unlock_activity:
        return 2, {}  # 该活动尚不能解锁
    next_config = game_config.fans_activity[next_id]
    cost = next_config['unlock_cost']
    if mm.user.dollar < cost:
        return 3, {}  #美元不足
    old_data = mm.fans_activity.activity_log[event_id]
    mm.fans_activity.activity_log.pop(event_id)
    mm.fans_activity.activity_log[next_id] = old_data
    mm.fans_activity.unlocked_activity.append(next_id)
    mm.user.dollar -= cost
    mm.fans_activity.save()
    mm.user.save()


#领奖
def get_reward(hm):
    mm = hm.mm
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    if not activity_id:
        return 1, {} #请选择活动
    if activity_id not in mm.fans_activity.activity_log:
        return 2, {}  #未参加活动
    if not mm.fans_activity.activity_log[activity_id]:
        return 2, {}  #未参加活动
    gift = mm.fans_activity.count_produce(get_reward=True,activity_id=activity_id)
    reward = add_mult_gift(mm,gift)
    return 0, {'reward':reward}
