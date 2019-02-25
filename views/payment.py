#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import json
import time

import settings
from logics import payment
from gconfig import game_config
from lib.sdk_platform.manager import sdk_manager
from logics.payment import payment_verify
from tools.gift import add_mult_gift
from models.payment import currencys


def index(hm):
    """ 充值首页

    :param hm:
    :return:
    """
    mm = hm.mm

    double = mm.user_payment.get_double_pay()
    # week_status = mm.user_payment.get_status(tp='week')
    # month_status = mm.user_payment.get_status(tp='month')
    result = {
        'double': double,
        # 'week_status': week_status,
        # 'month_status': month_status,
        'buy_log': mm.user_payment.buy_log.keys(),     # 充值购买id记录
        'vip_gift': mm.user.vip_gift,  # 已购买的特权礼包id
    }
    if 'ios' in mm.user.appid:
        result.update({
            'ios_pay': mm.user.ios_payment,  # iOS小额充值信息
            'limit_times': {8: 3, 9: 3},  # 购买上限 todo 小额充值的商品id需要改
        })


    return 0, result


def first_recharge(hm):
    """
    首充index
    :param hm:
    :return:
    """
    mm = hm.mm

    if 'tw' in settings.ENV_NAME:
        currency = 'USD'
    else:
        currency = 'CNY'
    price = round(mm.user_payment.charge_price / currencys.get(currency, 1), 2)

    data = {
        'charge_done': mm.user_payment.first_charge_done,   # 已领过奖励的id
        # 'price': price,             # 已充值金额
        'currency': currency,       # 货币
        # 'first_remain_time': mm.user_payment.get_first_charge_remain_time(),  # 首充倒计时
    }

    return 0, data


def get_first_charge(hm):
    """
    领取首充礼包
    :param hm:
    :return:
    """
    mm = hm.mm

    reward_id = hm.get_argument('reward_id', is_int=True)

    if reward_id <= 0:
        return 'error_100', {}

    first_recharge_config = game_config.first_recharge.get(reward_id)
    if not first_recharge_config:
        return 'error_config', {}

    if mm.user_payment.get_first_charge_status(reward_id) == 2:
        return 1, {}  # 奖励已领取

    if mm.user_payment.get_first_charge_status(reward_id) == 0:
        # if reward_id == 1:
        #     now = int(time.time())
        #     if now - mm.user.reg_time < first_recharge_config['time'] * 3600:
        #         return 2, {}    # 没有到领取时间
        # else:
        #     return 3, {}    # 未达到条件
        return 3, {}  # 未达到条件

    mm.user_payment.add_first_charge_done(reward_id)
    reward = add_mult_gift(mm, first_recharge_config['gift'])

    mm.user_payment.save()

    result = {
        'reward': reward,
        'first_recharge_red_dot': mm.user_payment.first_charge_alert()
    }
    result.update(first_charge(hm)[1])

    return 0, result


def add_recharge_index(hm):
    mm = hm.mm

    return 0, {'add_recharge': mm.user_payment.add_recharge_done,
               'remain_time':mm.user_payment.get_add_recharge_remain_time(),
               'version': mm.user_payment.add_recharge_version,
               'price': mm.user_payment.add_recharge_price}

def get_add_recharge(hm):
    mm = hm.mm

    reward_id = hm.get_argument('reward_id', is_int=True)

    if reward_id <= 0:
        return 'error_100', {}

    add_recharge_config = game_config.add_recharge.get(reward_id)
    if not add_recharge_config:
        return 'error_config', {}

    if mm.user_payment.get_add_recharge_status(reward_id) == 2:
        return 1, {}  # 奖励已领取

    if mm.user_payment.get_add_recharge_status(reward_id) == 0:
        return 3, {}  # 未达到条件

    mm.user_payment.add_add_recharge_done(reward_id)
    reward = add_mult_gift(mm, add_recharge_config['reward'])

    mm.user_payment.save()

    result = {
        'reward': reward,
        'add_recharge_red_dot': mm.user_payment.get_add_recharge_red_dot()
    }
    result.update(add_recharge_index(hm)[1])

    return 0, result


def notify_url(hm):
    """ 回调地址

    :param hm:
    :return:
    """

    tp = hm.get_argument('tp', '')

    notifyurl = settings.get_payment_callback_url(tp)

    result = {}
    if notifyurl:
        result[tp] = notifyurl

    return 0, result


def pay(hm):
    """ 支付接口
    """
    tp = hm.get_argument('tp', 'apple')
    func = getattr(payment, 'pay_%s' % tp, None)

    if func is None:
        return 1, {}
    rc = func(hm)

    if not rc:
        return 1, {}
    rc = {'status': 'ok'}
    return 0, rc


def pay_order(hm):
    """ 获取订单

    :param hm:
    :return:
    """
    tp = hm.get_argument('tp', '')
    func = getattr(payment, 'order_%s' % tp, None)

    if func is None:
        return 1, {}

    rs = func(hm)
    if not rs:
        return 2, {}

    return 0, rs

def balance(hm):
    """ 余额

    :param hm:
    :return:
    """
    tp = hm.get_argument('tp', '')
    func = getattr(payment, 'balance_%s' % tp, None)

    if func is None:
        return 1, {}

    rs = func(hm)
    if not rs:
        return 2, {}

    return 0, rs


def callback(request, tp=None):
    """ 支付回调

    :param request:
    :param tp:
    :return:
    """
    pay_status = payment_verify(request,tp)
    return pay_status


def get_order_meizu(env):
    """meizu充值，后端获取订单准备数据
    Args:
        request包含的参数如下:
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
    Returns:
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
    from lib.sdk_platform import sdk_meizu as meizu_app

    params = {
        'app_id': env.get_argument('app_id', ''),
        'cp_order_id': env.get_argument('cp_order_id'),
        'uid': env.get_argument('uid'),
        'product_id': env.get_argument('product_id', '0'),
        'product_subject': env.get_argument('product_subject', ''),
        'product_body': env.get_argument('product_body', ''),
        'product_unit': env.get_argument('product_unit', u'元'),
        'buy_amount': env.get_argument('buy_amount', '1'),
        'product_per_price': env.get_argument('product_per_price', ''),
        'total_price': env.get_argument('total_price', ''),
        'create_time': env.get_argument('create_time', ''),
        'pay_type': env.get_argument('pay_type', '0'),
        'user_info': env.get_argument('user_info', ''),
    }
    # 2016.7.7改为api请求
    # return 0, meizu_app.get_meizu_order(params)
    rs = meizu_app.get_meizu_order(params)
    if not rs:
        return 2, {}

    return 0, rs


def query_meizu_order(env):
    """ cp_order_id:   游戏生成的 order_id
            ts:        Unix_timestamp.eg: 1396424644
    """
    from lib.sdk_platform import sdk_meizu as meizu_app

    params = {
        'cp_order_id': env.get_argument('cp_order_id'),
        'ts': env.get_argument('ts'),
    }
    rs = meizu_app.query_meizu_order(params)
    if not rs:
        return 2, {}

    return 0, rs


def ysdk_pay(hm):
    """ ysdk支付接口
    /pay/?method=msdk_pay
    &openid=976BDA2E7D1DFA56F7AC9D3DCC3981CD
    &openkey=5AEC078161F774762226D3402CAF6864
    &pay_token=3DDCF4F5EF3C01203752EE9844CE7039
    &pf=desktop_m_qq-73213123-android-73213123-qq-1105133963-976BDA2E7D1DFA56F7AC9D3DCC3981CD
    &pfkey=4156de3b6f188f5c5c5d4af6f2827857
    &zoneid=1
    &price=1.0
    &user_token=m1234567
    &pt=msdk
    """
    from lib.utils.debug import print_log

    pay_method = getattr(payment, '%s_pay' % 'ysdk')
    result_data = {}
    if not pay_method(hm, result_data):
        result_data['custom_msg'] = result_data.get('msg', '')
        return 2, result_data

    # result_data['step'] = env.user.shop.vip_record_data
    result_data['double_pay'] = hm.mm.user_payment.get_double_pay()
    return 0, result_data



def ysdk_balance(hm):
    """
    获取ysdk的余额
    /pay/?method=msdk_balance
    &openid=976BDA2E7D1DFA56F7AC9D3DCC3981CD
    &openkey=5AEC078161F774762226D3402CAF6864
    &pay_token=6A9253E9C0B256FB750F0E38A7CD29D6
    &pf=desktop_m_qq-73213123-android-73213123-qq-1105133963-976BDA2E7D1DFA56F7AC9D3DCC3981CD
    &pfkey=e6f48a324832f62d22676d553595c239
    &zoneid=1
    """
    from lib.sdk_platform import sdk_ysdk as platform_app

    params = {
        'openid': hm.get_argument('openid', ''),
        'openkey': hm.get_argument('openkey', ''),
        'pay_token': hm.get_argument('pay_token', ''),
        'pf': hm.get_argument('pf', ''),
        'pfkey': hm.get_argument('pfkey', ''),
        'access_token': hm.get_argument('access_token', ''),
        'zoneid': hm.get_argument('zoneid', ''),
    }

    data = platform_app.balance(params, is_sandbox=settings.DEBUG)
    if not data:
        return 2, {}
    # ret = data['ret']
    return 0, data


def get_vivo_order(hm):
    """vivo充值，后端获取订单准备数据
    Args:
        request包含的参数如下:
            storeOrder: 商户自定义的订单号
            orderAmount: 交易金额 单位：元 精确到小数点后两位
            orderTitle: 商品的标题
            orderDesc: 订单描述
    Returns:
        {u'vivoSignature': u'2e1aeecb9e577e4b49d66a97a007ff33',
         u'respCode': 200,
         u'vivoOrder': u'139825362337769030858',
         u'respMsg': u'success',
         u'signMethod': u'MD5',
         u'signature': u'2d9d497bf2a2c9f987b336aec751426d',
         u'orderAmount': u'10.00'}
    """
    from lib.sdk_platform import sdk_vivo as vivo_app

    params = {
        'cpOrderNumber': hm.get_argument('storeOrder'),
        'orderAmount': hm.get_argument('orderAmount'),
        'orderTitle': hm.get_argument('orderTitle'),
        'orderDesc': hm.get_argument('orderDesc'),
        'notifyUrl': settings.get_payment_callback_url("vivo"),
    }
    rs = vivo_app.get_vivo_order(params)
    if not rs:
        return 2, {}

    return 0, rs


def query_vivo_order(hm):
    """vivo充值，查询订单数据
    Args:
        request包含的参数如下:
            storeOrder: 商户自定义的订单号
            orderAmount: 交易金额 单位：元 精确到小数点后两位
            vivoOrder: vivo订单号
    """
    from lib.sdk_platform import sdk_vivo as vivo_app

    params = {
        'cpOrderNumber': hm.get_argument('cpOrderNumber'),
        'orderAmount': hm.get_argument('orderAmount'),
        'orderNumber': hm.get_argument('orderNumber'),
    }
    rs = vivo_app.query_vivo_order(params)
    if not rs:
        return 2, {}

    return 0, rs


def get_jinli_order(hm):
    """金立手机平台充值，后端获取订单准备数据
    Args:
        request包含的参数如下:
            player_id:    字符串 玩家id（不参与签名）
            deal_price:   字符串 必填 商品总金额
            out_order_no: 字符串 必填 商户订单号，数字字母构成，32个字符以内。 商户需要确保订单号的唯一性，不能重复
            subject:      字符串 必填 商品名称，32个字符以内，不能含有半用 “+”、“&”或特殊字符集
            total_fee:    字符串 必填 需支付金额， 值必须等 于商品总 金额 23 （deal_price字段）
    Returns:
        {
          "status": "200010000",
          "api_key": "F5133AF3BA924202B1B122000EE79AA0",
          "description": "成功创建订单",
          "out_order_no": "29e0d905a798709b1530911d68313016",
          "submit_time": "20140514170045",
          "order_no": "537330be0cf2072b767c2e95"
        }
    """
    from lib.sdk_platform import sdk_jinli as platform_app

    params = {
        'player_id': hm.get_argument('player_id'),
        'deal_price': hm.get_argument('deal_price'),
        'out_order_no': hm.get_argument('out_order_no'),
        'subject': hm.get_argument('subject'),
        'total_fee': hm.get_argument('total_fee'),
    }
    rs = platform_app.create_pay_order(params)
    if not rs:
        return 2, {}

    return 0, rs


def get_order_uc(hm):
    """
    /api/?method=payment.get_uc_order&user_token=ql23598550&mk=1&tp=uc&channel_id=&
    device_mark=wifi02:00:00:00:00:00&version=1.1.5&__ts=1482397566&platform_channel=uc&identifier=861795032250667&
    devicename=C106&device_mem=2977488896&
    amount=1&
    accountId=ssh1gamefae424ee798d4d728352fb6abd3a2be6153049&
    cpOrderId=ql23598550-ql2-10-1482397566
    """
    from lib.sdk_platform import sdk_uc

    notifyUrl = settings.get_payment_callback_url('uc')
    data = {
        'callbackInfo': hm.get_argument('callbackInfo', ''),
        'amount': hm.get_argument('amount', ''),
        'notifyUrl': notifyUrl,
        'cpOrderId': hm.get_argument('cpOrderId', ''),
        'accountId': hm.get_argument('accountId', ''),
    }
    # print_log('--views.payment.get_uc_order-1', data)
    sign = sdk_uc.uc_new_sign(data)
    # print_log('--views.payment.get_uc_order-2', sign)
    return 0, {
        'sign': sign,
    }

