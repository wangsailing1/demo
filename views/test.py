# -*- coding: utf-8 –*-

"""
Created on 2017-06-29

@author: sm
"""

from logics.user import UserLogic
from lib.core.environ import ModelManager
from lib.toCpp.interface import lua_battle
from gconfig import game_config
from lib.utils.time_tools import timestamp_cache

def test_ok(hm):
    return 0, {}


def test_mail(hm):
    1 / 0
    return 0, {}


def test_return_error(hm):
    return 0, 0


def check_config_mapping(hm):
    """查看配置中间转换mapping状态"""
    name = hm.get_argument('name', '')
    return 0, {'name': getattr(game_config, name)}


def check_time_lru(hm):
    return 0, {'timestamp_cache': timestamp_cache.cache}


