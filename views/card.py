# -*- coding: utf-8 –*-

"""
Created on 2018-08-24

@author: sm
"""

from logics.card import CardLogic


def open(hm):
    mm = hm.mm
    user = mm.user
    card = mm.card
    return 0, {
        'card': card.cards,
        'user': {
            'name': user.name,
            'coin': user.coin,
            'diamond': user.diamond,
        }
    }


def card_level_up(hm):
    """卡牌升级，用经验道具
    """
    card_oid = hm.get_argument('card_oid')

    cl = CardLogic(hm.mm)
    rc, data = cl.card_level_up(card_oid)
    return rc, data


def card_add_love_exp(hm):
    """卡牌增加羁绊好感度
    """
    card_oid = hm.get_argument('card_oid')
    items = hm.get_mapping_arguments('items')

    cl = CardLogic(hm.mm)
    rc, data = cl.card_add_love_exp(card_oid, items)
    return rc, data


def card_love_lvup(hm):
    """卡牌羁绊，用经验道具
    """
    card_oid = hm.get_argument('card_oid')

    cl = CardLogic(hm.mm)
    rc, data = cl.card_love_level_up(card_oid)
    return rc, data


def card_quality_up(hm):
    """进阶/格调"""
    card_oid = hm.get_argument('card_oid')
    cl = CardLogic(hm.mm)
    rc, data = cl.card_quality_up(card_oid)
    return rc, data


def card_train(hm):
    """艺人培训
    """
    card_oid = hm.get_argument('card_oid')
    is_dimaond = hm.get_argument('is_dimaond', is_int=True)
    pro_ids = hm.get_mapping_argument('pro_ids', num=0)
    cl = CardLogic(hm.mm)
    rc, data = cl.card_train(card_oid, pro_ids, is_dimaond)
    return rc, data


def set_equip(hm):
    """穿装备
    """
    card_oid = hm.get_argument('card_oid')
    equip_ids = hm.get_mapping_argument('equip_ids', num=0)
    cl = CardLogic(hm.mm)
    rc, data = cl.set_equip(card_oid, equip_ids)
    return rc, data


def freezing(hm):
    """雪藏
    """
    card_oid = hm.get_argument('card_oid')
    cl = CardLogic(hm.mm)
    rc, data = cl.set_cold(card_oid, cold=True)
    return rc, data


def thaw(hm):
    """解冻
    """
    card_oid = hm.get_argument('card_oid')
    cl = CardLogic(hm.mm)
    rc, data = cl.set_cold(card_oid, cold=False)
    return rc, data


def card_piece_exchange(hm):
    """卡牌碎片合成
    :param hm:
    :return:
    """
    cl = CardLogic(hm.mm)
    card_id = hm.get_argument('card_id', is_int=True)
    rc, data = cl.card_piece_exchange(card_id)
    return rc, data

