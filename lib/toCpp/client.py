#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import random
from select import select
import json
import msgpack
import struct
from socket import AF_INET, SOCK_STREAM
import socket
# from redis.exceptions import (
#     ConnectionError,
#     TimeoutError,
# )

import settings


class Client(object):
    BUFSIZE = 40960

    def __init__(self, host, port, timeout=2, is_zip=0):
        """
        select([c._socket], [], [], 0)

        :param host:
        :param port:
        :param timeout:
        :param: is_zip:
                    0:不处理
                    1:json+zip
                    2:msgpack+zip
        """
        self.addr = (host, port)
        self.timeout = timeout
        self.is_zip = is_zip
        self._socket = None
        self.connect()

    def reconnect(self):
        """重连"""
        self.disconnect()
        self.connect()

    def connect(self):
        if self._socket:
            return

        try:
            s = socket.socket(AF_INET, SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect(self.addr)
            self._socket = s

            b = self.first_pack()
            self._socket.sendall(b)

        except socket.error:
            self.disconnect()

    def disconnect(self):
        if self._socket:
            self._socket.close()
            self._socket = None

    def encrypt_data(self, result):
        """
        加密数据
        :param result:
        """
        # if self.zip_open or \
        #         (self.zip_open is None and settings.ZIP_COMPRESS_SWITCH and 0 < settings.MIN_COMPRESS <= len(result)):
        #     result = result.encode("zip")
        #     is_zip = 1

        if self.is_zip == 1:
            s = json.dumps(result).encode('zip')
        elif self.is_zip == 2:
            s = msgpack.dumps(result).encode('zip')
        else:
            s = result

        return s

    def dencrypt_data(self, is_zip, result):
        """
        解密数据
        :param is_zip:
        :param result:
        :param is_zip:
        :return:
        """
        if is_zip == 1:
            s = json.loads(result.decode('zip'))
        elif is_zip == 2:
            s = msgpack.loads(result.decode('zip'))
        else:
            s = result

        return s

    def send(self, cmd, func_id, data):
        """
        发送的格式[cmd, is_zip, data] --> msgpack
        :param cmd: 对应slg服务器的协议号
        :param func_id: slg服务器处理函数名字
        :param data: 发送数据
        :return:
        """
        self.connect()
        if not self._socket:
            return None, {}

        self.flush_cache()

        a = self.pack(cmd, func_id, data)
        try:
            self._socket.sendall(a)
        except Exception:
            self.reconnect()
            if not self._socket:
                return None, {}
            try:
                self._socket.sendall(a)
            except Exception:
                self.disconnect()
                return None, {}

        return self.getData()

    def first_pack(self):
        s = 'REGSCLIENT'
        data = 2 << 24 | len(s)
        data = struct.pack('!i', data)
        return data + s

    def pack(self, cmd, func_id, data):
        # data = json.dumps(data)
        zip_data = self.encrypt_data(data)

        sendstr = msgpack.dumps([cmd, func_id, self.is_zip, zip_data])
        length = len(sendstr)
        data = struct.pack('!i', length)
        data += sendstr

        return data

    def unpack(self, data):
        try:
            get_data = msgpack.loads(data)
        except Exception:
            print 'error unpack', repr(data)
            return None, None

        if len(get_data) != 4:
            print 'error data', get_data
            return None, None

        cmd, func_id, is_zip, zip_data = get_data[0], get_data[1], get_data[2], get_data[3]
        ret_data = self.dencrypt_data(is_zip, zip_data)

        return cmd, ret_data

    def flush_cache(self):
        """清空缓存"""
        while self._socket and any(select([self._socket], [], [], 0)):
            a = self._socket.recv(self.BUFSIZE)
            if not a:
                self.reconnect()
                break

    def getOneData(self):
        """解析一条完整数据"""
        d_body = ''
        len2 = 0
        length = 0
        # cmd, data = None, None

        try:
            # 解析数据头
            d_header = self._socket.recv(4)
            length = struct.unpack('!i', d_header)[0]

            while len2 < length:
                d2 = self._socket.recv(length - len2)
                d_body += d2
                len2 += len(d2)

        except Exception:
            print 'error getOneData', length, repr(d_body)
            self.disconnect()
            # return None, None

        cmd, data = self.unpack(d_body)

        return cmd, data

    def getData(self):
        """读取数据"""

        cmd, data = self.getOneData()
        while (not data and self._socket and any(select([self._socket], [], [], 0))):
            cmd, data = self.getOneData()

        return cmd, data
        #
        #
        # d = ''
        # len2 = 0
        #
        # try:
        #     # 解析数据头
        #     d1 = self._socket.recv(4)
        #     length = struct.unpack('!i', d1)[0]
        #
        #     while len2 < length:
        #         d2 = self._socket.recv(length-len2)
        #         d += d2
        #         len2 += len(d2)
        # except Exception:
        #     self.disconnect()
        #     return None, None
        # # except socket.timeout:
        # #     raise TimeoutError("Timeout reading from socket")
        # # except socket.error:
        # #     e = sys.exc_info()[1]
        # #     raise ConnectionError("Error while reading from socket: %s" % (e.args,))
        #
        # print 222222, select([self._socket], [], [], 0)
        # # print 333333, nn
        # try:
        #     cmd, data = self.unpack(d)
        # except Exception:
        #     print 66666, repr(d1+d)
        #
        # return cmd, data


def get_rpc_client():
    """
    获取连接rpc的客户端
    :return:
    """
    # todo 临时用python分发，之后改成c++多线程
    if settings.ENV_NAME in settings.RANDOM_CLIENT_PLATFORM:
        return get_random_client()

    if not settings.RPC_CLIENT:
        if not settings.RPC_SERVER_ADDR:
            return None

        client = Client(*settings.RPC_SERVER_ADDR, is_zip=1)
        settings.RPC_CLIENT = client

    return settings.RPC_CLIENT


def get_random_client():
    addr_list = settings.RPC_SERVER_ADDR_LIST
    if not addr_list:
        return None

    index = random.choice(range(len(addr_list)))
    if index not in settings.RPC_CLIENT_DICT:
        addr = addr_list[index]
        client = Client(*addr, is_zip=1)
        settings.RPC_CLIENT_DICT[index] = client

    return settings.RPC_CLIENT_DICT[index]


if __name__ == '__main__':
    addr = ('localhost', 8001)
    client = Client(*addr, is_zip=1)
    client.send(100, 'test', {'1': 1})
