#! --*-- encoding:utf-8 --*--
import socket
from tornado.options import define, options
import handlers
import tornado
import tornado.web
import os

define('port', default=8888, help='设置端口', type=int)
define('env', default='wang', help='设置配置', type=str)
define("numprocs", default=16, help="process sum", type=int)
define('debug', default=True, help='是否为开发模式', type=bool)
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

handlers = [
    (r"/?[a-zA-Z0-9_]*/api/?", handlers.APIRequestHandler),
    (r'/?[a-zA-Z0-9_]*/template/?', handlers.TempLateHandler),
    (r'/?[a-zA-Z0-9_]*?',handlers.IndexHandler),
    (r'/?[a-zA-Z0-9_]*/websocket/?', handlers.Myserver),
]
app_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_prefix='%s/static/' % ROOT_PATH,
            debug=True,
            cookie_secret='1q2w3e4r',
            #设置跳转路由，为了防止在没有登录情况下，直接输入需要登录才可见的url进行访问，做判断，如果没有登录则跳转到这个路由下
            login_url='/?template=login.html',
        )


if __name__ == '__main__':
    app  = tornado.web.Application(handlers, **app_settings)
    app.listen(address='127.0.0.1', port=8000)
    tornado.ioloop.IOLoop.current().start()