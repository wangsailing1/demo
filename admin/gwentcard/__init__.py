#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config


@require_permission
def select(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'gwent_card': None, 'uid': uid, 'msg': '', 'card_detail': game_config.card_detail}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['gwent_card'] = mm.gwent_card

    return render(req, 'admin/gwent_card/index.html', **result)


@require_permission
def gwent_card_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    card_oid = int(req.get_argument('card_oid'))

    mm = ModelManager(uid)
    if mm.gwent_card.inited:
        return select(req, **{'msg': 'fail'})

    if card_oid in mm.gwent_card.gcard:
        mm.gwent_card.delete_gcard(card_oid)
        mm.gwent_card.save()
        msg = 'success'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


@require_permission
def add_gcard(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid}

    if req.request.method == 'POST':
        gcard_ids = req.get_arguments('gcard_id')
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/gwent_card/add_gcard.html', **result)

        for gcard_id in gcard_ids:
            gcard_id = int(gcard_id)
            if gcard_id not in game_config.card_detail:
                result['msg'] = 'fail'
                return render(req, 'admin/gwent_card/add_gcard.html', **result)

            mm.gwent_card.add_gcard(gcard_id)
        mm.gwent_card.save()
        result['msg'] = 'success'

    return render(req, 'admin/gwent_card/add_gcard.html', **result)
