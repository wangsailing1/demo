#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 命名规则 xxx_msg

import re


def register_msg_config(source, target):
    """ 注册提示消息

    :param source: 原 {}
    :param target: 目标 {}
    """
    source.update(target)
    target.clear()


def register_handler():
    match = re.compile('^[a-zA-Z0-9_]+_msg$').match
    g = globals()
    return_msg = g['return_msg_config']
    for name, value in g.iteritems():
        if match(name):
            register_msg_config(return_msg, value)


return_msg_config = {
    # 'error_home': u"返回主页的错误码，提示语需自定义",
    'error_0': u"vip级别不够，无法完成此操作",
    'error_1': u"战斗数据错误",
    'error_2': u"数据错误",
    'error_100': u"参数出错",
    'error_9527': u'连接异常，请重新登录(9527)',
    'error_close_shop': u'商店已关闭',
    'error_active_close': u'活动已结束',
    'error_config': u'缺少配置',
    'error_module': u"模块不存在",
    'error_method': u"方法不存在",
    'error_not_call_method': u"方法不可调用",
    'error_exp': u"战斗经验错误",
    'error_silver': u"金币不足",
    'error_diamond': u"钻石不足",
    'error_coin': u"金币不足",
    'error_dollar': u"美元不足",

    'error_card_cold': u'艺人被雪藏中',
    'error_card_piece': u'艺人碎片不足',

    'error_stone': u"灵魂石不足",
    'error_item': u'道具不足',
    'error_citem': u'采集物不足',
    'error_gitem': u'进阶材料不足',
    'error_ggitem': u'公会礼物不足',
    'error_bitem': u'战斗道具不足',
    'error_equip': u'基因不足',
    'error_challenge': u'挑战币不足',
    'error_equip_not_exist': u"基因不存在",
    'error_gene_not_exist': u"装备不存在",
    'error_hero_not_exist': u"英雄不存在",
    'error_gcard': u'昆特牌不足',
    'error_energy': u'能量不足',
    'error_point': u'体力不足',
    'error_like': u'点赞不足',
    'error_aitem': u'觉醒材料不足',
    'error_unlock': u'还未解锁',
    'error_team_skill': u'战队技能碎片不足',
    'error_silver_ticket': u'普通飞机票不足',
    'error_diamond_ticket': u'高级飞机票不足',
    'error_guild_coin': u'公会币不足',
    'error_hunt_coin': u'末日狩猎挑战券不足',
    'error_team_boss_coin': u'组队boss挑战券不足',
    'error_ladder_coin': u'巅峰币不足',
    'error_box_coin': u'补给碎片不足',
    'error_donate_coin': u'荣耀币不足',
    'error_box_key': u'觉醒宝箱钥匙不足',
    'error_shop_buy': u'兑换等级不够',
    'error_team_skill_exp': u'战队技能经验不足',
    'error_wormhole_score': u'虫洞币不足',
    'error_star_array_point': u'星座点不足',
    'error_open_later_tips': u'敬请期待',
    'error_lua_battle': u'战斗服异常',
    'error_endless_close': u'无尽远征功能00:00-05:00休息中',
    'error_endless_coin': u'无尽币不足',
    'error_endless_score': u'无尽积分不足',
    'error_gene_piece': u'装备碎片不足',
    'error_equip_coin': u'装备币不足',
    'error_honor_coin': u'荣誉币不足',
    'error_guild_add_max': u'今日添加成员已达上限，无法添加成员',
}

account_msg = {
    'account.register': {
        1: u"账号只能为6-20位的字母数字组合",
        2: u"密码不能为空",
        3: u"账号已经存在",
    },
    'account.login': {
        1: u"账号不存在",
        2: u"密码错误",
    },
    'account.platform_access': {
        1: u"登录失败",
    },
    'account.new_user': {
        3: u"该服已有角色",
    },
}

config_msg = {
    'config.all_config': {
        1: u"配置无效",
    },
}

user_msg = {
    'user.new_user': {
        1: u"不是新用户",
        2: u'名字不合法',
    },
    'user.gs_msg': {
        1: u"您提出的建议太频繁了, 请稍后再提",
        2: u"建议在100个字符内",
    },
    'user.set_title': {
        1: u"还没有该称号",
        2: u'该称号正在使用',
        3: u'没有称号可卸载',
    },
    'user.buy_silver': {
        1: u"没有购买次数",
    },
    'user.exchange_currency': {
        1: u"战斗等级需要到达40级开放",
        2: u"兑换配置错误",
        3: u"兑换上限超出",
    },
    'user.receive_player_exp': {
        1: u"没有可领取的经验",
    },
    'user.buy_privilege_gift': {
        1: u"参数错误",
        2: u"特权礼包不可购买",
        3: u"配置错误",
    },
    'user.buy_point': {
        1: u"今日已达购买上限",
        2: u"钻石不足"
    },
    'user.charge_name': {
        1: u'名字不合法',
    },
    'user.register_name': {
        1: u'名字不合法',
        2: u'已经有名字了',
        3: u'名字不能为空',
    },
    'user.show_hero_detail': {
        1: u'没有该英雄',
    },
    'user.top_rank': {
        -1: u'没有该类排行榜',
    },
    'user.level_award': {
        1: u'奖励已领取或者已过期',
        2: u'充值才能获得',
    },
    'user.change_icon': {
        1: u'该头像未解锁',
    },
    'user.unlock_icon': {
        1: u'没有头像',
        2: u'头像已解锁',
        3: u'性别不符',
    },
}

card_msg = {
    'card.card_add_love_exp': {
        2: u'道具类型不符',
        3: u'超出送礼上限',
    },
    'card.card_love_level_up': {
        2: u'经验不足，无法升级',
        3: u'已到最大等级',
    },

}


script_msg = {
    'script_gacha.get_gacha': {
        1: u'cd未结束'
    }
}


chapter_stage_msg = {
    'chapter_stage.chapter_stage_fight': {
        1: u'关卡参数错误',
        11: u'章节错误',
        12: u'难度错误',
        13: u'关卡错误',
        14: u'配置错误',
        15: u'关卡错误',
        16: u'剩余次数不足',
        17: u'体力不足',
        18: u'助战演员错误',
        19: u'角色错误',
        20: u'参数错误',
        23: u'有未拥有的艺人',
        24: u'等级不够',
    },
    'chapter_stage.auto_sweep': {
        11: u'章节错误',
        12: u'难度错误',
        13: u'关卡错误',
        14: u'配置错误',
        15: u'关卡错误',
        16: u'剩余次数不足',
        17: u'体力不足',
        18: u'助战演员错误',
        19: u'角色错误',
        20: u'参数错误',
        21: u'尚未通关',
        22: u'未达到扫荡星级',
        23: u'有未拥有的艺人',
        24: u'等级不够',
    },
    'chapter_stage.get_dialogue_reward': {
        11: u'剧情关配置错误',
        12: u'剧情选择错误',
        13: u'卡牌id错误',
    }
}

book_msg = {
    'book.get_card_reward': {
        1: u'组合未完成',
        2: u'组合未完成',
        3: u'奖励已领',
        4: u'没有相应组合',
        5: u'奖励错误',
    },
    'book.get_script_reward': {
        1: u'组合未完成',
        2: u'组合未完成',
        3: u'奖励已领',
        4: u'没有相应组合',
        5: u'奖励错误',
    },
    'book.get_group_reward': {
        1: u'组合未完成',
        2: u'组合未完成',
        3: u'奖励已领',
        4: u'没有相应组合',
        5: u'奖励错误',
    }
}

shop_msg = {
    'shop.index': {
        -1: u'未解锁',
        2: u'配置错误',
    },
    'shop.buy': {
        -1: u'未解锁',
        2: u'商品错误',
        3: u'配置错误',
        4: u'购买次数超过上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.refresh_goods': {
        -1: u'未解锁',
        1: u'我们正在准备进货，请耐心等待',
        2: u'刷新次数不足',
    },
    'shop.gift_index': {
        -1: u'未解锁',
        2: u'配置错误',
    },
    'shop.gift_buy': {
        -1: u'未解锁',
        2: u'商品错误',
        3: u'配置错误',
        4: u'购买次数超过上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.resource_index': {
        -1: u'未解锁',
        2: u'配置错误',
    },
    'shop.resource_buy': {
        -1: u'未解锁',
        2: u'商品错误',
        3: u'配置错误',
        4: u'购买次数超过上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.mystical_index': {
        -1: u'未解锁',
        2: u'配置错误',
    },
    'shop.mystical_buy': {
        -1: u'未解锁',
        2: u'商品错误',
        3: u'配置错误',
        4: u'购买次数超过上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.mystical_refresh': {
        -1: u'未解锁',
        1: u'刷新次数也达最大次数',
        2: u'配置错误',
        3: u'钻石不足',
    },
}

block_msg = {
    'block.get_reward': {
        1: u'已领奖',
    },
    'block.get_daily_reward': {
        1: u'已领奖',
        2: u'配置错误'
    },
    'block.congratulation': {
        1: u'已祝贺',
    }
}

friend_msg = {
    'friend.actor_chat': {
        1: u'未选择艺人',
        11: u'当前对话id错误',
        13: u'次数超出',
        14: u'当前对话id错误',
        15: u'对话配置错误',
        16: u'对话选择错误',
        17: u'已选择过对话',
        18: u'对话已结束',
        19: u'未选择对话',

    },
    'friend.rename': {
        1: u'已领奖',
        2: u'配置错误'
    }
}

fans_activity_msg = {
    'fans_activity.fans_index': {
        11: u'未举办该活动',

    },
    'fans_activity.activity': {
        1: u'没有艺人参加',
        2: u'未选活动',
        3: u'活动id错误',
        11: u'卡牌错误',
        12: u'没有艺人参加',
        13: u'有卡牌属性值不够',
        14: u'有卡牌性别不符',
        15: u'有卡牌类型不符',
        16: u'有卡牌人气不足',
        17: u'美元不足',
        18: u'活动未结束',
    },
    'fans_activity.unlock_activity': {
        1: u'没有活动',
        2: u'该活动尚不能解锁',
        3: u'美元不足',
        4: u'已解锁',
        5: u'首次建筑的等级错误',
    },
    'fans_activity.up_activity': {
        1: u'活动等级已经最大',
        2: u'该活动尚不能解锁',
        3: u'美元不足',
        4: u'活动错误',
        5: u'升级id错误',
    },
    'fans_activity.get_reward': {
        1: u'请选择活动',
        2: u'未参加活动',
    },
}

i18n = {
    'user_name': u'敢斗团',
    'dark_steet': u'黑街擂台',
    'friend': u'好友%s',
    'rally': u'血尘拉力赛',
    'market': u'集市',
    'guild': u'公会',
    'remove_guild': u'被公会强制请离通知！',
    'big_world': u'大地图',
    # 'guild_position': {1: u'会长', 2: u'副会长', 3: u'骨干', 4: u'成员'},
    'guild_position1': u'会长',
    'guild_position2': u'副会长',
    'guild_position3': u'骨干',
    'guild_position4': u'成员',
    'guild_fight': u'公会战',
    'monthly_sign': u'每日签到',
    'three_days_login': u'三顾茅庐',
    'daily_task': u'每日任务',
    'equip_drop_star': u'基因降星材料返还',
    'high_ladder_rank_reward': u'竞技场排名奖励',
    'mercenary': u'佣兵营地',
    'charge': u'充值奖励',
    'level_gift': u'限时等级礼包',
    'invest': u'零用钱银行',
    'first_recharge': u'首充礼包',
    'biography': u'传记',
    'star_reward': u'星芒法阵每日奖励',
    'recruit_title': u'招募有礼奖励',
    'recruit_des': u'您有“招募有礼”活动奖励未领取，特邮件发送给您，请查收。',
    'active_gacha_title': u'多次招募送碎片奖励',
    'active_gacha_des': u'您有“多次招募送机甲萝莉碎片”活动奖励未领取，特邮件发送给您，请查收。',
    'sign_recharge_title': u'连续充值',
    'sign_recharge_des': u'亲爱的玩家，您昨日参与连续充值的奖励未领取，特邮件发送给您，请查收。',
    'daily_package': u'每日礼包',
    'decisive_battle_title': u'争霸赛排名奖励',
    'decisive_battle_des': u'恭喜你在争霸赛中取得了第%d名，奖励如下：',
    'pay_sign_title': u'超值签到补发',
    'pay_sign_des': u'您昨日有未领取的超值签到奖励，现补发给您，请查收~',
    'doomsday_hunt': u'猛兽通缉令',
    'hunt_box': u'您的宝箱奖励未领取，请查收',
    'limit_discount': u'限时特惠礼包',
    'challenge_rank': u'极限挑战排名奖',
    1: u'%s (LV.%s) 将你加为好友',
    2: u'%s表示仰慕你很久了，申请添加你为好友，是否通过好友申请？',
    3: u'%s已通过了你的好友申请，你们现在已经是好友了，赶快私密他吧！',
    4: u'%s联盟邀请你的加入，申请添加你成为联盟成员，是否通过邀请？',
    5: u'道具组1',
    6: u'你在集市中出售的物品超过出售时间系统返回如下',
    7: u'你在每日挑战中获取排名奖励如下',
    8: u'恭喜获得黑街擂台击破奖励',
    9: u'恭喜获得黑街擂台轮数奖励',
    10: u'恭喜获得黑街擂台防守奖励',
    11: u'很遗憾,%s公会拒绝了您的公会申请!',
    12: u'%s公会同意了您的公会申请!',
    13: u'您的公会职位由 %s 变为了 %s ',
    14: u'恭喜获得公会战奖励',
    15: u'补发的每日签到奖励',
    16: u'补发的三顾茅庐未领取的奖励',
    17: u'补发的每日任务未领取的奖励',
    18: u'挑战券不足，需要%s张',
    19: u'别点太快了呦，亲',
    20: u'服务器出错啦！',
    21: u'降星成功，基因之魂从基因中完好无损的摘了下来，双手奉上',
    22: u'恭喜在竞技场中取得了%(rank)s名',
    23: u'您的佣兵【%s】收益',
    24: u'这是您充值获得的奖励，请查收',
    25: u'您成功购买限时等级礼包，奖励如下',
    26: u'尊敬的玩家，您参加了上一期古灵阁的活动，系统将上一期古灵阁投资所得的本金和利润通过本邮件返还给您，请查收。',
    27: u'<#A6F900>%(user_name)s<#77AAD5>投资%(per)s%%项目',
    28: u'<#A6F900>%(user_name)s<#77AAD5>领取了<#FFD340>%(coin)s钻石',
    29: u'首充礼包，请查收',
    30: u'操作频繁,请等待%s秒',
    31: u'传记技能周礼包',
    32: u'星芒法阵每日奖励',
    33: u'vip每日礼包',
    34: u'您昨日有未领取的礼包，请查收奖励。',
    35: u'您的公会觉得你们不太合适，挥一挥手与您划清了关系；别担心，天生我材必有用，快去找其他公会申请吧！',
    36: u'您的等级不足，关卡解锁需要%s级',
    37: u'内侧充值返利',
    38: u'''指挥官大人：
    这是您参与内侧充值返利的双倍钻石，请接收~
                                机要秘书---琳''',
    39: u'VIP专属通知',
    40: u'''指挥官大人：
    恭喜您达到VIP8，请您添加VIP专属客服QQ：800042348，我们会有专人为您解答问题并领取VIP豪华大礼包~
                                机要秘书---琳''',
    41: u'恭喜获得极限挑战每日排名第%s名',
    42: u'恭喜获得极限挑战每期排名第%s名',
}

# 注册需要写到最下面
register_handler()
