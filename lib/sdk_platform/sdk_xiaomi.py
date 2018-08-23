# coding: utf-8

from helper import http
import json
import hmac
import urllib
import hashlib
from helper import utils
from lib.utils.debug import print_log

PLATFORM_NAME = 'xiaomi'
# 平台分配的app_id
APP_ID = '2882303761517583562'
# 平台分配的app_key
APP_KEY = '5191758392562'
#  支付验证成功返回数据
# 支付验证失败返回数据
RETURN_DATA = {
    0: {'errcode': 200, 'errMsg': 'sucess'},
    1: {'errcode': 1525, 'errmsg': 'sign error'},
}
AppSecret = 'EesfeCtNgdIdAMVfFLhFTw=='
# 验证sessionURL
VERIFY_SESSION_URL = 'http://mis.migc.xiaomi.com/api/biz/service/verifySession.do'


def login_verify(req, params=None):
    """登陆验证
    Args:
        uid: 用户ID
        session_id: 用户sessionID
    Returns:
        用户标识
    """
    if not params:
        params = {
            'appId': APP_ID,
            'session':  req.get_argument('session_id', ''),
            'uid':     req.get_argument('user_id', ''),
        }
    params['signature'] = xiaomi_make_sign(params)
    url = '%s?%s' % (VERIFY_SESSION_URL, urllib.urlencode(params))

    http_code, content = http.get(url, timeout=5)

    if http_code != 200:
        return None

    result = json.loads(content)
    if result['errcode'] != 200:
        return None

    return {

        'openid': req.get_argument('user_id', ''),
    }


def payment_verify(req, params=None):
    """验证支付
    Args:
        params: 验证需要的所有数据,以下是必须的
            appId:            APP_ID
            cpOrderId:        开发商订单 ID
            cpUserInfo:       开发商透传信息
            uid:              用户 ID
            orderId:          游戏平台订单 ID
            orderStatus:      订单状态 TRADE_SUCCESS 代表成功
            payFee:           支付金额,单位为分,即 0.01 米币
            productCode:      商品代码
            productName:      商品名称
            productCount:     商品数量
            payTime:          支付时间,格式 yyyy-MM-dd HH:mm:ss
            orderConsumeType: 订单类型:10:普通订单 11:直充直消订单
            signature:        签名
    Returns:
        验证成功返回支付数据，失败返回None
    """
    if not params:
        params = {
            'appId': int(req.get_argument('appId')),
            'cpOrderId': req.get_argument('cpOrderId'),
            'cpUserInfo': req.get_argument('cpUserInfo'),
            'orderId': req.get_argument('orderId'),
            'orderStatus': req.get_argument('orderStatus', ''),
            'payFee': int(req.get_argument('payFee', '')),
            'payTime': req.get_argument('payTime'),
            'productCode': req.get_argument('productCode'),
            'productCount': int(req.get_argument('productCount')),
            'productName': req.get_argument('productName'),
            'uid': int(req.get_argument('uid')),
            'signature': req.get_argument('signature'),
            'partnerGiftConsume': req.get_argument('partnerGiftConsume', ''),
        }
    if params['orderStatus'] != 'TRADE_SUCCESS':
        return RETURN_DATA, None

    if int(params['appId']) != int(APP_ID):
        return RETURN_DATA, None

    if not params['partnerGiftConsume']:
        params.pop('partnerGiftConsume')

    new_sign = xiaomi_make_sign(params)
    if new_sign != params['signature']:
        return RETURN_DATA, None

    pay_data = {
        'app_order_id' : params['cpOrderId'],         # 自定义定单id
        'order_id'     : params['orderId'],           # 平台定单id
        'platform'     : PLATFORM_NAME,                # 平台标识名
        'real_price'   : float(params['payFee']) / 100
    }

    return RETURN_DATA, pay_data


def xiaomi_make_sign(params):
    """制作签名 按字母顺序排序 使用hmac-sha1
    Args:
        params: 要签名的字典数据
    Returns:
        hmac-sha1签名
    """
    # 所有的必选参数都必须参与签名，空串不参与签名
    sign_keys = sorted((k for k, v in params.iteritems() if v and k != 'signature'))
    sign_values = ['%s=%s' % (k, params[k]) for k in sign_keys if params[k] != '']

    msg = '&'.join(sign_values)
    return hmac.new(AppSecret, msg.encode('utf-8'), hashlib.sha1).hexdigest()


if __name__ == '__main__':
    params = {'orderId': '21143522661473595317', 'cpOrderId': 'h12343095-h1-8-1435226612', 'payFee': '100', 'uid': '31424627', 'productCode': '01', 'signature': '44b50b6601aefed6e76c726811978e2de8aafaf2', 'productCount': '1', 'productName': '\xe9\x92\xbb\xe7\x9f\xb3'.decode('utf-8'), 'orderStatus': 'TRADE_SUCCESS', 'cpUserInfo': 'h12343095-h1-8-1435226612', 'appId': '2882303761517351263', 'payTime': '2015-06-25 18:05:38'}
    print payment_verify(None, params)



