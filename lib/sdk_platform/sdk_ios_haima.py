# -*- coding: utf-8 -*-
# IOS系统 爱贝海马平台

___version__ = 'V4.0.1-2.0'

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
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC16hfv7dcFrncw/BlzDK2S+1JQ
gRFBjkfY4r3GjrcjWD0SOxXKmR7iJBwHb7cYjw2kOF7DNs8uNVh4gd+FX7uNNQXU
fnQdYXfXfyFlOeNkd7uXB6GyHr1q167HkKNZBdURPyLv5iWztV+Lr2m8U0Jni8Ve
Y/Gze9RwRm3XIhoHEQIDAQAB
-----END PUBLIC KEY-----
""",
        'private_key': """
-----BEGIN PRIVATE KEY-----
MIICXQIBAAKBgQCP081kRNM5XVpCrStTt1hFCGasmsFORKxV+tglqpReQOV3Y
zUv54hWJGGwxyAsd8tDkRjivUG4jSoD/K90Gd3OEDwcayN41hqtUoAv4FUQ59
XdcdJiMt6ByBGz4oL/axlsQDA5/4kYW+8/8lF9cv4ZGSRJbYvEPl+PEFIgUKP
UtQIDAQABAoGBAI2JQ+0xYZ9pA4LsAOAwZBgDDW88F5CbOfCemohulfUu7eGP
6m5K7bq/sLcTLdE0zf2e0xuGXR9tI3Sq/EpHjiJYuRFtw4prHO710eAVjSu+A
5Hd4SHUs4lDhnl/RYJ0mmHWFIlve4SOCupoEoVc413xCyaTK/E18Z2tlCvOeG
eBAkEAz5UsPjOoG8g55g6OK8EQWna6pu012ysj6StW790lPGI6C0TacYvNjgz
F/zX0trzJ/PKinbXp1agnph4F7gJ/VQJBALFfxxnBs6tGzOIrb8/f9boU+8yU
CAr5ZjvplAZL5faZu7rBRoX8vICN8hqnu3+qusl7k2BUCBsB+Zylxh6sP+ECQ
QCUTSmXosYWWxzqPDncDolFaA9/lHbmhtKYEcuBgEfK9Q4s4NsDRfLr6jpGU2
DqcMQJv7rn24AckY8KAecQnJ4lAkB+MorRxIM0hTcYY5c16z5FmtBcCaZ/SFp
4ngN3R2DiRxbOFN08T0k+nb93P4ejmbEz0PxWOPNbY9hYn4mKITuBAkBq8wId
ftOK7xDnMR35l9nxtYbpNUeIVn5tZ3v+qvVbLY1dd1mfYZOLGZhW2pOkc22kt
O0Lnw3SGjJw8tgcw9Wr
-----END PRIVATE KEY-----
""",
    },
}


VERIFY_SESSION_URL = 'http://ipay.iapppay.com:9999/payapi/tokencheck'


class SDKIOSHaima(object):
    """ 海马ios的sdk

    """

    SUCCESS = 'SUCCESS'
    FAIL = 'FAILURE'

    MD5_FORMAT = 'appid=%(appid)s&sessionid=%(sessionid)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = 'haima_%s' % pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_secret = PLATFORM_INFO.get(pf, {}).get('app_secret', '')
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

        transdata_data = {
            'appid': self.app_id,
            'logintoken': session_id,
        }

        transdata = json.dumps(transdata_data)

        transdata_md5 = crypto.md5(transdata)

        sign = crypto.rsa_private_sign(self.private_key, transdata_md5, rsa=self.private_rsa)

        post_data = {
            'transdata': transdata,
            'sign': sign,
            'signtype': 'RSA',
        }

        try:
            http_code, content = http.post(VERIFY_SESSION_URL, data=urllib.urlencode(post_data), timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        parse_data = crypto.parse_keqv(content)
        parse_transdata = json.loads(parse_data['transdata'])

        if parse_transdata.get('code') is not None:
            return None

        openid = parse_transdata.get('userid')

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            transdata:
                参数名称	    参数含义      数据类型	   是否可选	参数说明
                transtype	交易类型	     integer	必填	    "交易类型： 0–支付交易； 1–支付冲正（暂未启用）； 2–契约退订 3–自动续费"
                cporderid	商户订单号	 String(64)	可选	    商户订单号
                transid	    交易流水号	 String(32)	必填	    计费支付平台的交易流水号
                appuserid	用户在商户应用的唯一标识	String(32)	必填	用户在商户应用的唯一标识
                appid	    游戏id	     String(20)	必填	    平台为商户应用分配的唯一代码
                waresid	    商品编码	     integer	必填	    平台为应用内需计费商品分配的编码
                feetype	    计费方式	     integer	必填	    计费方式，具体定义见附录
                money	    交易金额	     Float(6,2)	必填	    本次交易的金额
                currency	货币类型	     String(32)	必填	    "货币类型以及单位： RMB – 人民币（单位：元）"
                result	    交易结果	     integer	必填	    "交易结果： 0–交易成功 1–交易失败"
                transtime	交易完成时间  String(20)	必填	    "交易时间格式： yyyy-mm-dd hh24:mi:ss"
                cpprivate	商户私有信息  String(64)	可选	    商户私有信息
                paytype	    支付方式      integer	    可选	    支付方式，具体定义见附录
            sign:
            signtype:
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        transdata = data_dict['transdata']

        try:
            json_transdata = json.loads(transdata)
        except:
            return False

        if json_transdata['result'] != '0':
            return False

        try:
            if not crypto.rsa_verify_signature(self.public_key, transdata, sign, rsa=self.public_rsa):
                return False
        except:
            print traceback.print_exc()
            return False

        pay_data = dict(game_order_id=json_transdata['cporderid'], order_id=json_transdata['transid'],
                        amount=float(json_transdata['money']), uin=json_transdata['appuserid'])

        return pay_data


SDKManager.register('sdk_ios_haima', SDKIOSHaima)
