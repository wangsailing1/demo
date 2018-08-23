# -*- coding: utf-8 -*-
# Android系统 应用汇平台

__version__ = 'v7.0.2'

import json
import traceback
import urllib
import time
from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'yyh': {
        'login_id': 10194,                  # 登录参数
        'login_key': 'dwiaCoPMI91GtR23',    # 登录参数
        'app_id': '10040800000001100408',   # 支付参数
        'private_key': '',                  # 支付参数
        'public_key': '',                   # 支付参数
    },
}


STRING_VERIFICATION_URL = 'http://api.appchina.com/appchina-usersdk/user/v2/get.json'


class SDKYingYongHui(object):

    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.login_id = PLATFORM_INFO.get(pf, {}).get('login_id', '')
        self.login_key = PLATFORM_INFO.get(pf, {}).get('login_key', '')
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.private_key = PLATFORM_INFO.get(pf, {}).get('private_key', '')
        self.public_key = PLATFORM_INFO.get(pf, {}).get('public_key', '')
        self.public_bio = BIO.MemoryBuffer(self.public_key)
        self.public_rsa = RSA.load_pub_key_bio(self.public_bio)

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """

        get_data = {
            'ticket': session_id,
            'login_id': self.login_id,
            'login_key': self.login_key,
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
        except ValueError:
            return None

        if obj['status'] != 0:
            return None

        openid = obj.get('data', {}).get('user_id')

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            transdata:
                参数名称 参数含义
                transtype   交易类型    0–支付交易 1–支付冲正(暂未启用) 2–契约退订 3–自动续费
                cporderid   商户订单号
                transid     交易流水号
                appuserid   用户在商户应用的唯一标识
                appid       游戏id
                waresid     商品编码
                feetype     计费方式
                money       交易金额
                currency    货币类型
                result      交易结果   0 成功 1 失败
                transtime   交易完成时间
                cpprivate   商户私有信息
                paytype     支付方式
            sign:
            signtype:   RSA


        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        transdata = data_dict.get('transdata')
        json_transdata = json.loads(transdata)

        if int(json_transdata['result']) != 0:
            return False

        try:
            if not crypto.rsa_verify_signature(self.public_key, transdata, sign, md='md5', rsa=self.public_rsa):
                return False
        except:
            print traceback.print_exc()
            return False

        pay_data = dict(game_order_id=data_dict['cporderid'], order_id=data_dict['transid'],
                        amount=float(data_dict['money']), uin=data_dict['appuserid'])

        return pay_data


SDKManager.register('sdk_yyh', SDKYingYongHui)
