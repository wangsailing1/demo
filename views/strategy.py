# -*- coding: utf-8 –*-

from logics.strategy import Strategy


def index(hm):
    """ 首页
    """
    mm = hm.mm

    sl = Strategy(mm)
    data = sl.index()
    return 0, data


def apply(hm):
    """ 申请
    """
    mm = hm.mm
    target = hm.get_argument('target')
    if not target:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.apply(target)
    if rc != 0:
        return rc, {}

    return rc, data


def agree(hm):
    """ 申请
    """
    mm = hm.mm
    target = hm.get_argument('target')
    if not target:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.agree_invite(target)
    if rc != 0:
        return rc, {}

    return rc, data


def refuse(hm):
    """ 拒绝合作
    """
    mm = hm.mm
    target = hm.get_argument('target')
    if not target:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.refuse_invite(target)
    if rc != 0:
        return rc, {}

    return rc, data


def del_msg(hm):
    """ 删除消息
    """
    mm = hm.mm
    sort = hm.get_argument('sort', )
    target = hm.get_argument('target')

    if sort not in ('invite', 'refuse', 'apply') or not target:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.del_msg(target, sort)

    return rc, data


def quit(hm):
    """ 退出合作
    """
    mm = hm.mm

    sl = Strategy(mm)
    rc, data = sl.quit_strategy()
    if rc != 0:
        return rc, {}

    return rc, data


def choice(hm):
    """ 选择任务
    """
    mm = hm.mm
    task_id = hm.get_argument('task_id', is_int=1)

    if not task_id:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.choice_task(task_id)

    return rc, data


def task_reward(hm):
    """ 选择任务
    """
    mm = hm.mm
    task_id = hm.get_argument('task_id', is_int=1)

    if not task_id:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.task_reward(task_id)

    return rc, data


def level_reward(hm):
    """ 领取等级奖励
    """
    mm = hm.mm

    sl = Strategy(mm)
    rc, data = sl.level_reward()

    return rc, data


def send_gift(hm):
    """ 送礼
    """
    mm = hm.mm
    kind = hm.get_argument('kind', is_int=1)

    sl = Strategy(mm)
    rc, data = sl.send_gift(kind)

    return rc, data


def quick_done(hm):
    """
    快速完成任务
    """
    mm = hm.mm

    sl = Strategy(mm)
    rc, data = sl.quick_done()
    return rc, data

