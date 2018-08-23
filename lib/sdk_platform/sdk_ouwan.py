# -*- coding: utf-8 -*-
# Android系统 偶玩平台

__version__ = '3.56'

import json
import urllib
from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

SERVER_SECRET = '9957aed20197defc'

PLATFORM_INFO = {
    'ouwan': {
        'server_secret': SERVER_SECRET,
    },
}


class SDKOuwan(object):

    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.server_secret = PLATFORM_INFO.get(pf, {}).get('server_secret', '')

    def login_check(self, session_id, *args, **kwargs):
        """
        登录验证
        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        openid = kwargs.get('openid')
        timestamp = kwargs.get('token')
        sign = kwargs.get('session_id')

        sign_str = openid + '&' + timestamp + '&' + self.server_secret

        new_sign = crypto.md5(sign_str)
        if sign != new_sign:
            return None

        return {
            'openid': openid,            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数                字段说明
            serverId            充值的时候传入的ID
            callbackInfo        SDK调用充值时传入的透传
            openId              充值用户标识ID
            orderId             偶玩订单唯一ID
            orderStatus         充值状态
            payType             用户支付方式
            amount              用户充值金额
            remark              错误信息
            sign                签名

        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        if data_dict['sign'] is None:
            return False

        sign_list = ['%s=%s' % (k, v) for k, v in data_dict.iteritems() if k != 'sign']
        sign_list = sorted(sign_list)
        sign_str = ''.join(sign_list) + self.server_secret

        # 通过md5算法为签名字符串生成一个md5(小写)
        new_sign = crypto.md5(sign_str)

        if new_sign != data_dict['sign']:
            return False

        pay_data = dict(game_order_id=data_dict['callbackInfo'], order_id=data_dict['orderId'],
                        amount=float(data_dict['amount']), uin=data_dict['callbackInfo'].split('-')[0])

        return pay_data


SDKManager.register('sdk_ouwan', SDKOuwan)
