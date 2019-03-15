#! --*-- coding: utf-8 --*--
"""
    本脚本经历数次改版，现在已经改成命令行直接执行的形式啦, 从三国同步
"""

__author__ = 'yanyunfei'

import time
import sys

from optparse import OptionParser
usage = "usage: %prog [options] arg"

parser = OptionParser(usage=usage)
parser.add_option('-p', '--destination', dest='CODE_PATH', help=u'项目路径', default='/data/sites/backend')
parser.add_option('-e', '--environment', dest='ENV_NAME', help=u'当前环境')
parser.add_option('-d', '--delete', dest='DELETE', help=u'删还是不删', default=False, action='store_true')
parser.add_option('-l', '--level', dest='LEVEL', help=u'等级,默认30', default=30, type=int)
parser.add_option('-o', '--out_days', dest='OUT_DAYS', help=u'未登录天数，默认30', default=30, type=int)
parser.add_option('-a', '--amount', dest='AMOUNT', help=u'充值金额，默认6', default=6, type=int)
parser.add_option('-s', '--servers', dest='SERVERS', help=u'服务器列表, 格式一定是m_1_10, 为金山1到10服', type='string', default=[])
(options, args) = parser.parse_args()

if not options.SERVERS:
    parser.error('服务器列表不能为空')

if not options.ENV_NAME:
    parser.error('环境不能不输入啊老铁')

if "_" not in options.SERVERS or len(options.SERVERS.split('_')) != 3:
    parser.error('服务器格式错误,应为"m_1_10"（UID_PREFIX, start_server, end_server 下划线拼接）')

CODE_PATH = options.CODE_PATH
ENV_NAME = options.ENV_NAME
DELETE = options.DELETE
LEVEL = options.LEVEL
OUT_DAYS = options.OUT_DAYS
AMOUNT = options.AMOUNT
s_tem = options.SERVERS.split('_')
SERVERS = ['%s%s' % (s_tem[0], i) for i in range(int(s_tem[1]), int(s_tem[2])+1)]

sys.path.insert(0, CODE_PATH)

import settings

settings.set_env(ENV_NAME)

from models.server import ServerConfig
from lib.core.environ import ModelManager
from models.payment import *
from models.account import Account


def get_uid_payed(amount=0):
    """
    获得充值！超过！amount的用户集合
    :param amount:
    :return:
    """
    if not amount:
        return set()

    mc = Payment()
    result = {}
    for data in mc.find_by_time('2000-01-01 00:00:00', '2099-12-31 00:00:00'):
        user_id = data['user_id']
        order_money = data['order_money']
        result[user_id] = result.get(user_id, 0) + order_money
    # print 'all_result---', result
    return {uid for uid, order_money in result.iteritems() if int(order_money) > amount}


def clear_server(server, diff_days=30, level=30, delete=False, summary=False, amount=0):
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
    # 已经删除的所有用户uid
    deleted = online_user.get_deleted_uids()
    deleted = set(deleted)
    # 所有充值用户uid
    uids_payed = get_uid_payed(amount=amount)
    print 'uids_payd---', uids_payed
    for idx, (uid, active_time) in enumerate(rs):
        # 过滤已删除或有充值记录的用户
        if uid in deleted:
            continue
        if uid in uids_payed:
            continue
        user = mm.get_mm(uid).user
        # 筛选等级
        if user.level >= level:
            continue
        # print uid, datetime.datetime.fromtimestamp(active_time)
        uids.append((uid, active_time))
        # print '=====index===', idx, len(rs)
        if not idx % 1000:
            print '============', idx, len(rs)
        keys = []
        for item, cls_instance in mm._register_base.iteritems():
            # 留着卡牌模块,在竞技场等地方还可以被人挑战
            if item in ['user']:
                continue
            if item in ['card']:
                # todo 是否需清除多余卡牌
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
            # 删除平台账号与角色uid的对应关系
            if user.account:
                uu = Account.get(user.account)
                # print uu.servers, user._server_name
                exit_uid = uu.servers.pop(user._server_name, 'Not exit')
                if exit_uid == user.uid:
                    uu.save()

            # 存储已经删除的用户的记录
            online_user.update_deleted_status(uid)

            if delte_keys:
                del_count += 1
                if settings.DEBUG:
                    print 'uid %s delete keys' % uid, delte_keys

    print 'clear_server: done', server, len(uids), uids, del_count
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


if __name__ == '__main__':
    # print options.__dict__
    # print args
    # print SERVERS
    # print get_uid_payed(AMOUNT)

    slst = SERVERS
    for server in slst:
        clear_server(server, diff_days=OUT_DAYS, level=LEVEL, delete=DELETE, amount=AMOUNT)
    # for server in slst:
    #     pass
