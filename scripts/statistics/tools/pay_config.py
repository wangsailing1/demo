#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import os
import sys

# 设置程序使用的编码格式, 统一为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir, os.path.pardir, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

if len(sys.argv) == 2:
    env = sys.argv[1]

    import settings
    settings.set_env(env)

    print 'mysql_host=%s; mysql_passwd=%s; mysql_db=%s; ' \
          'mysql_user=%s; mysql_tprefix=%s' % (settings.PAYMENT_CONFIG['host'], settings.PAYMENT_CONFIG['passwd'],
                                               settings.PAYMENT_CONFIG['db'], settings.PAYMENT_CONFIG['user'],
                                               settings.PAYMENT_CONFIG['table_prefix'])
else:
    print 'mysql_host=; mysql_passwd=; mysql_db=; mysql_user=; mysql_tprefix='
