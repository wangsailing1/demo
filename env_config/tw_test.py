#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

import importlib
import os
import inspect

# 每个env都需要有的全局变量
DEBUG = True        # debug模式
KVGAME_SDK_DEBUG = False     # 凯奇谷自有sdk 是否走测试环境验证
BACK_BATTLE_DEBUG = False   # 后端战斗debug
BDC_LOG_SEND_TO_ALIYUN = True   # bdc日志开关，是否发往阿里云
# 日志平台类型  SERVER|SERVER_TEST 正式|测试
BDC_PLATFORM = 'SERVER'


PLATFORM = 'tw_test'    # 平台标示
URL_PARTITION = 'big_sale_tw'
MASTER_HOST = '164.52.8.250'
IN_MASTER_HOST = '10.10.4.11'          # 内网地址 备份用
# CHAT_HOST = '192.168.1.9'
# CHAT_IDS = [('192.168.1.9', 9079)]
CHAT_IDS = [('164.52.8.250', 9999)]

LANGUAGE = 'tw'
CDN = 'big-sale-tw-test.hi365.com'
CONFIG_RESOURCE_OPEN = True
CURRENCY_TYPE = u'RMB'  # 货币类型
RPC_SERVER_ADDR = ('192.168.1.99', 8000)    # c++服务器地址

APP_STORE_BID_LIST = ['com.kqg.qyjy.twaos']

# DINGTALK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=e5739a6ec80b8e5215bdf95a52f08ce7ccb167192bb656272a2d3b6eb9f600f1'

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
master = {'host': '10.10.4.14', 'port': 6300, 'socket_timeout': 5, 'db': 0, 'password': 'HXeOrXEEls7ObAF3Xmy3'}
# 公共配置
public = {'host': '10.10.4.14', 'port': 6300, 'socket_timeout': 5, 'db': 1, 'password': 'HXeOrXEEls7ObAF3Xmy3'}
# 聊天
chat_config = {'host': '10.10.4.14', 'port': 6300, 'socket_timeout': 5, 'db': 2, 'password': 'HXeOrXEEls7ObAF3Xmy3'}
# celery
celery_config = {'host': '10.10.4.14', 'port': 6300, 'socket_timeout': 5, 'db': 14, 'password': 'HXeOrXEEls7ObAF3Xmy3'}

# 每个app配置
apps = [
    # server, long_net_name, redis_ip, redis_port, redis_db, father_server
    ('tw1', 'net1', '10.10.4.14', 6300, 3),
    ('tw2', 'net1', '10.10.4.14', 6301, 3),
    ('tw3', 'net1', '10.10.4.14', 6302, 3),
    ('tw4', 'net1', '10.10.4.14', 6303, 3),
]


# 前端热更资源地址
# resource = 'http://%s/%s/lr' % (MASTER_HOST, URL_PARTITION)

resource ='http://%s/%s/lr' % (CDN, URL_PARTITION)
# 前端热更配置地址
config_resource = [
    'http://%s/%s/lr/cr/' % (CDN, URL_PARTITION),
    'http://%s/%s/lr/cr/' % (MASTER_HOST, URL_PARTITION),
]

payment_callback_url = 'http://%s/%s' % (MASTER_HOST, URL_PARTITION)

PAYMENT_CONFIG = {
    'host': '10.10.4.14',
    'user': 'root',
    'passwd': '1MRzvCJZa0S0K6h929cT',
    'db': 'sale_tw',
    'table_prefix': 'payment',
}

SPEND_CONFIG = {
    'host': '10.10.4.14',
    'user': 'root',
    'passwd': '1MRzvCJZa0S0K6h929cT',
    'db': 'sale_tw',
    'table_prefix': 'spend',
}

EARN_CONFIG = {
    'host': '10.10.4.14',
    'user': 'root',
    'passwd': '1MRzvCJZa0S0K6h929cT',
    'db': 'sale_tw',
    'table_prefix': 'earn',
}

QUEST_CONFIG = {
    'host': '10.10.4.14',
    'user': 'root',
    'passwd': '1MRzvCJZa0S0K6h929cT',
    'db': 'sale_tw',
    'table_prefix': 'quest',
}

GS_HOST = {
    'host': '10.10.4.14',
    'user': 'root',
    'passwd': '1MRzvCJZa0S0K6h929cT',
    'db': 'sale_tw',
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
        'redis': {'host': i[2], 'port': i[3], 'socket_timeout': 5, 'db': i[4], 'password': 'HXeOrXEEls7ObAF3Xmy3'},
        # 'long_addr': long_net_config.get(i[1], long_net_config.values()[0]),
        'cpp_addr': {'ip': "192.168.1.9", "port": "8000"},
        'net_name': i[1],
        'chat_ip': chat_ip,
        'chat_port': chat_port,
        'father_server': father_server,
        'config_type': 1,
    }

VIVO_PAY_CALLBACK_URL = 'http://%s/%s/pay-callback-vivo/?tp=vivo' % (MASTER_HOST, URL_PARTITION)
