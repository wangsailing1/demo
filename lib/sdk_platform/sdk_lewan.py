# -*- coding: utf-8 -*-
# Android系统 乐玩平台

__version__ = 'v1.3'

import json
import traceback
import urllib

from M2Crypto import BIO, RSA

from lib.utils import http
from lib.utils import crypto
from lib.utils.encoding import force_str
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'lewan': {
        'app_id': '10041',
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+GY2/8wJuINxzJo9uWoMRUDcx
ONuK/48Fikze8EFpKWLLr6mBpqeoDVvZQoqGhGKn5wdtHujiCUYSn6pcWKY2Fz2R
xw6/1uA1gzKcLE36KLUkqvFbA3gItSiO3ADNCwJ1ochhdfcEnH2dtbiv5+f7m+xv
5B1aEP142v2CtYKFFQIDAQAB
-----END PUBLIC KEY-----
""",
        'private_key': """
-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIX/cV2vLpxqBEFm
uPpH+c+kLUCYihy2rWbKFSi4RmsRp9adEevTju7EeGWLLLPibz3RAnwCBmeMTAIl
A/ltfIDdNMYN4dZEuZ+m+AlprXeS53hP7f8ie9iA//r4aOzhtbwU+wecYuw++JBV
85eUNbVrkALBnkDazjlWnv0A+EfFAgMBAAECgYBHUGbGRFibODUhlYj28t1569eF
nGlM1NA+d2iBbmlTzGa16oxCJSrZ2kh1Sne1GNq5XIZk9zLvYxSEw6x00BdFNSTL
ufvMhhCGvdhevdhC828UZ7vgehArZv78FSj0cSERoj5IfcCXfPlsMlj0agKKLeq5
xMHsSZEGdBkKA4e4IQJBAPSVsB5Zt4iiAx5Qun2QwtdYc0aO4sxk3cchI6H9RJqX
59Cm2BpN68tDhssODoc53u2/cjuc38W4H9lbC2jOq0kCQQCMQHTWztG8QNq8FOv7
bDItUNqbfqeuH847WLkVGsjX33VewnOEZLdO4J5xpacXmsT7p2QwOMGytAbh43aM
U1ydAkAwmSWbgjwjm/1+oo/Lr13nqB2PoYiTEF+4127bGxXsmc5n+R7raxw1ET/R
TQO5/te66dVq3urfwIwjhiGoO5hxAkBvkIZgqTwlZ+GXY30kDrkLWxnKP0HbPOms
Q7NWmmvRbKvMqRmC4yr9z6e592+nUzIGjO0hfsR2BsbCwVH35gfxAkEAy3oNygRr
Y85yheqg45lJ5gYjB9cpq8qwluCbJepLUmqOWSYovX//JmK/W/sSDiWdqHN37d0J
frObNh0xxEMB5g==
-----END PRIVATE KEY-----
""",
    },
}


STRING_VERIFICATION_URL = 'http://lewanduo.com/mobile/user/verifyToken.html'


class SDKLewan(object):

    SUCCESS = 'success'
    FAIL = 'failure'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.public_key = PLATFORM_INFO.get(pf, {}).get('public_key', '')
        self.public_bio = BIO.MemoryBuffer(self.public_key)
        self.public_rsa = RSA.load_pub_key_bio(self.public_bio)
        self.private_key = PLATFORM_INFO.get(pf, {}).get('private_key', '')
        self.private_bio = BIO.MemoryBuffer(self.private_key)
        self.private_rsa = RSA.load_key_bio(self.private_bio)

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        openid = kwargs.get('openid')
        token = kwargs.get('token')
        channel_id = kwargs.get('channel_id')

        data = {
            'app_id': self.app_id,
            'code': openid,
            'password': session_id,
            'token': token,
            'channelId': channel_id,
        }

        get_data = {
            'notifyData': json.dumps(data),
        }

        url = '%s?%s' % (STRING_VERIFICATION_URL, urllib.urlencode(get_data))

        try:
            http_code, content = http.get(url, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except:
            return None

        if obj.get('success') not in ('true', True):
            return None

        openid = obj.get('userId')

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名         含义
            encryptkey    使用 RSA 加密商户AESKey后生成的密钥密文
            data          对含有签名的基本业务数据JSON串加密后形成的密文
                gameId              游戏ID
                gameOrderId         订单号
                gameUserId          用户标识
                payState            支付状态0:待支付 1:已经提交易宝成功 2：支付成功 3：支付失败
                errorCode           错误码 错误码请见附录，只有支付失败的时候才会显示错误码和错误提示，支付成功时不会显示
                errorMsg            错误信息
                expandMsg           扩展信息
                paySuccessMoney     支付金额 成功支付的钱数，单位：分
                lewanOrderId        乐玩系统里的定单ID
                serverId            服务的服ID
                balanceAmt          支付余额
                sign                签名
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        encryptkey = data_dict.get('encryptkey')

        if encryptkey is None:
            return False

        data = data_dict.get('data')

        aes_key = crypto.rsa_private_decrypt(self.private_key, encryptkey, rsa=self.private_rsa)

        aes_data = crypto.aes_decrypt(aes_key, data)

        try:
            aes_dict = json.loads(aes_data)
        except:
            return False

        if aes_dict.get('payState') != 2:
            return False

        sign = aes_dict.pop('sign', None)

        if sign is None:
            return False

        result = sorted(aes_dict.iteritems(), key=lambda x: x[0])

        result = ['%s' % v for k, v in result]
        result_str = force_str(''.join(result))

        if not crypto.rsa_verify_signature(self.public_key, result_str, sign, rsa=self.public_rsa):
            return False

        pay_data = dict(game_order_id=aes_dict['gameOrderId'], order_id=aes_dict['lewanOrderId'],
                        amount=float(aes_dict['paySuccessMoney']) / 100, uin=aes_dict['gameUserId'])

        return pay_data


SDKManager.register('sdk_lewan', SDKLewan)
