#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 缓存正则表达式

import re


CACHE = {}


def compile_match(reg_name):
    c = CACHE.get(reg_name)
    if c:
        return c

    CACHE[reg_name] = c = re.compile(reg_name).match

    return c
