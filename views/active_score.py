# -*- coding: utf-8 –*-
__author__ = 'ljm'

from logics.active_score import ActiveScore


# 首页
def index(hm):
    mm = hm.mm
    active_score = ActiveScore(mm)
    rc, data = active_score.index()
    return rc, data

# 领取奖励
def get_reward(hm):
    """
    :param hm:  tp: 1 每日奖励 2 累计奖励 3 排行奖励
    :return: 
    """
    mm = hm.mm
    tp = hm.get_argument('tp', 1, is_int=True)
    reward_id = hm.get_argument('reward_id', 1, is_int=True)
    active_score = ActiveScore(mm)
    rc, data = active_score.get_reward(tp, reward_id)
    return rc, data

# 获取排行信息
def rank_info(hm):
    mm = hm.mm
    start = hm.get_argument('start', 1, is_int=True)
    end = hm.get_argument('end', 20, is_int=True)
    active_score = ActiveScore(mm)
    rc, data = active_score.rank_info(start, end)
    return rc, data
