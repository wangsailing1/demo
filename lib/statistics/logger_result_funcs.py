# -*- coding: utf-8 -*-


def gacha_get_gacha(data):
    return {'reward': data.get('reward', {}), 'prize_id': data.get('prize_id', 0)}


def dark_street_battle_end(data):
    return {'reward': data.get('reward', {})}


def doomsday_hunt_battle_data(data):
    """末日狩猎组队战斗"""
    return {'reward': data.get('reward', {}), 'is_playback': data.get('is_playback', False)}


def doomsday_hunt_battle_end(data):
    """末日狩猎单人战斗"""
    return {'reward': data.get('reward', {})}


def rally_sweep(data):
    return {'reward': data.get('reward', {})}


def rally_shop_buy(data):
    return {'reward': data.get('reward', {})}


def rally_battle_end(data):
    return {'reward': data.get('reward', {})}


def daily_boss_battle_end(data):
    return {'reward': data.get('reward', {})}


def daily_advance_battle_end(data):
    return {'reward': data.get('reward', {})}


def daily_nightmares_battle_round(data):
    return {'reward': data.get('reward', {})}


def commander_rob(data):
    return {'win': data.get('win', False), 'parts': data.get('parts', {})}


def commander_compose(data):
    return {'reward': data.get('reward', {})}


def private_city_battle_end(data):
    return {'reward': data.get('reward', {}), 'first_pass': data.get('first_pass', False)}


def private_city_battle_dungeon_end(data):
    return {'reward': data.get('reward', {})}


def private_city_sweep(data):
    return {'reward': data.get('reward', {}), 'rewards': data.get('rewards', []), 'ext_reward': data.get('ext_reward', {})}


def private_city_sweep_dungeon(data):
    return {'reward': data.get('reward', {}), 'rewards': data.get('rewards', []), 'ext_reward': data.get('ext_reward', {})}


def private_city_receive_exploration_reward(data):
    return {'reward': data.get('reward', {})}


def private_city_receive_star_reward(data):
    return {'reward': data.get('reward', {})}


def manufacture_run_manu(data):
    return {'reward': data.get('reward', {})}


def collection_run_coll(data):
    return {'reward': data.get('reward', {})}


def collection_exchange(data):
    return {'reward': data.get('reward', {})}


def collection_batch_exchange(data):
    return {'reward': data.get('reward', {})}


def equip_new_strengthen(data):
    return {'reward': data.get('reward', {})}


def equip_equip_refine(data):
    return {'equip_refine_temp': data.get('equip_refine_temp', {})}


def equip_equip_refine_save(data):
    return {'reward': data.get('reward', {})}


def equip_st_levelup(data):
    return {'reward': data.get('reward', {})}


def hero_hero_lvlup(data):
    return {'reward': data.get('reward', {})}


def hero_hero_lvlup_full(data):
    return {'reward': data.get('reward', {})}


def hero_update_star(data):
    return {'reward': data.get('reward', {})}


def hero_summon_hero(data):
    return {'reward': data.get('reward', {})}


def hero_lvlup_evolution(data):
    return {'reward': data.get('reward', {})}


def hero_lvlup_skill(data):
    return {'reward': data.get('reward', {})}


def hero_lvlup_extra_skill(data):
    return {'reward': data.get('reward', {})}


def hero_lvlup_awaken(data):
    return {'new_hero_oid': data.get('new_hero_oid', {})}
