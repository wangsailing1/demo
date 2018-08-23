#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import itertools

from gconfig import game_config

# 英雄信息


def hero_info(hero_obj, hero_oids):
    """ 英雄icon基本信息

    :param hero_obj:
    :param hero_oids: []
    :return:
    """
    hero_data = []

    for hero_oid in hero_oids:
        hero_dict = hero_obj.heros.get(hero_oid, {})
        if not hero_dict:
            continue
        data = {
            'hero_id': hero_dict['id'],
            'oid': hero_dict['oid'],
            'lv': hero_dict['lv'],
            'star': hero_dict['star'],
            'evo': hero_dict['evo'],
            'combat': hero_dict['combat'],
        }
        hero_data.append(data)

    return hero_data


def format_hero_info(hero_dicts, show_attr=False):
    """
    格式化英雄数据
    :param hero_dicts: {id: {}}
    :return:
    """
    hero_data = []

    for hero_oid, hero_dict in hero_dicts.iteritems():
        data = {
            'hero_id': hero_dict['id'],
            'oid': hero_oid,
            'lv': hero_dict['lv'],
            'star': hero_dict['star'],
            'evo': hero_dict['evo'],
            'combat': hero_dict.get('combat', 0),
        }
        if show_attr:
            for attr_id in itertools.chain(game_config.base_attr, game_config.hero_basis_init_attr):
                attr_name = game_config.attr_mapping.get(attr_id)
                if not attr_name:
                    continue
                data[attr_name] = hero_dict.get(attr_name, 0)

        hero_data.append(data)

    return hero_data
