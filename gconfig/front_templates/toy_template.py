#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 用户相关的配置
from gconfig import check


# 付费娃娃机
rmb_gacha = {
    'uk':               ('id',              'int'),                 # id
    'library_id':       ('library_id',      'int'),                 # 库id
    'group':            ('group',           'int'),                 # 分组
    'award':            ('award',           'int_list'),            # 奖励
    'weight_show':      ('weight_show',     'int'),                 # 组内出现权重
    'sequence':         ('sequence',        'int'),                 # 显示顺序（从前往后）
    'undrop_rate':      ('undrop_rate',     'int_list'),            # 被抽中后不脱抓概率万分比（次数，概率）
    'mustlost':         ('mustlost',        'int'),                 # 第几次抓取之前必脱钩（不含没对准）
}

# 付费娃娃机消耗
rmb_gacha_cost = {
    'uk':               ('id',              'int'),                 # id
    'cost':             ('cost',            'int_list'),            # 奖券消耗
}

# 付费娃娃机消耗
rmb_gacha_control = {
    'uk':                   ('id',                  'int'),            # id
    'cd':                   ('cd',                  'int'),            # 免费刷新cd[分钟]
    'cost':                ('cost',               'int_list'),         # 刷新消耗1
    'group_num':            ('group_num',           'int_list'),       # 奖池数量[组，抽取数量]
    'group_choosequality':  ('group_choosequality', 'int_list'),       # 组抓取区域选择权重
    'group_mustgetnum':     ('group_mustgetnum',    'int_list'),       # 组不空抓取在第几次必不脱钩（仅对准任意奖品）
    'compensate':           ('compensate',          'int_list'),       # 补偿奖励
}

# 付费娃娃机排行
rmb_gacha_rank = {
    'uk':                   ('id',                  'int'),             # id
    'rank':                 ('rank',                'int_list'),        # 排名
    'reward':               ('reward',              'int_list'),        # 奖励
    'mail_title':           ('mail_title',          'str'),             # 邮件名称
    'mail_content':         ('mail_content',        'str'),             # 邮件内容
}

# 免费娃娃机
free_gacha = {
    'uk':               ('id',              'int'),                 # id
    'library_id':       ('library_id',      'int'),                 # 库id
    'group':            ('group',           'int'),                 # 分组
    'award':            ('award',           'int_list'),            # 奖励
    'weight_show':      ('weight_show',     'int'),                 # 组内出现权重
    'sequence':         ('sequence',        'int'),                 # 显示顺序（从前往后）
    'undrop_rate':      ('undrop_rate',     'int_list'),            # 被抽中后不脱抓概率万分比（次数，概率）
    'mustlost':         ('mustlost',        'int'),                 # 第几次抓取之前必脱钩（不含没对准）
}

# 免费娃娃机消耗
free_gacha_cost = {
    'uk':               ('id',              'int'),                 # id
    'cost':             ('cost',            'int_list'),            # 奖券消耗
}

# 免费娃娃机消耗
free_gacha_control = {
    'uk':                   ('id',                  'int'),            # id
    'cd':                   ('cd',                  'int'),            # 免费刷新cd[分钟]
    'cost':                ('cost',               'int_list'),       # 刷新消耗1
    'group_num':            ('group_num',           'int_list'),       # 奖池数量[组，抽取数量]
    'group_choosequality':  ('group_choosequality', 'int_list'),       # 组抓取区域选择权重
    'group_mustgetnum':     ('group_mustgetnum',    'int_list'),       # 组不空抓取在第几次必不脱钩（仅对准任意奖品）
    'compensate':           ('compensate',          'int_list'),       # 补偿奖励
}