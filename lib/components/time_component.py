#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time


def nature_time_component(model, func, time_var):
    """ 自然时间24点更新

    :param model:   模块
    :param func:    执行方法
    :param time_var: 模块中的时间属性
    :return:
    """
    time_str = getattr(model, time_var, None)
    today_str = time.strftime('%Y-%m-%d')

    if not time_str:
        # 第一次赋值
        setattr(model, time_var, today_str)
        return True

    if today_str > time_str:
        # 需要更新时间
        setattr(model, time_var, today_str)
        func()


def appoint_time_component(model, func, time_var, appoint_time):
    """ 指定时间更新

    :param model:
    :param func:
    :param time_var:
    :param appoint_time: %Y-%m-%d %H:%M:%S
    :return:
    """
    pass
