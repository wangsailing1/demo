# -*- coding: utf-8 -*-
# Android系统 熊猫玩平台

__version__ = '2.2.5'

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
    'xmwan': {
        'client_id': 'e7de049f9e1dcb181f14bc790a471cdb',
        'client_secret': '9736c023f44562ddf1542a14f66918b0',
    },
}


VERIFICATION_URL = 'http://open.xmwan.com/v2/users/me'
ACCESS_TOKEN_URL = 'http://open.xmwan.com/v2/oauth2/access_token'
ORDER_URL = 'http://open.xmwan.com/v2/purchases'
PAY_VERIFY = 'http://open.xmwan.com/v2/purchases/verify'


class SDKXMWan(object):

    SUCCESS = 'success'
    FAIL = 'fail'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.client_id = PLATFORM_INFO.get(pf, {}).get('client_id', '')
        self.client_secret = PLATFORM_INFO.get(pf, {}).get('client_secret', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        access_token = self.get_access_token(session_id)

        get_data = {
            'access_token': access_token,
        }

        url = '%s?%s' % (VERIFICATION_URL, urllib.urlencode(get_data))

        try:
            http_code, content = http.get(url, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except ValueError:
            return None

        openid = obj.get('xmw_open_id')

        return {
            'openid': openid,
        }

    def get_access_token(self, authorization_code):
        """ 获取token

        :param authorization_code:
        :return:
        """
        post_data= {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
        }

        try:
            http_code, content = http.post(ACCESS_TOKEN_URL, data=urllib.urlencode(post_data), timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except ValueError:
            return None

        return obj.get('access_token')

    def get_order(self, params, *args, **kwargs):
        """ 获取订单号

        :param params:
        :return:
        """
        app_order_id = params.get('app_order_id')

        if not app_order_id:
            return {}

        notify_url = kwargs.get('notify_url')

        timestamp = int(time.time())

        post_data = {
            'app_order_id': app_order_id,
            'app_user_id': params['app_user_id'],
            'notify_url': notify_url,
            'amount': params['amount'],
            'timestamp': timestamp,
        }

        update_data = {
            'access_token': params['access_token'],
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'sign': self.generate_sign(post_data),
        }
        post_data.update(update_data)

        try:
            http_code, content = http.post(ORDER_URL, data=json.dumps(post_data), timeout=3)
        except:
            return {}

        return json.loads(content)

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            serial:         熊猫玩消费订单序列号。
            amount:         充值金额,单位为元。
            status:         消费订单的状态。unpaid 标识尚未支付, success 标识已经支付完成。
            app_order_id:   应用游戏的订单号。
            app_user_id:    应用游戏的用户标识。
            sign:           参数签名。请参考参数签名章节。(小写字符串)
            app_subject:    应用游戏订单名称
            app_description:    应用游戏订单描述。
            app_ext1:       订单额外参数1
            app_ext2:       订单额外参数2
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        if data_dict['status'] != 'success':
            return False

        sign_params = {
            'serial': data_dict['serial'],
            'amount': data_dict['amount'],
            'status': data_dict['status'],
            'app_order_id': data_dict['app_order_id'],
            'app_user_id': data_dict['app_user_id'],
        }

        gen_sign = self.generate_sign(sign_params)

        if gen_sign != sign:
            return False

        if not self.payment_verify_check(data_dict):
            return False

        pay_data = dict(game_order_id=data_dict['app_order_id'], order_id=data_dict['serial'],
                        amount=float(data_dict['amount']), uin='')

        return pay_data

    def payment_verify_check(self, params):
        """ 支付验证

        :return:
        """
        post_data = {
            'serial': params['serial'],
            'amount': params['amount'],
            'app_order_id': params['app_order_id'],
        }

        update_data = {
            'sign': self.generate_sign(post_data),
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        post_data.update(update_data)

        try:
            http_code, content = http.post(PAY_VERIFY, data=urllib.urlencode(post_data), timeout=3)
        except:
            return False

        if http_code != 200:
            return False

        try:
            obj = json.loads(content)
        except ValueError:
            return False

        if obj.get('status') != 'success':
            return False

        return True

    def generate_sign(self, params):
        """ 生成sign

        :param params:
        :return:
        """
        sorted_items = sorted((k, v) for k, v in params.iteritems())
        sign_data = '&'.join(['%s=%s' % (k, v) for k, v in sorted_items])
        return crypto.md5('%s&client_secret=%s' % (sign_data, self.client_secret))


SDKManager.register('sdk_xmwan', SDKXMWan)
