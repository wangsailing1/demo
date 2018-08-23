# coding: utf-8

import json
import urllib
from helper import http
from helper import utils
from lib.utils.debug import print_log

__VERSION__ = '1.2.2'
# 酷派
PLATFORM_NAME = 'coolpad'
APP_ID = '5000008282'
APP_KEY = '809fbad29f0348cd829b18f0c0f1fb69'
REDIRECT_URI = APP_KEY  # 这个参数是由平台分配的, 不是固定值
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIICXgIBAAKBgQC4neqDitaReezXHEJZiZG2kR5KBvfvkVFK+Ysl0+sBrYtOrVgT
c61OX+w36DlG3OZar5VfIDtWAnnOiqCfQz6OxUSCYW+10m6BU806FM++lWJsA6Y4
aneYgl4OuAYymxgkZ+C1acqB22c+Gg7xqfbUHacVFWNGobBqk1XKeHE/uwIDAQAB
AoGBAJ0eEDq5Cxkt+cmsjC8lbDRC1tNLkPB67QNw0uJzs1pvNtLTpdSQKxs7eY6u
/Sf40ba2HdqiVL1DSCTmSAKiuPZW+CNUxTFADW/iunBDjUnWHUcvRXA3uBzCdiXf
//0+xe+0/DZwSOoQrCJcgVka0W54V8ecjJOV3HIvFBQYEbuRAkEA7qqWC4CLrgsG
Sr2z8dv9WhG2vW138zwTRj6xsmukY4fQkmgDOSZBAg8Pt5qC1tBtKjSbqTVIliH9
kWkvw9dm0wJBAMYGaZ3ZutYwFWH+EsUrXlT43HgiN8iFrUGBwT7gcu5tjpf/7OpE
orKflxl7V6sLvP+QMtHW/s9ErPJTn4dcAnkCQA3f+O0eQgCSP4Fk2es7oNT1pqwI
iyqm2XACAQ6gV2Q55xQ728Qcxza5bW59GxIl99K2UD5cDKY9v6IOfWpjQWUCQQC3
sAsYmXduZ3vuQjg3HVuLhq074sHMB/QG583R/XGfKZEz/fpN9QzWlKMcyAUybNkM
Vz5M2BnVOecTge5hKUBBAkEAkIQBiliCNlI+k0+yieEepoPrmMgw8+Pm8K1FB9ur
gT0WC1ZddD0SZ95TMltsqiSIIMwdw/jWpM5UgZ2yiT4D3w==
-----END PRIVATE KEY-----"""
PAY_APP_KEY = 'RjVEMjU1RUUyMTNDNzlDRDM2QTM3QkIyMUI1QkYxRjFGM0E0NkVBRk1UZ3pNekUzT1Rjek1UUXlNalF5T0RnMU9UY3JNak0xTkRFNU56RTJPRFl5TWpneU5EWTJOamc0TWpRM056QXlPRGs1TkRJNU9Ea3dNVFEz'

GET_ACCESS_TOKEN_URI = 'https://openapi.coolyun.com/oauth2/token'
GET_USER_URI = 'https://openapi.coolyun.com/oauth2/api/get_user_info'
#CREATE_PAY_ORDER_URL = 'http://pay.coolyun.com:6988/payapi/order'
# 返回数据0是成功的数据，1是失败的数据
RETURN_DATA = {
    0: 'SUCCESS',
    1: 'FAILURE',
}


def login_verify(req, params=None):
    """登录验证
    Args:
        req: request封装，以下是验证所需参数
            session_id: session_id
        params: 测试专用
    Returns:
        平台相关信息(openid必须有)
    """
    if not params:
        params = {
            'session_id': req.get_argument('session_id', ''),
        }
    authorization_code = params['session_id']
    access_token_data = get_access_token(authorization_code)
    # print access_token_data
    if not access_token_data:
        return None

    return {
        'openid': access_token_data['openid'],              # 平台用户ID
        # 'openname': access_token_data['openid'],            # 平台用户名字
        'access_token': access_token_data['access_token'],  # access_token
    }


def get_access_token(authorization_code):
    """通过code获得token
    Args:
        authorization_code: authorization_code
    Returns:
        access_token
    """
    query_str = urllib.urlencode({
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'client_id': APP_ID,
        'client_secret': APP_KEY,
        'code': authorization_code,
    })
    url = '%s?%s' % (GET_ACCESS_TOKEN_URI, query_str)
    try:
        http_code, content = http.get(url)
        print_log(http_code)
        # print http_code, content
    except:
        return None

    if http_code != 200:
        return None

    # {"openid":"103400","refresh_token":"0.11fae3b9fbb74","access_token":"0.e.c63"}
    obj = json.loads(content)
    print_log(obj)
    if not obj.get('access_token'):
        return None

    return obj


def payment_create_order(params):
    """创建支付订单
    """
    return {}


def payment_verify(req, params=None):
    """支付验证
    Args:
        params: 回调字典数据
            sign: 签名
            transdata: 票据，JSON格式
                transtype: 交易类型  0–支付交易
                cporderid: 商户订单号 可选
                transid:   计费支付平台的交易流水号
                #appuserid: 用户在商户应用的唯一标识
                appid:     游戏id    String(20)    平台为商户应用分配的唯一代码
                waresid:   商品编码    integer    必填    平台为应用内需计费商品分配的编码
                feetype:   计费方式    integer    计费方式，具体定义见附录
                money:     交易金额    Float(6,2)   本次交易的金额
                currency:  货币类型以及单位RMB – 人民币（单位：元）
                result:    交易结果 0–交易成功 1–交易失败
                transtime: 交易完成时间 yyyy-mm-dd hh24:mi:ss
                cpprivate: 商户私有信息  可选    商户私有信息
                paytype:   支付方式    integer    可选    支付方式，具体定义见附录
    """
    if not params:
        params = {
            'sign': req.get_argument('sign', ''),
            'transdata': req.get_argument('transdata', ''),
            'signtype': req.get_argument('signtype', 'RSA'),
        }
    sign = utils.force_str(params['sign'])
    transdata = utils.force_str(params['transdata'])
    print_log('sign', sign)
    print_log('transdata', transdata)
    if not sign or not transdata:
        return RETURN_DATA, None

    s_md5 = utils.trans_sign2md5(sign, PAY_APP_KEY)
    t_md5 = utils.hashlib_md5_sign(transdata)

    if s_md5 != t_md5:
        return RETURN_DATA, None

    data = json.loads(transdata)
    # 按接受成功处理
    if int(data['result']) != 0:
        return_data = dict(RETURN_DATA)
        return_data[1] = RETURN_DATA[0]
        return return_data, None

    pay_data = {
        'app_order_id': data['exorderno'],                # 自定义定单id
        'order_id': data['transid'],                      # 平台定单id
        'real_price': float(data['money'])/100,              # 平台实际支付money 单位分
        # 'uin': data.get('appuserid', ''),                 # 平台用户id
        'platform': PLATFORM_NAME,                        # 平台标识名
    }
    return RETURN_DATA, pay_data


if __name__ == '__main__':
    params = {'session_id': '4.f02efb2f9c5c1c0de30ace168a51cdcd.c8e66c5bb4a58591ba2972a30ca776a8.1419597824908'}
    #print login_verify('', params)
    params = {'signtype': u'RSA'}
    params['transdata'] = '{"appid":"3000777425","count":1,"cporderid":"dt06aaa064-06-2-1419929824","cpprivate":"cpprivateinfo123456","currency":"RMB","feetype":0,"money":0.10,"paytype":4,"result":0,"transid":"32021412301657170095","transtime":"2014-12-30 16:59:06","transtype":0,"waresid":1}'
    params['sign'] = 'AHYojoHbbkoXLYQuMS8/DcWoBIk2w9j4V6uYTXHEYcyedxG59tEykpwJ583WiUyM4dIdsahmnTXLIjd1pQgB6/oXzDYvRwXw8HCtyCuul0p+79ElXpeTLAWIODARSqdBwFZA6j7HtP+uTTVV+TDwt4ZT2QxwtMvaijRpGAn0MR8='
    print payment_verify('', params)
