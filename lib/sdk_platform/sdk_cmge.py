# -*- coding: utf-8 -*-
# Android系统 中手游平台

___version__ = '2.7.0'

import json
import traceback
import urllib

from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


VERIFY_SESSION_URL = 'http://sdksrv.joygame.cn/sdksrv/auth/'

PLATFORM_INFO = {
    'cmge': {
        'verify_session_url': VERIFY_SESSION_URL,

    },
}


class SDKCmge(object):

    SUCCESS = 'success'
    FAIL = 'failed'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.verify_session_url = PLATFORM_INFO.get(pf, {}).get('verify_session_url', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """

        return {
            'openid': '',
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数              说明

        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """

        pay_data = dict(game_order_id=data_dict['apporderID'], order_id=data_dict['apporderID'],
                        amount=float(data_dict['price']) / 100.0, uin=data_dict['uid'])

        return pay_data


SDKManager.register('sdk_cmge', SDKCmge)
