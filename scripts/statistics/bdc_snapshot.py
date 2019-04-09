#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os
import datetime
import time
import sys
import os

# 把当前文件父目录的父目录加入系统路径，保证从任何地方都可以调用此脚本
CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

env = sys.argv[1]

if len(sys.argv) == 3:
    arg_date = sys.argv[2]
else:
    arg_date = ''

import settings

if arg_date:
    today = datetime.datetime.strptime(arg_date, '%Y%m%d') + datetime.timedelta(days=1)
else:
    today = datetime.datetime.today()

create_day = today - datetime.timedelta(days=1)
create_date = create_day.date()
date_stamp = create_date.strftime('%Y%m%d')
create_date_str = create_date.strftime('%Y-%m-%d')


def get_bdc_real_path():
    # 本地测试用
    cur_path = os.path.abspath(os.path.dirname(__file__))
    if settings.ENV_NAME in ['song']:
        bdc_real_path = '%s/%s/bdc_snapshot' % (cur_path, settings.ENV_NAME)
    else:
        bdc_real_path = '/data/bi_data/%s/bdc_snapshot' % settings.ENV_NAME
    return bdc_real_path


def get_bdc_logger(sort, server, dbd_server_id=None):
    bdc_game_id = settings.BDC_GAME_ID

    from lib.utils.loggings import get_log, InfoLoggingUtil

    if sort not in {'userinfo', 'chargeinfo', 'eventinfo'}:
        return
    bdc_server_id = dbd_server_id or settings.get_bdc_server_id(server)
    # 105_130105010001_userinfo_2017-01-01.log
    file = '%s/%s_%s_%s_%s.log' % (get_bdc_real_path(), bdc_game_id, bdc_server_id, sort, create_date_str)
    return get_log(os.path.abspath(file), logging_class=InfoLoggingUtil, propagate=0)


def get_tpid_by_uid(uids, data_cache=None):
    """"""
    from lib.core.environ import ModelManager
    from models.user import User

    if isinstance(uids, (basestring, str)):
        uids = [uids]

    data = {}
    servers = {}
    for uid in uids:
        server = uid[:-7]
        servers.setdefault(server, []).append(uid)

    for server, server_uids in servers.iteritems():
        tpid_info = User.get_tpid_from_cache(server, server_uids)
        data.update(tpid_info)

    for uid in set(uids) - set(data):
        if data_cache and uid in data_cache:
            data[uid] = data_cache[uid]
            continue
        mm = ModelManager(uid)
        data[uid] = mm.user.tpid
        mm.user.set_tpid(mm.user.tpid)
    return {k: int(v) for k, v in data.iteritems()}


def bdc_realtime_info(today=None):
    """每小时调用一次，生成数据上传至英雄互娱ftp服务器
    """
    from lib.core.environ import ModelManager
    from lib.utils.loggings import get_log, InfoLoggingUtil
    from lib.utils.encoding import force_unicode
    from lib.utils.online_user import get_all_server_recent_online_info, get_recent_online_info_by_server

    from gconfig import game_config
    from models.payment import Payment
    from models.account import Account
    from models.server import ServerConfig
    from models.user import CheckinUsers

    FORMAT = '%F %T'
    log_day = today = today or datetime.datetime.today()
    start = today.date().strftime(FORMAT)
    end = today.strftime('%F %H:00:00')

    start_ts = int(time.mktime(today.date().timetuple()))
    end_ts = int(time.time())

    # 凌晨零点跑 取前一天的数据
    if start == end:
        today = today - datetime.timedelta(days=1)
        today = today.replace(hour=23, minute=59, second=59)
        start = today.date().strftime(FORMAT)
        end = today.strftime('%F %T')
        print start, end
        start_ts = int(time.mktime(today.date().timetuple()))
        end_ts = int(time.mktime(today.timetuple()))

    newbie_count_info = {}
    today_online_count_info = {}
    all_channels = set()

    sc = ServerConfig.get()
    cur_uid_per_server = {}

    all_servers = []
    for server_info in sc.server_list():
        server = server_info['server']
        all_servers.append(server)
        mm = ModelManager('%s1234567' % server)

        regist_users = mm.get_obj_tools('regist_users')
        # online_users = mm.get_obj_tools('online_users')
        #
        # today_online_uids = online_users.get_uids_by_active_days(active_days=-1)
        #
        checkin_users = CheckinUsers(server=server)
        today_online_uids = checkin_users.get_checkin_user(today.strftime('%Y%m%d'))

        online_user_tpids = get_tpid_by_uid(today_online_uids)
        per_server_online_info = today_online_count_info.setdefault(server, {})
        for uid, tpid in online_user_tpids.iteritems():
            per_server_online_info[tpid] = per_server_online_info.get(tpid, 0) + 1

        server_newbie_uids = regist_users.get_today_new_uids(t_ts=start_ts, end_ts=end_ts, withscores=False)

        newbie_user_tpids = get_tpid_by_uid(server_newbie_uids, online_user_tpids)
        per_server_newbie_info = newbie_count_info.setdefault(server, {})
        for uid, tpid in newbie_user_tpids.iteritems():
            per_server_newbie_info[tpid] = per_server_newbie_info.get(tpid, 0) + 1

        online_old_count_info = {}
        channels = set(online_user_tpids.values()) | set(newbie_user_tpids.values())
        for channel in channels:
            online_uids_by_channel = [k for k, v in online_user_tpids.iteritems() if v == channel]
            newbie_uids_by_channel = [k for k, v in newbie_user_tpids.iteritems() if v == channel]
            online_old_count_info[channel] = len(set(online_uids_by_channel) - set(newbie_uids_by_channel))

        all_channels |= channels
        cur_uid_per_server[server] = {
            'pay_rmb': {},
            'pay_users': {},
            'newbie_count_info': per_server_newbie_info,
            'today_online_info': per_server_online_info,
            'online_old_count_info': online_old_count_info
        }

    # 充值
    user_pay = {}
    s_dt = today.date().strftime(FORMAT)
    e_dt = today.strftime(FORMAT)
    filter_admin_pay = settings.FILTER_ADMIN_PAY

    payment = Payment()
    charge_config = game_config.charge

    tpids_cache = {}
    for x in payment.find_by_time(s_dt, e_dt):
        if filter_admin_pay and 'admin_test' in x['platform']:
            continue
        if str(x['order_id']).startswith('test'):
            continue
        x['pay_rmb'] = charge_config.get(x['product_id'], {}).get(
            'price_%s' % settings.get_admin_charge(settings.CURRENCY_TYPE), 0) * 1

        server_id = x['user_id'][:-7]
        uid = x['user_id']
        if uid in tpids_cache:
            tpid = tpids_cache[uid]
        else:
            tpid = tpids_cache[uid] = get_tpid_by_uid(uid)[uid]

        if server_id in cur_uid_per_server:
            pay_rmb_info = cur_uid_per_server[server_id]['pay_rmb']
            pay_users_info = cur_uid_per_server[server_id]['pay_users']

            pay_rmb_info[tpid] = pay_rmb_info.get(tpid, 0) + x['pay_rmb']
            pay_users_info.setdefault(tpid, set()).add(uid)
        else:
            cur_uid_per_server[server_id] = {'pay_rmb': {tpid: x['pay_rmb']},
                                             'user_count': 0,
                                             'pay_users': {tpid: {x['user_id']}}
                                             }

        if x['user_id'] in user_pay:
            user_pay[x['user_id']] += x['pay_rmb']
        else:
            user_pay[x['user_id']] = x['pay_rmb']

    bdc_real_path = get_bdc_real_path()
    bdc_game_id = settings.BDC_GAME_ID
    file = '%s/%s_%s_%s.log' % (bdc_real_path, bdc_game_id, 'realtime', log_day.strftime('%F_%H'))
    realtime_log = get_log(file, logging_class=InfoLoggingUtil, propagate=0)

    field_order = ['sid', 'cid', 'chge', 'chpe', 'logn', 'odau', 'regi', 'newr', 'newm', 'pcus', 'acus']

    # 各渠道新增设备信息
    device_info = Account.get_device_mark_count(server, today=today)
    device_channel_info = {}
    for k, v in device_info['info'].iteritems():
        info = k.split('||')
        if not len(info) == 2:
            print k, v
            continue
        _server, channel = info
        channel = int(channel)
        all_channels.add(channel)
        per_channel_info = device_channel_info.setdefault(channel, {})
        per_channel_info[_server] = per_channel_info.get(_server, 0) + int(v)

    # 各渠道新增账号信息
    account_info = Account.get_account_count(server, today=today)
    account_channel_info = {}
    for k, v in account_info['info'].iteritems():
        info = k.split('||')
        if not len(info) == 2:
            print k, v
            continue
        _server, channel = info
        channel = int(channel)
        all_channels.add(channel)
        per_channel_info = account_channel_info.setdefault(channel, {})
        per_channel_info[_server] = per_channel_info.get(_server, 0) + int(v)

    for server in all_servers:
        sid = settings.get_bdc_server_id(server)
        info = cur_uid_per_server[server]

        recent_hour_online_info = get_recent_online_info_by_server(server, today)
        # recent_hour_online_info = {k: int(v) for k, v in recent_hour_online_info.iteritems()
        #                            if k.startswith(today.strftime('%H'))}

        recent_hour_online_info = {k: int(v) for k, v in sorted(recent_hour_online_info.iteritems())[-12:]}
        if recent_hour_online_info:
            pcus = max(recent_hour_online_info.values())
            acus = sum(recent_hour_online_info.values()) / len(recent_hour_online_info)
        else:
            pcus = acus = 0

        print 'all_channels-----', server, all_channels
        for idx, channel in enumerate(all_channels):
            # 每服只一条log记录在线信息
            if idx:
                pcus = acus = 0

            per_account_info = account_channel_info.get(channel, {})
            per_device_info = device_channel_info.get(channel, {})
            per_newbie_info = info['newbie_count_info']
            cid = settings.get_bdc_channel_id(channel)

            data = {
                'sid': sid,
                'cid': cid,

                'chge': info['pay_rmb'].get(channel, 0),
                'chpe': len(info['pay_users'].get(channel, {})),

                'logn': info['today_online_info'].get(channel, 0),
                'odau': info['online_old_count_info'].get(channel, 0),
                'regi': per_account_info.get(server, 0),
                'newr': per_newbie_info.get(channel, 0),
                'newm': per_device_info.get(server, 0),

                'pcus': pcus,
                'acus': acus,
            }
            for k, v in data.items():
                print k, v

            realtime_log.info(settings.BDC_LOG_DELITIMER.join([force_unicode(data[i]) for i in field_order]))
            print settings.BDC_LOG_DELITIMER.join([force_unicode(data[i]) for i in field_order])
            print
            print
    print os.path.abspath(file)


def bdc_charge_info(today=None):
    """
    获取前一天的充值信息
    :param date:
    :return:
    """
    from models.payment import Payment, currencys
    from lib.core.environ import ModelManager
    from lib.utils.encoding import force_unicode
    from lib.statistics.bdc_event_funcs import get_anm

    today = today or datetime.datetime.today()
    query_date = today - datetime.timedelta(days=1)

    bdc_game_id = settings.BDC_GAME_ID
    bdc_version_id = settings.BDC_VERSION_ID

    query_date_str = query_date.strftime('%F')

    s_time = query_date.replace(hour=0, minute=0, second=0, microsecond=0)
    e_time = query_date.replace(hour=23, minute=59, second=59)
    # s_timestamp = datetime_to_timestamp(s_time)
    # e_timestamp = datetime_to_timestamp(e_time)
    s_day = s_time.strftime('%Y-%m-%d %H:%M:%S')
    e_day = e_time.strftime('%Y-%m-%d %H:%M:%S')
    filter_admin_pay = settings.FILTER_ADMIN_PAY

    mysql_conn = Payment()

    for item in mysql_conn.find_by_time(s_day, e_day):
        # print 'item:', item
        if filter_admin_pay and 'admin_test' in item['platform']:
            continue
        if str(item['order_id']).startswith('test'):
            continue
        user_id = item['user_id']
        mm = ModelManager(user_id)
        user = mm.user

        server_name = user._server_name
        bdc_server_id = settings.get_bdc_server_id(server_name)
        bdc_charge_log = get_bdc_logger('chargeinfo', server_name, bdc_server_id)

        order_time = item['order_time']
        bdc_channel_id = settings.get_bdc_channel_id(user.tpid)

        data = {
            'ldt': query_date_str,
            'gid': bdc_game_id,
            'cid': bdc_channel_id,
            'cpd': -1,
            'pid': bdc_version_id,
            'mac': user.device,
            'aid': user.account,
            'anm': get_anm(user.account, user.tpid, bdc_channel_id),
            'sid': bdc_server_id,
            'rid': user.uid,
            'rky': user.uid,
            'rnm': user.name,
            'rlv': user.level,
            'vip': user.vip,
            'slv': -1,
            'orid': item['order_id'],
            'type': item['product_id'],
            'amot': item['order_money'] * 100,
            # 货币类型 CNY人民币、USD美元、EUR欧元、HKD港币、GBP英镑、JPY日元、KRW韩元、CAD加元、AUD澳元、CHF瑞郎、SGD新加坡元、MYR马来西亚币、IDR印尼、NZD新西兰、VND越南、THB泰铢、PHP菲律宾
            'cury': item['currency'],
            'amoe': item['order_rmb'],  # rmb汇率
            'adid': item['order_diamond'] + item['gift_diamond'],  # 如果充值仅获得物品此处请填写-1
            'adit': '-1',  # 获得的物品数量，如果只获得钻石 此处填 -1
            'reid': '-1',  # 充值原因，没有填 -1
            'ntme': order_time,
            'rtme': order_time,
            'csta': 1,
            'chip': user.register_ip,  # TODO 充值时候ip

        }
        field_order = ['ldt', 'gid', 'cid', 'cpd', 'pid', 'mac', 'aid', 'anm', 'sid',
                       'rid', 'rky', 'rnm', 'rlv', 'vip', 'slv', 'orid', 'type', 'amot',
                       'cury', 'amoe', 'adid', 'adit', 'reid', 'ntme', 'rtme', 'csta', 'chip'
                       ]

        bdc_charge_log.info(settings.BDC_LOG_DELITIMER.join([force_unicode(data[i]) for i in field_order]))


def bdc_user_info(mm, **kwargs):
    from lib.statistics.bdc_event_funcs import get_game_base_info, BDC_EVENT_MAPPING

    user = mm.user
    base_info = get_game_base_info(user)

    context = {
        'event_id': BDC_EVENT_MAPPING['user_info'],
        'role_name': user.name,
        'role_level': user.level,
        'vip_level': user.vip,
        'sex': user.role,
        'free_diamond_balance': user.diamond_free,
        'donate_diamond_balance': 0,
        'charge_diamond_balance': user.diamond_charge,

        'phy_balance': user.action_point,
        'month_card_balance': 0,            # 月卡剩余领取次数
        'register_ip': user.register_ip,
        'accountregister_time': user.account_reg,
        'userregister_time': user.reg_time,

        'userlast_active_time': user.active_time,
        'bag_info': {},             # todo 玩家物品json格式、如果为空 填{}
        'total_charge': round(mm.user_payment.charge_price, 2),        # 累计充值金额
        'union_id': user.guild_id or 0,                      # 公会id
        'currency_info': {},                                 # 角色截止当前各类代币持有数量 json，如果为空，请填{}
    }

    context.update(base_info)

    server_name = user._server_name
    bdc_server_id = settings.get_bdc_server_id(server_name)
    bdc_info_log = get_bdc_logger('userinfo', server_name, bdc_server_id)

    bdc_info_log.info(json.dumps(context, separators=(',', ':')))
    return context


def create_zip_file(sort, today=None):
    date_str = today.strftime('%F') if today else create_date_str

    game_id = settings.BDC_GAME_ID
    path = get_bdc_real_path()
    cmd = '/usr/bin/zip -j'
    zip_file = '%s/%s_%s_%s.zip' % (path, game_id, sort, date_str)
    log_files = '%s/*%s_%s.log' % (path, sort, create_date_str)
    cmd = "%s %s %s " % (cmd, zip_file, log_files)
    print cmd
    os.system("""%s""" % cmd)


def do_snapshot():
    import traceback
    from scripts.statistics.tools import act_user
    from lib.core.environ import ModelManager

    act_uids = act_user.get_act_all_user(today=today)
    for uid in act_uids:
        try:
            mm = ModelManager(uid)
            u = mm.user
        except:
            continue

        bdc_user_info(mm)
    bdc_charge_info(today=today)

    create_zip_file('chargeinfo')
    create_zip_file('userinfo')


if __name__ == '__main__':
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-e", "--env", default='song', help="the env", type=str)
    # args = parser.parse_args()
    #
    # server_name = args.server_name
    # env = args.env
    settings.set_env(env)

    # bdc_charge_info, bdc_userinfo 每天一次
    # 直接在get_all_info.py跟着我们的bi数据一起生成，减少一些重复的数据查询

    # 这里只做每小时的实时数据生成
    bdc_realtime_info()
