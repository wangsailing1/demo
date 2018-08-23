#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

'''
这里提供python向c++服务器发送数据的接口
'''


from client import get_rpc_client

client = None


def check_connect(func):
    def wrapper(*args, **kwargs):
        _client = get_rpc_client()
        if not _client:
            return 'error_socket', {}
        global client
        client = _client
        return func(*args, **kwargs)

    return wrapper


@check_connect
def lua_battle(data, battle_name='high_ladder', _client=None):
    """
    从c++服务器获取后端战斗数据
    :param data: {
        att_team:
        att_heros:
        def_team:
        def_heros:
    }
    :param battle_name: 'high_ladder' or 'guild_boss',
    :return: {
        battle_result: {    # 其他数据
            'is_win': 1 or 0    # 输赢
            'hp_status': {      # 双方伤害值
                'att': 0,       # 攻击方
                'def': 0,       # 防守方
            }
        },
        'battle_data': {}   # 战报
    }
    """
    client1 = _client or client
    data['battle_name'] = battle_name
    status, battle_data = client1.send(100, "lua_battle", data)
    if status is None:
        print 'error not cmd'
        return 'error_socket', {}

    return 0, battle_data


def test_battle():
    """测试战斗"""
    from views.battle import test_battle_data

    rc, result = test_battle_data()
    rc, data = lua_battle(result)

    return rc, data



@check_connect
def guild_change(mm, guild_id):
    """
    公会变化后，通知c++
    :param mm:
    :param guild_id: 公会id
    :return:
    """
    data = {
        'uid': mm.uid,
        'guild_id': guild_id,
    }
    status, battle_data = client.send(101, data)
    if not status:
        return 'error_socket', {}

    return 0, {}


@check_connect
def point_change(mm, team_id, add_point):
    """
    行动力变化后，通知c++
    :param mm:
    :param team_id: 队伍id
    :param add_point: 增加行动力
    :return:
    """
    data = {
        'uid': mm.uid,
        'team_id': team_id,
        'add_point': add_point,
    }
    status, battle_data = client.send(3, data)
    if not status:
        return 'error_socket', {}

    return 0, {}


@check_connect
def hp_change(mm, hero_fid, add_hp):
    """
    增加血量后，通知c++
    :param mm:
    :param hero_fid: 卡牌fid
    :param add_hp: 增加血量百分比
    :return:
    """
    data = {
        'uid': mm.uid,
        'hero_fid': hero_fid,
        'add_point': add_hp,
    }
    status, battle_data = client.send(4, data)
    if not status:
        return 'error_socket', {}

    return 0, {}
