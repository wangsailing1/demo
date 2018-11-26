#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import json
import time

import settings

import MySQLdb
from lib.utils import md5
from lib.core.environ import ModelManager, EventBase
from lib.utils.timelib import now_time_to_str


class Earn(object):
    """ 获得钻石模块

    """
    TABLE_COUNT = 16

    def __init__(self):
        self.mysql_config = settings.EARN_CONFIG
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

    def generate_table(self, earn_id):
        """ 生产table

        :param earn_id:
        :return:
        """
        sid = int(md5(str(earn_id)), 16)
        table = '%s_%s' % (self.table_prefix, sid % self.TABLE_COUNT)
        return table

    def execute_insert(self, earn_id, data, commit=True):
        """ 执行命令

        :param earn_id:
        :param data:
        :return:
        """
        table = self.generate_table(earn_id)
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

    def exists_earn_id(self, earn_id):
        table = self.generate_table(earn_id)
        sql = self.select_generate(table, ['earn_id="%s"' % earn_id], ['earn_id'])
        return self.cursor.execute(sql)

    def insert_earn(self, data, commit=True):
        """ 插入充值记录

        :param data: {
            'earn_id': 0,  # 自增长
            'diamond_1st': old_diamond,
            'diamond_2nd': new_diamond,
            'diamond_num': old_diamond - new_diamond,
            'goods_type': method_param,
            'level': user.level,
            'subtime': time.strftime('%F %T'),
            'user_id': user.uid,
            'args': json.dumps(arguments, separators=(',', ':')),
        }
        :return:
        """
        earn_id = '%s_%s' % (data['user_id'], int(time.time()))
        self.execute_insert(earn_id, data, commit=commit)
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


class EarnEvent(EventBase):
    """ 消费处理event

    """
    def __init__(self, *args, **kwargs):
        """ 初始化

        :param args:
        :param kwargs:
        :return:
        """
        super(EarnEvent, self).__init__()
        self._event = []

    def record(self, cost):
        """ 记录

        :param cost:
        :return:
        """
        data = {
            'old_diamond': self.mm.user.diamond - cost,
            'diamond_num': cost,
            'goods_type': self.mm.action,
            'subtime': now_time_to_str(),
        }
        self._event.append(data)

        if not self.async_save:
            self.handler()

    def handler(self):
        """ 处理函数

        :param cost:
        :return:
        """
        # earn = Earn()
        is_save =  False
        for data in self._event:
            self.mm.user.coin_log.append(data)
            is_save = True
            # earn.insert_earn(data)

            # 处理其他的活动逻辑
            pass

        if is_save:
            self.mm.user.coin_log = self.mm.user.coin_log[-100:]
            # coin_log改成记录在user上,就不需要单独再save了,
            # 直接跟着业务里的user.add_diamond入库
            # self.mm.user.save()


ModelManager.register_events('earn_event', EarnEvent)
