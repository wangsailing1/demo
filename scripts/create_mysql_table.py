#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 批量导入配置

import os
import sys
import MySQLdb

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings


def init_env(env):
    settings.set_env(env)


PAYMENT_FORMAT = """
CREATE TABLE if not exists %(table)s (
        order_id varchar(255) NOT NULL,
        level smallint,
        old_diamond mediumint,
        gift_diamond mediumint,
        order_diamond mediumint,
        order_money decimal(10, 2),
        order_rmb decimal(10, 2),
        double_pay tinyint,
        currency varchar(32),
        order_time varchar(255),
        platform varchar(32),
        product_id mediumint,
        scheme_id varchar(255),
        raw_data blob,
        user_id varchar(32),
        uin varchar(32),
        admin varchar(32),
        lan_sort varchar(20),
        real_product_id int(12),
        reason blob,
        PRIMARY KEY(order_id),
        index(order_id),
        index(order_time),
        index(user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


SPEND_FORMAT = """
CREATE TABLE if not exists %(table)s (
        spend_id int(50) NOT NULL auto_increment,
        user_id varchar(32),
        level int(4),
        subtime varchar(32),
        diamond_num int(10),
        diamond_1st int(10),
        diamond_2nd int(10),
        goods_type varchar(50),
        args varchar(500),
        PRIMARY KEY(spend_id),
        index(subtime),
        index(spend_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


EARN_FORMAT = """
CREATE TABLE if not exists %(table)s (
        earn_id int(50) NOT NULL auto_increment,
        user_id varchar(32),
        level int(4),
        subtime varchar(32),
        diamond_num int(10),
        diamond_1st int(10),
        diamond_2nd int(10),
        goods_type varchar(50),
        args varchar(500),
        PRIMARY KEY(earn_id),
        index(subtime),
        index(earn_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


QUEST_FORMAT = """
CREATE TABLE if not exists %(table)s (
        quest_id int(50) NOT NULL auto_increment,
        quest_time varchar(255),
        s1 varchar(4),
        s2 varchar(4),
        s3 varchar(4),
        s4 varchar(4),
        s5 varchar(4),
        s6 blob,
        s7 varchar(4),
        s8 varchar(4),
        s9 varchar(4),
        s10 varchar(4),
        s11 varchar(4),
        s12 varchar(4),
        s13 varchar(4),
        s14 blob,
        s15 blob,
        s16 varchar(4),
        s17 varchar(4),
        s18 varchar(4),
        s19 blob,
        s20 varchar(4),
        s21 varchar(4),
        s22 blob,
        s23 blob,
        s24 varchar(32),
        PRIMARY KEY(quest_id),
        index(quest_id),
        index(quest_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


GS_FORMAT = """
CREATE TABLE if not exists %(table)s (
        ID int(32) NOT NULL auto_increment,
        user_id varchar(32) DEFAULT NULL,
        vip_level int(32) DEFAULT '0',
        platform varchar(32) DEFAULT '0',
        msg_type int(12) DEFAULT '0',
        msg varchar(255) DEFAULT NULL,
        status int(12) DEFAULT '0',
        gs_name varchar(32) DEFAULT NULL,
        reply_title varchar(50) NOT NULL DEFAULT '',
        last_update_date int(32) DEFAULT NULL,
        ask_time varchar(32) NOT NULL DEFAULT '',
        reply_content varchar(255) NOT NULL DEFAULT '',
        reply_time varchar(32) NOT NULL DEFAULT '',
        solve_status int(10) NOT NULL DEFAULT '0',
        solve_time varchar(32) NOT NULL DEFAULT '',
        index(ID)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


def check_payment_database(payment_config):
    conn = MySQLdb.connect(host=payment_config['host'], user=payment_config['user'],
                        passwd=payment_config['passwd'], charset='utf8')
    cursor = conn.cursor()
    sql = 'create database if not exists %s;' % payment_config['db']
    cursor.execute(sql)
    conn.commit()


def create_payment():
    from models.payment import Payment
    payment_config = settings.PAYMENT_CONFIG

    check_payment_database(payment_config)

    p = Payment()
    for table in p.tables():
        sql = PAYMENT_FORMAT % {'table': table}
        p.cursor.execute(sql)
        p.conn.commit()


def check_spend_database(spend_config):
    conn = MySQLdb.connect(host=spend_config['host'], user=spend_config['user'],
                        passwd=spend_config['passwd'], charset='utf8')
    cursor = conn.cursor()
    sql = 'create database if not exists %s;' % spend_config['db']
    cursor.execute(sql)
    conn.commit()


def create_spend():
    from models.spend import Spend
    spend_config = settings.SPEND_CONFIG

    check_spend_database(spend_config)

    s = Spend()
    for table in s.tables():
        sql = SPEND_FORMAT % {'table': table}
        s.cursor.execute(sql)
        s.conn.commit()


def check_earn_database(earn_config):
    conn = MySQLdb.connect(host=earn_config['host'], user=earn_config['user'],
                        passwd=earn_config['passwd'], charset='utf8')
    cursor = conn.cursor()
    sql = 'create database if not exists %s;' % earn_config['db']
    cursor.execute(sql)
    conn.commit()


def create_earn():
    from models.earn import Earn
    earn_config = settings.EARN_CONFIG

    check_earn_database(earn_config)

    e = Earn()
    for table in e.tables():
        sql = EARN_FORMAT % {'table': table}
        e.cursor.execute(sql)
        e.conn.commit()


def check_quest_database(quest_config):
    conn = MySQLdb.connect(host=quest_config['host'], user=quest_config['user'],
                        passwd=quest_config['passwd'], charset='utf8')
    cursor = conn.cursor()
    sql = 'create database if not exists %s;' % quest_config['db']
    cursor.execute(sql)
    conn.commit()


def create_quest():
    from models.questionnaire import Questionnaire
    quest_config = settings.QUEST_CONFIG

    check_quest_database(quest_config)

    p = Questionnaire()
    for table in p.tables():
        sql = QUEST_FORMAT % {'table': table}
        p.cursor.execute(sql)
        p.conn.commit()


def create_client_service():
    from models.user import GSMessage
    quest_config = settings.GS_HOST

    check_quest_database(quest_config)

    p = GSMessage()
    for table in p.tables():
        sql = GS_FORMAT % {'table': table}
        p.cursor.execute(sql)
        p.conn.commit()


if __name__ == '__main__':
    env = sys.argv[1]
    init_env(env)
    create_payment()
    create_spend()
    create_earn()
    create_quest()
    create_client_service()
