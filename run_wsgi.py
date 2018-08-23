#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import sys

# 设置程序使用的编码格式, 统一为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

import os

from tornado.wsgi import WSGIApplication
from tornado.options import options

# 解析tornado启动参数, 设置日志debug级别
options.parse_command_line(['', '--logging=debug'])

game_env = os.getenv('game_env')
server = os.getenv('server', 'all')
print 'game_env: %s | server: %s' % (game_env, server)

import settings
settings.set_env(game_env, server)


class Application(WSGIApplication):
    def __init__(self):
        handlers = [
            (r"/%s/pay-callback-([\w-]+)/?" % settings.URL_PARTITION, 'handlers.PayCallback'),
            (r"/?[a-zA-Z0-9_]*/api/?", 'handlers.APIRequestHandler'),
            (r"/?[a-zA-Z0-9_]*/login/?", 'handlers.LoginHandler'),
            (r"/?[a-zA-Z0-9_]*/config/?", 'handlers.ConfigHandler'),
            # (r"/?[a-zA-Z0-9_]*/lr_version/?", 'handlers.ConfigHandler'),
            (r"/%s/admin/([\w-]+)/?" % settings.URL_PARTITION, 'admin.handler.AdminHandler'),
            (r"/%s/admin/([\w-]+)/([\w-]+)/?" % settings.URL_PARTITION, 'admin.handler.AdminHandler'),
        ]

        app_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_prefix='/%s/static/' % settings.URL_PARTITION,
            debug=False,
            log_function=lambda x: 0,
        )

        super(Application, self).__init__(handlers, **app_settings)


app = Application()
