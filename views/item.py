#! --*-- coding: utf-8 --*--

__author__ = 'sm'


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

