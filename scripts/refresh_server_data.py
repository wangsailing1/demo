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
func_name = sys.argv[2]
settings.set_env(env)

from models.server import ServerConfig
from lib.core.environ import ModelManager


def all_server_iter():
    """获取区服列表
    """
    servers = ServerConfig.get().server_list()

    for srv in servers:
        server_id = srv['server']
        if server_id in ['master', 'public']:
            continue
        yield server_id


def clear_private_city_daily_rank(server_id):
    """
    清空每日通关排行榜旧数据
    :param uid:
    :return:
    """
    if not settings.is_father_server(server_id):
        return

    mm = ModelManager('%s1234567' % server_id)
    k = mm.private_city.get_stage_rank_key()
    r = mm.private_city.redis
    r.delete(k)
    return server_id


if __name__ == "__main__":
    func = globals().get(func_name)
    if not func:
        print 'error func name'
    else:
        for server in all_server_iter():
            print clear_private_city_daily_rank(server)
