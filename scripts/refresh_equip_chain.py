#!/usr/bin/env python
# coding: utf-8

"""
批量向指定 ID 的玩家發送系統郵件 - 可以帶獎勵
"""

import sys
import os.path

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings

env = sys.argv[1]
filename = sys.argv[2]
if len(sys.argv) >= 4:
    check = 0
else:
    check = 1

settings.set_env(env)

from lib.core.environ import ModelManager
from gconfig import game_config


def check_equip_chain(user_id, check=1):
    mm = ModelManager(user_id)
    is_save = False
    for hero_oid, hero_dict in mm.hero.heros.iteritems():
        new_equip = hero_dict.get('new_equip')
        if not new_equip:
            continue
        is_update = False
        for equip_id, equip_dict in new_equip.iteritems():
            awake_lv = equip_dict['awake_lv']
            equip_config = game_config.new_equip_detail.get(equip_id)
            if not equip_config:
                continue
            chain_id = equip_config['awake'].get(1)
            if awake_lv >= 1 and chain_id and chain_id not in hero_dict['chain']:
                check_user.add(user_id)
                print user_id, hero_oid
                if not check:
                    mm.hero.update_equip_chain(equip_config, hero_dict)
                    is_update = True
        if is_update and not check:
            mm.hero.update_chain_effect(hero_dict)
            mm.hero.update_base_attr(hero_oid, hero_dict)
            is_save = True

    if is_save:
        mm.hero.save()

success = []

# 获取区服列表
if not os.path.exists(filename):
    exit(1)
f = open(filename)
check_user = set()


for l in f:
    user_id = l.strip()
    check_equip_chain(user_id, check)

print check_user
