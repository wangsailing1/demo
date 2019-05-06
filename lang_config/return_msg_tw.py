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
    # 'error_home': u"返回主頁的錯誤碼，提示語需自訂",
    'error_0': u"vip級別不夠，無法完成此操作",
    'error_1': u"戰鬥資料錯誤",
    'error_2': u"資料錯誤",
    'error_14': u'等級不足！需要達到%s級才能繼續！',
    'error_21': u"重新登入",
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
    'error_dollar': u"美元不足",
    'error_no_ceremony': u'敬請期待明天晚上九點的頒獎典禮',

    'error_card_cold': u'藝人被雪藏中',
    'error_card_piece': u'藝人碎片不足',
    'error_equip_piece': u'裝備碎片不足',
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
    'error_like': u'點贊不足',
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
    'error_star_array_point': u'星座點不足',
    'error_open_later_tips': u'敬請期待',
    'error_lua_battle': u'戰鬥服異常',
    'error_endless_close': u'無盡遠征功能00:00-05:00休息中',
    'error_endless_coin': u'無盡幣不足',
    'error_endless_score': u'無盡積分不足',
    'error_gene_piece': u'裝備碎片不足',
    'error_equip_coin': u'裝備幣不足',
    'error_honor_coin': u'榮譽幣不足',
    'error_guild_add_max': u'今日添加成員已達上限，無法添加成員',
    'error_popularity': u'人氣不足',
    'error_food_enough': u'食品倉庫已滿',
    'error_assistant': u'請先聘請終身助理',
    'error_superplayer': u'活動未開啟',
    'error_sensitive_name': u'名字不合法',

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
        1: u"您提出的建議太頻繁了, 請稍後再提",
        2: u"建議在100個字元內",
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
        2: u'名字已使用',
        5: u'名字已經存在',
    },
    'user.register_name': {
        1: u'名字不合法',
        2: u'已經有名字了',
        3: u'名字不能為空',
        5: u'名字已經存在',
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
        1: u'該頭像未解鎖',
    },
    'user.unlock_icon': {
        1: u'沒有頭像',
        2: u'頭像已解鎖',
        3: u'性別不符',
    },
    'user.blacklist_add': {
        1: u'已經在遮罩名單中',
    },
    'user.build': {
        1: u'配置錯誤',
        3: u'已擁有建築',
        4: u'參數錯誤',
        5: u'地塊錯誤',
        6: u'未達到解鎖等級',
        101: u'未達到解鎖等級',
        201: u'沒有配置',
    },
    'user.up_build': {
        1: u'配置錯誤',
        2: u'還未擁有建築',
        4: u'參數錯誤',
        5: u'已到達最大等級',
        6: u'經驗值不足',
        101: u'未達到解鎖等級',
        201: u'沒有配置',
    },
    'user.get_company_vip_reward': {
        1: u'vip等級未達到',
        2: u'禮包已領取',
        4: u'vip等級錯誤',
    },
    'user.gift_award': {
        1: u'配置錯誤',
        2: u'禮包已領取',
    },
}

card_msg = {
    'card.card_level_up': {
        2: u'請升級格調等級',
    },
    'card.card_quality_up': {
        3: u'卡牌裝備不足',
        4: u'卡牌等級不足',
    },
    'card.card_add_love_exp': {
        2: u'道具類型不符',
        3: u'超出送禮上限',
        4: u'贈送禮物已達上限，屬性不再提升，請升級羈絆後再來',
    },
    'card.card_love_lvup': {
        1: u'尚未擁有此藝人',
        2: u'經驗不足，無法升級',
        3: u'已到最大等級',
    },
    'card.card_love_level_up': {
        2: u'經驗不足，無法升級',
        3: u'已到最大等級',
    },
    'card.card_train': {
        2: u'已達到最大培養次數',
    },
    'card.set_equip': {
        1: u'藝人不存在',
        2: u'已穿此類裝備',
        3: u'裝備超出所需上限',
        4: u'裝備與卡牌不匹配',
    },
    'card.equip_piece_auto_exchange': {
        1: u'碎片數量不足',
    },
    'card.card_piece_exchange': {
        1: u'已有此類藝人',
        2: u'活躍卡牌已達上限，請先雪藏藝人',
    },
    'card.up_card_building': {
        1: u'等級最大',
        2: u'等級未達到要求',
    },
    'card.add_card_box': {
        1: u'鑽石不足',
    },
    'card.thaw': {
        1: u'尚未擁有該藝人',
        2: u'活躍卡牌已達上限',
    },
    'card.add_card_popularity': {
        1: u'數量不足',
        2: u'未擁有此卡牌',
    },
    'card.skill_level_up': {
        1: u'未擁有該卡牌',
        2: u'該角色沒有該技能',
        3: u'技能未解鎖',
        4: u'已達到最高等級',
        5: u'技能經驗不足，請安排訓練或使用藥品補充',
    },
    'card.train_card': {
        1: u'未擁有該卡牌',
        2: u'已經在訓練中',
        3: u'沒有訓練空位',
        4: u'技能已滿',
        5: u'藝人經驗已足夠，可升到滿級'
    },
    'card.use_exp_item': {
        1: u'未擁有該卡牌',
        2: u'item_id未傳值',
        3: u'藝人經驗已足夠，可升到滿級',
    },
    'card.finish_train': {
        1: u'未傳遞參數tr_id',
        2: u'訓練位未開啟',
        3: u'訓練中',
    },
    'card.train_speed_up': {
        1: u'未傳遞參數tr_id',
        2: u'訓練位未開啟',
        3: u'該訓練位不在訓練中',
        4: u'鑽石不足',
    },
    'card.add_train_place': {
        1: u'鑽石不足',
        2: u'已達到最大訓練位',
    },
    'card.train': {
        1: u'未擁有該卡牌',
        2: u'未傳遞參數tr_id',
        3: u'訓練位未開啟',
        4: u'該訓練位正在被使用',
        5: u'此藝人技能已全滿級，不用再次訓練！',
        6: u'藝人經驗已足夠，可升到滿級',
        7: u'藝人正在訓練中',
    },
}

gacha_msg = {
    'gacha.get_gacha': {
        2: u'cd中',
        3: u'可抽卡次數不足'
    },
    'gacha.receive': {
        1: u"沒有此藝人",
        2: u'已簽約過',
        3: u'活躍卡牌已達上限，請先雪藏藝人',
    },

    'gacha.up_gacha': {
        1: u"已到最大等級",
        2: u"招募次數不夠",
    },
}

script_msg = {
    'script.pre_filming': {
        1: u'許可證不足',
    },
    'script.re_selection': {
        1: u'重新選擇劇本次數已用完',
    },
    'script.set_card': {
        2: u'已選完角色',
        3: u'演員與角色設置不可重複',
        4: u'請選角色',
        5: u'有卡牌休息中',
        6: u'藝人體力不足，請先休息',
        7: u'藝人心情糟糕，請先休息',
        'error_profession_class': u'藝人實力不符',
        'error_sex_type': u'藝人性別不符',
        'error_profession_type': u'藝人青春成熟度不符',
    },
    'script.set_directing_id': {
        2: u'本片無此指導方針',
        3: u'請上陣導演',
    },
    'script.upgrade_continued_level': {
        1: u'沒有該劇本',
        2: u'已是最大等級',
        3: u'推廣時間已過',
    },
    'script.finished_summary': {
        1: u'拍片已經結束'
    },
    'script.finished_analyse': {
        1: u'拍片已經結束'
    },
    'script.get_continued_reward': {
        1: u'拍片已經結束'
    },
}

super_player_msg = {
    'super_player.buy_goods': {
        -1: u'參數錯誤',
        1: u'該商品已售完',
        2: u'全服可購買次數不足',
        3: u'個人購買次數達到上限',
    },
    'super_player.index': {
        1: u'沒有配寘，活動未開啟',
    },
    'super_player.get_reward': {
        -1: u'沒有要領取的成就id',
        -2: u'該獎勵已領取',
    },
    'super_player.grab_bag': {
        -1: u'沒有要領取的紅包code',
        1: u'領取時間已過',
        2: u'未到領取時間',
        3: u'已全部領取完畢',
    }
}


script_gacha_msg = {
    'script_gacha.get_gacha': {
        1: u'可抽取次數不足'
    },
}

chapter_stage_msg = {
    'chapter_stage.chapter_stage_fight': {
        1: u'關卡參數錯誤',
        11: u'章節錯誤',
        12: u'難度錯誤',
        13: u'關卡錯誤',
        14: u'配置錯誤',
        15: u'關卡錯誤',
        16: u'剩餘次數不足',
        17: u'體力不足',
        18: u'助戰演員錯誤',
        19: u'角色錯誤',
        20: u'參數錯誤',
        23: u'有未擁有的藝人',
        24: u'等級不夠',
        25: u'關卡錯誤',
        31: u'影片最大票房未達到要求',
        32: u'公司等級未達到要求',
        37: u'卡牌錯誤',
        33: u'有卡牌屬性值不夠',
        34: u'有卡牌性別不符',
        35: u'有卡牌類型不符',
        36: u'有卡牌人氣不足',
    },
    'chapter_stage.auto_sweep': {
        11: u'章節錯誤',
        12: u'難度錯誤',
        13: u'關卡錯誤',
        14: u'配置錯誤',
        15: u'關卡錯誤',
        16: u'剩餘次數不足',
        17: u'體力不足',
        18: u'助戰演員錯誤',
        19: u'角色錯誤',
        20: u'藝人數錯誤',
        21: u'尚未通關',
        22: u'未達到掃蕩星級',
        23: u'有未擁有的藝人',
        24: u'等級不夠',
        25: u'關卡錯誤',
        31: u'影片最大票房未達到要求',
        32: u'公司等級未達到要求',
        37: u'卡牌錯誤',
        33: u'有卡牌屬性值不夠',
        34: u'有卡牌性別不符',
        35: u'有卡牌類型不符',
        36: u'有卡牌人氣不足',
    },
    'chapter_stage.get_dialogue_reward': {
        11: u'劇情關配置錯誤',
        12: u'劇情選擇錯誤',
        13: u'卡牌id錯誤',
    }
}

book_msg = {
    'book.get_card_reward': {
        1: u'組合未完成',
        2: u'組合未完成',
        3: u'獎勵已領',
        4: u'沒有相應組合',
        5: u'獎勵錯誤',
    },
    'book.get_script_reward': {
        1: u'組合未完成',
        2: u'組合未完成',
        3: u'獎勵已領',
        4: u'沒有相應組合',
        5: u'獎勵錯誤',
    },
    'book.get_group_reward': {
        1: u'組合未完成',
        2: u'組合未完成',
        3: u'獎勵已領',
        4: u'沒有相應組合',
        5: u'獎勵錯誤',
    }
}

shop_msg = {
    'shop.index': {
        -1: u'未解鎖',
        2: u'配置錯誤',
    },
    'shop.buy': {
        -1: u'未解鎖',
        2: u'商品錯誤',
        3: u'配置錯誤',
        4: u'購買次數超過上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.refresh_goods': {
        -1: u'未解鎖',
        1: u'我們正在準備進貨，請耐心等待',
        2: u'刷新次數不足',
    },
    'shop.gift_index': {
        -1: u'未解鎖',
        2: u'配置錯誤',
    },
    'shop.gift_buy': {
        -1: u'未解鎖',
        2: u'商品錯誤',
        3: u'配置錯誤',
        4: u'購買次數超過上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.resource_index': {
        -1: u'未解鎖',
        2: u'配置錯誤',
    },
    'shop.resource_buy': {
        -1: u'未解鎖',
        2: u'商品錯誤',
        3: u'配置錯誤',
        4: u'購買次數超過上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.mystical_index': {
        -1: u'未解鎖',
        2: u'配置錯誤',
    },
    'shop.mystical_buy': {
        -1: u'未解鎖',
        2: u'商品錯誤',
        3: u'配置錯誤',
        4: u'購買次數超過上限',
        5: u'商品已下架',
        6: u'商品未上架',
    },
    'shop.mystical_refresh': {
        -1: u'未解鎖',
        1: u'刷新次數也達最大次數',
        2: u'配置錯誤',
        3: u'鑽石不足',
    },
}

block_msg = {
    'block.get_reward': {
        1: u'已領獎',
    },
    'block.get_daily_reward': {
        1: u'已領獎',
        2: u'配置錯誤'
    },
    'block.congratulation': {
        1: u'已祝賀',
    }
}

friend_msg = {
    'friend.actor_chat': {
        1: u'未選擇藝人',
        11: u'當前對話id錯誤',
        13: u'次數超出',
        14: u'當前對話id錯誤',
        15: u'對話配置錯誤',
        16: u'對話選擇錯誤',
        17: u'已選擇過對話',
        18: u'對話已結束',
        19: u'未選擇對話',
        21: u'過普通十關後才能閒聊',
        -1: u'體力不足',
        -2: u'好感度不足',
        -3: u'次數不足',
    },
    'friend.rename': {
        1: u'未指定好友',
        2: u'名字不合法',
        3: u'不是好友',
    },
    'friend.rapport': {
        1: u'未選擇藝人',
        2: u'活動類型錯誤',
        4: u'請選擇約會場景',
        11: u'當前對話id錯誤',
        13: u'次數超出',
        14: u'當前對話id錯誤',
        15: u'對話配置錯誤',
        16: u'對話選擇錯誤',
        17: u'已選擇過對話',
        18: u'對話已結束',
        19: u'未選擇對話',
        -1: u'對話錯誤',
        -2: u'好感不夠',
        -3: u'次數超出',
        -4: u'上次約會尚未完成',
    },
    'friend.apply_friend': {
        1: u'不能添加自己',
        2: u'對方已是自己好友',
        3: u'自己的好友列表已達到上限',
        4: u'用戶不存在',
        5: u'好友的列表已經達到上限',
        6: u'已申請過',
    },
    'friend.search_friend': {
        1: u'uid錯誤',
        2: u'不能查找自己',
        3: u'uid格式不對或不存在',
    },
    'friend.sent_gift': {
        1: u'沒有該好友',
        2: u'已贈送過',
    },
    'friend.receive_gift': {
        1: u'沒有該好友',
        2: u'沒有該好友贈送的體力',
        3: u'體力領取已達上限',
    },
    'friend.agree_friend': {
        1: u'不能添加自己',
        2: u'對方已是自己好友',
        3: u'自己的好友列表已達到上限',
        4: u'對方好友已達到上限',
    },
    'friend.remove_friend': {
        1: u'不能刪除自己',
        2: u'對方不是自己好友',
    },
}

fans_activity_msg = {
    'fans_activity.fans_index': {
        11: u'未舉辦該活動',

    },
    'fans_activity.activity': {
        1: u'沒有藝人參加',
        2: u'未選活動',
        3: u'活動id錯誤',
        11: u'卡牌錯誤',
        12: u'沒有藝人參加',
        13: u'有卡牌屬性值不夠',
        14: u'有卡牌性別不符',
        15: u'有卡牌類型不符',
        16: u'有卡牌人氣不足',
        17: u'美元不足',
        18: u'活動已結束，請先領取獎勵',
        19: u'有卡牌休息中',
    },
    'fans_activity.unlock_activity': {
        1: u'沒有活動',
        2: u'該活動尚不能解鎖',
        3: u'美元不足',
        4: u'已解鎖',
        5: u'首次建築的等級錯誤',
        6: u'此地已有建築',
    },
    'fans_activity.up_activity': {
        1: u'活動等級已經最大',
        2: u'該活動尚不能解鎖',
        3: u'美元不足',
        4: u'活動錯誤',
        5: u'升級id錯誤',
    },
    'fans_activity.get_reward': {
        1: u'請選擇活動',
        2: u'未參加活動',
    },
}

mission_msg = {
    'mission.get_reward': {
        1: u'參數錯誤',
        2: u'未完成',
        3: u'已領',
        4: u'未完成',
    },
    'mission.refresh_mission': {
        1: u'刷新次數不足',
        2: u'任務id未在任務中',
    },
}

active_msg = {
    'active.seven_login': {
        1: u'活動已結束',
    },
    'active.seven_login_award': {
        1: u'條件不足，不能領取',
        2: u'已領取',
        3: u'活動已結束',
    },
    'active.monthly_sign': {
        1: u'已領取',
    },
    'active.active_card_award': {
        1: u'無該配置',
        2: u'尚未啟動',
        3: u'已領取',
        4: u'配置錯誤',
    },
    'active.get_gift': {
        1: u'充值尚未完成，請稍後重試',
        2: u'已經領取過了',
    },
}

code_msg = {
    'code.use_code': {
        1: u'啟動碼錯誤',
        2: u'vip等級不足',
        3: u'這個啟動碼已經被使用過了',
        4: u'活動已過期',
        6: u'不符合領取條件',
        -1: u'您已經領過這個禮包了',
    },
}

pvp_msg = {
    'king_of_song.enemy_battle': {
        -1: u'活動已結束',
        1: u'對手已經拍完',
        2: u'不是可選對手',
    },
    'king_of_song.battle': {
        -1: u'活動已結束',
        1: u'挑戰次數不足',
        2: u'所選劇本不存在',
        3: u'對手還未拍片',
    },
    'king_of_song.get_rank_award': {
        1: u'已領取過此獎勵',
        2: u'勝場次數不足',
    },
    'king_of_song.buy_battle_times': {
        1: u'當日購買次數已到上限',
    },

}

toy_msg = {
    'toy.index': {
        1: u'活動未開啟',
        11: u'vip等級不夠',
    },
    'toy.get_toy': {
        1: u'活動未開啟',
        2: u'娃娃已經被抓走了',
        3: u'娃娃錯誤',
        4: u'道具不足',
        11: u'vip等級不夠',
    },
    'toy.refresh': {
        1: u'活動未開啟',
        2: u'鑽石不足',
        11: u'vip等級不夠',
    },
    'toy.get_rank_reward': {
        1: u'活動未開啟',
        2: u'排行沒有獎勵',
        3: u'獎勵已領',
        11: u'vip等級不夠',
    },
}

carnival_msg = {
    'carnival.index': {
        1: u'活動已結束',
    },
    'carnival.dice': {
        1: u'活動已結束',
        2: u'骰子不足',
        11: u'格子已達最大',
    },
    'carnival.get_dice': {
        1: u'活動已結束',
        2: u'已領取',
        3: u'未完成',
        11: u'任務id錯誤',
    },
}

ranking_list_msg = {
    'ranking_list.get_script_info': {
        1: u'請選擇劇本',
    },
    'ranking_list.get_group_info': {
        1: u'請選擇劇本組',
    },
    'ranking_list.get_reward': {
        1: u'本人沒有排行',
        2: u'已領獎勵',
    },
}

business_msg = {
    'business.handling': {
        1: u'尚不能自動處理',
        2: u'請選擇',
        3: u'已處理完所有事務',
        11: u'配置錯誤',
        12: u'選項錯誤',
    },
}
rest_msg = {
    'rest.rest_index': {
        1: u'參數錯誤',
        17: u'尚未擁有建築',
    },
    'rest.card_rest': {
        1: u'參數錯誤',
        2: u'請選擇位置',
        3: u'請選擇卡牌',
        11: u'位置尚未開啟',
        12: u'位置有藝人休息中',
        13: u'未擁有此卡牌',
        14: u'卡牌已在餐廳中',
        15: u'卡牌已在酒吧中',
        16: u'卡牌已在醫院中',
        17: u'尚未擁有建築',
        18: u'美元不足',
        19: u'藝人狀態良好，不需休息',
        20: u'卡牌正在進行粉絲活動',
        21: u'卡牌正在拍攝中',
        22: u'藝人健康值不足',

    },
    'rest.get_rest_card': {
        1: u'參數錯誤',
        2: u'請選擇位置',
        11: u'位置尚未開啟',
        12: u'位置沒有藝人休息',
        13: u'藝人尚在休息中',
        17: u'尚未擁有建築',
    },
    'rest.done_now': {
        1: u'參數錯誤',
        2: u'請選擇位置',
        11: u'位置尚未開啟',
        12: u'位置沒有藝人休息',
        13: u'藝人已經休息好了',
        17: u'尚未擁有建築',
        18: u'鑽石不足',
    },
    'rest.buy_extra_pos': {
        1: u'參數錯誤',
        11: u'已購買到最大',
        18: u'鑽石不足',
    },
}

director_msg = {
    'director.get_gacha': {
        2: u'道具不足',
        13: u'已達最大次數',
        11: u'cd恢復中',
        12: u'該組導演你已全部招至麾下',
    },
    'director.get_gacha_id': {
        1: u'id錯誤',
        13: u'道具不足',
        11: u'選擇導演未在列表',
        12: u'配置錯誤',
        14: u'已經擁有這個導演',
    },
    'director.up_level': {
        1: u'導演id錯誤',
        11: u'未擁有這個導演',
        12: u'等級已達最大值',
        13: u'道具不足',
    },
    'director.work': {
        1: u'導演id錯誤',
        2: u'位置錯誤',
        11: u'未擁有這個導演',
        12: u'位置尚未開啟',
        13: u'已經有導演坐鎮',
        14: u'已經有導演坐鎮',
    },
    'director.rest': {
        1: u'導演id錯誤',
        11: u'未擁有這個導演',
        12: u'該導演已經在休息了',
    },
    'director.unlock_pos': {
        1: u'位置錯誤',
        13: u'鑽石不足',
        11: u'位置已經開啟',
        12: u'請順序開啟',
    },
    'director.buy_more_gacha_times': {
        13: u'鑽石不足',
    },
}

egg_msg = {
    'egg.egg_index': {
        1: u'活動未開啟',
        2: u'獎品配置錯誤',
    },
    'egg.open_egg': {
        1: u'參數錯誤',
        2: u'獎品配置錯誤',
        3: u'鑽石不足',
        4: u'活動未開啟',
        5: u'彩錘不足',
        6: u'高級金錘數量不足',
        7: u'高級彩錘數量不足',

    },
    'egg.refresh_egg': {
        1: u'活動未開啟',
        2: u'獎品配置錯誤',
        3: u'鑽石不足',
        4: u'參數錯誤',
    }
}

assistant_msg = {
    'assistant.get_daily_reward': {
        1: u'請先聘請終身助理',
        2: u'已經領取',
    },
    'assistant.license_apply': {
        1: u'請先聘請終身助理',
        2: u'申請次數達到上限',
        3: u'申請中',
        4: u'請先領取',
    },
    'assistant.get_license': {
        1: u'請先聘請終身助理',
        2: u'請先申請',
        3: u'申請中',
        4: u'已經領取過了',
        5: u'許可證已達上限',
    }
}

rmb_foundation_msg = {
    'rmb_foundation.rmbfoundation_index': {
        1: u'活動未開啟',
    },
    'rmb_foundation.withdraw': {
        1: u'活動未開啟',
        2: u'參數錯誤',
        3: u'該基金未啟動',
        4: u'無獎勵可領取',
        5: u'基金活動配寘錯誤',
    },
}

foundation_msg = {
    'foundation.foundation_index': {
        1: u'活動未開啟',
    },
    'foundation.withdraw': {
        1: u'活動未開啟',
        2: u'參數錯誤',
        3: u'該基金未啟動',
        4: u'無獎勵可領取',
        5: u'基金活動配寘錯誤',
    },
}

payment_msg = {
    'payment.get_first_charge':{
        1: u'獎勵已領取',
        3: u'未達到條件',
    },
    'payment.get_add_recharge':{
        1: u'活動未開啟',
        2: u'獎勵已領取',
        3: u'未達到條件',
    },
    'payment.add_recharge_index': {
        1: u'活動未開啟',
    },
}

limit_sign_msg = {
    'limit_sign.limit_sign_index': {
        1: u'活動未開啟',
    },
    'limit_sign.get_reward': {
        1: u'活動未開啟',
        2: u'參數錯誤',
        3: u'該獎勵未啟動',
        4: u'該獎勵已經領取',
    },
}

server_limit_sign_msg = {
    'server_limit_sign.limit_sign_index': {
        1: u'活動未開啟',
    },
    'server_limit_sign.get_reward': {
        1: u'活動未開啟',
        2: u'參數錯誤',
        3: u'該獎勵未啟動',
        4: u'該獎勵已經領取',
    },
}

mail_msg = {
    'mail.delete_all': {
        1: u'郵箱已空空如也',
    },
    'mail.get_reward': {
        1: u'郵箱已空空如也',
    },
}

strategy_msg = {
    'strategy.agree': {
        1: u'已經開始合作了',
        2: u'你的戰略合作夥伴已滿',
        3: u'對方戰略合作夥伴已滿',
        4: u'對方等級不足',
    },
    'strategy.quit': {
        1: u'当前没有同他人合作',
    },
    'strategy.choice': {
        1: u'沒有該任務',
        2: u'沒有該任務',
        3: u'該任務已經被領取',
        4: u'完成當前任務才可以領取下一個任務',
        5: u'請先領取上一個任務獎勵再領取該任務',
    },
    'strategy.task_reward': {
        1: u'沒有該任務',
        2: u'沒有該任務',
        3: u'該任務還未完成',
        4: u'已經領取過該獎勵了',
        5: u'只能領取自己接的任務的獎勵',
    },
    'strategy.level_reward': {
        1: u'經理不存在',
        2: u'完成任務數不足',
    },
    'strategy.quick_done': {
        1: u'沒有符合快速完成條件的任務',
        2: u'剩餘次數不足',
    },
    'strategy.help_done': {
        1: u'沒有該任務',
        2: u'沒有該任務',
        3: u'任務已經完成',
        4: u'無主的任務,不能幫忙哦',
        5: u'自己的任務, 快去完成吧',
    },
}

i18n = {
    'user_name': u'明日之星',
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
    'equip_drop_star': u'基因降星材料返還',
    'high_ladder_rank_reward': u'競技場排名獎勵',
    'mercenary': u'傭兵營地',
    'charge': u'充值獎勵',
    'level_gift': u'限時等級禮包',
    'invest': u'零用錢銀行',
    'first_recharge': u'首充禮包',
    'biography': u'傳記',
    'star_reward': u'星芒法陣每日獎勵',
    'recruit_title': u'招募有禮獎勵',
    'recruit_des': u'您有“招募有禮”活動獎勵未領取，特郵件發送給您，請查收。',
    'active_gacha_title': u'多次招募送碎片獎勵',
    'active_gacha_des': u'您有“多次招募送機甲蘿莉碎片”活動獎勵未領取，特郵件發送給您，請查收。',
    'sign_recharge_title': u'連續充值',
    'sign_recharge_des': u'親愛的玩家，您昨日參與連續充值的獎勵未領取，特郵件發送給您，請查收。',
    'daily_package': u'每日禮包',
    'decisive_battle_title': u'爭霸賽排名獎勵',
    'decisive_battle_des': u'恭喜你在爭霸賽中取得了第%d名，獎勵如下：',
    'pay_sign_title': u'超值簽到補發',
    'pay_sign_des': u'您昨日有未領取的超值簽到獎勵，現補發給您，請查收~',
    'doomsday_hunt': u'猛獸通緝令',
    'hunt_box': u'您的寶箱獎勵未領取，請查收',
    'limit_discount': u'限時特惠禮包',
    'challenge_rank': u'極限挑戰排名獎',
    'script_luck_buff': u'恭喜玩家 %s 最新影片《%s》把握住了市場脈搏，票房極大提升！',
    'script_luck_debuff': u'由於當前市場同類型作品過多，您的影片《%s》未能達到預期票房。',
    'add_recharge': u'累計充值禮包',

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
    37: u'內側充值返利',
    38: u'''指揮官大人：
    這是您參與內側充值返利的雙倍鑽石，請接收~
                                機要秘書---琳''',
    39: u'VIP專屬通知',
    40: u'''指揮官大人：
    恭喜您達到VIP8，請您添加VIP專屬客服QQ：800042348，我們會有專人為您解答問題並領取VIP豪華大禮包~
                                機要秘書---琳''',
    41: u'恭喜獲得極限挑戰每日排名第%s名',
    42: u'恭喜獲得極限挑戰每期排名第%s名',
    43: u'',
    44: u'您未領取的累充獎勵',
    1001: u'金幣',
    1002: u'鑽石',
    1003: u'體力',
    1004: u'美元',
    1007: u'點贊數',
    1011: u'玩家經驗',
    1012: u'工會資金',
    1013: u'工會貢獻',
    1014: u'vip經驗',
    1015: u'可拍攝劇本',
    1016: u'點贊',
    1018: u'藝人名片',
    1019: u'關注度',
    1020: u'卡牌人氣',
    1102: u'成就點',
    1101: u'目標點',
    1208: u'%s的%s 分享了紅包，快去超級大玩家搶吧',
    1209: u'已經起好名字了！請重新登入!',
    1210: u'群星紀念塔樓建到%s層解鎖',
    1211: u'活動已經結束，開服第%s天',
    1213: u'恭喜您在超級大玩家活動中發紅包全服排名第%s名，獲得獎勵:',
    1214: u'超級大玩家獎勵',
    1301: u'<#6cbaf4>%s<#ffffff>在砸金蛋活動中，使用高級金錘，獲得<#f65891>%s',
    1302: u'<#6cbaf4>%s<#ffffff>砸金蛋人品爆發，獲得<#f65891>%s',
    1303: u'<#6cbaf4>%s<#ffffff>在砸金蛋活動中，使用高級彩錘，獲得<#f65891>%s',
    1304: u'<#6cbaf4>%s<#ffffff>砸彩蛋人品爆發，獲得<#f65891>%s',
}
# 注册需要写到最下面
register_handler()
