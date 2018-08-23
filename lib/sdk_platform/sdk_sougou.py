# -*- coding: utf-8 -*-
# Android系统 搜狗平台

__version__ = '1.4.34'

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
    'sougou': {
        'app_id': '255',
        'app_key': '2525fd6bff45a68113deeff9584188bc22c7bec4237b892c77d4d79097fae704',
        'app_secret': '0e4711ea9a45b66bb553f3e7d248c8099b33bca22591fd35f68fd96caa02a907',
        'pay_key': '{18393804-B6BF-4D9E-A67E-2B63B0879760}',
    },
}


STRING_VERIFICATION_URL = 'http://api.app.wan.sogou.com/api/v1/login/verify'


class SDKSougou(object):

    SUCCESS = 'OK'
    FAIL = 'ERR_100'

    EXCLUDE_KEY = ('auth',)

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_secret = PLATFORM_INFO.get(pf, {}).get('app_secret', '')
        self.pay_key = PLATFORM_INFO.get(pf, {}).get('pay_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        openid = kwargs.get('openid')

        get_data = {
            'gid': self.app_id,
            'user_id': openid,
            'session_key': session_id,
        }

        get_data['auth'] = self.generate_auth(get_data, self.app_secret)

        url = '%s&%s' % (STRING_VERIFICATION_URL, urllib.urlencode(get_data))

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

        if not obj.get('result'):
            return None

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数              参数说明
            gid          game id 由平台分配的游戏编号
            sid          server id 由平台分配的游戏区服编号
            uid          user id 平台的用户id
            role         若游戏需充值到角色，传角色名。默认会传空
            oid          订单号，同一订单有可能多次发送通知
            date         订单创建日期，格式为yyMMdd
            amount1      用户充值金额（人民币元）
            amount2      金额（游戏币数量）（手游忽略此参数，但校验时需要传递）
            time         此时间并不是订单的产生或支付时间，而是通知发送的时间，也即当前时间
            appdata      透传参数（可无），若需要须向平台方申请开启此功能，默认开启
            realAmount   用户充值真实金额（人民币元）
            auth         验证字符串, 生成方式同auth token, 区别是在第三步, 附加支付秘钥而不是app secret
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        auth = data_dict.get('auth')

        if auth is None:
            return False

        gen_auth = self.generate_auth(data_dict, self.pay_key)

        if gen_auth != auth:
            return False

        pay_data = dict(game_order_id=data_dict['appdata'], order_id=data_dict['oid'],
                        amount=float(data_dict['realamount']), uin=data_dict['uid'])

        return pay_data

    def generate_auth(self, data, key):
        """ 生成auth

        :param data:
        :return:
        """
        sorted_items = sorted((k, v) for k, v in data.iteritems() if k not in self.EXCLUDE_KEY)
        params_str = urllib.urlencode(sorted_items)
        sign_str = '%s&%s' % (params_str, key)

        return crypto.md5(sign_str)


SDKManager.register('sdk_sougou', SDKSougou)
