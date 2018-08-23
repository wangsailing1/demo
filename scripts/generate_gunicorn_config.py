#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 批量导入配置

import os
import sys
import importlib

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
LONG_ROOT_PATH = os.path.join(ROOT_PATH, 'long_connection_server')
sys.path.insert(0, ROOT_PATH)
sys.path.insert(0, LONG_ROOT_PATH)


def config_format(env, server_group, server_name, path):
    """

    :return:
    """
    s = """
[program:%(env)s_long_%(server_name)s]
process_name = %%(program_name)s
directory = %(path)s/long_connection_server
command = /usr/local/bin/python appmain.py %(server_group)s %(server_name)s %(env)s

environment = PYTHONUNBUFFERED=1
environment = PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
environment = PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=2

autorestart = true
stopwaitsecs = 20

stdout_logfile=%(path)s/long_connection_server/log/%(server_name)s_out.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stdout_capture_maxbytes=100MB
stderr_logfile=%(path)s/long_connection_server/log/%(server_name)s_err.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
stderr_capture_maxbytes=100MB
loglevel=debug
    """ % {'env': env, 'server_name': server_name, 'path': path, 'server_group': server_group}
    return s


def trans(env, path):
    config_file = importlib.import_module('netsettings.%s' % env)
    config = config_file.config
    for server_group, server_config in config['servers'].iteritems():
        if isinstance(server_config, list):
            for server in server_config:
                server_name = server['name']
                print config_format(env, server_group, server_name, path)
        else:
            server_name = server_config['name']
            print config_format(env, server_group, server_name, path)


if __name__ == '__main__':
    env = sys.argv[1]
    path = sys.argv[2]
    trans(env, path)
