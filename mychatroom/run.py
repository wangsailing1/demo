#! --*-- encoding:utf-8 --*--
import socket
from tornado.httpserver import HTTPServer
from tornado import ioloop
from tornado import web
from tornado.options import define, options
import tornado
import handlers

define('port', default=8888, help='设置端口', type=int)
define('env', default='wang', help='设置配置', type=str)
define('debug', default=True, help='是否为开发模式', type=bool)

handlers = [
    (r'/?[]/([\w+])', handlers.User),
]




