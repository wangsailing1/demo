#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'


from logics.item import ItemLogic


def use_item(hm):
    """ 使用普通道具

    :param hm: HandlerManager
    :return:
    """
    mm = hm.mm
    item_id = hm.get_argument('item_id', is_int=True)
    num = hm.get_argument('num', 1, is_int=True)
    reward_index = hm.get_mapping_argument('reward_index', num=0)

    if num <= 0:
        return -1, {}

    il = ItemLogic(mm)
    rc, data = il.use_item(item_id, num, reward_index)

    return rc, data


def set_item_group(hm):
    """ 设置道具组

    :param hm:
    :return:
    """
    mm = hm.mm

    name = hm.get_argument('name')
    group_id = hm.get_argument('group_id', is_int=True)
    group = hm.get_mapping_argument('group', is_int=True, num=0)

    il = ItemLogic(mm)
    rc, data = il.set_item_group(group_id, name, group)
    if rc != 0:
        return rc, {}

    return rc, data


def synthesis_aitem(hm):
    """
    合成觉醒材料
    :param hm:
    :return:
    """
    mm = hm.mm

    awaken_id = hm.get_argument('awaken_id', is_int=True)
    num = hm.get_argument('num', is_int=True)

    if not awaken_id or num <= 0:
        return -1, {}   # 参数错误

    il = ItemLogic(mm)
    rc, data = il.synthesis_aitem(awaken_id, num)
    if rc != 0:
        return rc, {}

    return rc, data


def synthesis_item(hm):
    """
    道具碎片合成
    :param hm:
    :return:
    """
    mm = hm.mm

    item_id = hm.get_argument('item_id', is_int=True)
    num = hm.get_argument('num', default=1, is_int=True)

    if item_id <= 0 or num <= 0:
        return 'error_100', {}  # 参数错误

    il = ItemLogic(mm)
    rc, data = il.synthesis_item(item_id, num)
    if rc != 0:
        return rc, {}

    return rc, data


def sell_item(hm):
    """
    出售道具
    :param hm:
    :return:
    """
    mm = hm.mm

    item_type = hm.get_argument('item_type')
    item_id = hm.get_argument('item_id', is_int=True)
    num = hm.get_argument('num', default=1, is_int=True)

    if item_id <= 0 or num <= 0 or item_type not in ['item', 'grade_item', 'awaken_item']:
        return 'error_100', {}  # 参数错误

    il = ItemLogic(mm)
    rc, data = il.sell_item(item_type, item_id, num)
    if rc != 0:
        return rc, {}

    return rc, data
