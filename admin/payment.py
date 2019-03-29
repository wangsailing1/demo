#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import datetime

import settings
from admin import render, auth
from admin.decorators import require_permission, ApprovalPayment
from lib.core.environ import ModelManager
from logics.payment import virtual_pay_by_admin
from models.payment import Payment
from gconfig import game_config
import decimal

CURRENCY_CNY = 'CNY'  # 人民币
CURRENCY_USD = 'USD'  # 美元
CURRENCY_HKD = 'HKD'  # 港币
CURRENCY_EUR = 'EUR'  # 欧元
CURRENCY_GBP = 'GBP'  # 英镑
CURRENCY_JPY = 'JPY'  # 日元
CURRENCY_VND = 'VND'  # 越南盾
CURRENCY_KRW = 'KRW'  # 韩元
CURRENCY_AUD = 'AUD'  # 澳元
CURRENCY_CAD = 'CAD'  # 加元
CURRENCY_BUK = 'BUK'  # 缅甸元
CURRENCY_THB = 'THB'  # 泰铢
CURRENCY_TWD = 'TWD'  # 新台币
CURRENCY_SGD = 'SGD'  # 新加坡元
CURRENCY_YB = 'YB'  # Y币

# 币种对rmb
currencys = {
    CURRENCY_CNY: 1,  # 人民币
    CURRENCY_USD: 6.4768,  # 美元
    CURRENCY_HKD: 0.8357,  # 港币
    CURRENCY_EUR: 7.107,  # 欧元
    CURRENCY_GBP: 9.664,  # 英镑
    CURRENCY_JPY: 0.0538,  # 日元
    CURRENCY_VND: 0.0003,  # 越南盾
    CURRENCY_KRW: 179.7307,  # 韩元
    CURRENCY_AUD: 4.7099,  # 澳元
    CURRENCY_CAD: 4.6815,  # 加元
    CURRENCY_BUK: 0.005,  # 缅甸元
    CURRENCY_THB: 0.1795,  # 泰铢
    CURRENCY_TWD: 0.1979,  # 新台币
    CURRENCY_SGD: 4.6071,  # 新加坡元
    CURRENCY_YB: 1,  # Y币
}


@require_permission
def select_virtual(req, **kwargs):
    """ 虚拟充值首页

    :param req:
    :return:
    """
    data = {'msg': '', 'mm': None}
    if req.request.method == 'POST':
        uid = req.get_argument('user_id', '')
        mm = ModelManager(uid)
        if mm.user.inited:
            data['msg'] = u'not user'
            return render(req, 'admin/payment/virtual_index.html', **data)
        else:
            data['mm'] = mm
            return render(req, 'admin/payment/virtual_pay.html', **data)

    return render(req, 'admin/payment/virtual_index.html', **data)


@require_permission
def virtual_pay(req):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('user_id')
    goods_id = req.get_argument('goods_id')
    reason = req.get_argument('reason')
    times = int(req.get_argument('times', 1))
    act_id = int(req.get_argument('act_id', 0))
    act_item_id = int(req.get_argument('act_item_id', 0))

    if 'admin' in req.request.arguments:
        tp = 'admin'  # 后台代充  算真实收入
    elif 'admin_test' in req.request.arguments:
        tp = 'admin_test'  # 管理员测试用 不算真实收入
    else:
        tp = ''

    data = {'msg': '', 'user': None}
    mm = ModelManager(uid, async_save=True)
    if mm.user.inited:
        data['msg'] = u'not user'
        return render(req, 'admin/payment/virtual_index.html', **data)
    if not reason:
        data['msg'] = u'payment reason'
        return render(req, 'admin/payment/virtual_index.html', **data)

    approval_payment = ApprovalPayment()
    key = approval_payment.add_payment(req.uname, uid, goods_id, reason, times, tp, act_id, act_item_id)

    admin = auth.get_admin_by_request(req)
    if settings.DEBUG:  # or (admin and 'for_approval' in admin.right_links):
        approval_payment.approval_payment(req.uname, key, refuse=False)
        data['msg'] = u"充值成功"
    else:
        data['msg'] = u"已经提交审批"
    # for i in xrange(times):
    #     virtual_pay_by_admin(mm, goods_id, admin, reason, tp)

    # data['msg'] = u"success"

    data['mm'] = mm
    return render(req, 'admin/payment/virtual_pay.html', **data)


@require_permission
def select_pay(req, **kwargs):
    """ 充值查询

    :param req:
    :return:
    """
    start_day = req.get_argument('start_day', None)
    end_day = req.get_argument('end_day', None)

    now = datetime.datetime.now()

    day_interval = [(now - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in xrange(0, 40)]

    if not start_day:
        start_day = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

    if not end_day:
        end_day = now.strftime('%Y-%m-%d')

    data = {}

    s_day = '%s 00:00:00' % start_day
    e_day = '%s 23:59:59' % end_day

    payment = Payment()

    for item in payment.find_by_time(s_day, e_day):
        key = item['order_time'][:10]
        data.setdefault(key, []).append(item)

    st_list_0 = []
    charge_config = game_config.charge
    all_data = dict(all_pay_times=0, all_person_times=0,
                    all_pay_diamonds=0, all_pay_rmbs=0, all_pay_usd=0,
                    all_google_rmbs=0, all_apple_rmbs=0, all_mycard_rmbs=0,
                    all_google_usd=0, all_apple_usd=0, all_mycard_usd=0,
                    all_admin_pay_rmbs=0, all_platform_pay_rmbs=0,
                    )
    for day, item_list in data.iteritems():
        user_ids, pay_diamonds, pay_rmbs, admin_pay_rmbs, really_pay_rmbs, pay_usd = set(), 0, 0, 0, 0, 0
        really_google_rmbs_EN, really_google_rmbs_CN, really_google_rmbs_TW = 0, 0, 0
        really_apple_rmbs_EN, really_apple_rmbs_CN, really_apple_rmbs_TW = 0, 0, 0
        really_mycard_rmbs_EN, really_mycard_rmbs_CN, really_mycard_rmbs_TW = 0, 0, 0
        all_google_rmbs, all_apple_rmbs, all_mycard_rmbs = 0, 0, 0

        for item in item_list:
            user_ids.add(item['user_id'])
            really_google_rmbs_EN += charge_config.get(item['product_id'], {}).get('price_TW', 0) if str(
                item.get('platform', '')) == 'google-kvgames' and item.get('currency') in ['USD', 'TWD'] else 0
            if str(item.get('platform', '')) == 'google-kvgames' and item.get('currency') in ['USD', 'TWD']:
                item['currency'] = 'USD'
                item['order_money'] = charge_config.get(item['product_id'], {}).get('price_TW', 0)
                item['order_rmb'] = round(currencys.get(CURRENCY_USD, 1) * item['order_money'], 2)
            pay_diamonds += item['order_diamond']
            if 'admin_test' in item['platform']:
                admin_pay_rmbs += charge_config.get(item['product_id'], {}).get('price_TW', 0)
            else:
                pay_rmbs += float(item['order_rmb'] or 0)
                # pay_usd += round(float(item['order_rmb'] or 0) / currencys.get(CURRENCY_USD, 1), 2)
                pay_usd += charge_config.get(item['product_id'], {}).get('price_TW', 0)

                really_pay_rmbs = pay_usd
            all_google_rmbs += item['order_rmb'] if str(item.get('platform', '')) == 'google-kvgames' else 0
            really_google_rmbs_CN += item['order_money'] if str(
                item.get('platform', '')) == 'google-kvgames' and item.get('currency') == 'CNY' else 0
            really_google_rmbs_TW += 0

            all_apple_rmbs += item['order_rmb'] if str(item.get('platform', '')) == 'apple' else 0
            really_apple_rmbs_EN += item['order_money'] if str(item.get('platform', '')) == 'apple' and item.get(
                'currency') == 'USD' else 0
            none_currency_rmbs = item['order_rmb'] if str(item.get('platform', '')) == 'apple' and not item.get(
                'currency') else 0
            really_apple_rmbs_EN += none_currency_rmbs / decimal.Decimal(currencys.get(CURRENCY_USD, 1))
            really_apple_rmbs_CN += item['order_money'] if str(item.get('platform', '')) == 'apple' and item.get(
                'currency') == 'CNY' else 0
            really_apple_rmbs_TW += item['order_money'] if str(item.get('platform', '')) == 'apple' and item.get(
                'currency') == 'TWD' else 0

            all_mycard_rmbs += item['order_rmb'] if str(item.get('platform', '')) == 'MyCard' else 0
            really_mycard_rmbs_EN += item['order_money'] if str(item.get('platform', '')) == 'MyCard' and item.get(
                'currency') == 'USD' else 0
            really_mycard_rmbs_CN += item['order_money'] if str(item.get('platform', '')) == 'MyCard' and item.get(
                'currency') == 'CNY' else 0
            really_mycard_rmbs_TW += item['order_money'] if str(item.get('platform', '')) == 'MyCard' and item.get(
                'currency') == 'TWD' else 0

        all_data['all_pay_times'] += len(item_list)
        all_data['all_person_times'] += len(user_ids)
        all_data['all_pay_diamonds'] += pay_diamonds
        all_data['all_pay_rmbs'] += pay_rmbs
        all_data['all_admin_pay_rmbs'] += admin_pay_rmbs
        all_data['all_platform_pay_rmbs'] += really_pay_rmbs
        all_data['all_pay_usd'] += pay_usd

        all_data['all_google_rmbs'] += all_google_rmbs
        all_data['all_apple_rmbs'] += all_apple_rmbs
        all_data['all_mycard_rmbs'] += all_mycard_rmbs

        all_data['all_google_usd'] += really_google_rmbs_EN + really_google_rmbs_CN + really_google_rmbs_TW
        all_data['all_apple_usd'] += really_apple_rmbs_EN + really_apple_rmbs_CN + really_apple_rmbs_TW
        all_data['all_mycard_usd'] += really_mycard_rmbs_EN + really_mycard_rmbs_CN + really_mycard_rmbs_TW

        st_list_0.append({'day': day,
                          'pay_diamonds': pay_diamonds,
                          'pay_times': len(item_list),
                          'pay_rmbs': pay_rmbs,
                          'pay_usd': pay_usd,
                          'admin_pay_rmbs': admin_pay_rmbs,
                          'really_pay_rmbs': really_pay_rmbs,
                          'person_times': len(user_ids),
                          'all_google_rmbs': really_google_rmbs_EN,
                          'really_google_rmbs_EN': really_google_rmbs_EN,
                          'really_google_rmbs_CN': really_google_rmbs_CN,
                          'really_google_rmbs_TW': really_google_rmbs_TW,
                          'all_apple_rmbs': really_google_rmbs_EN,
                          'really_apple_rmbs_EN': round(really_apple_rmbs_EN, 2),
                          'really_apple_rmbs_CN': really_apple_rmbs_CN,
                          'really_apple_rmbs_TW': really_apple_rmbs_TW,
                          'all_mycard_rmbs': really_google_rmbs_EN,
                          'really_mycard_rmbs_EN': really_mycard_rmbs_EN,
                          'really_mycard_rmbs_CN': really_mycard_rmbs_CN,
                          'really_mycard_rmbs_TW': really_mycard_rmbs_TW,
                          })

    st_list_0.sort(key=lambda x: x['day'], reverse=True)

    return render(req, 'admin/payment/index.html', **{
        'st_list_0': st_list_0,
        'start_day': start_day,
        'end_day': end_day,
        'day_interval': day_interval,
        'environment': settings.ENV_NAME,
        'all_data': all_data,
    })


@require_permission
def pay_day(req):
    """

    :param req:
    :return:
    """
    day_dt = req.get_argument('day', None)

    add_diamond = rmb = 0
    usd = 0
    s_day = '%s 00:00:00' % day_dt
    e_day = '%s 23:59:59' % day_dt

    payment = Payment()

    st_list_0 = sorted(payment.find_by_time(s_day, e_day), key=lambda x: x['order_time'], reverse=True)
    charge_config = game_config.charge
    mm = ModelManager('')
    for x in st_list_0:
        x['pay'] = x['order_money']
        x['rmb'] = float(x['order_rmb'] or 0)
        add_diamond += x['order_diamond']
        x['name'] = mm.get_mm(x['user_id']).user.name
        x['usd'] = round(x['rmb'] / currencys.get(CURRENCY_USD, 1), 2)
        if str(x.get('platform', '')) == 'google-kvgames' and x.get('currency') in ['USD', 'TWD']:
            x['currency'] = 'USD'
            x['usd'] = charge_config.get(x['product_id'], {}).get('price_TW', 0)
            x['rmb'] = round(currencys.get(CURRENCY_USD, 1) * x['usd'], 2)
        usd += x['usd']
        rmb += x['rmb']

    return render(req, 'admin/payment/pay_day.html', **{
        'start_day': day_dt,
        'end_day': day_dt,
        'st_list_0': st_list_0,
        'add_diamond': add_diamond,
        'rmb': rmb,
        'usd': usd,
        'environment': settings.ENV_NAME,
    })


@require_permission
def pay_person(req):
    user_id = req.get_argument('user_id')

    payment = Payment()
    st_list_0 = sorted(payment.find_by_uid(user_id), key=lambda x: x['order_time'], reverse=True)

    add_diamond, pay, admin_pay, really_pay = 0, 0, 0, 0

    mm = ModelManager('')
    for x in st_list_0:
        x['pay'] = x['order_money']
        pay += x['pay']
        add_diamond += x['order_diamond']
        x['name'] = mm.get_mm(x['user_id']).user.name

        if 'admin_test' in x['platform']:
            admin_pay += x['order_money']
        else:
            really_pay += x['order_money']

    return render(req, 'admin/payment/pay_person.html', **{
        'admin_pay': admin_pay,
        'really_pay': really_pay,
        'st_list_0': st_list_0,
        'add_diamond': add_diamond,
        'pay': pay,
        'environment': settings.ENV_NAME,
        'user_id': user_id,
    })
