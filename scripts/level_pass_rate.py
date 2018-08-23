#!/usr/bin/env python
# coding: utf-8

"""
 等级滞留统计
"""

import sys
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings

env = sys.argv[1]
settings.set_env(env)

from lib.statistics.data_analysis import level_pass_rate


if __name__ == '__main__':
    level_pass_rate()
