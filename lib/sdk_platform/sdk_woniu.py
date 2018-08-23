# -*- coding: utf-8 -*-
# Android系统 蜗牛平台

__version__ = '0.0.2'

import json
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

APPID = 5415
ACT = 4
VERIFY_URL = 'http://api.app.snail.com/store/platform/sdk/ap'

PLATFORM_INFO = {
    'woniu': {
        'app_key': 'ZmgycykIWwYF',
        'app_id': APPID,
        'act': ACT,
        'verify_url': VERIFY_URL,
    },
}


class SDKWoniu(object):

    SUCCESS = {'ErrorCode': '0', 'ErrorDesc': ''}
    FAIL = {'ErrorCode': '1', 'ErrorDesc': ''}

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.act = PLATFORM_INFO.get(pf, {}).get('act', '')
        self.verify_url = PLATFORM_INFO.get(pf, {}).get('verify_url', '')

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

        sourceStr = self.app_id + self.act + openid + session_id + self.app_key
        sign = crypto.md5(sourceStr.encode('utf-8'))

        query_str = urllib.urlencode({
            'AppId': self.app_id,
            'Act': self.act,
            'Uin':openid,
            'SessionId': session_id,
            'Sign': sign,
        })

        url = '%s?%s' % (self.verify_url, query_str)
        http_code, content = http.get(url, timeout=5)

        if http_code != 200:
            return None

        obj = json.loads(content)
        if obj.get('ErrorCode') != '1':
            return None

        return {
            'openid': openid,            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数                  字段说明
            AppId               应用 ID
            Act                 1
            ProductName         游戏名称,encode￼
            ConsumeStreamId     消费流水号,encode
            CooOrderSerial      商户订单号,encode
            Uin                 蜗牛账号 ID
            GoodsId             商品 ID
            GoodsInfo           商品名称(比如点数),encode
            GoodsCount          商品数量
            OriginalMoney       原始总价(格式:0.00) 蜗牛币
                                注: 客户端 API 中的 setProductPrice 方法
            OrderMoney          实际总价(格式:0.00) 游戏点数
            Note                即支付描述(客户端 API 参数中的 payDesc 字段)购 买时客户端应用通过 API 传入,原样返回给应用服务器 开发者可以利用该字段,定义自己的扩展数据。例如区 分游戏服务器,encode
            PayStatus           支付状态:0=失败,1=成功
            CreateTime          创建时间(yyyy-MM-dd HH:mm:ss) ,encode
            Sign                以上参数的 MD5 值,其中 AppKey 为平台分配的应 用密钥
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        if data_dict['sign']:
            return False

        sign = data_dict['sign']
        sign_keys = ('AppId','Act', 'ProductName', 'ConsumeStreamId', 'CooOrderSerial', 'Uin', 'GoodsId', 'GoodsInfo',
                     'GoodsCount', 'OriginalMoney', 'OrderMoney', 'Note', 'PayStatus', 'CreateTime')
        sign_values = [str(data_dict[key]) for key in sign_keys if data_dict[key]]
        sign_values.append(self.app_key)
        sign_str = ''.join(sign_values)

        # 通过md5算法为签名字符串生成一个md5(小写)
        new_sign = crypto.md5(sign_str.encode('utf-8'))
        if new_sign != sign:
            return False

        pay_data = dict(game_order_id=data_dict['CooOrderSerial'], order_id=data_dict['ConsumeStreamId'],
                        amount=float(data_dict['OriginalMoney']), uin=data_dict['Uin'])

        return pay_data


SDKManager.register('sdk_woniu', SDKWoniu)
