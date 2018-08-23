# coding: utf-8

import sys

# 设置程序使用的编码格式, 统一为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

import logging

import socket

from tornado.httpserver import HTTPServer
from tornado import ioloop
from tornado import web
from tornado.options import define, options
import tornado

define("port", default=8888, help="run on the given port", type=int)
define("env", default='dev', help="the env", type=str)
define("server_name", default='1', help="the server name", type=str)
define("numprocs", default=16, help="process sum", type=int)
define("debug", default=False, help="run at debug mode", type=bool)
define("maxmem", default=0, help="max memory use, overflow kill by self. (0 unlimit)", type=int)

options.parse_command_line()
import settings

settings.set_env(options.env, options.server_name)
settings.ENVPROCS = 'run'

from lib.utils.debug import print_log


import os
import gc
import time
import psutil
import signal
# import resource

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class Application(web.Application):
    def __init__(self, debug=False):
        handlers = [
            (r"/pay/", 'handlers.PayOrder'),
            (r"/pay-callback-([\w-]+)/?", 'handlers.PayCallback'),
            (r"/?[a-zA-Z0-9_]*/api/?", 'handlers.APIRequestHandler'),
            (r"/?[a-zA-Z0-9_]*/slg/?", 'handlers.SLGRequestHandler'),
            (r"/?[a-zA-Z0-9_]*/login/?", 'handlers.LoginHandler'),
            (r"/?[a-zA-Z0-9_]*/config/?", 'handlers.ConfigHandler'),
            (r"/admin/([\w-]+)/?", 'handlers.AdminHandler'),
            (r"/admin/([\w-]+)/([\w-]+)/?", 'handlers.AdminHandler'),
            (r"/%s/admin/([\w-]+)/([\w-]+)/?" % settings.URL_PARTITION, 'handlers.AdminHandler'),  # 供本地开发
            (r'/genesis2/weixin/([\w-]+)/', 'handlers.WeixinHandler'),  # 微信签到

            (r'/hero/([\w-]+)/', 'handlers.HeroHandler'),  # 英雄互娱sdk回调
            (r'/heroIM/([\w-]+)/', 'handlers.HeroIMHandler'),  # 英雄互娱IM接口
        ]

        app_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_prefix='/%s/static/' % settings.URL_PARTITION,
            debug=debug,
            # log_function=lambda x: 0,
        )

        super(Application, self).__init__(handlers, **app_settings)

import pdb


def db(sig, frame):
    """# db: docstring
    args:
        sig, frame:    ---    arg
    returns:
        0    ---
    """
    pdb.set_trace()

CHILDREN = {}


def shutdown():
    logging.warning('Stopping http server')
    server.stop()

    logging.warning('Will shutdown in %s seconds ...', 1)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 1

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()


def sig_hander_parent(sig, frame):
    print 'sig', sig
    for task_id, pid in CHILDREN.iteritems():
        kill_child(task_id)
    sys.exit()


def sig_hander_child(sig, frame):
    logging.warning('Caught signal: %s', sig)   # wait request end
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)
    #sys.exit()
    os._exit(0)


def kill_child(task_id):
    pid = CHILDREN[task_id]
    print_log(options.server_name, ':', task_id, ':', pid, 'ending....')
    os.kill(pid, signal.SIGTERM)
    #os.waitpid(pid, 0)
    CHILDREN[task_id] = None


def start_child(task_id):
    pid = os.fork()
    if pid: # parent proces
        CHILDREN[task_id] = pid
        return pid
    signal.signal(signal.SIGTERM, sig_hander_child)
    signal.signal(signal.SIGINT, sig_hander_child)
    print_log(options.server_name, ':', task_id, ':', os.getpid(), 'started')
    return pid


def restart_child(task_id):
    kill_child(task_id)
    return start_child(task_id)


def mem_watcher(process):
    mem_size = process.get_memory_info().rss
    timestamp = int(time.time()) + 10

    if mem_size > options.maxmem:
        # logging.info(str(gc.get_objects()))
        logging.info('------mem_watcher--------:real: %s M -- limit: %s M, server restart' % (mem_size / 1024 / 1024, options.maxmem / 1024 / 1024))
        # TODO: 内存监控
        # os.kill(os.getpid(), signal.SIGTERM)


def main():
    app = Application()

    from gconfig import game_config, front_game_config
    print_log(os.getpid(), os.getppid(), options.port)
    try:
        sockets = tornado.netutil.bind_sockets(options.port)
    except socket.error, e:
        os.system('''for i in `ps aux | grep -v 'grep' | grep 'python' | grep 'run.py' | grep 'port=%d' | awk '{if($2!=%d){print $2}}'`;do kill -9 $i;done'''%(options.port, os.getpid()))
        sockets = tornado.netutil.bind_sockets(options.port)
        print_log('killed orphan process')
    parent = True
    print os.getpid()
    global CHILDREN
    process_sum = options.numprocs
    i = 1
    for i in xrange(1, process_sum+1):
        pid = start_child(i)
        if pid == 0:
            parent = False
            break
    if parent and process_sum:
        signal.signal(signal.SIGTERM, sig_hander_parent)
        signal.signal(signal.SIGINT, sig_hander_parent)
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)   # let init clear zombie child
        print CHILDREN
        while 1:
            time.sleep(5)
            print CHILDREN
            if (game_config and game_config.reload()) or \
                    (front_game_config and front_game_config.reload()):
            # if not game_config.is_config_out():
                print_log('config out')
                # game_config.load_all()
                for task_id in CHILDREN.iterkeys():
                    print_log('config out, restart '+str(task_id))
                    if not restart_child(task_id):
                        parent = False
                        break
            if not parent:
                break

            for task_id, pid in CHILDREN.iteritems():   # if child is alive
                try:
                    child_process = psutil.Process(pid)
                    if not child_process.is_running() or os.getpid() != child_process.ppid():
                        print_log('NO this child, ', task_id, pid, child_process.is_running(), child_process.pid, os.getpid(), child_process.ppid())
                        raise psutil.NoSuchProcess(pid)
                    #mem_watcher(child_process)
                except psutil.NoSuchProcess, e:
                    if not start_child(task_id):    # start child
                        parent = False
                        break
            if not parent:
                break

    from lib.utils.change_time import debug_sync_change_time
    # 注意, 正式环境禁止启动此函数
    if settings.DEBUG:
        # 重启先加载时间
        debug_sync_change_time()
        # 每10秒钟加载时间
        tornado.ioloop.PeriodicCallback(debug_sync_change_time, 10*1000).start()

    if settings.DEBUG and not process_sum:
        def check_config():
            if (game_config and game_config.reload()) or \
                    (front_game_config and front_game_config.reload()):
            # if not game_config.is_config_out():
                print_log('config out')
                # game_config.load_all()
        # 每5秒钟加载时间
        tornado.ioloop.PeriodicCallback(check_config, 5*1000).start()

    print 'start, ', options.port+i, os.getpid(), os.getppid()
    server = HTTPServer(app, xheaders=True)
    server.add_sockets(sockets)
    loop = ioloop.IOLoop.instance()
    loop.start()


def main_single():
    from gconfig import game_config, front_game_config

    # tornado多进程模式不支持debug模式中的autoreload
    debug = options.debug if options.numprocs == 1 else False
    # 开发环境 debug 模式启动
    app = Application(True)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port)
    server.start(options.numprocs)
    process = psutil.Process(os.getpid())

    def shutdown():
        server.stop()
        deadline = int(time.time()) + 1
        io_loop = tornado.ioloop.IOLoop.instance()

        def stop_loop():
            now = int(time.time())
            if now < deadline and io_loop._callbacks:
                io_loop.add_timeout(now+1, stop_loop)
                logging.info('stop_loop delayed: pid=%s' % os.getpid())
            else:
                logging.info('stop_loop success: pid=%s' % os.getpid())
                io_loop.stop()
        stop_loop()

    def sig_handler(sig, frame):
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    from lib.utils.change_time import debug_sync_change_time
    # 注意, 正式环境禁止启动此函数
    if settings.DEBUG:
        # 重启先加载时间
        debug_sync_change_time()
        # 每10秒钟加载时间
        tornado.ioloop.PeriodicCallback(debug_sync_change_time, 10*1000).start()

    # 监控配置
    # tornado.ioloop.PeriodicCallback(game_config.auto_reload_all, 10*1000).start()
    if game_config:
        tornado.ioloop.PeriodicCallback(game_config.reload, 10*1000).start()
    if front_game_config:
        tornado.ioloop.PeriodicCallback(front_game_config.reload, 10 * 1000).start()

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    logging.info('start_single_loop success: pid=%s, parent=%s' % (os.getpid(), os.getppid()))
    io_loop = tornado.ioloop.IOLoop.instance()
    io_loop.start()


if __name__ == "__main__":
    if options.numprocs == 1:
        print 'start server main_single()'
        main_single()
    else:
        print 'start server main()'
        main()
