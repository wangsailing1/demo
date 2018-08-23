#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import json

from lib.utils.debug import print_log
import settings

from models.config import ConfigRefresh

def to_json(obj):
    """# to_json: 将一些特殊类型转换为json
    args:
        obj:    ---    arg
    returns:
        0    ---    
    """
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(repr(obj) + ' is not json seralizable')


def user_status(mm):
    """ 用户状态

    :param mm:
    :return:
    """
    if mm is None:
        return {}

    user = mm.user

    guild_name = user.guild_name

    data = {
        'uid': user.uid,
        # 'title': mm.lead_title.cur, # 当前使用的称号
        'reg_time': user.reg_time,  # 注册时间
        'reg_name': user.reg_name,  # 是否注册过名字
        'change_name': user.change_name,
        'role': user.role,
        'name': user.name,
        'level': user.level,
        'exp': user.exp,
        'exp_pot': user.exp_pot,
        'diamond': user.diamond,
        'coin': user.coin,
        'like': user.like,
        'silver': user.silver,
        'vip': user.vip,
        'vip_exp': user.vip_exp,
        'guild_id': user.guild_id,
        'guild_name': guild_name,
        'unlock_build': user.unlock_build,
        'guide': user.guide,
        'action_point': user.action_point,
        'action_point_updatetime': user.action_point_updatetime,

        # 'battle_times': mm.private_city.battle_times,  # 副本挑战次数
        # 'max_battle_times': mm.private_city.MAX_BATTLE_TIMES,  # 简单以上挑战次数
        # 'max_reset_dungeon_times': mm.private_city.get_max_reset_dungeon_times(),
        # 'hard_reset_times': mm.private_city.hard_reset_times,
        # 'reset_hard_cost': mm.private_city.get_reset_hard_cost(),
        # 'avg_done': mm.private_city.get_avg_done(),  # 记录播放过的avg id

        'next_point_time': user.next_point_time(),
        'max_point_time': user.max_point_time(),
        'buy_point_times': user.buy_point_times,
        # 'max_combat': mm.hero.get_max_combat(),
        'hunt_coin': user.get_hunt_coin(),    # 末日狩猎挑战券
        'guild_coin': mm.user.guild_coin,       # 公会币
        'config_type': mm.user.config_type,
        'chat_times': mm.user.chat_times,       # 聊天次数
    }
    return data


def result_generator(rc, data, msg, mm):
    """ 统一生成返回格式

    :param rc: 接口状态
    :param data: 接口数据
    :param msg: 接口报错后的提示信息
    :param mm: ModelManager 对象管理类
    :return:
    """
    r = {
        'data': data,
        'status': rc,
        'msg': msg,
        'server_time': int(time.time()),
        'user_status': user_status(mm),
    }
    _, all_config_version, _ = ConfigRefresh.check()
    r['all_config_version'] = all_config_version
    if 'client_upgrade' in data:
        r['client_upgrade'] = data['client_upgrade']
    indent = 1 if settings.DEBUG else None
    r = json.dumps(r, ensure_ascii=False, separators=(',', ':'), encoding="utf-8", indent=indent, default=to_json)
    return r
