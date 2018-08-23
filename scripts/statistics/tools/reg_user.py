#! --*-- coding: utf-8 --*--

__author__ = 'sm'

"""
注册用户
"""

import time
import datetime

from models.user import RegistUsers
from models.server import ServerConfig


def get_reg_all_user(today=None, withscores=False):
    """ 获取注册用户

    :param today:
    :param withscores:
    :return: [('', 0),()]
    """
    today = today.date() if today else datetime.datetime.today().date()
    yesterday = today - datetime.timedelta(days=1)
    start_ts = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d'))) + 1
    end_ts = int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))

    sc = ServerConfig.get()
    for server_id, server_conf in sc.yield_open_servers():
        regist_users = RegistUsers(server=server_id)

        reg_uid = regist_users.get_register_count(start_ts, end_ts, withscores=withscores)
        for uid in reg_uid:
            yield uid
