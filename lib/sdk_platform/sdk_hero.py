# coding: utf-8

import base64
import time
import json
import urllib
from helper import http
from helper import utils
import math

import settings
from lib.utils.loggings import get_log, StatLoggingUtil
from models.server import ServerConfig
from chat.content import ContentFactory
from lib.utils.debug import print_log

GAME_ID = 173

PLATFORM_NAME = 'hero_android'
APP_ID = '10065'
APP_KEY = 'x1i9dk9c10xbwmgu2yte'
SYN_KEY = 'ajijmpyirshrlbv5ecla'
CHAT_GAME_ID = 177      # 聊天sdk用
SKEY = 'd9rDq8dQD9df0Dsds2sWq3FF6T1RfTFnRMMdfgeA6dj'   # 聊天推送用

SERVER_URL = 'http://usdk.yingxiong.com/hu/'
LOGIN_URL = '%sv1/login/checkUserInfo.lg' % SERVER_URL

PUSH_CHAT_URL = 'https://spro.yingxiong.com/fenghao/Chat/index'
PUSH_CHAT_URL_DEBUG = 'http://spro.bbsdev.yingxiong.com/fenghao/Chat/index'

# 返回数据0是成功的数据，1是失败的数据
RETURN_DATA = {
    0: 'SUCCESS',
    1: 'FAIL',
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

    data_params = {
        'cUid': req.get_argument('user_id', ''),
        # 'cName': req.get_argument('cName', ''),
        'accessToken': req.get_argument('session_id', ''),
    }

    params = {
        'pcode': APP_ID,
        'data': mark_data(data_params),
        'timestamp': int(time.time()),
    }
    sign = mark_sign(APP_KEY, params)
    params['sign'] = sign

    query_data = urllib.urlencode(params)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    http_code, content = http.post(LOGIN_URL, query_data, headers=headers)

    # print_log('x'*20, http_code, content, LOGIN_URL, query_data)

    if http_code != 200:
        return None
    result = json.loads(content)
    if int(result['code']) != 0:
        return None

    return {
        'openid': result['cUid'],       # 平台标识
        'openname': result.get('cName', ''),    # 平台昵称
    }


def payment_verify(req, params=None):
    """支付验证
    Args:
        req: request封装，以下是验证所需参数
            amount 	Double 	必须 	SDK 	成交金额，单位元
            gameOrder 	Sring 	必须 	游戏 	游戏订单号
            orderNo 	String 	必须 	SDK 	整合sdk订单号
            status 	Integer 	必须 	SDK 	交易状态，0表示成功
            selfDefine 	String 	可选 	游戏 	透传参数
            channelUid 	String 	必须 	SDK 	渠道的用户id
            payTime 	String 	必须 	SDK 	交易时间yyyy-MM-dd HH:mm:ss
            channel 	String 	必须 	SDK 	渠道类型
        params: 测试专用
    """
    if not params:
        params = {
            'data': req.get_argument('data', ''),
            'sign': req.get_argument('sign', ''),
        }

    data_sign = mark_sign(SYN_KEY, {'data': params['data']})
    if data_sign != params['sign']:
        return RETURN_DATA, None

    try:
        content = base64.b64decode(params['data'])
        data = json.loads(content)
    except:
        return RETURN_DATA, None

    pay_data = {
        'app_order_id': data['gameOrder'],  # 自定义定单id
        'order_id': data['orderNo'],  # 平台定单id
        'real_price': float(data['amount']),  # 实际金额元
        'platform': PLATFORM_NAME,  # 平台标识名
    }
    return RETURN_DATA, pay_data


def mark_data(params):
    """
    :param params: {}
    :return:
    """
    json_str = json.dumps(params, separators=(',', ':'))
    tmp_data = base64.b64encode(json_str)
    if len(tmp_data) > 51:
        final_data = change_array(list(tmp_data), [1, 33, 10, 42, 18, 50, 19, 51])
    else:
        final_data = tmp_data

    return final_data


def unmark_data(data):
    """
    :return:
    """
    if len(data) > 51:
        final_data = change_array(list(data), [1, 33, 10, 42, 18, 50, 19, 51])
    else:
        final_data = data

    print 'x'*20, final_data

    tmp_data = base64.b64decode(final_data)

    d = json.loads(tmp_data)


    return d


def change_array(chars, index):
    for i in range(0, len(index), 2):
        l = index[i]
        r = index[i+1]
        chars[l], chars[r] = chars[r], chars[l]

    return ''.join(chars)


def mark_sign(app_key, params):
    sign_items = sorted([(key, value) for key, value in params.iteritems()])
    sign_data1 = '&'.join('%s=%s' % (key, value) for key, value in sign_items)
    sign_data2 = '%s&%s' % (sign_data1, app_key)

    return utils.hashlib_md5_sign(sign_data2)


def save_player_charger_log(mm, obj, game_order_id):
    """
    英雄互娱玩家充值事件记录
    :return:
    """
    if not settings.HERO_LOG_SWITCH:
        return

    today = time.strftime('%Y%m%d%H%M%S')
    gameId = GAME_ID                # 游戏id
    channelId = 'hero'              # 渠道id
    gameServerId = settings.get_server_num(mm.server)        # 区服id
    if mm.user.appid == 'ios':      # 平台id IOS:0, Android: 1, 其他: -1
        platformId = 0
    elif mm.user.appid == 'android':
        platformId = 1
    else:
        platformId = -1
    gameUserId = mm.user.account    # cp账户id
    roleId = mm.uid                 # 角色id
    orderId = game_order_id         # 订单id
    thirdOrderId = obj['order_id']  # 第三方订单id
    state = 0                       # 订单状态
    orderTime = today               # 订单时间
    dealTime = today                # 订单成交时间
    orderAmount = obj['order_money'] * 100      # 订单金额
    currency = 'CNY'                # 币种
    charge = obj['order_diamond']   # 付费获得的货币
    donate = obj['gift_diamond']    # 付费赠送的货币
    goldType = 0                    # 货币类型
    orderType = obj['product_id']   # 档位类型  todo 要不要类型
    roleName = mm.user.name         # 角色名称
    level = mm.user.level           # 角色等级
    vipLevel = mm.user.vip          # 角色vip等级
    totalAmount = -1                # 账户总付费金额
    area = mm.user.register_ip      # IP
    eventName = 'playercharger'     # 事件名称
    deviceId = mm.user.device       # 设备ID

    log_data = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
        gameId, channelId, gameServerId, platformId, gameUserId, roleId, orderId, thirdOrderId, state, orderTime,
        dealTime, orderAmount, currency, charge, donate, goldType, orderType, roleName, level, vipLevel, totalAmount,
        area, eventName, deviceId
    )

    f_name = 'superhero2-%s-%s.log' % (time.strftime('%Y%m%d'), gameServerId)

    log = get_log('hero_log/%s' % f_name, logging_class=StatLoggingUtil, propagate=0)
    log.info(log_data)

    save_gold_obtain_log(mm, amount=orderAmount, gold_charge=obj.get('add_diamond', 0))


def save_gold_obtain_log(mm, amount=0, gold_charge=0, gold_type=0):
    """
    英雄互娱玩家虚拟货币获得事件记录
    :return:
    """
    if not settings.HERO_LOG_SWITCH:
        return

    today = time.strftime('%Y%m%d%H%M%S')
    gameId = GAME_ID                # 游戏id
    channelId = 'hero'              # 渠道id
    gameServerId = settings.get_server_num(mm.server)        # 区服id
    if mm.user.appid == 'ios':      # 平台id IOS:0, Android: 1, 其他: -1
        platformId = 0
    elif mm.user.appid == 'android':
        platformId = 1
    else:
        platformId = -1
    gameUserId = mm.user.account    # cp账户id
    roleId = mm.uid                 # 角色id
    amount = amount                 # 付费金额(分)
    if not amount:
        currency = 'N/A'
    else:
        currency = 'CNY'                # 币种

    reason = mm.action              # 原因
    subReason = ''                  # 子原因
    goldDetailFree = 0              # 免费获得的货币个数
    goldDetailDonate = 0            # 付费赠送的货币个数
    goldDetailCharge = gold_charge  # 付费获得的货币个数
    goldCurrentFree = 0             # 当前剩余的免费获得的货币数量
    goldCurrentDonate = 0           # 当前剩余的付费赠送的货币数量

    if gold_type == 0:
        goldCurrentCharge = mm.user.diamond  # 当前剩余的付费获得的级货币数量
    elif gold_type == 1:
        goldCurrentCharge = mm.user.silver
    else:
        goldCurrentCharge = 0

    roleName = mm.user.name         # 角色名称
    level = mm.user.level           # 角色等级
    vipLevel = mm.user.vip          # 角色vip等级
    totalAmount = -1                # 账户总付费金额
    area = mm.user.register_ip      # IP
    optime = today                  # 操作事件
    eventName = 'goldobtain'        # 事件名称
    deviceId = mm.user.device       # 设备ID
    goldtype = gold_type            # 货币类型

    log_data = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
        gameId, channelId, gameServerId, platformId, gameUserId, roleId, amount, currency, reason, subReason,
        goldDetailFree, goldDetailDonate, goldDetailCharge, goldCurrentFree, goldCurrentDonate, goldCurrentCharge,
        roleName, level, vipLevel, totalAmount, area, optime, eventName, deviceId, goldtype
    )

    f_name = 'superhero2-%s-%s.log' % (time.strftime('%Y%m%d'), gameServerId)

    log = get_log('hero_log/%s' % f_name, logging_class=StatLoggingUtil, propagate=0)
    log.info(log_data)


def save_gold_consume_log(mm, gold_charge=0, gold_type=0):
    """
    英雄互娱货币消耗事件记录
    :return:
    """
    if not settings.HERO_LOG_SWITCH:
        return

    today = time.strftime('%Y%m%d%H%M%S')
    gameId = GAME_ID                # 游戏id
    channelId = 'hero'              # 渠道id
    gameServerId = settings.get_server_num(mm.server)        # 区服id
    if mm.user.appid == 'ios':      # 平台id IOS:0, Android: 1, 其他: -1
        platformId = 0
    elif mm.user.appid == 'android':
        platformId = 1
    else:
        platformId = -1
    gameUserId = mm.user.account    # cp账户id
    roleId = mm.uid                 # 角色id

    reasonID = mm.action            # 消耗货币的原因ID
    subReason = ''                  # 子原因
    goldDetailFree = 0              # 消耗的免费的货币
    goldDetailDonate = 0            # 消耗的付费赠送的货币
    goldDetailCharge = gold_charge  # 消耗的付费一级货币
    goldCurrentFree = 0             # 当前剩余的免费的货币数量
    goldCurrentDonate = 0           # 当前剩余的付费赠送的货币数量
    if gold_type == 0:
        goldCurrentCharge = mm.user.diamond     # 当前剩余的付费获得的货币数量
    elif gold_type == 1:
        goldCurrentCharge = mm.user.silver
    else:
        goldCurrentCharge = 0

    roleName = mm.user.name         # 角色名称
    level = mm.user.level           # 角色等级
    vipLevel = mm.user.vip          # 角色vip等级
    totalAmount = -1                # 账户总付费金额
    area = mm.user.register_ip      # IP
    optime = today                  # 操作事件
    eventName = 'goldconsume'       # 事件名称
    deviceId = mm.user.device       # 设备ID
    goldtype = gold_type            # 货币类型

    log_data = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
        gameId, channelId, gameServerId, platformId, gameUserId, roleId, reasonID, subReason, goldDetailFree,
        goldDetailDonate, goldDetailCharge, goldCurrentFree, goldCurrentDonate, goldCurrentCharge, roleName, level,
        vipLevel, totalAmount, area, optime, eventName, deviceId, goldtype
    )

    f_name = 'superhero2-%s-%s.log' % (time.strftime('%Y%m%d'), gameServerId)

    log = get_log('hero_log/%s' % f_name, logging_class=StatLoggingUtil, propagate=0)
    log.info(log_data)


def save_item_obtain_log(mm, amount=0, gold_charge=0, item_id=0, item_count=0, item_type=0, current_num=0):
    """
    英雄互娱道具获得事件记录
    :return:
    """
    if not settings.HERO_LOG_SWITCH:
        return

    today = time.strftime('%Y%m%d%H%M%S')
    gameId = GAME_ID                # 游戏id
    channelId = 'hero'              # 渠道id
    gameServerId = settings.get_server_num(mm.server)        # 区服id
    if mm.user.appid == 'ios':      # 平台id IOS:0, Android: 1, 其他: -1
        platformId = 0
    elif mm.user.appid == 'android':
        platformId = 1
    else:
        platformId = -1
    gameUserId = mm.user.account    # cp账户id
    roleId = mm.uid                 # 角色id

    amount = amount                 # 付费金额(分)
    if not amount:
        currency = 'N/A'
    else:
        currency = 'CNY'            # 币种

    goldFree = 0                    # 购买时消耗的免费货币
    goldDonate = 0                  # 购买时消耗的付费赠送的货币
    goldCharge = gold_charge        # 购买时消耗的付费获得的货币

    reason = mm.action              # 原因

    itemId = item_id                # 道具id
    itemCount = item_count          # 道具数量
    itemDuration = -1               # 道具有效期
    itemType = item_type            # 道具类型

    level = mm.user.level           # 角色等级
    vipLevel = mm.user.vip          # 角色vip等级
    area = mm.user.register_ip      # IP
    optime = today                  # 操作事件
    eventName = 'itemobtain'        # 事件名称
    deviceId = mm.user.device       # 设备ID
    currentNum = current_num        # 道具总数

    log_data = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
        gameId, channelId, gameServerId, platformId, gameUserId, roleId, amount, currency, goldFree, goldDonate,
        goldCharge, reason, itemId, itemCount, itemDuration, itemType, level, vipLevel, area, optime, eventName,
        deviceId, currentNum,
    )

    f_name = 'superhero2-%s-%s.log' % (time.strftime('%Y%m%d'), gameServerId)

    log = get_log('hero_log/%s' % f_name, logging_class=StatLoggingUtil, propagate=0)
    log.info(log_data)


def save_item_consume_log(mm, item_id=0, item_count=0, item_type=0, current_num=0):
    """
    英雄互娱道具消耗事件记录
    :return:
    """
    if not settings.HERO_LOG_SWITCH:
        return

    today = time.strftime('%Y%m%d%H%M%S')
    gameId = GAME_ID                # 游戏id
    channelId = 'hero'              # 渠道id
    gameServerId = settings.get_server_num(mm.server)        # 区服id
    if mm.user.appid == 'ios':      # 平台id IOS:0, Android: 1, 其他: -1
        platformId = 0
    elif mm.user.appid == 'android':
        platformId = 1
    else:
        platformId = -1
    gameUserId = mm.user.account    # cp账户id
    roleId = mm.uid                 # 角色id

    reason = mm.action              # 原因

    itemId = item_id                # 道具id
    itemCount = item_count          # 道具数量
    itemDuration = -1               # 道具有效期
    itemType = item_type            # 道具类型

    level = mm.user.level           # 角色等级
    vipLevel = mm.user.vip          # 角色vip等级
    area = mm.user.register_ip      # IP
    optime = today                  # 操作事件
    eventName = 'itemconsume'       # 事件名称
    deviceId = mm.user.device       # 设备ID
    currentNum = current_num        # 道具总数

    log_data = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
        gameId, channelId, gameServerId, platformId, gameUserId, roleId, itemId, itemCount, itemDuration, itemType,
        level, vipLevel, area, optime, eventName, deviceId, reason, currentNum
    )

    f_name = 'superhero2-%s-%s.log' % (time.strftime('%Y%m%d'), gameServerId)

    log = get_log('hero_log/%s' % f_name, logging_class=StatLoggingUtil, propagate=0)
    log.info(log_data)


def send_chat_data_to_hero():
    """
    给英雄互娱推送聊天数据
    :param data: []
    :return:
    """
    debug = True
    if not settings.HERO_CHAT_SWITCH:
        return

    if debug:
        url = PUSH_CHAT_URL_DEBUG
    else:
        url = PUSH_CHAT_URL

    headers = {"Content-Type": "application/json; charset=utf-8"}
    now = int(time.time())
    sign = utils.hashlib_md5_sign(str(now) + SKEY + str(CHAT_GAME_ID))

    data = get_hero_chat_data()

    num = int(math.ceil(len(data) / 100.0))
    for i in range(num):
        _data = data[i * 100: (i + 1) * 100]
        params = {
            'time': now,
            'sign': sign,
            'data': _data,
        }

        http_code, content = http.post(url, json.dumps(params), headers=headers)

        if http_code != 200:
            return None

        result = json.loads(content)
        if int(result['code']) != 0:
            return None

    print '----send_chat_data_to_hero----success'


def get_hero_chat_data():
    """
    给英雄互娱的聊天数据
    :return:
    """

    def format_chat_data(chat_data, _type):
        """格式化返回数据"""
        format_data = {
            'server_id': '',
            'role_id': '',
            'time': '',
            'vip_level': '',
            'level': '',
            'game_id': CHAT_GAME_ID,
            'role_name': '',
            'message': '',
            'type': _type
        }
        uid = chat_data['uid']
        format_data['server_id'] = uid[:-7]
        format_data['role_id'] = uid
        format_data['time'] = time.strftime('%F %T', time.localtime(json_data['time']))
        format_data['vip_level'] = json_data['vip']
        format_data['level'] = json_data['level']
        format_data['role_name'] = json_data['name']
        format_data['message'] = json_data['msg']

        return format_data

    data = []
    content_factory = ContentFactory(settings.SERVERS['master']['redis'])

    # 世界聊天
    all_world_content = content_factory.get('AllWorld', 'chat')
    for i in all_world_content.msgs:
        json_data = settings.analysis_chat_data(i)
        if not json_data:
            continue
        new_data = format_chat_data(json_data, _type='5')
        data.append(new_data)

    sc = ServerConfig.get()
    for server_id, server_config in sc.yield_open_servers():
        # 本服聊天
        world_content = content_factory.get('WorldSystem', server_id)
        for i in world_content.msgs:
            json_data = settings.analysis_chat_data(i)
            if not json_data:
                continue
            new_data = format_chat_data(json_data, _type='1')
            data.append(new_data)

        # # 公会聊天
        # all_guild = AllGuild(server=server_id)
        # for gid in all_guild.get_all():
        #     guild_content = content_factory.get(content_factory.MAPPINGS['guild'], server_id, gid)
        #     for i in guild_content.msgs:
        #         index1 = i.find('{')
        #         index2 = i.rfind('}')
        #         if -1 in [index1, index2]:
        #             continue
        #         j = i[index1:index2 + 1]
        #         json_data = json.loads(j)
        #
        #         new_data = format_chat_data(json_data, _type=2)
        #         data.append(new_data)

    return data
