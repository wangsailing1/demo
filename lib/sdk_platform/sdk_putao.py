# -*- coding: utf-8 -*-
# Android系统 葡萄平台

__version__ = 'v2.1.0'

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
    'putao': {
        'cp_id': '7',   # 游戏 CP 的唯一标识
        'cp_key': 'DCE9814ACF91FE81118BE8426A154795',   # 签名密钥
        'agentid': '',  # 运营商葡萄平台唯一分配
    },
}


STRING_VERIFICATION_URL = 'http://sdk.pt.cn:8080/gamesdk/cp.jsp'


class SDKPutao(object):

    MD5_FORMAT = 'source=%(source)s&trade_no=%(trade_no)s&amount=%(amount)s&' \
                 'partner=%(partner)s&paydes=%(paydes)s&debug=%(debug)s&' \
                 'tborder=%(tborder)s&key=%(key)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.cp_id = PLATFORM_INFO.get(pf, {}).get('cp_id', '')
        self.cp_key = PLATFORM_INFO.get(pf, {}).get('cp_key', '')
        self.agentid = PLATFORM_INFO.get(pf, {}).get('agentid', '')
        self.cache_payment = {}

    @property
    def SUCCESS(self):
        orderid = self.cache_payment.get('orderid', '')
        tstamp = self.cache_payment.get('tstamp', '')
        response = {
            'result': '1',  #//通知结果:1 成功 0 失败
            'cpid': self.cp_id,  #//游戏开发商 id 号
            'orderid': orderid,  #//sdk 服务器平台的订单号
            'tstamp': tstamp,
        }
        sign = self.result_sign(response)
        return {
            'response': response,
            'sign': sign,  #//签名
        }

    @property
    def FAIL(self):
        orderid = self.cache_payment.get('orderid', '')
        tstamp = self.cache_payment.get('tstamp', '')
        response = {
            'result': '0',  #//通知结果:1 成功 0 失败
            'cpid': self.cp_id,  #//游戏开发商 id 号
            'orderid': orderid,  #//sdk 服务器平台的订单号
            'tstamp': tstamp,
        }
        sign = self.result_sign(response)
        return {
            'response': response,
            'sign': sign,  #//签名
        }

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        get_data = {
            't': 1000,
            'agentid': self.agentid,
            'cpid': self.cp_id,
            'sid': session_id,
            'sign': crypto.md5('%s%s%s%s' % (self.agentid, self.cp_id, session_id, self.cp_key)),
        }

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

        openid = obj.get('cplogin', {}).get('uid')

        if openid is None:
            return None

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名
            t           通知消息类型: 1: 表示充值状态通知消息
            status      订单状态:   1:成功; 0:失败
            userid      平台用户 ID(唯一标识)
            cpid        游戏 CP 的唯一标识
            serverid    游戏区服(1、2、3...)
            orderid     平台订单号
            cporderid   游戏 CP 订单号
            tstamp      用以签名和验签参数
            paytype     支付类型:
            extrainfo   平台 SDK 透传的数据
            amount      成功充值金额,返回单位(RMB 分),实际 float 类型
            sign        Sign=md5 (userId+orderid+cporderid+ tstamp+amount+apikey)
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        if data_dict['status'] != 1:
            return False

        gen_sign = crypto.md5('%s%s%s%s%s%s' % (data_dict['userid'], data_dict['orderid'],
                                                data_dict['cporderid'], data_dict['tstamp'],
                                                data_dict['amount'], self.cp_key))

        if gen_sign.upper() != sign:
            return False

        self.cache_payment = {
            'orderid': data_dict['orderid'],
            'tstamp': data_dict['tstamp'],
        }

        pay_data = dict(game_order_id=data_dict['cporderid'], order_id=data_dict['orderid'],
                        amount=float(data_dict['amount']) / 100, uin=data_dict['userid'])

        return pay_data

    def result_sign(self, response):
        return crypto.md5('%s%s%s%s%s' % (response['result'], response['cpid'],
                                          response['tstamp'], response['orderid'],
                                          self.cp_key))


SDKManager.register('sdk_putao', SDKPutao)
