# coding: utf-8

import os
os.environ["C_FORCE_ROOT"] = '1'

from optparse import OptionParser


parser = OptionParser()
parser.add_option("--env", dest="env", action="store", default="dev", help="env config")
parser.add_option("--server_name", dest="server", action="store", default="master", help="server_name")
parser.add_option("-B", "--beat", dest="beat", action="store_true", default=False, help="celery beat")
parser.add_option("-C", "--concurrency", dest="concurrency_num", action="store", default=1, help="celery worker concurrency")
# parser.add_option("-Q", "--queue", dest="queue", action="store", default='default', help="celery worker queue")
parser.add_option("--cw_num", dest="cw_num", action="store", default='1', help="cw_num")
parser.add_option("--all_cw", dest="all_cw", action="store", default='1', help="all_cw")

(options, args) = parser.parse_args()


import settings
env = options.env
server = options.server
all_cw = int(options.all_cw)
cw_num = int(options.cw_num)

settings.set_env(env, server, cw_num)
from celery_app import which_queue


if __name__ == "__main__":
    worker_args = ['worker', '--loglevel=info', '-n worker{}@%h'.format(cw_num)]
    servers = []
    # servers = [x for x in settings.SERVERS if x != 'master']
    for s in settings.SERVERS.keys():
        if s in ['master', 'public']:
            continue
        if not settings.is_father_server(s):
            continue
        # open_new_war = settings.COUNTRY_WAR_HOST.get(s)
        # if open_new_war:
        #     continue
        servers.append(s)
    servers.sort(key=lambda x:int(x[1:]) if x[1:].isdigit() else x)

    celery_queues = []
    # servers_filter = []
    polling_idx = cw_num % all_cw
    for idx, server in enumerate(servers):
        if idx % all_cw == polling_idx:
            celery_queues.append(which_queue(server))
            # servers_filter.append(server)
    # if options.beat:
    #     worker_args.append("-B")

    worker_args.append("-Q")
    worker_args.append(','.join(celery_queues))

    from celery_app import app
    from celery_app.celeryconfig import change_concurrency
    change_concurrency(options.concurrency_num)

    # from apps.country_war_1.tasks import start_beat
    # start_beat(servers_filter)

    app.worker_main(worker_args)
