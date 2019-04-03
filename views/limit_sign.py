#! --*-- coding: utf-8 --*--

from gconfig import game_config
from tools.gift import add_mult_gift


def limit_sign_index(hm):
    mm = hm.mm
    limit_sign = mm.limit_sign
    if not limit_sign.is_open():
        return 1, {}
    return 0, {'version': limit_sign.version,
               'reward_dict': limit_sign.reward_dict,
               'score': limit_sign.score,
               'remain_time': limit_sign.get_remain_time()}

def get_reward(hm):
    mm = hm.mm
    limit_sign = mm.limit_sign
    r_id = hm.get_argument('r_id', is_int=True)
    if not limit_sign.is_open():
        return 1, {}  # 活动未开启
    config = game_config.get_add_recharge_limit_mapping()[limit_sign.version]
    if r_id not in config:
        return 2, {}  # 参数错误
    if r_id not in limit_sign.reward_dict:
        return 3, {}  # 该奖励未激活
    if limit_sign.reward_dict[r_id].get('status', 1):
        return 4, {}  # 该奖励已经领取
    gift = config[r_id]['reward']
    reward = add_mult_gift(mm, gift)
    limit_sign.reward_dict[r_id]['status'] = 1
    limit_sign.save()
    _, data = limit_sign_index(hm)
    data['reward'] = reward
    return 0, data
