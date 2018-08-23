# -*- coding: utf-8 -*-
# Android and IOS系统 PP平台和九游平台

__version__ = '1.5.6'

import time
import json
import traceback

from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.utils.encoding import force_str
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'android': {
        'app_id': 1234,
        'app_key': 'test',
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzY9c0mC2H1a8YObm0KN9
5Qx3p5/TAjkiU/eogbC+HKE+8gJlgtdjRfhTQIbNuibOWahQK2NnT15G3cLUGzF4
5gPNOuH2JgDs/Zkh6wIzGgt025YOSeVEnMk+HtdaDvL3iArODOZQGiRE3HoaRLuC
5hfxZhvZt3IDf40oH6fTAIWD4irejGJlvewyfM3SEZgCKDMprWESohANwXsaqdDT
frEqb4MJqBLRuPcQ1lSq1sxONfm9OS2Rrk7qOdrkWGGXy3Ldw5EwWNPXuPfAxsKa
DIjdG0RzqIq42K2cw/cd0RHGCCMJXgYc5jNF7ZnakCYYSjy15rDihdGHMQsx5NcQ
PQIDAQAB
-----END PUBLIC KEY-----
""",
    },
    'ios': {
        'app_id': 1234,
        'app_key': 'test',
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzY9c0mC2H1a8YObm0KN9
5Qx3p5/TAjkiU/eogbC+HKE+8gJlgtdjRfhTQIbNuibOWahQK2NnT15G3cLUGzF4
5gPNOuH2JgDs/Zkh6wIzGgt025YOSeVEnMk+HtdaDvL3iArODOZQGiRE3HoaRLuC
5hfxZhvZt3IDf40oH6fTAIWD4irejGJlvewyfM3SEZgCKDMprWESohANwXsaqdDT
frEqb4MJqBLRuPcQ1lSq1sxONfm9OS2Rrk7qOdrkWGGXy3Ldw5EwWNPXuPfAxsKa
DIjdG0RzqIq42K2cw/cd0RHGCCMJXgYc5jNF7ZnakCYYSjy15rDihdGHMQsx5NcQ
PQIDAQAB
-----END PUBLIC KEY-----
""",
    },
    'yios': {
        'app_id': 1234,
        'app_key': 'test',
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzY9c0mC2H1a8YObm0KN9
5Qx3p5/TAjkiU/eogbC+HKE+8gJlgtdjRfhTQIbNuibOWahQK2NnT15G3cLUGzF4
5gPNOuH2JgDs/Zkh6wIzGgt025YOSeVEnMk+HtdaDvL3iArODOZQGiRE3HoaRLuC
5hfxZhvZt3IDf40oH6fTAIWD4irejGJlvewyfM3SEZgCKDMprWESohANwXsaqdDT
frEqb4MJqBLRuPcQ1lSq1sxONfm9OS2Rrk7qOdrkWGGXy3Ldw5EwWNPXuPfAxsKa
DIjdG0RzqIq42K2cw/cd0RHGCCMJXgYc5jNF7ZnakCYYSjy15rDihdGHMQsx5NcQ
PQIDAQAB
-----END PUBLIC KEY-----
""",
    },
}


STRING_VERIFICATION_URL = 'http://passport_i.25pp.com:8080/account?tunnel-command=2852126760'


class SDKPP(object):

    SUCCESS = 'success'
    FAIL = 'fail'

    def __init__(self, pf, *args, **kwargs):
        self.name = 'pp_%s' % pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
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
        post_data = {
            'id': int(time.time()),
            'service': 'account.verifySession',
            'data': {
                'sid': crypto.md5('sid=%s%s' % (session_id, self.app_key)),
            },
            'game': {
                'gameId': self.app_id,
            },
            'encrypt': 'MD5',
            'sign': '',
        }

        post_json = json.dumps(post_data)

        try:
            http_code, content = http.post(STRING_VERIFICATION_URL, data=post_json, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except ValueError:
            return None

        if str(obj.get('state', {}).get('code', 0)) != '1':
            return None

        data = obj.get('data', {})
        openid = data.get('accountId')
        creator = data.get('creator')

        return {
            'openid': openid,
            'channel': creator,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            字段名         长度          描述                          是否必须
            order_id    bigint(20)  兑换订单号                           是
            billno      varchar(30) 厂商订单号 原样返回给游戏服            是
            account     varchar(50) 通行证账号                           是
            amount      double(8,2) 兑换 PP 币数量                       是
            status      tinyint(1)  状态: 0 正常状态 1 已兑换过并成功返回   是
            app_id      int(10)     厂商应用 ID(原样返回给游戏服)           是
            uuid        char(40)    设备号(返回的 uuid 为空)              是
            roleid      varchar(30) 厂商应用角色 id(原样返回给游戏服)       是
            zone        int(10)     厂商应用分区 id(原样返回给游戏服)       是
            sign        text        签名(RSA 私钥加密)                    是
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        if str(data_dict['status']) != '0':
            return True

        try:
            context = crypto.rsa_public_decrypt(self.public_key, sign, rsa=self.rsa)
        except:
            print traceback.print_exc()
            return False

        try:
            jdata = json.loads(context)
        except ValueError:
            print traceback.print_exc()
            return False

        for k, v in jdata.iteritems():
            if force_str(v) != force_str(data_dict[k]):
                return False

        pay_data = dict(game_order_id=jdata['billno'], order_id=jdata['order_id'],
                        amount=float(jdata['amount']), uin=jdata['account'])

        return pay_data


SDKManager.register('sdk_pp', SDKPP)
