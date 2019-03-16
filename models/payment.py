#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import settings

import MySQLdb
from lib.utils import md5

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
    CURRENCY_CNY: 1,         # 人民币
    CURRENCY_USD: 6.4768,    # 美元
    CURRENCY_HKD: 0.8357,    # 港币
    CURRENCY_EUR: 7.107,     # 欧元
    CURRENCY_GBP: 9.664,     # 英镑
    CURRENCY_JPY: 0.0538,    # 日元
    CURRENCY_VND: 0.0003,    # 越南盾
    CURRENCY_KRW: 179.7307,  # 韩元
    CURRENCY_AUD: 4.7099,    # 澳元
    CURRENCY_CAD: 4.6815,    # 加元
    CURRENCY_BUK: 0.005,     # 缅甸元
    CURRENCY_THB: 0.1795,    # 泰铢
    CURRENCY_TWD: 0.1979,    # 新台币
    CURRENCY_SGD: 4.6071,    # 新加坡元
    CURRENCY_YB: 1,          # Y币
}


COIN_RATE = {
    'CN': 1.0 / 8,
    'EN': 1.0 / 8,
    'TW': 1.0 / 8,
    'TH': 4.4,
    'ID': 1923.0,
    'VN': 3280.0,
}

# 货币与国家映射
CURRENCY_COUNTRY = {
    'CNY': 'CN',
    'TWD': 'TWD',
    'USD': 'EN',
    'KRW': 'KR',
    'THB': 'TH',
    'VND': 'VN',
    'IDR': 'ID',
    'MYR': 'MYR',
    'SGD': 'SGD',
    'AUD': 'AUD',
    'PHP': 'PHP',
    'BRL': 'BRL',
    'NZD': 'NZN',
    'INR': 'INR',
    'MMK': 'MMK',
}


# 每种货币兑换元宝/vip经验数
CURRENCY_VIP_EXP = {
    'THB': 2.5,
    'TWD': 2.5,
    'USD': 65,
    'VND': 0.003,
    'IDR': 0.0045,
    'KRW': 0.055,
    'CNY': 10,
    'MYR': 16,
    'SGD': 50,
    'AUD': 50,
    'PHP': 1.5,
    'BRL': 20,
    'NZD': 50,
    'INR': 1,
    'MMK': 0.05,
}


class Payment(object):
    """ 充值模块

    """
    TABLE_COUNT = 16

    def __init__(self):
        self.mysql_config = settings.PAYMENT_CONFIG
        self.table_prefix = self.mysql_config['table_prefix']
        self.conn = MySQLdb.connect(
            host=self.mysql_config['host'],
            user=self.mysql_config['user'],
            passwd=self.mysql_config['passwd'],
            db=self.mysql_config['db'],
            charset="utf8"
        )
        self.cursor = self.conn.cursor()

    def __enter__(self,):
        return self

    def __del__(self,):
        self.conn.close()
        self.cursor.close()

    def generate_table(self, order_id):
        """ 生产table

        :param order_id:
        :return:
        """
        sid = int(md5(str(order_id)), 16)
        table = '%s_%s' % (self.table_prefix, sid % self.TABLE_COUNT)
        return table

    def execute_insert(self, order_id, data, commit=True):
        """ 执行命令

        :param order_id:
        :param data:
        :return:
        """
        table = self.generate_table(order_id)
        sql = self.insert_generate(table, data)
        self.cursor.execute(sql)
        if commit:
            self.conn.commit()

    def commit_transaction(self):
        """ 提交事务

        :return:
        """
        self.conn.commit()

    def select_generate(self, table, where, result=None):
        """ 查询生成器

        :param table: str: 字符串
        :param where: where [str, str, str]
        :param result: [str, str]
        :return:
        """
        if result is None:
            result = ["*"]
        return 'select %s from %s where %s;' % (','.join(result), table, ' and '.join(where))

    def insert_generate(self, table, update):
        """ 插入生成器

        :param table:
        :param update:
        :return:
        """
        update = ','.join('%s=%s' % (key, self.conn.literal(item)) for key, item in update.iteritems())
        return 'insert into %(table)s set %(update)s' % {'table': table, 'update': update}

    def exists_order_id(self, order_id):
        table = self.generate_table(order_id)
        sql = self.select_generate(table, ['order_id="%s"' % order_id], ['order_id'])
        return self.cursor.execute(sql)

    def insert_pay(self, data, commit=True):
        """ 插入充值记录

        :param data: {
            'order_id': '',         # 订单id
            'level': 0,             # 充值时的等级
            'old_diamond': 0,          # 充值时的钻石
            'gift_diamond': 0,         # 赠送的钻石
            'order_diamond': 0,        # 购买钻石
            'order_money': 0,       # 充值金额
            'currency': '',         # 金额币种
            'double_pay': 0,        # 是否双倍
            'order_time': '',       # 充值时间
            'platform': 0,          # 充值平台
            'product_id': 0,        # 配置id
            'scheme_id': 0,         # 平台配置id
            'raw_data': '',         # 平台充值数据
            'user_id': '',          # 用户uid
            'uin': '',              # 平台id
            'admin': '',            # admin账号
            'reason': 0,            # admin充值原因
        }
        :return:
        """
        order_id = data['order_id']
        if self.exists_order_id(order_id):
            return False
        self.execute_insert(order_id, data, commit=commit)
        return True

    def find_by_time(self, start_dt, end_dt):
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        for table in self.tables():
            sql = self.select_generate(table, ['order_time>="%s"' % start_dt, 'order_time<="%s"' % end_dt])
            count = cursor.execute(sql)
            while count > 0:
                count -= 1
                yield cursor.fetchone()

    def find_by_uid(self, user_id):
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        for table in self.tables():
            sql = self.select_generate(table, ['user_id="%s"' % user_id])
            count = cursor.execute(sql)
            while count > 0:
                count -= 1
                yield cursor.fetchone()

    def find(self, *args):
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        for table in self.tables():
            sql = self.select_generate(table, args)
            count = cursor.execute(sql)
            while count > 0:
                count -= 1
                yield cursor.fetchone()

    def tables(self):
        """ 返回所有表

        :return:
        """
        for table in ['%s_%s' % (self.table_prefix, x) for x in xrange(self.TABLE_COUNT)]:
            yield table
