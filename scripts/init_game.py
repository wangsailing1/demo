#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 批量导入配置

import os
import sys
import MySQLdb

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings


def init_env(env):
    settings.set_env(env)


def main():
    from logics.market import init_market

    # 初始集市数据
    init_market()


if __name__ == '__main__':
    env = sys.argv[1]
    init_env(env)
    main()
