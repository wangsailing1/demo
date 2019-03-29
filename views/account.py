#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import time
import random

import settings
from lib.utils.string_operation import is_account
from lib.core.environ import ModelManager
from lib.statistics.bdc_event_funcs import special_bdc_log
from models.account import Account
from models.user import User
from models.server import ServerUidList, ServerUid
from models.server import ServerConfig
from models.bloom_filter import BloomFilter
from logics.account import login_verify
from lib.utils import sid_generate
from lib.utils.sensitive import is_sensitive
from tools.gift import add_mult_gift
from gconfig import game_config, MUITL_LAN
from return_msg_config import i18n_msg
from gconfig import get_str_words
import hashlib
from lib.sdk_platform.sdk_uc import send_role_data_uc
from lib.utils.time_tools import str2timestamp
import copy


def generate_mk(account):
    """生成随机数，做单点登录之用"""
    mk_str = str(time.time()) + account
    return hashlib.md5(str(mk_str)).hexdigest()[:10]


def register(hm):
    """ 注册账号

    :param hm: HandlerManager
    :return:
    """
    account = hm.get_argument('account')
    password = hm.get_argument('passwd', '')

    if not is_account(account):
        return 1, {}

    if not password:
        return 2, {}

    acc = Account.get(account)

    if not acc.inited:
        return 3, {}

    now = int(time.time())
    sid = sid_generate(account, now)
    acc.update_passwd(password)
    acc.save()

    rc, data = get_user_server_list(hm)
    if rc != 0:
        from lib.utils.debug import print_log
        print_log('platform_access..get_user_server_list..error: ', rc)

    return 0, {
        'server_list': data['server_list'],
        'current_server': data['current_server'],
        'resource': settings.resource,
        'config_resource': settings.config_resource,
        'ks': data['ks'],
        'mk': data['mk'],
    }


def login(hm):
    """ 登录

    :param hm:
    :return:
    """
    # account_name = hm.get_argument('account')
    # password = hm.get_argument('passwd', '')
    #
    # acc = Account.get(account_name)
    # if acc.inited:
    #     return 1, {}
    #
    # if not acc.check_passwd(password):
    #     return 2, {}
    #
    # sid, expired = acc.get_or_create_session_and_expired(force=True)

    rc, data = get_user_server_list(hm)
    if rc != 0:
        from lib.utils.debug import print_log
        print_log('platform_access..get_user_server_list..error: ', rc)

    result = {
        'server_list': data['server_list'],
        'current_server': data['current_server'],
        'resource': settings.resource,
        'config_resource': settings.get_config_resource(),
        'ks': data['ks'],
        'mk': data['mk'],
    }

    return 0, result


def new_user(hm):
    """ 新建角色

    :param hm:
    :return:
    """
    # name = hm.get_argument('name')
    tpid = hm.get_argument('tpid', 0, is_int=True)
    role = hm.get_argument('role', 1, is_int=True)
    server = hm.get_argument('server')
    account = hm.get_argument('account')
    device_mark = hm.get_argument('device_mark')
    channel = hm.get_argument('pt')
    appid = hm.get_argument('appd', '')
    uuid = hm.get_argument('uuid', '')
    lan = hm.get_argument('lan', 1)
    remote_ip = hm.req.request.headers.get('X-Real-Ip', '') or hm.req.request.remote_ip

    if not role or not server or not account:
        return 'error_100', {}

    # if is_sensitive(name):
    #     return 2, {}  # 名字不合法

    acc = Account.get(account)
    if server in acc.servers:
        return 3, {}  # 该服已有角色

    # 创建uid
    now = int(time.time())
    server_uid_list = ServerUidList()
    uid = server_uid_list.create_uid(server)
    acc.servers[server] = uid
    acc.cur_server = server
    if not acc.tpid:
        acc.set_tpid(tpid)

    bf = BloomFilter()
    new_account = True
    new_device = False
    if not acc.reg_time:
        acc.reg_time = now
    # 每个服单独记录account、device新增
    acc.incr_account_count(server, tpid)
    server_device = '%s%s' % (server, device_mark)
    if device_mark and not bf.is_contains(server_device):
        acc.incr_device_mark_count(server, tpid)
        bf.insert(server_device)
        new_device = True

    sid, expired = acc.get_or_create_session_and_expired(force=True)

    mm = ModelManager(uid)
    if acc.mk:
        mk = acc.mk
    else:
        mk = generate_mk(mm.user.account)
    mm.user.mk = mk
    mm.user.reg_time = now
    mm.user.active_time = now
    mm.user.online_time = now
    mm.user.channel = channel
    mm.user.account = account
    mm.user.account_reg = acc.reg_time
    mm.user.update_session_and_expired(sid, expired)
    mm.user.device = device_mark
    mm.user.is_new = 0
    mm.user.set_tpid(tpid)

    mm.user.role = 0
    mm.user.name = i18n_msg.get('user_name', mm.user.language_sort) + game_config.get_last_random_name(
        mm.user.language_sort)
    mm.user.register_ip = remote_ip
    # 发送等级为1的邮件
    mm.user.send_level_mail(0, 1)

    mm.user.appid = mm.user.APPID_OS_MAPPING.get(appid, 'android')

    mm.user.package_appid = appid
    mm.user.uuid = uuid

    # 记录注册
    regist_users = mm.get_obj_tools('regist_users')
    regist_users.update_regist_status(uid)

    # 首次建号赠送的道具等
    reward = {}
    # for index, config in game_config.initial_data.iteritems():
    #     sort = config.get('sort')
    #     gift = config.get('reward')
    #     if sort == 1:
    #         add_mult_gift(mm, gift, cur_data=reward)
    #     elif sort == 2:
    #         mm.battle_item.groups[1] = {'name': i18n_msg.get(5, mm.user.language_sort), 'group': gift, 'status': 1}
    #         mm.battle_item.save()
    #     elif sort == 3:
    #         pass

    # 测试服，创建指定账号
    test_init(mm, lan)

    # 公测返利
    mm.user.rebate_recharge()

    mm.user.save()
    mm.do_save()
    acc.save()

    hm.mm = mm
    # bdc 日志
    kwargs = {'hm': hm, 'ldt': time.strftime('%F %T'), 'ip': remote_ip}
    if new_account:
        special_bdc_log(mm.user, sort='new_account', **kwargs)
    if new_device:
        special_bdc_log(mm.user, sort='new_device', **kwargs)

    # 上传uc玩家数据
    send_role_data_uc(mm.user)
    # 向360发送玩家角色数据
    # if account.startswith('360'):
    #     from lib.sdk_platform.sdk_360 import send_role_data
    #     from models.server import ServerConfig
    #     sc = ServerConfig.get()
    #     try:
    #         role_data = {
    #             'qid': account.split('_')[1],
    #             'zoneid': 0,
    #             'zonename': sc.config_value[mm.user._server_name]['name'],
    #             'roleid': mm.user.uid,
    #             'rolename': mm.user.name,
    #             'professionid': 0,
    #             'profession': u'无',
    #             'gender': u'无',
    #             'balance': {'balanceid': 0, 'balancename': u'默认', 'balancenum':0},
    #             'vip': 0,
    #             'power': 0,
    #             'rolelevel': mm.user.level,
    #             'partyid': 0,
    #             'partyname': u'无',
    #             'type': 'createRole',
    #             'partyroleid': 0,
    #             'partyrolename': u'无',
    #             'friendlist': u'无',
    #             'friend': u'无',
    #         }
    #         send_role_data(role_data)
    #     except:
    #         from lib.utils.debug import print_log
    #         print_log('new_user..send_role_data to 360..error: ')
    #         pass

    return 0, {
        'uid': uid,
        'reward': reward
    }

    # mm = ModelManager('%s1234567' % server)
    # ul = UserLogic(mm)
    # rc, data = ul.new_user(name, role, server, account, device_mark, channel)
    # if rc != 0:
    #     return rc, {}

    # return 0, data


def test_init(mm, lan):
    """
    测试服，创建指定账号
    :param mm:
    :return:
    """
    # 是否直接跳过引导
    # mm.user.finish_guide()
    if not settings.DEBUG or not mm.user.account.startswith('test'):
        return

    # 跳过新手引导
    mm.user.finish_guide()

    # 战队等级
    level = game_config.initial_account.get('level')
    if level:
        mm.user.level = 90

    # 邮件
    good = game_config.initial_account.get('good')
    if good:
        # 直接给送东西
        add_mult_gift(mm, good)

        # mail_dict = mm.mail.generate_mail(
        #     u'测试道具',
        #     title=u'测试道具',
        #     gift=good,
        # )
        # mm.mail.add_mail(mail_dict)

    # 英雄
    card_config = game_config.initial_account.get('card')
    if card_config:
        # id, 等级，好感，羁绊
        for cid, lv, love_exp, love_lv in card_config:
            mm.card.add_card(cid, lv=lv, love_lv=love_lv, love_exp=love_exp, lan=lan)
        mm.card.save()


def mark_user_login(hm):
    """mark_user_login: 标记用户最近登录，防多设备登录
    args:
        req:    ---    arg
    returns:
        0    ---
    """
    mm = hm.mm
    mm.user.mk += 1
    mm.user.save()

    return 0, {
        'mk': mm.user.mk,
    }


def get_user_server_list(hm, account=None):
    """# login: 交给前端用户的server_list（此步不需要验证）
    args:
        hm:    ---    arg
    returns:
        0    ---
    """
    account = hm.get_argument('account', '') if not account else account
    remote_ip = hm.req.request.headers.get('X-Real-Ip', '') or hm.req.request.remote_ip
    appid = hm.get_argument('appd', '')

    # 英雄互娱给的 渠道id, 0为母包，母包不上线
    tpid = hm.get_argument('tpid', 0, is_int=True)

    # api session验证
    now = int(time.time())
    sid = sid_generate(account, now)

    server_list = ServerConfig.get().server_list(tpid=tpid)
    another_server_list = get_another_list(hm)
    uu = Account.get(account)
    device_mark = hm.get_argument('device_mark', '')
    serve_active_time = []
    # 多点登录限制
    mk = generate_mk(account)
    uu.mk = mk
    if not uu.tpid and tpid:
        uu.set_tpid(tpid)

    uu.save()
    for s in server_list:
        uid = s['uid'] = uu.servers.get(s['server'], '')
        s['level'] = 0
        if uid:
            mm = ModelManager(uid)
            u = mm.user
            s['level'] = u.level
            if u.reg_time:
                serve_active_time.append((s['server'], u.active_time))
                if u.name:
                    # if u.device and u.device == device_mark:
                    #     continue
                    if device_mark:
                        u.device = device_mark
                    u.mk = mk
                    u.save()
    # 合并服务器列表
    if another_server_list:
        server_list.extend(another_server_list)

    if not server_list:
        return 'error_1024', {
            'server_list': server_list,
            'current_server': '',
            'ks': sid,
            'mk': '',
        }

    serve_active_time.sort(key=lambda x: x[1])
    current_server = serve_active_time[-1][0] if serve_active_time else ''
    select_server = get_server_list(server_list, current_server)[0]['server']

    if not Account.check_exist(account):
        return 0, {  # 查无此人
            'server_list': server_list,
            'current_server': select_server,
            'ks': sid,
            'mk': '',
        }

    if another_server_list:
        server_list.sort(key=lambda x: (x['server'] not in ['master', 'public'], -x['sort_id'], x['server']))

    kwargs = {'ip': remote_ip, 'device': device_mark, 'client_os': User.APPID_OS_MAPPING.get(appid, 'android')}
    special_bdc_log(uu, sort='account_login', **kwargs)
    return 0, {
        'server_list': server_list,
        'current_server': select_server,
        'ks': sid,
        'mk': mk,
    }


def get_server_list(server_list, current_server):
    if current_server:
        return [server for server in server_list if server['server'] == current_server]
    new_servers = []
    not_enough_new_servers = []
    for server_id in server_list:
        if server_id['server'] in ['master', 'public']:
            continue
        if game_config.get_config_type(server_id['server']) == 1:
            new_servers.append(server_id)
            server_uid = ServerUid(server_id['server'])
            if server_uid.owned_count() <= 2000:
                not_enough_new_servers.append(server_id)
    if not_enough_new_servers:
        return [random.choice(not_enough_new_servers)]
    if new_servers:
        return [random.choice(new_servers)]
    all_list = server_list[-2:] if len(server_list) >= 2 else server_list
    return [random.choice(all_list)]


def get_another_list(hm, flag=None):
    """
    获取另一个服的服务器列表, 平台之间的合服列表, 参照武娘或超级英雄
    Args:
        hm:
        flag:

    Returns:

    """
    return []
    # from lib.utils import http
    # import json
    #
    # # white_list = settings.KAIQIGU_IP
    # account = hm.get_argument('account', '')
    # # remote_ip = hm.hmuest.headers.get('X-Real-Ip', '') or hm.hmuest.remote_ip
    #
    # # 把腾讯服 新开的服进入的玩家的请求转到金山新服上
    # another_server_list = []
    # # if remote_ip in white_list or settings.ENV_NAME in ['local', 'rg']:
    # if settings.ENV_NAME in ['pub_tencent'] and settings.OPEN_MERGE_SERVER:
    #     merge_server_domain = settings.PLATFORM_MERGE_SERVER_DOMAIN.get(settings.ENV_NAME)
    #     if merge_server_domain:
    #         _platform = account.split('_')[0].lower() if account else ''
    #         # if flag:
    #         #     hm.hmuest.uri = hm.hmuest.uri.replace('method=login', 'method=get_user_server_list')
    #         url = '%s%s' % (merge_server_domain, hm.hmuest.uri)
    #         rc, data = http.get(url)
    #
    #         another_data = json.loads(data)['data']
    #         if 'server_list' in another_data:
    #             another_list = another_data['server_list']
    #         else:
    #             another_list = []
    #
    #         for info in another_list:
    #             # 2016-11-18 01:10:00 之后开启的服可见
    #             if info['open_time'] < 1479402600.0:
    #                 continue
    #             # if info['server'] not in game_config.server_config:
    #             #     continue
    #
    #             name_mapping = game_config.server_config.get(info['server'], '')
    #             if name_mapping:
    #                 info['server_name'] = name_mapping.get(_platform, info['server_name'])
    #             #     info['server_name'] = name_mapping['msdk']
    #             another_server_list.append(info)
    #
    # return another_server_list


def platform_access(hm):
    """ 平台登录验证

    :param hm:
        pre_platform: 验证平台前缀, account前缀
        channel: 渠道
    :return:
    """
    channel = hm.get_argument('channel', 'cmge')

    account, data, channel = login_verify(hm, channel)

    result = {}

    if data is None:
        return 1, result

    if isinstance(data, dict):
        result.update(**data)
    else:
        result['openid'] = data
    result.update(
        notify_url=settings.get_payment_callback_url(channel),  # 支付回调地址
        order_url=settings.get_payment_order_url(channel),  # 获取定单地址
    )

    # acc = Account.get(account)
    # if not acc.cur_server and not acc.servers:
    #     server_uid_list = ServerUidList()
    #     server, uid = server_uid_list.create_uid()
    #
    #     acc.servers[server] = uid
    #     acc.cur_server = server
    #
    # else:
    #     uid = acc.servers[acc.cur_server]
    #
    # result['user_token'] = uid
    #
    # sid, expired = acc.get_or_create_session_and_expired(force=True)
    #
    # now = int(time.time())
    #
    # hm.mm = hm.mm_class(uid)
    # if hm.mm.user.inited:
    #     hm.mm.user.reg_time = now
    #     hm.mm.user.channel = channel
    #     hm.mm.user.account = account
    #     # 记录注册
    #     regist_users = hm.mm.get_obj_tools('regist_users')
    #     regist_users.update_regist_status(uid)
    #
    # hm.mm.user.mk += 1
    # hm.mm.user.active_time = now
    # hm.mm.user.update_session_and_expired(sid, expired)
    #
    # hm.mm.user.save()
    # acc.save()

    # long_ip, long_port = settings.long_addr(hm.mm)
    #
    # result['long_ip'] = long_ip
    # result['long_port'] = long_port
    # result['mk'] = hm.mm.user.mk
    result['resource'] = settings.resource
    result['config_resource'] = settings.config_resource

    rc, data = get_user_server_list(hm, account)
    if rc != 0:
        from lib.utils.debug import print_log
        print_log('platform_access..get_user_server_list..error: ', rc)
    result.update(data)

    return 0, result


def check_session(hm):
    """
    检查session,给c++服务器提供验证接口
    :param hm:
    :return:
    """
    mm = hm.mm

    mk = hm.get_argument('mk')
    sid = hm.get_argument('sid')

    if mm.user.mk != mk or mm.user.session_expired(sid):
        return 1, {}

    return 0, {}


def notice(hm):
    lan = hm.get_argument('lan', '1')
    config = copy.deepcopy(game_config.welfare_notice)
    info = {}
    lan = MUITL_LAN[lan]
    now = int(time.time())
    for k, v in config.iteritems():
        if not v['start_time'] or not v['end_time']:
            continue
        start_time = str2timestamp(v['start_time'])
        end_time = str2timestamp(v['end_time'])
        if start_time <= now <= end_time:
            content = game_config.get_language_config(lan)[v['des']]
            name = game_config.get_language_config(lan)[v['name']]
            info[k] = v
            info[k]['des'] = content
            info[k]['name'] = name
    return 0, info
