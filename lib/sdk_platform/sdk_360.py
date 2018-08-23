# coding: utf-8
import copy
import hashlib
import base64
import json
import urllib
import time
from helper import http
from helper import utils

# 平台名字
PLATFORM_NAME = '360'
# 平台分配的app_id
APP_ID = '203597181'
# 平台分配的app_key
APP_KEY = '0918136f8aed60f54b2a6ade0b639aa6'
# # 平台分配的app_secret
APP_SECRET = '5df19036d8f693e29eef1449362c970b'
# 用access_token获取用户信息URL
GET_USER_URI = 'https://openapi.360.cn/user/me.json'
# 平台支付验证的URL
PAYMENT_VERIFY_URI = 'http://mgame.360.cn/pay/order_verify.json'
# 平台支付回调地址
NOTIFY_URL = 'http://120.132.57.113:7005/transformer/pay-callback-cn360/'
# 360开发平台添加的包名
PNAME = 'conm.kaiqigu.superhero2.qihoo'
# 上传角色数据接口地址
ROLEINTERFACE = 'https://role.gamebox.360.cn/7/role/rolesave'
# # 支付验证失败返回数据,不为ok的任意值
# 支付成功与失败所返回的数据
RETURN_DATA = {
    0: {"status": "ok", "delivery": "success", "msg": ""},
    1: {"status": "error", "delivery": "other", "msg": ""},
}

def login_verify(req, access_token=None):
    """sid用户会话验证
    Args:
        authorization_code: authorization_code
    Returns:
        用户标识ID和会话ID数据
    """
    if not access_token:
        access_token = req.get_argument('session_id')

    query_str = urllib.urlencode({
        'access_token': access_token,
    })

    url = '%s?%s' % (GET_USER_URI, query_str)
    http_code, content = http.get(url, timeout=5)

    if http_code != 200:
        return None

    obj = json.loads(content)

    return {
        'openid': obj['id'],           # 平台用户ID
        'access_token': access_token,  # access_token
        'openname': obj['name'],       # 平台用户名字
    }


def payment_verify(req, params=None):
    """支付回调验证，app_order_id为自定义
    Args:
        params: 字典参数数据
            app_key:      应用 app key
            product_id:   所购商品 id
            amount:       总价,以分为单位
            app_uid:      应用内用户 id
            app_ext1:     应用扩展信息 1 原样返回
            app_ext2:     应用扩展信息 2 原样返回
            user_id:      360 账号 id
            order_id:     360 返回的支付订单号
            gateway_flag: 如果支付返回成功,返回 success应用需要确认是 success 才给用户加钱
            sign_type:    定值 md5
            app_order_id: 应用订单号 支付请求时若传递就原样返回
            sign_return:  应用回传给订单核实接口的参数 不加入签名校验计算
            sign:         签名
    Returns:
        支付数据
    """
    print_log("in 360 payment_verify req is: %s" % req)
    if not params:
        params = {
            'app_uid': req.get_argument('app_uid'),
            'amount': int(req.get_argument('amount')),
            'app_order_id': req.get_argument('app_order_id'),
            'user_id': int(req.get_argument('user_id', '')),
            'gateway_flag': req.get_argument('gateway_flag', ''),
            'product_id': int(req.get_argument('product_id')),
            'order_id': req.get_argument('order_id'),
            'sign_return': req.get_argument('sign_return'),
            'app_key': req.get_argument('app_key'),
            'sign_type': req.get_argument('sign_type'),
            'sign': req.get_argument('sign'),
        }
    print_log("in 360 payment_verify params is: %s" % params)
    if params['gateway_flag'] != "success":
        return RETURN_DATA, None

    new_sign = generate_sign(params)
    print_log("in 360 payment_verify new_sign is: %s" % new_sign)
    if new_sign != params['sign']:
        return RETURN_DATA, False
    #
    # copy_params = copy.deepcopy(params)
    #
    # for i in ('sign_return'):
    #     if i in copy_params:
    #         del copy_params[i]
    # copy_params['sign'] = new_sign
    #
    # url = '%s?%s' % (PAYMENT_VERIFY_URI, urllib.urlencode(copy_params))
    # http_code, content = http.get(url, timeout=10)
    # print_log("in 360 payment_verify http_code is: %s, content is: %s" % (new_sign, content))
    # if http_code != 200:
    #     return RETURN_DATA, None
    #
    # obj = json.loads(content)
    #
    # if obj.get('ret') != 'verified':
    #     return RETURN_DATA, None
    # print_log("in 360 payment_verify ")
    pay_data = {
        'app_order_id':       params['app_order_id'],         # 自定义定单id
        'order_id':           params['order_id'],             # 平台定单id
        'platform':           PLATFORM_NAME,                  # 平台标识名
        'real_price':         float(params['amount']) / 100       # 实际充值人民币数　单位元
    }
    return RETURN_DATA, pay_data


def generate_sign(params):
    # 按key自然排序
    sign_values = [str(params[k]) for k in sorted(params.iterkeys())
                   if k not in ['sign', 'sign_return'] and params[k]]
    sign_values.append(APP_SECRET)
    sign_str = '#'.join(sign_values)
    return hashlib.md5(sign_str).hexdigest()


def send_role_data(params):
    '''上传角色数据
    args:
        params:
            qid: 奇虎用户账号id
            zoneid: 区服id
            zonename: 区服名称
            roleid: 角色id
            rolename: 角色名称
            gender: 性别
            vip: vip等级
            power: 战斗力
            rolelevel: 等级
            professionid: 职业id
            profession: 职业名称
            partyid: 帮派id
            partyname: 帮派名称
            type: 上传角色数据场景(enterServer, levelUp, createRole, exitServer)
    '''
    params['gender'] = u'无'
    params['profession'] = u'无'
    params['professionid'] = 0
    role = base64.b64encode(json.dumps(params).encode('zlib'))
    post_data = {
        'appkey': APP_KEY,
        'appid': APP_ID,
        'pname': PNAME,
        'plat': 'android',
        'lt': time.time(),
        'role': role,
    }
    sign = ('appkey=%(appkey)s&appid=%(appid)s&'
            'pname=%(pname)s&plat=%(plat)s&lt=%(lt)s') % post_data
    post_data['sign'] = hashlib.md5(sign).hexdigest()
    post_data = urllib.urlencode(post_data)
    try:
        http_code, content = http.post(ROLEINTERFACE, post_data, timeout=2)
    except Exception, e:
        print e
    return


if __name__ == '__main__':
    # print login_verify(None, '174820871e76f8010350044abf90e6693c3fd499d365924c2')
    params = {'gateway_flag': 'success', 'user_id': '174820871', 'product_id': '8', 'order_id': '1506296065517829641', 'sign_return': 'bc37a5171fdb0a44830ea2fb3f9cb6ae', 'app_key': '5f290f9ce1d7bf3a4b3b26113bb52bd8', 'sign': 'f524eb9aae11c12c00f7c63594a5207c', 'app_order_id': 'h19278339-h1-8-1435567849', 'amount': '100', 'sign_type': 'md5', 'app_uid': 'h19278339'}
    payment_verify(None, params)
