# -*- coding: utf-8 –*-
__author__ = 'ljm'

import time
from tools.gift import add_mult_gift
from gconfig import game_config


# 助理首页
def assistant_index(hm):
    mm = hm.mm
    ass = mm.assistant
    return 0, {
        'assistant': ass.assistant,
        'assistant_gift': ass.assistant_gift,
        'assistant_daily': ass.assistant_daily,
        'license_apply_times': ass.license_apply_times,
        'license_apply_done_time': ass.license_apply_done_time,
        'max_times':ass.get_max_time(),
        'status':ass.get_status()
    }

# 领取日常奖励
def get_daily_reward(hm):
    mm = hm.mm
    if not mm.assistant.assistant:
        return 1, {}  # 请先聘请终身助理
    if mm.assistant.assistant_daily:
        return 2, {}  # 已经领取
    gift = game_config.assistant[1]['gift']
    reward = add_mult_gift(mm,gift)
    mm.assistant.assistant_daily = 1
    mm.assistant.save()
    _ , info = assistant_index(hm)
    info['reward'] = reward
    return 0 , info

# 申请许可证
def license_apply(hm):
    mm = hm.mm
    if not mm.assistant.assistant:
        return 1, {}  # 请先聘请终身助理
    if mm.assistant.license_apply_times >= mm.assistant.get_max_time():
        return 2, {}  # 申请次数达到上限
    now = int(time.time())
    if mm.assistant.license_apply_done_time:
        if mm.assistant.license_apply_done_time > now:
            return 3, {}  # 申请中
        else:
            return 4, {}  # 请先领取
    mm.assistant.license_apply_times += 1
    mm.assistant.license_apply_done_time = now + game_config.common.get(95, 240) * 60
    mm.assistant.save()
    _, info = assistant_index(hm)
    return 0, info

# 领取许可证
def get_license(hm):
    mm = hm.mm
    if not mm.assistant.assistant:
        return 1, {}  # 请先聘请终身助理
    if mm.assistant.license_apply_times and not mm.assistant.license_apply_done_time:
        return 4, {}  # 已经领取过了
    if not mm.assistant.license_apply_done_time:
        return 2, {}  # 请先申请
    now = int(time.time())
    if mm.assistant.license_apply_done_time and mm.assistant.license_apply_done_time > now:
        return 3, {}  # 申请中
    if mm.user.script_license >= mm.user.max_license():
        return 5, {}  # 许可证已达上限
    mm.user.script_license += 1
    mm.assistant.license_apply_done_time = 0
    mm.user.save()
    mm.assistant.save()
    _, info = assistant_index(hm)
    return 0, info

def get_gift(hm):
    mm = hm.mm
    if not mm.assistant.assistant_gift:
        return 1, {}  # 未充值
    if mm.assistant.assistant_gift == 2:
        return 2, {}  # 已经领取
    gift = game_config.charge[11]['gift']
    reward = add_mult_gift(mm, gift)
    _, info = assistant_index(hm)
    info['reward'] = reward
    return 0, info


