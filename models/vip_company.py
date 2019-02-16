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


def buy_point(user, *args, **kwargs):
    """购买体力次数上限"""
    vip = user.company_vip
    return game_config.vip_company[vip]['buy_point']


def if_catcher(user, *args, **kwargs):
    """是否解锁娃娃机"""
    vip = user.company_vip
    return game_config.vip_company[vip]['if_catcher']


def if_super_catcher(user, *args, **kwargs):
    """是否解锁超级娃娃机"""
    vip = user.company_vip
    return game_config.vip_company[vip]['if_super_catcher']


def bussiness_gold(user, *args, **kwargs):
    """明星活动金币收益+N%"""
    vip = user.company_vip
    return game_config.vip_company[vip]['bussiness_gold']


def bussiness_exp(user, *args, **kwargs):
    """明星活动公司经验收益+M%"""
    vip = user.company_vip
    return game_config.vip_company[vip]['bussiness_exp']


def shop_num(user, *args, **kwargs):
    """商店限购物品个数"""
    vip = user.company_vip
    return game_config.vip_company[vip]['shop_num']


def task_cd(user, *args, **kwargs):
    """随机任务刷新时间变快N分钟"""
    vip = user.company_vip
    return game_config.vip_company[vip]['task_cd']


def buy_gold(user, *args, **kwargs):
    """兑换金币次数+N"""
    vip = user.company_vip
    return game_config.vip_company[vip]['buy_gold']


def if_skip_story(user, *args, **kwargs):
    """可使用跳过剧情功能"""
    vip = user.company_vip
    return game_config.vip_company[vip]['if_skip_story']


def if_skip_battle(user, *args, **kwargs):
    """可使用跳过票房功能"""
    vip = user.company_vip
    return game_config.vip_company[vip]['if_skip_battle']


def card_max(user, *args, **kwargs):
    """可拥有艺人上限数量+N"""
    vip = user.company_vip
    return game_config.vip_company[vip]['card_max']


def extra_script(user, *args, **kwargs):
    """续作拍摄上限+N档"""
    vip = user.company_vip
    return game_config.vip_company[vip]['extra_script']


def scriptgacha_maxnum(user, *args, **kwargs):
    """抽剧本可积攒的次数上限"""
    vip = user.company_vip
    return game_config.vip_company[vip]['scriptgacha_maxnum']


def chapterstage_fastten(user, *args, **kwargs):
    """快速工作10场"""
    vip = user.company_vip
    return game_config.vip_company[vip]['chapterstage_fastten']


def script_reselectiontimes(user, *args, **kwargs):
    """重新选择自制拍摄剧本次数"""
    vip = user.company_vip
    return game_config.vip_company[vip]['script_reselectiontimes']


def avgdatetimes(user, *args, **kwargs):
    """约会次数"""
    vip = user.company_vip
    return game_config.vip_company[vip]['avgdatetimes']


def phonecalltimes(user, *args, **kwargs):
    """手机聊天次数"""
    vip = user.company_vip
    return game_config.vip_company[vip]['phonecalltimes']
