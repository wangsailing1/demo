# -*- coding: utf-8 -*-
# Android系统 安智平台

__version__ = 'v3.5.2'

import json
import traceback
import time
import base64
import datetime
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'anzhi': {
        'app_key': '1397465227cU0kt6gcU71D7d2tr172',
        'app_secret': 'bPyCI8u0GtD9XFEnS31Mv6aB',
    },
}


STRING_VERIFICATION_URL = 'http://user.anzhi.com/web/api/sdk/third/1/queryislogin'


class SDKAnzhi(object):

    SUCCESS = 'success'
    FAIL = 'money_error'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_secret = PLATFORM_INFO.get(pf, {}).get('app_secret', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        post_data = {
            'time': datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:17],
            'appkey': self.app_key,
            'sid': session_id,
            'sign': base64.b64encode('%s%s%s' % (self.app_key, session_id, self.app_secret))
        }

        try:
            http_code, content = http.post(STRING_VERIFICATION_URL, data=urllib.urlencode(post_data), timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        if "'" in content:
            content = content.replace("'", '"')

        try:
            obj = json.loads(content)
        except:
            return None

        if int(obj.get('sc', 0)) not in (1, 200):
            return None

        json_msg = json.loads(base64.b64decode(obj['msg']))

        openid = json_msg['uid']

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名     含义
            data
                uid             安智账号id
                orderId         订单号
                orderAmount     实际付费金额(单位为分)
                orderTime       支付时间
                orderAccount    支付账号
                code            订单状态 (1 为成功)
                msg
                payAmount       订单金额(单位为分)
                cpInfo          回调信息 用户自定义参数
                notifyTime      通知时间
                memo            备注
                redBagMoney     礼券金额(单位为分)
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        data = data_dict.get('data')

        if data is None:
            return False

        des3_data = crypto.des3_decrypt(self.app_secret, data)

        des3_dict = json.loads(des3_data)

        if int(data_dict['code']) != 1:
            return False

        pay_data = dict(game_order_id=des3_dict['cpInfo'], order_id=des3_dict['orderId'],
                        amount=float(des3_dict['orderAmount']) / 100, uin=des3_dict['uid'])

        return pay_data


SDKManager.register('sdk_anzhi', SDKAnzhi)
