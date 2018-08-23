# -*- coding: utf-8 -*-
# Android系统 YY平台

__version__ = '3.2.1'

import json
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager

APPID = 5415
VERIFY_URL = 'http://uaas.yy.com/otp/check'

PLATFORM_INFO = {
    'yy': {
        'app_key': 'ZmgycykIWwYF',
        'app_id': APPID,
        'verify_url': VERIFY_URL,

    },
}


class SDKYy(object):

    SUCCESS = 'success'
    FAIL = 'fail'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.verify_url = PLATFORM_INFO.get(pf, {}).get('verify_url', '')

    def login_check(self, session_id, *args, **kwargs):
        """
        登录验证
        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        token = kwargs.get('token')
        if not token:
            return False

        url = '%s/%s/%s/%s' % (self.verify_url, self.app_id, session_id, token)

        http_code, content = http.get(url, timeout=5)
        if http_code != 200:
            return None

        obj = json.loads(content)
        # {"appId":5415,"sign":"", "data":{"code": 1,"udbuid":"1105846919"}}
        if int(obj['data']['code']) != 1:
            return None

        return {
            'openid': obj['data']['udbuid'],            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数                  字段说明            参数类型              必填            备注
            appId                   业务ID            string(12)          Y               由支付平台分配
            sign                    签名              string              Y
            data                    数据集合           string              Y            Json格式，包括所有的响应数据，对象属性如下
                statusCode          状态码             string              Y
                statusMsg           状态描述           string              N
                appOrderId          业务订单号         string              Y             业务订单号
                payId               订单唯一流水号      string              Y              营收充值服务中的唯一订单号
                prodId              产品ID            string               Y              便于交易查询使用，业务方可自定义，建议不要用纯数字。
                prodName            产品名称            string             Y                用户支付时能看到对应的商品名
                amount              需要支付的总金额     string             Y               精确到小数点后两位（元）
                unit                金额的单位          String(20)         Y                 取值范围（RMB：人民币、USD：美元、YB：Y币）
                openId              用户开放ID          String(21)         N                用户开放ID
                ext                 扩展字段            String(2000)       N                扩展字段，该字段在支付时作为自定义字段传入，营收充值服务不会处理该字段
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        if data_dict['sign']:
            return False

        sign = data_dict['sign']
        data = data_dict['data']
        data = urllib.unquote(data)
        sign_str = "appId=%s&data=%s&key=%s" % (self.app_id, data, self.app_key)

        new_sign = crypto.md5(sign_str.encode('utf-8'))
        if sign != new_sign:
            return False

        data = json.loads(data)

        if data['statusCode'] != 'CODE_SUCCESS':
            return False

        pay_data = dict(game_order_id=data['appOrderId'], order_id=data['payId'],
                        amount=float(data['amount']), uin=data['openId'], currency=data['unit'])

        return pay_data


SDKManager.register('sdk_yy', SDKYy)
