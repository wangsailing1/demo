#! --*-- coding: utf-8 --*--

__author__ = 'shaoqiang'

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
    'error_0': u"vip級別不夠，無法完成此操作",
    'error_1': u"戰鬥數據錯誤",
    'error_100': u"參數出錯",
    'error_9527': u'連接異常，請重新登錄(9527)',
    'error_close_shop': u'商店已關閉',
    'error_active_close': u'活動已結束',
    'error_config': u'缺少配置',
    'error_module': u"模組不存在",
    'error_method': u"方法不存在",
    'error_not_call_method': u"方法不可調用",
    'error_exp': u"戰鬥經驗錯誤",
    'error_silver': u"金幣不足",
    'error_diamond': u"鑽石不足",
    'error_coin': u"金幣不足",
    'error_dark_coin': u'黑街貨幣不足',
    'error_stone': u"靈魂石不足",
    'error_item': u'道具不足',
    'error_citem': u'採集物不足',
    'error_gitem': u'進階材料不足',
    'error_ggitem': u'公會禮物不足',
    'error_bitem': u'戰鬥道具不足',
    'error_equip': u'基因不足',
    'error_challenge': u'挑戰幣不足',
    'error_equip_not_exist': u"基因不存在",
    'error_gene_not_exist': u"裝備不存在",
    'error_hero_not_exist': u"英雄不存在",
    'error_gcard': u'昆特牌不足',
    'error_energy': u'能量不足',
    'error_point': u'體力不足',
    'error_aitem': u'覺醒材料不足',
    'error_unlock': u'還未解鎖',
    'error_team_skill': u'戰隊技能碎片不足',
    'error_silver_ticket': u'普通飛機票不足',
    'error_diamond_ticket': u'高級飛機票不足',
    'error_guild_coin': u'公會幣不足',
    'error_hunt_coin': u'末日狩獵挑戰券不足',
    'error_team_boss_coin': u'組隊boss挑戰券不足',
    'error_ladder_coin': u'巔峰幣不足',
    'error_box_coin': u'補給碎片不足',
    'error_donate_coin': u'榮耀幣不足',
    'error_box_key': u'覺醒寶箱鑰匙不足',
    'error_shop_buy': u'兌換等級不夠',
    'error_team_skill_exp': u'戰隊技能經驗不足',
    'error_wormhole_score': u'蟲洞幣不足',
    'error_star_array_point': u'星座點',
    'error_open_later_tips': u'敬請期待',
    'error_lua_battle': u'戰鬥服異常',
    'error_endless_close': u'無盡遠征功能00:00-05:00休息中',
    'error_endless_coin': u'無盡幣不足',
    'error_endless_score': u'無盡積分不足',
    'error_gene_piece': u'裝備碎片不足',
    'error_equip_coin': u'裝備幣不足',
    'error_honor_coin': u'榮譽幣不足',
    'error_guild_add_max': u'今日添加成員已達上限，無法添加成員',
}


account_msg = {
    'account.register': {
        1: u"帳號只能為6-20位元的字母數位組合",
        2: u"密碼不能為空",
        3: u"帳號已經存在",
    },
    'account.login': {
        1: u"帳號不存在",
        2: u"密碼錯誤",
    },
    'account.platform_access': {
        1: u"登錄失敗",
    },
    'account.new_user': {
        3: u"該服已有角色",
    },
}


config_msg = {
    'config.all_config': {
        1: u"配置無效",
    },
}


user_msg = {
    'user.new_user': {
        1: u"不是新用戶",
        2: u'名字不合法',
    },
    'user.gs_msg': {
        1: u"您提出的建議太頻繁了，請稍後再提",
        2: u"建議在100個字符內",
    },
    'user.set_title': {
        1: u"還沒有該稱號",
        2: u'該稱號正在使用',
        3: u'沒有稱號可卸載',
    },
    'user.buy_silver': {
        1: u"沒有購買次數",
    },
    'user.exchange_currency': {
        1: u"戰鬥等級需要到達40級開放",
        2: u"兌換配置錯誤",
        3: u"兌換上限超出",
    },
    'user.receive_player_exp': {
        1: u"沒有可領取的經驗",
    },
    'user.buy_privilege_gift': {
        1: u"參數錯誤",
        2: u"特權禮包不可購買",
        3: u"配置錯誤",
    },
    'user.buy_point': {
        1: u"今日已達購買上限",
        2: u"鑽石不足"
    },
    'user.charge_name': {
        1: u'名字不合法',
    },
    'user.register_name': {
        1: u'名字不合法',
        2: u'已經有名字了',
        3: u'名字不能為空',
    },
    'user.show_hero_detail': {
        1: u'沒有該英雄',
    },
    'user.top_rank': {
        -1: u'沒有該類排行榜',
    },
    'user.level_award': {
        1: u'獎勵已領取或者已過期',
        2: u'充值才能獲得',
    },
    'user.change_icon': {
        1: u'該頭像為解鎖',
    },
}


i18n = {
    'user_name': u'敢鬥團',
    'dark_steet': u'黑街擂臺',
    'friend': u'好友%s',
    'rally': u'血塵拉力賽',
    'market': u'集市',
    'guild': u'公會',
    'remove_guild': u'被公會強制請離通知！',
    'big_world': u'大地圖',
    # 'guild_position': {1: u'會長', 2: u'副會長', 3: u'骨幹', 4: u'成員'},
    'guild_position1': u'會長',
    'guild_position2': u'副會長',
    'guild_position3': u'骨幹',
    'guild_position4': u'成員',
    'guild_fight': u'公會戰',
    'monthly_sign': u'每日簽到',
    'three_days_login': u'三顧茅廬',
    'daily_task': u'每日任務',
    'equip_drop_star': u'覺醒材料返還',
    'high_ladder_rank_reward': u'競技場排名獎勵',
    'mercenary': u'傭兵營地',
    'charge': u'充值獎勵',
    'level_gift': u'限時等級禮包',
    'invest': u'零用錢銀行',
    'first_recharge': u'首充禮包',
    'biography': u'傳記',
    'star_reward': u'星芒法陣每日獎勵',
    'recruit_title': u'招募有禮獎勵',
    'recruit_des': u'您有“招募有禮”活動獎勵未領取,特郵件發送給您,請查收。',
    'active_gacha_title': u'多次招募送碎片獎勵',
    'active_gacha_des': u'您有“多次招募送機甲蘿莉碎片”活動獎勵未領取,特郵件發送給您,請查收。',
    'sign_recharge_title': u'連續充值',
    'sign_recharge_des': u'親愛的玩家，您昨日參與連續充值的獎勵未領取，特郵件發送給您，請查收。',
    'daily_package': u'每日禮包',
    'decisive_battle_title': u'爭霸賽排名獎勵',
    'decisive_battle_des': u'恭喜你在爭霸賽中取得了第%d名，獎勵如下：',
    'pay_sign_title': u'超值签到补发',
    'pay_sign_des': u'您昨日有未领取的超值签到奖励，现补发给您，请查收~',
    'doomsday_hunt': u'猛獸通緝令',
    'hunt_box': u'您的寶箱獎勵未領取，請查收',
    'limit_discount': u'限時特惠禮包',
    'challenge_rank': u'極限挑戰排名獎',
    1: u'%s (LV.%s) 將你加為好友',
    2: u'%s表示仰慕你很久了，申請添加你為好友，是否通過好友申請？',
    3: u'%s已通過了你的好友申請，你們現在已經是好友了，趕快私密他吧！',
    4: u'%s聯盟邀請你的加入，申請添加你成為聯盟成員，是否通過邀請？',
    5: u'道具組1',
    6: u'你在集市中出售的物品超過出售時間系統返回如下',
    7: u'你在每日挑戰中獲取排名獎勵如下',
    8: u'恭喜獲得黑街擂臺擊破獎勵',
    9: u'恭喜獲得黑街擂臺輪數獎勵',
    10: u'恭喜獲得黑街擂臺防守獎勵',
    11: u'很遺憾,%s公會拒絕了您的公會申請!',
    12: u'%s公會同意了您的公會申請!',
    13: u'您的公會職位由 %s 變為了 %s ',
    14: u'恭喜獲得公會戰獎勵',
    15: u'補發的每日簽到獎勵',
    16: u'補發的三顧茅廬未領取的獎勵',
    17: u'補發的每日任務未領取的獎勵',
    18: u'挑戰券不足，需要%s張',
    19: u'別點太快了呦，親',
    20: u'伺服器出錯啦！',
    21: u'降星成功，基因之魂從基因中完好無損的摘了下來，雙手奉上',
    22: u'恭喜在競技場中取得了%(rank)s名',
    23: u'您的傭兵【%s】收益',
    24: u'這是您充值獲得的獎勵，請查收',
    25: u'您成功購買限時等級禮包，獎勵如下',
    26: u'尊敬的玩家，您參加了上一期古靈閣的活動，系統將上一期古靈閣投資所得的本金和利潤通過本郵件返還給您，請查收。',
    27: u'<#A6F900>%(user_name)s<#77AAD5>投資%(per)s%%項目',
    28: u'<#A6F900>%(user_name)s<#77AAD5>領取了<#FFD340>%(coin)s鑽石',
    29: u'首充禮包，請查收',
    30: u'操作頻繁,請等待%s秒',
    31: u'傳記技能周禮包',
    32: u'星芒法陣每日獎勵',
    33: u'vip每日禮包',
    34: u'您昨日有未領取的禮包，請查收獎勵。',
    35: u'您的公會覺得你們不太合適，揮一揮手與您劃清了關係；別擔心，天生我材必有用，快去找其他公會申請吧！',
    36: u'您的等級不足，關卡解鎖需要%s級',
    37: u'内侧充值返利',
    38: u'''指挥官大人：
    这是您参与内侧充值返利的双倍钻石，请接收~
                                机要秘书---琳''',
    39: u'VIP專屬通知',
    40: u'''指揮官大人：
    恭喜您達到VIP8，請您添加VIP專屬客服QQ：800042348，我們會有專人為您解答問題並領取VIP豪華大禮包~
                                機要秘書---琳''',
    41: u'恭喜獲得極限挑戰每日排名第%s名',
    42: u'恭喜獲得極限挑戰每期排名第%s名',
}

# 注册需要写到最下面
register_handler()
