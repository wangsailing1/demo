# -*- coding: utf-8 -*-
"""
Created on 2014-7-10

@author: Administrator
"""

'''
def module_funcname(env, args, result_data):
    """# module_funcname: module中的funcname接口的统计方法, 此函数命名规则：views中模块名_函数名
                            比如views.cards.open的统计方法命名为：cards_open
    args:
        env:
        args: 请求参数
        return_data: 比如views层函数处理后的result_data,
    returns:
        0    ---
        data:     需要记录的结果
    """
    data={}
    return data

'''


def gacha_get_gacha(hm, args, data):
    return {'reward': data.get('reward', {}), 'prize_id': data.get('prize_id', 0)}


def gacha_get_box(hm, args, data):
    return {'reward': data.get('reward', {}), 'gifts': data.get('gifts', [])}


def gacha_recieve_score(hm, args, data):
    return {'reward': data.get('reward', {}), 'group_done': data.get('group_done', [])}


def gacha_recieve_box_score(hm, args, data):
    return {'reward': data.get('reward', {}), 'box_group_done': data.get('box_group_done', [])}

# def dark_street_battle_end(hm, args, data):
#     return {'reward': data.get('reward', {})}
#
#
# def doomsday_hunt_battle_data(hm, args, data):
#     """末日狩猎组队战斗"""
#     return {'reward': data.get('reward', {}), 'is_playback': data.get('is_playback', False)}
#
#
# def doomsday_hunt_battle_end(hm, args, data):
#     """末日狩猎单人战斗"""
#     return {'reward': data.get('reward', {})}
#
#
# def rally_sweep(hm, args, data):
#     return {'reward': data.get('reward', {})}


def rally_shop_buy(hm, args, data):
    return {'reward': data.get('reward', {})}

def shop_buy(hm, args, data):
    return {'reward': data.get('reward', {})}


def shop_sell(hm, args, data):
    return {'reward': data.get('reward', {})}

# def rally_battle_end(hm, args, data):
#     return {'reward': data.get('reward', {})}
#
#
# def daily_boss_battle_end(hm, args, data):
#     return {'reward': data.get('reward', {})}
#
#
# def daily_advance_battle_end(hm, args, data):
#     return {'reward': data.get('reward', {})}
#
#
# def daily_nightmares_battle_round(hm, args, data):
#     return {'reward': data.get('reward', {})}


# def commander_rob(hm, args, data):
#     return {'win': data.get('win', False), 'parts': data.get('parts', {})}


def commander_compose(hm, args, data):
    return {'reward': data.get('reward', {})}


# def private_city_battle_end(hm, args, data):
#     return {'reward': data.get('reward', {}), 'first_pass': data.get('first_pass', False)}


# def private_city_battle_dungeon_end(hm, args, data):
#     return {'reward': data.get('reward', {})}


# def private_city_sweep(hm, args, data):
#     return {'reward': data.get('reward', {}), 'rewards': data.get('rewards', []), 'ext_reward': data.get('ext_reward', {})}


# def private_city_sweep_dungeon(hm, args, data):
#     return {'reward': data.get('reward', {}), 'rewards': data.get('rewards', []), 'ext_reward': data.get('ext_reward', {})}


def private_city_receive_exploration_reward(hm, args, data):
    return {'reward': data.get('reward', {})}


def private_city_receive_star_reward(hm, args, data):
    return {'reward': data.get('reward', {})}


# def manufacture_run_manu(hm, args, data):
#     return {'reward': data.get('reward', {})}
#
#
# def collection_run_coll(hm, args, data):
#     return {'reward': data.get('reward', {})}
#
#
# def collection_exchange(hm, args, data):
#     return {'reward': data.get('reward', {})}
#
#
# def collection_batch_exchange(hm, args, data):
#     return {'reward': data.get('reward', {})}


def equip_new_strengthen(hm, args, data):
    return {'reward': data.get('reward', {})}


def equip_equip_refine(hm, args, data):
    return {'equip_refine_temp': data.get('equip_refine_temp', {})}


# def equip_equip_refine_save(hm, args, data):
#     return {'reward': data.get('reward', {})}


def equip_st_levelup(hm, args, data):
    return {'reward': data.get('reward', {})}


# def hero_hero_lvlup(hm, args, data):
#     return {'reward': data.get('reward', {})}


# def hero_hero_lvlup_full(hm, args, data):
#     return {'reward': data.get('reward', {})}


def hero_update_star(hm, args, data):
    return {'reward': data.get('reward', {})}


def hero_summon_hero(hm, args, data):
    return {'reward': data.get('reward', {})}


def hero_lvlup_evolution(hm, args, data):
    return {'reward': data.get('reward', {})}


def hero_lvlup_skill(hm, args, data):
    return {'reward': data.get('reward', {})}


def hero_lvlup_extra_skill(hm, args, data):
    return {'reward': data.get('reward', {})}


def hero_awaken(hm, args, data):
    return {'new_hero_oid': data.get('new_hero_oid', {})}
