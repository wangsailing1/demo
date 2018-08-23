# -*- coding: utf-8 -*-
# Android IOS系统 腾讯移动应用平台

__version__ = ''

import json
import time
import traceback
import urllib
import hmac
import hashlib
import base64
import binascii

from M2Crypto import BIO, RSA
from oauth import oauth

from lib.utils import http
from lib.utils import crypto
from lib.utils.encoding import force_str
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'tencent': {
        'app_id': '1101819566',
        'app_key': '0mR2qHHdjzg7DeH9&',
    },
}


VERIFICATION_URL = 'https://openapi.tencentyun.com'
SANDBOX_VERIFICATION_URL = 'https://119.147.19.43'


class SDKTencent(object):

    SUCCESS = 'success'
    FAIL = 'fail'

    BALANCE_URL = '/mpay/get_balance_m'
    PAY_URL = '/mpay/pay_m'

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
        debug = kwargs.get('debug', False)
        token = kwargs.get('token')
        openid = kwargs.get('openid')

        get_data = {
            'appid': self.app_id,
            'openid': openid,
            'openkey': token,
            'pf': 'qzone',
            'format': 'json',
        }

        url = '%s?%s' % (VERIFICATION_URL if not debug else SANDBOX_VERIFICATION_URL, urllib.urlencode(get_data))

        try:
            http_code, content = http.get(url, timeout=3)
        except:
            return None

        if http_code != 200:
            return None

        try:
            obj = json.loads(content)
        except ValueError:
            return None

        if obj.get('ret') != 0:
            return None

        return {
            'openid': openid,
        }

    def get_balance(self, data_dict, debug=False):
        """ 获取余额

        :param data_dict:
        :param debug:
        :return:
        """
        openid = data_dict.get('openid')
        if openid is None:
            return {}

        params = {
            'openid': openid,
            'openkey': data_dict['openkey'],
            'pf': data_dict['pf'],
            'pfkey': data_dict['pfkey'],
            'pay_token': data_dict['pay_token'],
            'ts': int(time.time()),
            'zoneid': data_dict['zoneid'],
            'appid': self.app_id,
        }

        params['sig'] = self.hmac_sha1_sig('GET', self.BALANCE_URL, params, self.app_key)

        url = '%s%s?%s' % (SANDBOX_VERIFICATION_URL if debug else VERIFICATION_URL,
                           self.BALANCE_URL, urllib.urlencode(params))

        headers = {
            'Cookie': '; '.join(['session_id=openid', 'session_type=kp_actoken', 'org_loc=%s' % self.BALANCE_URL])
        }

        try:
            http_code, content = http.get(url, headers=headers, timeout=3)
        except:
            return {}

        try:
            obj = json.loads(content)
        except:
            return {}

        if obj.get('ret') != 0:
            return {}

        return obj

    def payment_verify(self, data_dict, debug=False):
        """支付验证

        :param data_dict:
            openid	从手Q登录态中获取的openid的值
            openkey	从手Q登录态中获取的access_token 的值
            pay_token	从手Q登录态中获取的pay_token的值
            appid	应用的唯一ID。可以通过appid查找APP基本信息。这个appid在数值上和支付ID也就是客户端设置的offerid是相同的
            ts	UNIX时间戳（从格林威治时间1970年01月01日00时00分00秒起至现在的总秒数）。
            sig	请求串的签名（可以参考下面具体示例，或者到wiki下载SDK）。
            pf	平台来源，平台-注册渠道-系统运行平台-安装渠道-业务自定义。
            例如： qq_m_qq-10000144-android-10000144-xxxx
            qq_m_qq 表示 手Q平台启动，用qq登录态
            zoneid	账户分区ID_角色。和PC接入时保持一致，分区可以在open.qq.com上自助配置。如过应用选择支持角色，
                    则角色接在分区ID号后用"_"连接，角色需要进行urlencode。
            注意：如果游戏PC端和移动端是游戏币互通模式，zoneid 的数值保持和PC侧接入支付时传递的一致。
            例如，游戏A在PC上运行是接入过支付，PC上有分区0和分区1，再接入移动支付是要求移动端账户和PC端账户互通，
            那么接入移动支付时，zoneid根据需要由业务自己传递PC上配置的分区ID，对0分区操作就传0，对1分区操作就传1
            amt	扣游戏币数量。
            pfkey	登录时候跳转到应用首页后，URL后会带该参数。由平台直接传给应用。
        :param debug:
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        openid = data_dict.get('openid')
        if openid is None:
            return False

        params = {
            'openid': openid,
            'openkey': data_dict['openkey'],
            'pay_token': data_dict['pay_token'],
            'appid': self.app_id,
            'ts': int(time.time()),
            'pf': data_dict['pf'],
            'zoneid': data_dict['zoneid'],
            'amt': data_dict['amt'],
            'pfkey': data_dict['pfkey'],
        }

        params['sig'] = self.hmac_sha1_sig('GET', self.PAY_URL, params, self.app_key)

        url = '%s%s?%s' % (SANDBOX_VERIFICATION_URL if debug else VERIFICATION_URL,
                           self.PAY_URL, urllib.urlencode(params))

        headers = {
            'Cookie': '; '.join(['session_id=openid', 'session_type=kp_actoken', 'org_loc=%s' % self.PAY_URL])
        }

        try:
            http_code, content = http.get(url, headers=headers, timeout=3)
        except:
            return False

        try:
            obj = json.loads(content)
        except:
            return False

        if obj.get('ret') != 0:
            return False

        return obj

    def mk_soucrce(self, method, url_path, params):
        str_params = urllib.quote("&".join(k + "=" + str(params[k]) for k in sorted(params.keys())), '')
        source = '%s&%s&%s' % (
            method.upper(),
            urllib.quote(url_path,''),
            str_params
        )
        return source

    def hmac_sha1_sig(self, method, url_path, params, secret):
        source = self.mk_soucrce(method, url_path, params)
        hashed = hmac.new(secret, source, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]


SDKManager.register('sdk_tencent', SDKTencent)
