#! --*-- coding: utf-8 --*--


def index(hm):
    mm = hm.mm
    return 0, {}

def get_toy(hm):
    mm = hm.mm
    catch = hm.get_argument('catch',is_int=True)
    reward_id = hm.get_argument('reward_id',is_int=True)