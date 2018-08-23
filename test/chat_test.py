#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import socket
import json
import time

CONTENT = '<xml><length>359</length><content>%s</content></xml>'

port = 9999
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

msg_data = {
    'uid': 'gtt11234567',
    'guild_id': '',
    'game_id': '',
    'vip': 0,
    'domain': '',
    'team_id': '',
    'sid': '',
    'device_mark': '',
    'device_mem': '',
    'kqgFlag': 'first'
}


def demo_first():
    msg_data['uid'] = 'gtt11234568'
    msg = CONTENT % json.dumps(msg_data)
    s.sendall(msg)


def demo1():
    msg = CONTENT % json.dumps(msg_data)
    s.sendall(msg)
    time.sleep(1)
    msg_data['kqgFlag'] = 'world'
    msg = CONTENT % json.dumps(msg_data)
    s.sendall(msg)

    print 'ssssssss', s.recv(10240)
    # s.close()

if __name__ == "__main__":
    demo1()
