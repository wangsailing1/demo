# -*- coding: utf-8 -*-
# Android系统 豌豆荚平台

__version__ = '4.0.7'

import json
import urllib
from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

APP_KEY = 'ZfHkdP6YfTGMNWzIQ3GPTvi89zcLUVnn'
APPKEY_ID = 5415
VERIFY_URL = 'https://pay.wandoujia.com/api/uid/check'

PLATFORM_INFO = {
    'wandoujia': {
        'app_key': APPKEY_ID,
        'app_id': APPKEY_ID,
        'verify_url': VERIFY_URL,
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCd95FnJFhPinpNiE/h4VA6bU1r
zRa5+a25BxsnFX8TzquWxqDCoe4xG6QKXMXuKvV57tTRpzRo2jeto40eHKClzEgj
x9lTYVb2RFHHFWio/YGTfnqIPTVpi7d7uHY+0FZ0lYL5LlW4E2+CQMxFOPRwfqGz
Mjs1SDlH7lVrLEVy6QIDAQAB
-----END PUBLIC KEY-----
"""
    },
}


class SDKWandoujia(object):

    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.verify_url = PLATFORM_INFO.get(pf, {}).get('verify_url', '')
        self.public_key = PLATFORM_INFO.get(pf, {}).get('public_key', '')
        self.bio = BIO.MemoryBuffer(self.public_key)
        self.rsa = RSA.load_pub_key_bio(self.bio)

    def login_check(self, session_id, *args, **kwargs):
        """
        登录验证
        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        openid = kwargs.get('openid')
        if not openid:
            return None

        query_data = urllib.urlencode({
            'uid': openid,
            'token': session_id,
            'appkey_id': self.app_id,
        })
        url = '%s?%s' % (self.verify_url, query_data)
        http_code, content = http.get(url)

        if http_code != 200:
            return None

        if content != 'true':
            return None

        return {
            'openid': openid,            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数                  类型             字段说明            备注
            sing                string             签名
            signType            string             签名类型(RSA)       值固定RSA
            content             string             回调内容            以PHP为例,($_POST['content'])
                timeStamp       string             时间戳
                orderId         string             豌豆荚订单id
                money           string             支付金额            单位分
                chargeType      string             支付类型            APIPAY:支付宝,SHENZHOUPAY:充值卡,BALANCEPAY:余额,CREDITCARD:信用卡,DEBITCARD:借记卡
                appKeyId        string             appKeyId
                buyerId         string             购买人的账号id
                out_trade_no    string             开发者订单号         创建订单时候传入的订单号原样返还
                cardNo          string             充值卡id            只有充值卡充值的时候才不为空

        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict['sign']
        content = data_dict['content'].encode('utf-8')

        if not crypto.rsa_verify_signature(self.public_key, content, sign, rsa=self.rsa):
            return None

        obj = json.loads(content)

        pay_data = dict(game_order_id=obj['out_trade_no'], order_id=obj['orderId'],
                        amount=float(obj['amount']) / 100, uin=obj['buyerId'])

        return pay_data


SDKManager.register('sdk_wandoujia', SDKWandoujia)
