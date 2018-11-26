#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import datetime

from admin import render
from admin.decorators import require_permission
from admin.decorators import Logging as AdminLogging


@require_permission
def adminlog_index(req, search_args=None, msg=None):
    """
    查询近期所有日志
    :param req:
    :param search_args:
    :param msg:
    :return:
    """
    admin_logging = AdminLogging(None)
    if search_args:
        if isinstance(search_args, basestring):
            data = admin_logging.get_all_logging()
            logging_data = [i for i in data if i['admin'] == search_args]
        elif isinstance(search_args, dict) and 'search_time' in search_args:
            logging_data = admin_logging.get_logging(search_args['search_time'])
        else:
            logging_data = admin_logging.get_all_logging()
    else:
        logging_data = admin_logging.get_all_logging()
    args = {
        'logging_data': logging_data,
        'message': msg if msg else '',
    }
    return render(req, 'admin/adminlogs/index.html', **args)


@require_permission
def adminlog_search_by_name(req):
    """ 按名字搜索

    :param req:
    :return:
    """
    username = req.get_argument('username', '')
    if not username:
        return adminlog_index(req, msg=u"请输入账号")

    return adminlog_index(req, search_args=username)


@require_permission
def adminlog_search_by_time(req):
    """ 按日期搜索

    :param req:
    :return:
    """
    search_time = req.get_argument('search_time', '')
    if not search_time:
        return adminlog_index(req, msg=u"请输入时间")

    try:
        datetime.datetime.strptime(search_time, '%Y-%m-%d')
    except:
        return adminlog_index(req, msg=u"请输入正确的时间, 例如:2015-03-28")

    return adminlog_index(req, search_args={'search_time': search_time})
