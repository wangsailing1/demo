#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
import os
import sys

from models.server import ServerConfig
from lib.core.environ import ModelManager


def clear_server(server, diff_days=30, level=30, delete=False, summary=False):
    """

    :param server:
    :param diff_days:
    :param level:
    :param delete:      是否直接删除各模块数据
    :param summary:     是否统计各各模块大小
    :return:
    """
    mm = ModelManager('%s1234567' % server)
    r = mm.user.redis
    online_user = mm.get_obj_tools('online_users')
    last_active_time = int(time.time()) - diff_days * 3600 * 24
    rs = r.zrangebyscore(online_user.get_online_key(), 0, last_active_time, withscores=True)
    uids = []
    del_count = 0
    per_module_size = {}
    for idx, (uid, active_time) in enumerate(rs):
        user = mm.user
        if user.vip_exp or user.level >= level:
            continue
        # print uid, datetime.datetime.fromtimestamp(active_time)
        uids.append((uid, active_time))
        # print '=====index===', idx, len(rs)
        if not idx % 1000:
            print '============', idx, len(rs)
        keys = []
        for item, cls_instance in mm._register_base.iteritems():
            # 留着卡牌模块,在竞技场等地方还可以被人挑战
            if item in ['cards']:
                continue
            # 只处理指定的模块数据
            # if item not in ['expedition', 'fivefaces']:
            #     continue
            cls_key = cls_instance.make_key_cls(uid, server)
            if summary:
                size = r.strlen(cls_key)
                if size:
                    if cls_instance in per_module_size:
                        per_module_size[cls_instance].append(size)
                    else:
                        per_module_size[cls_instance] = [size]
            keys.append(cls_key)
        # 有参与其他业务模块
        if delete:
            delte_keys = r.delete(*keys)
            if delte_keys:
                del_count += 1
                print 'uid %s delete keys' % uid, delte_keys

    print 'clear_server: done', server, len(uids), del_count
    # for a, b in per_module_size.items():
        # print a, '=======', max(b)
        # print (a, max(b))
    return per_module_size


def clear_all_sever():
    sc = ServerConfig.get()
    servers = [x[0] for x in sc.yield_open_servers()]
    all_module_size = {}
    for server in servers:
        module_size = clear_server(server, diff_days=0, level=200, summary=True)
        all_module_size[server] = module_size

    return all_module_size
