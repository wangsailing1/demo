#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'

from logics.user import UserLogic
from logics.friend import FriendLogic
# from logics.manufacture import ManufactureLogic
from tools.unlock_build import FRIEND_SORT
from lib.utils.sensitive import is_sensitive


def check_unlock(func):
    def wrapper(hm):
        mm = hm.mm
        if not mm.user.check_build(FRIEND_SORT):
            return 'error_unlock', {}

        return func(hm)

    return wrapper


@check_unlock
def friends(hm):
    """ 获取好友列表

    :param hm:
    :return:
    """
    mm = hm.mm

    fl = FriendLogic(mm)

    data = fl.friends_info()

    return 0, data


@check_unlock
def sent_gift(hm):
    """
    发送时间胶囊给好友
    :param hm:
    :return:
    """
    mm = hm.mm

    friend_id = hm.get_argument('friend_id')

    if not friend_id:
        return 'error_100', {}

    fl = FriendLogic(mm)
    rc, data = fl.sent_gift(friend_id)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def sent_gift_all(hm):
    """
    一键发送时间胶囊给好友
    :param hm:
    :return:
    """
    mm = hm.mm

    fl = FriendLogic(mm)
    rc, data = fl.sent_gift_all()
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def receive_gift(hm):
    """
    领取好友赠送的时间胶囊
    :param hm:
    :return:
    """
    mm = hm.mm

    friend_id = hm.get_argument('friend_id')

    if not friend_id:
        return 'error_100', {}

    fl = FriendLogic(mm)
    rc, data = fl.receive_gift(friend_id)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def receive_gift_all(hm):
    """
    一键领取好友赠送的时间胶囊
    :param hm:
    :return:
    """
    mm = hm.mm

    fl = FriendLogic(mm)
    rc, data = fl.receive_gift_all()
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def messages(hm):
    """ 获取好友消息列表

    :param hm:
    :return:
    """
    mm = hm.mm

    fl = FriendLogic(mm)

    data = fl.messages_info()

    return 0, data


@check_unlock
def search_friend(hm):
    """ 查找好友, 通过uid

    :param hm:
    :return:
    """
    mm = hm.mm

    uid = hm.get_argument('uid')

    fl = FriendLogic(mm)

    rc, data = fl.search_friend(uid)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def recommend_friend(hm):
    """ 推荐好友

    :param hm:
    :return:
    """
    mm = hm.mm

    fl = FriendLogic(mm)

    rc, data = fl.recommend_friend()
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def apply_friend(hm):
    """ 申请好友

    :param hm:
    :return:
    """
    mm = hm.mm

    uid = hm.get_argument('uid')

    fl = FriendLogic(mm)

    rc, data = fl.apply_friend(uid)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def agree_friend(hm):
    """ 同意好友申请

    :param hm:
    :return:
    """
    mm = hm.mm
    uid = hm.get_argument('uid')
    mid = hm.get_argument('mid', '')

    fl = FriendLogic(mm)

    rc, data = fl.agree_friend(uid, mid)
    # if rc != 0:
    #     return rc, {}

    return rc, data


@check_unlock
def refuse_friend(hm):
    """ 拒绝好友申请

    :param hm:
    :return:
    """
    mm = hm.mm
    mids = set(hm.get_mapping_argument('mid', num=0))
    all_mid = bool(hm.get_argument('all_mid'))

    fl = FriendLogic(mm)

    rc, data = fl.refuse_friend(mids, all_mid)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def remove_friend(hm):
    """ 删除好友

    :param hm:
    :return:
    """
    mm = hm.mm
    uid = hm.get_argument('uid')

    fl = FriendLogic(mm)

    rc, data = fl.remove_friend(uid)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def visit_friend(hm):
    """ 访问好友主场景请求

    :param hm: HandlerManager
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')

    fl = FriendLogic(mm)

    rc, data = fl.visit_friend(f_uid)
    if rc != 0:
        return rc, {}

    f_mm = mm.get_mm(f_uid)

    ful = UserLogic(f_mm)
    result = ful.main()
    data.update(result)

    return 0, data


@check_unlock
def parise_friend(hm):
    """
    给好友点赞
    :param hm:
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')

    fl = FriendLogic(mm)

    rc, data = fl.parise_friend(f_uid)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def manufacture(hm):
    """
    好友生产中心
    :param hm:
    :return:
    """
    # mm = hm.mm
    # f_uid = hm.get_argument('uid')
    # f_mm = mm.get_mm(f_uid)
    #
    result = {}
    # study_hero = {}
    # for workbench_id, workbench_dict in f_mm.manufacture.workbenchs.iteritems():
    #     if not workbench_dict:
    #         continue
    #     if workbench_dict['study_hero']['uid'] == mm.user.uid:
    #         study_hero[workbench_id] = workbench_dict['study_hero']['hero_oid']
    #
    # result['study_hero'] = study_hero
    #
    # ml = ManufactureLogic(f_mm)
    # data = ml.index()
    # result['manufacture'] = data

    return 0, result


@check_unlock
def sweep_workbench(hm):
    """
    打扫好友工作台
    :param hm:
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')
    workbench_id = hm.get_argument('workbench_id', is_int=True)

    fl = FriendLogic(mm)
    rc, data = fl.sweep_workbench(f_uid, workbench_id)

    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def encourage_workbench(hm):
    """
    给好友生产加油鼓劲
    :param hm:
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')
    workbench_id = hm.get_argument('workbench_id', is_int=True)

    fl = FriendLogic(mm)
    rc, data = fl.encourage_workbench(f_uid, workbench_id)

    if rc != 0:
        return rc, {}

    rc, result = manufacture(hm)
    result.update(data)

    return 0, result


@check_unlock
def study_manufacture(hm):
    """
    在好友生产中心实地学习
    :param hm:
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')
    hero_oid = hm.get_argument('hero_id')
    workbench_id = hm.get_argument('workbench_id', is_int=True)

    fl = FriendLogic(mm)
    rc, result = fl.study_manufacture(f_uid, hero_oid, workbench_id)

    if rc != 0:
        return rc, {}

    # 返回好友生产界面数据
    rc, data = manufacture(hm)
    result.update(data)

    return 0, result


@check_unlock
def revoke_study_hero(hm):
    """
    取回实地学习的卡牌
    :param hm:
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')
    hero_oid = hm.get_argument('hero_id')
    workbench_id = hm.get_argument('workbench_id', is_int=True)

    fl = FriendLogic(mm)
    rc, result = fl.revoke_study_hero(f_uid, hero_oid, workbench_id)

    if rc != 0:
        return rc, {}

    # 返回好友生产界面数据
    rc, data = manufacture(hm)
    result.update(data)

    return 0, result


@check_unlock
def redpacket_reward(hm):
    """
    领取红包
    :param hm:
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')

    fl = FriendLogic(mm)

    rc, data = fl.redpacket_reward(f_uid)
    if rc != 0:
        return rc, {}

    fl.visit_friend(f_uid)

    f_mm = mm.get_mm(f_uid)

    ful = UserLogic(f_mm)
    result = ful.main()
    data.update(result)

    return 0, data


@check_unlock
def receive_friendly_reward(hm):
    """
    领取友好度奖励
    :param hm:
    :return:
    """
    mm = hm.mm
    f_uid = hm.get_argument('uid')
    friend_lv = hm.get_argument('friend_lv', is_int=True)

    fl = FriendLogic(mm)
    rc, data = fl.receive_friendly_reward(f_uid, friend_lv)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def actor_chat(hm):
    mm = hm.mm
    group_id = hm.get_argument('group_id', 0, is_int=True)
    chapter_id = hm.get_argument('chapter_id', 0, is_int=True)
    choice_id = hm.get_argument('choice_id', 0, is_int=True)
    now_stage = hm.get_argument('now_stage', 0, is_int=True)
    if not group_id:
        return 1, {}  # 未选择艺人
    if not chapter_id and not now_stage:
        return 0, {'choice_id': mm.friend.get_chat_choice(group_id)}
    fl = FriendLogic(mm)
    rc, data = fl.actor_chat(group_id, chapter_id, choice_id, now_stage)
    _, actor_data = fl.actor_chat_index()
    data['actor'] = actor_data
    return rc, data


@check_unlock
def actor_chat_index(hm):
    mm = hm.mm
    fl = FriendLogic(mm)
    rc, data = fl.actor_chat_index()
    return rc, {'actor': data}


@check_unlock
def rename(hm):
    mm = hm.mm
    uid = hm.get_argument('uid', '')
    name = hm.get_argument('name', '')
    if not uid:
        return 1, {}  # 未指定好友
    if is_sensitive(name):
        return 2, {}  # 名字不合法
    # 好友为艺人
    if uid.isdigit():
        uid = int(uid)
        if uid not in mm.friend.actors:
            return 3, {}  # 不是好友
        mm.friend.actors[uid]['nickname'] = name
    else:
        if uid not in mm.friend.friends:
            return 3, {}  # 不是好友
        mm.friend.nickname[uid] = name
    mm.friend.save()
    return 0, {}
