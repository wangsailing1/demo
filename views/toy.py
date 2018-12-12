#! --*-- coding: utf-8 --*--

from logics.toy import Toy

def index(hm):
    mm = hm.mm
    sort = hm.get_argument('sort',is_int=True)
    toy = Toy(mm,sort)
    rc, data = toy.index()
    return rc, data


def get_toy(hm):
    mm = hm.mm
    catch = hm.get_argument('catch',is_int=True)
    sort = hm.get_argument('sort', is_int=True)
    reward_id = hm.get_argument('reward_id',is_int=True)
    toy = Toy(mm, sort)
    rc, data = toy.get_toy(catch, reward_id)
    return rc, data

def refresh(hm):
    mm = hm.mm
    sort = hm.get_argument('sort', is_int=True)
    toy = Toy(mm, sort)
    rc, data = toy.refresh()
    return rc, data

def get_rank_reward(hm):
    mm = hm.mm
    sort = hm.get_argument('sort', is_int=True)
    if sort != 1:
        return 0, {}
    toy = Toy(mm, sort)
    rc, data = toy.get_rank_reward()
    return rc, data