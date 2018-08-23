#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'

import time

import settings

import MySQLdb
from lib.utils import md5
from lib.utils.timelib import now_time_to_str
from lib.utils.debug import print_log


class Questionnaire(object):
    """ 问卷调查

    """
    TABLE_COUNT = 1

    def __init__(self):
        self.mysql_config = settings.QUEST_CONFIG
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

    def execute_insert(self, quest_key, data, commit=True):
        """ 执行命令

        :param quest_key:
        :param data:
        :param commit:
        :return:
        """
        table = self.generate_table(quest_key)
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

    def insert_quest(self, data, commit=True):
        """ 插入调查记录

        :param data: {
            's1': '',
            ...
        }
        :return:
        """
        data['quest_time'] = now_time_to_str()
        quest_key = '%s' % int(time.time())
        self.execute_insert(quest_key, data, commit=commit)
        return True

    def find_by_time(self, start_dt, end_dt):
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        for table in self.tables():
            sql = self.select_generate(table, ['quest_time>="%s"' % start_dt, 'quest_time<="%s"' % end_dt])
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

