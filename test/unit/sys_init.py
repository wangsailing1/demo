#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
sys.path.insert(0, '../..')
import settings
server_name = '1'
settings.set_env('song', server_name)
settings.DEBUG = False
