#! --*-- coding: utf-8 --*--

__author__ = 'sm'


import os
import re
import importlib
import time
import json

DEBUG = True
# 是否强制发出来error至钉钉，忽略DEBUG影响
IMMEDIATE_DINGTALK_ERROR_MAIL = True

PRODUCT_NAME = u'大卖王'
PLATFORM = ''    # 平台标示
BACK_BATTLE_DEBUG = False   # 后端战斗debug

# 注册包名(只有iOS的, 现主要用于过滤其它游戏模拟iOS充值回调我们的请求)
APP_STORE_BID_LIST = ['com.kqg.qyjy.twaos', 'com.kaiqigu.cjyx2.cntzd']
ADMIN_LIST = [
    'jianmin.liu@kaiqigu.com',
    'ming.song@kaiqigu.com',
]

DEFAULT_BACKEND_ADMIN = [   # 初始化后台管理员
    ('test_admin', '1qwer$#@'),      # username, password
]

# 报错 钉钉通知地址
DINGTALK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=18313a7facae1b034a61512918d79d7bb35335ddbe95c997503f1c62b6adffdd'

############### 2019.12.11 英雄互娱新版 BI 接入系统相关参数，直接对接阿里云 ###############

BDC_LOG_SEND_TO_ALIYUN = False      # bdc日志开关，是否发往阿里云
BDC_APP_KEY = '3bfd444171e8488fbeb3d7984176c60b'
# 日志平台类型  SERVER|SERVER_TEST 正式|测试
BDC_PLATFORM = 'SERVER_TEST'

BDC_END_POINT = 'http://cn-beijing.log.aliyuncs.com'
BDC_LOG_PROJECT = 'tyrannosaurus'
BDC_LOG_STORE_SERVER = 'bwl_risingstar_serverlib'
BDC_ACCESS_KEY_ID = 'LTAI3eTRUxker0ei'
BDC_ACCESS_KEY_SECRET = 'DwuWlaS2Quqdoy8ZI8SNc1qbVKhg8a'



############### 2019.12.11 英雄互娱新版 BI 接入系统相关参数，直接对接阿里云 ###############



#### 作废 2019.12.11 #######
# 英雄互娱 bi 接入相关参数 ########

BDC_VERSION_ID = '13'       # 版本ID          # ios 11, 安卓13
BDC_GAME_ID = '0172'        # GameID

# "CP同学请自行选取1-2位数字对不同区服进行区分（如iOS、硬核、混服）,通服可不用区分。
# 例：010002 01-硬核 0002区服号"
BDC_SERVER_TYPE = '01'   # 2位区服分类ID

BDC_CHANNEL_ID = '001270'   # 渠道ID 安卓渠道     000001: 官方正版
BDC_LOG_DELITIMER = '\x1b\x7c'
# 英雄互娱 bi 接入相关参数 ########
#### 作废 2019.12.11 #######



# slg服务redis地址，用来查看slg在线人数等
SLG_RESPONE_MSG = {}
SLG_REDIS_TABLE_PREFIX = 'h2.'
SLG_REQUESTRUN = {
    # slg_server_id: redis_config
    # <redis ip = "127.0.0.1" port = "6379" password = "" timeout = "1" select_db = "7"/>
    # 8: {'host': '127.0.0.1', 'port': 6379, 'socket_timeout': 5, 'db': 3, 'password': ''}
}
# slg gm redis
SLG_RESPONE = {
    # 'host': '127.0.0.1', 'port': 6379, 'socket_timeout': 5, 'db': 3, 'password': ''
}



bdc_server_cache = {}


def get_bdc_server_id(server):
    if server in bdc_server_cache:
        return bdc_server_cache[server]
    UID_PREFIX = globals()['UID_PREFIX']
    # account_login 登录动作 无法判断区服，默认都走1
    if server in ['master']:
        server_num = '1'
    else:
        server_num = server[len(UID_PREFIX):]
    bdc_server_cache[server] = file = ''.join((BDC_VERSION_ID, BDC_GAME_ID, BDC_SERVER_TYPE, server_num.zfill(4)))
    return file


def get_bdc_channel_id(yxhy_channel_id):
    """获取英雄互娱的渠道信息
    :param yxhy_channel_id: 英雄互娱提供的渠道id
    :return:
    """
    from gconfig import game_config

    yxhy_channel_id = int(yxhy_channel_id)
    channel_config = game_config.hero_channel_config.get(yxhy_channel_id)
    # todo 等前端接完sdk、配置
    return 18   # 英雄互娱-安卓

    bdc_id = BDC_CHANNEL_ID
    if channel_config:
        bdc_id = channel_config['bdc_id'].zfill(6)
    return ''.join((BDC_VERSION_ID, BDC_GAME_ID, bdc_id))


def get_channel_name(channel):
    from gconfig import game_config
    try:
        channel = int(channel)
    except:
        pass
    return game_config.hero_channel_config.get(channel, {}).get('channel_name', channel)


BASE_ROOT = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
INFO_ROOT = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

ZIP_COMPRESS_SWITCH = True     # 数据压缩开关
MIN_COMPRESS = 50           # 最小字节的压缩大小
FILTER_ADMIN_PAY = True    # 后台页面是否过滤 虚拟充值

SESSION_SWITCH = False       # session开关
SESSION_EXPIRED = 24 * 60 * 60    # session过期时间

REGISTER_MODELS_STATUS = False
REGISTER_TOOLS_STATUS = False

LANG = 'ch'  # 语言: ch 简体中文
LAN_SORT = 1    # 语言: 1:中文简体，0:台湾
CURRENCY_TYPE = u'RMB'  # 货币类型

ENV_NAME = ''
SERVERS = {}
ALL_DB_SERVERS = {}
long_settings = {}
SERVER_SORT = 'all'

resource = ''  # 前端热更地址
config_resource = []    # 前端配置热更地址

# 提供查询支付回调的平台
notify_url_platform = ('vivo', 'jinli', '360', 'lenovo', 'oppo', 'youku', 'yy', 'lewan', 'xmwan', 'uc', 'meizu', 'hero')
currency_map_charge = {'RMB': 'CN', 'USD': 'TW', 'TWD': 'TWD'}
payment_callback_url = ''       # 支付回调地址

admin_cookie = 'kqggenesis2'    # admin的cookie
admin_secret_key = '5e3b4530b293b5c1f4eeca4638ab4dc1'   # admin使用

BACK_CONFIG_SWITCH = False      # 后端配置开关
FRONT_CONFIG_SWITCH = False     # 前端配置开关
BACK_CONFIG_NAME_LIST = []      # 后端配置名列表
FRONT_CONFIG_NAME_LIST = []     # 前端配置名列表

FRONTWINDOW = '5e3b4530b293b5c1f4eeca4638ab4dc1'        # 多点验证码
BROWSER = 'a7b87e9d6faae5e7c4962d001bbd62b1'            # 浏览器验证码

# xxtes key
XXTEA_SIGNATURE_KEY = 'Kqg-+9Myfront1*/'

# 配置走cdn开关、地址
CONFIG_RESOURCE_OPEN = False
CONFIG_RESOURCE_PATH = '%slogs/lr/cr/' % BASE_ROOT

# 战斗加密环境
ENCRYPT_ENV = []

# 消费活动记录忽略接口
SPEND_IGNORE_METHOD = ['bandit.get_reward', 'server_bandit.get_reward', 'invest.investing', 'invest.quickly_reward', 'server_invest.investing', 'server_invest.quickly_reward']

# celery开关
CELERY_SWITCH = False
# 英雄互娱服务器日志开关
HERO_LOG_SWITCH = False
# 英雄互娱聊天数据上传开关
HERO_CHAT_SWITCH = False

# rpc客户端
RPC_CLIENT = None
RPC_SERVER_ADDR = ()
RPC_SERVER_ADDR_LIST = []
RPC_CLIENT_DICT = {}
RANDOM_CLIENT_PLATFORM = ['tw_release_new', 'release_new']

# 英雄互娱IM sdk 用到,区服类型1：IOS, 2:Android 3:混服
HERO_SERVER_TYPE = 2


def import_check():
    """检查下所有py文件"""

    exclude_files = ['__init__', 'battle', 'load_config', 'ggtornado', 'gvg', 'fabfile']
    exclude_dirs = ['scripts', 'test', 'apps', 'logs', 'upload_xls', 'battle_test', 'battle_test2', 'long_connection_server']
    count = {}
    for path, dirs, files in os.walk(BASE_ROOT):
        if '/.' in path:
            continue
        if '__init__.py' not in files:
            continue

        module_dir = path.replace(BASE_ROOT, '')
        package = module_dir.replace('/', '.').replace('\\', '.')
        if not package:
            continue
        if module_dir in exclude_dirs:
            continue
        dir_name = package.split('.')[0]
        if dir_name in exclude_dirs:
            continue

        for name in files:
            if name[0] == '.':
                continue
            file_name, file_ext = os.path.splitext(name)
            if file_ext != '.py' or file_name in exclude_files:
                continue
            module = '.'.join([package, file_name])
            if DEBUG:
                print 'import_file:', path, module, file_name
            m = __import__(module, globals(), locals(), fromlist=[file_name])
            count[dir_name] = count.get(dir_name, 0) + 1

    print '--------------------check files: %s--------------------' % sum(count.values())
    for module, num in sorted(count.items()):
        print '\t'.join(map(str, (module, num)))
    print '--------------------check files end--------------------'


def set_env(env_name, server=None, cw_num=1, *args, **kwargs):
    """

    :param env_name: 环境名
    :param server:  服务类型 login | config | app | admin | payment
    :param cw_num: celery_worker数量
    :param args:
    :param kwargs:
    :return:
    """
    # game_config里的配置都是只读的,copy的时候改回原始类型
    import copy
    import copy_hook
    copy._reconstruct = copy_hook._reconstruct
    start = time.time()

    # long_env_module = importlib.import_module('long_connection_server.netsettings.%s' % env_name)
    # long_settings = getattr(long_env_module, 'config')
    #
    # globals()['long_settings'] = long_settings

    execfile(os.path.join(BASE_ROOT, 'env_config/%s.py' % env_name), globals(), globals())

    globals()['CW_NUM'] = cw_num
    globals()['ENV_NAME'] = env_name
    if server:
        globals()['SERVER_SORT'] = server

    # 当服务为配置或者后台管理需要打开前端配置
    if globals()['SERVER_SORT'] in ['config', 'admin', 'all']:
        globals()['FRONT_CONFIG_SWITCH'] = True
        globals()['BACK_CONFIG_SWITCH'] = True

    # # 当服务器为配置时需要关闭后端配置加载
    # if globals()['SERVER_SORT'] in ['config']:
    #     globals()['BACK_CONFIG_SWITCH'] = False

    # uid匹配
    prefix = ''
    length = 1
    for k in globals()['SERVERS']:
        if k in ['master', 'public']: continue
        if prefix:
            temp = len(k[len(prefix):])
            if length < temp:
                length = temp
        else:
            for idx, i in enumerate(k):
                if not k[idx:].isdigit():
                    prefix += i
                else:
                    temp = len(k[idx:])
                    if length < temp:
                        length = temp
    # eg: g11234567
    pattern = re.compile('^%s\d{%s,%s}$' % (prefix, 1 + 7, length + 7)).match
    globals()['UID_PATTERN'] = pattern
    globals()['UID_PREFIX'] = prefix
    globals()['CN_NAME_PATTERN'] = re.compile(u"([\u4e00-\u9fa5]+)").match
    globals()['GID_PATTERN'] = re.compile('%s\d+-\d+' % prefix).match

    import_check()
    print 'set_env_spend_time: ', time.time() - start


def long_addr(mm):
    """ 通过mm获取长连地址

    :param mm:
    :return:
    """
    config = globals()['SERVERS'].get(mm.server)
    return config['long_addr']


def get_net_by_uid(uid):
    """ 通过uid获取net名字

    :param uid:
    :return:
    """
    if isinstance(uid, list) or isinstance(uid, set):
        uids = uid
    else:
        uids = [uid]

    result = {}
    for uid in uids:
        net_name = globals()['SERVERS'].get(uid[:-7], {}).get('net_name', 'net1')
        if net_name not in result:
            result[net_name] = [uid]
        else:
            result[net_name].append(uid)

    return result


def check_uid(uid):
    """
    检查uid格式是否正确
    :param uid:
    :return:
    """
    if not globals()['UID_PATTERN'](uid):
        return False
    else:
        return True


def check_name(name):
    """
    名字只能是汉字,字母或数字
    :param name:
    :return:
    """
    new_name = re.findall(u'[\d,a-z,A-Z]+|[\u4e00-\u9fa5]+', name)
    if len(''.join(new_name)) != len(name):
        return False

    return True


def get_payment_callback_url(channel):
    """ 获取支付回调地址

    :param channel:
    :return:
    """
    if channel not in notify_url_platform:
        return ''
    else:
        return '%s/pay-callback-%s/' % (payment_callback_url, channel)


def get_payment_order_url(channel):
    """ 获取平台下定单的地址

    :param channel:
    :return:
    """
    if channel not in notify_url_platform:
        return ''
    if channel in ['jinli', 'vivo']:
        return '%s/pay/?method=get_%s_order&' % (payment_callback_url, channel)
    else:
        return '%s/pay/?method=get_order_%s&' % (payment_callback_url, channel)


def get_father_server(server_name):
    """如果合服则使用父服务器（father_server）, 否则返回自己
    """
    sc = globals()['SERVERS'][server_name]
    return sc.get('father_server', server_name)


def is_father_server(server_name):
    """判断是否为主服务器
    """
    return server_name == get_father_server(server_name)


def set_debug_print():
    """使print打印输出到logging输出文件中
    """
    # 让打印输出到logging.log中
    import sys
    import logging

    h = logging.getLogger('debug_print')
    h.write = h.critical
    old_stdout = sys.stdout
    sys.stdout = h


def get_near_server_name(server_name):
    """
    获取上一个和下一个服务器名
    :param server_name:
    :return:
    """
    servers = sorted([i for i in globals()['SERVERS'] if i not in ['master', 'public']])
    last_server = ''
    next_server = ''

    if server_name not in servers:
        return last_server, next_server

    _index = servers.index(server_name)
    if _index <= 0:
        last_server = ''
    else:
        last_server = servers[_index - 1]

    if _index >= len(servers) - 1:
        next_server = ''
    else:
        next_server = servers[_index + 1]

    return last_server, next_server


def get_same_redis_db_server(server_name):
    """
    获取同一个redis_db的服务器
    :param server_name:
    """
    servers = globals()['SERVERS']
    all_db_servers = globals()['ALL_DB_SERVERS']

    cur_cache_list = servers[server_name]['redis']
    cur_db_key = "%s-%s-%s" % (cur_cache_list['host'], cur_cache_list['port'], cur_cache_list['db'])
    if cur_db_key not in all_db_servers:
        for server_id, server_info in servers.iteritems():
            # if server_id in ['master', 'public']:
            #     continue
            cache_list = server_info['redis']
            cur_host, cur_port, cur_db = cache_list['host'], cache_list['port'], cache_list['db']
            db_key = "%s-%s-%s" % (cur_host, cur_port, cur_db)
            all_db_servers.setdefault(db_key, set())
            all_db_servers[db_key].add(server_id)

    return all_db_servers.get(cur_db_key, [])


def get_config_resource():
    """
    获取配置cdn地址
    :return:
    """
    if not globals()['CONFIG_RESOURCE_OPEN']:
        return []

    return globals()['config_resource']


def get_server_num(server_name):
    """
    获取服务器的数字id
    :param server_name:
    :return:
    """
    if server_name in ['master', 'public']:
        return -1
    UID_PREFIX = globals()['UID_PREFIX']
    return int(server_name[len(UID_PREFIX):])


def get_admin_charge(currency):
    if currency and currency in currency_map_charge.keys():
        return currency_map_charge[currency]
    else:
        return "CN"


def analysis_chat_data(msg):
    """解析数据"""
    index1 = msg.find('{')
    index2 = msg.rfind('}')
    if -1 in [index1, index2]:
        return ''

    j = msg[index1:index2 + 1]
    json_data = json.loads(j)

    return json_data
