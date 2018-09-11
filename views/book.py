# -*- coding: utf-8 –*-
from tools.gift import add_mult_gift
from gconfig import game_config

def card_book_index(hm):
    mm = hm.mm
    return 0, {'data':mm.card_book.book}

def get_card_reward(hm):
    mm = hm.mm
    group_id = int(hm.get_argument('group_id',0))
    if group_id not in mm.card_book.book:
        return 1, {}  #组合未完成
    if mm.card_book.book[group_id]['flag'] == -1:
        return 2, {}  #组合未完成
    if mm.card_book.book[group_id]['flag'] == 1:
        return 3, {}  #奖励已领
    config = game_config.card_book
    if group_id not in config:
        return 4, {}  #没有相应组合
    gift = config[group_id]['award']
    mm.card_book.book[group_id]['flag'] = 1
    reward = add_mult_gift(mm,gift)
    if not reward:
        return 5, {}
    mm.card_book.save()

    return {'reward':reward,
            'data':mm.card_book.book}

def script_book_index(hm):
    mm = hm.mm
    return 0, mm.script_book.book


def get_script_reward(hm):
    mm = hm.mm
    group_id = int(hm.get_argument('group_id', 0))
    if group_id not in mm.script_book.book:
        return 1, {}  # 组合未完成
    if mm.script_book.book[group_id]['flag'] == -1:
        return 2, {}  # 组合未完成
    if mm.script_book.book[group_id]['flag'] == 1:
        return 3, {}  # 奖励已领
    config = game_config.script_book
    if group_id not in config:
        return 4, {}  # 没有相应组合
    gift = config[group_id]['award']
    mm.script_book.book[group_id]['flag'] = 1
    reward = add_mult_gift(mm, gift)
    if not reward:
        return 5, {}
    mm.script_book.save()

    return 0, {'reward': reward,
            'data': mm.script_book.book}


def script_group_index(hm):
    mm = hm.mm
    return 0, mm.script_group.group


def get_group_reward(hm):
    mm = hm.mm
    group_id = int(hm.get_argument('group_id', 0))
    if group_id not in mm.script_group.group:
        return 1, {}  # 组合未完成
    if mm.script_group.group[group_id]['flag'] == -1:
        return 2, {}  # 组合未完成
    if mm.script_group.group[group_id]['flag'] == 1:
        return 3, {}  # 奖励已领
    config = game_config.script_group_object
    if group_id not in config:
        return 4, {}  # 没有相应组合
    gift = config[group_id]['award']
    mm.script_group.group[group_id]['flag'] = 1
    reward = add_mult_gift(mm, gift)
    if not reward:
        return 5, {}
    mm.script_group.save()

    return 0, {'reward': reward,
            'data': mm.script_group.group}

