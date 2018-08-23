# -*- coding: utf-8 -*-
# Android系统 益玩平台

__version__ = 'v2.1.1'

import json
import traceback
import urllib

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'ewan': {
        'app_id': '10111',
        'app_key': '50npGLA3uzTaKD8P',
    },
}


STRING_VERIFICATION_URL = 'http://channellogin.supersdk.ewan.cn/verifyToken'


class SDKEwan(object):

    SUCCESS = '1'
    FAIL = '100'

    MD5_FORMAT = '%(serverid)s|%(custominfo)s|%(openid)s|%(ordernum)s|%(status)s|%(paytype)s|' \
                 '%(amount)s|%(errdesc)s|%(paytime)s|%(appkey)s'

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
        openid = kwargs.get('openid')

        get_data = {
            'openid': openid,
            'token': session_id,
            'sign': crypto.md5('%s|%s|%s' % (openid, session_id, self.app_key)),
        }

        url = '%s?%s' % (STRING_VERIFICATION_URL, urllib.urlencode(get_data))

        try:
            http_code, content = http.get(url, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        if content != 'success':
            return None

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名         含义
            serverid    游戏服务器 ID
            custominfo  客户端传入的自定义数据
            openid      合作方账号唯一标识
            ordernum    订单 ID,益玩订单系统唯一 号
            status      订单状态,1 为成功,其他为 失败
            paytype     充值类型, 详见附表 PayType
            amount      成功充值金额,单位为分
            errdesc     充值失败错误码,成功为空
            paytime     充值成功时 间,yyyyMMddHHmmss
            sign        所有参数+appkey 的 MD5
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        if data_dict['status'] != '1':
            return False

        data_dict['appkey'] = self.app_key

        gen_sign = crypto.md5(self.MD5_FORMAT % data_dict)

        if gen_sign != sign:
            return False

        pay_data = dict(game_order_id=data_dict['custominfo'], order_id=data_dict['ordernum'],
                        amount=float(data_dict['amount']) / 100, uin=data_dict['openid'])

        return pay_data


SDKManager.register('sdk_ewan', SDKEwan)
