#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 命名规则 xxx_mapping

import re


def register_mapping_config(source, target):
    """ 注册提示消息

    :param source: 原 {}
    :param target: 目标 {}
    """
    for k, v in target.iteritems():
        if k in source:
            raise RuntimeError("config [%s] Already exists in %s" % (k, __file__))
        source[k] = v
    target.clear()

    # source.update(target)
    # target.clear()


def register_handler():
    match = re.compile('^[a-zA-Z0-9_]+_mapping$').match
    g = globals()
    mapping = g['mapping_config']
    for name, value in g.iteritems():
        if match(name):
            register_mapping_config(mapping, value)


mapping_config = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'name': (None, True),     # simple
    'ban_ip': ('ban_ip', True),
    'common': ('common', True),

}

hero_bdc_channel_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'hero_channel_config': ('hero_channel_config', True),
}

card_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'card_basis': ('card_basis', True),
    'card_level': ('card_level', True),
    'card_script_exp': ('card_script_exp', True),
    'card_level_grow': ('card_level_grow', True),
    'card_love_level': ('card_love_level', True),

    'card_love_grow': ('card_love_grow', True),
    'card_love_gift': ('card_love_gift', True),
    'card_love_gift_taste': ('card_love_gift_taste', True),
    'card_train_cost': ('card_train_cost', True),
    'card_train_grow': ('card_train_grow', True),
    'card_train_type': ('card_train_type', True),
    'card_piece': ('card_piece', True),
    'card_quality': ('card_quality', True),
    'card_repick': ('card_repick', True),

}

name_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'card_name': ('card_name', True),
    'script_name': ('script_name', True),
    'nic_name': ('nic_name', True),
}

gacha_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'coin_gacha': ('coin_gacha', True),
    'coin_gacha_lv': ('coin_gacha_lv', True),
    'coin_gacha_cd': ('coin_gacha_cd', True),

    # 'gacha': ('gacha', True),
    # 'gacha_vip': ('gacha_vip', True),
    # 'gacha_prize': ('gacha_prize', True),
    # 'gacha_board': ('gacha_board', True),
    # 'diamond_gacha': ('diamond_gacha', True),
    # 'box_gacha': ('box_gacha', True),
    # 'vip_gacha_rate': ('vip_gacha_rate', True),

    # 'diamond_gacha_score': ('diamond_gacha_score', True),
    # 'box_gacha_score': ('box_gacha_score', True),
}

plot_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'E_dialogue_words': ('E_dialogue_words', True),
    # 'P_dialogue_words': ('P_dialogue_words', True),

    'avg_dialogue': ('avg_dialogue', True),
    'phone_daily_dialogue': ('phone_daily_dialogue', True),
    'phone_dialogue': ('phone_dialogue', True),
    'phone_chapter_dialogue': ('phone_chapter_dialogue', True),
    'tour_dialogue': ('tour_dialogue', True),
    'explain': ('explain', True),
    'dinner_begin': ('dinner_begin', True),
    'dinner_in': ('dinner_in', True),
    'date_chapter': ('date_chapter', True),

    # 'ad': ('ad', True),
    # 'ad_text': ('ad_text', True),
    # 'dialogue_chapter': ('dialogue_chapter', True),
    # 'dialogue_role': ('dialogue_role', True),
    # 'animation_words': ('animation_words', True),
    # 'monster_talk': ('monster_talk', True),
    # 'animation_chapter': ('animation_chapter', True),
    # 'hero_talk': ('hero_talk', True),
    # 'chapter_words': ('chapter_words', True),
    # 'dialogue_guide_team': ('dialogue_guide_team', True),
    # 'dialogue_guide': ('dialogue_guide', True),
    # 'opera_awards': ('opera_awards', True),
    # 'opera_click': ('opera_click', True),
    # 'opera': ('opera', True),
    # 'opera_location': ('opera_location', True),
    # 'pda': ('pda', True),
    # 'avg_opera': ('avg_opera', True),
    # 'avg_note': ('avg_note', True),
}

script_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'script': ('script', True),
    'script_style_suit': ('script_style_suit', True),
    'script_style': ('script_style', True),
    'script_type_style': ('script_type_style', True),
    'script_role': ('script_role', True),
    'script_end_level': ('script_end_level', True),
    'script_continued_level': ('script_continued_level', True),
    'script_market': ('script_market', True),
    'script_curve': ('script_curve', True),
    'script_license': ('script_license', False),
    'script_gacha': ('script_gacha', True),
    'diamond_script_gacha': ('diamond_script_gacha', True),
    'script_gacha_cd': ('script_gacha_cd', True),
    'script_gacha_cost': ('script_gacha_cost', True),
    'attention_level': ('attention_level', True),
    'difficulty_level': ('difficulty_level', True),

    'audi_comment_choice': ('audi_comment_choice', True),
    'media_comment': ('media_comment', True),
    'audi_comment': ('audi_comment', True),
    'barrage': ('barrage', True),

    'random_event': ('random_event', True),
    'global_market': ('global_market', True),


}

king_of_song_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'pvp_rank': ('pvp_rank', True),
    'pvp_robots': ('pvp_robots', True),
    'singerking_rate': ('singerking_rate', False),
}

equip_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'equip': ('equip', True),
    'equip_piece': ('equip_piece', True),
}

chapter_stage_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'chapter_stage': ('chapter_stage', True),
    'chapter': ('chapter', True),
    'chapter_enemy': ('chapter_enemy', True),
}

shop_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'shop_goods': ('shop_goods', True),
    'shop_id': ('shop_id', True),
    'mystical_store_cd': ('mystical_store_cd', True),
    'price_ladder': ('price_ladder', True),
}

book_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'card_book': ('card_book', True),
    'script_book': ('script_book', True),
    'script_group_object': ('script_group_object', True),
}

danmu_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'danmu': ('danmu', True),
    'dan_word2': ('dan_word2', True),
    'danmu_pve': ('danmu_pve', True),
}

item_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'grade_lvlup_item': ('grade_lvlup_item', True),
    'use_item': ('use_item', True),
    'use_item_box': ('use_item_box', True),
    # 'collection_resource': ('collection_resource', True),
    'special_use_item': ('special_use_item', True),
}

equip_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'equip_basis': ('equip_basis', True),
    # 'equip_lvlup': ('equip_lvlup', True),
    # 'equip_random': ('equip_random', True),
    # 'equip_suit': ('equip_suit', True),
    # 'equip_color': ('equip_color', True),
    # 'equip_grade': ('equip_grade', True),
    # 'equip_refine': ('equip_refine', True),
}

user_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'server_type': ('server_type', True),
    'tag': ('tag', True),
    'tag_score': ('tag_score', True),
    'player_level': ('player_level', True),
    'vip': ('vip', True),
    'initial_account': ('initial_account', False),
    'main_hero': ('main_hero', True),
    'action_exp': ('action_exp', True),
    'vip_pay': ('vip_pay', True),
    'city_inside': ('city_inside', True),
    'city_pos': ('city_pos', True),
    'speed_up_cost': ('speed_up_cost', True),
    'building_unlock': ('building_unlock', True),
    'charge': ('charge', True),
    'month_privilege': ('month_privilege', True),
    'charge_ios': ('charge_ios', True),
    'currency_exchange': ('currency_exchange', True),
    'value': ('value', True),
    'privilege': ('privilege', True),
    # 'charge_privilege': ('charge_privilege', True),
    # 'guide': ('guide', True),
    'guide_unlock': ('guide_unlock', True),
    'jump': ('jump', True),
    'item_coin': ('item_coin', True),
    'mission_guide': ('mission_guide', True),
    # 'guide_team': ('guide_team', True),
    # 'initial_data': ('initial_data', True),
    'first_random_name': ('first_random_name', True),
    'last_random_name': ('last_random_name', True),
    # 'drama': ('drama', True),

    # 'test_config': ('test_config', True),
    'version': ('version', True),
    'team_skill': ('team_skill', True),
    'skill_stone': ('skill_stone', True),
    'title': ('title', True),
    'player_icon': ('player_icon', True),
    'dirtyword_ch': ('dirtyword_ch', True),
    'homepage_button': ('homepage_button', True),
    'message': ('message', True),
    'common_attention': ('common_attention', True),
    'play_help': ('play_help', True),
    'push_message': ('push_message', True),
    'level_mail': ('level_mail', True),
    'level_gift': ('level_gift', True),
    'team_skill_mastery': ('team_skill_mastery', True),
    'team_skill_mastery_up': ('team_skill_mastery_up', True),
    'server_inreview': ('server_inreview', True),
    'gold_exchange': ('gold_exchange', True),
    'team_skill_lvl_up': ('team_skill_lvl_up', True),
    'team_skill_unlock': ('team_skill_unlock', True),
    'loading_des': ('loading_des', True),
    'loading_gif': ('loading_gif', True),
    'help': ('help', True),
    'login_reward_id': ('login_reward_id', True),
    'money_guide': ('money_guide', True),
}

#
# guild_mapping = {
#     # key 为 config_name, value: 表名, 前端是否能看的
#     'guild_build': ('guild_build', True),
#     'guild_info': ('guild_info', True),
#     'guild_protect_money': ('guild_protect_money', True),
#     'guild_technology_lvlup': ('guild_technology_lvlup', True),
#     'guild_technology': ('guild_technology', True),
#     'guild_war': ('guild_war', True),
#     'guild_war_theme': ('guild_war_theme', True),
#     'guild_war_reward': ('guild_war_reward', True),
#     'guild_war_rank_reward': ('guild_war_rank_reward', True),
#     'guild_icon': ('guild_icon', True),
#     'guild_boss_reward': ('guild_boss_reward', True),
#     'guild_boss_coin': ('guild_boss_coin', True),
#     'guild_boss_exp': ('guild_boss_exp', True),
#     'guild_donate': ('guild_donate', True),
#     'guild_texas': ('guild_texas', True),
#     'guild_texas_reward': ('guild_texas_reward', True),
#     'guild_texas_point_reward': ('guild_texas_point_reward', True),
#     'guild_boss_killreward': ('guild_boss_killreward', True),
#     'guild_boss_breakreward': ('guild_boss_breakreward', True),
#     'guild_boss_rankreward': ('guild_boss_rankreward', True),
#     'guild_boss_hp': ('guild_boss_hp', True),
# }



friend_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'friend_cheer': ('friend_cheer', True),
    # 'friend_clean': ('friend_clean', True),
    # 'redpacket': ('redpacket', True),
    # 'friend_point': ('friend_point', True),
}

market_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'market': ('market', True),
    # 'market_type': ('market_type', True),
}

active_mapping = {
    #     # key 为 config_name, value: 表名, 前端是否能看的
    #     'mission_main': ('mission_main', True),
    #     'mission_side': ('mission_side', True),
    #     'mission_record': ('mission_record', True),
    #     'slg_task_daily': ('slg_task_daily', True),
    #     'slg_rank_reward': ('slg_rank_reward', True),
    #     'log_reward': ('log_reward', True),
    #     'guild_task': ('guild_task', True),
    #     'person_task': ('person_task', True),
    #     'score_reward': ('score_reward', True),
    #     'rank_reward': ('rank_reward', True),
    #     # 'score_reward_pool': ('score_reward_pool', True),
    #     'task_main': ('task_main', True),
    #     'task_main_detail': ('task_main_detail', True),
    #     'shoot_plank': ('shoot_plank', True),
    #     'server_shoot_plank': ('server_shoot_plank', True),
    #     'super_all': ('super_all', True),
    #     'super_rich': ('super_rich', True),
    #     'task_random': ('task_random', True),
    #     'achievement': ('achievement', True),
    #     'achievement_collection': ('achievement_collection', True),
    #     'task_daily': ('task_daily', True),
    #     'task_daily_reward': ('task_daily_reward', True),
    #     'diamond_get': ('diamond_get', True),
    #     'server_diamond_get': ('server_diamond_get', True),
    #     'invest': ('invest', True),
    #     'invest_rate': ('invest_rate', True),
    #     'server_invest': ('server_invest', True),
    #     'server_invest_rate': ('server_invest_rate', True),
    #     'daily_reward': ('daily_reward', True),
    #     # 'active_show': ('active_show', True),
    #     'gift_show': ('gift_show', True),
    #     # 'buy_reward': ('buy_reward', True),
    'first_recharge': ('first_recharge', True),
    #     'daily_charge': ('daily_charge', True),
    #     'points_exchange': ('points_exchange', True),
    #     'star_task': ('star_task', True),
    #     'server_points_exchange': ('server_points_exchange', True),
    #     'server_star_task': ('server_star_task', True),
    #     'active_consume': ('active_consume', True),
    #     'active_daily_consume': ('active_daily_consume', True),
    #     'active_recharge': ('active_recharge', True),
    #     'active_daily_recharge': ('active_daily_recharge', True),
    #     'normal_exchange': ('normal_exchange', True),
    #     'omni_exchange': ('omni_exchange', True),
    #     'sign_daily_charge': ('sign_daily_charge', True),
    #     'active_show': ('active_show', True),
    #     'gacha_reward_hero': ('gacha_reward_hero', True),
    #     'gacha_reward': ('gacha_reward', True),
    #     'month_card': ('month_card', True),
        'active_inreview': ('active_inreview', True),
    #     'limit_weapon': ('limit_weapon', True),
    #     'limit_box_reward': ('limit_box_reward', True),
    #     'limit_box_shop': ('limit_box_shop', True),
    #     'limit_hero_score': ('limit_hero_score', True),
    #     'limit_hero_rank': ('limit_hero_rank', True),
    #     'limit_card_chip': ('limit_card_chip', True),
    #     'limit_diamond_gacha': ('limit_diamond_gacha', True),
    #     'limit_gacha': ('limit_gacha', True),
    #     'extra_hero': ('extra_hero', True),
    #     'hero_description': ('hero_description', True),
    #     'server_limit_weapon': ('server_limit_weapon', True),
    #     'server_limit_box_reward': ('server_limit_box_reward', True),
    #     'server_limit_box_shop': ('server_limit_box_shop', True),
    #     'server_limit_hero_score': ('server_limit_hero_score', True),
    #     'server_limit_hero_rank': ('server_limit_hero_rank', True),
    #     'server_limit_card_chip': ('server_limit_card_chip', True),
    #     'server_limit_diamond_gacha': ('server_limit_diamond_gacha', True),
    #     'server_limit_gacha': ('server_limit_gacha', True),
    #     'server_extra_hero': ('server_extra_hero', True),
    #     'server_hero_description': ('server_hero_description', True),
    #     'honor_shop_new': ('honor_shop_new', True),
    'sign_first_week': ('sign_first_week', True),
    'sign_daily_normal': ('sign_daily_normal', True),
    'active': ('active', True),
}

daily_activity_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'daily_nightmares': ('daily_nightmares', True),
    # 'daily_rewards_nightmares': ('daily_rewards_nightmares', True),
    # 'daily_boss': ('daily_boss', True),
    # 'daily_rewards_boss': ('daily_rewards_boss', True),
    'daily_advance': ('daily_advance', True),
    'sign_reward': ('sign_reward', True),
    'sign_final_reward': ('sign_final_reward', True),
    'sign_reward_coin': ('sign_reward_coin', True),
    'sign_final_reward_coin': ('sign_final_reward_coin', True),
    'growth_fund': ('growth_fund', True),
    'growth_fund_reward': ('growth_fund_reward', True),
    'daily_activity': ('daily_activity', True),
    'growth_fund_all': ('growth_fund_all', True),
    'growth_fund_water': ('growth_fund_water', True),
}

code_mapping = {
    'code': ('code', True),
}

home_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'home_main': ('home_main', True),
    'home_dressup_sort': ('home_dressup_sort', True),
    'home_dressup_detail': ('home_dressup_detail', True),
    'home_flower_reward': ('home_flower_reward', True),
    'home_flsend_reward': ('home_flsend_reward', True),
}

language_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'ZH_CN': ('ZH_CN', True),
    'ZH_TW': ('ZH_TW', True),
    'ZH_CN_FOREND': ('ZH_CN_FOREND', True),
    'ZH_TW_FOREND': ('ZH_TW_FOREND', True),
    'ZH_TW_YUNYING': ('ZH_TW_YUNYING', True),
    'ZH_CN_YUNYING': ('ZH_CN_YUNYING', True),
}

server_active_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'server_consume': ('server_consume', True),
    'server_daily_consume': ('server_daily_consume', True),
    'server_recharge': ('server_recharge', True),
    'server_daily_recharge': ('server_daily_recharge', True),
    'server_normal_exchange': ('server_normal_exchange', True),
    'server_omni_exchange': ('server_omni_exchange', True),
    'server_sign_daily_charge': ('server_sign_daily_charge', True),
    'server_active_show': ('server_active_show', True),
    'server_daily_charge': ('server_daily_charge', True),
    'server_daily_reward': ('server_daily_reward', True),
    'server_gift_show': ('server_gift_show', True),
    'server_buy_reward': ('server_buy_reward', True),
}

leading_role_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的

    'main_hero_evo': ('main_hero_evo', True),
    'main_hero_medal': ('main_hero_medal', True),
    'main_hero_medal_evo': ('main_hero_medal_evo', True),
    'main_hero_skill_combine': ('main_hero_skill_combine', True),
    'main_hero_skill': ('main_hero_skill', True),
    'main_hero_medal_milestone': ('main_hero_medal_milestone', True),
    'machine': ('machine', True),
}

challenge_mapping = {
    'challenge_theme': ('challenge_theme', True),
    'battle_reward': ('battle_reward', True),
    'rank_reward_daily': ('rank_reward_daily', True),
    'uc_rank_reward': ('uc_rank_reward', True),
}

server_celebrate_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'rank_reward_show': ('rank_reward_show', True),
    'level_rank': ('level_rank', True),
    'level_reward': ('level_reward', True),
    'combat_rank': ('combat_rank', True),
    'combat_reward': ('combat_reward', True),
    'prison_reward': ('prison_reward', True),
    'get_equip': ('get_equip', True),
    'get_skill': ('get_skill', True),
    'pvp_reward': ('pvp_reward', True),
    'hero_star_recharge': ('hero_star_recharge', True),
}

limit_discount_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'limit_discount': ('limit_discount', True),
    'server_limit_discount': ('server_limit_discount', True),
    'red_bag': ('red_bag', True),
    'server_red_bag': ('server_red_bag', True),
}

rank_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'rank_reward_list': ('rank_reward_list', True),
    'dan_grading_list': ('dan_grading_list', True),
    'cup_num': ('cup_num', True),
    'dan_grading_privilage': ('dan_grading_privilage', True),
}

fans_activity_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'fans_activity': ('fans_activity', True),
}

mission_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'liveness_reward': ('liveness_reward', True),
    'liveness': ('liveness', True),
    'box_office': ('box_office', True),
    'guide_mission': ('guide_mission', True),
    'random_mission': ('random_mission', True),
    'achieve_mission': ('achieve_mission', True),
    'new_guide_mission': ('new_guide_mission', True),
}

build_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'card_building': ('card_building', True),
    'building': ('building', True),
    'field': ('field', True),
    'functional_building': ('functional_building', True),
    'rest': ('rest', True),
}

guide_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'guide': ('guide', True),
    'guide_team': ('guide_team', True),
    'dialogue_guide_team': ('dialogue_guide_team', True),
    'dialogue_guide': ('dialogue_guide', True),
}

carvinal_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'carnival_mission': ('carnival_mission', True),
    'carnival_new_reward': ('carnival_new_reward', True),
    'carnival_old_reward': ('carnival_old_reward', True),
    'carnival_days': ('carnival_days', True),
    'carnival_random': ('carnival_random', True),
}

toy_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'rmb_gacha': ('rmb_gacha', True),
    'rmb_gacha_cost': ('rmb_gacha_cost', True),
    'rmb_gacha_control': ('rmb_gacha_control', True),
    'free_gacha': ('free_gacha', True),
    'free_gacha_cost': ('free_gacha_cost', True),
    'free_gacha_control': ('free_gacha_control', True),
    'rmb_gacha_rank': ('rmb_gacha_rank', True),
}

gift_center_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'welfare_notice': ('welfare_notice', True),
    'scroll_bar': ('scroll_bar', True),
}

business_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'business': ('business', True),
    'business_times': ('business_times', True),
}

# 注册需要写到最下面
register_handler()
