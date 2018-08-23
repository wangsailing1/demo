# -*- coding: utf-8 -*-
# Android系统 UC平台

__version__ = '1.2.4'

from lib.utils import http
import json
import time
import hashlib
import urllib
import settings
from celery_app import app
from celery_app import which_queue

GAMEID = 776283
DEBUG_VERIFY_URL = 'http://sdk.test4.9game.cn/cp/account.verifySession'
VERIFY_URL = 'http://sdk.9game.cn/cp/account.verifySession'
SERVER_URL = 'http://sdk.g.uc.cn/ss/'
PLATFORM_NAME = 'uc'

# 平台分配的api_key
APIKEY = '96ad3db58e0f526d150b18990e5078ef'

# 支付验证成功返回数据
# PAYMENT_SUCCESS_RETURN = 'SUCCESS'
# # 支付验证失败返回数据
# PAYMENT_FAILURE_RETURN = 'FAILURE'
RETURN_DATA = {
    0: 'SUCCESS',
    1: 'FAILURE',
}
# “S”还是“F”，只要验证签名SIGN匹配正确，都必须返回SUCCESS给UC服务器，此处代表已经接收到UC服务器通知，不需继续通知的含义
F_RETURN_DATA = {
    0: 'SUCCESS',
    1: 'SUCCESS',
}
# 上传角色信息url
ROLE_UPLOAD_URL_TEST = 'http://gamedata.sdk.test4.9game.cn/ng/cpserver/gamedata/ucid.game.gameData'
ROLE_UPLOAD_URL = 'http://collect.sdkyy.9game.cn:8080/ng/cpserver/gamedata/ucid.game.gameData'


def login_verify(req, sid=None, debug=False):
    """sid用户会话验证
    Args:
        sid: 从游戏客户端的请求中获取的sid值
        debug: 是否是测试环境
    Returns:
        平台ID和平台name数据
        账号标识、账号创建者和昵称
    """
    if not sid:
        sid = req.get_argument('session_id')

    if debug:
        server_url = DEBUG_VERIFY_URL
    else:
        server_url = VERIFY_URL

    data = {'sid': sid}
    post_data = json.dumps({
        'id': int(time.time()),
        'game': {'gameId': GAMEID},
        'data': data,
        'sign': uc_generate_sign(data),
    })
    http_code, content = http.post(server_url, post_data, timeout=10)

    if http_code != 200:
        return None

    obj = json.loads(content)
    if obj['state']['code'] != 1:
        return None

    return {
        'openid':     obj['data']['accountId'],

    }


def payment_verify(req, dict_data=None):
    """post_data 为回调post数据
    Args:
        post_data: 为uc回调post数据， json格式
            sign: 签名
            data: 支付票据
                orderId: UC充值订单号
                gameId: 游戏编号
                serverId: 服务器编号
                ucid: UC 账号ID
                payWay: 支付通道代码
                amount: 支付金额 单位:元。
                callbackInfo: 游戏合作商自定义参数
                orderStatus: 订单状态 S-成功支付 F-支付失败
                failedDesc: 订 单 失 败 原 因 string 详细描述 Y 如果是成功支付,则为空串。
                roleId: 角色编号 对于在SDK 中充值的,无此参数。
                intfType:订单场景0 或无此字段:SDK 方式1:WAP 方式2:WEB 方式
    Returns:
        验证成功返回支付数据，失败返回None
    """
    if not dict_data:
        body = req.request.body
        dict_data = json.loads(body)

    # if dict_data['data']['orderStatus'] != 'S':
    #     return F_RETURN_DATA, None

    sign = uc_generate_sign(dict_data['data'])
    if sign.lower() != dict_data['sign'].lower():
        return RETURN_DATA, None

    if dict_data['data']['orderStatus'] != 'S':
        return F_RETURN_DATA, None

    pay_data = {
        'real_price'  :  int(float(dict_data['data']['amount'])),         # 实际金额
        'app_order_id':  dict_data['data']['callbackInfo'],         # 自定义定单id
        'order_id':      dict_data['data']['orderId'],           # 平台定单id
        'platform':      PLATFORM_NAME,                   # 平台标识名
    }

    return RETURN_DATA, pay_data


def uc_generate_sign(data):
    """生成sign
    Args:
        data: 要签名的字典数据
    Returns:
        uc签名
    """
    sorted_data = sorted(data.iteritems(), key=lambda x: x[0])
    list_data = ['%s=%s' % (k, v) for k, v in sorted_data if k != '']
    sign_str = '%s%s' % (''.join(list_data), APIKEY)
    if isinstance(sign_str, unicode):
        sign_str = sign_str.encode('utf-8')

    return hashlib.md5(sign_str).hexdigest()


def uc_new_sign(data):
    """生成sign
        Args:
            data: 要签名的字典数据
        Returns:
            uc签名
        """
    sorted_data = sorted(data.iteritems(), key=lambda x: x[0])
    list_data = ['%s=%s' % (k, v) for k, v in sorted_data]
    sign_str = '%s%s' % (''.join(list_data), APIKEY)
    if isinstance(sign_str, unicode):
        sign_str = sign_str.encode('utf-8')

    return hashlib.md5(sign_str).hexdigest()


@app.task
def send_role_data(params, account_id):
    '''上传角色数据
    args:
        params:
            zoneId: 区服id
            zoneName: 区服名称
            roleId: 角色id
            roleName: 角色昵称
            roleCTime: 角色创建时间(单位:秒)long
            roleLevel: 角色等级
        account_id: uc账号id
    '''
    game_data = {
        'category': 'loginGameRole',
        'content': params,
    }
    sign_data = {
        'accountId': account_id,
        'gameData': urllib.quote(json.dumps(game_data)),
    }
    sign = uc_new_sign(sign_data)
    post_data = json.dumps({
        'id': int(time.time()),
        'service': 'ucid.game.gameData',
        'data': sign_data,
        'game': {'gameId': GAMEID},
        'sign': sign,
    })
    if settings.DEBUG:
        post_url = ROLE_UPLOAD_URL_TEST
    else:
        post_url = ROLE_UPLOAD_URL
    try:
        http_code, content = http.post(post_url, post_data, timeout=2)
    except:
        pass
    return


def send_role_data_uc(user):
    """
    上传uc玩家数据
    """
    if settings.DEBUG:
        return

    if user.account.startswith('uc') or user.account.startswith('wandoujia'):
        from models.server import get_server_config
        uc_role_data = {
            'zoneId': settings.get_server_num(user._server_name),
            'zoneName': get_server_config(user._server_name)['name'],
            'roleId': user.uid,
            'roleName': user.name,
            'roleCTime': int(user.reg_time),
            'roleLevel': user.level,
        }
        if settings.CELERY_SWITCH:
            send_role_data.apply_async(args=(uc_role_data, user.account.split('_')[1]), queue=which_queue(user._server_name))
        else:
            send_role_data(uc_role_data, user.account.split('_')[1])
    return

