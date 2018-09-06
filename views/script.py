# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
from gconfig import game_config

from lib.db import ModelBase
from lib.utils import salt_generator
from logics.script import ScriptLogic


def index(hm):
    sl = ScriptLogic(hm.mm)
    rc, data = sl.index()
    return rc, data


def pre_filming(hm):
    """ 准备拍摄, 消耗许可证

    :param hm:
    :return:
    """
    mm = hm.mm

    sl = ScriptLogic(mm)
    rc, data = sl.pre_filming()
    return rc, data


def filming(hm):
    """
    拍片, 设置剧本名字
    :param hm:
    :return:
    """
    mm = hm.mm
    name = hm.get_argument('name')  # 名字
    script_id = hm.get_argument('script_id', is_int=True)  # 剧本id

    sl = ScriptLogic(mm)
    rc, data = sl.filming(script_id, name)
    return rc, data


def set_card(hm):
    """
    选演员上阵
    :param hm:
    :return:
    """
    mm = hm.mm
    role_card = hm.get_mapping_arguments('role_card', params_type=(int, str))

    sl = ScriptLogic(mm)
    rc, data = sl.set_card(role_card)
    return rc, data


def set_style(hm):
    """
    设置片子类型
    :param hm:
    :return:
    """
    mm = hm.mm
    style = hm.get_argument('style')  # 剧本id

    sl = ScriptLogic(mm)
    rc, data = sl.set_style(style)
    return rc, data

