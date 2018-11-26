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
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if modify:
        equip_id = int(req.get_argument('equip_id'))
        equip_num = int(req.get_argument('equip_num'))

        mm.equip.equips[equip_id] = equip_num
    elif delete:
        equip_id = int(req.get_argument('equip_id'))

        mm.equip.equips.pop(equip_id, None)
    else:
        return select(req, **{'msg': 'fail'})

    mm.equip.save()

    return select(req, **{'msg': 'success'})


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
            if param_name not in game_config.equip:
                result['msg'] = 'fail'
                return render(req, 'admin/equip/add_equip.html', **result)
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.equip.add_equip(param_name, param_value)

        mm.equip.save()
        result['msg'] = 'success'

    return render(req, 'admin/equip/add_equip.html', **result)


@require_permission
def add_piece(req, **kwargs):
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
            return render(req, 'admin/equip/add_piece.html', **result)

        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/equip/add_piece.html', **result)

        params = req.get_reg_params(r'^piece_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.equip.add_piece(param_name, param_value)

        mm.equip.save()
        result['msg'] = 'success'

    return render(req, 'admin/equip/add_piece.html', **result)


@require_permission
def piece_update(req, **kwargs):
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
    if mm.equip.inited:
        return select(req, **{'msg': 'fail'})

    if modify:
        piece_id = int(req.get_argument('piece_id'))
        piece_num = int(req.get_argument('piece_num'))
        mm.equip.equip_pieces[piece_id] = piece_num
        mm.equip.save()
        msg = 'success'
    elif delete:
        piece_id = int(req.get_argument('piece_id'))
        mm.equip.equip_pieces.pop(piece_id, None)
        mm.equip.save()
        msg = 'success'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})

