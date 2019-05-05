#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from gevent import monkey

monkey.patch_all()

import os
import sys
import traceback
import signal
import psutil
import socket
import time
import gevent
from gevent.server import StreamServer
import json
import re

import settings

env = sys.argv[1]
server_name = sys.argv[2]
settings.set_env(env, server_name)
settings.ENVPROCS = 'chat'

from lib.utils.debug import print_log
from chat.client import Client, ClientManager, get_pub_sub, channel_name, publish_to_other_server
from chat.content import ContentFactory
from lib.utils.encoding import force_str
from lib.utils import sid_generate, get_timestamp_from_sid
from lib.utils.zip_date import dencrypt_data, encrypt_data
from lib.core.environ import ModelManager
from lib.db import get_redis_client
from models.user import User as UserM

# HOST = settings.SERVERS[settings.SERVICE_NAME]['chat_ip']
PORT = settings.SERVERS[[s for s in settings.SERVERS if s != 'master'][0]]['chat_port']

# 简单获取本机ip
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostbyname('www.baidu.com'), 80))
# HOST = s.getsockname()[0]
# s.close()
# HOST = settings.SERVERS[sorted(settings.SERVERS.keys())[0]]['chat_ip']
HOST = '0.0.0.0'
# HOST = '192.168.1.100'
# define("port", default=9999, help="run on the given port", type=int)
# options.parse_command_line()


POOLNUM = 1000
BUFFSIZA = 128 * 2
MAX_BUFFER_SIZE = 1024 * 4
messages_cache = {}  # 缓存最近 几条对话
MESSAGE_CACHE_SIZE = 50  # 缓存对话 数量

GAG_UIDS = []  # 禁言的uid

GAG_MSG_SWICTH = False


def get_default_msg():
    return '<xml><length>359</length><content>{"inputStr":"尊敬的英雄们：近期因为聊天服务器出现故障，导致部分捣乱分子可以通过非法手段冒名其他英雄发送聊天消息，我们正在紧急修复。修复期间暂时关停聊天服务器，对您造成的不便我们深表歉意。","data":{},"dsign":"1430753055","avatarID":"1","vip":0,"level":1,"kqgFlag":"system"}</content></xml>'


process = psutil.Process(os.getpid())

try:
    get_memory_info = process.memory_info
except:
    get_memory_info = process.get_memory_info


def get_datetime_str():
    return time.strftime('%F %T')


def handle_channel_message(message):
    """处理订阅的消息，发送给对应的用户"""
    pid = os.getpid()
    data = dencrypt_data(message['data'])
    if settings.DEBUG:
        print_log(pid, data)
    if message['type'] == 'message':
        try:
            chat_info = data['chat_info']
            if pid == data['pid']:
                pass
                # print 'owner message, chat_info: ', chat_info
                # return

            send_to_other_client(data['client_info'], chat_info)

        except Exception, e:
            tb = traceback.format_exc()
            print e.message, tb
            return

            # todo 发送给client


# 通过redis pubsub 与其它chat server通信
ps = get_pub_sub()
ps.subscribe(channel_name, **{channel_name: handle_channel_message})
ps.run_in_thread()

client_manager = ClientManager()
content_factory = ContentFactory(settings.chat_config)


def request_handler(client_socket, addr):
    global messages_cache

    now = int(time.time())
    client = Client(client_socket, addr)
    client_manager.add_client(client)

    client_manager.lose_time_out_clients(now)

    print_log('[%s]' % get_datetime_str(), 'connected from %s:%s' % addr, 'client_socket_fd:', client.fileno)
    print_log('clients_num :', client_manager.get_client_count())

    while True:
        # 注意, 正式环境禁止启动此函数
        if settings.DEBUG:
            # 重启先加载时间
            from lib.utils.change_time import debug_sync_change_time
            debug_sync_change_time()

        try:
            data = client_socket.recv(BUFFSIZA)
        except:
            # print_log(222222, 'try raise line:89', client.fileno, client.ip, client.uid)
            client_manager.lose_client(client)
            break

        if not data:
            print_log('[%s]' % get_datetime_str(), 'client %s:%s disconnected' % addr,
                      'flag: %s, %s' % (data, type(data)), client.ip)
            client_manager.lose_client(client)
            print_log('clients_num :', client_manager.get_client_count())
            break

        if 'get_content_msg@' in data.strip().lower():
            "get_content_msg@world@gtt1"
            _, flag, server = data.strip().lower().split('@')
            if flag == 'all_world':
                server = 'chat'
            content = content_factory.get(content_factory.MAPPINGS[flag], server)
            client_socket.sendall('''%s''' % json.dumps(content.msgs))
            continue

        if 'delete_content_msg@' in data.strip().lower():
            'delete_content_msg@world@gtt1@["xxx", "xxx"]'
            _, flag, server, sign_ids_str = data.strip().lower().split('@')
            try:
                sign_ids = json.loads(sign_ids_str)
            except:
                sign_ids = []
            if flag == 'all_world':
                server = 'chat'
            content = content_factory.get(content_factory.MAPPINGS[flag], server)
            msgs = content.msgs
            for msg in msgs[:]:
                re_result = re.findall('"sign".*?([\w\d-]+)', msg)
                if not any(re_result):
                    continue
                s = re_result[0]
                if s in sign_ids:
                    msgs.remove(msg)
            continue

        if data.strip().lower() == 'check':
            now = int(time.time())
            client_socket.sendall(str(get_memory_info()) + '|')
            client_socket.sendall('\nclients_num : %s;' % client_manager.get_client_count())
            client_socket.sendall('\nper_client_connet_time: "[(fileno, uid, game_id, '
                                  'guild_id, server_name, vip, domain, team_id, live_time, ip)]--> %s";' %
                                  str(sorted([(x, y.uid, y.game_id, y.guild_id, y.server_name,
                                               y.vip, y.domain, y.team_id, now - y.ttl, y.ip)
                                              for x, y in client_manager._clients.iteritems()],
                                             key=lambda x: x[1], reverse=True)))
            client_socket.sendall('\n')
            continue

        if data.strip().lower() == 'check_contents':
            client_socket.sendall(str(get_memory_info()) + '|' + str(id(content_factory)))
            client_socket.sendall('\ncontents : %s;' %
                                  repr([content.__dict__ for content in content_factory._contents.itervalues()]))
            client_socket.sendall('\n')
            continue

        if data.strip().lower() == 'quit':
            client_manager.lose_client(client)
            break

        data_str = data.strip().lower()
        if data_str.startswith('kill '):
            _, fileno = data_str.split(' ')
            client_manager.lose_client_by_fileno(int(fileno))
            continue

        # buffer超了指定大小还未找到规定格式的数据，主动断开连接
        if len(client.buffer) >= MAX_BUFFER_SIZE:
            print_log('lose_client......buffer max')
            client_manager.lose_client(client)
            break

        info = client.parse(data)

        if not info:
            continue

        if not info.get('uid'):
            print_log('lose_client......not uid', client.fileno, client.ip)
            client_manager.lose_client(client)

        # if info.get('uid') not in ['gtt11542725', 'gtt13832261', 'gtt16092309']:
        #     continue

        # print_log(1111111111111, info, client.fileno)

        tp = info['kqgFlag']
        if tp == 'first':
            try:
                mm = ModelManager(info.get('uid'))
            except:
                print_log('lose_client......ModelManager raise')
                client_manager.lose_client(client)
                break
            #
            # if u.session_expired(info.get('ks')) or (u.device_mark and u.device_mark != info.get('device_mark'))\
            #         or (u.device_mem and u.device_mem != info.get('device_mem')):
            #     client_manager.lose_client(client)
            #     continue

            # 封号信息
            ban_info = mm.user.get_ban_info()
            ban_chat = mm.user.is_ban_chat()
            if ban_info or ban_chat:
                client_manager.lose_client(client)
                break

            client.init_info(info.get('uid'), info.get('guild_id', ''),
                             info.get('game_id', ''), info.get('vip', 0),
                             info.get('domain', ''), info.get('team_id', ''),
                             addr[0], info.get('device_mark'), info.get('device_mem'),
                             info.get('lan', 1))
            client_manager.add_server_client(client)
            if GAG_MSG_SWICTH:
                client.socket.sendall(force_str(get_default_msg()))
            if not GAG_MSG_SWICTH:
                # 系统
                content = content_factory.get(content_factory.MAPPINGS['system'], client.server_name)
                msgs = content.show()
                if msgs:
                    client.socket.sendall(''.join(msgs))

                # 全服
                content_all_world = content_factory.get(content_factory.MAPPINGS['all_world'], 'chat')
                msgs = content_all_world.show(uid=client.uid)
                if msgs:
                    client.socket.sendall(''.join(msgs))

                # 本服
                content = content_factory.get(content_factory.MAPPINGS['world'], client.server_name)
                msgs = content.show(uid=client.uid)
                if msgs:
                    client.socket.sendall(''.join(msgs))

                # 好友
                msgs = []
                content_friend = content_factory.get(content_factory.MAPPINGS['friend'], client.server_name, '')
                for friend_uid in content_friend.get_friend_mapping(client.uid):
                    if client.uid < friend_uid:
                        uid_key = '%s_%s' % (client.uid, friend_uid)
                    else:
                        uid_key = '%s_%s' % (friend_uid, client.uid)
                    content_friend = content_factory.get(content_factory.MAPPINGS['friend'], client.server_name,
                                                         uid_key)
                    m = content_friend.show()
                    msgs += m
                # content_factory.delete(content_factory.MAPPINGS['friend'], client.server_name, client.uid)
                if msgs:
                    client.socket.sendall(''.join(msgs))

                # 公会
                if client.guild_id:
                    content_guild = content_factory.get(content_factory.MAPPINGS['guild'], client.server_name,
                                                        client.guild_id)
                    msgs = content_guild.show(uid=client.uid)
                    if msgs:
                        client.socket.sendall(''.join(msgs))

                client_manager.lose_repeat_clients(client)
            continue

        if tp == 'update':
            client.update_info(info.get('guild_id'), info.get('domain'), info.get('team_id'))
            continue

        if GAG_MSG_SWICTH:
            continue

        if client.uid in GAG_UIDS:
            continue

        if tp != 'system':
            mm = ModelManager(client.uid)
            u = mm.user
            # 封号信息
            ban_info = u.get_ban_info()
            ban_chat = u.is_ban_chat()
            if ban_info or ban_chat:
                client_manager.lose_client(client)
                break
            # TODO 后续需要加
            # if not settings.SESSION_SWITCH and u.ip and u.ip != client.ip:
            #     continue

            account = u.account
            ks = info.get('ks')

            timestamp = get_timestamp_from_sid(ks)
            session = sid_generate(account, str(timestamp))
            expired = timestamp + settings.SESSION_EXPIRED
            session_expired = (ks != session or (int(expired) < int(time.time())))

            # TODO 后续需要加
            # if settings.SESSION_SWITCH and (session_expired
            #                                 or (u.device_mark and u.device_mark != info.get('device_mark'))
            #                                 or (u.device_mem and u.device_mem != info.get('device_mem'))):
            #     continue
            #
            # if u.is_ban:
            #     continue

            # 聊天限制次数
            if tp in ['all_world', 'world']:
                rc = u.add_chat_times(tp)
                if not rc:
                    continue

        else:
            client.server_name = info['server']

        sendToUid = info.get('sendToUid', '')
        next_flag = info.get('next')
        if next_flag and tp in ['all_world', 'world', 'system', 'guild', 'friend'] and next_flag in [1, 2]:
            if tp == 'guild' and client.guild_id:
                content = content_factory.get(content_factory.MAPPINGS[tp], client.server_name, client.guild_id)
            elif tp == 'friend' and sendToUid:
                content = content_factory.get(content_factory.MAPPINGS[tp], client.server_name, '')
            else:
                content = content_factory.get(content_factory.MAPPINGS[tp], client.server_name)

            if tp == 'friend':
                msgs = []
                for friend_uid in content.get_friend_mapping(client.uid):
                    if client.uid < friend_uid:
                        uid_key = '%s_%s' % (client.uid, friend_uid)
                    else:
                        uid_key = '%s_%s' % (friend_uid, client.uid)
                    content = content_factory.get(content_factory.MAPPINGS[tp], client.server_name, uid_key)
                    m = content.show(next_flag)
                    msgs += m
            else:
                msgs = content.show(next_flag)
            if msgs:
                client.socket.sendall(''.join(msgs))
            continue

        # 自己的信息发回给自己，前端统一处理服务端的推送
        gevent.joinall([gevent.spawn(client.socket.sendall, client.msg)])
        # publish to other chat sever node
        publish_to_other_server(client, info)


def send_to_other_client(client, info):
        """
        :param client 发送方信息: kqgFlag为 first 标记时候发送的信息，玩家uid， guild_id等
                    {'uid': '', 'guild_id': ''}
        :param info: 消息详情
        :return:
        """
        if isinstance(client, dict):
            client = Client.loads(client)

        if not client.msg:
            json_msg_str = json.dumps(info)
            client.msg = client.format_str % (len(json_msg_str), json_msg_str)

        tp = info['kqgFlag']
        sendToUid = info.get('sendToUid', '')

        con_name = content_factory.MAPPINGS.get(tp)
        if con_name and con_name not in content_factory.IGNORE:
            if tp == 'all_world':
                content = content_factory.get(con_name, 'chat')
            else:
                content = content_factory.get(con_name, client.server_name)
            content.add(client.msg)
            content.save()

        receivers = []
        for _fd in client_manager._clients.keys():
            _client = client_manager._client.get(_fd)
            if not _client:
                continue
                # for _fd, _client in client_manager.get_client_by_server_name(client.server_name).iteritems():
            # if _fd == client.fileno:
            #     continue
            # 判断消息是否需要发送  用gevent.spawn 处理
            # print_log(444444444444, _fd)

            # 屏蔽列表
            if client.uid in _client.get_blacklist():
                # receivers.append(gevent.spawn(client.socket.sendall, client.msg))
                continue

            if tp in ['all_world', 'world', 'system']:  # 世界, 本服, 系统
                receivers.append(gevent.spawn(_client.socket.sendall, client.msg))
            elif tp == 'guild':  # 公会
                if _client.guild_id and _client.guild_id == client.guild_id:
                    # print_log(333333333333333)
                    receivers.append(gevent.spawn(_client.socket.sendall, client.msg))
            elif tp == 'friend' and _client.uid == sendToUid:  # 好友
                receivers.append(gevent.spawn(_client.socket.sendall, client.msg))
                # receivers.append(gevent.spawn(client.socket.sendall, client.msg))
                break
            elif tp == 'guild_war':  # 工会战
                if _client.guild_id and client.guild_id:
                    receivers.append(gevent.spawn(_client.socket.sendall, client.msg))
            elif tp in ['rob', 'escort']:  # 运镖, 打劫
                if client.domain and client.domain == _client.domain:
                    receivers.append(gevent.spawn(_client.socket.sendall, client.msg))
            elif tp == 'team':  # 队伍
                if client.team_id and client.team_id == _client.team_id:
                    receivers.append(gevent.spawn(_client.socket.sendall, client.msg))

        # 私聊缓存
        if tp == 'friend' and sendToUid:  # and not receivers:
            to_user = UserM.get(sendToUid, from_req=False)
            mm = ModelManager(client.uid)
            mm.friend.add_newest_uid(sendToUid, is_save=True)
            if client.uid not in to_user.blacklist:
                # if not receivers:
                #     receivers.append(gevent.spawn(client.socket.sendall, client.msg))
                if client.uid < sendToUid:
                    uid_key = '%s_%s' % (client.uid, sendToUid)
                else:
                    uid_key = '%s_%s' % (sendToUid, client.uid)
                content = content_factory.get(content_factory.MAPPINGS[tp], client.server_name, uid_key)
                content.add(client.msg)
                content.add_friend_mapping(client.uid, sendToUid)
                content.save()

        # 公会聊天缓存
        elif tp == 'guild' and client.guild_id:
            # print_log('guild', client.guild_id)
            content = content_factory.get(content_factory.MAPPINGS[tp], client.server_name, client.guild_id)
            content.add(client.msg)
            content.save()

        gevent.joinall(receivers)


def close():
    content_factory.save()


def socket_server(host, port):
    print_log(__file__, '[%s] start handler_client server on port %s:%s' % (get_datetime_str(), host, port))
    server = StreamServer((host, int(port)), request_handler, spawn=10000)
    gevent.signal(signal.SIGTERM, close)
    gevent.signal(signal.SIGINT, close)
    server.serve_forever()


if __name__ == '__main__':
    socket_server(HOST, PORT)
