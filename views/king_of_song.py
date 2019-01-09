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


def battle(hm):
    """
    挑战对手
    :param hm:
    :return:
    """
    mm = hm.mm
    enemy_uid = hm.get_argument('enemy_uid')
    role_card = hm.get_mapping_arguments('role_card', params_type=(int, str))

    kl = KingOfSongLogics(mm)
    rc, data = kl.battle(role_card, target_uid=enemy_uid)
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
