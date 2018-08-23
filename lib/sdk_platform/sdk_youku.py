# -*- coding: utf-8 -*-
# Android系统 优酷平台

___version__ = 'v2.6'

import json
import traceback
import urllib

from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'youku': {
        'app_id': '462',
        'app_key': 'abfe9cc5a2dbafb4',
        'app_secret': '09bed2e63c5f75cb5c479c4820790e9a',
        'payment_key': '52efb52c7628a71554030c3d0ca4be9e',
    },
}


VERIFY_SESSION_URL = 'http://sdk.api.gamex.mobile.youku.com/game/user/infomation'


class SDKYouku(object):

    SUCCESS = {'status': 'success', 'desc': '通知成功'}
    FAIL = {'status': 'failed', 'desc': ''}

    EXCLUDE = ('sign', 'passthrough', 'result', 'success_amount'),

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_secret = PLATFORM_INFO.get(pf, {}).get('app_secret', '')
        self.payment_key = PLATFORM_INFO.get(pf, {}).get('payment_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """

        post_data = {
            'appkey': self.app_key,
            'sessionid': session_id,
            'sign': crypto.hmac_md5(self.payment_key, 'appkey=%s&sessionid=%s' % (self.app_key, session_id)),
        }

        try:
            http_code, content = http.post(VERIFY_SESSION_URL, data=urllib.urlencode(post_data), timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        if not content:
            return None

        try:
            obj = json.loads(content)
        except ValueError:
            return None

        if obj['status'] != 'success':
            return None

        openid = obj.get('uid')

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict, callback_url):
        """支付验证

        :param data_dict:
            参数              说明
            apporderID      订单号(最长不超过 64 位)
            uid             用户 id
            price           价格(单位为“分”)
            sign            数字签名
            passthrough     透传参数(最长 128 位)
            result          计费结果 0:计费失败 1:计费成功 2: 计费部分成功(短代支付独有的参数, 其他支付方式没有这个参数)
            success_amount  成功支付金额(短代支付独有的参数, 其他支付方式没有这个参数)
        :param callback_url:
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        sign_items = sorted([(key, value) for key, value in data_dict.iteritems() if key not in self.EXCLUDE])
        query_str = '&'.join('%s=%s' % (key, value) for key, value in sign_items)

        gen_sign = crypto.hmac_md5(self.payment_key, '%s?%s' % (callback_url, query_str))

        if gen_sign != sign:
            return False

        pay_data = dict(game_order_id=data_dict['apporderID'], order_id=data_dict['apporderID'],
                        amount=float(data_dict['price']) / 100.0, uin=data_dict['uid'])

        return pay_data


SDKManager.register('sdk_youku', SDKYouku)
