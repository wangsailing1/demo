#! --*-- coding: utf-8 --*--

__author__ = 'sm'

BACK_CONFIG_TEMPLATES_STATUS = False
FRONT_CONFIG_TEMPLATES_STATUS = False

import settings

from gconfig.model import GameConfig, FrontGameConfig
from lib.utils.debug import print_log
MUITL_LAN = {'0': 'TW', '1': 'CN', 0: 'TW', 1: 'CN'}

game_config = GameConfig()
game_config.refresh()
front_game_config = FrontGameConfig()
front_game_config.refresh()


def get_str_words(languages_sort, *args):
    """
        获取对应字段的提示
    Args:
        languages_sort: 语言种类
        *args:          获取字段对应的提示
    Returns:
    """
    if languages_sort in MUITL_LAN:
        lan = MUITL_LAN[languages_sort]
    else:
        lan = MUITL_LAN['0']

    str_words = game_config.get_language_config(lan)
    if str_words:
        if len(args) < 2:
            return str_words.get(str(args[0]), '')
        return_msg = []
        for str_name in args:
            return_msg.append(str_words.get(str(str_name), ''))
        return return_msg

    return ''


def charge_scheme_func():
    """充值定单配置，额外增加商品id到配置的映射配置 多语言 安卓
    """
    charge_config = game_config.charge
    charge_ios_config = game_config.charge_ios
    d = [charge_config, charge_ios_config]
    new_r = {}
    for i in d:
        for buy_id, obj in i.iteritems():
            cost = obj['cost']
            new_r[cost] = buy_id
    return new_r
