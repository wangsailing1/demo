#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from celery_app import app
import os
import sys


@app.task
def battle(x, y):
    from lib.core.environ import ModelManager
    from battle_test.control import Control
    att_mm = ModelManager('tw1123456a')
    att_team = att_mm.hero.heros.keys()[:1]
    att_heros = {hoid: att_mm.hero.heros[hoid] for hoid in att_team}

    dfd_mm = ModelManager('tw1123456b')
    dfd_team = dfd_mm.hero.heros.keys()[:1]
    dfd_heros = {hoid: dfd_mm.hero.heros[hoid] for hoid in dfd_team}

    control = Control(att_team, att_heros, dfd_team, 1, enemy_heros=dfd_heros, is_pvp=True)
    control.onEnter()
    return control.win
    # import models
    # from models.hero import Hero
    # hero = Hero.get('tw1123456a', 'tw1')
    # print hero.heros
