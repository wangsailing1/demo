#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config

MAX_NUM = 999

@require_permission
def select(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'hero': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['hero'] = mm.hero
        result['mm'] = mm

    return render(req, 'admin/hero/index.html', **result)


@require_permission
def hero_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    hero_oid = req.get_argument('hero_oid')
    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.hero.inited:
        return select(req, **{'msg': 'fail'})

    if mm.hero.has_hero(hero_oid):
        if modify:
            lv = int(req.get_argument('lv'))
            star = int(req.get_argument('star'))
            evo = int(req.get_argument('evo'))
            hero_dict = mm.hero.heros.get(hero_oid)
            if not hero_dict:
                msg = 'fail'
            else:
                max_level = game_config.hero_lvl_limit.get(mm.user.level, {}).get('hero_lvl', 0)
                hero_config = game_config.hero_basis[hero_dict['id']]
                star_limit = max(game_config.hero_star or [1])
                max_evo = len(game_config.grade_lvlup_badge.get(hero_config['job'], {}).get(hero_config['quality'], {}))

                hero_dict['lv'] = min(lv, max_level)
                hero_dict['star'] = min(star, star_limit)
                hero_dict['evo'] = min(evo, max_evo)
                mm.hero.unlock_skill(hero_oid, hero_dict=hero_dict)
                mm.hero.update_base_attr(hero_oid, hero_dict=hero_dict, hero_config=hero_config)
                # mm.hero.calc_avg_max_evo()

                mm.hero.save()
                msg = 'success'
        elif delete:
            mm.hero.del_hero(hero_oid)
            mm.hero.save()
            msg = 'success'
        else:
            msg = 'fail'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


@require_permission
def stone_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.hero.inited:
        return select(req, **{'msg': 'fail'})

    if modify:
        stone_id = int(req.get_argument('stone_id'))
        stone_num = int(req.get_argument('stone_num'))
        mm.hero.stones[stone_id] = stone_num
        mm.hero.save()
        msg = 'success'
    elif delete:
        stone_id = int(req.get_argument('stone_id'))
        mm.hero.stones.pop(stone_id, None)
        mm.hero.save()
        msg = 'success'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


@require_permission
def add_hero(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/hero/add_hero.html', **result)

        hero_ids = req.get_arguments('hero_id')
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/hero/add_hero.html', **result)

        for hero_id in hero_ids:
            hero_id = int(hero_id)
            if hero_id not in game_config.hero_basis:
                result['msg'] = 'fail'
                return render(req, 'admin/hero/add_hero.html', **result)

            if mm.hero.has_hero_with_hero_id(hero_id):
                continue

            mm.hero.add_hero(hero_id)
        mm.hero.save()
        result['msg'] = 'success'

    return render(req, 'admin/hero/add_hero.html', **result)


@require_permission
def add_stone(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/hero/add_stone.html', **result)

        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/hero/add_stone.html', **result)

        params = req.get_reg_params(r'^stone_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.hero.add_stone(param_name, param_value)

        mm.hero.save()
        result['msg'] = 'success'

    return render(req, 'admin/hero/add_stone.html', **result)


@require_permission
def select_attr(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    hid = req.get_argument('hid', '')
    result = {'hero_data': {}, 'uid': uid, 'hid': hid, 'msg': ''}
    result.update(kwargs)
    if uid and not hid:
        mm = ModelManager(uid)
        result['mm'] = mm
        return render(req, 'admin/hero/hero_attr.html', **result)
    if uid and hid:
        mm = ModelManager(uid)
        result['mm'] = mm
        for i, j in mm.hero.heros.iteritems():
            hero_id = i.split('-')[0]
            if hid != hero_id:
                continue
            result['hero_data'] = j
            break
        else:
            result['msg'] = u'没有改英雄'

        result['attr_mapping'] = game_config.ATTR_MAPPING

    return render(req, 'admin/hero/hero_attr.html', **result)
