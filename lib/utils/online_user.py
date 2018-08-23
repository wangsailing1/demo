# -*- coding: utf-8 –*-

"""
Created on 2018-05-30

@author: sm
"""

import datetime
from lib.db import ModelBase
from lib.statistics.data_analysis import get_global_cache
from lib.core.environ import ModelManager
from models.server import ServerConfig

all_server_online_prefix = 'all_server_online_info_'
FORMAT = '%Y%m%d'


def get_online_count(server):
    mm = ModelManager('%s1234567' % server)

    online_users = mm.get_obj_tools('online_users')
    online_user_count = online_users.get_online_user_count()
    return online_user_count


def get_recent_online_info_by_server(server, today=None):
    mm = ModelManager('%s1234567' % server)
    online_users = mm.get_obj_tools('online_users')
    return online_users.get_recent_online_info(today)


def backup_all_server_online_count():
    """
    在线统计，按 时:分 为key统计
    :return:
    """
    count = 0
    sc = ServerConfig.get()
    today = datetime.datetime.today()

    for server_id, _ in sc.yield_open_servers():
        mm = ModelManager('%s1234567' % server_id)
        online_users = mm.get_obj_tools('online_users')
        online_user_count = online_users.get_online_user_count()
        # 备份每服的在线
        online_users.backup_online_user_count(online_user_count, today)
        count += online_user_count

    global_cache = get_global_cache()
    online_key = '%s%s' % (all_server_online_prefix, today.strftime(FORMAT))
    if count:
        global_cache.hset(online_key, today.strftime('%H:%M'), count)
        global_cache.expire(online_key, 24 * 3600 * 7)
    return count


def get_all_server_recent_online_info(today=None):
    """返回当天的在线统计记录
    :param date_str: eg: 20180528
    :return:
    """
    today = today or datetime.datetime.today()
    global_cache = get_global_cache()

    online_key = '%s%s' % (all_server_online_prefix, today.strftime(FORMAT))
    online_info = global_cache.hgetall(online_key)
    return online_info
