#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from test.unit import sys_init
from lib.core.environ import ModelManager
from logics.gacha import GachaLogics
from gconfig import game_config


class GachaLogicTest(unittest.TestCase):
    def setUp(self):
        self.mm = ModelManager('gtt13629803')

    def test_pve(self):
        self.assertEqual(1, 1)
