# -*- coding: utf-8 –*-

"""
Created on 2018-08-24

@author: sm
"""

from logics.card import CardLogic
from gconfig import game_config


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


def equip_piece_exchange(hm):
    """装备碎片合成
    :param hm:
    :return:
    """
    cl = CardLogic(hm.mm)
    equip_piece_id = hm.get_argument('piece_id', is_int=True)
    num = hm.get_argument('num', default=1, is_int=True)
    rc, data = cl.equip_piece_exchange(equip_piece_id, num)
    return rc, data


def equip_piece_auto_exchange(hm):
    """装备碎片一键合成
    :param hm:
    :return:
    """
    cl = CardLogic(hm.mm)
    rc, data = cl.equip_piece_auto_exchange()
    return rc, data


def set_name(hm):
    """卡牌取名字"""
    cl = CardLogic(hm.mm)
    card_oid = hm.get_argument('card_oid')
    name = hm.get_argument('name')
    rc, data = cl.set_name(card_oid, name)
    return rc, data


def up_card_building(hm):
    cl = CardLogic(hm.mm)
    rc, data = cl.up_card_building()
    return rc, data


def add_card_box(hm):
    mm = hm.mm
    cost = game_config.common[6]
    if mm.user.diamond < cost:
        return 1, {}  # 钻石不足
    mm.card.card_box += 1
    mm.user.deduct_diamond(cost)
    mm.user.save()
    mm.card.save()
    return 0, {'card_box': mm.card.card_box}


def add_card_popularity(hm):
    mm = hm.mm
    count = hm.get_argument('count', 1, is_int=True)
    card_id = hm.get_argument('card_id', '')
    # todo max取值
    max_num = 10
    if count > max_num:
        return 1, {}  # 数量不足
    if card_id not in mm.card.cards:
        return 2, {}  # 未拥有此卡牌
    mm.card.add_card_popularity(card_id, count)
    # todo 减数值
    add_exp = count * game_config.common(89)
    mm.user.add_company_vip_exp(add_exp, is_save=True)
    mm.card.save()
    return 0, {}
