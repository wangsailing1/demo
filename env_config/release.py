#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import importlib
import os
import inspect

# 每个env都需要有的全局变量
DEBUG = False        # debug模式
BACK_BATTLE_DEBUG = False   # 后端战斗debug
PLATFORM = 'release3'    # 平台标示
URL_PARTITION = 'release'
# MASTER_HOST = 'yxhysuper2game3.yingxiong.com'
MASTER_HOST = '120.92.211.71'
# CHAT_HOST = '120.92.211.71'
CHAT_IDS = [
    ('120.92.211.71', 9999),        # nginx-003
    ('120.92.105.72', 9999),        # app-006
    ('120.92.107.117', 9999),       # app-013
]

LANGUAGE = 'ch'
CDN = 'supyxlmcdn2.yingxiong.com'
CONFIG_RESOURCE_OPEN = True
HERO_LOG_SWITCH = True
HERO_CHAT_SWITCH = True
APP_STORE_BID_LIST = ['com.zygames.cjyxlm']
CURRENCY_TYPE = u'RMB'  # 货币类型
RPC_SERVER_ADDR = ('10.0.0.18', 8001)    # c++服务器地址

# RPC_SERVER_ADDR_LIST = [('10.0.0.18', 8001), ('10.0.0.18', 8002), ('10.0.0.18', 8003), ('10.0.0.18', 8004)]
RPC_SERVER_ADDR_LIST = [('10.0.0.18', 8001)]
RPC_CLIENT_DICT = {}
# 大地图服务器地址
SLG_CPP_ADDR = {'ip': "120.92.81.240", "port": "8001"}

HERO_SERVER_TYPE = 2    # 英雄互娱区服类型，iOS需要改成1

# slg服务redis地址，用来查看slg在线人数等
SLG_REDIS_DEFAULT = {'host': '10.0.0.19', 'port': 6301, 'socket_timeout': 5, 'db': 0, 'password': 'Afn27Nh2WBwEPET2BtrD'}
SLG_REQUESTRUN = {
    # slg_server_id: redis_config
    # <redis ip = "127.0.0.1" port = "6379" passgword = "" timeout = "1" select_db = "7"/>
    '1': {'prefix': 'h1.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=0)},
    '2': {'prefix': 'h2.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=1)},
    '3': {'prefix': 'h3.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=2)},
    '4': {'prefix': 'h4.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=3)},
    '5': {'prefix': 'h5.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=4)},
    '6': {'prefix': 'h6.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=5)},
    '7': {'prefix': 'h7.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=6)},
    '8': {'prefix': 'h8.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=7)},
    '9': {'prefix': 'h9.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=8)},
    '10': {'prefix': 'h10.', 'redis_config': dict(SLG_REDIS_DEFAULT, db=9)},
}
# slg gm redis
SLG_RESPONE = dict(SLG_REDIS_DEFAULT, db=0)


# master配置
master = {'host': '10.0.0.5', 'port': 6305, 'socket_timeout': 5, 'db': 0, 'password': 'Afn27Nh2WBwEPET2BtrD'}
# 公共配置
public = {'host': '10.0.0.5', 'port': 6305, 'socket_timeout': 5, 'db': 1, 'password': 'Afn27Nh2WBwEPET2BtrD'}
# 聊天
chat_config = {'host': '10.0.0.5', 'port': 6305, 'socket_timeout': 5, 'db': 1, 'password': 'Afn27Nh2WBwEPET2BtrD'}
# celery
celery_config = {'host': '10.0.0.5', 'port': 6305, 'socket_timeout': 5, 'db': 2, 'password': 'Afn27Nh2WBwEPET2BtrD'}

# 每个app配置
apps = [
    # 10.0.0.19：6302,此redis端口用于slg功能用
    # server, long_net_name, redis_ip, redis_port, redis_db, father_server
    ('gt1', 'net1', '10.0.0.19', 6302, 0),
    ('gt2', 'net1', '10.0.0.19', 6303, 0),
    # ('gt3', 'net1', '10.0.0.19', 6304, 0),
    ('gt4', 'net1', '10.0.0.19', 6305, 0),
    ('gt5', 'net1', '10.0.0.19', 6306, 0),
    ('gt6', 'net1', '10.0.0.19', 6307, 0),
    ('gt7', 'net1', '10.0.0.19', 6308, 0),
    ('gt8', 'net1', '10.0.0.19', 6309, 0),
    ('gt9', 'net1', '10.0.0.19', 6310, 0),

    ('gt10', 'net1', '10.0.0.19', 6303, 0),
    ('gt11', 'net1', '10.0.0.19', 6304, 0),
    ('gt12', 'net1', '10.0.0.19', 6305, 0),
    ('gt13', 'net1', '10.0.0.19', 6306, 0),
    ('gt14', 'net1', '10.0.0.19', 6307, 0),
    ('gt15', 'net1', '10.0.0.19', 6308, 0),
    ('gt16', 'net1', '10.0.0.19', 6309, 0),
    ('gt17', 'net1', '10.0.0.19', 6310, 0),

    ('gt18', 'net1', '10.0.0.37', 6301, 0),
    ('gt19', 'net1', '10.0.0.37', 6302, 0),
    ('gt20', 'net1', '10.0.0.37', 6303, 0),
    ('gt21', 'net1', '10.0.0.37', 6304, 0),
    ('gt22', 'net1', '10.0.0.37', 6305, 0),
    ('gt23', 'net1', '10.0.0.37', 6306, 0),
    ('gt24', 'net1', '10.0.0.37', 6307, 0),
    ('gt25', 'net1', '10.0.0.37', 6308, 0),
    ('gt26', 'net1', '10.0.0.37', 6309, 0),
    ('gt27', 'net1', '10.0.0.37', 6310, 0),

    ('gt28', 'net1', '10.0.0.9', 6301, 0),
    ('gt29', 'net1', '10.0.0.9', 6302, 0),
    ('gt30', 'net1', '10.0.0.9', 6303, 0),
    ('gt31', 'net1', '10.0.0.9', 6304, 0),
    ('gt32', 'net1', '10.0.0.9', 6305, 0),
    ('gt33', 'net1', '10.0.0.9', 6306, 0),
    ('gt34', 'net1', '10.0.0.9', 6307, 0),
    ('gt35', 'net1', '10.0.0.9', 6308, 0),
    ('gt36', 'net1', '10.0.0.9', 6309, 0),
    ('gt37', 'net1', '10.0.0.9', 6310, 0),

    ('gt38', 'net1', '10.0.0.37', 6301, 0),
    ('gt39', 'net1', '10.0.0.37', 6302, 0),
    # ('gt40', 'net1', '10.0.0.37', 6303, 0),
    ('gt40', 'net1', '10.0.0.37', 6304, 0),
    ('gt41', 'net1', '10.0.0.37', 6305, 0),
    ('gt42', 'net1', '10.0.0.37', 6306, 0),
    ('gt43', 'net1', '10.0.0.37', 6307, 0),
    ('gt44', 'net1', '10.0.0.37', 6308, 0),
    ('gt45', 'net1', '10.0.0.37', 6309, 0),
    ('gt46', 'net1', '10.0.0.37', 6310, 0),

    ('gt47', 'net1', '10.0.0.9', 6301, 0),
    ('gt48', 'net1', '10.0.0.9', 6302, 0),
    ('gt49', 'net1', '10.0.0.9', 6303, 0),
    ('gt50', 'net1', '10.0.0.9', 6304, 0),
    ('gt51', 'net1', '10.0.0.9', 6305, 0),
    ('gt52', 'net1', '10.0.0.9', 6306, 0),
    ('gt53', 'net1', '10.0.0.9', 6307, 0),
    ('gt54', 'net1', '10.0.0.9', 6308, 0),
    ('gt55', 'net1', '10.0.0.9', 6309, 0),
    ('gt56', 'net1', '10.0.0.9', 6310, 0),

    ('gt57', 'net1', '10.0.0.37', 6301, 0),
    ('gt58', 'net1', '10.0.0.37', 6302, 0),
    ('gt59', 'net1', '10.0.0.37', 6304, 0),
    ('gt60', 'net1', '10.0.0.37', 6305, 0),
    ('gt61', 'net1', '10.0.0.37', 6307, 0),
    ('gt62', 'net1', '10.0.0.37', 6309, 0),
    ('gt63', 'net1', '10.0.0.37', 6310, 0),

    ('gt64', 'net1', '10.0.0.19', 6303, 0),
    ('gt65', 'net1', '10.0.0.19', 6304, 0),
    ('gt66', 'net1', '10.0.0.19', 6305, 0),
    ('gt67', 'net1', '10.0.0.19', 6306, 0),
    ('gt68', 'net1', '10.0.0.19', 6307, 0),
    ('gt69', 'net1', '10.0.0.19', 6308, 0),
    ('gt70', 'net1', '10.0.0.19', 6309, 0),
    ('gt71', 'net1', '10.0.0.19', 6310, 0),

    ('gt72', 'net1', '10.0.0.9', 6301, 0),
    ('gt73', 'net1', '10.0.0.9', 6302, 0),
    ('gt74', 'net1', '10.0.0.9', 6303, 0),
    ('gt75', 'net1', '10.0.0.9', 6304, 0),
    ('gt76', 'net1', '10.0.0.9', 6305, 0),
    ('gt77', 'net1', '10.0.0.9', 6306, 0),
    ('gt78', 'net1', '10.0.0.9', 6307, 0),
    ('gt79', 'net1', '10.0.0.9', 6308, 0),
    ('gt80', 'net1', '10.0.0.9', 6309, 0),
    ('gt81', 'net1', '10.0.0.9', 6310, 0),
]


resource = [
    'http://%s/%s/lr' % (CDN, URL_PARTITION),
    'http://%s/%s/lr' % (MASTER_HOST, URL_PARTITION)
]
# 前端热更配置地址
config_resource = [
    'http://%s/%s/lr/cr/' % (CDN, URL_PARTITION),
]

payment_callback_url = 'http://%s/%s' % (MASTER_HOST, URL_PARTITION)

PAYMENT_CONFIG = {
    'host': '10.0.0.5',
    'user': 'super2_test3',
    'passwd': '8tIpyvTQoAKtk8NmaJYE',
    'db': 'super2_test3',
    'table_prefix': 'payment',
}

SPEND_CONFIG = {
    'host': '10.0.0.5',
    'user': 'super2_test3',
    'passwd': '8tIpyvTQoAKtk8NmaJYE',
    'db': 'super2_test3',
    'table_prefix': 'spend',
}

EARN_CONFIG = {
    'host': '10.0.0.5',
    'user': 'super2_test3',
    'passwd': '8tIpyvTQoAKtk8NmaJYE',
    'db': 'super2_test3',
    'table_prefix': 'earn',
}

QUEST_CONFIG = {
    'host': '10.0.0.5',
    'user': 'super2_test3',
    'passwd': '8tIpyvTQoAKtk8NmaJYE',
    'db': 'super2_test3',
    'table_prefix': 'quest',
}

GS_HOST = {
    'host': '10.0.0.5',
    'user': 'super2_test3',
    'passwd': '8tIpyvTQoAKtk8NmaJYE',
    'db': 'super2_test3',
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
        'redis': {'host': i[2], 'port': i[3], 'socket_timeout': 5, 'db': i[4], 'password': 'Afn27Nh2WBwEPET2BtrD'},
        # 'long_addr': long_net_config.get(i[1], long_net_config.values()[0]),
        'cpp_addr': SLG_CPP_ADDR,
        'net_name': i[1],
        'chat_ip': chat_ip,
        'chat_port': chat_port,
        'father_server': father_server,
        'config_type': 1,
    }
