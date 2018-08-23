#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import re


int_compile = re.compile('^-?\d+$').match
float_compile = re.compile('^-?\d+\.\d*$').match
account_compile = re.compile('^[a-zA-Z0-9]{6,20}$').match


def is_int(value):
    """ 字符串是否为整数包括负数

    :param value:
    :return:
    """
    if int_compile(value):
        return True
    else:
        return False


def is_float(value):
    """ 字符串是否为浮点数

    :param value:
    :return:
    """
    if float_compile(value):
        return True
    else:
        return False


def is_account(value):
    """ 字符串是否符合账号, 账号只能为6-20位的字母数字组合

    :param value:
    :return:
    """
    if account_compile(value):
        return True
    else:
        return False
