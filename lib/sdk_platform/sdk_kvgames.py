# coding: utf-8

import json
import urllib
from helper import http
from helper import utils
# from lib.utils.debug import print_log
import settings

PLATFORM_NAME = 'androdikvgames.cn'
APP_ID = 'popstar'

SECRET_KEY = 'b4c9ab67bec00df240119825f8cd1c05'

# 台湾sdk
VERIFY_SESSIONID_URI = 'http://app.tw.hi365.com/taiwan/backend_account_check/'
TEST_VERIFT = 'http://apptest.tw.hi365.com/taiwan/backend_account_check/'

# 大陆sdk
# VERIFY_SESSIONID_URI = 'http://app.cn.hi365.com/backend_account_check/'
# TEST_VERIFT = 'http://219.142.26.114:9097/backend_account_check/'

# 返回数据0是成功的数据，1是失败的数据
RETURN_DATA = {
    0: 'success',
    1: 'fail',
}


CURRENCY_RATE = {
    'TWD': 0.2077,
    'HKD': 0.8612,
    'USD': 6.6796,
}


def login_verify(req, params=None, DEBUG=False):
    """登录验证
    Args:
        req: request封装，以下是验证所需参数
            session_id: session_id
            user_id: user_id
        params: 测试专用
    Returns:
        平台相关信息(openid必须有)
    """
    sandbox = 'sandbox'
    if not params:
        sandbox = req.get_argument('account_env', '')
        params = {
            'session_id': req.get_argument('session_id', ''),
            'user_id': req.get_argument('user_id', ''),
        }
    # # todo 先不做验证，等确定是接国内还是台湾的sdk服务
    # if settings.DEBUG:
    #     return {
    #         'openid': params['user_id'],
    #         'openname': '',
    #     }

    # 两个地址，签名参数名 user_id, app_id 不同
    # http://app.tw.hi365.com/taiwan/backend_account_check/
    # {
    #     'session_id': req.get_argument('session_id', ''),
    #     'user_id': req.get_argument('user_id', ''),
    #     'app_id': APP_ID,
    # }

    # http://app.tw.hi365.com/backend_account_check/
    # {
    #     'session_id': req.get_argument('session_id', ''),
    #     'uid': req.get_argument('user_id', ''),
    #     'appid': APP_ID,
    # }

    params['app_id'] = APP_ID

    sign = make_sign(params)
    query_data = urllib.urlencode({
        'app_id': APP_ID,
        'session_id': params['session_id'],
        'uid': params['user_id'],
        'sign': sign,
    })
    http_code, content = http.post(VERIFY_SESSIONID_URI, query_data)
    if http_code != 200:
        return None
    result = json.loads(content)
    # if result['status'] == -6:
        # 开发环境参数发到测试环境验证 status = -6
    if sandbox:
        # 根据前端传的参数判断 是否把参数发到测试环境验证
        # print result
        http_code, content = http.post(TEST_VERIFT, query_data)
        if http_code != 200:
            return None
        result = json.loads(content)

    # print result
    if int(result['status']) != 1:
        return None

    return {
        'openid': result['data']['uid'],           # 平台标识
        'openname': result['data']['username'],    # 平台昵称
    }


def payment_verify(req, params=None):
    """支付验证
    Args:
        req: request封装，以下是验证所需参数
            mhtOrderNo:             订单号             string
            mhtOrderName:           商品名称           string
            mhtOrderAmt:            订单交易金额        int       单位(人民币):分
            mhtOrderStartTime:      商户订单开始时间    string     yyyyMMddHHmmss
            mhtCharset:             字符编码           string     定值:UTF-8
            tradeStatus:            支付状态           string     A001 支付成功
            mhtReserved:            游戏自定义数据      string
            PlatformUid:            平台uid           string
            signType:               签名方法           string     定值:MD5
            signature:              数据签名           string     排除signType, signature
        params: 测试专用
    """
    # 台湾版单独接口
    if True:
        return payment_verify_tw(req, params)
    if not params:
        params = {
            'mhtOrderNo': req.get_argument('mhtOrderNo', ''),
            'mhtOrderName': req.get_argument('mhtOrderName', ''),
            'mhtOrderAmt': req.get_argument('mhtOrderAmt', 0),
            'mhtOrderStartTime': req.get_argument('mhtOrderStartTime', ''),
            'mhtCharset': req.get_argument('mhtCharset', ''),
            'tradeStatus': req.get_argument('tradeStatus', ''),
            'mhtReserved': req.get_argument('mhtReserved', ''),
            'PlatformUid': req.get_argument('PlatformUid', ''),
            'signType': req.get_argument('signType', ''),
            'signature': req.get_argument('signature', ''),
        }

    signType = params.pop('signType')
    signature = params.pop('signature')

    if params['tradeStatus'] != 'A001':
        return RETURN_DATA, None

    sign = make_sign(params)
    if sign != signature:
        return RETURN_DATA, None

    pay_data = {
        'app_order_id':    params['mhtReserved'],                   # 自定义定单id
        'order_id':        params['mhtOrderNo'],                    # 平台定单id
        'order_money':     float(params['mhtOrderAmt'])/100,        # 平台实际支付money 单位元
        'uin':             params['PlatformUid'],                   # 平台用户id
        'platform':        PLATFORM_NAME,                           # 平台标识名
    }
    return RETURN_DATA, pay_data


def payment_verify_tw(req, params=None):
    """台湾版支付验证
    Args:
        req: request封装，以下是验证所需参数
            order_no:               订单号             string
            product_name:           商品名称           string
            amount:                 订单交易金额        int       单位(人民币):分
            ext:                    游戏自定义数据      string     "tw31764987-tw3-12-1464186203" 游戏uid-分服id-商品id-时间戳
            account_id:             平台账号id         string
            currency:               货币类型           string    (TWD/HKD/USD)
            sign_type:              签名方法           string     定值:MD5
            signature:              数据签名           string     排除sign_type, signature

            pay_tp:                 支付平台           string     '1':google_play '2':台湾本地mycard '3':mycard海外
            promo_code:             my_card的活动号    string     用于活动期间钻石发放
        params: 测试专用
    """
    if not params:
        params = {
            'order_no': req.get_argument('order_no', ''),
            'product_name': req.get_argument('product_name', ''),
            'amount': req.get_argument('amount', 0),
            'ext': req.get_argument('ext', ''),
            'account_id': req.get_argument('account_id', ''),
            'currency': req.get_argument('currency', ''),
            'sign_type': req.get_argument('sign_type', ''),
            'signature': req.get_argument('signature', ''),

            'pay_tp': req.get_argument('pay_tp', ''),
            'promo_code': req.get_argument('promo_code', ''),
        }
    platform = ''
    sign_type = params.pop('sign_type')
    signature = params.pop('signature')

    sign = make_sign(params)
    if sign != signature:
        return RETURN_DATA, None

    # 汇率转换
    currency = params.get('currency')
    amount = float(params.get('amount'))
    if not currency:
        currency = 'TWD'
    # if currency == 'HKD':
    #     order_money = amount * HKD_RATE
    # elif currency == 'USD':
    #     order_money = amount * USD_RATE
    # else:
    #     order_money = amount
    if params['pay_tp'] in [2, 3, '2', '3']:            # mycard支付
        platform = 'MyCard'
    pay_data = {
        'app_order_id':    params['ext'],                   # 自定义定单id
        'order_id':        params['order_no'],              # 平台定单id
        'order_money':     float(params['amount']),                   # 平台实际支付money
        'uin':             params['account_id'],            # 平台用户id
        'platform':        platform if platform else PLATFORM_NAME,                   # 平台标识名
        'currency':        currency,                        # 平台货币类型
        'currency_rate':   CURRENCY_RATE[currency],         # 汇率
        'pay_tp':          params['pay_tp'],                # 支付平台类型(google-play/mycard)
        'promo_code':      params['promo_code'],            # mycard促销代码
        'real_price':      float(params['amount']),
    }
    return RETURN_DATA,  pay_data


def make_sign(params):
    """制作签名
    Args:
        params: 要签名的字典数据
    Returns:
    """
    # 所有的必选参数都必须参与签名，空串不参与签名
    sign_items = sorted([(key, value) for key, value in params.iteritems() if params[key]])
    sign_data1 = '&'.join('%s=%s' % (key, value) for key, value in sign_items)
    secret_md5 = utils.hashlib_md5_sign(SECRET_KEY)
    sign_data2 = '%s&%s' % (sign_data1, secret_md5)

    return utils.hashlib_md5_sign(sign_data2)


if __name__ == '__main__':
    print login_verify('', {'session_id': 'vfsyi8vvoi0mxkaghueowgykyhgu0u89', 'uid': '364'})
