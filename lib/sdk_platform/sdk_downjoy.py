# -*- coding: utf-8 -*-
# Android系统 当乐平台

__version__ = '4.2.3'

import json
import traceback
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'downjoy': {
        'app_id': 'd8fbf84377744e0648f276db00ad8146',
        'app_key': 'fecbb61f1a52f8a9f29f0bb082803334',
        'pay_key': 'Ur2rd8rIMuWg',
    },
}


STRING_VERIFICATION_URL = 'http://ngsdk.d.cn/api/cp/checkToken'


class SDKDownjoy(object):

    SUCCESS = 'success'
    FAIL = 'failure'

    MD5_FORMAT = 'order=%(order)s&money=%(money)s&mid=%(mid)s&time=%(time)s&result=%(result)s&ext=%(ext)s&key=%(key)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.pay_key = PLATFORM_INFO.get(pf, {}).get('pay_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        openid = kwargs.get('openid')

        post_data = {
            'appid': self.app_id,
            'token': session_id,
            'umid': openid,
        }

        post_data['sig'] = crypto.md5('%s|%s|%s|%s' % (self.app_id, self.app_key, session_id, openid))

        try:
            http_code, content = http.post(STRING_VERIFICATION_URL, data=urllib.urlencode(post_data), timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except:
            return None

        if obj.get('msg_code') != 2000:
            return None

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名     含义
            result    支付结果,固定值。“1”代表成功,“0” 代表失败
            money     支付金额,单位:元,两位小数。
            order     本次支付 SDK 生成的订单号
            mid       本次支付用户的乐号,既登录后返回的 umid 参数。 最长长度 64 字符
            time      时间戳,格式:yyyymmddHH24mmss 月日小 时分秒小于 10 前面补充 0
            ext       客户端购买商品时候传入的 TransNo 字段。
            signature MD5 验证串,用于与接口生成的验证串做比 较,保证计费通知的合法性。 具体步骤见 下节:如何验证通知合法性。
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        signature = data_dict.get('signature')

        if signature is None:
            return False

        if data_dict['result'] != '1':
            return False

        data_dict['key'] = self.pay_key

        gen_sign = crypto.md5(self.MD5_FORMAT % data_dict)

        if gen_sign != signature:
            return False

        pay_data = dict(game_order_id=data_dict['ext'], order_id=data_dict['order'],
                        amount=float(data_dict['money']), uin=data_dict['mid'])

        return pay_data


SDKManager.register('sdk_downjoy', SDKDownjoy)
