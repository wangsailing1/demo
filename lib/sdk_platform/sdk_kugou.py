# -*- coding: utf-8 -*-
# Android系统 酷狗平台

__version__ = '5.4.3'

import json
import urllib
import time

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

APP_KEY = 'ZfHkdP6YfTGMNWzIQ3GPTvi89zcLUVnn'
APPID = 5415
PAY_KEY = '3e9e9bd5b3bc4fa82a942b8c601aefcb'
MerchantId = 1
VERIFY_URL = 'http://sdk.game.kugou.com/index.php?r=ValidateIsLogined/CheckToken'

PLATFORM_INFO = {
    'kugou': {
        'app_key': APP_KEY,
        'app_id': APPID,
        'pay_key': PAY_KEY,
        'MerchantId': MerchantId,
        'verify_url': VERIFY_URL,
    },
}


class SDKKugou(object):

    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.pay_key = PLATFORM_INFO.get(pf, {}).get('pay_key', '')
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.merchant_id = PLATFORM_INFO.get(pf, {}).get('MerchantId', '')
        self.verify_url = PLATFORM_INFO.get(pf, {}).get('verify_url', '')

    def login_check(self, session_id, *args, **kwargs):
        """
        登录验证
        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        sign_str = self.merchant_id + self.app_id + session_id + int(time.time()) + self.app_key
        token = crypto.md5(sign_str)
        url = '%s&token=%s' % (self.verify_url, token)
        http_code, content = http.get(url)

        if http_code != 200:
            return None

        data = json.loads(content)
        if data['response']['code'] != '0':
            return None

        return {
            'openid': session_id,            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数             类型                   字段说明
            orderid     	long	            平台订单号（联运平台唯一订单号）
            outorderid	    String	            游戏厂商订单号(游戏厂商需保证订单唯一性) (回调时url编码)
            amount	        int	                充值金额(人民币)，以此值兑换游戏币。单位（元）
            username	    string	            平台帐号(回调时url编码)
            status	        Int	                是否扣费成功.1:成功,0:不成功
            time	        int	                发起请求时间，Unix时间戳
            ext1	        String	            扩展字段1,原样传回(回调时url编码)
            ext2	        String	            扩展字段2,原样传回(回调时url编码)
            sign	        string	            "签名验证，md5后的结果小写
                                                md5(orderid+outorderid+amount+username+status+time+ext1+ext2+key)
            注：

            1. key为联运接口密钥，由平台提供对接时找平台技术取
            2.此处”+”号为连接符,不参与加密，不同语言使用不同的连接符，如php为”.”;"
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        if int(data_dict['status']) != 1:
            return False

        data_dict['key'] = self.pay_key

        sign_str = ('%(orderid)s'
                    '%(outorderid)s'
                    '%(amount)s'
                    '%(username)s'
                    '%(status)s'
                    '%(time)s'
                    '%(ext1)s'
                    '%(ext2)s'
                    '%(key)s') % data_dict

        new_sign = crypto.md5(sign_str.encode('utf-8'))
        if new_sign != data_dict['sign']:
            return False

        pay_data = dict(game_order_id=data_dict['outorderid'], order_id=data_dict['orderid'],
                        amount=float(data_dict['amount']), uin=data_dict['username'])

        return pay_data


SDKManager.register('sdk_kugou', SDKKugou)
