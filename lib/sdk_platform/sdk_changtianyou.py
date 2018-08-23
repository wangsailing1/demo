# -*- coding: utf-8 -*-
# Android系统 小米平台

__version__ = ''

import json
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

ACCESS_KEY = 'qxvrwa'

PLATFORM_INFO = {
    'changtianyou': {
        'access_key': ACCESS_KEY,
    },
}


class SDKChangtianyou(object):

    SUCCESS = 'success'
    FAIL = 'fail'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.access_key = PLATFORM_INFO.get(pf, {}).get('access_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """
        登录验证
        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """

        return {
            'openid': session_id,            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数                 必填     备注
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        pre_sign = (
            "%(CompanyID)s"
            "%(Mobile)s"
            "%(Amount)s"
            "%(OrderID)s"
            "%(Result)s"
        ) % data_dict + self.access_key

        if data_dict['Key'] != crypto.md5(pre_sign):
            return True

        pay_data = dict(game_order_id=data_dict['CompanyID'], order_id=data_dict['OrderID'],
                        amount=float(data_dict['Amount']), uin=data_dict['Mobile'])

        return pay_data


SDKManager.register('sdk_changtianyou', SDKChangtianyou)
