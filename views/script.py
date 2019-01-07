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
    is_sequel = hm.get_argument('is_sequel', is_int=True)  # 是否续集 0 否 1 是

    sl = ScriptLogic(mm)
    rc, data = sl.filming(script_id, name, is_sequel)
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
    style = hm.get_argument('style', is_int=True)  # 剧本id

    sl = ScriptLogic(mm)
    rc, data = sl.set_style(style)
    return rc, data


def check_finished_step(hm):
    """
    拍摄结算阶段奖励
    :param hm:
    :return:
    """
    mm = hm.mm
    finished_step = hm.get_argument('finished_step', is_int=True)  # 剧本id

    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(finished_step)
    return rc, data


def finished_commmon_reward(hm):
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(1)
    return rc, data


def finished_attr_reward(hm):
    """属性结算"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(2)
    return rc, data


def finished_attention(hm):
    """关注度结算"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(3)
    return rc, data


def finished_first_income(hm):
    """首日上映"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(4)
    return rc, data


def finished_medium_judge(hm):
    """专业评价"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(5)
    return rc, data


def finished_audience_judge(hm):
    """观众评价"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(6)
    return rc, data


def finished_continue_income(hm):
    """持续上映"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(7)
    return rc, data


def finished_summary(hm):
    """票房总结"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(8)
    return rc, data


def debug_finished_summary(hm):
    """票房总结 开发测试用"""
    mm = hm.mm
    script = mm.script
    script_oid = hm.get_argument('oid')

    cur_script = script.continued_script.get(script_oid)
    if not cur_script:
        return 1, {}

    sl = ScriptLogic(mm)
    data = {}
    key = 'finished_summary'
    data[key] = cur_script[key]

    data['cur_script'] = cur_script
    data['step'] = sl.get_step()
    return 0, data


def finished_analyse(hm):
    """票房分析"""
    mm = hm.mm
    sl = ScriptLogic(mm)
    rc, data = sl.check_finished_step(9)
    return rc, data


def continued_script(hm):
    """查看持续收入阶段的电影

    :param hm:
    :return:
    """
    mm = hm.mm
    return 0, {'continued_script': mm.script.continued_script}


def upgrade_continued_level(hm):
    """

    :param hm:
    :return:
    """
    mm = hm.mm
    script_id = hm.get_argument('script_id')
    sl = ScriptLogic(mm)
    rc, data = sl.upgrade_continued_level(script_id)
    return rc, data


def get_continued_reward(hm):
    """领取持续奖励
    """
    mm = hm.mm
    script_id = hm.get_argument('script_id')
    sl = ScriptLogic(mm)
    rc, data = sl.get_continued_reward(script_id)
    return rc, data
