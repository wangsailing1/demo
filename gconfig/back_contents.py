#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 命名规则 xxx_mapping

import re


def register_mapping_config(source, target):
    """ 注册提示消息

    :param source: 原 {}
    :param target: 目标 {}
    """
    for k, v in target.iteritems():
        if k in source:
            raise RuntimeError("config [%s] Already exists in %s" % (k, __file__))
        source[k] = v
    target.clear()

    # source.update(target)
    # target.clear()


def register_handler():
    match = re.compile('^[a-zA-Z0-9_]+_mapping$').match
    g = globals()
    mapping = g['mapping_config']
    for name, value in g.iteritems():
        if match(name):
            register_mapping_config(mapping, value)


mapping_config = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'name': (None, True),     # simple
}


# 注册需要写到最下面
register_handler()
