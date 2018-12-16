# -*- coding: utf-8 –*-

"""
Created on 2017-06-29

@author: sm
"""

from logics.user import UserLogic
from lib.core.environ import ModelManager
from lib.toCpp.interface import lua_battle


def test_ok(hm):
    return 0, {}


def test_mail(hm):
    1 / 0
    return 0, {}


def test_return_error(hm):
    return 0, 0
