# coding: utf-8

from helper import http
import json
import time
import urllib
import hashlib
from lib.utils.debug import print_log

# 平台：魅族
PLATFORM_NAME = 'meizu'
# 平台分配的app_id
APP_ID = "3179239"
# 平台分配的app_key
APP_KEY = '34ccf92c34284f6f9f9eb9b83d1707ca'
# 0 支付验证成功返回数据   1 支付验证失败返回数据
RETURN_DATA = {
    0: {"code": 200},
    1: {"code": 120014},
}
APP_SECRET = '3wSfRcWSlAqYUrcq8nd4tVZeRecF7BQB'
# 验证sessionURL
VERIFY_SESSION_URL = 'https://api.game.meizu.com/game/security/checksession'
QUERY_MEIZU_URL = 'https://api.game.meizu.com/game/order/query'


def login_verify(req, params=None):
    """登陆验证
    Args:
        app_id: 游戏 id
        session_id: 用户sessionID
        uid: 用户 id
        ts: timestamp.eg: 1396424644001
        sign_type: 常量:md5
        sign: 签数签名
    Returns:
        用户标识
    """
    if not params:
        params = {
            'app_id':  APP_ID,
            'session_id': req.get_argument('session_id'),
            'uid':  req.get_argument('user_id'),
            'ts': int(time.time()*1000),
            'sign_type': 'md5',
            # 'new_channel': req.get_argument('new_channel', ''),
        }

    params['sign'] = meizu_make_sign(params)
    http_code, content = http.post(
            VERIFY_SESSION_URL, urllib.urlencode(params), validate_cert=True)

    if http_code != 200:
        return None

    result = json.loads(content)
    if result['code'] != 200:
        return None

    return {
        'openid': params['uid'],
    }


def payment_verify(req, params=None):
    """验证支付
    Args:
        params: 验证需要的所有数据,以下是必须的
            notify_time:      通知的发送时间
            notify_id:        通知 id
            order_id:         订单 id
            app_id:           应用 id
            uid:              用户 id
            partner_id:       商户 id
            cp_order_id:      游戏订单 id
            product_id:       产品 id
            product_unit:     商品名称
            buy_amount:       购买数量
            product_per_price: 产品单价
            total_price:      购买总价
            trade_status:     交易状态: 1:待支付(订单已创建) 2:支付中
                                       3:已支付
                                       4:取消订单 5:未知异常取消订单
            create_time:      订单时间
            pay_time:         支付时间
            pay_type:         支付类型:1 不定金额充值,0 购 买
            user_info:        用户自定义信息
            sign:             参数签名
            sign_type:        签名类型,常量 md5
    Returns:
        验证成功返回支付数据，失败返回None
    """
    if not params:
        params = {
            'notify_time': req.get_argument('notify_time'),
            'notify_id': req.get_argument('notify_id'),
            'order_id': req.get_argument('order_id'),
            'app_id': req.get_argument('app_id'),
            'uid': req.get_argument('uid'),
            'partner_id': req.get_argument('partner_id'),
            'cp_order_id': req.get_argument('cp_order_id'),
            'product_id': req.get_argument('product_id'),
            'product_unit': req.get_argument('product_unit', ''),
            'buy_amount': req.get_argument('buy_amount', ''),
            'product_per_price': req.get_argument('product_per_price', ''),
            'total_price': req.get_argument('total_price'),
            'trade_status': req.get_argument('trade_status'),
            'create_time': req.get_argument('create_time'),
            'pay_time': req.get_argument('pay_time'),
            'pay_type': req.get_argument('pay_type', ''),
            'user_info': req.get_argument('user_info', ''),
            'sign': req.get_argument('sign', ''),
            'sign_type': 'md5',
        }
    # flag = 1
    # if params['app_id'] == APP_ID2:
    #     flag = 2

    new_sign = meizu_make_sign(params)
    if new_sign != params['sign']:
        return RETURN_DATA, None

    pay_data = {
        'app_order_id': params['cp_order_id'],    # 自定义定单id
        'order_id': params['order_id'],           # 平台定单id
        'platform': PLATFORM_NAME,                # 平台标识名
        'real_price': float(params['total_price'])
    }

    return RETURN_DATA, pay_data


def meizu_make_sign(params, flag=None):
    """制作签名 按字母顺序排序 使用md5
    Args:
        params: 要签名的字典数据
    Returns:
        md5签名
    """
    # 所有的必选参数都必须参与签名，none不参与签名, ''参与签名
    sign_keys = sorted((k for k, v in params.iteritems(
        ) if k not in ['sign_type', 'sign']))

    sign_values = []
    for k in sign_keys:
        v = params[k]
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        sign_values.append('%s=%s' % (k, v))

    msg = '&'.join(sign_values)
    secret = APP_SECRET
    msg += ':' + secret

    return hashlib.md5(msg).hexdigest()


def get_meizu_order(params):
    """获取meizu此次的订单数据
    Args:

    params:
        订单数据: json格式
            app_id:        游戏 ID(不能为空)
            cp_order_id:   CP 定单 ID(不能为空)
            uid:           游戏玩家 ID(不能为空)
            product_id:    CP 游戏道具 ID,默认值:”0”
            product_subject: 订单标题,格式为:”购买 N 枚金币”
            product_body:  游戏道具说明,默认值:””
            product_unit:  游戏道具的单位,默认值:””
            buy_amount:    道具购买的数量,默认值:”1”
            product_per_price: 游戏道具单价,默认值:总金额
            total_price:   总金额
            create_time:   创建时间戳
            pay_type:      支付方式,默认值:”0”(即定额支付)
            user_info:     CP 自定义信息,默认值:””
            sign:          参数签名(不能为空)
            sign_type      签名算法,默认值:”md5”(不能为空)
    """
    post_data = {
        'app_id': params['app_id'],
        'cp_order_id': params['cp_order_id'],
        'uid': params['uid'],
        'product_id': params['product_id'],
        'product_subject': params['product_subject'],
        'product_body': params['product_body'],
        'product_unit': params['product_unit'],
        'buy_amount': params['buy_amount'],
        'product_per_price': params['product_per_price'],
        'total_price': params['total_price'],
        'create_time': str(int(time.time())),
        'pay_type': params['pay_type'],
        'user_info': params['user_info'],
        'sign_type':  'md5',
    }

    post_data['sign'] = meizu_make_sign(post_data)

    return post_data


def query_meizu_order(params):
    """订单查询接口
    Args:
        params: 字典参数数据
            app_id:        游戏 id
            cp_order_id:   游戏生成的 order_id
            ts:            Unix_timestamp.eg: 1396424644
            sign_type:     常量:md5
            sign:           签数签名
    return:
        订单情况: json格式
            appId: 游戏 Id
            buyAmount: 购买数量
            cpOrderId: 游戏定单 Id
            orderId: SDK 服务器定单 Id
            partnerId: 开发者 Id
            tradeStatus: 0000，代表支付成功
            uid: 用户 Id
            productId: 产品 Id
            productSubject: 定单标题
            productBody: 产品详情
            productUnit: 产品单位
            buyAmount: 单价
            totalPrice: 总价
            tradeStatus: 交易状态,1:待支付(订单已创建) 2:支付中 3:已支付 4:取消订单 5: 未知
            createTime: 创建时间
            payTime: 支付时间
            deliverStatus: 发货状态,1:支付未完成,2:待 发货:3:已发货,4:发货失败
    """
    post_data = {
        'app_id': APP_ID,
        'cp_order_id': str(params['cp_order_id']),
        'ts': str(params['ts']),
        'sign_type': 'md5',
    }
    post_data['sign'] = meizu_make_sign(post_data)  # 查询接口暂不实现，临时处理

    try:
        _, content = http.post(
            QUERY_MEIZU_URL, urllib.urlencode(post_data), timeout=2)
    except:
        return {}

    return json.loads(content)


if __name__ == '__main__':
    pass
