# coding: utf-8

import cPickle as pickle
import msgpack
import settings


def dencrypt_data(result):
    if not result:
        return result
    # 2018.01.22 改成msgpack序列化数据，兼容slg 代码
    protocol = result[:2]
    if protocol == '\x01\x01':
        return msgpack.loads(result[2:], encoding='utf-8')
    elif protocol == '\x01\x02':
        decode_data = result[2:].decode("zip")
        return msgpack.loads(decode_data, encoding='utf-8')
    # 2018.01.22 改成msgpack序列化数据，兼容slg 代码
    elif result[0] == '\x01':
        decode_data = result[1:].decode("zip")
        return pickle.loads(decode_data)
    else:
        return pickle.loads(result)


def encrypt_data(result, protocol=pickle.HIGHEST_PROTOCOL):
    # s = pickle.dumps(result, protocol)
    # if settings.ZIP_COMPRESS_SWITCH and settings.MIN_COMPRESS > 0 and len(s) >= settings.MIN_COMPRESS:
    #     s = "\x01" + s.encode("zip")

    # 2018.01.22 改成msgpack序列化，兼容slg 代码
    s = msgpack.dumps(result)
    if settings.ZIP_COMPRESS_SWITCH and settings.MIN_COMPRESS > 0 and len(s) >= settings.MIN_COMPRESS:
        s = "\x01\x02" + s.encode("zip")
    else:
        s = '\x01\x01' + s
    return s


def encrypt_data_by_pickle(result, protocol=pickle.HIGHEST_PROTOCOL):
    s = pickle.dumps(result, protocol)
    if settings.ZIP_COMPRESS_SWITCH and settings.MIN_COMPRESS > 0 and len(s) >= settings.MIN_COMPRESS:
        s = "\x01" + s.encode("zip")
    return s
