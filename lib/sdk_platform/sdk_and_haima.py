# -*- coding: utf-8 -*-
# Android系统 海马平台

___version__ = 'v1.1.9.1'

import json
import traceback
import urllib

from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'android': {
        'app_id': '35e8d09a943959ed11cb21fdefff1e28',
        'app_key': '7d7c62a77717826ced5ade62a046f816',
    },
}


VERIFY_SESSION_URL = 'http://api.haimawan.com/index.php?m=api&a=validate_token'


class SDKAndHaima(object):
    """ 海马android的sdk

    """

    SUCCESS = 'success'
    FAIL = 'fail'

    MD5_FORMAT = 'notify_time=%(notify_time)s&appid=%(app_id)s&out_trade_no=%(out_trade_no)s&' \
                 'total_fee=%(total_fee)s&subject=%(subject)s&body=%(body)s&' \
                 'trade_status=%(trade_status)s%(app_key)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = 'haima_%s' % pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """

        post_data = {
            'appid': self.app_id,
            't': session_id,
        }

        post_json = urllib.urlencode(post_data)

        try:
            http_code, content = http.post(VERIFY_SESSION_URL, data=post_json, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        if content != 'success':
            return None

        return {}

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名             含义                        备注
            notify_time     通知时间                    格式为yyyy-MM-dd HH:mm:ss
            appid           应用id                     应用的appid
            out_trade_no    订单号String(64)            开发者的订单号
            total_fee       总金额                      该笔订单的总金额, 单位元
            subject         商品名称String(256)         请求时对应的参数
            body            游戏名或商品详情String(400)  请求时的body参数
            trade_status    交易状态                    0 未支付 1 支付成功 2 请求订单失败 3 签名失败 4 支付失败 5 其他失败
            sign            验证签名
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        data_dict['appid'] = self.app_id
        data_dict['app_key'] = self.app_key

        try:
            gen_sign = crypto.md5(self.MD5_FORMAT % data_dict)
        except:
            print traceback.print_exc()
            return False

        if gen_sign != sign:
            return False

        if str(data_dict['trade_status']) != '1':
            return False

        pay_data = dict(game_order_id=data_dict['out_trade_no'], order_id=data_dict['out_trade_no'],
                        amount=float(data_dict['total_fee']), uin='')

        return pay_data


SDKManager.register('sdk_and_haima', SDKAndHaima)
