#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'


import sys
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

CURRENCY_USD = 6.4768


def update_charge_data():
    """
    google旧充值数据问题,币种TWD改为USD,order_rmb按汇率由order_money转换
    :return:
    """
    payment = Payment()

    for table in payment.tables():
        sql = 'update %s set currency="USD", order_rmb=order_money*6.4768 where platform="google-kvgames" and currency="TWD"' % table
        payment.cursor.execute(sql)

    payment.conn.commit()


def update_first_charge_data():
    """
    由于google充值记录问题，导致首充人民币计算有问题,按人民币刷新首充数据
    :return:
    """
    payment = Payment()
    payment_data = payment.find('platform="google-kvgames"')

    user_data = {}  # {uid: rmb}
    for i in payment_data:
        user_id = i['user_id']
        order_money = float(i['order_money'])
        order_rmb = order_money*CURRENCY_USD
        if user_id not in user_data:
            user_data[user_id] = order_rmb
        else:
            user_data[user_id] += order_rmb
        user_data[user_id] = round(user_data[user_id], 2)

    for uid, rmb in user_data.iteritems():
        mm = ModelManager(uid)
        mm.user_payment.charge_price = 0
        mm.user_payment.add_first_charge(rmb)

    return user_data


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'argv error, python first_charge_bug env func_name'
        exit(0)

    env = sys.argv[1]
    import settings
    settings.set_env(env, 'app')

    from models.payment import Payment
    from lib.core.environ import ModelManager

    func_name = sys.argv[2]
    print globals()[func_name]()
