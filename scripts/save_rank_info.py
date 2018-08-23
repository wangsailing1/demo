#!/usr/bin/env python
# coding: utf-8

"""
 排行信息
"""

import sys
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings

env = sys.argv[1]
settings.set_env(env)

from lib.statistics.data_analysis import save_one_day_rank_data


if __name__ == '__main__':
    save_one_day_rank_data('level_rank')

