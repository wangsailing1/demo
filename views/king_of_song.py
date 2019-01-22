# -*- coding: utf-8 –*-

"""
Created on 2018-12-03

@author: sm
"""


from logics.king_of_song import KingOfSongLogics


def index(hm):
    """
    首页
    :param hm:
    :return:
    """
    mm = hm.mm
    kl = KingOfSongLogics(mm)
    rc, data = kl.index()
    return rc, data


def enemy_battle(hm):
    """
    对手拍片数据
    :param hm:
    :return:
    """
    mm = hm.mm
    enemy_uid = hm.get_argument('enemy_uid')

    kl = KingOfSongLogics(mm)
    rc, data = kl.enemy_battle(enemy_uid)
    return rc, data


def battle(hm):
    """
    自己拍片数据
    :param hm:
    :return:
    """
    mm = hm.mm
    script_id = hm.get_argument('script_id', is_int=True)
    role_card = hm.get_mapping_arguments('role_card', params_type=(int, str))

    kl = KingOfSongLogics(mm)
    rc, data = kl.battle(script_id, role_card)
    return rc, data


def buy_battle_times(hm):
    """
    购买挑战次数
    :param hm:
    :return:
    """
    mm = hm.mm
    kl = KingOfSongLogics(mm)
    rc, data = kl.buy_battle_times()
    return rc, data


def get_rank_award(hm):
    rank = hm.get_argument('rank', is_int=True)
    kl = KingOfSongLogics(hm.mm)
    rc, data = kl.get_rank_award(rank)
    return rc, data
