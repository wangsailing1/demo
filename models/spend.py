#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'

import json
import time
import copy

import settings

import MySQLdb
from lib.utils import md5
from lib.core.environ import ModelManager, EventBase
from lib.utils.timelib import now_time_to_str


class Spend(object):
    """ 消费模块

    """
    TABLE_COUNT = 16

    def __init__(self):
        self.mysql_config = settings.SPEND_CONFIG
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

    def generate_table(self, spend_id):
        """ 生产table

        :param spend_id:
        :return:
        """
        sid = int(md5(str(spend_id)), 16)
        table = '%s_%s' % (self.table_prefix, sid % self.TABLE_COUNT)
        return table

    def execute_insert(self, spend_id, data, commit=True):
        """ 执行命令

        :param spend_id:
        :param data:
        :return:
        """
        table = self.generate_table(spend_id)
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

    def exists_spend_id(self, spend_id):
        table = self.generate_table(spend_id)
        sql = self.select_generate(table, ['spend_id="%s"' % spend_id], ['spend_id'])
        return self.cursor.execute(sql)

    def insert_spend(self, data, commit=True):
        """ 插入充值记录

        :param data: {
            'spend_id': 0,  # 自增长
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
        spend_id = '%s_%s' % (data['user_id'], int(time.time()))
        self.execute_insert(spend_id, data, commit=commit)
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


class SpendEvent(EventBase):
    """ 消费处理event

    """
    def __init__(self, *args, **kwargs):
        """ 初始化

        :param args:
        :param kwargs:
        :return:
        """
        super(SpendEvent, self).__init__()
        self._event = []

    def record(self, cost):
        """ 记录

        :param cost:
        :return:
        """
        args = copy.deepcopy(self.mm.args)
        for i in {"device_mk", "platform_channel", "device_mem", "user_token",
                  "version", "mk", "method", "device_mark", "cjyx2", '__ts', 'ks'}:
            args.pop(i, None)
        data = {
            'diamond_1st': self.mm.user.diamond + cost,
            'diamond_2nd': self.mm.user.diamond,
            'diamond_num': cost,
            'goods_type': self.mm.action,
            'level': self.mm.user.level,
            'subtime': now_time_to_str(),
            'user_id': self.mm.user.uid,
            'args': json.dumps(args, separators=(',', ':')),
        }
        self._event.append(data)

        if not self.async_save:
            self.handler()

    def handler(self):
        """ 处理函数

        :param cost:
        :return:
        """
        spend = Spend()
        for data in self._event:
            spend.insert_spend(data)

            # 处理其他的活动逻辑
            pass


ModelManager.register_events('spend_event', SpendEvent)