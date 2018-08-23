# -*- coding: utf-8 -*-
# IOS系统 itools平台

___version__ = '2.6.0'

import json
import traceback
import urllib

from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'yios': {
        'app_id': '5179759',
        'app_key': 'VjiprywVjgRaNUG626AMhBw0',
        'app_secret': '4zcb3iZ4peBEOWS3rH24iey5HouhbUA6',
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2kcrRvxURhFijDoPpqZ/IgPlA
gppkKrek6wSrua1zBiGTwHI2f+YCa5vC1JEiIi9uw4srS0OSCB6kY3bP2DGJagBo
Egj/rYAGjtYJxJrEiTxVs5/GfPuQBYmU0XAtPXFzciZy446VPJLHMPnmTALmIOR5
Dddd1Zklod9IQBMjjwIDAQAB
-----END PUBLIC KEY-----
""",
    },
}


VERIFY_SESSION_URL = 'https://pay.slooti.com/?r=auth/verify'


class SDKItools(object):

    SUCCESS = 'success'
    FAIL = 'fail'

    MD5_FORMAT = 'appid=%(appid)s&sessionid=%(sessionid)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = 'itools_%s' % pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_secret = PLATFORM_INFO.get(pf, {}).get('app_secret', '')
        self.public_key = PLATFORM_INFO.get(pf, {}).get('public_key', '')
        self.bio = BIO.MemoryBuffer(self.public_key)
        self.rsa = RSA.load_pub_key_bio(self.bio)

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """

        get_data = {
            'appid': self.app_id,
            'sessionid': session_id,
        }

        get_data['sign'] = crypto.md5(self.MD5_FORMAT % get_data)

        url = '%s&%s' % (VERIFY_SESSION_URL, urllib.urlencode(get_data))

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

        if obj['status'] != 'success':
            return None

        openid, _ = session_id.split('_', 1)

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            键值         说明
            sign        签名校验值(base64 编码)
            notify_data 加密数据(base64 编码)
                键值              类型      说明
                order_id_com    string  发起支付时的订单号即商户订单号
                user_id         string  支付的用户 id
                amount          string  成功支付的金额
                account         string  支付帐号
                order_id        string  支付平台的订单号
                result          string  支付结果, 目前只有成功状态, success
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        notify_data = data_dict.get('notify_data')

        # 游戏服务器接收到数据后先使用base64解码并使用RSA公钥解密传输数据 (notify_data)
        try:
            context = crypto.rsa_public_decrypt(self.public_key, notify_data, rsa=self.rsa)
        except:
            print traceback.print_exc()
            return False

        # 然后使用RSA公钥校验数据签名,签名校验成功后根据传输数据做逻辑处理。
        try:
            if not crypto.rsa_verify_signature(self.public_key, context, sign, rsa=self.rsa):
                return False
        except:
            print traceback.print_exc()
            return False

        try:
            jdata = json.loads(context)
        except ValueError:
            print traceback.print_exc()
            return False

        if jdata['result'] != 'success':
            return False

        pay_data = dict(game_order_id=jdata['order_id_com'], order_id=jdata['order_id'],
                        amount=float(jdata['amount']), uin=jdata['user_id'])

        return pay_data


SDKManager.register('sdk_itools', SDKItools)
