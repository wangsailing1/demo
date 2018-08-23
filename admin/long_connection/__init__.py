#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import datetime
import os
import json

import settings
from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from lib.utils import http


ENV_NAME = settings.ENV_NAME
CONFIG_NAME = 'copy_for_long_config'

@require_permission
def index(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    config = settings.long_settings

    msg = u''
    webhost = config.get('master', {}).get('webhost')
    webport = config.get('master', {}).get('webport')

    try:
        code, content = http.get('http://%s:%s/info' % (webhost, webport), timeout=5)
        content = json.loads(content)
        if code != 200:
            msg = u'请求错误'
    except:
        # import traceback
        # print traceback.print_exc()
        content = {}
        msg = u'请求失败'

    data = {
        'environment': ENV_NAME,
        'msg': msg,
        'content': content,
    }

    return render(req, 'admin/long_connection/index.html', **data)
