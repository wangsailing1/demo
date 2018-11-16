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
    result = {'card': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['card'] = mm.card
        result['mm'] = mm

    return render(req, 'admin/card/index.html', **result)


@require_permission
def card_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    card_oid = req.get_argument('card_oid')
    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.card.inited:
        return select(req, **{'msg': 'fail'})

    if mm.card.has_card(card_oid):
        if modify:
            lv = int(req.get_argument('lv'))
            star = int(req.get_argument('star'))
            evo = int(req.get_argument('evo'))
            card_dict = mm.card.cards.get(card_oid)
            if not card_dict:
                msg = 'fail'
            else:
                max_level = game_config.card_lvl_limit.get(mm.user.level, {}).get('card_lvl', 0)
                card_config = game_config.card_basis[card_dict['id']]
                star_limit = max(game_config.card_star or [1])
                max_evo = len(game_config.grade_lvlup_badge.get(card_config['job'], {}).get(card_config['quality'], {}))

                card_dict['lv'] = min(lv, max_level)
                card_dict['star'] = min(star, star_limit)
                card_dict['evo'] = min(evo, max_evo)
                mm.card.unlock_skill(card_oid, card_dict=card_dict)
                mm.card.update_base_attr(card_oid, card_dict=card_dict, card_config=card_config)
                # mm.card.calc_avg_max_evo()

                mm.card.save()
                msg = 'success'
        elif delete:
            mm.card.del_card(card_oid)
            mm.card.save()
            msg = 'success'
        else:
            msg = 'fail'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


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
    if mm.card.inited:
        return select(req, **{'msg': 'fail'})

    if modify:
        piece_id = int(req.get_argument('piece_id'))
        piece_num = int(req.get_argument('piece_num'))
        mm.card.pieces[piece_id] = piece_num
        mm.card.save()
        msg = 'success'
    elif delete:
        piece_id = int(req.get_argument('piece_id'))
        mm.card.pieces.pop(piece_id, None)
        mm.card.save()
        msg = 'success'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


@require_permission
def add_card(req, **kwargs):
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
            return render(req, 'admin/card/add_card.html', **result)

        card_ids = req.get_arguments('card_id')
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/card/add_card.html', **result)

        for card_id in card_ids:
            card_id = int(card_id)
            if card_id not in game_config.card_basis:
                result['msg'] = 'fail'
                return render(req, 'admin/card/add_card.html', **result)

            if mm.card.has_card_with_group_id(card_id):
                continue

            mm.card.add_card(card_id)
        mm.card.save()
        result['msg'] = 'success'

    return render(req, 'admin/card/add_card.html', **result)


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
            return render(req, 'admin/card/add_piece.html', **result)

        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/card/add_piece.html', **result)

        params = req.get_reg_params(r'^piece_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.card.add_piece(param_name, param_value)

        mm.card.save()
        result['msg'] = 'success'

    return render(req, 'admin/card/add_piece.html', **result)


@require_permission
def select_attr(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    hid = req.get_argument('hid', '')
    result = {'card_data': {}, 'uid': uid, 'hid': hid, 'msg': ''}
    result.update(kwargs)
    if uid and not hid:
        mm = ModelManager(uid)
        result['mm'] = mm
        return render(req, 'admin/card/card_attr.html', **result)
    if uid and hid:
        mm = ModelManager(uid)
        result['mm'] = mm
        for i, j in mm.card.cards.iteritems():
            card_id = i.split('-')[0]
            if hid != card_id:
                continue
            result['card_data'] = j
            break
        else:
            result['msg'] = u'没有改英雄'

        result['attr_mapping'] = game_config.ATTR_MAPPING

    return render(req, 'admin/card/card_attr.html', **result)
