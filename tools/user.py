#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import pickle
import zlib
import datetime

from lib.db import ModelBase, ModelTools
from lib.core.environ import ModelManager
from gconfig import game_config
from models.server import ServerUid
from lib.utils import generate_rank_time
from models.server import get_server_config
from models.ranking_list import BlockRank


# 玩家信息


def user_info(mm):
    """
    用户基本信息
    :param mm:
    :return:
    """
    user_dict = {
        'uid': mm.uid,
        'vip': mm.user.vip,
        'name': mm.user.name,
        'level': mm.user.level,
        'role': mm.user.role,
        'tile_power': mm.user.tile_power,
        'combat': 0,  # mm.hero.get_max_combat(),
        'guild_id': mm.user.guild_id,
        'guild_name': mm.get_obj_by_id('guild', mm.user.guild_id).name if mm.user.guild_id else '',
        'server_name': get_server_config(mm.user._server_name).get('name', '')
    }

    return user_dict


def user_friend_info(mm, uid):
    """ 用户好友信息

    :param mm:
    :param uid:
    :return:
    """
    target_mm = mm.get_mm(uid)
    target_user = target_mm.user

    guild = mm.get_obj_by_id('guild', target_user.guild_id)
    friend = target_mm.friend

    if target_user.active_time and int(time.time()) - target_user.active_time <= 5 * 60:
        # 5分钟之内是在线
        user_status = 1
    else:
        user_status = 0
    block_rank_uid = mm.block.get_key_profix(mm.block.block_num, mm.block.block_group,
                                             'income')
    br = BlockRank(block_rank_uid, mm.block._server_name)

    user_dict = {
        'uid': target_user.uid,
        'name': target_user.name,
        'level': target_user.level,
        'vip': target_user.vip,
        # 'guild_name': guild.name,
        # 'guild_id': guild.guild_id,
        'user_status': user_status,  # 用户状态, 0: 离线, 1: 在线
        'active_time': target_user.active_time,  # 活跃时间戳
        'role': target_user.role,
        # 'parise_count': friend.parise_count,  # 点赞数
        # 'has_redpacket': friend.red_packet['has_reward'],   # 有没有红包
        # 'high_ladder_rank': target_mm.get_obj_tools('high_ladder_rank').get_rank(uid),  # 竞技场排名
        # 'dark_street': target_mm.dark_street.milestone_id,  # 黑街段位
        # 'combat': target_mm.hero.get_max_combat(),
        'nickname': mm.friend.nickname.get(uid, ''),
        'block': target_mm.block.block_num,
        'block_rank': br.get_rank(target_user.uid),
        'like': mm.friend.friends_info.get(uid, {}).get('like', 0)
    }
    result = {
        'user': user_dict
    }

    return result


def user_rank_info(mm, uid, rank, score):
    """ 用户排名信息

    :param mm:
    :param uid:
    :return:
    """
    target_mm = mm.get_mm(uid)

    result = {
        'user': user_info(target_mm),
        'rank': rank,
        'score': score,
    }

    return result


def rally_rank_info(mm, uid, rank, score):
    """ 血尘拉力赛用户排名信息

    :param mm:
    :param uid:
    :return:
    """
    target_mm = mm.get_mm(uid)

    result = {
        'user': user_info(target_mm),
        'rank': rank,
        'score': round(score),
        'rich_time': time.strftime('%H:%M:%S', time.localtime(generate_rank_time(score))),
    }

    return result


def user_battle_info(mm, uid, team):
    """ 用户战斗信息

    :param mm:
    :param uid:
    :return:
    """
    heros = {}
    for hero_oid in team:
        hero_dict = mm.hero.effect.get_hero(hero_oid)
        if not hero_dict:
            team.remove(hero_oid)
            continue
        heros[hero_oid] = hero_dict

    result = {
        'uid': mm.uid,
        'name': mm.user.name,
        'level': mm.user.level,
        'role': mm.user.role,
        'team': team,
        'heros': heros,
    }

    return result


def guild_info(mm, guild_id):
    guild = mm.get_obj_by_id('guild', guild_id)
    user_dict = {
        'uid': guild_id,
        'name': guild.name,
        'level': guild.get_guild_lv(),
        'icon': guild.icon,
        'server_name': get_server_config(guild._server_name).get('name', '')
    }

    return user_dict


def guild_rank_info(mm, guild_id, rank, score):
    result = {
        'user': guild_info(mm, guild_id),
        'rank': rank,
        'score': score,
    }
    return result


class VipInfo(ModelTools):
    """ VIP玩家及等级信息
    """
    GLOBAL_VIP_KEY = 'VIP'  # 记录报名信息

    def __init__(self, uid='', server='', *args, **kwargs):
        self.uid = uid
        self.server = server
        super(VipInfo, self).__init__()
        self.redis = self.get_redis_client(self.server)

    def get_uid(self, level_start=None, level_end=None):
        """
        获取记录, 不传入参数时取所有， 只传入level_start，取大于等于该vip等级的玩家,都传入的时候取区间内的
        """
        result = []
        log_key = self.generate_info_log_key(self.GLOBAL_VIP_KEY)
        vip_log = self.redis.get(log_key)
        if not vip_log:
            vip_log = self.calculate_default_data()
            self.add_log(vip_log, self.GLOBAL_VIP_KEY)
        else:
            vip_log = pickle.loads(zlib.decompress(vip_log))
        if not level_start and not level_start:
            return vip_log
        if level_start and not level_end:  # 取大于等于的vip_level的
            for i in vip_log.keys():
                if i >= level_start:
                    result += vip_log[i]
        if level_start and level_end:
            for i in xrange(level_start, level_end + 1):
                if i not in vip_log.keys():
                    continue
                result += vip_log[i]
        return result if result else []

    def exchange_vip_log(self, level, uid):
        """
        修改记录
        """
        if level == 0:
            return
        vip_info = self.get_uid()
        for k, v in vip_info.iteritems():
            if uid in v:
                vip_info[k].pop(v.index(uid))
        vip_config = game_config.vip.keys()
        if level not in vip_config:
            return
        if not vip_info.get(level, []):
            vip_info[level] = [uid]
        else:
            vip_info[level].append(uid)
        self.add_log(vip_info, self.GLOBAL_VIP_KEY)

    def generate_info_log_key(self, tp):
        """
        生成key
        :param tp:
        :return:
        """
        key = '%s_info_log' % tp
        return self.make_key_cls(key, self.server)

    def compress_log(self, battle):
        """
        压缩数据
        """
        return zlib.compress(pickle.dumps(battle, pickle.HIGHEST_PROTOCOL))

    def add_log(self, data, tp):
        """
        记录
        """
        info_log_key = self.generate_info_log_key(tp)
        compress_battle = self.compress_log(data)
        self.redis.set(info_log_key, compress_battle)

        return info_log_key

    def calculate_default_data(self):
        """
        找VIP玩家
        :return:
        """
        init_data = {}
        vip_config = game_config.vip.keys()
        for i in vip_config:
            init_data[i] = []
        server_uid = ServerUid(self.server)
        for i in server_uid.get_all_uid():
            mm = ModelManager(i)
            if mm.user.vip > 0 and mm.user.vip in game_config.vip.keys():
                init_data[mm.user.vip].append(i)

        return init_data
