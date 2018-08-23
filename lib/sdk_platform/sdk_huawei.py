
# coding: utf-8

from helper import utils
import urllib

# 平台名字
PLATFORM_NAME = 'huawei'
# 平台分配的app_id
APP_ID = '100052539'
# 平台分配的支付ID（原昵称）
PAYMENT_ID = '900086000034074192'
# 平台分配的rsa公钥
APP_RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxpsjxh4IipiCVO2zEolU
WLY4ukGtJwksXGE+5/gpa1hyGtEKt9g6VnzcKvtzLNgwjiSCLxKq1zb6aaZVq5oT
RIzUfKgP/x9EUNMALORTwnfJiCijF+oZSHo7U94ovBMJqUH5GqVahYZxzonf52oL
SB931nayiIVa4bnDwIUKnBe2jSqrKUcaM2zjtcHO90Pk18pQutzUAkkP5ubUPQuQ
Fwi1Lybzgv6sZ2TwOtkYNGwi176JQk+K2sCD/PzVSIkGUKuDxfoeDl0gDbPkR+ew
BTLSWp6ujxCPNsxTt3KWGC7k7eFETZLdhD1Jh3LJXV/0lrxcEG6yzkqGyIHqSSWp
awIDAQAB
-----END PUBLIC KEY-----"""

APP_RSA_PRIVATE_KEY = """
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDGmyPGHgiKmIJU
7bMSiVRYtji6Qa0nCSxcYT7n+ClrWHIa0Qq32DpWfNwq+3Ms2DCOJIIvEqrXNvpp
plWrmhNEjNR8qA//H0RQ0wAs5FPCd8mIKKMX6hlIejtT3ii8EwmpQfkapVqFhnHO
id/nagtIH3fWdrKIhVrhucPAhQqcF7aNKqspRxozbOO1wc73Q+TXylC63NQCSQ/m
5tQ9C5AXCLUvJvOC/qxnZPA62Rg0bCLXvolCT4rawIP8/NVIiQZQq4PF+h4OXSAN
s+RH57AFMtJanq6PEI82zFO3cpYYLuTt4URNkt2EPUmHcsldX/SWvFwQbrLOSobI
gepJJalrAgMBAAECggEBAIVXqegdR/zNskuVH/KlE2VQSrv61mdsCEWp4NNb0WtK
AaoxibGvUlO5FxUgp86HA+qbZnB2Zw+B0RTX4ZMKKj+PEibzq3HNq09cqzR4xCe/
xyZMqlunB/yaXHTNpqnHWmgybC5QsHsPrh9OgG7dyt9MiWgLX4i7iC4fS+dZK6tq
LS+1RAFW6wZTpmTbDz//1TL87WaR7/dI/2xSCYUDxb6IJyNvgVba4tGzRx+miIGS
2GpsZviDNE7DEDWxzRRrdNXpYr9RGcv6H+tuFTiWfMxakXjuBcVKsfcVsqzC7pY4
sq4rrOquiawH+XCx+PN3Otwp8pbqtlMx+X3dTjgjKRECgYEA7ViIJJAZANLlVQKM
URZnM8qZ6grgzPSZkLrn+MgdTkOiLq2U1Q0Rdd/My7lErNoiz4FCrUqYkuT8XNzN
jhwk06jBIh1uTXeSn+5JQJnLQSSRgYycG5kD45164JPhDT/FEOlySbQhwPFL2m2N
NqV+ilzSgPyeShOpe4xehWYQT0kCgYEA1jcmxY7KG6aHQyfRRnMQOI4QXtj+c1fx
BvOfLK6n2rR0cy5UBLgxYRFdevCFNEjCqrY0FGW7pzYlh5oeinI75Q72q9KigqZl
PmYYHkG3eGKUeGw5JK8Z+wK/vnHyGziFJP5i8NuemFaKy4dTeOmlpmliU2O/HFI0
eZ8oJZ52jxMCgYEA6kr4qc8tP2jwRcisJueMnM2kvipa2zeh2AMJNsakVzvgf1+O
ifnKgKeaDIkox9DViC07WsFGd8tfa3Pz3hLeL6pobHrNBd/Bd+rLmN+4iufEUzQw
bfXQpwIv6D1SbbfDmvw3e5Y7s7D+hfKa8ZTQo1kZ24aD4vAh3/oi3GByPTECgYAx
uON6/8XR3TmQUPG2lIazWeZa3atSQptjrbDIwlGb5j8RbTN7VPXBPjKgkquYkzr8
PQahpWuFSIA1lYR5RkK4zFxdTasDAHSHo1L90usvOlKUESrCZRJ2vRCct/4ma1wc
Vh/JIHETkyLsUyEA89rLYbK9AG4fuMUNZe//q2SBmQKBgEOX50iGDmKIXu+52Tkw
pPauZYGtHxHcDtoGHgIs8uBVtLKPt28gKomhKLIgX2Kq8h9QckSxkJJKw4nHjnFW
lWZ5P/gB1/ND0DBpC/xMqf3q2Xthuj73OccE6c6qSQ0nsK51x5sUdNT2LuufqTQk
f7nr4yCnk+0LRUsMHiRpWuC3
"""


LOGIN_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmKLBMs2vXosqSR2rojMz
ioTRVt8oc1ox2uKjyZt6bHUK0u+OpantyFYwF3w1d0U3mCF6rGUnEADzXiX/2/Rg
LQDEXRD22er31ep3yevtL/r0qcO8GMDzy3RJexdLB6z20voNM551yhKhB18qyFes
iPhcPKBQM5dnAOdZLSaLYHzQkQKANy9fYFJlLDo11I3AxefCBuoG+g7ilti5qgpb
km6rK2lLGWOeJMrF+Hu+cxd9H2y3cXWXxkwWM1OZZTgTq3Frlsv1fgkrByJotDpR
e8SwkiVuRycR0AHsFfIsuZCFwZML16EGnHqm2jLJXMKIBgkZTzL8Z+201RmOheV4
AQIDAQAB
-----END PUBLIC KEY-----"""

# 用access_token获取用户信息URL
GET_USERINFO_URI = 'https://api.vmall.com/rest.php?'
NSP_SVC = 'OpenUP.User.getInfo'
# 支付验证成功返回数据0
# 支付验证失败返回数据1
RETURN_DATA = {
    0: {'result': 0},
    1: {'result': 1},
}


def login_verify(req, access_token=None):
    """用户会话验证
    Args:
        access_token: access_token
        user_id: open_id
    Returns:
        用户标识ID
    """
    from lib.utils.debug import print_log
    player_id = req.get_argument('user_id', '')
    print_log('------22222--login_verify----  %s' % player_id)
    if not player_id:
        return None
    return {
        'openid': player_id,
    }


def payment_verify(req, params=None):
    """支付回调验证，requestId为自定义
    Args:
        params: 字典参数数据
            result: 支付结果“0”，表示支付成功
            userName:   开发者社区用户名或联盟用户编号
            productName: 商品名称
            payType:    支付类型
            amount:     商品支付金额 (格式为：元.角分，最小金额为分， 例如：20.00)
            orderId:    华为订单号
            notifyTime: 通知时间。 (自 1970 年 1 月 1 日 0 时起的毫秒数)
            requestId:  开发者支付请求 ID，原样返回
            orderTime:  下单时间 yyyy-MM-dd hh:mm:ss
            tradeTime: 交易/退款时间 yyyy-MM-dd hh:mm:ss
            accessMode: 接入方式
            spending: 渠道开销，保留两位小数，单位元。
            sign:       RSA 签名
    Returns:
        支付数据
    """
    if not params:
        params = req.request.body

    params = dict(utils.parse_cgi_data(params))
    if 'sign' not in params:
        return RETURN_DATA, None

    params['sign'] = urllib.unquote(params['sign'])
    if params.get('sysReserved', ''):
        params['sysReserved'] = urllib.unquote(params['sysReserved'])
    if params.get('extReserved', ''):
        params['extReserved'] = urllib.unquote(params['extReserved'])
    signType = params.pop('signType', '')
    params_keys = sorted((k for k, v in params.iteritems() if v and k != 'sign'))
    sign_values = ('%s=%s' % (k, params[k]) for k in params_keys)
    sign_data = '&'.join(sign_values)
    # if not utils.rsa_verify_signature(APP_RSA_PUBLIC_KEY, sign_data, params['sign'], md='sha256'):
    if not utils.rsa_verify_sign(sign_data, params['sign'], APP_RSA_PUBLIC_KEY):
        return RETURN_DATA, None

    pay_data = {
        'app_order_id': params['requestId'],  # 自定义定单id
        'order_id': params['orderId'],  # 平台定单id
        'platform': PLATFORM_NAME,  # 平台标识名
        'real_price': float(params['amount']),  # 实际>充值人民币数　单位元
        'order_money': float(params['amount']),  # 平台实际支付money 单位元
    }
    return RETURN_DATA, pay_data


if __name__ == '__main__':
    # print login_verify(None, 'BlWaW/UjRCrLnDq3tbaFFDtf2RjJvO3SKUFaW1iFgoXzovGT8I6lN+yYxrJwIA==')
    # params = {'userName': '900086000027626132', 'orderId': 'A20150630132811883417625', 'payType': '4', 'productName': '60\xe9\x92\xbb\xe7\x9f\xb3\xe5\x8c\x85', 'amount': '1.00', 'result': '0', 'notifyTime': '1435642158359', 'sign': 'ZRiTn+C7FWcVMyLiNR5u3wYFky13jsBunhCtZSjwS0mCK6JQ28xavzEtpDiHcNcYvzer5ku+nZjnmbF1KaeARg==', 'requestId': 'h10367664-h1-8-1435642044'}
    params = 'result=0&userName=900086000027626132&productName=60\xe9\x92\xbb\xe7\x9f\xb3\xe5\x8c\x85&payType=4&amount=1.00&orderId=A20150630132811883417625&notifyTime=1435642158359&requestId=h10367664-h1-8-1435642044&sign=ZRiTn%2BC7FWcVMyLiNR5u3wYFky13jsBunhCtZSjwS0mCK6JQ28xavzEtpDiHcNcYvzer5ku%2BnZjnmbF1KaeARg%3D%3D'
    print payment_verify(None, params)
