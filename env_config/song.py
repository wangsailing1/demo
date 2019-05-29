#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import importlib
import os
import inspect
import socket


# 本机开发环境直接读本机ip
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


local_ip = get_host_ip() or '127.0.0.1'

# 每个env都需要有的全局变量
DEBUG = True        # debug模式
BACK_BATTLE_DEBUG = False   # 后端战斗debug
BDC_LOG_SEND_TO_ALIYUN = False   # bdc日志开关，是否发往阿里云

PLATFORM = 'song'    # 平台标示
URL_PARTITION = 'big_sale'
# MASTER_HOST = '192.168.7.224:8888'
MASTER_HOST = '%s:8888' % local_ip
# CHAT_HOST = '127.0.0.1'
CHAT_IDS = [('127.0.0.1', 9999)]

LANGUAGE = 'ch'
CURRENCY_TYPE = u'RMB'  # 货币类型

RPC_SERVER_ADDR = ('localhost', 8000)

resource = 'http://%s/%s/lr' % (MASTER_HOST, URL_PARTITION)
payment_callback_url = 'http://%s/%s' % (MASTER_HOST, URL_PARTITION)

# DINGTALK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=65b10b52e5038db8362f6d6334df207dccf95410a5e74c99e64ac5dc1152a761'


# slg服务redis地址，用来查看slg在线人数等
SLG_REDIS_DEFAULT = {'host': '127.0.0.1', 'port': 6379, 'socket_timeout': 5, 'db': 15, 'password': ''}
SLG_REQUESTRUN = {
    # slg_server_id: redis_config
    # 同 <redis ip = "127.0.0.1" port = "6379" password = "" timeout = "1" select_db = "7"/>
    '8': {'prefix': 'h2.', 'redis_config': SLG_REDIS_DEFAULT}

}
# slg gm redis
SLG_RESPONE = dict(SLG_REDIS_DEFAULT, db=3)


# master配置
master = {'host': '127.0.0.1', 'port': 6301, 'socket_timeout': 5, 'db': 15, 'password': ''}
# 公共配置
public = {'host': '127.0.0.1', 'port': 6301, 'socket_timeout': 5, 'db': 14, 'password': ''}
# 聊天
chat_config = {'host': '127.0.0.1', 'port': 6301, 'socket_timeout': 5, 'db': 14, 'password': ''}
# celery
celery_config = {'host': '127.0.0.1', 'port': 6301, 'socket_timeout': 5, 'db': 14, 'password': ''}

# 每个app配置
apps = [
    # server, long_net_name, redis_ip, redis_port, redis_db, father_server
    # 传给前端的各个区服连接对应的net节点,与netsettings里的匹配
    ('gtt1', 'net1', '127.0.0.1', 6301, 3),
    ('gtt2', 'net1', '127.0.0.1', 6301, 3),
    ('gtt3', 'net1', '127.0.0.1', 6301, 3),
    ('gtt4', 'net1', '127.0.0.1', 6301, 3),
    ('gtt5', 'net1', '127.0.0.1', 6301, 3),
]

PAYMENT_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'big_sale',
    'table_prefix': 'payment',
}

SPEND_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'big_sale',
    'table_prefix': 'spend',
}

EARN_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'big_sale',
    'table_prefix': 'earn',
}

QUEST_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'big_sale',
    'table_prefix': 'quest',
}

GS_HOST = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'big_sale',
    'table_prefix': 'client_service',
}

SERVERS = {
    'master': {
        'redis': master,
        'server': 'http://%s/%s/' % (MASTER_HOST, URL_PARTITION),
    },
    'public': {
        'redis': public,
        'server': 'http://%s/%s/' % (MASTER_HOST, URL_PARTITION),
    }
}

# 获取当前文件名
filename = inspect.getframeinfo(inspect.currentframe()).filename
env_name = os.path.basename(filename).split('.')[0]

# 长连配置获取
# long_env_module = importlib.import_module('long_connection_server.netsettings.%s' % env_name)
# long_settings = getattr(long_env_module, 'config')
# long_net_config = dict([(net['name'], (net.get('netouterhost', net['netinnerhost']), net['netport']))
#                         for net in long_settings.get('servers', {}).get('net', [])])

chat_ips_len = len(CHAT_IDS)
x = []
for k, i in enumerate(apps):
    if i[0] in x:
        continue
    father_server = i[5] if len(i) > 5 and i[5] else i[0]
    chat_ip, chat_port = CHAT_IDS[int(father_server[-1]) % chat_ips_len]
    SERVERS[i[0]] = {
        'server': 'http://%s/%s/' % (MASTER_HOST, i[0]),
        'redis': {'host': i[2], 'port': i[3], 'socket_timeout': 5, 'db': i[4], 'password': ''},
        'cpp_addr': {'ip': local_ip, "port": "8000"},
        'net_name': i[1],
        'chat_ip': chat_ip,
        'chat_port': chat_port,
        'father_server': father_server,
        'config_type': 1,
    }
