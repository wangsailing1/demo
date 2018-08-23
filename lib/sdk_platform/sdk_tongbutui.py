# -*- coding: utf-8 -*-
# Android系统 同步推平台

__version__ = '1.3.0'

import json
import time
import traceback
import urllib
import hmac
import hashlib
import base64
import binascii

from M2Crypto import BIO, RSA
from oauth import oauth

from lib.utils import http
from lib.utils import crypto
from lib.utils.encoding import force_str
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'android': {
        'app_id': '140419',
        'payment_key': 'qANkax@UJ5tE7od1AXNkxH0Ug5t7Qndq',
    },
}


STRING_VERIFICATION_URL = 'http://tgi.tongbu.com/api/LoginCheck.ashx'


class SDKTongbutui(object):

    SUCCESS = {'status': 'success'}
    FAIL = {'status': 'failure'}

    MD5_FORMAT = 'source=%(source)s&trade_no=%(trade_no)s&amount=%(amount)s&' \
                 'partner=%(partner)s&paydes=%(paydes)s&debug=%(debug)s&' \
                 'tborder=%(tborder)s&key=%(key)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = 'tongbutui_%s' % pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.payment_key = PLATFORM_INFO.get(pf, {}).get('payment_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        get_data = {
            'session': session_id,
            'appid': self.app_id,
        }

        url = '%s&%s' % (STRING_VERIFICATION_URL, urllib.urlencode(get_data))

        try:
            http_code, content = http.get(url, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            openid = int(content)
        except ValueError:
            return None

        if openid in (0, -1):
            return None

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数              参数说明
            source          数据来源,默认值tongbu
            trade_no        订单编号(游戏订单号)
            amount          额,单位为分
            partner         游戏编号----同步游戏联运平台为游戏分 配的唯编号
            paydes          付说明(客户端不能传中 )
            debug           是否调试模式(判断订单是否是测试订单)
            tborder         同步订单号
            sign            签名----将以上参数加key后得到的签名
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        data_dict['key'] = self.payment_key

        gen_sign = crypto.md5(self.MD5_FORMAT % data_dict)

        if gen_sign != sign:
            return False

        pay_data = dict(game_order_id=data_dict['trade_no'], order_id=data_dict['tborder'],
                        amount=float(data_dict['amount']) / 100, uin='')

        return pay_data


SDKManager.register('sdk_tongbutui', SDKTongbutui)
