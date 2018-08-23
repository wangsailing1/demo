#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import sys
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings

env = sys.argv[1]
if not env:
    exit(0)
settings.set_env(env)


def clear_server_data():
    print '-----clear_server_data start----'
    sc = ServerConfig.get()
    for server_id, _ in sc.yield_open_servers():
        mm = ModelManager('%s1234567' % server_id)
        r = mm.user.redis
        for i in r.keys():
            r.delete(i)

    master = ModelTools.get_redis_client('master')
    master_keys = master.keys()
    for i in master_keys:
        if 'models.config' in i:
            continue
        if 'game_admin' in i:
            continue
        master.delete(i)

    public = ModelTools.get_redis_client('public')
    public_keys = public.keys()
    for i in public_keys:
        if 'code' in i:
            continue
        public.delete(i)

    print '-----clear_server_data end----'

def clear_mysql_data():
    print '-----clear_mysql_data start----'
    payment = Payment()
    for table in payment.tables():
        sql = 'delete from %s' % (table)
        payment.cursor.execute(sql)
    payment.conn.commit()

    spend = Spend()
    for table in spend.tables():
        sql = 'delete from %s' % (table)
        spend.cursor.execute(sql)
        spend.conn.commit()

    print '-----clear_mysql_data end----'


if __name__ == '__main__':
    from lib.core.environ import ModelManager
    from lib.db import ModelTools
    from models.server import ServerConfig
    from models.payment import Payment
    from models.spend import Spend

    clear_server_data()
    clear_mysql_data()







