#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import os
import sys
import base64
import json
import random

# 设置程序使用的编码格式, 统一为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) == 3:
    env = sys.argv[1]
    path = sys.argv[2]
else:
    env = 'yyf'
    path = '/Users/m0005/data/superhero2/backend2/'
sys.path.insert(0, path)

import cProfile as profile
import cPickle as pickle
import settings

settings.set_env(env)

from lib.utils import zip_date
from lib.utils.change_time import debug_sync_change_time
from lib.db import *
from lib.core.environ import ModelManager

from gconfig import front_game_config as game_config
from test.test_helper import get_hm
import time
import datetime
from lib.utils import weight_choice

if settings.DEBUG:
    debug_sync_change_time()

if settings.ENV_NAME in ['song', 'dev']:
    mm = ModelManager('%s11234567' % settings.UID_PREFIX)
    mm2 = ModelManager('%s11234568' % settings.UID_PREFIX)

    c = mm.user.redis
