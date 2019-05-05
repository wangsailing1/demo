#!/usr/bin/python
# encoding: utf-8

__author__ = 'hougd'

import time
from gconfig import game_config
from lib.utils.debug import print_log
from lib.utils.time_tools import str2timestamp
import datetime
import settings


def active_inreview_open_and_close(active_config=None, server_type='', server_num=''):
    """
    # 获取哪个活动开启了  此方法根据active_inreview配置表写的
    :return: 返回活动的id号和显示的等级 如 {501:0, 502:45}
    """
    active_number_list = {}
    active_remain_time = {}
    active_config = active_config or game_config.active_inreview
    for active_id, config in active_config.iteritems():
        if not config:
            continue  # 此活动没有配置

        server_id = config.get('server_id')
        server_new = config.get('server_new')
        if (server_new and not (server_type and server_type == server_new)) and \
                (server_id and not (server_num and server_id[0] <= server_num <= server_id[-1])):
            continue

        if config['is_open'] <= 0:
            continue  # 此活动不能开启

        config_time = config['show_time']
        if not config_time:
            continue  # 此活动没有时间配置

        config_time = config_time.split(',')
        # config_time.reverse()  #list反转
        # 每个活动的时间点
        time_list = {}
        now = time.time()
        FORMAT = '%Y-%m-%d %H:%M:%S'
        # for id, name_config_time in enumerate(config_time):
        for name_config_time in config_time:
            if not name_config_time:
                continue
            start_time, end_time = name_config_time.split('/')
            # 字符串转成时间戳
            start_time_stamp = str2timestamp(start_time, FORMAT)
            end_time_stamp = str2timestamp(end_time, FORMAT)

            if start_time_stamp > end_time_stamp:
                return {}  # 时间的配置的不对
            if not time_list:
                time_list[active_id] = [start_time_stamp, end_time_stamp]
            elif time_list[active_id] and start_time_stamp < time_list[active_id][-1]:
                return {}  # 时间交叉
            if start_time_stamp not in time_list[active_id] and end_time_stamp not in time_list[active_id]:
                # 时间加入到list中
                time_list[active_id].append(start_time_stamp)
                time_list[active_id].append(end_time_stamp)
            if config['is_open'] == 2 and start_time_stamp <= now <= end_time_stamp:
                if active_id not in active_number_list:
                    active_number_list[active_id] = config['show_lv']  # {active_id:show_lv}
                if active_id not in active_remain_time:
                    active_remain_time[active_id] = int(end_time_stamp)
    return active_number_list, active_remain_time


def get_active_inreview_start_end_time(config, server=None, channel_id=None, config_type=None, diff_time=0):
    """
    # 获取活动的开启和结束的时间
    :param config: 配置表 如game_config.roulette
    :param server: 当前server,数字
    :return: 版本号,开始时间,结束时间
    """
    now = time.time()
    for active_id, value in config.iteritems():
        if server and value.get('server_id') and not value['server_id'][0] <= server <= value['server_id'][1]:
            return 0, 0, 0

        # 全服活动特殊判断
        no_server_id = value.get('no_server_id')
        open_channel_id = value.get('channel_id', [])
        open_server_type = value.get('server', [])
        if no_server_id:
            if (server is not None and channel_id is not None) and (
                (server in no_server_id) or (open_channel_id and channel_id not in open_channel_id)):
                # return 0, 0, 0
                continue
        else:
            if (channel_id is not None and config_type is not None) and (
                (open_server_type and config_type not in open_server_type) or (
                open_channel_id and channel_id not in open_channel_id)):
                # return 0, 0, 0
                continue

        # 判断是否上传了配置表
        if 'start_time' not in value or 'end_time' not in value:
            return 0, 0, 0
        start_time = value['start_time']
        if not start_time:
            return 0, 0, 0
        start_time_stamp = str2timestamp(start_time)
        end_time = value['end_time']
        if not end_time:
            return 0, 0, 0
        end_time_stamp = str2timestamp(end_time)
        if start_time_stamp <= now - diff_time <= end_time_stamp:
            if value.get('version', 0):
                return value['version'], start_time_stamp, end_time_stamp
            else:
                return active_id, start_time_stamp, end_time_stamp
    return 0, 0, 0


def get_active_inreview_start_end_time_diff_time(config, diff_time=0, server=None):
    """
    # 获取活动的开启和结束的时间
    :param config: 配置表 如game_config.roulette
    :return: 版本号,开始时间,结束时间
    """
    now = time.time()
    for active_id, value in config.iteritems():
        if server and value.get('server_id') and not value['server_id'][0] <= server <= value['server_id'][1]:
            return 0, 0, 0
        # 判断是否上传了配置表
        if 'start_time' not in value or 'end_time' not in value:
            return 0, 0, 0
        start_time = value['start_time']
        if not start_time:
            return 0, 0, 0
        end_time = value['end_time']
        if not end_time:
            return 0, 0, 0
        start_time_stamp = str2timestamp(start_time)
        end_time_stamp = str2timestamp(end_time)
        if start_time_stamp <= now - diff_time <= end_time_stamp:
            return value['version'], start_time_stamp, end_time_stamp
    return 0, 0, 0


def get_server_active_start_end_time(user, config, start_arg='start_time', end_arg='end_time', diff_time=0):
    """
    # 获取新服活动的开启和结束的时间   server_open_time  开服时间戳
    :param config: 配置表 如  game_config.roulette   diff_time  时间补偿
    :return: 版本号,开始时间,结束时间
    """
    _format = "%Y-%m-%d %H:%M:%S"
    now = time.time()
    server_open_time = user.server_opening_time_info().get('open_time', '')

    if int(user.config_type) != 1:
        return 0, 0, 0

    for active_id, value in config.iteritems():
        # 判断是否上传了配置表
        if start_arg not in value or end_arg not in value:
            return 0, 0, 0

        start_time = value[start_arg]
        end_time = value[end_arg]

        open_day, open_time = start_time.split(' ')
        end_day, close_time = end_time.split(' ')

        if not start_time and not end_time:
            return 0, 0, 0

        active_open_time_ = server_open_time + ' ' + open_time
        active_end_time_ = server_open_time + ' ' + close_time

        active_open_time_ = datetime.datetime.strptime(active_open_time_, _format)
        active_end_time_ = datetime.datetime.strptime(active_end_time_, _format)

        active_start_time = active_open_time_ + datetime.timedelta(days=int(open_day) - 1)
        active_end_time = active_end_time_ + datetime.timedelta(days=int(end_day) - 1)

        start_time_stamp = time.mktime(active_start_time.timetuple())

        end_time_stamp = time.mktime(active_end_time.timetuple())

        if start_time_stamp <= now - diff_time <= end_time_stamp:
            if value.get('version', 0):
                return value.get('version', 0), start_time_stamp, end_time_stamp
            else:
                # 兼容server_roulette直接把version当索引的case
                return active_id, start_time_stamp, end_time_stamp

    return 0, 0, 0


def active_inreview_start_end_time(config, format='%Y-%m-%d %H:%M:%S'):
    """
    # 获取活动的开启和结束的时间
    :param config: 配置表 如game_config.roulette
    :return: 版本号,开始时间,结束时间
    """
    now = time.time()
    for active_id, value in config.iteritems():
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time = value['start_time']
        if not start_time:
            return 0
        start_time_stamp = str2timestamp(start_time, format)
        end_time = value['end_time']
        if not end_time:
            return 0
        end_time_stamp = str2timestamp(end_time, format)
        if start_time_stamp <= now <= end_time_stamp:
            return value['version']
    return 0


def active_inreview_start_end_time_by_timestamp(config, differ_time=0):
    """
    # 获取活动的开启和结束的时间
    :param config: 配置表 如game_config.roulette
    :return: 版本号,开始时间,结束时间
    """
    now = time.time()
    for active_id, value in config.iteritems():
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time_stamp = value['start_time']
        end_time_stamp = value['end_time']
        if start_time_stamp <= now - differ_time <= end_time_stamp:
            return value['version']
    return 0


def get_active_inreview_version_start_end_time(config, active_id=0):
    """
    # 获取活动的开启和结束的时间
    :param config: 配置表 如game_config.roulette
    :return: 版本号,开始时间,结束时间
    """
    now = time.time()
    FORMAT = '%Y-%m-%d %H:%M:%S'
    for version, value in config.iteritems():
        if value['active_type'] != active_id:
            continue
        if 'start_time' not in value or 'end_time' not in value:
            return 0, 0, 0, 0
        start_time = value['start_time']
        if not start_time:
            return 0, 0, 0, 0
        end_time = value['end_time']
        if not end_time:
            return 0, 0, 0, 0
        start_time_stamp = str2timestamp(start_time, FORMAT)
        end_time_stamp = str2timestamp(end_time, FORMAT)
        if start_time_stamp <= now <= end_time_stamp:
            version_id = version if not value.get('active_version', 0) else value.get('active_version', 0)
            return version, version_id, start_time_stamp, end_time_stamp
    return 0, 0, 0, 0


def active_inreview_version(config, diff_time=0, server_id='', active_id=0):
    """
    # 获取活动的版本号
    :param config: 配置表 如game_config.roulette
    :return: 版本号
    """
    now = time.time()
    if server_id:
        server_type = game_config.get_config_type(server_id)
        server_num = settings.get_server_num(server_id)
    else:
        server_type = ''
        server_num = 0

    for version, value in config.iteritems():
        if value.get('active_type', 0) != active_id:
            continue
        if 'server_id' in value:
            server = value['server_id']
            if (server_type and server_type != 2) or \
                    (server and not (server_num and server[0] <= server_num <= server[-1])):
                continue
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time = value['start_time']
        if not start_time:
            return 0
        end_time = value['end_time']
        if not end_time:
            return 0
        start_time_stamp = str2timestamp(start_time)
        end_time_stamp = str2timestamp(end_time)
        if start_time_stamp <= now - diff_time <= end_time_stamp:
            version = version if not value.get('active_version', 0) else value.get('active_version', 0)
            return version
    return 0


def active_inreview_version_by_timestamp(config):
    """
    # 获取活动的版本号
    :param config: 配置表 如game_config.roulette
    :return: 版本号
    """
    now = time.time()
    for version, value in config.iteritems():
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time_stamp = value['start_time']
        end_time_stamp = value['end_time']
        if start_time_stamp <= now <= end_time_stamp:
            return version
    return 0


def format_time_active_version(config, format, differ_time=0):
    """
    #获取活动的版本号
    :param config: 配置表 如game_config.roulette
    :param format: 时间的格式为%Y-%m-%d 或者 %Y-%m-%d
    :param differ_time: 活动结束几小时之后发奖, differ_time是时间差值
    :return: 版本号
    """
    now = time.time()
    for version, value in config.iteritems():
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time = value['start_time']
        if not start_time:
            return 0
        end_time = value['end_time']
        if not end_time:
            return 0
        start_time_stamp = str2timestamp(start_time, format)
        end_time_stamp = str2timestamp(end_time, format)
        if start_time_stamp <= now - differ_time <= end_time_stamp:
            return version
    return 0


def format_time_active_config_version(config, format, differ_time=0):
    """
    #获取活动的版本号
    :param config: 配置表 如game_config.roulette
    :param format: 时间的格式为%Y-%m-%d 或者 %Y-%m-%d
    :param differ_time: 活动结束几小时之后发奖, differ_time是时间差值
    :return: 版本号
    """
    now = time.time()
    for version, value in config.iteritems():
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time = value['start_time']
        if not start_time:
            return 0

        end_time = value['end_time']
        if not end_time:
            return 0
        start_time_stamp = str2timestamp(start_time, format)
        end_time_stamp = str2timestamp(end_time, format)
        if start_time_stamp <= now - differ_time <= end_time_stamp:
            return value['version']
    return 0


def active_inreview_version_mapping(config, diff_time=0, server_type=''):
    """
    # 获取活动的版本号
    :param config: 配置表 如game_config.super_all_mapping
    :return: 版本号
    """
    now = time.time()
    FORMAT = '%Y-%m-%d %H:%M:%S'
    for version, data in config.iteritems():
        value_id = min(data)
        value = data[value_id]
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time = value['start_time']
        if not start_time:
            return 0
        end_time = value['end_time']
        if not end_time:
            return 0
        start_time_stamp = str2timestamp(start_time, FORMAT)
        end_time_stamp = str2timestamp(end_time, FORMAT)
        if start_time_stamp <= now - diff_time <= end_time_stamp:
            return version
    return 0


def active_inreview_version_mapping_by_timestamp(config, diff_time=0):
    """
    # 获取活动的版本号
    :param config: 配置表 如game_config.super_all_mapping
    :return: 版本号
    """
    now = time.time()
    for version, data in config.iteritems():
        value_id = min(data)
        value = data[value_id]
        if 'start_time' not in value or 'end_time' not in value:
            return 0
        start_time_stamp = value['start_time']
        end_time_stamp = value['end_time']
        if start_time_stamp <= now - diff_time <= end_time_stamp:
            return version
    return 0


def active_inreview_version_and_start_and_end_mapping(config, diff_time=0):
    """
    # 获取活动的版本号
    :param config: 配置表 如game_config.super_all_mapping
    :return: 版本号
    """
    now = time.time()
    for version, data in config.iteritems():
        value_id = min(data)
        value = data[value_id]
        if 'start_time' not in value or 'end_time' not in value:
            return 0, 0, 0
        start_time = value['start_time']
        if not start_time:
            return 0, 0, 0
        end_time = value['end_time']
        if not end_time:
            return 0, 0, 0
        start_time_stamp = str2timestamp(start_time)
        end_time_stamp = str2timestamp(end_time)
        if start_time_stamp <= now - diff_time <= end_time_stamp:
            return version, start_time_stamp, end_time_stamp
    return 0, 0, 0


def active_is_open(start_time, end_time, now=None):
    """ 获取一条记录是否开启

    :param start_time:
    :param end_time:
    :param now:
    :return:
    """
    now = now or time.time()
    start_time_stamp = str2timestamp(start_time)
    end_time_stamp = str2timestamp(end_time)
    if start_time_stamp <= now <= end_time_stamp:
        return True
    else:
        return False


# 切分形如 15 00:00:00 的格式的时间差
def split_timedelta(tm):
    day, time_24 = tm.split(' ')
    hour, minute, seconds = time_24.split(':')
    return int(day), int(hour), int(minute), int(seconds)


# 分隔时间如 1 00:00:00-15 00:00:00 的格式的时间范围， 支持以逗号分隔的多组
def split_time_list(tm, open_dt, diff_hour=0):
    intervals = tm.split(',')  # 取出开服活动的每一个时间段
    s_time = datetime.datetime.now()
    e_time = datetime.datetime.now()
    for i, interval in enumerate(intervals):
        start, end = interval.split('-')
        s_day, s_hour, s_minute, s_seconds = split_timedelta(start)
        e_day, e_hour, e_minute, e_seconds = split_timedelta(end)
        s_delta = datetime.timedelta(s_day - 1)  # 开服后第几天开始的数值
        e_delta = datetime.timedelta(e_day - 1)
        e_hour -= diff_hour
        s_day = open_dt + s_delta
        e_day = open_dt + e_delta
        s_clock = datetime.time(s_hour, s_minute, s_seconds)  # 开始的具体时刻
        e_clock = datetime.time(e_hour, e_minute, e_seconds)
        s_time = datetime.datetime.combine(s_day, s_clock)  # 活动开始时间
        e_time = datetime.datetime.combine(e_day, e_clock)  # 活动结束时间
        now = datetime.datetime.now()
        if s_time <= now <= e_time:
            return i + 1, s_time, e_time
    return 0, s_time, e_time


# 获取inreview表的活动时间确定版本信息
def get_inreview_version(user, active_id, diff_hour=0):
    opening = user.server_opening_time_info()
    open_time = opening['open_time']
    open_dt = datetime.datetime.strptime(open_time, "%Y-%m-%d")  # 开服时间
    if active_id not in game_config.server_inreview:
        now = datetime.datetime.now()
        return 0, 0, now, now
    show_lv = game_config.server_inreview[active_id]['show_lv']
    if user.level < show_lv:
        now = datetime.datetime.now()
        return 0, 0, now, now
    time_list = game_config.server_inreview[active_id]['name']
    version, s_time, e_time = split_time_list(time_list, open_dt, diff_hour=diff_hour)
    new_server = 0  # 是否为开服活动期间
    if version:
        new_server = 1
    # 当在开服活动中没有找到，则version值为0
    return version, new_server, s_time, e_time


def get_version_by_active_id(format='%Y-%m-%d %H:%M:%S', active_id=0, differ_time=0):
    """
    #获取活动的版本号
    :param config: 配置表 如game_config.roulette
    :param format: 时间的格式为%Y-%m-%d 或者 %Y-%m-%d
    :param differ_time: 活动结束几小时之后发奖, differ_time是时间差值
    :return: id,版本号
    """
    config = game_config.active
    if not active_id:
        return 0, 0
    now = time.time()
    for version, value in config.iteritems():
        if value['active_type'] != active_id:
            continue
        if 'start_time' not in value or 'end_time' not in value:
            return 0, 0
        start_time = value['start_time']
        if not start_time:
            return 0, 0

        end_time = value['end_time']
        if not end_time:
            return 0, 0
        start_time_stamp = str2timestamp(start_time, format)
        end_time_stamp = str2timestamp(end_time, format)
        if start_time_stamp <= now - differ_time <= end_time_stamp:
            return version, value['active_version']
    return 0, 0

def get_version_start_and_end_time_by_active_id(format='%Y-%m-%d %H:%M:%S', active_id=0, differ_time=0):
    """
    #获取活动的版本号
    :param config: 配置表 如game_config.roulette
    :param format: 时间的格式为%Y-%m-%d 或者 %Y-%m-%d
    :param differ_time: 活动结束几小时之后发奖, differ_time是时间差值
    :return: id,版本号
    """
    config = game_config.active
    if not active_id:
        return 0, 0, 0, 0
    now = time.time()
    for version, value in config.iteritems():
        if value['active_type'] != active_id:
            continue
        if 'start_time' not in value or 'end_time' not in value:
            return 0, 0, 0, 0
        start_time = value['start_time']
        if not start_time:
            return 0, 0, 0, 0
        s_time = time.strptime(start_time, format)
        start_time_stamp = time.mktime(s_time)
        end_time = value['end_time']
        if not end_time:
            return 0, 0, 0, 0
        e_time = time.strptime(end_time, format)
        end_time_stamp = time.mktime(e_time)
        if start_time_stamp <= now - differ_time <= end_time_stamp:
            return version, value['active_version'], start_time_stamp, end_time_stamp
    return 0, 0, 0, 0