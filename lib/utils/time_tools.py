#!/usr/bin/python
# encoding: utf-8

import time
import datetime as datetime_module
from gconfig import game_config
import settings
from models import server as serverM


timestamp_cache = {}


def str2timestamp(time_str, fmt='%Y-%m-%d %H:%M:%S'):
    """字符串转成时间戳
    :param time_str:
    :param fmt:
    """
    if time_str in timestamp_cache:
        ts = timestamp_cache[time_str]
    else:
        ts = timestamp_cache[time_str] = time.mktime(time.strptime(time_str, fmt))
    return ts


def datetime(year, month, day, hour, minute, second):
    """# timestamp_from_date: 根据给的时间生成datetime对象
    args:
        year, month, day, hour, minute, second:    ---    arg
    returns:
        0    ---    
    """
    datetime_module.datetime(year, month, day, hour, minute, second)


def datetime_from_timestamp(timestamp):
    """# datetime_from_timestamp: docstring
    args:
        timestamp:    ---    arg
    returns:
        0    ---    
    """
    return datetime_module.datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(datetime_obj):
    """# datetime_to_timestamp: docstring
    args:
        datetime_obj:    ---    arg
    returns:
        0    ---    
    """
    return time.mktime(datetime_obj.timetuple())


def timestamp_from_deltadaytime(datetime_obj, delta_day_int, hour, minute, second):
    """# timestamp_from_deltadaytime: 指定
    args:
        ll:    ---    arg
    returns:
        0    ---    
    """
    delta_day = datetime_module.timedelta(delta_day_int, 0, 0)
    dt = datetime_obj + delta_day
    dt_new = datetime_module.datetime(
        dt.year,
        dt.month,
        dt.day,
        hour,
        minute,
        second
    )
    return datetime_to_timestamp(dt_new)


def timestamp_from_deltamonthtime(datetime_obj, month_delta, month_day, hour, minute, second):
    """# timestamp_from_deltadaytime: 指定
    args:
        ll:    ---    arg
    returns:
        0    ---    
    """
    delta_day = datetime_module.timedelta(month_delta*30, 0, 0)
    dt = datetime_obj + delta_day
    dt_new = datetime_module.datetime(
        dt.year,
        dt.month,
        month_day,
        hour,
        minute,
        second
    )
    return datetime_to_timestamp(dt_new)


def dt2timestamp(dt):
    """转换日期时间对象到时间戳
    Args:
        dt: datetime.datetime()对象
    Returns:
        时间戳
    """
    struct_time = dt.timetuple()
    return int(time.mktime(struct_time))


def strftimestamp(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    """转换时间戳到字符串
    Args:
        timestamp: 时间戳
        fmt: 对应的时间格式
    Returns:
        时间字符串
    """
    struct_time = time.localtime(timestamp)
    return time.strftime(fmt, struct_time)


def timestamp_now():
    """# timestamp_now: docstring
    args:
        :    ---    arg
    returns:
        0    ---    
    """
    return time.time()


def datetime_now():
    """# datetime_now: docstring
    args:
        :    ---    arg
    returns:
        0    ---    
    """
    return datetime_module.datetime.now()

SECONDS_ONE_DAY = 3600*24


def timestamp_day(t=0):
    """# timestamp_today: 获得当天0点的时间戳
    args:
        :    ---    arg
    returns:
        0    ---    
    """
    if not t:
        today = datetime_module.date.today()
        time_0 = time.mktime(today.timetuple())
    else:
        today = datetime.datetime.strptime(time.strftime('%F',time.localtime(t)), "%Y-%m-%d").timetuple()
        time_0 = time.mktime(today.timetuple())
    return time_0


def timestamp_different_days(time_1, time_2):
    """# timestamp_different_days: 计算两个时间戳相差的天数，天数不是按照24小时计算
    args:
        arg:    ---    arg
    returns:
        0    ---    
    """
    return (datetime_from_timestamp(timestamp_day(time_2)) - datetime_from_timestamp(timestamp_day(time_1))).days


FORMAT_DATE = '%Y-%m-%d %H:%M:%S'


def is_open_from_week(start_week_int, start_time_str, end_week_int, end_time_str, cur_date=None):
    """ 根据星期判断是否开启功能, 只支持7天以内

    :return int 0: 未开启
    :return int >0: 开启
    """
    cur_date = cur_date if cur_date else datetime_module.datetime.now()
    cur_time = time.mktime(cur_date.timetuple())
    cur_week = cur_date.weekday()

    start_time = datetime_module.datetime.strptime(start_time_str, '%H:%M:%S').time()
    end_time = datetime_module.datetime.strptime(end_time_str, '%H:%M:%S').time()
    start_week = start_week_int - 1
    end_week = end_week_int - 1

    if start_week < end_week:
        # 开始星期和结束星期在同一个星期里面
        if start_week < cur_week < end_week:
            # 当前星期在开始星期和结束星期中
            d_date = cur_date.date() + datetime_module.timedelta(days=end_week - cur_week)
            open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
            return time.mktime(time.strptime(open_str, FORMAT_DATE))
        elif start_week == cur_week and start_time < cur_date.time():
            d_date = cur_date.date() + datetime_module.timedelta(days=end_week - cur_week)
            open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
            return time.mktime(time.strptime(open_str, FORMAT_DATE))
        elif end_week == cur_week and end_time > cur_date.time():
            d_date = cur_date.date()
            open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
            return time.mktime(time.strptime(open_str, FORMAT_DATE))
        else:
            return 0
    elif start_week == end_week:
        # 开始星期和结束星期在同一星期或者不在同一星期
        if start_time < end_time:
            # 同一个星期
            if start_week == cur_week and start_time < cur_date.time() < end_time:
                d_date = cur_date.date()
                open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
                return time.mktime(time.strptime(open_str, FORMAT_DATE))
            else:
                return 0
        elif start_time > end_time:
            # 不同星期
            if start_week == cur_week and end_time < cur_date.time() < start_time:
                return 0
            else:
                d_date = cur_date.date() + datetime_module.timedelta(days=7)
                open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
                return time.mktime(time.strptime(open_str, FORMAT_DATE))
        else:
            # 数据有问题
            return 0
    else:
        # 开始星期和结束星期不在同一个星期里面
        if start_week < cur_week:
            # 开始星期大于当前星期
            d_date = cur_date.date() + datetime_module.timedelta(days=7 - cur_week + end_week)
            open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
            return time.mktime(time.strptime(open_str, FORMAT_DATE))
        elif start_week == cur_week:
            if start_time < cur_date.time():
                d_date = cur_date.date() + datetime_module.timedelta(days=7 - cur_week + end_week)
                open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
                return time.mktime(time.strptime(open_str, FORMAT_DATE))
            else:
                return 0
        elif cur_week < end_week:
            # 当前星期小于结束日期
            d_date = cur_date.date() + datetime_module.timedelta(days=end_week - cur_week)
            open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
            return time.mktime(time.strptime(open_str, FORMAT_DATE))
        elif cur_week == end_week:
            if end_time > cur_date.time():
                d_date = cur_date.date()
                open_str = '%s-%s-%s %s' % (d_date.year, d_date.month, d_date.day, end_time_str)
                return time.mktime(time.strptime(open_str, FORMAT_DATE))
            else:
                return 0
        else:
            return 0


def timestamp_from_relative_time(server_open_time, relative_time):
    """ 根据服务器开启时间和相对时间，计算绝对时间

    args：
        server_open_time: 服务器开启时间，timestamp格式，如1406090351
        relative_time：格式为字符串'1 00:00'，意思是服务器开启后第一天的00:00，如服务器是25日开启，则'1 00:00'为25日00：00
    return：
        绝对时间的时间戳
    """
    relative_time = relative_time if relative_time else '1 00:00:00'
    server_open_date = datetime_module.date.fromtimestamp(server_open_time)
    relative_days, abs_time = relative_time.split() # '1 00:00'拆开成'1'和'00:00'分别存入relative_days, abs_time
    hour, minite, second = abs_time.split(':')
    abs_date = server_open_date + datetime_module.timedelta(days=int(relative_days)-1)
    abs_datetime = datetime_module.datetime.combine(abs_date, datetime_module.time(int(hour), int(minite), int(second)))
    return datetime_to_timestamp(abs_datetime)


def relative_activity_remain_time(server_open_time, start_time, end_time, now=None):
    """ 根据活动开始时间和结束时间计算距离活动结束还有多久

    args:
        server_open_time: 服务器开启时间，timestamp格式，如1406090351
        start_time: 活动开始时间，格式为字符串'1 00:00'，意思是服务器开启后第一天的00:00，如服务器是25日开启，则'1 00:00'为25日00：00
        end_time:   活动结束时间，格式同start_time
        now:        当前时间，若未传入则取当前时间
    return:      
        离活动结束还有多久，格式为timestamp，若当前时间不在活动时间范围内，则返回0
    """
    now =  now if now else time.time()
    start_timestamp =  timestamp_from_relative_time(server_open_time, start_time)
    end_timestamp = timestamp_from_relative_time(server_open_time, end_time)
    if start_timestamp <=  now <= end_timestamp:
        return end_timestamp - now
    else:
        return 0


def relative_config_remain_time(server_open_time, config_relative_time, now=None):
    """ 根据配置定义的相对时间段返回活动剩余时间

    args:
        server_open_time: 服务器开启时间，timestamp格式，如1406090351
        config_relative_time：活动时间段，格式形如'1 00:00-2 00:00,3 00:00-4 00:00'，每一段为相对于开服时间的开始和结束时间，可以为多段
    return:
        离活动结束还有多久，格式为timestamp，若当前时间不在活动时间范围内，则返回0。
    """
    now =  now if now else time.time()
    for atime in config_relative_time.split(','):
        # print atime, 11111111111111
        start_time, end_time = atime.strip().split('-')
        remain_time = relative_activity_remain_time(server_open_time, start_time, end_time, now)
        if remain_time: 
            return remain_time

    return 0


def get_server_activity_time(config_id, server_id, now=None):
    """ 根据新服活动配置id读取活动开始和结束的时间 
    """
    now = now if now else time.time()
    server_open_time = serverM.get_server_config(server_id).get('open_time')
    config_relative_time = game_config.server_inreview.get(config_id, {}).get('name', '')
    if server_open_time is None or server_open_time <= 0 or config_relative_time == '':
        return 0, 0
    if not game_config.server_inreview.get(config_id, {}).get('is_open', 0):
        return 0, 0
    for atime in config_relative_time.split(','):
        start_time, end_time = atime.strip().split('-')
        start_timestamp = timestamp_from_relative_time(server_open_time, start_time)
        end_timestamp = timestamp_from_relative_time(server_open_time, end_time)
        if start_timestamp <= now <= end_timestamp:
            return start_timestamp, end_timestamp

    return 0, 0


def trans_relative_to_active_time(config_id, server_id, now=None):
    """ 根据新服活动配置id读取活动开始和结束的时间 
    """
    now =  now if now else time.time()
    server_open_time = serverM.get_server_config(server_id).get('open_time')
    config_relative_time = game_config.server_inreview.get(config_id, {}).get('name', '')
    result = []
    if server_open_time is None or server_open_time <=0 or config_relative_time == '':
        return result
    for atime in config_relative_time.split(','):
        start_time, end_time = atime.strip().split('-')
        start_timestamp = timestamp_from_relative_time(server_open_time, start_time)
        end_timestamp = timestamp_from_relative_time(server_open_time, end_time)
        result.append((start_timestamp, end_timestamp))

    return result


def trans_relative_to_version(config_id, server_id, now=None):
    """ 根据新服活动配置id读取活动版本号
    """
    now = now if now else time.time()
    server_open_time = serverM.get_server_config(server_id).get('open_time')
    config_relative_time = game_config.server_inreview.get(config_id, {}).get('name', '')
    if server_open_time is None or server_open_time <= 0 or config_relative_time == '':
        return 0
    for indx, atime in enumerate(config_relative_time.split(',')):
        start_time, end_time = atime.strip().split('-')
        start_timestamp = timestamp_from_relative_time(server_open_time, start_time)
        end_timestamp = timestamp_from_relative_time(server_open_time, end_time)
        if start_timestamp <= now <= end_timestamp:
            return indx + 1

    return 0


def analyze_config_time(config_time, time_format='%Y-%m-%d %H:%M:%S', now=None):
    """ 解析配置中的时间

    :param config_time: 2014/8/10  23:00-2014/8/11 22:00,2014/9/10 15:00-2014/9/12 23:00
    :return:
    """
    if not config_time:
        return 0

    now = now or time.time()
    start_and_end_time = config_time.split(',')
    for s in start_and_end_time:
        start_time, end_time = s.split('-')
        start_timestamp = time.mktime(time.strptime(start_time, time_format))
        end_timestamp = time.mktime(time.strptime(end_time, time_format))
        if start_timestamp <= now < end_timestamp:
            return int(end_timestamp - now)

    return 0


def server_active_inreview_open_and_close(mm):
    """新服活动开关及剩余活动时间"""
    server_inreview = {}
    active_remain_time = {}
    server_inreview_config = game_config.server_inreview
    if not server_inreview_config:
        return server_inreview, active_remain_time
    if not mm.user.new_server():
        return server_inreview, active_remain_time
    now = int(time.time())
    for k in server_inreview_config:
        s_time, e_time = get_server_activity_time(k, mm.user._server_name)
        if server_inreview_config[k]['is_open'] == 2 and s_time <= now <= e_time:
            server_inreview[k] = 1
            active_remain_time[k] = e_time
    return server_inreview, active_remain_time


def get_server_days(server_id):
    server_open_time = serverM.get_server_config(server_id).get('open_time')
    now = int(time.time())
    return timestamp_different_days(server_open_time, now) + 1