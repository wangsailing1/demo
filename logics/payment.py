#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import math
import json
import urllib
import traceback

import settings
from models.payment import *
from gconfig import game_config
from lib.core.environ import ModelManager
from lib.utils.timelib import now_time_to_str
from lib.sdk_platform.manager import sdk_manager
from return_msg_config import i18n_msg
from gconfig import MUITL_LAN, charge_scheme_func
from lib.sdk_platform.sdk_hero import save_player_charger_log
from lib.sdk_platform.helper import http
from lib import utils
from logics.egg import Egg
from lib.utils.debug import print_log
from tools.gift import add_mult_gift


def pay_apply(mm, obj, charge_config):
    """ 支付统一函数

    :param mm: ModelManager对象
    :param obj: 充值数据字典对象，现统一格式
            'order_id': '',         # 订单id          ok
            'level': 0,             # 充值时的等级    ok
            'old_diamond': 0,          # 充值时的钻石    ok
            'gift_diamond': 0,         # 赠送的钻石     ok
            'order_diamond': 0,        # 购买钻石        ok
            'order_money': 0,       # 充值金额      ok
            'order_rmb': 0,         # 充值rmb金额      ok
            'currency': '',         # 金额币种      ok
            'order_time': '',       # 充值时间      ok
            'platform': 0,          # 充值平台      ok
            'product_id': 0,        # 配置id         ok
            'scheme_id': 0,         # 平台配置id      ok
            'raw_data': '',         # 平台充值数据    ok
            'user_id': '',          # 用户uid         ok
            'uin': '',              # 平台id          ok
            'admin': '',            # admin账号
            'reason': 0,            # admin充值原因
    :return True | False
    """
    amount = 0
    obj['old_diamond'] = mm.user.diamond
    obj['level'] = mm.user.level
    obj['user_id'] = mm.user.uid
    over_diamond = obj.pop('over_diamond', 0)
    can_open_gift = obj.pop('can_open_gift', True)
    # 已完成订单直接返回True
    payment = Payment()
    if payment.exists_order_id(obj['order_id']):
        return True
    act_id = obj.pop('act_id') if 'act_id' in obj else 0
    act_item_id = obj.pop('act_item_id') if 'act_item_id' in obj else 0
    if payment.insert_pay(obj, commit=False):
        order_diamond = obj['order_diamond']
        gift_diamond = 0 # obj['gift_diamond'] # 暂时废弃
        gift = charge_config['gift']          # 香水等礼物
        order_money = obj['order_money']
        order_rmb = obj['order_rmb']
        product_id = obj['product_id']
        double_pay = obj['double_pay']
        open_gift = charge_config.get('sort', 0)
        add_vip_exp = charge_config.get('level_exp', 0)

        if double_pay:
            amount = order_diamond * 2 + gift_diamond + over_diamond
            # mm.user.add_diamond(order_diamond * 2 + gift_diamond)
            mm.user_payment.add_double_pay(product_id)
        else:
            amount = order_diamond + gift_diamond + over_diamond
            # mm.user.add_diamond(order_diamond + gift_diamond)

        mm.user.diamond_charge += amount
        # 助理特权礼包 只能领一次
        if open_gift == 4 and mm.assistant.assistant_gift:
            gift = []

        add_diamond = mm.user_payment.add_pay(open_gift, obj['currency'], price=order_money, order_diamond=order_diamond, order_rmb=order_rmb,
                                              product_id=product_id, can_open_gift=can_open_gift,act_id=act_id,act_item_id=act_item_id)
        if add_diamond:
            mm.user.add_diamond(int(add_diamond))

        # 砸金蛋
        egg = Egg(mm)
        try:
            egg.add_payment_and_item_times(order_diamond)
        except:
            print_log(traceback.format_exc())

        # 钻石福利基金
        try:
            mm.foundation.add_score(order_diamond)
        except:
            print_log(traceback.format_exc())

        # 累积充值活动记录钻石
        server_type = int(mm.user.config_type)
        if server_type == 1:
            pass
            # mm.server_recharge.reward(order_diamond + gift_diamond, order_money, product_id, charge_config=charge_config)
            # # 每日充值活动记录钻石
            # mm.server_daily_recharge.reward(order_diamond + gift_diamond, product_id)
            #
            # # 豪华签到记录钻石或者现金
            # mm.server_sign_recharge.reward(order_diamond + gift_diamond, order_money)
            # # 每日礼包
            # mm.server_daily_package.recharge_reward(product_id)
            #
            # # 许愿池
            # mm.server_charge_roulette.add_out_remain_time(order_diamond + gift_diamond, product_id)
            #
            # # 限时特惠
            # mm.server_limit_discount.buy_gift(product_id)
            #
            # # 天降红包
            # mm.server_red_bag.pay_trigger(product_id, amount)
        else:
            pass
            # mm.active_recharge.reward(order_diamond + gift_diamond, order_money, product_id, charge_config=charge_config)
            # # 每日充值活动记录钻石
            # mm.active_daily_recharge.reward(order_diamond + gift_diamond, product_id)
            #
            # # 豪华签到记录钻石或者现金
            # mm.sign_recharge.reward(order_diamond + gift_diamond, order_money)
            # # 每日礼包
            # mm.daily_package.recharge_reward(product_id)
            #
            # # 许愿池
            # mm.charge_roulette.add_out_remain_time(order_diamond + gift_diamond, product_id)
            #
            # # 限时特惠
            # mm.limit_discount.buy_gift(product_id)
            #
            # # 天降红包
            # mm.red_bag.pay_trigger(product_id, amount)

        # mm.user.record_privilege_gift(charge_config=charge_config)
        mm.superplayer.add_day_pay(order_diamond)
        mm.user.add_vip_exp(add_vip_exp, is_save=False)
        add_mult_gift(mm, gift)
        mm.user.save()
        mm.rmbfoundation.save()

        # 购买商品日期记录，用于刷新次数
        mm.user_payment.add_buy_log(product_id)

        # 首充礼包
        mm.user_payment.add_first_charge(price=order_rmb, charge_config=charge_config)
        mm.user_payment.add_add_recharge(price_dict={1:order_diamond,2:order_rmb})
        # # 超值签到
        # mm.pay_sign.set_pay_sign_status(order_money+gift_diamond, product_id)

        # 充值项奖励
        # mail_dict = mm.mail.generate_mail(
        #     i18n_msg[24],
        #     title=i18n_msg['charge'],
        #     gift=charge_config['charge_reward'],
        # )
        # mm.mail.add_mail(mail_dict)

        # # 福利中心
        # mm.gift_center.payment(product_id, order_money, diamond=order_diamond)

        # 统一保存, 下面不要写逻辑
        mm.do_save()
        payment.commit_transaction()

        obj['add_diamond'] = amount

        return True
    else:
        return False


def analysis_order(order_id, split='-'):
    """ 解析游戏订单号

    :param order_id:
    :param split:
    :return:
    """
    order_list = order_id.split(split)
    order_len = len(order_list)
    if order_len == 6:
        user_id, server_id, goods_id, _, act_id, act_item_id = order_list
        goods_id = int(goods_id)
        charge_config = game_config.charge[goods_id]
    elif order_len == 5:
        user_id, server_id, goods_id, act_id, act_item_id = order_list
        goods_id = int(goods_id)
        charge_config = game_config.charge[goods_id]
    else:
        user_id, goods_id, charge_config, act_id, act_item_id = None, 0, {}, 0, 0

    return user_id, goods_id, charge_config, act_id, act_item_id


def generate_pay(user_id, goods_id, order_id, amount, uin, platform, act_id, act_item_id, raw_data='',
                 currency=CURRENCY_CNY, charge_config=None, pay_tp=-1, game_order_id=''):
    """ 生成支付数据

    :param user_id: 游戏中uid
    :param goods_id: 购买的充值id
    :param order_id: 平台方订单号
    :param amount: 支付金额单位元
    :param uin: 平台账号
    :param platform: 平台标示
    :param raw_data: 原始数据
    :param currency: 币种, 默认人民币
    :return:
    """
    if isinstance(user_id, basestring):
        mm = ModelManager(user_id, async_save=True)
    else:
        mm = user_id
    lan_sort = MUITL_LAN[mm.user.language_sort]
    charge_config = charge_config or game_config.charge[goods_id]
    order_diamond = charge_config['diamond']
    gift_diamond = charge_config['gift_diamond']
    # order_money = charge_config['price']
    scheme_id = charge_config['cost']

    order_money = charge_config['price_%s' % CURRENCY_COUNTRY.get(currency, 'CN')]
    can_open_gift = True
    real_product_id = goods_id
    over_diamond = 0
    # 实际充值金额小于订单金额
    if amount < order_money:
        real_product_id = 0     # todo 计算给多少钻石
        can_open_gift = False   # todo 限制哪些活动
        order_diamond = int(math.ceil(amount * CURRENCY_VIP_EXP.get(currency, 1)))
        gift_diamond = 0
    # 实际充值金额大于订单金额
    elif amount > order_money:
        over_money = amount - order_money
        over_diamond = int(math.ceil(over_money * CURRENCY_VIP_EXP.get(currency, 1)))
        # 如果是谷歌支付，则直接按照泰语的给，不bibi
    if int(pay_tp) == 1:
        order_diamond = charge_config['diamond']
        gift_diamond = charge_config['gift_diamond']
        amount = charge_config['price_TW']
        over_diamond = 0
        platform = 'google-kvgames'
        currency = 'USD'
    obj = {
        'product_id': goods_id,
        'scheme_id': scheme_id,
        'order_diamond': order_diamond,
        'gift_diamond': gift_diamond,
        'double_pay': mm.user_payment.is_double_pay(goods_id, charge_config),
        'order_money': float(amount),
        'order_rmb': float(currencys.get(currency, 1) * amount),
        'order_id': order_id,
        'order_time': now_time_to_str(),
        'raw_data': raw_data,
        'platform': platform,
        'uin': uin,
        'currency': currency,
        'can_open_gift': can_open_gift,
        'real_product_id': real_product_id,
        'lan_sort': lan_sort,
        'over_diamond': over_diamond,
        'act_id': act_id,
        'act_item_id': act_item_id,
    }

    flag = pay_apply(mm, obj, charge_config)

    if platform in ['hero_android']:
        game_order_id = game_order_id or order_id
        save_player_charger_log(mm, obj, game_order_id=game_order_id)

    return flag


def payment_verify(req, tp=None):
    """ 支付验证

    :param sdk:
    :param args:
    :param kwargs:
    :return:
    """
    params = req.params()
    # 数字开头的平台模块名加cn前缀
    module_name = ('sdk_%s' % tp)
    method_name = 'payment_verify'
    module = __import__('lib.sdk_platform.%s' % module_name, globals(), locals(), [method_name])
    callback_method = getattr(module, method_name)
    return_data, pay_data = callback_method(req)
    if not pay_data:
        return return_data[1]
    game_order_id = pay_data['app_order_id']

    # todo 兼容英雄互娱二测和三测回调地址一样的问题
    test_uid = game_order_id.split('-')[0]
    if settings.UID_PREFIX in ['gt'] and test_uid[:4] == 'gtt1':
        url = 'http://yxhysuper2game3.yingxiong.com/inreview_release/pay-callback-hero'

        test_params = {
            'data': req.get_argument('data', ''),
            'sign': req.get_argument('sign', ''),
        }
        query_data = urllib.urlencode(params)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        http_code, content = http.post(url, query_data, headers=headers)
        if http_code != 200:
            return return_data[1]
        return content


    order_id = pay_data['order_id']
    amount = pay_data['real_price']
    uin = req.get_argument('uid', '')
    platform = pay_data['platform']
    pay_tp = pay_data.get('pay_tp', -1)

    user_id, goods_id, charge_config, act_id, act_item_id = analysis_order(game_order_id)
    if user_id is None:
        return return_data[1]
    real_price = charge_config['price_TW']
    if pay_data.get('currency', ''):
        currency = pay_data['currency']
        success = generate_pay(user_id, goods_id, order_id, amount, uin,
                               platform, act_id, act_item_id, charge_config=charge_config, currency=currency, pay_tp=pay_tp, game_order_id=game_order_id)
    else:
        success = generate_pay(user_id, goods_id, order_id, amount, uin,
                               platform, act_id, act_item_id, charge_config=charge_config, pay_tp=pay_tp, game_order_id=game_order_id)
    rc = 0 if success else 1

    return return_data[rc]


def virtual_pay_by_admin(mm, goods_id, admin=None, reason='', tp='admin', currency=CURRENCY_CNY, charge_config=None, act_id=0, act_item_id=0):
    """ tp: admin 后台代充，算真实收入
        admin_test  管理员测试用

    :param mm:
    :param goods_id:
    :param admin:
    :param reason:
    :param tp:
    :param currency:
    :return:
    """
    goods_id = int(goods_id)
    charge_config = charge_config or game_config.charge[goods_id]
    # scheme_id = charge_config['cost']
    order_diamond = charge_config['diamond']
    gift_diamond = charge_config['gift_diamond']
    order_money = charge_config['price_rmb']

    order_id = '%s-%s-%s-%s_%s' % (mm.user.uid, mm.user._server_name, goods_id, int(time.time()), utils.rand_string(3))

    # ios充值6元 和 30 元充值项 同一个uid 24小时之内只能各支付三次
    if goods_id in [8, 9]:
        mm.user.ios_payment[goods_id] = 1 + mm.user.ios_payment.get(goods_id, 0)

    obj = {
        'product_id': goods_id,
        'scheme_id': 1,
        'order_diamond': order_diamond,
        'gift_diamond': gift_diamond,
        'double_pay': mm.user_payment.is_double_pay(goods_id, charge_config),
        'order_money': order_money,
        'order_rmb': order_money,
        'order_id': order_id,
        'order_time': now_time_to_str(),
        'raw_data': 'virtual_pay_by_admin',
        'platform': tp,
        'uin': mm.user.account,
        'currency': currency,
        'admin': admin,
        'reason': reason,
        'act_id': act_id,
        'act_item_id': act_item_id,
    }
    save_player_charger_log(mm, obj, order_id)

    return pay_apply(mm, obj, charge_config)


def order_jinli(req):
    """ 金立 生成订单号

    :param req:
    :return:
    """
    params = req.params()

    sdk_jinli = sdk_manager.get_sdk('sdk_jinli', 'jinli')

    return sdk_jinli.get_order(params, notify_url=settings.get_payment_callback_url('jinli'))


def order_vivo(req):
    """ vivo 生成订单号

    :param req:
    :return:
    """
    params = req.params()

    sdk_vivo = sdk_manager.get_sdk('sdk_vivo', 'vivo')

    return sdk_vivo.get_order(params, notify_url=settings.get_payment_callback_url('vivo'))


def order_xmwan(req):
    """ 熊猫玩 生成订单号

    :param req:
    :return:
    """
    params = req.params()

    sdk_xmwan = sdk_manager.get_sdk('sdk_xmwan', 'xmwan')

    return sdk_xmwan.get_order(params, notify_url=settings.get_payment_callback_url('xmwan'))


def balance_tencent(hm):
    """ 腾讯移动应用平台 余额

    :param hm:
    :return:
    """
    params = hm.params()

    sdk_tencent = sdk_manager.get_sdk('sdk_tencent', 'tencent')

    return sdk_tencent.get_balance(params, debug=settings.DEBUG)


def pay_apple(hm):
    """ apple 支付回调接口

    :param hm:
    :return:
    """
    from lib.sdk_platform import sdk_appstore as platform_app
    user = hm.mm.user
    receipt_data = hm.get_argument('receipt-data', '')
    real_product_id = hm.get_argument('productIndex', is_int=True)
    order_id_own = hm.get_argument('order_id')
    user_id, _, _, act_id, act_item_id = analysis_order(order_id_own)
    if not receipt_data:
        body_date = hm.req.request.body
        body_str = json.loads(body_date)
        receipt_data = body_str['receipt-data']
    pay_data = platform_app.payment_verify(receipt_data, settings.DEBUG)

    if isinstance(pay_data, bool):
        return {}

    # 过滤不是本公司游戏的充值回调请求
    if pay_data['bid'] not in settings.APP_STORE_BID_LIST:
        return {'status': 'ok'}
    order_id = pay_data['transaction_id']
    product_id = pay_data['product_id']
    raw_data = pay_data['purchase_date'][:10]
    charge_config = None
    goods_id = None

    charge_ios_mapping = game_config.get_charge_ios_mapping()
    if product_id in charge_ios_mapping:
        suit_id = charge_ios_mapping[product_id]
        # www.mancalajbsg.com_jbsg150_1
        qu_str = suit_id.split('_')[0]
        product_id = suit_id.replace('%s_' % qu_str, '')

    for k, v in game_config.charge.iteritems():
        if v['cost'] == product_id:
            charge_config = v
            goods_id = k
            break

    if real_product_id:
        if game_config.charge.get(real_product_id, {}).get('cost', '') == product_id:
            goods_id = real_product_id
            charge_config = game_config.charge.get(real_product_id, {})

    # if real_product_id:
    #     charge_config = game_config.charge.get(real_product_id, {})
    #     if charge_config.get('cost', '') == product_id:
    #         goods_id = real_product_id
    # else:
    #     for k, v in game_config.charge.iteritems():
    #         if v['cost'] == product_id:
    #             charge_config = v
    #             goods_id = k
    #             break

    # ios充值6元 和 30 元充值项 同一个uid 24小时之内只能各支付三次
    if goods_id in [8, 9]:  # todo 商品要换
        user.ios_payment[product_id] = 1 + user.ios_payment.get(product_id, 0)

    if charge_config is None:
        return {}
    uin = user.account
    scheme_id = charge_config['cost']
    order_diamond = charge_config['diamond']
    gift_diamond = charge_config['gift_diamond']
    lan_sort = MUITL_LAN[hm.mm.user.language_sort]
    order_money = charge_config['price_%s' % lan_sort]
    order_rmb = float(currencys.get('USD', 1) * order_money)
    if hm.mm.user.language_sort in ['1', 1]:
        order_rmb = order_money
        order_money = round(order_money / currencys.get('USD', 1), 2)
    obj = {
        'product_id': goods_id,
        'scheme_id': scheme_id,
        'order_diamond': order_diamond,
        'gift_diamond': gift_diamond,
        'double_pay': hm.mm.user_payment.is_double_pay(goods_id, charge_config),
        'order_money': order_money,
        'order_rmb': order_rmb,
        'order_id': order_id,
        'order_time': now_time_to_str(),
        'raw_data': raw_data,
        'platform': platform_app.PLATFORM_NAME,
        'uin': uin,
        'can_open_gift': True,
        'real_product_id': goods_id,
        'lan_sort': lan_sort,
        'act_id': act_id,
        'act_item_id': act_item_id,
    }
    return pay_apply(hm.mm, obj, charge_config)


def pay_tencent(hm):
    """ 腾讯移动应用平台 支付回调接口

    :param hm:
    :return:
    """
    user = hm.user

    params = hm.params()

    if not params:
        return {}

    goods_id = int(params.get('product_id'))

    charge_config = game_config.charge.get(goods_id)

    if charge_config is None:
        return {}

    sdk_tencent = sdk_manager.get_sdk('sdk_tencent', 'tencent')

    pay_data = sdk_tencent.payment_verify(params, debug=settings.DEBUG)

    if isinstance(pay_data, bool):
        return {}

    order_id = pay_data['order_id']

    user_id = user
    amount = charge_config['price']
    uin = user.account

    generate_pay(user_id, goods_id, order_id, amount, uin,
                 sdk_tencent.name, charge_config=charge_config)

    return {'status': 'ok'}


def ysdk_pay(hm, result_data):
    """ysdk支付验证
    """
    from lib.sdk_platform import sdk_ysdk as platform_app

    mm = hm.mm
    lan_sort = mm.user.language_sort
    uin = mm.user.account
    product_id = int(hm.get_argument('product_id'))

    charge_config = game_config.charge.get(product_id)

    if not charge_config:
        return False

    params = {
        'openid': hm.get_argument('openid', ''),
        'openkey': hm.get_argument('openkey', ''),
        'pay_token': hm.get_argument('pay_token', ''),
        'pf': hm.get_argument('pf', ''),
        'zoneid': hm.get_argument('zoneid', ''),
        'amt': int(charge_config['price_CN'] * 10),
        'pfkey': hm.get_argument('pfkey', ''),
    }

    pay_data = platform_app.pay(params)

    if not pay_data:
        return False

    scheme_id = game_config.charge[product_id]['cost']
    order_diamond = game_config.charge[product_id]['diamond']
    gift_diamond = game_config.charge[product_id]['gift_diamond']
    real_price = game_config.charge[product_id]['price_CN']
    can_open_gift = True    # 标识是否可以开启周卡月卡活动

    result_data.update(pay_data)
    result_data['scheme_id'] = scheme_id
    result_data['product_id'] = product_id

    # 根据实际支付的钱做一些特殊处理，如果没有则忽略
    # order_money = pay_data['order_money']
    # if real_price > order_money:
    #     can_open_gift = False
    #     if order_money < 100:
    #         order_coin = int(order_money * 11)
    #     else:
    #         order_coin = int(order_money * 11.5)
    #     gift_coin = 0
    # elif real_price > order_money:
    #     over_money = real_price - order_money
    #     if order_money < 100:
    #         gift_coin += int(over_money * 11)
    #     else:
    #         gift_coin += int(over_money * 11.5)

    order_money = real_price

    obj = {
        'product_id': product_id,
        'scheme_id': scheme_id,
        'order_diamond': order_diamond,
        'gift_diamond': gift_diamond,
        'double_pay': mm.user_payment.is_double_pay(product_id, charge_config),
        'order_money': order_money,
        'order_rmb': order_money,
        'order_id': pay_data['billno'],
        'order_time': now_time_to_str(),
        'raw_data': '',
        'platform': pay_data['game_platform'],
        'uin': uin,
        'currency': 'RMB',
        'can_open_gift': can_open_gift,
        'real_product_id': product_id,
        'lan_sort': lan_sort,
        'over_diamond': 0,
    }

    return pay_apply(mm, obj, charge_config)
