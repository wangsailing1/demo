# encoding:utf-8

import os
import sys
import datetime
import json

# 设置程序使用的编码格式, 统一为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

env = sys.argv[1]

if len(sys.argv) == 3:
    arg_date = sys.argv[2]
else:
    arg_date = ''

import settings
settings.set_env(env)

from scripts.statistics.tools import act_user
from lib.utils.loggings import get_log, InfoLoggingUtil
from lib.core.environ import ModelManager


default_path = '../statistic/%s/redis_static/' % settings.ENV_NAME
log_path = '/data/bi_data/%s/redis_static/' % settings.ENV_NAME
real_path = log_path if log_path else default_path


def main():
    if arg_date:
        today = datetime.datetime.strptime(arg_date, '%Y%m%d') + datetime.timedelta(days=1)
    else:
        today = datetime.datetime.today()

    create_date = today - datetime.timedelta(days=1)
    date_stamp = create_date.strftime('%Y%m%d')
    file_name = 'act_%s' % date_stamp

    act_uids = act_user.get_act_all_user(today=today, withscores=True)

    for data in act_uids:
        x_uid = data[0]
        x_act_time = int(data[1])
        x_date = datetime.datetime.fromtimestamp(x_act_time).strftime('%Y-%m-%d')
        x_time = datetime.datetime.fromtimestamp(x_act_time).strftime('%H:%M:%S')

        try:
            mm = ModelManager(x_uid)
            plat = mm.user.channel
            if not plat:
                plat = "NULL"
        except:
            plat = 'error'

        data = {
            'uid': x_uid,
            'date': x_date,
            'time': x_time,
            'plat': plat,
        }

        log = get_log('%s/%s' % (real_path, file_name),
                      logging_class=InfoLoggingUtil, propagate=0)
        log.info(json.dumps(data, separators=[',', ':']))
        # log.info('{uid}\t{date}\t{time}\t{plat}'.format(**data))


if __name__ == "__main__":
    main()
