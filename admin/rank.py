#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import datetime

from models.server import ServerConfig
from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from lib.statistics.data_analysis import get_one_day_rank_data

limit_days = 40
all_rank = [('level_rank', u'等级排行榜')]


# @require_permission
def select(req, channel_data=None, select_server=None, select_day=None, select_rank=None, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    rank_num = int(req.get_argument('rank_num', 20))

    sc = ServerConfig.get()
    today = datetime.datetime.today()
    day_interval = ((today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                    for i in xrange(0, limit_days + 1))
    day_data = []
    server_data = []
    rank_data = []
    for i in day_interval:
        for server_id, _ in sc.yield_open_servers():
            for rank in all_rank:
                data = get_one_day_rank_data(i, server_id, rank[0])
                if data:
                    if i not in day_data:
                        day_data.append(i)
                    if server_id not in server_data:
                        server_data.append(server_id)
                    if rank not in rank_data:
                        rank_data.append(rank)
    result = {
        'day_data': day_data,
        'server_data': server_data,
        'rank_data': rank_data,
        'select_server': select_server,
        'select_day': select_day,
        'select_rank': select_rank,
        'channel_data': channel_data,
        'level_rank': [],
        'top_hero_rank': [],
        'top_hero': {},
        'combat_rank': [],
        'private_city_rank': [],
        'msg': '',
        'uid': uid,
        'rank_num': rank_num,
    }
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        level_rank = mm.get_obj_tools('level_rank')
        top_hero_rank = mm.get_obj_tools('top_hero_rank')
        combat_rank = mm.get_obj_tools('combat_rank')
        private_city_rank = mm.get_obj_tools('private_city_rank')

        result['level_rank'] = level_rank.get_all_user(0, rank_num-1, withscores=True)
        result['top_hero_rank'] = top_hero_rank.get_all_user(0, rank_num-1, withscores=True)
        result['combat_rank'] = combat_rank.get_all_user(0, rank_num-1, withscores=True)
        result['private_city_rank'] = private_city_rank.get_all_user(0, rank_num-1, withscores=True)

        for user_id, hero_combat in result['top_hero_rank']:
            _mm = ModelManager(user_id)
            hero_rank = _mm.hero.hero_rank
            result['top_hero'][user_id] = hero_rank

    return render(req, 'admin/rank/index.html', **result)


def select_rank(req):
    """

    :param req:
    :return:
    """
    day = req.get_argument('day', '')
    rank_num = int(req.get_argument('', 20))
    server = req.get_argument('server_name', '')
    which_rank = req.get_argument('which_rank', '')
    obj = get_one_day_rank_data(day, server, which_rank)

    if rank_num > 100:
        rank_num = 100
    if not rank_num:
        rank_num = 20
    rank_data = []
    if obj:
        for i, j in enumerate(obj):
            if i + 1 > rank_num:
                break
            mm1 = ModelManager(j[0])
            rank_data.append([i+1, mm1.user.name, j[0], j[1]])
    return select(req, channel_data=rank_data,
                  select_server=server, select_day=day, select_rank=which_rank)
