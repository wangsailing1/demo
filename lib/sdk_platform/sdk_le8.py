# -*- coding: utf-8 -*-
# Android系统 乐8平台

__version__ = '1.1.0'

import json
import traceback
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'le8': {
        'app_id': 'd8fbf84377744e0648f276db00ad8146',
        'app_key': 'fecbb61f1a52f8a9f29f0bb082803334',
    },
}


STRING_VERIFICATION_URL = 'http://api.le890.com/index.php?m=api&a=validate_token'


class SDKLe8(object):

    SUCCESS = 'success'
    FAIL = 'failure'

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
        post_data = {
            'appid': self.app_id,
            't': session_id,
        }

        try:
            http_code, content = http.post(STRING_VERIFICATION_URL, data=urllib.urlencode(post_data), timeout=3)
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
            参数名     含义              备注
            n_time    通知时间          yyyy-MM-dd HH:mm:ss
            appid     应用id           应用的appid
            o_id      开发者订单号      需保证在商户网站中的唯一性. (此项是您在sdk中传入的订单号)
            t_fee     订单金额          该笔订单的总金额. 请求时对应的参数,原样通知回来。
            g_name    商品名称          是请求时对应的参数,原样返回
            g_body    商品详情/游戏名    对应请求时的body参数,原样返回
            t_status  交易状态          0 未支付 1 支付成功 2 请求订单失败 3 签名失败 4 支付失败 5 其他失败
            o_sign    验证签名
            u_param Y 开发者自定义参数   不参与sign验证
            o_orderid SDK平台订单号     不参与sign验证
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        o_sign = data_dict.get('o_sign')

        if o_sign is None:
            return False

        if data_dict['t_status'] != '1':
            return False

        data_dict['appkey'] = self.app_key

        sign_content = "n_time=%(n_time)s&appid=%(appid)s&o_id=%(o_id)s&" \
                       "t_fee=%(t_fee)s&g_name=%(g_name)s&g_body=%(g_body)s&" \
                       "t_status=%(t_status)s%(appkey)s" % data_dict

        gen_sign = crypto.md5(sign_content)

        if gen_sign != o_sign:
            return False

        pay_data = dict(game_order_id=data_dict['o_id'], order_id=data_dict['o_orderid'],
                        amount=float(data_dict['t_fee']), uin='')

        return pay_data


SDKManager.register('sdk_le8', SDKLe8)
