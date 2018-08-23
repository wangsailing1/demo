# -*- coding: utf-8 -*-
# Android系统 4399平台

__version__ = 'v2.7.1.0'

import json
import traceback
import urllib

from M2Crypto import BIO, RSA

from lib.utils import http
from lib.utils import crypto
from lib.utils.encoding import force_str
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    '4399': {
        'app_id': '',
        'app_key': '',
        'app_secret': '75b2d6c006b879c45a810334269b212f',
    },
}


STRING_VERIFICATION_URL = 'http://m.4399api.com/openapi/oauth-check.html'


class SDK4399(object):

    SUCCESS = {"status": 2, "code": None, "money": "0", "gamemoney": "0", "msg": ""}
    FAIL = {"status": 1, "code": None, "money": "0", "gamemoney": "0", "msg": ""}

    MD5_FORMAT = '%(orderid)s%(uid)s%(money)s%(gamemoney)s%(serverid)s%(app_secret)s%(mark)s%(roleid)s%(time)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_secret = PLATFORM_INFO.get(pf, {}).get('app_secret', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        openid = kwargs.get('openid')

        get_data = {
            'state': session_id,
            'uid': openid,
        }

        url = '%s?%s' % (STRING_VERIFICATION_URL, urllib.urlencode(get_data))

        try:
            http_code, content = http.get(url, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except:
            return None

        if obj.get('code') != 100:
            return None

        openid = obj.get('result', {}).get('uid')

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名             含义
            orderid         (4399生成的订单号) 22位以内的字符串 唯一
            p_type          充值渠道id
            uid             要充值的用户ID，my平台的用户uid
            money           用户充值的人民币金额，单位：元
            gamemoney       兑换的游戏币数量，兑换标准由双方共同约定，若在标准兑换比率基础上，有一些优惠或者赠送策略，
                            可无视此数据，由应用端自行计算实际的兑换数额
            serverid        要充值的服务区号(最多不超过8位)。只针对有分服的游戏有效。参数的格式为：区服id。 例如 1服 为 1, 11服为 11
            mark            作为预留字段，部分游戏在游戏内发起充值时，会生成唯一标识来标注该笔充值的相关信息时,
                            可以用本字段。（游戏方生成的订单号）
            roleid          要充值的游戏角色id，只针对pc端充值时，需要选择游戏角色的游戏有效。roleid的值由角色接口提供（见接口2）
            time            发起请求时的时间戳
            sign            加密签名
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        data_dict['app_secret'] = self.app_secret

        gen_sign = crypto.md5(self.MD5_FORMAT % data_dict)

        if gen_sign != sign:
            return False

        pay_data = dict(game_order_id=data_dict['mark'], order_id=data_dict['orderid'],
                        amount=float(data_dict['money']), uin=data_dict['uid'])

        return pay_data


SDKManager.register('sdk_4399', SDK4399)
