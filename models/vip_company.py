# -*- coding: utf-8 –*-

"""
Created on 2019-01-29

@author: sm
"""

from gconfig import game_config


def init_vip_coin_gacha_count():
    return game_config.vip_company[0]['vip_coin_gacha_count']


def vip_coin_gacha_count(user, *args, **kwargs):
    """免费招募次数积累上限"""
    vip = user.company_vip
    return game_config.vip_company[vip]['vip_coin_gacha_count']


def more_license(user, *args, **kwargs):
    """秘书每天申请许可证数量+L"""
    vip = user.company_vip
    return game_config.vip_company[vip]['more_license']


def buy_pvp(user, *args, **kwargs):
    """谁是歌手每日购买次数上限"""
    vip = user.company_vip
    return game_config.vip_company[vip]['buy_pvp']
