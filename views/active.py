#! --*-- coding: utf-8 --*--

from logics.active import ActiveCard
from logics.user import UserLogic


def active_card_index(hm):
    """月卡至尊卡活动首页
    :param hm:
    :return:
    """
    mm = hm.mm
    acl = ActiveCard(mm)
    data = acl.show()

    return 0, data


def active_card_award(hm):
    """月卡至尊卡奖励领取"""
    mm = hm.mm

    active_id = hm.get_argument('active_id', 0, is_int=True)

    acl = ActiveCard(mm)

    rc, data = acl.receive(active_id)
    # data['active_center'] = mm.active_hot_dot.hot_dot()
    if rc != 0:
        return rc, data

    data['show'] = acl.show()

    return 0, data