#!/usr/bin/env python
# coding: utf-8

"""
批量向指定 ID 的玩家發送系統郵件 - 可以帶獎勵
"""

import sys
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings

env = sys.argv[1]
filename = sys.argv[2]
ts = 0
if len(sys.argv) == 4:
    ts = sys.argv[3]
settings.set_env(env)

from models.server import ServerConfig
from models.user import RegistUsers
from lib.utils.time_tools import str2timestamp
if ts:
    if len(ts) == 8:
        ts = '%s000000'%ts
    ts = str2timestamp(ts,fmt='%Y%m%d%H%M%S')



def all_server_iter():
    """获取区服列表
    """
    servers = ServerConfig.get().server_list()

    for srv in servers:
        server_id = srv['server']
        if server_id in ['master', 'public']:
            continue
        yield server_id

def get_server_user(server_id, file_obj):
    # 所有注册用户
    regist_users = RegistUsers('', server=server_id)
    user_ids = regist_users.get_today_new_uids(t_ts=0)
    for user_id, ts in user_ids:
        file_obj.writelines(user_id + '\n')


if __name__ == "__main__":
    f = open(filename, 'w')
    for server in all_server_iter():
        get_server_user(server, f)

    f.close()
