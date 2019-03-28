# coding: utf-8
from gevent import monkey
monkey.patch_all()

import os
os.environ["C_FORCE_ROOT"] = '1'

from optparse import OptionParser


parser = OptionParser()
parser.add_option("--env", dest="env", action="store", default="dev", help="env config")
parser.add_option("--server_name", dest="server", action="store", default="master", help="server_name")
parser.add_option("-B", "--beat", dest="beat", action="store_true", default=False, help="celery beat")
parser.add_option("-C", "--concurrency", dest="concurrency_num", action="store", default=1, help="celery worker concurrency")
parser.add_option("-P", "--pool", dest="pool", action="store", default='gevent', help="")

# parser.add_option("-Q", "--queue", dest="queue", action="store", default='default', help="celery worker queue")
parser.add_option("--cw_num", dest="cw_num", action="store", default='10', help="cw_num")
parser.add_option("--all_cw", dest="all_cw", action="store", default='1', help="all_cw")

(options, args) = parser.parse_args()


import settings
env = options.env
server = options.server
pool = options.pool
all_cw = int(options.all_cw)
cw_num = int(options.cw_num)

settings.set_env(env, server, cw_num)

from celery_app import app
from celery_app.celeryconfig import change_concurrency


if __name__ == "__main__":
    worker_args = ['worker', '--loglevel=info', '-P={}'.format(pool),  '-n worker{}@%h'.format(cw_num)]

    # celery_queues = ['celery']
    # worker_args.append("-Q")
    # worker_args.append(','.join(celery_queues))
    change_concurrency(options.concurrency_num)

    # print worker_args
    app.worker_main(worker_args)
