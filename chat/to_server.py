#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import socket
import time
import json

import settings
from lib.utils import salt_generator


def send_to_all(msg_dict, server_name):
    """
    聊天发送系统消息
    :param msg_dict: {
        'message_id': mid,
        'uid': uid,
        'name': name,
        'target1': target1,     # 卡牌档次
        'target2': target2,     # 卡牌配置id
    }
    :param server_name:
    :return:
    """
    s = get_socket(server_name)
    data = {"level": 1, "combat": 1, "sign": "", "kqgFlag": "system", "guild": "",
            "uid": "", "guild_id": "", "time": 0, "vip": 0, "name": "", "role": 1, "msg": "", "server": server_name}
    # data = {"kqgFlag": "system", "server": server_name, "msg": ""}
    data.update(msg_dict)
    data['sign'] = make_sign(data['uid'])
    msg = '<xml><content>%s</content></xml>' % json.dumps(data)
    s.send(msg)
    s.close()


def make_sign(uid):
    """

    :return:
    """
    return '%s-%s-%s' % (uid, int(time.time()), salt_generator())


def get_socket(server_name, timeout=1):
    addr = get_socket_addr(server_name)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect(addr)

    return s


def get_socket_addr(server_name):
    server_config = settings.SERVERS[server_name]
    host = server_config['chat_ip']
    port = int(server_config['chat_port'])
    addr = (host, port)

    return addr


def receive_data(s):
    data = ''
    while 1:
        try:
            data_str = s.recv(1000000)
            data += data_str
        except Exception, e:
            print e
            break
    return data


def get_content_msg(command, server_name):
    """
    获取聊天数据
    :param command: 'get_content_msg@world@gtt1'
    :param server_name:
    :return:
    """
    s = get_socket(server_name, timeout=2)
    s.send(command)
    data_str = receive_data(s)
    s.close()

    index = data_str.rfind('</content></xml>')
    if index == -1:
        data = '[]'
    else:
        data = data_str[:index+17] + ']'

    data = json.loads(data)

    return data


def delete_content_msg(command, server_name):
    """
    删除聊天数据
    :param command: 'delete_content_msg@world@gtt1@["xxxx", "xxxx"]'
    :param server_name:
    :return:
    """
    s = get_socket(server_name)
    s.send(command)
    s.close()


if __name__ == '__main__':
    server = 'gtt1'
    msg_dict = {
        'message_id': 1,
        'uid': 'gtt11234567',
        'name': 'test_system',
        'target1': 1,  # 卡牌档次
        'target2': 1,  # 卡牌配置id
    }
    def get_socket_addr(*args):
        return ('192.168.1.9', 9090)

    send_to_all(msg_dict, server)
