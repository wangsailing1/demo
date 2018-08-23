# -*- coding: utf-8 -*-
# Android IOS系统 腾讯开放平台

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
    'wechat': {     # 微信
        'app_id': 'wx86e877f7e51daff4',
        'app_key': 'd4624c36b6795d1d99dcf0547af5443d',
        'app_key_pay': 'd4624c36b6795d1d99dcf0547af5443d',
        'login_url': '/auth/check_token/',
    },
    'mpqq': {   # 手Q
        'app_id': 1104950218,
        'app_key': 'zjy3L6fVprPMkiAi',  # 沙箱appkey，用于现网和测试登录，和测试的支付
        'app_key_pay': '6iBB5jjma3mDFTr2W0g4OgNF8G7bNn0z',   # 现网appkey，用于现网的支付
        'login_url': '/auth/verify_login/',
    },
}


VERIFICATION_URL = 'http://msdk.qq.com'
SANDBOX_VERIFICATION_URL = 'http://msdktest.qq.com'


class SDKMsdk(object):

    SUCCESS = 'success'
    FAIL = 'fail'

    BALANCE_URL = '/mpay/get_balance_m'
    PAY_URL = '/mpay/pay_m'

    def __init__(self, pf, *args, **kwargs):
        self.name = 'msdk_' % pf
        self.pf = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.app_key_pay = PLATFORM_INFO.get(pf, {}).get('app_key_pay', '')
        self.login_url = PLATFORM_INFO.get(pf, {}).get('login_url', '')

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        debug = kwargs.get('debug', False)
        openid = kwargs.get('openid')

        now = int(time.time())

        if self.pf == 'wechat':  # 微信
            post_data = {
                'openid': openid,
                'accessToken': session_id,
            }
        else:  # 手机QQ
            post_data = {
                'appid': self.app_id,
                'openid': openid,
                'openkey': session_id,
            }

        get_data = {
            'appid': self.app_id,
            'timestamp': now,
            'sig': crypto.md5('%s%s' % (self.app_key, now)),
            'encode': 1,
            'openid': openid,
        }

        url = '%s%s?%s' % (VERIFICATION_URL if not debug else SANDBOX_VERIFICATION_URL,
                           self.login_url, urllib.urlencode(get_data))

        try:
            http_code, content = http.post(url, data=json.dumps(post_data), timeout=3)
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

        if self.pf == 'wechat':  # 微信
            session_type = 'wc_actoken'
            session_id = 'hy_gameid'
        else:  # 手机QQ
            session_type = 'kp_actoken'
            session_id ='openid'

        config = PLATFORM_INFO['mpqq']

        cookie = {
            'org_loc': urllib.quote(self.BALANCE_URL),
            'session_id': session_id,
            'session_type': session_type,
        }

        headers = {
            'Cookie': "; ".join('%s=%s' % (k, v) for k, v in cookie.items()),
        }

        app_key = '%s&' % (config['app_key'] if debug else config['app_key_pay'])

        now = int(time.time())

        get_data = {
            'openid': data_dict['openid'],
            'openkey': data_dict['openkey'],
            'pf': data_dict['pf'],
            'pfkey': data_dict['pfkey'],
            'pay_token': data_dict['pay_token'],
            'ts': now,
            'zoneid': data_dict['zoneid'],
            'format':'json',
            'appid': config['app_id'],
        }

        get_data['sig'] = self.hmac_sha1_sig('GET', self.BALANCE_URL, get_data, app_key)

        url = '%s%s?%s' % (VERIFICATION_URL if not debug else SANDBOX_VERIFICATION_URL,
                           self.BALANCE_URL, urllib.urlencode(get_data))

        try:
            http_code, content = http.get(url, headers=headers, timeout=3)
        except:
            return {}

        try:
            obj = json.loads(content)
        except:
            return {}

        return obj

    def payment_verify(self, data_dict, debug=False):
        """支付验证

        :param data_dict:

        :param debug:
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        if self.pf == 'wechat':  # 微信
            session_type = 'wc_actoken'
            session_id = 'hy_gameid'
        else:  # 手机QQ
            session_type = 'kp_actoken'
            session_id ='openid'

        config = PLATFORM_INFO['mpqq']

        cookie = {
            'org_loc': urllib.quote(self.PAY_URL),
            'session_id': session_id,
            'session_type': session_type,
        }
        headers = {
            'Cookie': "; ".join('%s=%s' % (k, v) for k, v in cookie.items()),
        }

        app_key = '%s&' % (config['app_key'] if debug else config['app_key_pay'])

        now = int(time.time())

        get_data = {
            'openid': data_dict['openid'],
            'openkey': data_dict['openkey'],
            'pay_token': data_dict['pay_token'],
            'pf': data_dict['pf'],
            'zoneid': data_dict['zoneid'],
            'amt': data_dict['amt'],
            'pfkey': data_dict['pfkey'],
            'appid': config['app_id'],
            'ts': now,
        }

        get_data['sig'] = self.hmac_sha1_sig('GET', config['pay'], get_data, app_key)

        url = '%s%s?%s' % (SANDBOX_VERIFICATION_URL if debug else VERIFICATION_URL,
                           self.PAY_URL, urllib.urlencode(get_data))

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


SDKManager.register('sdk_msdk', SDKMsdk)
