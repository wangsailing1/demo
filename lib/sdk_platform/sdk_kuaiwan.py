# -*- coding: utf-8 -*-
# Android系统 快玩平台

__version__ = 'v1.6'

import json
import traceback
import urllib

from M2Crypto import BIO, RSA

from lib.utils import http
from lib.utils import crypto
from lib.utils.encoding import force_str
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'kuaiwan': {
        'app_id': '',
        'app_key': 'CJYXKW',
    },
}


STRING_VERIFICATION_URL = 'http://user.dyn.mobi.kuaiwan.com/account/session/check/'


class SDKKuaiwan(object):

    SUCCESS = {"result": "1"}
    FAIL = {"result": "-2"}

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """

        get_data = {
            'sid': session_id,
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

        if obj.get('ok') not in ('true', True):
            return None

        openid = obj.get('data', {}).get('user_id')

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名             含义
            user_id         快玩玩家通行证[int/varchar(20)]
            order_no        快玩订单号
            ext_order_num   游戏厂商订单号[varchar(30)]（可选，从游戏客户端传入）
            ext_product_id  游戏厂商产品ID[varchar(30)]（可选，从游戏客户端传入）
            money           充值RMB[int],单位元
            token           认证串
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        token = data_dict.get('token')

        if token is None:
            return False

        gen_token = crypto.md5('%s%s%s%s' % (data_dict['user_id'], data_dict['money'],
                                             data_dict['order_no'], self.app_key))

        if gen_token != token:
            return False

        pay_data = dict(game_order_id=data_dict['ext_order_num'], order_id=data_dict['order_no'],
                        amount=float(data_dict['money']), uin=data_dict['user_id'])

        return pay_data


SDKManager.register('sdk_kuaiwan', SDKKuaiwan)
