#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
import datetime
import pickle
from collections import defaultdict

import settings
from gconfig import game_config
from lib.db import ModelTools, get_redis_client
from models.server import ServerConfig
from lib.core.environ import ModelManager
from lib.utils import time_tools
from scripts.server_config.ipip import get_ip_addr
from lib.utils import encoding
from lib.utils.zip_date import dencrypt_data, encrypt_data_by_pickle
from lib.utils.time_tools import str2timestamp, strftimestamp

DATA_RETENTION_DAILY_KEY_FOR_ACCOUNT = ModelTools.make_key_cls('data_retention_daily_key_for_account', 'public')
DATA_RETENTION_CHANNEL_DAILY_KEY_FOR_ACCOUNT = ModelTools.make_key_cls('data_retention_channel_daily_key_for_account', 'public')

DATA_RETENTION_DAILY_KEY_FOR_DEVICE = ModelTools.make_key_cls('data_retention_daily_key_for_device', 'public')
DATA_RETENTION_CHANNEL_DAILY_KEY_FOR_DEVICE = ModelTools.make_key_cls('data_retention_channel_daily_key_for_device', 'public')

DATA_STATISTICS_DAILY_KEY_FOR_ACCOUNT = ModelTools.make_key_cls('data_statistics_daily_key_for_account', 'public')
DATA_STATISTICS_CHANNEL_DAILY_KEY_FOR_ACCOUNT = ModelTools.make_key_cls('data_statistics_channel_key_for_account', 'public')
DATA_RETENTION_DAILY_KEY = ModelTools.make_key_cls('data_retention_daily_key', 'public')
DATA_RETENTION_CHANNEL_DAILY_KEY = ModelTools.make_key_cls('data_retention_channel_daily_key', 'public')
DATA_STATISTICS_DAILY_KEY = ModelTools.make_key_cls('data_statistics_daily_key', 'public')
DATA_STATISTICS_CHANNEL_DAILY_KEY = ModelTools.make_key_cls('data_statistics_channel_key', 'public')
DATA_ONE_DAY_LEVEL_RANK_KEY = ModelTools.make_key_cls('data_one_day_level_rank_key', 'public')
PASS_RATE_KEY = ModelTools.make_key_cls('pass_rate_key', 'public')

DATA_PROCESS_DONE_KEY = ModelTools.make_key_cls('data_process_done_key', 'public')


def get_global_cache():
    return get_redis_client(settings.SERVERS['public']['redis'])


def set_process_done_time():
    cache = get_global_cache()
    cache.set(DATA_PROCESS_DONE_KEY, time.strftime('%F %T'))


def get_process_done_time():
    cache = get_global_cache()
    return cache.get(DATA_PROCESS_DONE_KEY) or ''


def do_data_process_hourly(now=None):
    """每小时更新后台统计数据   改为每日两次
    :param now:
    """
    now = now or datetime.datetime.now()
    # 0点后跑昨天数据
    if now.hour == 0:
        query_datetime = now - datetime.timedelta(days=1)
    else:
        query_datetime = now

    # 基于uid的统计
    all_data = get_statistics_retention_data(query_datetime)
    update_cache_statistics_data(query_datetime, all_data)
    update_cache_retention_data(query_datetime, all_data)

    # 基于account的统计
    all_data_for_account = get_statistics_retention_data_for_account(all_data)
    update_cache_statistics_data_for_account(query_datetime, all_data_for_account)
    update_cache_retention_data_for_account(query_datetime, all_data_for_account)

    # 基于设备的留存
    all_data_for_device = get_statistics_retention_data_for_account(all_data, target='device')
    update_cache_retention_data_for_account(query_datetime, all_data_for_device, tp='device')

    # # 等级通过率
    # update_lv_pass_rate_cache()
    return all_data


def get_statistics_retention_data(query_date):
    """获取后台统计需要的所有数据
    :param query_date: datetime.datetime.now()
    """
    from models.payment import Payment

    query_datestr = query_date.strftime('%Y-%m-%d')
    s_time = query_date.replace(hour=0, minute=0, second=0, microsecond=0)
    e_time = query_date.replace(hour=23, minute=59, second=59)
    now = datetime.datetime.now()

    min_score = time_tools.dt2timestamp(s_time)
    max_score = time_tools.dt2timestamp(e_time)
    now_max_score = time_tools.dt2timestamp(now.replace(hour=23, minute=59, second=59))

    s_day = s_time.strftime('%Y-%m-%d %H:%M:%S')
    e_day = e_time.strftime('%Y-%m-%d %H:%M:%S')
    pay_data = defaultdict(int)
    charge_config = game_config.charge
    payment = Payment()
    for item in payment.find_by_time(s_day, e_day):
        # 跳过测试充值的记录
        if 'admin_test' in item['platform']:
            continue
        # google_play测试账号不计入真实收入
        if item['order_id'].startswith('test'):
            continue
        # if item['user_id'] in game_config.gm_uid:
        #     continue
        # pay_data[item['user_id']] += float(item['order_money'])
        # 台湾正式服用美元计算
        pay_data[item['user_id']] += float(charge_config.get(item['product_id'], {}).get('price_%s' % settings.get_admin_charge(settings.CURRENCY_TYPE), 0))

    server_uid_data = {}
    sc = ServerConfig.get()
    for server_id, _ in sc.yield_open_servers():
        uid_data = server_uid_data.setdefault(server_id, {})
        uid_data.setdefault('regist_uids', set())
        uid_data.setdefault('login_uids', set())

        mm = ModelManager('{}1234567'.format(server_id))
        regist_rank_key = mm.get_obj_tools('regist_users').get_regist_time_key()
        online_rank_key = mm.get_obj_tools('online_users').get_online_key()
        c = ModelTools.get_redis_client(server_id)

        regist_temp = c.zrevrangebyscore(regist_rank_key, max_score, min_score)
        uid_data['regist_uids'].update(regist_temp)
        login_temp = c.zrevrangebyscore(online_rank_key, now_max_score, min_score)
        uid_data['login_uids'].update(login_temp)

    user_data = {}
    # pay_data 中已跑玩家过滤 不用每个server_id都跑
    done_uids = set()
    for server_id, uid_data in server_uid_data.iteritems():
        login_uids = uid_data['login_uids']
        regist_uids = uid_data['regist_uids']
        for uid in login_uids.union(regist_uids).union(set(pay_data.keys())):
            # if uid in game_config.gm_uid:
            #     continue
            if uid in done_uids:
                continue
            done_uids.add(uid)
            mm = ModelManager(uid)
            token = mm.user.account
            if settings.DEBUG:
                channel = 'test_admin'
            else:
                channel = token.split('_')[0] if '_' in token else ''
            channel = str(mm.user.tpid or channel)
            login_days = set(mm.user.login_days)
            # 过滤掉查询日没登陆的用户
            if query_datestr not in login_days:
                continue
            # 过滤掉测试用户
            if channel in ['']:
                continue
            user_data[uid] = {
                'server_id': mm.user._server_name,                  # 分服id
                'token': token,                                     # token
                'device': mm.user.device,                                     # device
                'channel': channel,                                 # 渠道
                'appid': mm.user.appid,                             # appid标示 区分ios与安卓
                'package_appid': mm.user.package_appid,              # 包类型 twjjwsshb
                'level': mm.user.level,                             # 等级
                'regist_time': time_tools.strftimestamp(mm.user.reg_time),     # 注册时间
                'login_days': login_days,                           # 登陆日期记录
                'pay_award_daily': mm.user_payment.daily,           # 每日充值记录
                'account_regist_time': mm.user.reg_time,            # 平台账号注册时间
            }
    return {
        'user_data': user_data,    # 用户数据
        'pay_data': pay_data,      # 支付数据
    }


def update_cache_statistics_data(query_datetime, data):
    """更新统计数据
    :param query_datetime: datetime.datetime.now()
    :param data: {
        "pay_data": {}
        "user_data": {}
    }
    """
    cache = get_global_cache()

    query_daystr = query_datetime.strftime('%Y-%m-%d')
    pay_data = data['pay_data']
    user_data = data['user_data']
    channel_result = {}

    for uid, obj in user_data.iteritems():
        server_id = obj['server_id']
        channel = obj['channel']
        login_days = obj['login_days']
        regist_day = obj['regist_time'][:10]
        pay_award_daily = obj['pay_award_daily']
        p_result = channel_result.setdefault(server_id, {}).setdefault(channel, {})
        p_result.setdefault('login_num', 0)
        p_result.setdefault('regist_num', 0)
        p_result.setdefault('uid_pay_num', 0)
        p_result.setdefault('regist_uid_pay_num', 0)
        p_result.setdefault('first_uid_pay_num', 0)
        p_result.setdefault('first_uid_pay_rmb', 0)
        p_result.setdefault('login_uid_pay_num', 0)
        p_result.setdefault('pay_rmb', 0)

        if query_daystr in login_days:
            p_result['login_num'] += 1

        if query_daystr == regist_day:
            p_result['regist_num'] += 1

        if uid in pay_data:
            pay_money = pay_data[uid]
            p_result['uid_pay_num'] += 1
            p_result['pay_rmb'] += pay_money

            if query_daystr == regist_day:
                p_result['regist_uid_pay_num'] += 1

        # 指定日期跑数据，只计算查询日期以前的数据
        pay_award_daily = {k: v for k, v in pay_award_daily.items() if k <= query_daystr}
        if len(pay_award_daily) == 1 and query_daystr in pay_award_daily and uid in pay_data:
            p_result['first_uid_pay_num'] += 1
            p_result['first_uid_pay_rmb'] += pay_money
        if len(pay_award_daily) >= 1:
            p_result['login_uid_pay_num'] += 1

    # 合并分服后的总值
    total_result = {}
    sum_result = defaultdict(int)
    for server_id, channel_data in channel_result.iteritems():
        for channel, obj in channel_data.iteritems():
            obj['pay_rate'] = round(100.0 * obj['uid_pay_num'] / (obj['login_num'] or 1), 2)
            obj['pay_arpu'] = round(1.0 * obj['pay_rmb'] / (obj['uid_pay_num'] or 1), 2)
            obj['login_arpu'] = round(1.0 * obj['pay_rmb'] / (obj['login_num'] or 1), 2)

            result = total_result.setdefault(channel, defaultdict(int))
            result['login_num'] += obj['login_num']
            result['regist_num'] += obj['regist_num']
            result['uid_pay_num'] += obj['uid_pay_num']
            result['regist_uid_pay_num'] += obj['regist_uid_pay_num']
            result['first_uid_pay_num'] += obj['first_uid_pay_num']
            result['first_uid_pay_rmb'] += obj['first_uid_pay_rmb']
            result['login_uid_pay_num'] += obj['login_uid_pay_num']
            result['pay_rmb'] += obj['pay_rmb']

            sum_result['login_num'] += obj['login_num']
            sum_result['regist_num'] += obj['regist_num']
            sum_result['uid_pay_num'] += obj['uid_pay_num']
            sum_result['regist_uid_pay_num'] += obj['regist_uid_pay_num']
            sum_result['first_uid_pay_num'] += obj['first_uid_pay_num']
            sum_result['first_uid_pay_rmb'] += obj['first_uid_pay_rmb']
            sum_result['login_uid_pay_num'] += obj['login_uid_pay_num']
            sum_result['pay_rmb'] += obj['pay_rmb']

    for channel, obj in total_result.iteritems():
        obj['pay_rate'] = round(100.0 * obj['uid_pay_num'] / (obj['login_num'] or 1), 2)
        obj['pay_arpu'] = round(1.0 * obj['pay_rmb'] / (obj['uid_pay_num'] or 1), 2)
        obj['login_arpu'] = round(1.0 * obj['pay_rmb'] / (obj['login_num'] or 1), 2)

    sum_result['pay_rate'] = round(100.0 * sum_result['uid_pay_num'] / (sum_result['login_num'] or 1), 2)
    sum_result['pay_arpu'] = round(1.0 * sum_result['pay_rmb'] / (sum_result['uid_pay_num'] or 1), 2)
    sum_result['login_arpu'] = round(1.0 * sum_result['pay_rmb'] / (sum_result['login_num'] or 1), 2)
    # 合并分服后的总值
    channel_result['00'] = total_result

    cache.hset(DATA_STATISTICS_CHANNEL_DAILY_KEY, query_daystr, encrypt_data_by_pickle(channel_result, 1))
    cache.hset(DATA_STATISTICS_DAILY_KEY, query_daystr, encrypt_data_by_pickle(sum_result, 1))

    print 'update_cache_statistics_data done at: %s' % datetime.datetime.now()


def update_cache_retention_data(query_datetime, data):
    """更新留存数据
    :param query_datetime: datetime.datetime.now()
    :param data: {
        "pay_data": {}
        "user_data": {}
    }
    """
    cache = get_global_cache()

    add_data = {}
    for uid, obj in data['user_data'].iteritems():
        server_id = obj['server_id']
        channel = obj['channel']
        login_days = obj['login_days']
        regist_day = obj['regist_time'][:10]
        temp = add_data.setdefault(regist_day, {}).setdefault(server_id, {}).setdefault(channel, {})
        for day in login_days:
            temp.setdefault(day, set()).add(uid)

    # 昨天没留存数据
    if not add_data:
        print 'update_cache_retention_data: empty add data, break'
        return

    keys = add_data.keys()
    channel_values = cache.hmget(DATA_RETENTION_CHANNEL_DAILY_KEY, keys)
    total_values = cache.hmget(DATA_RETENTION_DAILY_KEY, keys)

    channel_new_data = {}
    total_new_data = {}
    for idx, day in enumerate(keys):
        channel_value = channel_values[idx]
        channel_old_value = dencrypt_data(channel_value) if channel_value else {}

        total_vaulue = total_values[idx]
        total_old_value = dencrypt_data(total_vaulue) if total_vaulue else {}

        add_value = add_data[day]
        for server_id, server_data in add_value.iteritems():
            channel_old_value.setdefault(server_id, {})
            for channel, channel_data in server_data.iteritems():
                temp = channel_old_value[server_id].setdefault(channel, {})
                for login_day, uid_sets in channel_data.iteritems():
                    if login_day not in temp:
                        temp[login_day] = set(uid_sets)
                    else:
                        temp[login_day].update(uid_sets)
                    if login_day not in total_old_value:
                        total_old_value[login_day] = set(uid_sets)
                    else:
                        total_old_value[login_day].update(uid_sets)
        # print 'channel_old_value:', channel_old_value, '\n\ntotal_old_value:', total_old_value
        channel_new_data[day] = encrypt_data_by_pickle(channel_old_value, 1)
        total_new_data[day] = encrypt_data_by_pickle(total_old_value, 1)

    cache.hmset(DATA_RETENTION_CHANNEL_DAILY_KEY, channel_new_data)
    cache.hmset(DATA_RETENTION_DAILY_KEY, total_new_data)

    print 'update_cache_retention_data done at: %s' % datetime.datetime.now()


def get_statistics_retention_data_for_account(all_data, target='token'):
    """
    获取后台统计需要的所有数据(基于账号的)
    :param all_data: {
        "pay_data": {}
        "user_data": {}
    }
        target: token 账号| device 设备码
    """
    from lib.utils import merge_dict
    user_data = defaultdict(dict)
    for uid, data in all_data['user_data'].iteritems():
        account_data = user_data[data[target]]
        account_data['channel'] = data['channel']
        account_data['appid'] = data['appid']
        account_data['package_appid'] = data['package_appid']
        # print account_data, data['login_days']      # debug_flag
        account_data.setdefault('login_days', set()).update(data['login_days'])
        account_data.setdefault('pay_award_daily', {})
        account_data['regist_time'] = time.strftime("%F %T", time.localtime(data['account_regist_time']))
        merge_dict(account_data['pay_award_daily'], data['pay_award_daily'])

    pay_data = defaultdict(int)
    for uid, pay_money in all_data['pay_data'].iteritems():
        if uid not in all_data['user_data']:
            continue
        account = all_data['user_data'][uid]['token']
        pay_data[account] += pay_money

    return {
        'user_data': user_data,    # 用户数据
        'pay_data': pay_data,      # 支付数据
    }


def update_cache_statistics_data_for_account(query_datetime, data):
    """
    更新统计数据(基于账号的)
    :param query_datetime: datetime.datetime.now()
    :param data: {
        "pay_data": {}
        "user_data": {}
    }
    """
    cache = get_global_cache()

    query_daystr = query_datetime.strftime('%Y-%m-%d')
    pay_data = data['pay_data']
    user_data = data['user_data']
    channel_result = {}

    for uid, obj in user_data.iteritems():
        # if uid in game_config.gm_uid:
        #     continue
        # channel = obj['channel']
        login_days = obj['login_days']
        regist_day = obj['regist_time'][:10]
        pay_award_daily = obj['pay_award_daily']

        # for channel_pt in ['channel', 'appid', 'package_appid']:
        for channel_pt in ['channel']:
            if channel_pt not in obj:
                continue
            channel = obj[channel_pt]
            if not channel:
                continue

            p_result = channel_result.setdefault(channel, {})
            p_result.setdefault('login_num', 0)
            p_result.setdefault('regist_num', 0)
            p_result.setdefault('uid_pay_num', 0)
            p_result.setdefault('regist_uid_pay_num', 0)
            p_result.setdefault('first_uid_pay_num', 0)
            p_result.setdefault('first_uid_pay_rmb', 0)
            p_result.setdefault('login_uid_pay_num', 0)
            p_result.setdefault('pay_rmb', 0)

            if query_daystr in login_days:
                p_result['login_num'] += 1

            if query_daystr == regist_day:
                p_result['regist_num'] += 1

            if uid in pay_data:
                pay_money = pay_data[uid]
                p_result['uid_pay_num'] += 1
                p_result['pay_rmb'] += pay_money

                if query_daystr == regist_day:
                    p_result['regist_uid_pay_num'] += 1

            # 指定日期跑数据，只计算查询日期以前的数据
            pay_award_daily = {k: v for k, v in pay_award_daily.items() if k <= query_daystr}
            if len(pay_award_daily) == 1 and query_daystr in pay_award_daily and uid in pay_data:
                p_result['first_uid_pay_num'] += 1
                p_result['first_uid_pay_rmb'] += pay_money
            if len(pay_award_daily) >= 1:
                p_result['login_uid_pay_num'] += 1

    sum_result = defaultdict(int)
    for channel, obj in channel_result.iteritems():
        obj['pay_rate'] = round(100.0 * obj['uid_pay_num'] / (obj['login_num'] or 1), 2)
        obj['pay_arpu'] = round(1.0 * obj['pay_rmb'] / (obj['uid_pay_num'] or 1), 2)
        obj['login_arpu'] = round(1.0 * obj['pay_rmb'] / (obj['login_num'] or 1), 2)

        # IOS, Android是按手机操作系统划分,不是真实渠道,不计入汇总统计
        if channel in ['IOS', 'Android'] or any(chl in str(channel) for chl in ('twwn', 'cnwn', 'yingyongbao')):
            continue
        sum_result['login_num'] += obj['login_num']
        sum_result['regist_num'] += obj['regist_num']
        sum_result['uid_pay_num'] += obj['uid_pay_num']
        sum_result['regist_uid_pay_num'] += obj['regist_uid_pay_num']
        sum_result['first_uid_pay_num'] += obj['first_uid_pay_num']
        sum_result['first_uid_pay_rmb'] += obj['first_uid_pay_rmb']
        sum_result['login_uid_pay_num'] += obj['login_uid_pay_num']
        sum_result['pay_rmb'] += obj['pay_rmb']

    sum_result['pay_rate'] = round(100.0 * sum_result['uid_pay_num'] / (sum_result['login_num'] or 1), 2)
    sum_result['pay_arpu'] = round(1.0 * sum_result['pay_rmb'] / (sum_result['uid_pay_num'] or 1), 2)
    sum_result['login_arpu'] = round(1.0 * sum_result['pay_rmb'] / (sum_result['login_num'] or 1), 2)

    cache.hset(DATA_STATISTICS_CHANNEL_DAILY_KEY_FOR_ACCOUNT, query_daystr, encrypt_data_by_pickle(channel_result, 1))
    cache.hset(DATA_STATISTICS_DAILY_KEY_FOR_ACCOUNT, query_daystr, encrypt_data_by_pickle(sum_result, 1))

    print 'update_cache_statistics_data_for_account done at: %s' % datetime.datetime.now()
    return channel_result, sum_result


def update_cache_retention_data_for_account(query_datetime, data, tp='token'):
    """
    更新留存数据(基于账号的)
    :param query_datetime: datetime.datetime.now()
    :param data: {
        "pay_data": {}
        "user_data": {}
    }
        tp: token 账号 | device 设备码
    """
    if tp == 'token':
        channel_daily_key = DATA_RETENTION_CHANNEL_DAILY_KEY_FOR_ACCOUNT
        retention_daily_key = DATA_RETENTION_DAILY_KEY_FOR_ACCOUNT
    else:
        channel_daily_key = DATA_RETENTION_CHANNEL_DAILY_KEY_FOR_DEVICE
        retention_daily_key = DATA_RETENTION_DAILY_KEY_FOR_DEVICE

    cache = get_global_cache()

    add_data = {}
    for uid, obj in data['user_data'].iteritems():
        channel = obj['channel']
        login_days = obj['login_days']
        regist_day = obj['regist_time'][:10]
        temp = add_data.setdefault(regist_day, {}).setdefault(channel, {})
        for day in login_days:
            temp.setdefault(day, set()).add(uid)

    # 昨天没留存数据
    if not add_data:
        print 'update_cache_retention_data: empty add data, break'
        return

    keys = add_data.keys()
    channel_values = cache.hmget(channel_daily_key, keys)
    total_values = cache.hmget(retention_daily_key, keys)

    channel_new_data = {}
    total_new_data = {}
    for idx, day in enumerate(keys):
        channel_value = channel_values[idx]
        channel_old_value = dencrypt_data(channel_value) if channel_value else {}

        total_vaulue = total_values[idx]
        total_old_value = dencrypt_data(total_vaulue) if total_vaulue else {}

        add_value = add_data[day]
        # for server_id, server_data in add_value.iteritems():
            # channel_old_value.setdefault(server_id, {})
        for channel, channel_data in add_value.iteritems():
            temp = channel_old_value.setdefault(channel, {})
            for login_day, uid_sets in channel_data.iteritems():
                if login_day not in temp:
                    temp[login_day] = set(uid_sets)
                else:
                    temp[login_day].update(uid_sets)
                if login_day not in total_old_value:
                    total_old_value[login_day] = set(uid_sets)
                else:
                    total_old_value[login_day].update(uid_sets)

        channel_new_data[day] = encrypt_data_by_pickle(channel_old_value, 1)
        total_new_data[day] = encrypt_data_by_pickle(total_old_value, 1)

    cache.hmset(channel_daily_key, channel_new_data)
    cache.hmset(retention_daily_key, total_new_data)

    print 'update_cache_retention_data_for_account tp: %s done at: %s' % (tp, datetime.datetime.now())
    return channel_new_data, total_new_data


def level_pass_rate(now=None):
    """
    等级滞留率  一天跑一次
    :param now:
    :return:
    """
    # 等级通过率
    update_lv_pass_rate_cache()


def update_lv_pass_rate_cache():
    """更新等级滞留率cache
    """
    max_lv = max(game_config.player_level)

    global_cache = get_global_cache()

    result = {}
    pass_user_all = [0] * max_lv
    pass_num_all = 0
    sc = ServerConfig.get()
    for i in sc.server_list():
        server_name = i['server']
        result[server_name] = {}
        pass_user_one, pass_num_one = lv_pass_rate(server=server_name)
        pass_num_all += pass_num_one
        pass_rate_one = [0] * max_lv

        # 单个通过率计算
        for index, value in enumerate(pass_user_one):
            pass_user_all[index] += value
            if pass_num_one == 0:
                pass_rate_one[index] = 0
                continue
            pass_rate_one[index] = 1.0 * (pass_num_one - value) / pass_num_one
            pass_num_one -= value
        result[server_name]['rate'] = pass_rate_one
        result[server_name]['num'] = pass_user_one

    # 总的通过率计算
    pass_rate_all = [0] * max_lv
    for index, value in enumerate(pass_user_all):
        if pass_num_all == 0:
            pass_rate_all[index] = 0
            continue
        pass_rate_all[index] = round(1.0 * (pass_num_all - value) / pass_num_all, 2)
        pass_num_all -= value
    result['all'] = {
        'rate': pass_rate_all,
        'num': pass_user_all,
    }
    raw_data = encrypt_data_by_pickle(result, pickle.HIGHEST_PROTOCOL)
    global_cache.set(PASS_RATE_KEY, raw_data)
    print 'update_lv_pass_rate_cache done at: %s' % datetime.datetime.now()
    return result


def lv_pass_rate(server='h1'):
    """
    取出单服各级人数分布
    :param server:
    :return:
        - lv_pass_num: 等级分布列表，形如 array('l', [0, 12, 17, 5, 12]), 分别为1~max_lv的人数
        - all_uids: 全服人数
    """
    from models.ranking_list import LevelRank
    max_lv = max(game_config.player_level)
    lv_pass_num = [0] * max_lv

    rank_obj = LevelRank(uid='', server=server)
    all_user_lvs = rank_obj.get_all_user(withscores=True)
    for uid, lv in all_user_lvs:
        lv = int(lv)
        if lv > max_lv:
            continue
        lv_pass_num[lv - 1] += 1
    return lv_pass_num, len(all_user_lvs)


def get_lv_pass_rate_from_cache():
    """
    获取等级滞留率
    """
    global_cache = get_global_cache()
    result = global_cache.get(PASS_RATE_KEY)
    if result:
        return dencrypt_data(result)
    else:
        return update_lv_pass_rate_cache()


def get_statistics_by_day(day, today=None, for_account=False):
    """
    获取指定天的统计数据
    :param day:
    :param today:
    :param for_account:
    """
    cache = get_global_cache()

    today = today or datetime.datetime.now()
    key = DATA_STATISTICS_DAILY_KEY if not for_account else DATA_STATISTICS_DAILY_KEY_FOR_ACCOUNT

    if day < today.strftime('%Y-%m-%d'):
        raw_data = cache.hget(key, day)
        obj = dencrypt_data(raw_data) if raw_data else None
    else:
        raw_data = cache.hget(key, day)
        obj = dencrypt_data(raw_data) if raw_data else None

    return obj


def get_statistics_channel_by_day_for_one(select_channel_id, select_end_day):
    """
    获取日期渠道分析数据 单渠道
    :param select_channel_id:
    :param select_end_day:
    """
    cache = get_global_cache()
    key = DATA_STATISTICS_CHANNEL_DAILY_KEY_FOR_ACCOUNT

    time_stamp = time_tools.str2timestamp(select_end_day, fmt='%Y-%m-%d')
    time_datetime = time_tools.datetime_from_timestamp(time_stamp)
    day_sections = [(time_datetime - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
                    for delta in xrange(0, 30)]

    raw_data = cache.hmget(key, day_sections)
    # raw_data = cache.hget(key, select_start_day)
    obj_list = []
    for d in raw_data:
        obj = dencrypt_data(d) if d else None
        obj_list.append(obj)

    result = {}
    channel_ids = set()
    for index, obj in enumerate(obj_list):
        day = day_sections[index]
        if obj:
            channel_ids.update(obj.keys())
            result[day] = obj.get(select_channel_id, {})
        else:
            result[day] = {}

    return result, list(channel_ids)


def get_statistics_channel_by_day(select_day, for_account=False):
    """
    获取日期渠道分析数据
    """
    cache = get_global_cache()
    key = DATA_STATISTICS_CHANNEL_DAILY_KEY if not for_account else DATA_STATISTICS_CHANNEL_DAILY_KEY_FOR_ACCOUNT

    raw_data = cache.hget(key, select_day)
    obj = dencrypt_data(raw_data) if raw_data else None

    return obj


def get_statistics_channel_by_range_day(start_day, end_day, for_account=False):
    """
    获取日期渠道分析数据
    """
    s_day = str2timestamp(start_day, fmt='%Y-%m-%d')
    e_day = str2timestamp(end_day, fmt='%Y-%m-%d')
    range_time = (e_day - s_day) / (3600 * 24) + 1
    cache = get_global_cache()
    key = DATA_STATISTICS_CHANNEL_DAILY_KEY if not for_account else DATA_STATISTICS_CHANNEL_DAILY_KEY_FOR_ACCOUNT
    result = {}

    for i in xrange(int(range_time)):
        cur_day = strftimestamp((s_day + i * 3600 * 24), fmt='%Y-%m-%d')
        raw_data = cache.hget(key, cur_day)
        obj = dencrypt_data(raw_data) if raw_data else {}
        for k, v in obj.iteritems():
            if result == obj:
                break
            for m, n in v.iteritems():
                if not result:
                    result = obj
                    break
                else:
                    if k not in result:
                        result.update({k: v})
                    else:
                        result[k][m] += n
        """
        付费ARPU = 付费金额/付费人数
        登陆ARPU = 付费金额/登陆用户
        付费率 = 付费人数/登陆用户
        """
        for k, v in result.iteritems():
            if 'uid_pay_num' in v:
                if v['uid_pay_num']:
                    v['pay_arpu'] = round(float(v['pay_rmb']) / v['uid_pay_num'], 2)
            if 'login_num' in v:
                if v['login_num']:
                    v['login_arpu'] = round(float(v['pay_rmb']) / v['login_num'], 2)
                    v['pay_rate'] = round(float(v['uid_pay_num']) / v['login_num'], 2)
    return result


def get_retention_channel_by_day(select_day, for_account=False, **kwargs):
    """获取分渠道留存分析数据
    """
    cache = get_global_cache()
    for_device = kwargs.get('for_device')
    if for_device:
        key = DATA_RETENTION_CHANNEL_DAILY_KEY_FOR_DEVICE
    elif for_account:
        key = DATA_RETENTION_CHANNEL_DAILY_KEY_FOR_ACCOUNT
    else:
        key = DATA_RETENTION_CHANNEL_DAILY_KEY

    raw_data = cache.hget(key, select_day)
    obj = dencrypt_data(raw_data) if raw_data else {}
    # print 'obj:', obj             # debug_flag

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    day = select_day
    day_date = datetime.datetime.strptime(day, '%Y-%m-%d')
    if not for_account:
        result = {'00': {}}
        for server_id, server_data in obj.iteritems():
            result.setdefault(server_id, {})
            for channel, data in server_data.iteritems():
                new_temp = result[server_id].setdefault(channel, {})
                all_temp = result['00'].setdefault(channel, {})
                for lday, uid_sets in data.iteritems():
                    if now_str >= lday >= day:
                        lday_date = datetime.datetime.strptime(lday, '%Y-%m-%d')
                        delta = (lday_date - day_date).days
                        new_temp[delta+1] = len(uid_sets)
                        all_temp[delta+1] = all_temp.get(delta+1, 0) + len(uid_sets)
    else:
        result = {}
        for channel, data in obj.iteritems():
            new_temp = result.setdefault(channel, {})
            for lday, uid_sets in data.iteritems():
                if now_str >= lday >= day:
                    lday_date = datetime.datetime.strptime(lday, '%Y-%m-%d')
                    delta = (lday_date - day_date).days
                    new_temp[delta+1] = len(uid_sets)

    return result


def get_retention_channel_by_day_and_ip(select_day, for_account=True):
    """获取分渠道留存分析数据
    """
    from models.account import Account
    from models.user import User

    cache = get_global_cache()
    key = DATA_RETENTION_CHANNEL_DAILY_KEY_FOR_ACCOUNT

    raw_data = cache.hget(key, select_day)
    obj = dencrypt_data(raw_data) if raw_data else {}

    ip_data = {}
    for channel, channel_info in obj.iteritems():
        for date, accounts in channel_info.iteritems():
            for account in accounts:
                uu = Account.get(account)
                if not uu.servers:
                    continue
                ip_data.setdefault(date, [])
                if account not in ip_data[date]:
                    ip_data[date].append(account)

    result = {}
    if not ip_data.get(select_day):
        return result
    today_login_uids = ip_data[select_day]
    day_date = datetime.datetime.strptime(select_day, '%Y-%m-%d')
    for date, accounts in ip_data.iteritems():
        for daily_account in today_login_uids:
            if daily_account in accounts and select_day <= date:
                lday_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                delta = (lday_date - day_date).days
                uu = Account.get(daily_account)
                uid = max({v: User.get(v).level for k, v in uu.servers.items()}.items(), key=lambda x: x[1])[0]
                u = User.get(uid)
                if not u.register_ip:
                    continue
                ip_addr = encoding.force_str(get_ip_addr(u.register_ip))
                # print 'uid: ', uid, ip_addr, delta
                result.setdefault(ip_addr, {})
                result[ip_addr].setdefault(delta+1, [])
                result[ip_addr][delta+1].append(daily_account)
    # 处理成天数
    for ip_addr, addr_info in result.items():
        for days, accounts in addr_info.items():
            result[ip_addr][days] = len(accounts)

    return result


def get_retention_data(days=30, for_account=False, **kwargs):
    """获取留存统计数据
    """
    cache = get_global_cache()
    for_device = kwargs.get('for_device')
    if for_device:
        key = DATA_RETENTION_DAILY_KEY_FOR_DEVICE
    elif for_account:
        key = DATA_RETENTION_DAILY_KEY_FOR_ACCOUNT
    else:
        key = DATA_RETENTION_DAILY_KEY

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    keys = [(now - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
            for delta in xrange(0, days)]
    values = cache.hmget(key, keys)
    result = {}
    for idx, day in enumerate(keys):
        day_date = datetime.datetime.strptime(day, '%Y-%m-%d')
        raw_data = values[idx]
        if raw_data:
            temp = dencrypt_data(raw_data)
            new_temp = {}
            for lday, uid_sets in temp.iteritems():
                if now_str >= lday >= day:
                    lday_date = datetime.datetime.strptime(lday, '%Y-%m-%d')
                    delta = (lday_date - day_date).days
                    new_temp[delta+1] = len(uid_sets)
            if new_temp:
                result[day] = new_temp

    return result


def save_one_day_rank_data(which_rank):
    """每日保存排行数据
    """
    cache = get_global_cache()
    sc = ServerConfig.get()
    info = {}
    info[which_rank] = {}
    cur_day = datetime.datetime.now().strftime("%Y-%m-%d")
    for server_id, _ in sc.yield_open_servers():
        mm = ModelManager('{}1234567'.format(server_id))
        rank_obj = mm.get_obj_tools(which_rank)
        ranks = rank_obj.get_all_user(0, 100 - 1, withscores=True)
        info[which_rank][server_id] = ranks

    cache.hset(DATA_ONE_DAY_LEVEL_RANK_KEY, cur_day, encrypt_data_by_pickle(info, 1))

    print 'update_cache_retention_data done at: %s' % datetime.datetime.now()


def get_one_day_rank_data(day, server, which_rank):
    """
    获取每日排行数据
    """
    cache = get_global_cache()
    key = DATA_ONE_DAY_LEVEL_RANK_KEY
    raw_data = cache.hget(key, day)
    obj = dencrypt_data(raw_data) if raw_data else {}
    result = obj.get(which_rank, {}).get(server, [])

    return result
