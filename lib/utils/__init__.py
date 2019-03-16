# coding: utf-8

VERSION = (0, 0, 1)

import json
import math
import copy
import debug
import socket
import fcntl
import struct
import time
import datetime
import bisect
import random
import string
import psutil
import os
import hashlib
import logging
from collections import defaultdict, OrderedDict
import msgpack
import re

sys_random = random.SystemRandom()

chars = string.ascii_letters + string.digits


class LRUCache(object):
    def __init__(self, max_size=5):
        self.max_size = max_size
        self.cache = OrderedDict()

    def set(self, key, value):
        if self.cache.has_key(key):
            self.cache.pop(key)
        elif len(self.cache) == self.max_size:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def get(self, key):
        if self.cache.has_key(key):
            value = self.cache.pop(key)
            self.cache[key] = value
        else:
            value = None
        return value

    def __len__(self):
        return len(self.cache)


def salt_generator(size=6):
    return ''.join(random.choice(chars) for x in xrange(size))


def get_it(probability):
    """ 判断概率是否命中

    随机1-100判断当前指定的概率是否符合要求
    
    Args:
       probability: 指定概率

    Returns:
       是否命中
    """

    return sys_random.randint(0, 100) <= probability

# def rand_weight(weight, weights, goods):
#    """随机一个值
#
#    Args:
#       weight: max（weights）
#       weights：从小到大 的权重列表
#       goods: 跟weights对应的列表
#
#    Returns:
#       随机出的值
#    """
#
#    w = sys_random.randint(0, weight)
#    idx = bisect.bisect_left(weights, w)
#
#    return goods[idx]


def to_json(obj):
    """# to_json: 将一些特殊类型转换为json
    args:
        obj:    ---    arg
    returns:
        0    ---
    """
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(repr(obj) + ' is not json seralizable')


def json_dumps(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), encoding="utf-8", default=to_json)


def md5(s):
    """# md5: docstring
    args:
        s:    ---    arg
    returns:
        0    ---    
    """
    return hashlib.md5(str(s)).hexdigest()


def sid_generate(account, cur_time, long_value=False):
    """
     api session验证 根据帐号标识和时间戳生成md5
    :param account:
    :return:
    """
    session = md5('%s%s' % (account, str(cur_time)))
    if not long_value:
        session = session[:10]

    return ''.join([session, str(cur_time)])


def get_timestamp_from_sid(sid):
    """
    从api session生成的md5分解出时间戳
    :param sid:
    :return:
    """
    if not sid:
        return 0

    ts = sid[-10:]
    return int(ts) if ts.isdigit() else 0


# def weight_choice(l, index= -1):
#     """# weight: d
#     args:
#         l:    ---    [       # 权重
#                         [1,1,10],
#                         [1,1, 20]
#                      ]
#         index: 指定权重数字在数组中的位置
#     returns:
#         0    ---
#     """
#     sum_n = sum([i[index] for i in l])
#     w = sys_random.randint(0, sum_n - 1)
#
#     data = []
#     for ind, value in enumerate(l):
#         data.extend([ind] * value[index])
#
#     random.shuffle(data)
#
#     return l[data[w]]
#
#     # ll = sorted(l, key=lambda x: x[index])
#     # length = len(ll)
#     # i = 0
#     # while  i < length and ll[i][index] < w:
#     #     i += 1
#     # return ll[i-1]
#
#     # weight = 0
#     # for x in ll:
#     #     weight += x[index]
#     #     if weight >= w:
#     #         return x


def weight_choice(l, index=-1):
    """# weight: d
    args:
        l:    ---    [       # 权重
                        [1,1,10],
                        [1,1, 20]
                     ]
        index: 指定权重数字在数组中的位置
    returns:
        0    ---
    """
    sum_n = sum([i[index] for i in l])
    w = sys_random.randint(1, sum_n)
    ll = sorted(l, key=lambda x: x[index])
    # length = len(ll)
    # i = 0
    # while  i < length and ll[i][index] < w:
    #     i += 1
    # return ll[i-1]

    weight = 0
    for x in ll:
        weight += x[index]
        if weight >= w:
            return x


def weight_choice_list(l):
    """

    :param l: [1,2,3,4]
    :return: index, x
    """
    sum_n = sum([i for i in l])
    w = sys_random.randint(1, sum_n)
    ll = sorted(l)

    weight = 0
    for index, x in enumerate(ll):
        weight += x
        if weight >= w:
            return index, x


def not_repeat_weight_choice(population, num=1, index=-1):
    if not population or not num:
        return []

    t_sum_n = sum([i[index] for i in population])

    data = []
    for ind, value in enumerate(population):
        data.extend([ind] * value[index])
    random.shuffle(data)

    goods = []
    for _ in xrange(num):
        w = sys_random.randint(0, t_sum_n - 1)
        i = data[w]
        item = population[i]
        sum_n = item[index]
        t_sum_n -= sum_n
        goods.append(item)
        for tmp in xrange(sum_n):
            data.remove(i)

    return goods


def not_repeat_weight_choice_2(population, num=1, index=-1):
    """
    不重复的,性能修改版
    :param population:
    :param num:
    :param index:
    :return:
    """
    if not population or not num:
        return []

    goods = []
    population_copy = copy.deepcopy(population)
    for _ in xrange(num):
        p = weight_choice(population_copy, index)
        goods.append(p)
        population_copy.remove(p)

    return goods


STR_SOURCE = '23456789abcdefghijkmnpqrstuvwxyz'
def rand_string(length, s=''):
    """# rand_string: 随机生成一个长度的字符串
    args:
        length:    ---    arg
    returns:
        0    ---    
    """
    if not s:
        s = STR_SOURCE
    l = []
    for i in xrange(length):
        l.append(s[random.randint(0, len(s) - 1)])
    return ''.join(l)

def get_datetime_str(dt=None):
    dt = dt or datetime.datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def round_float_or_str(num):
    """ 数据向上取整

    :param num: 需要转换的数据(float|str)
    :return:
    """
    return round(float(num))


def generate_rank_score(score, now=None, flag=False):
    """ 生成排名的积分

    :param score: 需要转换的积分
    :param now: 当前的时间搓
    :param flag: False:减法，True:加法
    :return:
    """
    if not flag:
        sub = -1
    else:
        sub = 1
    now = now if now else time.time()
    return score + sub * now / 10**13


def generate_rank_time(score):
    """ 根据排名的积分生成当时的时间

    :param score: 需要转换的积分
    :param now: 当前的时间搓
    :return:
    """
    return (round(score) - score) * 10**13


def get_local_ip(ifname="eth0"):
    """ 获取本地内网ip

    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        name = socket.getfqdn(socket.gethostname())
        local_ip = socket.gethostbyname(name)
    return local_ip


def get_pid_by_port(port):
    """ 通过端口号获取进程号

    :param port:
    :return:
    """
    pid_list = []
    for process in psutil.get_process_list():
        try:
            cons = process.connections()
        except:
            cons = []
        for con in cons:
            if con.laddr and con.laddr[1] == port:
                pid_list.append(process.pid)
    return pid_list


def merge_dict(source, target):
    """合并字典

    :param source: 源字典 {'k': v}
    :param target: 目标字典 {'k': v}
    :return:
    """
    for k in target:
        if k in source:
            source[k] += target[k]
        else:
            source[k] = target[k]


def merge_dict_list(source, target):
    """合并字典, value值为list

    :param source: 源字典 {'k', [v]}
    :param target: 目标字典 {'k', [v]}
    :return:
    """
    for k in target:
        if k in source:
            source[k].extend(target[k])
        else:
            source[k] = list(target[k])


def merge_complex_dict(source, target):
    """合并复杂字典

    :param source: 源字典 {'k', v}
    :param target: 目标字典 {'k', v}
    :return:
    """
    for target_key, target_value in target.iteritems():
        if target_key in source:
            tp = type(target_value)
            if tp == list:
                source[target_key].extend(target_value)
            elif tp == dict:
                source[target_key].update(target_value)
            else:
                source[target_key] += target_value
        else:
            source[target_key] = copy.deepcopy(target_value) if isinstance(target_value, (dict, list)) else target_value


def add_dict(source, k, v):
    """合并字典

    :param source: 源字典 {'k', v}
    :param k: 增加的k
    :param v: 增加k的值
    :return:
    """
    if k in source:
        source[k] += v
    else:
        source[k] = v


def add_dict_list(source, k, v):
    """合并字典

    :param source: 源字典 {'k', v}
    :param k: 增加的k
    :param v: 增加k的值
    :return:
    """
    if k in source:
        source[k].append(v)
    else:
        source[k] = [v]


def merge_list_3(source, target):
    """ 合并list

    :param source: 原list [[1, 2, 3], [1, 2, 3]]
    :param target: 目标list [[1, 2, 3], [1, 2, 3]]
    :return:
    """
    for t in target:
        exist = False
        for s in source:
            if s[0] == t[0] and s[1] == t[1]:
                s[2] += t[2]
                exist = True
        if not exist:
            source.append(list(t))


def merge_list_2(source, target):
    """ 合并list

    :param source: 原list [[1, 2], [1, 2]]
    :param target: 目标list [[1, 2], [1, 2]]
    :return:
    """
    for t in target:
        exist = False
        for s in source:
            if s[0] == t[0]:
                s[1] += t[1]
                exist = True
        if not exist:
            source.append(list(t))


def mult_list_3(source, target):
    """ source中的list按target中的数值百分比加成

    :param source: 原list [[1, 2, 3], [1, 2, 3]]
    :param target: 目标list [[1, 2, 3], [1, 2, 3]]
    :return:
    """
    for t in target:
        exist = False
        for s in source:
            if s[0] == t[0] and s[1] == t[1]:
                s[2] += math.ceil(s[2] * t[2] / 100.0)
                exist = True
        if not exist:
            source.append(list(t))


def str_len(str):
    """
    计算字符长度
    :param str:
    :return:
    """
    try:
        row_l = len(str)
        utf8_l = len(str.encode('utf-8'))
        return (utf8_l - row_l) / 2 + row_l
    except:
        return None


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class filedefaultdict(defaultdict):
    """
    构造一个数据结构，类似defaultdict，传入文件路径，返回对应的写文件handler。
    如果不存在则创建一个。在所有操作阶数后，关闭改字典中所有的文件。
    这样可以避免反复开关文件的开销，且可以进行容错处理，保证文件全都关闭。
    """
    def __init__(self, mode='w'):
        self.mode = mode

    def __missing__(self, key):
        try:
            f = open(key, self.mode)
        except IOError:
            # 解决可能的路径不存在问题
            dir_path = os.path.dirname(key)
            if dir_path:
                os.system("""[ ! -d '{0}' ] && mkdir -p {0}""".format(dir_path))
            f = open(key, self.mode)
        ret = self[key] = f
        return ret

    def __del__(self):
        for f in self.itervalues():
            f.close()


def get_last_refresh_time(hour_format):
    """
    获取上次刷新时间
    :param hour_formant: %H:%M:%S，  刷新的时间点
    :return:
    """
    today = datetime.datetime.today()
    hour = time.strftime('%T')
    format = '%F {}'.format(hour_format)
    if hour_format < hour:
        return today.strftime(format)
    else:
        return (today - datetime.timedelta(1)).strftime(format)


def fake_deepcopy(data):
    return msgpack.loads(msgpack.dumps(data), encoding='utf-8')


def switch_endless_coin(coin):
    """
    对无尽币进行转换，主要是带有abc字母的字符串
    :param coin:
    :return:
    """
    if isinstance(coin, int):
        return coin

    N = 26
    float_len = 0

    coin1, coin2 = re.findall('(\d*\.*\d*)([a-zA-Z]*)', coin)[0]
    if not coin1:
        coin1 = 1
    else:
        if coin1.isdigit():
            coin1 = int(coin1)
        else:
            float_len = len(coin1.split('.')[-1])
            coin1 = int(float(coin1) * 10 ** float_len)

    if not coin2:
        return coin1

    index = 0
    for i, j in enumerate(list(coin2)[::-1]):
        num = ord(j) - ord('a') + 1
        index += num * N ** i

    return coin1 * 10 ** (3*index-float_len)


def clear_log_dir(dirname, expire_days=14, recursion=False):
    now = time.time()
    for abs_path, dirs, files in os.walk(dirname):
        # print 'test====', abs_path, dirs, files
        for file_name in files:
            file_path = os.path.join(abs_path, file_name)
            try:
                st = os.stat(file_path)
                # 删除超过两周的文件
                if now - st.st_mtime > 3600 * 24 * expire_days:
                    os.remove(file_path)
                    print 'remove file: ', file_path
            except Exception, e:
                print e

        if not recursion:
            break
