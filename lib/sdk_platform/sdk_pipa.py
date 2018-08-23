# -*- coding: utf-8 -*-
# Android系统 琵琶平台

___version__ = '2.3'

import json
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'pipa': {
        'app_id': '10971409722086',
        'merchant_id': '1097',
        'merchant_app_id': '1115',
        'app_secret': '6df75b5c599df80ebf850043556ffecf',
    },
}


VERIFICATION_URL = 'http://pay.pipaw.com/appuser/Checksid'


class SDKPipa(object):

    SUCCESS = 'OK'
    FAIL = 'Fail'

    EXCLUED_KEYS = ('sign', 'sign_v1', 'version')

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_secret = PLATFORM_INFO.get(pf, {}).get('app_secret', '')
        self.merchant_id = PLATFORM_INFO.get(pf, {}).get('merchant_id', '')
        self.merchant_app_id = PLATFORM_INFO.get(pf, {}).get('merchant_app_id', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        username = kwargs.get('token')
        time = kwargs.get('channel_id')

        post_data = {
            'username': username,
            'appId': self.app_id,
            'merchantId': self.merchant_id,
            'merchantAppId': self.merchant_app_id,
            'sid': session_id,
            'time': time,
        }

        try:
            http_code, content = http.post(VERIFICATION_URL, data=urllib.urlencode(post_data), timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except:
            return None

        if int(obj['result']) != 1:
            return None

        return {
            'openid': obj['uid'],
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数              类型      说明
            order:      商家自己的订单号
            subject:    商家提交的支付项目名称
            body:       商家提交的支付项目描述
            sign:       2.3以下 签名(只对body,order,subject 3项数据的签名)；
                        2.3及以上 签名(对amount,extraParam,order,pipaworder,player_id,subject 6项数据按照键名从小到大排序的签名)
            amount:     支付的金额
            player_id:  最终用户玩家ID
            sign_v1:    2.3以下才有的 签名(对order,subject,body,amount,player_id 5项数据按照键名从小到大排序的签名) 安全性更高
            version:    2.3 及以上的版本,可通过参数 version 获得当前 SDK 的版本号
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        sorted_items = sorted((k, v) for k, v in data_dict.iteritems() if v and k not in self.EXCLUED_KEYS)
        sign_values = ['%s=%s' % (k, v) for k, v in sorted_items]
        sign_data = '&'.join(sign_values)

        gen_sign = crypto.md5('%s%s' % (sign_data, self.app_secret))

        if gen_sign != sign:
            return False

        pay_data = dict(game_order_id=data_dict['order'], order_id=data_dict['order'],
                        amount=float(data_dict['amount']), uin=data_dict['player_id'])

        return pay_data


SDKManager.register('sdk_pipa', SDKPipa)
