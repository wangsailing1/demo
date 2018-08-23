#!/usr/bin/env python
# coding: utf-8

"""
刷新玩家数据
"""

import sys
import itertools
import os.path

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings

env = sys.argv[1]
filename = sys.argv[2]
func_name = sys.argv[3]

settings.set_env(env)

from lib.core.environ import ModelManager
from gconfig import game_config


def refresh_favor(uid):
    """
    刷新好感度数据
    :param uid:
    :return:
    """
    mm = ModelManager(uid)
    for h_oid, h_dict in mm.hero.heros.iteritems():
        h_id = h_dict['id']
        favor_dict = h_dict.get('favor')
        if not favor_dict:
            continue
        favor_lv = favor_dict['lv']
        hero_favor_config = game_config.hero_favor.get(h_id)
        if not hero_favor_config:
            continue
        hero_favor_grade_config = game_config.hero_favor_grade.get(favor_lv)
        if not hero_favor_grade_config:
            continue

        try:
            # 主要成长
            main_attr = hero_favor_config['main_attr']
            main_rate = hero_favor_grade_config['main_rate']
            favor_dict['main_attr'][0][1] = main_attr[0][1] * main_rate
            if len(main_attr) == 2:
                favor_dict['main_attr'][1][1] = main_attr[1][1]

            # 阵营成长
            for i, j in itertools.izip(favor_dict['sec_attr'], hero_favor_config['sec_attr']):
                i[-1] = j[-1] * hero_favor_grade_config['sec_rate']
        except:
            continue

        mm.hero.calc_favor_effect(h_dict, favor_dict)
        mm.hero.update_base_attr(h_oid, h_dict)

    mm.hero.save()
    return uid


def refresh_guide(uid):
    """
    刷新新手引导数据
    :param uid:
    :return:
    """
    mm = ModelManager(uid)

    sort_list = []
    value = {}
    for i in sorted(game_config.guide_team):
        j = game_config.guide_team[i]
        if mm.user.level < j['open_level']:
            break
        sort_list.append(j['sort'])

    if not sort_list:
        return

    for sort in sort_list:
        guide_ids = game_config.get_guide_mapping(sort)
        if not guide_ids:
            continue

        key = guide_ids[-1]
        value[sort] = key

    mm.user.guide = value
    mm.user.save()
    return uid


success = []

# 获取区服列表
if not os.path.exists(filename):
    exit(1)
f = open(filename)

for l in f:
    user_id = l.strip()
    func = globals().get(func_name)
    if func:
        print func(user_id)
    else:
        print 'error func name'
