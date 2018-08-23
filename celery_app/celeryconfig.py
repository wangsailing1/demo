#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from datetime import timedelta
from celery.schedules import crontab
import os
import sys
import time

import settings

# Broker and Backend
# redis://[:password]@localhost:6379/0
# BROKER_URL = 'redis://:xAP5nIyANfLKlDBP@192.168.1.51:6400/40'
# CELERY_RESULT_BACKEND = 'redis://:xAP5nIyANfLKlDBP@192.168.1.51:6400/49'

redis_config = settings.celery_config
BROKER_URL = 'redis://:%s@%s:%s/%d' % (
    redis_config.get('password', ''), redis_config.get('host', ''),
    redis_config.get('port', 6300), redis_config.get('db', 0)
)
CELERY_RESULT_PERSISTENT = False
CELERY_RESULT_BACKEND = 'rpc://'

CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

# Timezone
CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'celery_app.task1',
    'celery_app.task2',
    'celery_app.test_battle',
)

CELERYD_CONCURRENCY = 1
def change_concurrency(num):
    """ celery worker 并发数
    """
    globals()['CELERYD_CONCURRENCY'] = num

schdule_logs_path = os.path.join(settings.BASE_ROOT, 'logs/cw_logs')
if not os.path.exists(schdule_logs_path):
    os.makedirs(schdule_logs_path)
CELERYD_LOG_FILE = os.path.join(schdule_logs_path, 'cw_%s_%s' % (str(settings.CW_NUM), time.strftime("%Y%m%d")))
CELERY_DEFAULT_QUEUE = 'celery'


# schedules
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=1),       # 每 30 秒执行一次
#          'args': (0, 1)                           # 任务函数参数
#     },
#     'add-every-30-seconds1': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=1),       # 每 30 秒执行一次
#          'args': (0, 2)                           # 任务函数参数
#     },
#     'add-every-30-seconds2': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=1),       # 每 30 秒执行一次
#          'args': (0, 3)                           # 任务函数参数
#     },
#     'add-every-30-seconds3': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=1),       # 每 30 秒执行一次
#          'args': (0, 4)                           # 任务函数参数
#     },
#     'multiply-at-some-time': {
#         'task': 'celery_app.task2.multiply',
#         'schedule': timedelta(seconds=1),   # 每天早上 9 点 50 分执行一次
#         'args': (1, 5)                            # 任务函数参数
#     }
# }
