# coding: utf-8

from helper import http
from helper import utils
import json
import urllib
import time
import hmac
import random
import hashlib
from lib.utils.debug import print_log

__VERSION__ = '3.0.0'
PLATFORM_NAME = 'oppo'
APP_ID = '3575727'
APP_KEY = '7RIyopMhD1ooO8sc4k0cS4cKK'
APP_SECRET = '4736fCbE51837c51096Ed4ad16715e0F'
APP_RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCmreYIkPwVovKR8rLHWlFVw7YD
fm9uQOJKL89Smt6ypXGVdrAKKl0wNYc3/jecAoPi2ylChfa2iRu5gunJyNmpWZzl
CNRIau55fxGW0XEu553IiprOZcaw5OuYGlf60ga8QT6qToP0/dpiL/ZbmNUO9kUh
osIjEu22uFgR+5cYyQIDAQAB
-----END PUBLIC KEY-----"""
GET_USERINFO_URI = 'http://i.open.game.oppomobile.com/gameopen/user/fileIdInfo?'
REQUEST_METHOD = 'GET'
# 返回数据0是成功的数据，1是失败的数据
RETURN_DATA = {
    0: 'result=OK&resultMsg=SUCCESS',
    1: 'result=FAIL&resultMsg=signerror',
}


def login_verify(req, oauth_token=None, oauth_token_secret=None):
    """用户会话验证
    Args:
        oauth_token: oauth_token
        oauth_token_secret: oauth_token_secret
    Returns:
        用户标识ID
    """
    if not oauth_token:
        oauth_token = req.get_argument('session_id')
    if not oauth_token_secret:
        oauth_token_secret = req.get_argument('token_secret')
    oauth_token_secret = oauth_token_secret.replace(' ', '+')
    oauth_token_secret = urllib.quote(oauth_token_secret, 'utf-8')
    oauth_token = urllib.quote(oauth_token,'utf-8')
    token = 'fileId={}&token={}'.format(oauth_token, oauth_token_secret)
    sign_values = [
        'oauthConsumerKey=' + APP_KEY,
        'oauthToken=' + urllib.quote(oauth_token),
        'oauthSignatureMethod=HMAC-SHA1',
        'oauthTimestamp=' + str(int(time.time())),
        'oauthNonce=' + str(random.randint(1, 1000)),
        'oauthVersion=1.0&'
    ]

    basestr = '&'.join(sign_values)
    sign = urllib.quote(oppo_make_sign(basestr))
    headers = {
        'param': basestr,
        'oauthSignature': sign
    }
    http_code, content = http.get(GET_USERINFO_URI+token, headers=headers, timeout=15)
    if http_code != 200:
        return None

    obj = json.loads(content)
    if obj['resultCode'] != '200':
        return None
    return {
        'openid': obj['ssoid'],           # 平台用户ID
    }


def payment_verify(req, params=None):
    """支付回调验证，app_order_id为自定义
    Args:
        params: 字典参数数据
            notifyId:     回调通知ID（该值使用系统为这次支付生成的订单号）
            partnerOrder: 开发者订单号（客户端上传）
            productName:  商品名称（客户端上传）
            productDesc:  商品描述（客户端上传）
            price:        商品价格(以分为单位)
            count:        商品数量（一般为1）
            attach:       请求支付时上传的附加参数（客户端上传）
            sign:         签名
    Returns:
        支付数据
    """
    print_log("in oppo payment_verify req is: %s" % req)
    if not params:
        params = {
            'notifyId':     req.get_argument('notifyId'),
            'partnerOrder': req.get_argument('partnerOrder'),
            'productName':  req.get_argument('productName'),
            'productDesc':  req.get_argument('productDesc', ''),
            'price':        int(req.get_argument('price', '')),
            'count':        int(req.get_argument('count')),
            'attach':       req.get_argument('attach'),
            'sign':         req.get_argument('sign'),
        }
    print_log("in oppo payment_verify params is: %s" % params)
    sign_keys = ('notifyId', 'partnerOrder', 'productName', 'productDesc',
                 'price', 'count', 'attach')
    sign_values = ('%s=%s' % (k, params[k]) for k in sign_keys)
    sign_data = '&'.join(sign_values).encode('utf-8')
    print_log("in oppo payment_verify sign_data is: %s" % sign_data)
    if not utils.rsa_verify_signature(APP_RSA_PUBLIC_KEY, sign_data, params['sign']):
        print_log("in oppo payment_verify sign_error")
        return RETURN_DATA, None

    pay_data = {
        'app_order_id':  params['attach'],           # 自定义定单id
        'order_id':      params['notifyId'],                # 平台定单id
        'platform':      PLATFORM_NAME,                    # 平台标识名
        'real_price':    float(params['price']) / 100,      # 实际充值人民币数　单位元
        'uid': '',
    }
    return RETURN_DATA, pay_data


def oppo_make_sign(msg):
    """制作签名 按字母顺序排序 使用hmac-sha1
    Args:
        params: 要签名的字典数据
    Returns:
        hmac-sha1签名
    """
    return hmac.new(APP_SECRET+'&', msg.encode('utf-8'), hashlib.sha1).digest().encode('base64').rstrip()


if __name__ == '__main__':
    print login_verify(None, 'TOKEN_bni9yI4FaMFp3lvi5kp7sEa6PRX8s6UUlNd3RXsyGgMz441oR5K75A%25253D%25253D', '103608866')
