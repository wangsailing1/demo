#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import datetime

from admin import render
from admin.decorators import require_permission
from models.server import ServerConfig
from lib.db import get_redis_client
from lib.core.environ import ModelManager
from lib.utils.online_user import get_all_server_recent_online_info
from gconfig import game_config
from models.user import OnlineUsers
from models.payment import Payment
from tools.user import user_info
import settings


@require_permission
def select(req):
    """

    :param req:
    :return:
    """

    result = {}
    cur_uid_per_server = {}
    redis_server_memory_info = {}       # redis使用率
    cur_online_uids = 0                 # 当前在线
    today_online_users_count = 0        # 今日登录
    formatter = '%F %T'
    today = datetime.datetime.now()
    sc = ServerConfig.get()

    for server_info in sc.server_list(ignore_master_public=False):
        server = server_info['server']
        mm = ModelManager('%s1234567' % server)

        regist_users = mm.get_obj_tools('regist_users')
        online_users = mm.get_obj_tools('online_users')
        online_user_count = online_users.get_online_user_count()

        # # 同一个redis db 对应多个服 注册总数和激活总数合并
        # cur_db_data = settings.get_same_redis_db_server(server)
        # all_regist_num = sum([regist_users.get_all_regist_count(server_id) for server_id in cur_db_data])
        # all_online_num = sum([online_users.get_all_online_count(server_id) for server_id in cur_db_data])

        today_online = online_users.get_user_count_by_active_days(active_days=-1)
        open_time = datetime.datetime.fromtimestamp(server_info['open_time'])
        redis_used_memory, per_port_used, redis_used_memory_byte = ServerConfig.get_redis_userd_memory(server_info['server'])
        cur_uid_per_server[server] = {
            'user_count': online_user_count,
            'pay_rmb': 0,
            'pay_users': set(),
            'server_name': server_info['server_name'],
            'open_time': open_time.strftime('%F %T'),
            'open_days': (today.date() - open_time.date()).days + 1,
            'newbie_count': regist_users.get_today_new_uids(only_count=True),
            'server_user_count': regist_users.get_all_regist_count(),
            'real_server_user_count': online_users.get_all_online_count(),
            # 'all_server_user_count': all_regist_num,
            # 'all_real_server_user_count': all_online_num,
            'today_online': today_online,
            'redis_used_memory': redis_used_memory,
            'redis_used_memory_byte': redis_used_memory_byte,
            'config_type': game_config.get_config_type(server),
        }

        # redis使用率
        for ip, info in per_port_used.iteritems():
            if ip not in redis_server_memory_info:
                redis_server_memory_info[ip] = info
                continue
            for port, used_memory in info.iteritems():
                if port not in redis_server_memory_info[ip]:
                    redis_server_memory_info[ip][port] = used_memory

        cur_online_uids += online_user_count
        today_online_users_count += today_online

    # 计算同一个redis db 对应多个服 注册总数和激活总数合并
    for k, v in cur_uid_per_server.iteritems():
        cur_db_data = settings.get_same_redis_db_server(k)
        all_server_user_count = 0
        all_real_server_user_count = 0
        for i in cur_db_data:
            if i in cur_uid_per_server:
                all_server_user_count += cur_uid_per_server[i]['server_user_count']
                all_real_server_user_count += cur_uid_per_server[i]['real_server_user_count']
        v['all_server_user_count'] = all_server_user_count
        v['all_real_server_user_count'] = all_real_server_user_count

    # 充值
    user_pay = {}
    user_money = {}         # 原始货币
    big_brother_uid = ''
    big_brother_pay = 0
    big_brother_server = ''
    s_dt = today.date().strftime(formatter)
    e_dt = today.strftime(formatter)
    filter_admin_pay = settings.FILTER_ADMIN_PAY
    payment = Payment()
    charge_config = game_config.charge
    for x in payment.find_by_time(s_dt, e_dt):
        if filter_admin_pay and 'admin_test' in x['platform']:
            continue
        if str(x['order_id']).startswith('test'):
            continue
        x['pay_rmb'] = charge_config.get(x['product_id'], {}).get('price_%s' % settings.get_admin_charge(settings.CURRENCY_TYPE), 0) * 1
        server_id = x['user_id'][:-7]
        if server_id in cur_uid_per_server:
            cur_uid_per_server[server_id]['pay_rmb'] += x['pay_rmb']
            cur_uid_per_server[server_id]['order_money'] += x['order_money']
            cur_uid_per_server[server_id]['pay_users'].add(x['user_id'])
        else:
            cur_uid_per_server[server_id] = {'pay_rmb': x['pay_rmb'], 'user_count': 0, 'pay_users': set(x['user_id'])}
        if x['user_id'] in user_pay:
            user_pay[x['user_id']] += x['pay_rmb']
            user_money[x['user_id']] += x['order_money']
        else:
            user_pay[x['user_id']] = x['pay_rmb']
            user_money[x['user_id']] = x['order_money']

    if user_pay:
        big_brother_uid, big_brother_pay = max(user_pay.iteritems(), key=lambda x:x[1])
        big_brother_server = cur_uid_per_server.get(big_brother_uid[:-7], {}).get('server_name', big_brother_server)

    recent_online_info = get_all_server_recent_online_info()
    result['recent_online_info'] = recent_online_info
    result['cur_uid_per_server'] = cur_uid_per_server
    result['today_online_users_count'] = today_online_users_count
    result['redis_server_memory_info'] = redis_server_memory_info
    result['ONLINE_USERS_TIME_RANGE'] = OnlineUsers.ONLINE_USERS_TIME_RANGE
    result['cur_online_uids'] = cur_online_uids
    result['today'] = today.strftime('%F')
    result['now'] = today.strftime(formatter)
    result['currency_type'] = settings.CURRENCY_TYPE

    result['user_pay'] = user_pay
    result['user_money'] = user_money
    result['pay_top_server'] = 0
    result['big_brother_uid'] = big_brother_uid
    result['big_brother_pay'] = big_brother_pay
    result['big_brother_server'] = big_brother_server
    result['big_brother_pay_money'] = user_money[big_brother_uid]

    # celery queue size
    celery_redis = get_redis_client(settings.celery_config)
    result['celey_queue_size'] = celery_redis.llen('celery')
    return render(req, 'admin/server_overview/index.html', **result)


def server_online_user(req):
    """
    当前 5 分钟在线
    :param req:
    """
    online_uids = []
    sc = ServerConfig.get()
    for i in sc.server_list():
        server_id = i['server']
        mm = ModelManager("%s1234567" % server_id)
        online_users = mm.get_obj_tools('online_users')
        online_uids.extend(online_users.get_online_uids())

    page_size = 50
    page = abs(int(req.get_argument('page', 1))) or 1

    div, mod = divmod(len(online_uids), page_size)
    pages = div + 1 if mod else div
    if page > pages:
        page = pages
    uids = online_uids[(page - 1) * page_size:page * page_size]

    users = []
    for uid, _t in uids:
        mm = ModelManager(uid)
        users.append(user_info(mm))
    r = {
        'online_uids': online_uids,
        'cur_page_uids': uids,
        'cur_page': page,
        'pages': pages,
        'pre_page': max(page - 1, 0),
        'next_page': min(page + 1, pages),
        'users': users,
    }
    return render(req, 'admin/server_overview/online_users.html', **r)

