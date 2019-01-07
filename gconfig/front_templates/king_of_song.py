# -*- coding: utf-8 –*-


pvp_rank = {
    'uk':               ('id',              'int'),         # id
    'name':             ('name',            'str'),         # 区间名称
    'name0':            ('name0',           'str'),         # 段位名称
    'icon':             ('icon',            'int'),         # 段位图标
    'script':           ('script',          'int_list'),    # 可选作品库
    'card_num':         ('card_num',        'int'),         # 剧本上阵人数
    'star_up':          ('star_up',         'int'),         # 晋级临界值
    'star_down':          ('star_down',     'int'),         # 降级临界值
    'award_win':          ('award_win',     'int_list'),    # 胜利1场奖励
    'award_lose':         ('award_lose',    'int_list'),    # 失败1场奖励
    'award_tast':         ('award_tast',    'int_list'),    # 胜场奖励
    'award_end':          ('award_end',     'int_list'),    # 赛季结束奖励
}

pvp_robots = {
    'uk':               ('id',          'int'),         # 机器人id
    'rank':             ('rank',        'int'),         # 所属段位
    'lv':               ('lv',          'int'),         # 显示等级
    'name':             ('name',        'unicode'),     # 显示名字
    'card':             ('card',        'int_list'),    # 拥有艺人
}