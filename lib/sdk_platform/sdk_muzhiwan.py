# -*- coding: utf-8 -*-
# Android系统 拇指玩平台

___version__ = '3.2.1.5'

import json
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

APP_KEY = 'b0e4070df58e1e47d7618f8b1ea6b20a'
VERIFY_SESSION_URL = 'http://sdk.muzhiwan.com/oauth2/getuser.php'

PLATFORM_INFO = {
    'muzhiwan': {
        'app_key': APP_KEY,
        'verify_session_url': VERIFY_SESSION_URL,
    },
}


class SDKMuzhiwan(object):

    SUCCESS = 'SUCCESS'
    FAIL = 'NOT SUCCESS'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.verify_session_url = PLATFORM_INFO.get(pf, {}).get('verify_session_url', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        query_data = urllib.urlencode({
            'token': session_id,
            'appkey': self.app_key,
        })
        url = '%s?%s' % (self.verify_session_url, query_data)
        try:
            # 对方服务器不稳定
            http_code, content = http.get(url)
        except:
            return None

        if http_code != 200:
            return None

        # {"code”:”1”,"msg”:””,”user”:{"username”:””,"uid”:””,"sex”:0,"mail”:””,"icon”:””}}
        obj = json.loads(content)
        if int(obj['code']) != 1:
            return None

        return {
            'openid': obj['user']['uid'],
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数              类型      说明
            appkey	        字符串	游戏唯一标记
            orderID	        字符串	订单唯一标记
            productName	    字符串	商品名称
            productDesc	    字符串	商品描述
            productID	    字符串	商品ID
            money	        字符串	金额，元为单位
            uid	            字符串	充值用户ID
            extern	        字符串	扩展域
            sign            字符串   签名
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign_sort_keys = ('appkey', 'orderID', 'productName', 'productDesc', 'productID',
                          'money', 'uid', 'extern')
        sign_values = [data_dict[k].encode('utf-8') if isinstance(data_dict[k], unicode) else data_dict[k]
                       for k in sign_sort_keys]
        sign_values.append(self.app_key)
        sign_str = ''.join(sign_values)
        new_sign = crypto.md5(sign_str)
        if new_sign != data_dict['sign']:
            return False

        pay_data = dict(game_order_id=data_dict['extern'], order_id=data_dict['orderID'],
                        amount=float(data_dict['money']), uin=data_dict['uid'])

        return pay_data


SDKManager.register('sdk_muzhiwan', SDKMuzhiwan)
