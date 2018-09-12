# -*- coding: utf-8 –*-
from tools.gift import add_mult_gift
from gconfig import game_config


def book_index(hm):
    mm = hm.mm
    data = {}
    data['cards'] = mm.card_book.cards
    data['card_data'] = {i: {'flag': j['flag']} for i, j in mm.card_book.book.iteritems()}
    data['scripts'] = mm.script_book.scripts
    data['script_data'] = {i: {'flag': j['flag']} for i, j in mm.script_book.book.iteritems()}
    data['group'] = mm.script_book.group
    return 0, data


def get_card_reward(hm):
    mm = hm.mm
    group_id = int(hm.get_argument('group_id', 0))
    if group_id not in mm.card_book.book:
        return 1, {}  # 组合未完成
    if mm.card_book.book[group_id]['flag'] == -1:
        return 2, {}  # 组合未完成
    if mm.card_book.book[group_id]['flag'] == 1:
        return 3, {}  # 奖励已领
    config = game_config.card_book
    if group_id not in config:
        return 4, {}  # 没有相应组合
    gift = config[group_id]['award']
    mm.card_book.book[group_id]['flag'] = 1
    reward = add_mult_gift(mm, gift)
    if not reward:
        return 5, {}
    mm.card_book.save()
    data = {}
    data['cards'] = mm.card_book.cards
    data['data'] = {i: {'flag': j['flag']} for i, j in mm.card_book.book.iteritems()}

    return {'reward': reward,
            'data': data}


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
    data = {}
    data['scripts'] = mm.script_book.scripts
    data['data'] = {i: {'flag': j['flag']} for i, j in mm.script_book.book.iteritems()}
    data['group'] = mm.script_book.group
    return 0, {'reward': reward,
               'data': data}


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
    data = {}
    data['scripts'] = mm.script_book.scripts
    data['data'] = {i: {'flag': j['flag']} for i, j in mm.script_book.book.iteritems()}
    data['group'] = mm.script_book.group

    return 0, {'reward': reward,
               'data': data}
