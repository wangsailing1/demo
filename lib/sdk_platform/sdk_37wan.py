# -*- coding: utf-8 -*-
# Android系统 37玩平台, 应该用魅族的sdk, 37玩和魅族合作

__version__ = 'v2.1.2'

import json
import time
import traceback
import urllib

from M2Crypto import BIO, RSA

from lib.utils import http
from lib.utils import crypto
from lib.utils.encoding import force_str
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    '37wan': {
        'partner_id': '1',   # 联运id
        'app_id': '1002424',
        'app_key': 'E;jXR@znsg49tWP8h1C6xSDdrlpKZFfJ',
        'pay_key': 'xcnLKBj18q;5a$9TGH64UfIWtZOCmwSA',
    },
}


STRING_VERIFICATION_URL = 'http://vt.api.m.37.com/verify/token/'


class SDK37wan(object):

    SUCCESS = {"state": 1, "data": "", "msg": "" }
    FAIL = {"state": 0, "data": "", "msg": "" }

    MD5_FORMAT = '%(time)s%(key)s%(oid)s%(doid)s%(dsid)s%(uid)s%(money)s%(coin)s'

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.partner_id = PLATFORM_INFO.get(pf, {}).get('partner_id', '')
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

        today = int(time.time())

        get_data = {
            'pid': self.partner_id,
            'gid': self.app_id,
            'time': today,
            'token': session_id,
            'sign': crypto.md5('%s%s%s' % (self.app_id, today, self.app_key))
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

        if obj.get('state') != 1:
            return None

        openid = obj.get('data', {}).get('uid')

        return {
            'openid': openid,
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名             含义
            pid          联运商
            gid          游戏 ID
            time         Unix 时间戳
            sign         校验令牌
            oid          联运平台订单 ID
            doid         CP 订单 ID
            dsid         CP 游戏服 ID
            dext         CP 扩展回调参数
            drid         CP 角色 ID
            drname       CP 角色名
            drlevel      CP 角色等级
            uid          用户 UID
            money        金额,例如:1.00
            coin         游戏,例如:10
            remark       简单的备注
            paid         平台应用标识
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        data_dict['key'] = self.pay_key

        gen_sign = crypto.md5(self.MD5_FORMAT % data_dict)

        if gen_sign != sign:
            return False

        pay_data = dict(game_order_id=data_dict['doid'], order_id=data_dict['oid'],
                        amount=float(data_dict['money']), uin=data_dict['uid'])

        return pay_data


SDKManager.register('sdk_37wan', SDK37wan)
