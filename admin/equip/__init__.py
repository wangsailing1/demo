#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config

MAX_NUM = 100

@require_permission
def select(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'equip': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['equip'] = mm.equip
        result['mm'] = mm

    return render(req, 'admin/equip/index.html', **result)


@require_permission
def equip_update(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')
    equip_oid = req.get_argument('equip_oid')
    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.equip.inited:
        return select(req, **{'msg': 'fail1'})

    if mm.equip.has_equip(equip_oid):
        if modify:
            lv = int(req.get_argument('lv'))
            quality = int(req.get_argument('quality'))
            evo = int(req.get_argument('evo'))
            equip_dict = mm.equip.equips.get(equip_oid)
            if not equip_dict:
                msg = 'fail'
            else:
                max_quality = max(game_config.equip_color)
                quality = min(quality, max_quality)
                max_lv = max(game_config.equip_lvlup)
                lv = min(lv, max_lv)
                max_evo = game_config.equip_color.get(quality, {}).get('lvlup_limit', 1)
                evo = min(evo, max_evo)

                equip_dict['lv'] = lv
                equip_dict['evo'] = evo
                equip_dict['quality'] = quality
                mm.equip.update_base_attr(equip_dict)

                mm.equip.save()
                msg = 'success'
        elif delete:
            mm.equip.del_equip(equip_oid, force=True)
            mm.equip.save()
            msg = 'success'
        else:
            msg = 'fail'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


@require_permission
def add_equip(req, **kwargs):
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
            return render(req, 'admin/equip/add_equip.html', **result)

        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/equip/add_equip.html', **result)

        params = req.get_reg_params(r'^equip_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_name not in game_config.equip_basis:
                result['msg'] = 'fail'
                return render(req, 'admin/equip/add_equip.html', **result)
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            for i in xrange(param_value):
                mm.equip.add_equip(param_name, force=True)

        mm.equip.save()
        result['msg'] = 'success'

    return render(req, 'admin/equip/add_equip.html', **result)
