# -*- coding: utf-8 –*-

"""
Created on 2017-12-27

@author: sm
"""
import json

from gconfig import game_config, get_str_words
from admin import render
from admin.decorators import require_permission
from chat.to_server import get_content_msg, delete_content_msg
from lib.core.environ import ModelManager

#
# @require_permission
# def king_war_hero_use_info(req, *args, **kwargs):
#     """
#
#     :param req:
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     client = KingWar.get_global_cache()
#     use_key = KingWar.generate_hero_use_log_key()
#     win_key = KingWar.generate_hero_win_log_key()
#     battle_times_key = KingWar.generate_battle_times_log_key()
#
#     use_info = client.hgetall(use_key)
#     win_info = client.hgetall(win_key)
#     battle_times_info = client.hgetall(battle_times_key)
#     battle_times_info = {k: int(v) for k, v in battle_times_info.iteritems()}
#
#     hero_log = []
#     for hero_id, use_times in use_info.items():
#         config = game_config.hero_basis[int(hero_id)]
#         name = get_str_words('1', config['name'])
#         win_times = win_info.get(hero_id, 0)
#         use_times, win_times = int(use_times), int(win_times)
#         hero_log.append({
#             'hero_id': hero_id,
#             'name': name,
#             'use_times': use_times,
#             'win_times': win_times,
#             'win_rate': round(win_times * 100.0 / use_times, 2)
#         })
#
#     data = {'battle_times_info': battle_times_info, 'hero_log': hero_log}
#     return render(req, 'admin/other/king_war_hero_use_info.html', **data)


@require_permission
def select_chat_data(req, *args, **kwargs):
    """

    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    server = req.get_argument('server', '')
    flag = req.get_argument('flag', '')

    result = {'server': server, 'flag': flag, 'msg': '', 'data': []}

    if not server or flag not in ['all_world', 'world']:
        result['msg'] = u'参数错误'
        return render(req, 'admin/other/chat_data.html', **result)

    command = 'get_content_msg@%s@%s' % (flag, server)
    chat_data = get_content_msg(command, server)
    data = []
    for i in chat_data:
        index1 = i.find('{')
        index2 = i.rfind('}')
        if -1 in [index1, index2]:
            continue
        j = i[index1:index2+1]
        data.append(json.loads(j))
    result['data'] = data

    return render(req, 'admin/other/chat_data.html', **result)


@require_permission
def delete_chat_data(req, *args, **kwargs):
    """

    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    server = req.get_argument('server', '')
    flag = req.get_argument('flag', '')
    sign_ids = req.get_arguments('sign_id')

    result = {'server': server, 'flag': flag, 'msg': '', 'data': []}

    if not server or flag not in ['all_world', 'world', 'guild'] or not sign_ids:
        result['msg'] = u'参数错误'
        return render(req, 'admin/other/chat_data.html', **result)

    command = 'delete_content_msg@%s@%s@%s' % (flag, server, json.dumps(sign_ids))
    delete_content_msg(command, server)

    return select_chat_data(req, *args, **kwargs)


@require_permission
def select_danmu_data(req, *args, **kwargs):
    """
    查询弹幕数据
    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    server = req.get_argument('server', '')
    stage_id = int(req.get_argument('stage_id', 0))

    result = {'server': server, 'stage_id': stage_id, 'msg': '', 'data': []}

    if not server or not stage_id:
        result['msg'] = u'参数错误'
        return render(req, 'admin/other/danmu_data.html', **result)

    data = []
    mm = ModelManager('%s1234567' % server)
    danmu_obj = mm.get_obj_tools('danmu')
    danmu_list = danmu_obj.get_danmu(t='private_city', arg1=stage_id)
    for i in danmu_list:
        j = eval(i)
        data.append(j)

    result['data'] = data
    print 'x'*20, result

    return render(req, 'admin/other/danmu_data.html', **result)


@require_permission
def delete_danmu_data(req, *args, **kwargs):
    """
    删除弹幕数据
    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    server = req.get_argument('server', '')
    stage_id = int(req.get_argument('stage_id', 0))
    sign_ids = req.get_arguments('sign_id')

    result = {'server': server, 'stage_id': stage_id, 'msg': '', 'data': []}

    if not server or not stage_id or not sign_ids:
        result['msg'] = u'参数错误'
        return render(req, 'admin/other/danmu_data.html', **result)

    mm = ModelManager('%s1234567' % server)
    danmu_obj = mm.get_obj_tools('danmu')
    for i in sign_ids:
        print '99' * 10, i
        danmu_obj.del_danmu(i, arg1=stage_id)

    return select_danmu_data(req, *args, **kwargs)
