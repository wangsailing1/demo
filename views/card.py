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
    max_num = mm.item.get_item(mm.item.PERFUME)
    if count > max_num:
        return 1, {}  # 数量不足
    if card_id not in mm.card.cards:
        return 2, {}  # 未拥有此卡牌
    add_num = game_config.use_item.get(mm.item.PERFUME, {}).get('use_effect', 1) * count
    mm.card.add_card_popularity(card_id, add_num)
    mm.item.del_item(mm.item.PERFUME, count)

    add_exp = int(count * game_config.common[89])
    mm.user.add_company_vip_exp(add_exp, is_save=True)
    mm.card.save()
    mm.item.save()
    return 0, {
        'card_info': mm.card.cards[card_id],
        'company_vip_exp': mm.user.company_vip_exp
    }


def skill_level_up(hm):
    cl = CardLogic(hm.mm)
    card_oid = hm.get_argument('card_oid', '')
    skill_id = hm.get_argument('skill_id', 0, is_int=True)
    rc, data = cl.skill_level_up(card_oid, skill_id)
    return rc, data


def train_card(hm):
    card_oid = hm.get_argument('card_oid', '')
    if not hm.mm.card.cards.get(card_oid):
        return 1, {}  # 未拥有该卡牌

    cl = CardLogic(hm.mm)
    rc, data = cl.train_card(card_oid)
    return rc, data


def use_exp_item(hm):
    card_oid = hm.get_argument('card_oid', '')
    item_id = hm.get_argument('item_id', '', is_int=True)
    item_num = hm.get_argument('item_num', '', is_int=True)
    cl = CardLogic(hm.mm)
    rc, data = cl.use_exp_item(card_oid, item_id, item_num)
    return rc, data


def training_room_index(hm):
    mm = hm.mm
    return 0, mm.card.training_room


def finish_train(hm):
    mm = hm.mm
    training_position_id = hm.get_argument('tr_id', 0, is_int=True)
    if not training_position_id:
        return 1, {}  # 未传递参数tr_id

    if training_position_id not in mm.card.training_room:
        return 2, {}  # 训练位未开启

    cl = CardLogic(mm)
    rc, data = cl.finish_train(training_position_id)
    return rc, data


def train_speed_up(hm):
    mm = hm.mm
    training_position_id = hm.get_argument('tr_id', 0, is_int=True)
    if not training_position_id:
        return 1, {}  # 未传递参数tr_id

    if training_position_id not in mm.card.training_room:
        return 2, {}  # 训练位未开启

    cl = CardLogic(mm)
    rc, data = cl.train_speed_up(training_position_id)
    return rc, data


def add_train_place(hm):
    mm = hm.mm
    cl = CardLogic(mm)
    rc, data = cl.add_train_place()
    return rc, data


def choice_train_card(hm):
    mm = hm.mm
    return 0, mm.card.choice_train_card()


def train(hm):
    mm = hm.mm
    card_oid = hm.get_argument('card_oid', '')
    training_position_id = hm.get_argument('tr_id', 0, is_int=True)
    if not mm.card.cards.get(card_oid):
        return 1, {}  # 未拥有该卡牌

    if not training_position_id:
        return 2, {}  # 未传递参数tr_id

    if training_position_id not in mm.card.training_room:
        return 3, {}  # 训练位未开启

    cl = CardLogic(mm)
    rc, data = cl.train(card_oid, training_position_id)
    return rc, data