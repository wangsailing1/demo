# coding: utf-8

import time
from helper import http
import json
import urllib
import hashlib
import hmac
import binascii
import settings
from lib.utils.debug import print_log

HOSTS = {
    'sandbox': 'https://ysdktest.qq.com',   # 测试
    'official': 'https://ysdk.qq.com',  # 正式
}


PLATFORM_SETTINGS = {
    '2': {  # 微信
        'app_id': 'wx1b3d6af569370c67',
        'app_key_login': 'a33a19cde1202faeacf49a56546dfa22',
        'app_key': 'a33a19cde1202faeacf49a56546dfa22',
        'app_key_pay': 'yb4zUXXbBhDvIFYu',
        'name': 'msdk_wechat',     # 自己支付使用
        'login_verify_url': '/auth/wx_check_token',
        'balance': '/mpay/get_balance_m',
        'pay': '/mpay/pay_m',
    },
    '1': {  # 手机QQ
        'app_id': 1106196012,
        'app_key_login': 'yb4zUXXbBhDvIFYu',
        'app_key': '03dvcfsDHt7vlvGwtnWzVlvD0ytcEC0q',  # 沙箱appkey，用于现网和测试登录，和测试的支付
        'app_key_pay': 'hn9MTJI9RmgrtCFCIpaV2ZnICfqmwMqU',   # 现网appkey，用于现网的支付
        'name': 'msdk_mpqq',     # 自己支付使用
        'login_verify_url': '/auth/qq_check_token',
        'balance': '/mpay/get_balance_m',
        'pay': '/mpay/pay_m',
    },
}


def get_platform_app_key(config, is_sandbox=False):
    """ 获取平台app_key

    :param config:
    :param is_sandbox:
    :return:
    """
    if is_sandbox:
        return config['app_key']
    else:
        return config['app_key_pay']


def get_host(is_sandbox):
    """ 获取域名

    :param env:
    :return:
    """
    if is_sandbox:
        return HOSTS.get('sandbox', '')
    else:
        return HOSTS.get('official', '')


def mk_source(method, url_path, params):
    str_params = urllib.quote("&".join(k + "=" + str(params[k]) for k in sorted(params.keys())), '')
    source = '%s&%s&%s' % (
        method.upper(),
        urllib.quote(url_path, ''),
        str_params
    )
    return source


def hmac_sha1_sig(method, url_path, params, secret):
    source = mk_source(method, url_path, params)
    hashed = hmac.new(secret, source, hashlib.sha1)
    return binascii.b2a_base64(hashed.digest())[:-1]


def mk_msdk_sig(appkey,  ts):
    str_params = str(appkey) + str(ts)
    m = hashlib.md5()
    m.update(str_params)
    return m.hexdigest()


def login_verify(req, params=None, is_sandbox=False):
    """
    登录验证
    实验证明:
    沙箱测试时, 登录app_key要用现网key; 支付要用沙箱app_key
    """
    is_sandbox = settings.DEBUG
    if not params:
        params = {
            'openkey': req.get_argument('session_id', ''),
            'openid': req.get_argument('user_id', ''),
            'login_type': req.get_argument('login_type', '1'),
        }

    login_type = params['login_type']
    openkey = params['openkey']
    openid = params['openid']
    config = PLATFORM_SETTINGS.get(login_type)
    if not config:
        return False

    now = int(time.time())
    # ?timestamp = & appid = & sig = & openid = & openkey = & userip
    app_key = config['app_key_login']
    qs = urllib.urlencode({
        'timestamp': now,
        'appid': config['app_id'],
        'sig': mk_msdk_sig(app_key, now),
        'openid': openid,
        'openkey': openkey,
        'encode': 1,
    })

    host = get_host(is_sandbox)
    url = '%s%s?%s' % (host, config['login_verify_url'], qs)

    print_log("---ysdk_access_url-----", url)
    http_code, content = http.get(url, timeout=10)
    print_log("---ysdk_access-----", http_code, "---", content)
    if http_code != 200:
        return None

    obj = json.loads(content)

    if obj.get('ret') != 0:
        return None

    return {
        'openid': openid,
    }


def balance(params, is_sandbox=False):
    """
    获取余额接口, 微信登录态和手Q登录态使用的支付接口相同，支付ID相同；
    服务端使用的appid和appkey都使用手Qappid和appkey

    'openid': env.get_argument('openid', ''),
        'openkey': env.get_argument('openkey', ''),
        'pay_token': env.get_argument('pay_token', ''),
        'pf': env.get_argument('pf', ''),
        'pfkey': env.get_argument('pfkey', ''),
        'zoneid': env.get_argument('zoneid', ''),

    http://123.207.139.137/gloryroad_qt/pay/?method=ysdk_balance
    &openid=0E3B4AEF80F934ABCC480F7432B9BDA3
    &openkey=316691CE6DF1D75BD30ADBF10DE35B41
    &pay_token=316691CE6DF1D75BD30ADBF10DE35B41
    &pf=desktop_m_qq-00000000-android-00000000-353490069870208
    &pfkey=aae77af2deef87e63cbb1475b788de4
    d&zoneid=1

    https://ysdk.qq.com/mpay/get_balance_m?openid=5ADF61B4940821E4D7EAC14AFAEB7D21&pfkey=89c51d9e36a6a9096185353afc45e9aa&ts=1481535330&zoneid=1&pf=desktop_m_qq-00000000-android-00000000-867567023077456&appid=1105743742&sig=BYtb88OzBLmv9MgV%2BgLNdp6kmyw%3D&openkey=984A073F77749BDAA96B3A31B91793F5,
    {'Cookie': 'org_loc=/mpay/get_balance_m; session_id=openid; session_type=kp_actoken'}
    """
    config = PLATFORM_SETTINGS.get('1')
    if not config:
        return False

    if not params['pay_token']:     # 微信
        session_type = 'wc_actoken'
        session_id = 'hy_gameid'
    else:                           # 手Q
        session_type = 'kp_actoken'
        session_id = 'openid'

    cookie = {
        'org_loc': urllib.quote(config['balance']),
        'session_id': session_id,
        'session_type': session_type,
    }
    headers = {
        'Cookie': "; ".join('%s=%s' % (k, v) for k, v in cookie.items()),
    }

    app_key = get_platform_app_key(config, is_sandbox)
    app_key = '%s&' % app_key

    params['appid'] = config['app_id']
    params['ts'] = int(time.time())
    if params['pay_token']:
        params['openkey'] = params['pay_token']

    params.pop('access_token')
    params.pop('pay_token')

    print_log('ysdk_balance--------1111: ', 'GET', '/v3/r' + config['balance'], params, app_key)
    params['sig'] = hmac_sha1_sig('GET', '/v3/r'+config['balance'], params, app_key)

    host = get_host(is_sandbox)

    url = '%s%s?%s' % (host, config['balance'], urllib.urlencode(params))
    print_log('ysdk_balance--------2222: ', url, headers)
    http_code, content = http.get(url, headers=headers, timeout=10)
    print_log('ysdk_balance--------3333: ', http_code, content)
    if http_code != 200:
        return False

    obj = json.loads(content)

    # if obj['ret'] != 0:
    #     return False

    return obj


def pay(params):
    """
    扣除游戏币接口, 微信登录态和手Q登录态使用的支付接口相同，支付ID相同；
    服务端使用的appid和appkey都使用手Qappid和appkey
    """
    config = PLATFORM_SETTINGS.get('1')
    if not config:
        return {}

    is_sandbox = settings.DEBUG
    if not params['pay_token']:
        session_type = 'wc_actoken'
        session_id = 'hy_gameid'
    else:
        session_type = 'kp_actoken'
        session_id = 'openid'

    cookie = {
        'org_loc': urllib.quote(config['pay']),
        'session_id': session_id,
        'session_type': session_type,
        # 'appip': basic_config['app_id'],
    }
    headers = {
        'Cookie': "; ".join('%s=%s' % (k, v) for k, v in cookie.items()),
    }

    app_key = get_platform_app_key(config, is_sandbox)

    app_key = '%s&' % app_key

    params['appid'] = config['app_id']
    params['ts'] = int(time.time())
    params['sig'] = hmac_sha1_sig('GET', '/v3/r'+config['pay'], params, app_key)

    host = get_host(is_sandbox)

    url = '%s%s?%s' % (host, config['pay'], urllib.urlencode(params))

    http_code, content = http.get(url, headers=headers, timeout=10)
    print_log('payment--------: ', url, headers, http_code, content)
    if http_code != 200:
        return {}

    obj = json.loads(content)

    if obj['ret'] != 0:
        return {}

    obj['game_platform'] = config['name']

    return obj

if __name__ == '__main__':
    params = {
            'openkey': '84DCBE2C83BC5218E054A407C69BFE4B',
            'openid': '0E3B4AEF80F934ABCC480F7432B9BDA3',
            'login_type': '1',
    }
    print login_verify(None, params)

