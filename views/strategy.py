# -*- coding: utf-8 –*-

from gconfig import game_config
from logics.strategy import Strategy
from return_msg_config import get_error_14_msg


def get_enter_level():
    return game_config.common.get(100, 0)             # 等级拦截


def level_limit(method):
    """判断是否符合等级要求
    """
    def wrapper(hm, *args, **kwargs):
        u = hm.mm.user
        enter_level = get_enter_level()
        if u.level < enter_level:
            return 'error_14', {'custom_msg': get_error_14_msg(u.language_sort, enter_level)}
        else:
            return method(hm, *args, **kwargs)
    return wrapper


@level_limit
def index(hm):
    """ 首页
    """
    mm = hm.mm

    sl = Strategy(mm)
    data = sl.index()
    return 0, data


@level_limit
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


@level_limit
def agree(hm):
    """ 同意申请
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

    if sort not in ('invite', 'refuse', 'apply', 'quit') or not target:
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


@level_limit
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


@level_limit
def task_reward(hm):
    """ 领取任务奖励
    """
    mm = hm.mm
    task_id = hm.get_argument('task_id', is_int=1)

    if not task_id:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.task_reward(task_id)

    return rc, data


@level_limit
def level_reward(hm):
    """ 领取等级奖励
    """
    mm = hm.mm

    sl = Strategy(mm)
    rc, data = sl.level_reward()

    return rc, data


@level_limit
def send_gift(hm):
    """ 送礼
    """
    mm = hm.mm
    kind = hm.get_argument('kind', is_int=1)

    sl = Strategy(mm)
    rc, data = sl.send_gift(kind)

    return rc, data


@level_limit
def quick_done(hm):
    """
    快速完成任务
    """
    mm = hm.mm

    sl = Strategy(mm)
    rc, data = sl.quick_done()
    return rc, data


def help_done(hm):
    """ 去帮忙
    """
    mm = hm.mm
    task_id = hm.get_argument('task_id', is_int=1)

    if not task_id:
        return 'error_100', {}

    sl = Strategy(mm)
    rc, data = sl.help_done(task_id)
    return rc, data

