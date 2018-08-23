# -*- coding: utf-8 -*-
# Android系统 快用汇平台

__version__ = '3.0.0'

import json
import urllib
from M2Crypto import RSA, BIO

from lib.utils import http
from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


ANDROID_VERIFICATION_URL = 'http://api.hisdk.7659.com/user/get'
ANDROID_APP_KEY = 'b34c2847b66ff6cdc9673a5a3afc3999'
IOS_VERIFICATION_URL = 'http://f_signin.bppstore.com/loginCheck.php'
IOS_APP_KEY = 'fca9fdf362af4e1f0922397ef5bb5c66'


PLATFORM_INFO = {
    'android': {
        'app_key': ANDROID_APP_KEY,
        'verification_url': ANDROID_VERIFICATION_URL,
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDF/vrPsqYJxft6g59KQAv3+VAs
OskcOTgl4NIr8ZzNKEyCWqMf/dKxuIMLV15XRNwhiMQ9rhH6o4Z7m4iwRtiExwAe
L6oYuEorhN7Z91EMfpbWgbEPyCpFDVRkQWwqIO57XGZU7wOkQqFJ9urDzIkURUoU
Bul94ZI5PUUuNfu4OwIDAQAB
-----END PUBLIC KEY-----
""",
    },
    'ios': {
        'app_key': IOS_APP_KEY,
        'verification_url': IOS_VERIFICATION_URL,
        'public_key': """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC/pr0yuoZ3mtQmcMYlvrorbwok
hqnvi5IfSRUQL8T2aKnOq47czpPjOVRwpehSWkgfJ3NrsRW9F3GdbNgej0NsQYsU
RrT+U3Gmz2MLzjkk3E8sUJJLlzkMXGdvGy2+hCH5wtHdS8GftiNDpdHtN+XyopgB
5xPdLYOpbpg7R+L+XQIDAQAB
-----END PUBLIC KEY-----
""",
    },
}


class SDKKuaiYong(object):

    SUCCESS = 'success'
    FAIL = 'failed'

    def __init__(self, pf, *args, **kwargs):
        self.name = 'kuaiyong_%s' % pf
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.verification_url = PLATFORM_INFO.get(pf, {}).get('verification_url', '')
        self.public_key = PLATFORM_INFO.get(pf, {}).get('public_key', '')
        self.bio = BIO.MemoryBuffer(self.public_key)
        self.rsa = RSA.load_pub_key_bio(self.bio)

    def login_check(self, session_id, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        token_key = session_id

        query_data = urllib.urlencode({
            'tokenKey': token_key,
            'sign': crypto.md5(self.app_key+ token_key),
        })

        http_code, content = http.post(self.verification_url, query_data)
        if http_code != 200:
            return None

        obj = json.loads(content)
        # {"code":0,"msg":"\u53c2\u6570\u9519\u8bef","data":{"guid":"s1234567890","username":"testUser"}}
        if int(obj['code']) != 0:
            return None

        return {
            'openid': obj['data']['guid'],            # 平台用户ID
        }

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数                  参数类型              参数说明
            notify_data:           String           RSA 加密的关键数据，解密后格式为：
                                                    dealseq=20130219160809567&fee=0.01&payresult=0；
                                                    其中 payresult 是支付结果：0：成功，-1：支付失败， -2 超时失败；
                                                    dealseq 是开发商交易号；
                                                    fee 是支付金额：支付成功时， 表示实际支付金额
            orderid:               String           快用平台订单号
            dealseq:               String           游戏订单号（透传，唯一开发商可以自定义的参数）
            uid:                   String           快用平台用户GUID
            subject:               String           购买物品名
            v:                     String           版本号（固定参数=1.0）
            sign:                  String           RSA 签名。签名的原串，是将收到的除去 sign 这个值之外的参数，
                                                    根据key 值做排序组成的 url 参数形式，

        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')
        notify_data = data_dict.get('notify_data')

        if not sign or not notify_data:
            return False

        public_key = self.public_key

        # 根据key做排序
        params_keys = sorted((k for k, v in data_dict.iteritems() if k != 'sign'))
        sign_values = ('%s=%s' % (k, data_dict[k]) for k in params_keys)
        sign_data = '&'.join(sign_values)
        if isinstance(sign_data, unicode):
            sign_data = sign_data.encode('utf-8')

        # 验签数据
        if not crypto.rsa_verify_signature(public_key, sign_data, sign, rsa=self.rsa):
            return False

        # 解密 notify_data
        decrypt_data = crypto.rsa_public_decrypt(public_key, notify_data, rsa=self.rsa)
        obj = dict(crypto.parse_keqv(decrypt_data))

        if int(obj["payresult"]) != 0 or data_dict['dealseq'] != obj['dealseq']:
            return False

        pay_data = dict(game_order_id=data_dict['dealseq'], order_id=data_dict['orderid'],
                        amount=float(obj['fee']), uin=data_dict['uid'])

        return pay_data


SDKManager.register('sdk_kuaiyong', SDKKuaiYong)
