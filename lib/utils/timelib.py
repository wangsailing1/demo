# -*- coding: utf-8 -*-

__author__ = 'sm'

import time
import datetime


def now_time_to_str(datetime_format='%Y-%m-%d %H:%M:%S'):
    """ 时间转换字符串

    :param now:
    :param datetime_format:
    :return:
    """
    return time.strftime(datetime_format)


def timestamp_to_datetime_str(t, datetime_format='%Y-%m-%d %H:%M:%S'):
    """ time转换为字符串
        >> timestamp_to_datetime_str(1388477789)
        >> 2013-12-31 16:16:29

    :param t:
    :param datetime_format:
    :return:
    """
    if not t:
        return ""
    return time.strftime(datetime_format, time.localtime(t))


def datetime_str_to_timestamp(dt, datetime_format='%Y-%m-%d %H:%M:%S'):
    """ 字符串转换为time
        >> datetime_str_to_timestamp('2013-12-31 16:16:29')
        >> 1388477789

    :param dt:
    :param datetime_format:
    :return:
    """
    if not dt:
        return 0
    return int(time.mktime(time.strptime(str(dt), datetime_format)))


def str_to_datetime(s, datetime_format='%Y-%m-%d %H:%M:%S'):
    """ 字符串转换为datetime
        >> str_to_datetime('2013-12-31 16:16:29')

    :param s:
    :param datetime_format:
    :return:
    """
    return datetime.datetime.strptime(s, datetime_format)


def datetime_to_str(dt, datetime_format='%Y-%m-%d %H:%M:%S'):
    """ datetime转换为字符串
        >> datetime_to_str(datetime.datetime.now())
        >> 2014-01-22 15:54:51

    :param dt:
    :param datetime_format:
    :return:
    """
    return dt.strftime(datetime_format)


def datetime_to_time(dt):
    """datetime类型转换为time类型

    :return:
    """
    return time.mktime(dt.timetuple()) if dt else 0


def time_to_datetime(t):
    """time类型转换为datetime类型
        In [18]: datetime.datetime.fromtimestamp(int(time.time()))
        Out[18]: datetime.datetime(2014, 3, 24, 20, 33, 1)

    :param t:
    """
    return datetime.datetime.fromtimestamp(t) if t else datetime.datetime.now()
