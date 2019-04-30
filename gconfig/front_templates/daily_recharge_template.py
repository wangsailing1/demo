#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 用户相关的配置

# 每日充值
daily_recharge = {
    'uk':               ('id',              'int'),                 # id
    'version':          ('version',         'int'),                 # 版本号
    'day':              ('day',             'int'),                 # 第几天
    'type':             ('type',            'int'),                 # 充值类型
    'number':           ('number',          'int'),                 # 充值数量
    'reward':           ('reward',          'int_list'),            # 奖励[类型，id，数量]
    'des':              ('des',             'int'),                 # 描述
    'mail_title':       ('mail_title',      'int'),                 # 邮件标题
    'mail':             ('mail',            'int'),                 # 邮件内容
}


# 新服每日充值
server_daily_recharge = {
    'uk':               ('id',              'int'),                 # id
    'version':          ('version',         'int'),                 # 版本号
    'day':              ('day',             'int'),                 # 第几天
    'type':             ('type',            'int'),                 # 充值类型
    'number':           ('number',          'int'),                 # 充值数量
    'reward':           ('reward',          'int_list'),            # 奖励[类型，id，数量]
    'des':              ('des',             'int'),                 # 描述
    'mail_title':       ('mail_title',      'int'),                 # 邮件标题
    'mail':             ('mail',            'int'),                 # 邮件内容
}