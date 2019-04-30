# -*- coding: utf-8 –*-


# 单笔充值
single_recharge = {
    'uk':           ('id',              'int'),             # 商品编号
    'version':      ('version',         'int'),             # 版本号
    'charge_id':    ('charge_id',       'int'),             # 购买项
    'limit_num':    ('limit_num',       'int'),             # 限次
    'reward':       ('reward',          'int_list'),        # 奖励[类型，id，数量]
}


# 新服单笔充值
server_single_recharge = {
    'uk':           ('id',              'int'),             # 商品编号
    'version':      ('version',         'int'),             # 版本号
    'charge_id':    ('charge_id',       'int'),             # 购买项
    'limit_num':    ('limit_num',       'int'),             # 限次
    'reward':       ('reward',          'int_list'),        # 奖励[类型，id，数量]
}