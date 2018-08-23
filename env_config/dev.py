#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import importlib
import os
import inspect

# 每个env都需要有的全局变量
DEBUG = True        # debug模式
BACK_BATTLE_DEBUG = False   # 后端战斗debug
PLATFORM = 'dev'    # 平台标示
URL_PARTITION = 'big_sale'
MASTER_HOST = '203.86.67.226'
IN_MASTER_HOST = '192.168.1.9'
# CHAT_HOST = '192.168.1.9'
CHAT_IDS = [('192.168.1.9', 9990)]

LANGUAGE = 'ch'
CDN = 'cdncn.cjyx2.hi365.com'
CONFIG_RESOURCE_OPEN = True
CURRENCY_TYPE = u'RMB'  # 货币类型
RPC_SERVER_ADDR = ('192.168.1.99', 8000)    # c++服务器地址

APP_STORE_BID_LIST = ['com.kqg.qyjy.twaos']

# slg服务redis地址，用来查看slg在线人数等
SLG_REDIS_DEFAULT = {'host': '192.168.1.98', 'port': 6300, 'socket_timeout': 5, 'db': 0, 'password': 'MpkgVasDIakFEqwUgtqL'}
SLG_REQUESTRUN = {
    # slg_server_id: redis_config
    # <redis ip = "127.0.0.1" port = "6379" password = "" timeout = "1" select_db = "7"/>
    '8': {'prefix': 'h2.', 'redis_config': SLG_REDIS_DEFAULT}

}
# slg gm redis
SLG_RESPONE = dict(SLG_REDIS_DEFAULT, db=3)


# master配置
master = {'host': '192.168.1.103', 'port': 6311, 'socket_timeout': 5, 'db': 0, 'password': 'k2IEKp2PbiQSOfu2MNOf'}
# 公共配置
public = {'host': '192.168.1.103', 'port': 6311, 'socket_timeout': 5, 'db': 1, 'password': 'k2IEKp2PbiQSOfu2MNOf'}
# 聊天
chat_config = {'host': '192.168.1.103', 'port': 6311, 'socket_timeout': 5, 'db': 2, 'password': 'k2IEKp2PbiQSOfu2MNOf'}
# celery
celery_config = {'host': '192.168.1.103', 'port': 6311, 'socket_timeout': 5, 'db': 2, 'password': 'k2IEKp2PbiQSOfu2MNOf'}

# 每个app配置
apps = [
    # server, long_net_name, redis_ip, redis_port, redis_db, father_server
    ('gtt1', 'net1', '192.168.1.103', 6311, 3),
    ('gtt2', 'net1', '192.168.1.103', 6311, 3),
    ('gtt3', 'net1', '192.168.1.103', 6311, 3),
    ('gtt4', 'net1', '192.168.1.103', 6311, 3),
    ('gtt5', 'net1', '192.168.1.103', 6311, 3),
]


# 前端热更资源地址
resource = 'http://%s/%s/lr' % (MASTER_HOST, URL_PARTITION)
# 前端热更配置地址
config_resource = [
    # 'http://%s/%s/lr/cr/' % (CDN, URL_PARTITION),
    'http://%s/%s/lr/cr/' % (MASTER_HOST, URL_PARTITION),
]

payment_callback_url = 'http://%s/%s' % (MASTER_HOST, URL_PARTITION)

PAYMENT_CONFIG = {
    'host': '192.168.1.51',
    'user': 'root',
    'passwd': 'Kaiqigu1',
    'db': 'big_sale_dev',
    'table_prefix': 'payment',
}

SPEND_CONFIG = {
    'host': '192.168.1.51',
    'user': 'root',
    'passwd': 'Kaiqigu1',
    'db': 'big_sale_dev',
    'table_prefix': 'spend',
}

EARN_CONFIG = {
    'host': '192.168.1.51',
    'user': 'root',
    'passwd': 'Kaiqigu1',
    'db': 'big_sale_dev',
    'table_prefix': 'earn',
}

QUEST_CONFIG = {
    'host': '192.168.1.51',
    'user': 'root',
    'passwd': 'Kaiqigu1',
    'db': 'big_sale_dev',
    'table_prefix': 'quest',
}

GS_HOST = {
    'host': '192.168.1.51',
    'user': 'root',
    'passwd': 'Kaiqigu1',
    'db': 'big_sale_dev',
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
    },
}

# 获取当前文件名
filename = inspect.getframeinfo(inspect.currentframe()).filename
env_name = os.path.basename(filename).split('.')[0]

# 长连配置获取
# long_env_module = importlib.import_module('long_connection_server.netsettings.%s' % env_name)
# long_settings = getattr(long_env_module, 'config')
# long_net_config = dict([(net['name'], (net.get('netouterhost', net['netinnerhost']), net['netport']))
#                     for net in long_settings.get('servers', {}).get('net', [])])

chat_ips_len = len(CHAT_IDS)
x = []
for k, i in enumerate(apps):
    if i[0] in x:
        continue
    father_server = i[5] if len(i) > 5 and i[5] else i[0]
    chat_ip, chat_port = CHAT_IDS[int(father_server[-1]) % chat_ips_len]
    SERVERS[i[0]] = {
        # 'server': 'http://%s/%s/' % (MASTER_HOST, i[0]),
        'server': 'http://%s/%s/' % (MASTER_HOST, URL_PARTITION),
        'redis': {'host': i[2], 'port': i[3], 'socket_timeout': 5, 'db': i[4], 'password': 'k2IEKp2PbiQSOfu2MNOf'},
        # 'long_addr': long_net_config.get(i[1], long_net_config.values()[0]),
        'cpp_addr': {'ip': "203.86.67.226", "port": "8000"},
        'net_name': i[1],
        'chat_ip': chat_ip,
        'chat_port': chat_port,
        'father_server': father_server,
        'config_type': 1,
    }

VIVO_PAY_CALLBACK_URL = 'http://203.86.67.226/genesis2/pay-callback-vivo/?tp=vivo'
