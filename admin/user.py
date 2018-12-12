#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import datetime

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config
from models.logging import Logging
from logics.user import UserLogic
from models.spend import Spend
import settings
from admin import auth
from models.user import OnlineUsers
from models.server import ServerUidList


ALL_BAN_UIDS_KEY = 'all_ban_uids'
ALL_BAN_IPS_KEY = 'all_ban_ips'


@require_permission
def select(req, **kwargs):
    """

    :param req:
    :return:
    """
    ignore_reset_module = ['server_config']

    uid = req.get_argument('uid', '')
    result = {'mm': None, 'user': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['user'] = mm.user
        result['mm'] = mm
        result['ignore_reset_module'] = ignore_reset_module

    return render(req, 'admin/user/index.html', **result)


@require_permission
def update(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail1'})

    level = int(req.get_argument('level'))
    exp = int(req.get_argument('exp'))
    name = req.get_argument('name')
    diamond = int(req.get_argument('diamond'))
    coin = int(req.get_argument('coin', 0))
    like = int(req.get_argument('like', 0))
    # silver = int(req.get_argument('silver'))
    dollar = int(req.get_argument('dollar'))
    vip = int(req.get_argument('vip'))
    guild_coin = int(req.get_argument('guild_coin'))
    action_point = int(req.get_argument('action_point'))
    script_license = int(req.get_argument('script_license'))
    server_dice_num = int(req.get_argument('server_dice_num'))

    cur_level = mm.user.level
    level = min(level, max(game_config.player_level))
    add_exp = 0
    if cur_level != level:
        if level < cur_level:
            cur_level = mm.user.level = 1
        for lv in xrange(cur_level, level):
            add_exp += game_config.hero_exp.get(lv, {}).get('player_exp', 0)
        if add_exp > 0:
            mm.user.add_player_exp(add_exp)
    else:
        mm.user.exp = exp
    mm.user.name = name

    # 钻石
    admin = auth.get_admin_by_request(req)
    if admin:
        mm.action = 'admin.%s' % admin.username
    diff_diamond = mm.user.diamond - diamond
    if diff_diamond > 0:
        mm.user.deduct_diamond(diff_diamond)
    elif diff_diamond < 0:
        mm.user.add_diamond(-diff_diamond)

    # 金币
    diff_coin = mm.user.coin - coin
    if diff_coin > 0:
        mm.user.deduct_coin(diff_coin)
    elif diff_coin < 0:
        mm.user.add_coin(-diff_coin)

    # 点赞
    diff_like = mm.user.like - like
    if diff_like > 0:
        mm.user.deduct_like(diff_like)
    elif diff_like < 0:
        mm.user.add_like(-diff_like)

    # 美元
    diff_dollar = mm.user.dollar - dollar
    if diff_dollar > 0:
        mm.user.deduct_dollar(diff_dollar)
    elif diff_dollar < 0:
        mm.user.add_dollar(-diff_dollar)

    # # 银币
    # diff_silver = mm.user.silver - silver
    # if diff_silver > 0:
    #     mm.user.deduct_silver(diff_silver)
    # elif diff_silver < 0:
    #     mm.user.add_silver(-diff_silver)

    # 公会币
    diff_guild_coin = mm.user.guild_coin - guild_coin
    if diff_guild_coin > 0:
        mm.user.deduct_guild_coin(diff_guild_coin)
    elif diff_guild_coin < 0:
        mm.user.add_guild_coin(-diff_guild_coin)

    # # 战斗道具积分
    # mm.battle_item.energy = energy
    # diff_energy = mm.battle_item.energy - energy
    # if diff_energy > 0:
    #     mm.battle_item.deduct_energy(diff_energy)
    # elif diff_energy < 0:
    #     mm.battle_item.add_energy(-diff_energy)

    # 体力
    diff_action_point = mm.user.action_point - action_point
    if diff_action_point > 0:
        mm.user.decr_action_point(diff_action_point)
    elif diff_action_point < 0:
        mm.user.add_action_point(-diff_action_point)

    # # 统帅精力
    # diff_energy = mm.commander.energy - energy
    # if diff_energy > 0:
    #     mm.commander.decr_energy(diff_energy)
    # elif diff_energy < 0:
    #     mm.commander.add_energy(-diff_energy)

    # # 觉醒宝箱钥匙
    # diff_box_key = mm.user.box_key - box_key
    # if diff_box_key > 0:
    #     mm.user.deduct_box_key(diff_box_key)
    # elif diff_box_key < 0:
    #     mm.user.add_box_key(-diff_box_key)
    mm.user.script_license = script_license
    mm.carnival.server_dice_num = server_dice_num
    vip = min(max(game_config.vip), vip)
    if mm.user.vip != vip:
        mm.user.vip = vip
        mm.user.vip_exp = 0

    mm.user.save()
    mm.carnival.save()

    msg = 'success'

    return select(req, **{'msg': msg})


@require_permission
def reset_guide(req, **kwargs):
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail1'})

    sort = int(req.get_argument('sort', '1'))
    key = int(req.get_argument('key', '1'))

    if not sort or not key:
        return select(req, **{'msg': 'sort or key not empty'})

    value = {}

    for k, v in game_config.guide.iteritems():
        if v['sort'] > sort:
            continue
        if k > key:
            continue
        if v['sort'] not in value:
            value[v['sort']] = k
        else:
            value[v['sort']] = k

    mm.user.guide = value
    mm.user.save()

    msg = 'success'

    return select(req, **{'msg': msg})


@require_permission
def reset_module(req, **kwargs):
    """
    重置模块
    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    module_name = req.get_argument('reset_module', '')
    mm = ModelManager(uid)
    module = getattr(mm, module_name, None)
    if module:
        module.reset()
        msg = 'success'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


@require_permission
def user_logging(req):
    """
    玩家动作记录
    :param req:
    :return:
    """
    uid = req.get_argument('user_id')
    l = Logging(uid)
    st_list_0 = l.get_all_logging()
    return render(req, 'admin/user/user_logging.html', **{
        'st_list_0': st_list_0,
        'environment': settings.ENV_NAME,
        'user_id': uid,
        })


@require_permission
def earn_log(req):
    """
    钻石获取记录
    :param req:
    :return:
    """
    data = {'msg': '', 'mm': None, 'environment': settings.ENV_NAME, 'total': 0, 'user_id': '', 'st_list_0': []}
    if req.request.method == 'POST':
        uid = req.get_argument('user_id', '')
        mm = ModelManager(uid)
        if mm.user.inited:
            data['msg'] = u'not user'
            return render(req, 'admin/user/earn_log.html', **data)
        else:
            # earn = Earn()
            # st_list_0 = sorted(earn.find_by_uid(mm.user.uid), key=lambda x: x['subtime'], reverse=True)
            st_list_0 = sorted(mm.user.coin_log, key=lambda x: x['subtime'], reverse=True)

            total = sum([st['diamond_num'] for st in st_list_0 if st['diamond_num']])

            data['mm'] = mm
            data['st_list_0'] = st_list_0
            data['user_id'] = uid
            data['total'] = total
            return render(req, 'admin/user/earn_log.html', **data)

    return render(req, 'admin/user/earn_log.html', **data)


@require_permission
def diamond_log(req):
    """
    钻石总记录
    :param req:
    :return:
    """
    data = {'msg': '', 'mm': None, 'environment': settings.ENV_NAME, 'total': 0, 'user_id': '', 'st_list_0': []}
    if req.request.method == 'POST':
        uid = req.get_argument('user_id', '')
        mm = ModelManager(uid)
        if mm.user.inited:
            data['msg'] = u'not user'
            return render(req, 'admin/user/diamond_log.html', **data)
        else:
            # earn = Earn()
            spend = Spend()
            st_list_0 = []
            total1 = 0
            total2 = 0

            # st_list1 = earn.find_by_uid(mm.user.uid)
            st_list1 = mm.user.coin_log
            for i in st_list1:
                i['flag'] = 1
                total1 += i['diamond_num']
                st_list_0.append(i)
            st_list2 = spend.find_by_uid(mm.user.uid)
            for i in st_list2:
                i['flag'] = -1
                total2 += i['diamond_num']
                st_list_0.append(i)
            st_list_0 = sorted(st_list_0, key=lambda x: x['subtime'], reverse=True)

            for x in st_list_0:
                x['name'] = mm.user.name

            data['mm'] = mm
            data['st_list_0'] = st_list_0
            data['user_id'] = uid
            data['total1'] = total1
            data['total2'] = total2
            return render(req, 'admin/user/diamond_log.html', **data)

    return render(req, 'admin/user/diamond_log.html', **data)


@require_permission
def spend_person(req):
    data = {'msg': '', 'mm': None, 'environment': settings.ENV_NAME, 'total': 0, 'user_id': '', 'st_list_0': []}
    if req.request.method == 'POST':
        uid = req.get_argument('user_id', '')
        mm = ModelManager(uid)
        if mm.user.inited:
            data['msg'] = u'not user'
            return render(req, 'admin/user/spend_person.html', **data)
        else:
            spend = Spend()
            st_list_0 = sorted(spend.find_by_uid(mm.user.uid), key=lambda x: x['subtime'], reverse=True)

            for x in st_list_0:
                x['name'] = mm.get_mm(x['user_id']).user.name

            total = sum([st['diamond_num'] for st in st_list_0 if st['diamond_num']])

            data['mm'] = mm
            data['st_list_0'] = st_list_0
            data['user_id'] = uid
            data['total'] = total
            return render(req, 'admin/user/spend_person.html', **data)

    return render(req, 'admin/user/spend_person.html', **data)


@require_permission
def export(req, reset_msg=None, msgs=None):
    """
     导出玩家数据
    """
    uid1 = req.get_argument('export_uid', 'test')

    mm = ModelManager(uid1)
    r = mm.user.redis

    key_list = []
    for model_name in mm._register_base:
        if model_name in ['friend', 'guild']:
            continue
        print model_name
        cls_instance = getattr(mm, model_name)
        cls_key = cls_instance.make_key_cls(uid1, uid1[:-7])
        key_list.append(cls_key)

    l = ["""uid1 = '%s'\ndata=[""" % uid1, ]

    for key in key_list:
        if not 'BattleLog' in key:
            if r.type(key) == 'string':
                raw = r.get(key)
                l.append("(%r, %r)," % (key, raw))

    l.append(']')
    s = ''.join(l)
    req.set_header('Content-Type', 'application/txt')
    req.set_header('Content-Disposition', 'attachment;filename=%s.txt' % uid1)
    req.write(s)


@require_permission
def inject(req, reset_msg=None, msgs=None):
    """
    导入玩家数据
    :param req:
    :param reset_msg:
    :param msgs:
    :return:
    """
    uid2 = req.get_argument('inject_uid', 'test')

    mm = ModelManager(uid2)
    r = mm.user.redis

    file_obj = req.request.files.get('user_file', None)
    content = file_obj[0]['body']

    f = open('%sadmin/my_value.py' % settings.BASE_ROOT, 'w+')  # A temp file to store HTTP body content, to facilitate the file reading process
    f.write(content)
    f.seek(0)

    l = []

    for i in f:
        l.append(i)

    for i in l:
        if 'uid' in i or 'data' in i:  # Simple condition selector to prevent misoperation.
            exec i

    # print_log('len l %d' % len(l))
    # print_log('inject data %s' % data)

    for i in data:
        if '|_combat_cache' in i[0]:
            continue
        temp = i[0].split('||')
        if '|_combat_cache' in i[0] or '|_god_field_combat_' in i[0]:
            continue
        temp[3] = uid2
        temp[2] = temp[3][:-7]             # Remove last 7 numbers of uid to get server id
        replaced_data = '||'.join(temp)
        if 'Friend' in replaced_data or 'association' in replaced_data:
            continue
        r.set(replaced_data, i[1])

    msgs = 'OK!'
    mm = ModelManager(uid2)
    mm.user.guild_id = ''
    mm.user.save()
    if reset_msg is None:
        reset_msg = []

    cur_date = time.localtime(mm.user.reg_time)
    cur_date = time.strftime('%Y-%m-%d %H:%M', cur_date)
    active_date = datetime.datetime.fromtimestamp(mm.user.active_time) if mm.user.active_time else ''

    return select(req, **{'msg': msgs})

    # return render(req, 'admin/user/user.html', **{
    #     'user': mm.user,
    #     'reset_msg': reset_msg,
    #     'user_attrs': user_attrs,
    #     'msgs': msgs,
    #     'settings': settings,
    #     'cur_date': cur_date,
    #     'active_date': active_date,
    # })


@require_permission
def finish_all_guide(req):
    uid = req.get_argument('uid')
    if uid:
        mm = ModelManager(uid)
        userl = UserLogic(mm)
        for sort, v in game_config.guide.iteritems():
            step = max(v)
            userl.do_guide(sort, step, True, True)
    return select(req, **{'msg': u'finish all guide'})


@require_permission
def reset_mission_main(req, **kwargs):
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail1'})

    task_id = int(req.get_argument('task_id', 0))

    if not task_id:
        return select(req, **{'msg': 'sort or key not empty'})

    mission_side_save = False
    mm.mission_main.reset()
    mm.mission_side.reset()

    for k in sorted(game_config.mission_main):
        if k == task_id:
            break
        if k not in mm.mission_main.done:
            mm.mission_main.done.append(k)
        config = game_config.mission_main[k]
        if config['mission_side']:
            mm.mission_side.refresh_next_task(config['mission_side'])
            mission_side_save = True

    mm.mission_main.refresh_next_task(task_id)
    mm.mission_main.save()
    if mission_side_save:
        mm.mission_side.save()

    msg = 'success'

    return select(req, **{'msg': msg})


@require_permission
def reset_mission_side(req, **kwargs):
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail1'})

    task_ids = req.get_argument('task_ids', '')

    if not task_ids:
        return select(req, **{'msg': 'sort or key not empty'})

    mm.mission_side.reset()
    for task_id in task_ids.split(','):
        if not task_id:
            continue
        task_id = int(task_id)

        mm.mission_side.refresh_next_task(task_id)

    mm.mission_side.save()

    msg = 'success'

    return select(req, **{'msg': msg})


@require_permission
def select_high_ladder(req, msg=''):
    """
    查看竞技场
    :param req:
    :return:
    """
    uid = req.get_argument('uid')
    result = {'self_rank': 0, 'uid': uid, 'msg': msg, 'mm': None}
    if uid:
        mm = ModelManager(uid)
        high_ladder_rank = mm.get_obj_tools('high_ladder_rank')
        result['self_rank'] = high_ladder_rank.get_rank(uid)
        result['mm'] = mm
    return render(req, 'admin/user/high_ladder_index.html', **result)


@require_permission
def modify_high_ladder_rank(req):
    """
    修改竞技场排名
    :param req:
    :return:
    """
    from logics.high_ladder import HighLadderLogic
    uid = req.get_argument('uid')
    rank = int(req.get_argument('self_rank'))
    msg = ''

    if rank <= 0:
        msg = u'排名需要整数'

    mm = ModelManager(uid)
    high_ladder_rank = mm.get_obj_tools('high_ladder_rank')
    cur_rank = high_ladder_rank.get_rank(uid)

    if cur_rank != rank:
        count = high_ladder_rank.get_count()
        rank = count if rank > count else rank
        self_score = high_ladder_rank.get_multi_score([uid])[0]
        [[(target_uid, target_score)]] = high_ladder_rank.get_uids_by_rank([rank], withscores=True)

        high_ladder_rank.set_multi_score({uid: target_score, target_uid: self_score})
        hll = HighLadderLogic(mm)
        hll.refresh_enemy(force=True)
        hll.high_ladder.save()
        if 'robot_' not in target_uid:
            hll = HighLadderLogic(mm.get_mm(target_uid))
            hll.refresh_enemy(force=True)
            hll.high_ladder.save()

    return select_high_ladder(req, msg)


@require_permission
def modify_high_ladder_enemy(req):
    """
    修改竞技场敌人排名
    :param req:
    :return:
    """
    uid = req.get_argument('uid')
    def_enemy = int(req.get_argument('def_enemy'))
    rank = int(req.get_argument('rank'))

    mm = ModelManager(uid)
    if not 0 < def_enemy < len(mm.high_ladder.def_enemy):
        mm.high_ladder.def_enemy[def_enemy] = rank
        mm.high_ladder.save()

    return select_high_ladder(req)


def by_name_jump_guide(req):
    success = []
    uid = req.get_argument('uid', '')
    name_list = req.get_argument('name_list', '')
    uid_list = []
    if name_list and uid:
        # 通过名字获取uid
        name_list = name_list.replace('\n', '').replace('\r', '').replace(' ', '').split(',')
        for name in name_list:
            for server_id in ServerUidList().all_server():
                mm = ModelManager('%s1234567' % server_id)
                online_users = mm.get_obj_tools('online_users')
                for uid in online_users.get_uids_by_active_days(0):
                    mm = ModelManager(uid)
                    if name in mm.user.name and uid not in uid_list:
                        uid_list.append(uid)
            if not uid_list:
                continue
            for i in uid_list:
                mm = ModelManager(i)
                userl = UserLogic(mm)
                for sort, v in game_config.guide.iteritems():
                    step = max(v)
                    userl.do_guide(sort, step, True, True)
                success.append(i)

    return render(req, 'admin/user/jump_guide.html', **{
        'success': len(success),
        'uid': uid,
        'name_list': name_list
    })


@require_permission
def ban_user(req):
    uid = req.get_argument('user_id')
    chat_type = req.get_argument('chat_type', '')
    is_ban = int(req.get_argument('is_ban'))
    if is_ban:
        is_ban = 1
    ban_expire = int(float(req.get_argument('ban_expire', 0)))
    ban_days = int(float(req.get_argument('ban_days', 0)))
    if ban_days:
        ban_expire = int(time.time()) + ban_days*86400
    ban_reason = req.get_argument('ban_reason', '')
    global_redis = OnlineUsers(server='public')
    global_redis = global_redis.redis
    if uid:
        mm = ModelManager(uid)
        u = mm.user
        if is_ban:
            # 过期时间作为value记进去
            global_redis.zadd(ALL_BAN_UIDS_KEY, **{u.uid: ban_expire})
            u.ban_user(is_ban, ban_expire, ban_reason=ban_reason, uname=req.uname)
        else:
            global_redis.zrem(ALL_BAN_UIDS_KEY, u.uid)
            u.ban_user(is_ban, 0, ban_time=0)
        u.save()
        return select(req, **{'msg': u'封禁成功'})
    return select(req, **{'msg': u'error:unexpected uid'})


def watch_ban_uids(req):
    global_redis = OnlineUsers(server='public')
    global_redis = global_redis.redis
    global_redis.zremrangebyscore(ALL_BAN_UIDS_KEY, 1, time.time())     # 删除已过封禁期的id
    uids = global_redis.zrange(ALL_BAN_UIDS_KEY, 0, -1)
    uid_infos = {}
    for uid in uids:
        mm = ModelManager(uid)
        u = mm.user
        uid_infos[uid] = {
            'ban_time': u.ban_time,
            'ban_expire': u.ban_expire,
            'ban_reason': u.ban_reason,
            'ban_person': u.ban_person,
        }
    data = {
        'uid_infos': uid_infos,
    }
    return render(req, 'admin/gs/ban_info.html', **data)


def watch_ban_ips(req):
    global_redis = OnlineUsers(server='public')
    global_redis = global_redis.redis
    global_redis.zremrangebyscore(ALL_BAN_IPS_KEY, 1, time.time())     # 删除已过封禁期的id
    uids = global_redis.zrange(ALL_BAN_IPS_KEY, 0, -1)
    uid_infos = {}
    for uid in uids:
        mm = ModelManager(uid)
        u = mm.user
        uid_infos[uid] = {
            'ban_time': u.ban_time,
            'ban_expire': u.ban_expire,
            'ban_reason': u.ban_reason,
            'ban_person': u.ban_person,
        }
    data = {
        'uid_infos': uid_infos,
    }
    return render(req, 'admin/gs/ip_ban_info.html', **data)


