#! --*-- coding: utf-8 --*--


import time
from gconfig import game_config
from logics.fans_activity import FansActivity
from tools.gift import add_mult_gift


# 首页
def fans_index(hm):
    mm = hm.mm
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    fa = FansActivity(mm)
    rc, data = fa.fans_index(activity_id)
    return rc, data


# 举办活动
def activity(hm):
    mm = hm.mm
    cards = hm.get_argument('cards', '')
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    config = game_config.fans_activity[activity_id]
    group = config['groupid']
    if activity_id != mm.fans_activity.activity.get(group, 0):
        return 3, {}  # 活动id错误
    if not activity_id:
        return 2, {}  # 未选活动
    if not cards:
        return 1, {}  # 没有艺人参加
    fa = FansActivity(mm)
    rc, data = fa.activity(activity_id, cards)
    return rc, data


# 解锁活动
def unlock_activity(hm):
    mm = hm.mm
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    field_id = hm.get_argument('field_id', 0, is_int=True)
    config = game_config.fans_activity[activity_id]
    if not config['type']:
        return 5, {}  # 首次建筑的等级错误
    cost = config['unlock_cost']
    if mm.user.dollar < cost:
        return 3, {}  # 美元不足
    if not activity_id:
        return 1, {}  # 没有活动
    if activity_id not in mm.fans_activity.can_unlock_activity:
        return 2, {}  # 该活动尚不能解锁
    group = config['groupid']
    if group in mm.fans_activity.activity:
        return 4, {}  # 已解锁
    if field_id in mm.user.get_pos_info:
        return 6, {}  # 此地已有建筑
    mm.fans_activity.activity[group] = activity_id
    mm.fans_activity.activity_log[activity_id] = {}
    mm.fans_activity.unlocked_activity.append(activity_id)
    mm.user.dollar -= cost
    mm.user.add_build(config['build_id'],field_id)
    mm.user.save()
    mm.fans_activity.save()
    fa = FansActivity(mm)
    rc, data = fa.fans_index()
    data['group_id'] = game_config.building.get(config['build_id'],{}).get('group', 0)
    return 0, data


# 升级活动
def up_activity(hm):
    mm = hm.mm
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    config = game_config.fans_activity[activity_id]
    next_id = config['next_id']
    group = config['groupid']
    if next_id == -1:
        return 1, {}  # 活动等级已经最大
    if next_id not in mm.fans_activity.can_unlock_activity:
        return 2, {}  # 该活动尚不能解锁
    next_config = game_config.fans_activity[next_id]
    cost = next_config['unlock_cost']
    if mm.user.dollar < cost:
        return 3, {}  # 美元不足
    if activity_id not in mm.fans_activity.activity_log:
        return 4, {}  # 活动错误
    if activity_id != mm.fans_activity.activity.get(group, 0):
        return 5, {}  # 升级id错误
    old_data = mm.fans_activity.activity_log[activity_id]
    mm.fans_activity.activity_log.pop(activity_id)
    mm.fans_activity.activity[group] = next_id
    mm.fans_activity.activity_log[next_id] = old_data
    mm.fans_activity.unlocked_activity.append(next_id)
    mm.fans_activity.change_card_mapping(activity_id,next_id)
    build_id = game_config.fans_activity[next_id]['build_id']
    mm.user.dollar -= cost
    mm.user.up_build(build_id,is_save=True)
    mm.fans_activity.save()
    mm.user.save()
    fa = FansActivity(mm)
    rc, data = fa.fans_index()
    return 0, data


# 领奖
def get_reward(hm):
    mm = hm.mm
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    if not activity_id:
        return 1, {}  # 请选择活动
    if activity_id not in mm.fans_activity.activity_log:
        return 2, {}  # 未参加活动
    if not mm.fans_activity.activity_log[activity_id]:
        return 2, {}  # 未参加活动
    gift = mm.fans_activity.count_produce(get_reward=True, activity_id=activity_id)
    reward = add_mult_gift(mm, gift)
    fa = FansActivity(mm)
    rc, data = fa.fans_index()
    data['reward'] = reward
    return 0, data
