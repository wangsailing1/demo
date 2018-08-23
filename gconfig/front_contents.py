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
}


user_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'server_type': ('server_type', True),

}

hero_bdc_channel_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'hero_channel_config': ('hero_channel_config', True),
}


stage_task_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'stage_task_main': ('stage_task_main', True),
    'stage_task_details': ('stage_task_details', True),
    'stage_task_info': ('stage_task_info', True),
}


danmu_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'danmu': ('danmu', True),
    'dan_word2': ('dan_word2', True),
    'danmu_pve': ('danmu_pve', True),
}


hero_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'hero_basis': ('hero_basis', True),
    'hero_growth_rate': ('hero_growth_rate', True),
    'hero_exp': ('hero_exp', True),
    'hero_lvl_limit': ('hero_lvl_limit', True),
    'hero_stone': ('hero_stone', True),
    'grade_lvlup_badge': ('grade_lvlup_badge', True),
    'grade_lvlup_reward': ('grade_lvlup_reward', True),
    'grade_lvlup_reward_new': ('grade_lvlup_reward_new', True),
    'hero_attribute': ('hero_attribute', True),
    'skill_detail': ('skill_detail', True),
    'skill_buff': ('skill_buff', True),
    'skill_lvlup_cost': ('skill_lvlup_cost', True),
    'skill_growth_rate': ('skill_growth_rate', True),
    # 'skill_big_basis': ('skill_big_basis', True),
    'skill_normal_basis': ('skill_normal_basis', True),
    'passive_skill': ('passive_skill', True),
    # 'extra_skill': ('extra_skill', True),
    # 'extra_skill_exp': ('extra_skill_exp', True),
    # 'extra_skill_growth': ('extra_skill_growth', True),
    # 'collection_skill': ('collection_skill', True),
    # 'manufacture_skill': ('manufacture_skill', True),
    'hero_grade_rate': ('hero_grade_rate', True),
    'npc': ('npc', True),
    'npc_show': ('npc_show', True),
    'hero_quanlity': ('hero_quanlity', True),
    # 'skill_effect': ('skill_effect', True),
    'pokedex': ('pokedex', True),
    'pokedex_hero': ('pokedex_hero', True),
    'hero_milestone': ('hero_milestone', True),
    'milestone': ('milestone', True),
    'skill_detail_upgrade': ('skill_detail_upgrade', True),
    'hero_story': ('hero_story', True),
    'assistant_hero': ('assistant_hero', True),
    'chain': ('chain', True),
    'skill_enemy': ('skill_enemy', True),
    'hero_favor': ('hero_favor', True),
    'hero_favor_grade': ('hero_favor_grade', True),
    'hero_star_rate': ('hero_star_rate', True),
    'hero_star_passive': ('hero_star_passive', True),
    'hero_star': ('hero_star', True),
    'personality': ('personality', True),
    'hero_character': ('hero_character', True),
}


item_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'grade_lvlup_item': ('grade_lvlup_item', True),
    'use_item': ('use_item', True),
    'use_item_box': ('use_item_box', True),
    # 'collection_resource': ('collection_resource', True),
    'special_use_item': ('special_use_item', True),
}


battle_item_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'battle_item_pro': ('battle_item_pro', True),
    # 'battle_item_skill': ('battle_item_skill', True),
    # 'battle_item_layer': ('battle_item_layer', True),
    # 'battle_item_bank': ('battle_item_bank', True),
    # 'battle_item_limit': ('battle_item_limit', True),
    # 'battle_item_oppo': ('battle_item_oppo', True),
    # 'add_battle_item': ('add_battle_item', True),
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


new_equip_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'new_equip_detail': ('new_equip_detail', True),
    'new_equip_grade': ('new_equip_grade', True),
    'new_equip_awake': ('new_equip_awake', True),
}


gene_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'gene_basis': ('gene_basis', True),
    'gene_suit': ('gene_suit', True),
    'gene_random': ('gene_random', True),
    'gene_lvlup': ('gene_lvlup', True),
    'gene_starup': ('gene_starup', True),
    'gene_evoup': ('gene_evoup', True),
    'piece_equip': ('piece_equip', True),
}


collection_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'activity_dialogue': ('activity_dialogue', True),
    # 'collection_weary': ('collection_weary', True),
    # 'resource_exchange': ('resource_exchange', True),
}


user_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'server_type': ('server_type', True),

    'action_exp': ('action_exp', True),
    'vip': ('vip', True),
    'vip_pay': ('vip_pay', True),
    'city_inside': ('city_inside', True),
    'city_pos': ('city_pos', True),
    'speed_up_cost': ('speed_up_cost', True),
    'building_unlock': ('building_unlock', True),
    'charge': ('charge', True),
    'charge_ios': ('charge_ios', True),
    'currency_exchange': ('currency_exchange', True),
    'value': ('value', True),
    'privilege': ('privilege', True),
    # 'charge_privilege': ('charge_privilege', True),
    'guide': ('guide', True),
    'guide_unlock': ('guide_unlock', True),
    'jump': ('jump', True),
    'item_coin': ('item_coin', True),
    'mission_guide': ('mission_guide', True),
    'guide_team': ('guide_team', True),
    # 'initial_data': ('initial_data', True),
    'first_random_name': ('first_random_name', True),
    'last_random_name': ('last_random_name', True),
    # 'drama': ('drama', True),

    # 'test_config': ('test_config', True),
    # 'version': ('version', True),
    'team_skill': ('team_skill', True),
    'skill_stone': ('skill_stone', True),
    'title': ('title', True),
    'player_icon': ('player_icon', True),
    # 'dirtyword_ch': ('dirtyword_ch', True),
    'homepage_button': ('homepage_button', True),
    'message': ('message', True),
    'play_help': ('play_help', True),
    'push_message': ('push_message', True),
    # 'level_mail': ('level_mail', True),
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
}


manufacture_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'manufacture': ('manufacture', True),
    'manufacture_weary': ('manufacture_weary', True),
    # 'manufacture_star': ('manufacture_star', True),
    'manufacture_stone': ('manufacture_stone', True),
    # 'collection_manufacture': ('collection_manufacture', True),
}


battle_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'crit_atk_suppress': ('crit_atk_suppress', True),
    # 'crit_def_suppress': ('crit_def_suppress', True),
    'damage_suppress': ('damage_suppress', True),
    # 'dodge_suppress': ('dodge_suppress', True),
    'hit_suppress': ('hit_suppress', True),
    'fight': ('fight', True),
    'protect_skill_cost': ('protect_skill_cost', True),
    'protect_skill_detail': ('protect_skill_detail', True),
    'protect_skill_attr_rate': ('protect_skill_attr_rate', True),
}


private_city_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'chapter': ('chapter', True),
    'chapter_stage': ('chapter_stage', True),
    'chapter_to_stage': ('chapter_to_stage', True),
    'chapter_star': ('chapter_star', True),
    # 'chapter_lose': ('chapter_lose', True),
    'enemy_basis': ('enemy_basis', True),
    # 'boss': ('boss', True),
    'chain_story': ('chain_story', True),
    'chain_story_content': ('chain_story_content', True),
    'awaken_chapter': ('awaken_chapter', True),
    'chapter_enemy': ('chapter_enemy', True),
    'activity_enemy': ('activity_enemy', True),
    # 'chapter_single_mail': ('chapter_single_mail', True),
    # 'chapter_double_mail': ('chapter_double_mail', True),
    'awaken_group': ('awaken_group', True),
    'battle_story': ('battle_story', True),
}


plot_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'E_dialogue_words': ('E_dialogue_words', True),
    # 'P_dialogue_words': ('P_dialogue_words', True),
    'ad': ('ad', True),
    'ad_text': ('ad_text', True),
    'dialogue_chapter': ('dialogue_chapter', True),
    'dialogue_role': ('dialogue_role', True),
    'animation_words': ('animation_words', True),
    'monster_talk': ('monster_talk', True),
    'animation_chapter': ('animation_chapter', True),
    'hero_talk': ('hero_talk', True),
    'chapter_words': ('chapter_words', True),
    'dialogue_guide_team': ('dialogue_guide_team', True),
    'dialogue_guide': ('dialogue_guide', True),
    'opera_awards': ('opera_awards', True),
    'opera_click': ('opera_click', True),
    'opera': ('opera', True),
    'opera_location': ('opera_location', True),
    'pda': ('pda', True),
    'avg_dialogue': ('avg_dialogue', True),
    'avg_opera': ('avg_opera', True),
    'avg_note': ('avg_note', True),
}


guild_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'guild_build': ('guild_build', True),
    'guild_info': ('guild_info', True),
    'guild_protect_money': ('guild_protect_money', True),
    'guild_technology_lvlup': ('guild_technology_lvlup', True),
    'guild_technology': ('guild_technology', True),
    'guild_war': ('guild_war', True),
    'guild_war_theme': ('guild_war_theme', True),
    'guild_war_reward': ('guild_war_reward', True),
    'guild_war_rank_reward': ('guild_war_rank_reward', True),
    'guild_icon': ('guild_icon', True),
    'guild_boss_reward': ('guild_boss_reward', True),
    'guild_boss_coin': ('guild_boss_coin', True),
    'guild_boss_exp': ('guild_boss_exp', True),
    'guild_donate': ('guild_donate', True),
    'guild_texas': ('guild_texas', True),
    'guild_texas_reward': ('guild_texas_reward', True),
    'guild_texas_point_reward': ('guild_texas_point_reward', True),
    'guild_boss_killreward': ('guild_boss_killreward', True),
    'guild_boss_breakreward': ('guild_boss_breakreward', True),
    'guild_boss_rankreward': ('guild_boss_rankreward', True),
    'guild_boss_hp': ('guild_boss_hp', True),
}


shop_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'shop_sell': ('shop_sell', False),
    # 'period_shop': ('period_shop', False),
    # 'darkstreet_shop': ('darkstreet_shop', False),
    # 'guild_shop': ('guild_shop', True),
    # 'rally_shop': ('rally_shop', True),
    # 'arena_shop': ('arena_shop', True),
    # 'donate_shop': ('donate_shop', True),
    # 'shop_box': ('shop_box', True),
}


gacha_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'gacha': ('gacha', True),
    # 'gacha_vip': ('gacha_vip', True),
    # 'gacha_prize': ('gacha_prize', True),
    # 'gacha_board': ('gacha_board', True),
    'diamond_gacha': ('diamond_gacha', True),
    'box_gacha': ('box_gacha', True),
    # 'vip_gacha_rate': ('vip_gacha_rate', True),
    'coin_gacha': ('coin_gacha', True),
    'diamond_gacha_score': ('diamond_gacha_score', True),
    'box_gacha_score': ('box_gacha_score', True),
}

pvp_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'pvp_arena': ('pvp_arena', True),
    'text': ('text', True),
    # 'robots': ('robots', True),
    # 'darkstreet_reward_round': ('darkstreet_reward_round', True),
    'darkstreet_fight': ('darkstreet_fight', True),
    'darkstreet_reward_break': ('darkstreet_reward_break', True),
    'darkstreet_milestone': ('darkstreet_milestone', True),
    'arena_milestone_reward': ('arena_milestone_reward', True),
}

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
    # key 为 config_name, value: 表名, 前端是否能看的
    'mission_main': ('mission_main', True),
    'mission_side': ('mission_side', True),
    'mission_record': ('mission_record', True),
    'slg_task_daily': ('slg_task_daily', True),
    'slg_rank_reward': ('slg_rank_reward', True),
    'log_reward': ('log_reward', True),
    'guild_task': ('guild_task', True),
    'person_task': ('person_task', True),
    'score_reward': ('score_reward', True),
    'rank_reward': ('rank_reward', True),
    # 'score_reward_pool': ('score_reward_pool', True),
    'task_main': ('task_main', True),
    'task_main_detail': ('task_main_detail', True),
    'shoot_plank': ('shoot_plank', True),
    'server_shoot_plank': ('server_shoot_plank', True),
    'super_all': ('super_all', True),
    'super_rich': ('super_rich', True),
    'task_random': ('task_random', True),
    'achievement': ('achievement', True),
    'achievement_collection': ('achievement_collection', True),
    'task_daily': ('task_daily', True),
    'task_daily_reward': ('task_daily_reward', True),
    'diamond_get': ('diamond_get', True),
    'server_diamond_get': ('server_diamond_get', True),
    'invest': ('invest', True),
    'invest_rate': ('invest_rate', True),
    'server_invest': ('server_invest', True),
    'server_invest_rate': ('server_invest_rate', True),
    'daily_reward': ('daily_reward', True),
    # 'active_show': ('active_show', True),
    'gift_show': ('gift_show', True),
    # 'buy_reward': ('buy_reward', True),
    'first_recharge': ('first_recharge', True),
    'daily_charge': ('daily_charge', True),
    'points_exchange': ('points_exchange', True),
    'star_task': ('star_task', True),
    'server_points_exchange': ('server_points_exchange', True),
    'server_star_task': ('server_star_task', True),
    'active_consume': ('active_consume', True),
    'active_daily_consume': ('active_daily_consume', True),
    'active_recharge': ('active_recharge', True),
    'active_daily_recharge': ('active_daily_recharge', True),
    'normal_exchange': ('normal_exchange', True),
    'omni_exchange': ('omni_exchange', True),
    'sign_daily_charge': ('sign_daily_charge', True),
    'active_show': ('active_show', True),
    'gacha_reward_hero': ('gacha_reward_hero', True),
    'gacha_reward': ('gacha_reward', True),
    'month_card': ('month_card', True),
    'active_inreview': ('active_inreview', True),
    'limit_weapon': ('limit_weapon', True),
    'limit_box_reward': ('limit_box_reward', True),
    'limit_box_shop': ('limit_box_shop', True),
    'limit_hero_score': ('limit_hero_score', True),
    'limit_hero_rank': ('limit_hero_rank', True),
    'limit_card_chip': ('limit_card_chip', True),
    'limit_diamond_gacha': ('limit_diamond_gacha', True),
    'limit_gacha': ('limit_gacha', True),
    'extra_hero': ('extra_hero', True),
    'hero_description': ('hero_description', True),
    'server_limit_weapon': ('server_limit_weapon', True),
    'server_limit_box_reward': ('server_limit_box_reward', True),
    'server_limit_box_shop': ('server_limit_box_shop', True),
    'server_limit_hero_score': ('server_limit_hero_score', True),
    'server_limit_hero_rank': ('server_limit_hero_rank', True),
    'server_limit_card_chip': ('server_limit_card_chip', True),
    'server_limit_diamond_gacha': ('server_limit_diamond_gacha', True),
    'server_limit_gacha': ('server_limit_gacha', True),
    'server_extra_hero': ('server_extra_hero', True),
    'server_hero_description': ('server_hero_description', True),
    'honor_shop_new': ('honor_shop_new', True)
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


rally_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'rally_main': ('rally_main', True),
    'rally_event': ('rally_event', True),
    'rally_map': ('rally_map', True),
    'rally_buff': ('rally_buff', True),
    # 'rally_stage': ('rally_stage', True),
    # 'rally_stage_detail': ('rally_stage_detail', True),
    # 'rally_checkpoint': ('rally_checkpoint', True),
    # 'rally_checkpoint_detail': ('rally_checkpoint_detail', True),
    # 'rally_box': ('rally_box', True),
}


bounty_hunter_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'doomsday_hunt_main': ('doomsday_hunt_main', True),
    'doomsday_hunt': ('doomsday_hunt', True),
    # 'reward_set': ('reward_set', True),
    'clone': ('clone', True),
    'clone_bank': ('clone_bank', True),
    'hunt_map': ('hunt_map', True),
    # 'bufword': ('bufword', True),
    # 'bufwordmap': ('bufwordmap', True),
}


team_boss_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'team_boss': ('team_boss', True),
}


gift_center_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'welfare': ('welfare', True),
    # 'gift_center': ('gift_center', True),
    'welfare_sign': ('welfare_sign', True),
    # 'sign_daily_charge': ('sign_daily_charge', True),
    # 'first_charge_reward': ('first_charge_reward', True),
    # 'sign_first_week': ('sign_first_week', True),
    'welfare_energy': ('welfare_energy', True),
    'welfare_login': ('welfare_login', True),
    'welfare_card_login': ('welfare_card_login', True),
    'welfare_3days': ('welfare_3days', True),
    'welfare_online': ('welfare_online', True),
    'welfare_level': ('welfare_level', True),
    'welfare_notice': ('welfare_notice', True),
    'server_notice': ('server_notice', True),
}


commander_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    # 'commander_type': ('commander_type', True),
    # 'commander_recipe': ('commander_recipe', True),
    # 'commander_part': ('commander_part', True),
    # 'commander_reward': ('commander_reward', True),
    # 'commander': ('commander', True),
}

seven_scripture_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'sevenday': ('sevenday', True),
    'sevenday_info': ('sevenday_info', True),
    'sevenday_shop': ('sevenday_shop', True),
}

prison_config_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'prison_main': ('prison_main', True),
    'prison_artifact': ('prison_artifact', True),
    'prison_artifact_upgrade': ('prison_artifact_upgrade', True),
    'prison_treasure': ('prison_treasure', True),
    'prison_treasure_upgrade': ('prison_treasure_upgrade', True),
    'prison_break': ('prison_break', True),
    'prison_words': ('prison_words', True),
    'random_drop': ('random_drop', True),
    'prison_artifact_milestone': ('prison_artifact_milestone', True),
}

high_ladder_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'arena_award': ('arena_award', True),
    'arena_once_reward': ('arena_once_reward', True),
    'arena_daily_reward': ('arena_daily_reward', True),
    # 'arena_enemy': ('arena_enemy', True),
    # 'arena_robot': ('arena_robot', True),
}

code_mapping = {
    'code': ('code', True),
}


mercenary_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'awaken_material': ('awaken_material', True),
    'team_skill_fuben': ('team_skill_fuben', True),
    # 'team_skill_reward_set': ('team_skill_reward_set', True),
    'mercenary': ('mercenary', True),
    'mercenary_select': ('mercenary_select', True),
    'team_skill_cost': ('team_skill_cost', True),
    'awaken_chapter_cost': ('awaken_chapter_cost', True),
    'team_skill_milestone': ('team_skill_milestone', True),
    'awaken_chapter_milestone': ('awaken_chapter_milestone', True),
    'mercenary_value': ('mercenary_value', True),
    'awaken_history': ('awaken_history', True),
}


home_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'home_main': ('home_main', True),
    'home_dressup_sort': ('home_dressup_sort', True),
    'home_dressup_detail': ('home_dressup_detail', True),
    'home_flower_reward': ('home_flower_reward', True),
    'home_flsend_reward': ('home_flsend_reward', True),
}


biography_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'biography_detail': ('biography_detail', True),
    # 'biography_grade': ('biography_grade', True),
    # 'biography_skill': ('biography_skill', True),
    # 'biography_exp': ('biography_exp', True),
    'biography_chapter': ('biography_chapter', True),
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


decisive_battle_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'duel_rank_award': ('duel_rank_award', True),
    'duel_exchange': ('duel_exchange', True),
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


king_war_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'king_war': ('king_war', True),
    'king_war_rank_person': ('king_war_rank_person', True),
    'king_war_grade': ('king_war_grade', True),
    'king_war_active': ('king_war_active', True),
    'king_war_rank_guild': ('king_war_rank_guild', True),
    'king_war_shop': ('king_war_shop', True),
}


pve_raid_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'pve_enemy': ('pve_enemy', True),
    'pve_stagelist': ('pve_stagelist', True),
    'pve_teamskill': ('pve_teamskill', True),
    'pve_attribute': ('pve_attribute', True),
    'pve_hero': ('pve_hero', True),
    'pve_stagesort1': ('pve_stagesort1', True),
    'pve_stagesort2': ('pve_stagesort2', True),
    'pve_recommend': ('pve_recommend', True),
}

leading_role_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'main_hero': ('main_hero', True),
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

tech_tree_mapping = {
    'tech_tree': ('tech_tree', True),
    'tech_tree_pic': ('tech_tree_pic', True),
    'tech_display': ('tech_display', True),
}

wormhole_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'wormhole_detail': ('wormhole_detail', True),
    'wormhole_theme': ('wormhole_theme', True),
    'wormhole': ('wormhole', True),
    'wormhole_reward_break': ('wormhole_reward_break', True),
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


star_array_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'star_array': ('star_array', True),
    'star_array_reward': ('star_array_reward', True),
    'star_pic': ('star_pic', True),
}


ednless_march_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'endless_march_hero': ('endless_march_hero', True),
    'endless_march_hero_skill': ('endless_march_hero_skill', True),
    'endless_march_main': ('endless_march_main', True),
    'endless_march_main_skill': ('endless_march_main_skill', True),
    'endless_march_enemy': ('endless_march_enemy', True),
    'endlesscoin_exchange': ('endlesscoin_exchange', True),
    'endless_breakreward': ('endless_breakreward', True),
    'endless_lucky': ('endless_lucky', True),
    'endless_artifact': ('endless_artifact', True),
    'endless_bg': ('endless_bg', True),
}


roulette_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'roulette': ('roulette', True),
    'achieve_reward': ('achieve_reward', True),
    'server_roulette': ('server_roulette', True),
    'server_achieve_reward': ('server_achieve_reward', True),
    'charge_roulette': ('charge_roulette', True),
    'server_charge_roulette': ('server_charge_roulette', True),
}


limit_discount_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'limit_discount': ('limit_discount', True),
    'server_limit_discount': ('server_limit_discount', True),
    'red_bag': ('red_bag', True),
    'server_red_bag': ('server_red_bag', True),
}


slg_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'slg_block_reward': ('slg_block_reward', True),
}


world_boss_mapping = {
    # key 为 config_name, value: 表名, 前端是否能看的
    'worldboss_boss': ('worldboss_boss', True),
    'worldboss_streward': ('worldboss_streward', True),
    'worldboss_topreward': ('worldboss_topreward', True),
    'worldboss_pointreward': ('worldboss_pointreward', True),
    'worldboss_guild': ('worldboss_guild', True),
    'worldboss_heroact': ('worldboss_heroact', True),

}

# 注册需要写到最下面
register_handler()
