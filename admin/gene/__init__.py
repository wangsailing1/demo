#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config

MAX_NUM = 99

@require_permission
def select(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'gene': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['gene'] = mm.gene
        result['mm'] = mm
    # print '66666666', result
    return render(req, 'admin/gene/index.html', **result)


@require_permission
def gene_update(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')
    gene_oid = req.get_argument('gene_oid')
    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.gene.inited:
        return select(req, **{'msg': 'fail1'})

    if mm.gene.has_gene(gene_oid):
        if modify:
            lv = int(req.get_argument('lv'))
            star = int(req.get_argument('star'))
            evo = int(req.get_argument('evo'))
            gene_dict = mm.gene.genes.get(gene_oid)
            if not gene_dict:
                msg = 'fail'
            else:
                max_star = max(game_config.gene_starup)
                star = min(star, max_star)
                # max_lv = max(game_config.gene_lvlup)
                # lv = min(lv, max_lv)
                max_evo = max(game_config.gene_evoup)
                evo = min(evo, max_evo)

                gene_dict['lv'] = lv
                gene_dict['new_star'] = evo
                gene_dict['star'] = star
                mm.gene.update_base_attr(gene_dict)

                mm.gene.save()
                msg = 'success'
        elif delete:
            mm.gene.del_gene(gene_oid, force=True)
            mm.gene.save()
            msg = 'success'
        else:
            msg = 'fail'
    else:
        msg = 'fail'

    return select(req, **{'msg': msg})


@require_permission
def add_gene(req, **kwargs):
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
            return render(req, 'admin/gene/add_gene.html', **result)

        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/gene/add_gene.html', **result)

        params = req.get_reg_params(r'^gene_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_name not in game_config.gene_basis:
                result['msg'] = 'fail'
                return render(req, 'admin/gene/add_gene.html', **result)
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            for i in xrange(param_value):
                mm.gene.add_gene(param_name, force=True)

        mm.gene.save()
        result['msg'] = 'success'

    return render(req, 'admin/gene/add_gene.html', **result)
