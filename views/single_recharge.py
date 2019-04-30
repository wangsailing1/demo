# -*- coding: utf-8 –*-


from logics.single_recharge import SingleRecharge as SRL
from logics.single_recharge import ServerSingleRecharge as SSRL


def index(hm):
    """ 首页
    """
    mm = hm.mm
    srl = SRL(mm)
    rc, data = srl.index()
    return rc, data


def reward(hm):
    """ 领奖
    """
    mm = hm.mm
    reward_id = hm.get_argument('reward_id', is_int=True)

    srl = SRL(mm)
    rc, data = srl.reward(reward_id)
    return rc, data


def server_index(hm):
    """ 首页
    """
    mm = hm.mm
    ssrl = SSRL(mm)
    rc, data = ssrl.index()
    return rc, data


def server_reward(hm):
    """ 领奖
    """
    mm = hm.mm
    reward_id = hm.get_argument('reward_id', is_int=True)

    ssrl = SSRL(mm)
    rc, data = ssrl.reward(reward_id)
    return rc, data
