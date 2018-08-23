#! --*-- coding: utf-8 --*--

__author__ = 'sm'

"""
活跃用户
"""

import time
import datetime

from models.user import CheckinUsers
from models.server import ServerConfig
from lib.statistics.data_analysis import get_global_cache


def get_act_all_user(today=None, withscores=False):
    """ 获得昨天的活跃用户

    :param today:
    :param withscores:
    :return:
    """
    today = today.date() if today else datetime.datetime.today().date()
    yesterday = today - datetime.timedelta(days=1)
    date_str = yesterday.strftime('%Y%m%d')

    sc = ServerConfig.get()
    for server_id, server_conf in sc.yield_open_servers():
        checkin_users = CheckinUsers(server=server_id)

        active_uid = checkin_users.get_checkin_user(date_str, withscores=withscores)
        for uid in active_uid:
            yield uid

