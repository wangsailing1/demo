#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
import datetime

from admin import render
from admin.decorators import require_permission
from models.server import ServerConfig
from lib.statistics import data_analysis
from lib.toCpp import check_slg_status
from gconfig import game_config
from settings import get_channel_name
from models.ranking_list import WorldBossRank
import settings


limit_days = 30


@require_permission
def data_index(req, field='statistics', msg='', **kwargs):
    """数据查看首页
    :param req:
    :param field:
    :param msg:
    """

    default = {
        'msg': msg,
        'user': None,
        'field': field,
        'get_channel_name': get_channel_name
    }
    default.update(kwargs)
    return render(req, 'admin/data/%s_index.html' % field, **default)

@require_permission
def statistics_index(req, channel_data=None, select_server=None, select_day=None):
    """用户数据分析页面
    """
    from lib.utils import time_tools

    for_account = bool(req.get_argument('for_account', ''))
    only_channel = req.get_argument('channel', '')
    field = 'statistics' if not for_account else 'statistics_for_account'
    if only_channel:
        field = 'statistics_only_%s' % only_channel
    channel_data = channel_data if channel_data is not None else {}
    today = datetime.datetime.today()
    day_interval = ((today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                    for i in xrange(0, limit_days + 1))
    show_all = int(req.get_argument('show_all', 0))
    # open_days = 31
    # if show_all:
    #     open_days = game_config.get_server_open_days(settings.SERVER_PREFIX+'1')
    statistics_data = {}
    for day in day_interval:
        data = data_analysis.get_statistics_by_day(day, today, for_account=for_account)
        if data:
            statistics_data[day] = data

    # 单渠道统计
    select_channel_id = 'huawei'
    select_one_end_day = time_tools.strftimestamp(time.time(), '%Y-%m-%d')
    one_channel_data, channel_ids = data_analysis.get_statistics_channel_by_day_for_one(select_channel_id,
                                                                                            select_one_end_day)
    sc = ServerConfig.get()

    html_data = {
        'statistics_data'   : statistics_data,
        'channel_data'      : channel_data,
        'select_server'     : select_server,
        'select_day'        : select_day,
        'sc': sc,
        # 单渠道
        'one_channel_data'  : one_channel_data,
        'channel_ids'       : channel_ids,
        'select_channel_id' : select_channel_id,
        'select_one_end_day': select_one_end_day,
        'show_all'          : 'checked=checked' if show_all else '',
        'show_all2'         : show_all,
    }

    return data_index(req, field=field, **html_data)

@require_permission
def statistics_index_account(req):
    """
    用户数据分析页面
    :param req:
    :return:
    """
    req.request.arguments['for_account'] = ['1']
    return statistics_index(req)

@require_permission
def statistics_channel(req):
    """渠道统计
    """
    select_server = req.get_argument('server_id', '00')
    select_day = req.get_argument('day')
    for_account = bool(req.get_argument('for_account', ''))

    channel_data = data_analysis.get_statistics_channel_by_day(select_day, for_account=for_account)
    if for_account:
        server_channel_data = channel_data
    else:
        server_channel_data = channel_data.get(select_server, {}) if channel_data else {}
    # print channel_data
    return statistics_index(req, channel_data=server_channel_data,
                            select_server=select_server, select_day=select_day)

@require_permission
def retention_index(req, select_server='', select_day='', ip_data=''):
    """
    留存统计
    """
    for_account = bool(req.get_argument('for_account', ''))
    for_device = bool(req.get_argument('for_device', ''))
    for_ip = bool(req.get_argument('for_ip', ''))
    if for_account and ip_data and for_ip:
        field = 'retention_for_account_ip_data'
    elif for_account:
        field = 'retention_for_account'
    elif for_device:
        field = 'retention_for_device'
    else:
        field = 'retention'

    if select_day:
        day_channel_data = data_analysis.get_retention_channel_by_day(select_day, for_account=for_account, for_device=for_device)
        # print 'day_channel_data:', day_channel_data             # debug_flag
        if for_account and for_ip:
            channel_data = data_analysis.get_retention_channel_by_day_and_ip(select_day)
        elif for_account:
            channel_data = day_channel_data
        elif select_server:
            channel_data = day_channel_data.get(select_server, {}) if day_channel_data else {}
    else:
        channel_data = {}

    retention_data = data_analysis.get_retention_data(days=limit_days, for_account=for_account, for_device=for_device)
    rate_data = {}
    channel_rate_data = {}
    rate_days = (2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 30)
    day_keys = sorted(retention_data.iterkeys())
    days_delta = []
    if day_keys:
        datetime_strptime = datetime.datetime.strptime
        first_date = datetime_strptime(day_keys[0], '%Y-%m-%d')
        for day in day_keys:
            delta = (datetime_strptime(day, '%Y-%m-%d')-first_date).days
            days_delta.append(delta+1)
            value = retention_data[day]
            temp = {}
            first = value.get(1, 1)
            for dd in rate_days:
                temp[dd] = round(value.get(dd, 0) * 100.0 / first, 2)
            rate_data[day] = temp
        # for channel, data in channel_data.iteritems():
        #     pass

    sc = ServerConfig.get()

    html_data = {
        'day_keys': day_keys,
        'days_delta': days_delta,
        'retention_data': retention_data,
        'rate_data': rate_data,
        'rate_days': rate_days,
        'channel_data': channel_data,
        'channel_rate_data': channel_rate_data,
        'select_server': select_server,
        'select_day': select_day,
        'sc': sc,
    }

    return data_index(req, field=field, **html_data)

@require_permission
def retention_ip(req):
    """分区域留存统计
    """
    select_day = req.get_argument('day')
    return retention_index(req, select_day=select_day, ip_data='ip_data')

@require_permission
def retention_index_account(req):
    """

    :param req:
    :return:
    """
    req.request.arguments['for_account'] = ['1']
    return retention_index(req)


@require_permission
def retention_index_device(req):
    """

    :param req:
    :return:
    """
    req.request.arguments['for_device'] = ['1']
    return retention_index(req)


@require_permission
def retention_channel(req):
    """分渠道留存统计
    """
    select_server = req.get_argument('server_id', '00')
    select_day = req.get_argument('day', None)

    return retention_index(req, select_server=select_server, select_day=select_day)


@require_permission
def statistics_channel_for_one(req):
    """单渠道统计
    """
    select_channel_id = req.get_argument('channel_id', '')
    select_one_end_day = req.get_argument('one_end_day')

    one_channel_data, channel_ids = data_analysis.get_statistics_channel_by_day_for_one(select_channel_id, select_one_end_day)
    return statistics_index_for_one(
        req,
        one_channel_data=one_channel_data,
        channel_ids=channel_ids,
        select_channel_id=select_channel_id,
        select_one_end_day=select_one_end_day
    )


@require_permission
def statistics_index_for_one(req, channel_data=None, select_server=None,
                             select_start_day=None, select_end_day=None,
                             select_channel_id=None, select_one_end_day=None,
                             one_channel_data=None, channel_ids=None):
    """用户数据统计 单渠道
    """
    field = 'statistics_for_account'
    show_all = int(req.get_argument('show_all', 0))
    channel_data = channel_data if channel_data is not None else {}
    today = datetime.datetime.today()
    open_days = limit_days + 1
    if show_all:
        open_days = game_config.get_server_open_days(settings.SERVER_PREFIX + '1')
    day_interval = ((today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                    for i in xrange(0, open_days))

    statistics_data = {}
    for day in day_interval:
        data = data_analysis.get_statistics_by_day(day, today, for_account=True)
        if data:
            statistics_data[day] = data

    sc = ServerConfig.get()
    html_data = {
        'statistics_data': statistics_data,
        'channel_data': channel_data,
        'select_server': select_server,
        'select_start_day': select_start_day,
        'select_end_day': select_end_day,
        'one_channel_data': one_channel_data,
        'channel_ids': channel_ids,
        'select_channel_id': select_channel_id,
        'select_one_end_day': select_one_end_day,
        'sc': sc,
        'show_all': 'checked=checked' if show_all else '',
        'show_all2': show_all,
        'select_day': select_start_day,
        'end_day': None,
    }

    return data_index(req, field=field, **html_data)


@require_permission
def lv_pass_rate_index(req):
    """
    等级滞留统计
    :param req:
    :return:
    """
    selected_server = req.get_argument('selected_server', 'all')
    all_servers = {'all': u'所有服总量'}
    sc = ServerConfig.get()
    for server_name, server_info in sc.yield_open_servers():
        all_servers[server_name] = server_info['name']
    lv_pass_rate = data_analysis.get_lv_pass_rate_from_cache()
    data = {
        'lv_pass_rate': lv_pass_rate,
        'selected_server': selected_server,
        'all_servers': all_servers,
    }
    return render(req, 'admin/data/lv_pass_rate.html', **data)


@require_permission
def world_boss_rank_show(req):
    """
    世界BOSS排行榜
    :param req:
    :return:
    """
    rank_infos = {}
    selected_server = req.get_argument('selected_server', '')
    selected_date = req.get_argument('selected_date', '')
    if selected_date == "":
        selected_date = datetime.datetime.now().strftime('%F')
    if selected_server:
        for boss_id, config in game_config.worldboss_boss.iteritems():
            version = selected_date + '_' + str(boss_id)
            rank_boss = WorldBossRank(uid=boss_id, server=selected_server, version=version)
            key = rank_boss.backup_key()
            rank_infos[boss_id] = rank_boss.fredis.zrevrange(key, 0, 100, withscores=True)
        rank_infos = sorted(rank_infos.items(), key=lambda x: x[0])
    data = {
        'rank_infos': rank_infos,
        'server': selected_server,
        'date': selected_date,
    }
    return render(req, 'admin/data/world_boss_rank_show.html', **data)

@require_permission
def slg_status(req):
    data = []
    for k, v in settings.SLG_REQUESTRUN.iteritems():
        rc, status = check_slg_status(k)
        if not rc:
            data.append(status)
    return render(req, 'admin/data/slg_status.html', **{'data': data})
