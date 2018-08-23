# -*- coding: utf-8 -*-
# IOS系统 91平台

__version__ = ''

import json
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

LOGIN_ACT_ID = 4
PAYMENT_ACT_ID = 1
APP_ID = '113291'
APP_KEY = 'd6173358a689e6b3067d4f39aba33b8416ea4dabf67167d7'
VERIFY_SESSION_URL = 'http://service.sj.91.com/usercenter/AP.aspx'

PLATFORM_INFO = {
    '91': {
        'app_key': APP_KEY,
        'app_id': APP_ID,
        'verify_url': VERIFY_SESSION_URL,
        'login_act_id': LOGIN_ACT_ID,
        'payment_act_id': PAYMENT_ACT_ID,
    },
}


class SDK91(object):

    SUCCESS = {"ErrorCode":"1","ErrorDesc": ""}
    FAIL = {"ErrorCode":"0","ErrorDesc": ""}

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.verify_url = PLATFORM_INFO.get(pf, {}).get('verify_url', '')
        self.login_act_id = PLATFORM_INFO.get(pf, {}).get('login_act_id', '')
        self.payment_act_id = PLATFORM_INFO.get(pf, {}).get('payment_act_id', '')

    def login_check(self, session_id, *args, **kwargs):
        """
        登录验证
        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        openid = kwargs.get('openid')
        if not openid:
            return False

        sign_str = "%s%s%s%s%s" % (self.app_id, self.login_act_id,
                                   openid, session_id, self.app_key)
        sign = crypto.md5(sign_str)

        query_data = urllib.urlencode({
            'AppId': self.app_id,
            'Act': self.login_act_id,
            'Uin': openid,
            'SessionID': session_id,
            'Sign': sign,
        })
        url = '%s?%s' % (self.verify_url, query_data)
        http_code, content = http.get(url)

        if http_code != 200:
            return None

        obj = json.loads(content)

        # 错误码(0=失败，1=成功(SessionId 有效)，2= AppId 无效，3= Act无效，4=参数无效，5= Sign 无效，11=SessionId 无效
        if int(obj['ErrorCode']) != 1:
            return None

        return {
            'openid': openid,            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数              备注
            AppId:           应用 ID，对应游戏客户端中使用的 APPID
            Act:             固定值1
            ProductName:     应用名称
            ConsumeStreamId: 消费流水号
            CooOrderSerial:  商户订单号， 自定义格式
            Uin:             91 账号 ID
            GoodsId:         商品 ID
            GoodsInfo:       商品名称
            GoodsCount:      商品数量
            OriginalMoney:   原始总价(格式：0.00)
            OrderMoney:      实际总价(格式：0.00)
            Note:            即支付描述（自定义格式）
            PayStatus:       支付状态：0=失败，1=成功
            CreateTime:      创建时间(yyyy-MM-dd HH:mm:ss)
            Sign:            签名,­‐将以上参数加 key 后得到的签名
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        data_dict['AppKey'] = self.app_key

        pre_sign = ("%(AppId)s"
                    "%(Act)s"
                    "%(ProductName)s"
                    "%(ConsumeStreamId)s"
                    "%(CooOrderSerial)s"
                    "%(Uin)s"
                    "%(GoodsId)s"
                    "%(GoodsInfo)s"
                    "%(GoodsCount)s"
                    "%(OriginalMoney)s"
                    "%(OrderMoney)s"
                    "%(Note)s"
                    "%(PayStatus)s"
                    "%(CreateTime)s"
                    "%(AppKey)s") % data_dict

        new_sign = crypto.md5(pre_sign.encode('utf-8'))
        if new_sign != data_dict['Sign']:
            return None

        # 支付状态：0=失败，1=成功
        if int(data_dict['PayStatus']) != 1:
            return None

        pay_data = dict(game_order_id=data_dict['CooOrderSerial'], order_id=data_dict['ConsumeStreamId'],
                        amount=float(data_dict['OrderMoney']), uin=data_dict['Uid'])

        return pay_data


SDKManager.register('sdk_91', SDK91)
