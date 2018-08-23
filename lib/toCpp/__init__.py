#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import uuid
import time
import msgpack

import settings
from lib.db import get_redis_client


def check_slg_status(server_id):
    redis_server = settings.SLG_REQUESTRUN.get(str(server_id))
    # print redis_server
    if not redis_server:
        return 1, {}
    cache = get_redis_client(redis_server['redis_config'])
    _id = str(uuid.uuid1())
    request_msg = {
        'id': _id,
        'time': int(time.time()),
        'server_id': int(server_id),
        'gm': 'getServerData',
    }
    packed = msgpack.packb(request_msg)
    cache.rpush(getRealTableName("gm_cmds", server_id), packed)
    rc, SLG_RESPONE_dict = get_SLG_RESPONE(_id, server_id)
    return rc, SLG_RESPONE_dict


def get_SLG_RESPONE(_id, server_id):
    """
    获取返回值
    :param _id:
    :return:
    """
    if not settings.SLG_RESPONE:
        return -1, {}
    msg_res = get_redis_client(settings.SLG_RESPONE)
    for i in xrange(3):
        time.sleep(0.3)  # 休眠0.3秒
        user_value = msg_res.rpoplpush(getRealTableName('gm_respones', server_id), 'gm_success')
        # print 'get_respone', user_value
        while user_value:
            u = msgpack.unpackb(user_value)
            key = u.get('id')
            settings.SLG_RESPONE_MSG.update({key: u})
            user_value = msg_res.rpoplpush(getRealTableName('gm_respones', server_id), 'gm_success')
        for k in settings.SLG_RESPONE_MSG:
            if k == _id:
                if settings.SLG_RESPONE_MSG[_id]['return_state'] == 0:
                    return 0, settings.SLG_RESPONE_MSG[k]
                else:
                    return settings.SLG_RESPONE_MSG[_id]['return_state'], {}
    return -2, {}


def getRealTableName(tname, server_id):
    redis_server = settings.SLG_REQUESTRUN.get(str(server_id))
    table_prefix = redis_server.get('prefix') or settings.SLG_REDIS_TABLE_PREFIX
    return table_prefix + tname
