# coding: utf-8

import json
import base64
import urllib
from helper import http
from helper import utils
from lib.utils.debug import print_log

__VERSION__ = 'v3.0.0'
PLATFORM_NAME = 'baidu'
APP_ID = '8199656'
APP_KEY = '93a69oXYAmReZWqhIlEoLz1i'
SECRET_KEY = 'DoZK71QVmrpvbmsHQt3l4p2tiRt26xla'
VERIFY_SESSIONID_URI = 'http://querysdkapi.baidu.com/query/cploginstatequery?'
# 返回数据0是成功的数据，1是失败的数据
RETURN_DATA = {
    0: {'AppID': APP_ID, 'ResultCode': 1, 'ResultMsg': 'success', 'Sign': '', 'Content': ''},
    1: {'AppID': APP_ID, 'ResultCode': 0, 'ResultMsg': 'failure', 'Sign': '', 'Content': ''},
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
            'user_id': req.get_argument('user_id', ''),
        }

    AccessToken = params['session_id']

    sign_str = "%s%s%s" % (APP_ID, AccessToken, SECRET_KEY)
    sign = utils.hashlib_md5_sign(sign_str)

    query_data = urllib.urlencode({
        'AppID': APP_ID,
        'AccessToken': AccessToken,
        'Sign': sign,
    })
    http_code, content = http.post(VERIFY_SESSIONID_URI, query_data)

    if http_code != 200:
        return None

    result = json.loads(content)
    if int(result['ResultCode']) != 1:
        return None

    Content = base64.b64decode(result['Content'])
    obj = json.loads(Content)
    return {
        'openid': obj['UID'],                     # 平台标识
    }


def payment_verify(req, params=None):
    """支付验证
    Args:
        req: request封装，以下是验证所需参数
            AppID:                 应用 ID，对应游戏客户端中使用的 APPID
            OrderSerial:           SDK 系统内部订单号
            CooperatorOrderSerial: CP 订单号
            Sign:                  签名
            Content:  JSON 编码格式:UTF-8,Base64 编码
                UID:             用户 ID
                MerchandiseName: 商品名称
                OrderMoney:      订单金额,保留两位小数。单位:元
                StartDateTime:   订单创建时间 格式:yyyy-MM-dd HH:mm:ss
                BankDateTime:    银行到帐时间 格式:yyyy-MM-dd HH:mm:ss
                OrderStatus:     支付状态：0=失败，1=成功
                StatusMsg:       StatusMsg
                ExtInfo:         ExtInfo
        params: 测试专用
    """
    if not params:
        params = {
            'AppID': req.get_argument('AppID', ''),
            'OrderSerial': req.get_argument('OrderSerial', ''),
            'CooperatorOrderSerial': req.get_argument('CooperatorOrderSerial', ''),
            'Sign': req.get_argument('Sign', ''),
            'Content': req.get_argument('Content', ''),
        }
    params['SecretKey'] = SECRET_KEY

    # 生成返回数据
    return_data = {}
    for code, data in RETURN_DATA.iteritems():
        ResultCode = 1 if code == 0 else 0
        return_Sign = utils.hashlib_md5_sign('%s%s%s' % (APP_ID, ResultCode, SECRET_KEY))
        return_data[code] = dict(data, AppID=params['AppID'], Sign=return_Sign)

    sign_str = ('%(AppID)s'
                '%(OrderSerial)s'
                '%(CooperatorOrderSerial)s'
                '%(Content)s'
                '%(SecretKey)s') % params
    new_sign = utils.hashlib_md5_sign(sign_str)
    if new_sign != params['Sign']:
        return return_data, None

    content = base64.b64decode(params['Content'])
    obj = json.loads(content)
    # 支付状态：0=失败，1=成功
    if int(obj['OrderStatus']) != 1:
        return_data[1] = return_data[0]
        return return_data, None

    pay_data = {
        'app_order_id':    params['CooperatorOrderSerial'],     # 自定义定单id
        'order_id':        params['OrderSerial'],                   # 平台定单id
        'order_money':     float(obj['OrderMoney']),             # 平台实际支付money 单位元
        'uin':             obj['UID'],                                   # 平台用户id
        'platform':        PLATFORM_NAME,                           # 平台标识名
        'real_price':      float(obj['OrderMoney']),
    }
    return RETURN_DATA, pay_data

if __name__ == '__main__':
    params = {'user_id': u'2023496020', 'session_id': u'2c9e3fe9665975962c9e404936387206-29a7c573e3d19824dab2d0b2d57a5c8e-20160531112532-d006beba29b1ae45762edf8d07997eac-4e3f8dfdd3f7c49b15db420226633d93-da4755a82e55b4e9359ac094752cefa0'}
    print login_verify(None, params)

    # params = {'Content': 'eyJVSUQiOjU3NzY1MDI2MiwiTWVyY2hhbmRpc2VOYW1lIjoiNjDpkrvnn7PljIUiLCJPcmRlck1vbmV5IjoiMS4wMCIsIlN0YXJ0RGF0ZVRpbWUiOiIyMDE1LTA2LTMwIDE0OjM5OjA5IiwiQmFua0RhdGVUaW1lIjoiMjAxNS0wNi0zMCAxNDozOToyMyIsIk9yZGVyU3RhdHVzIjoxLCJTdGF0dXNNc2ciOiLmiJDlip8iLCJFeHRJbmZvIjoi5YWF5YC8IiwiVm91Y2hlck1vbmV5IjowfQ==', 'AppID': '6168644', 'OrderSerial': 'b2fd06380f5373cd_01001_2015063014_000000', 'Sign': 'd1392e08fa385d5677a88ce5902c47df', 'CooperatorOrderSerial': 'h18380283-h1-8-1435646327'}
    # payment_verify(None, params)
