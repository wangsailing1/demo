#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import datetime

from tools.gift import add_mult_gift


def check_time(config, now=None):
    """检测激活码活动配置里这个活动是否有效
    args:
        config: 活码活动配置
        now: 对比时间，datetime.datetime对象
    returns:
        bool值，True表示有效，False表示无效
    """
    now = now or datetime.datetime.now()

    opentime = closetime = now
    if config['open'] != '-1':
        opentime = datetime.datetime.strptime(config['open'], '%Y-%m-%d %H:%M:%S')
    if config['close'] != '-1':
        closetime = datetime.datetime.strptime(config['close'], '%Y-%m-%d %H:%M:%S')

    return opentime <= now <= closetime


class CodeLogic(object):
    """激活码逻辑
    """
    def __init__(self, mm):
        self.mm = mm
        self.code = self.mm.code

    def use_code(self, code, code_data, config):
        """使用激活码， 并给用户奖励
        args:
            code: 激活码
            code_data: 激活码数据  eg:{'code_id': 1, 'create': '2014-01-24-18:29:39', 'used_uid': None}
            config: 此激活码活动配置
        returns:
            奖励
        """

        award = add_mult_gift(self.mm, config['reward'])
        self.code.use_code(code, code_data)
        return award
