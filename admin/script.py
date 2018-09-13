# -*- coding: utf-8 –*-

"""
Created on 2018-09-11

@author: sm
"""

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config

MAX_NUM = 1


@require_permission
def select(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'script': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['script'] = mm.script
        result['mm'] = mm

    return render(req, 'admin/script/index.html', **result)


@require_permission
def add_script(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM, 'script': None}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/script/add_script.html', **result)

        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/script/add_script.html', **result)

        params = req.get_reg_params(r'^script_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_name not in game_config.script:
                result['msg'] = 'fail'
                return render(req, 'admin/script/add_script.html', **result)
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.script.add_own_script(param_name)

        mm.script.save()
        result['msg'] = 'success'
        result['script'] = mm.script

    return render(req, 'admin/script/add_script.html', **result)


@require_permission
def script_update(req, **kwargs):
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

    delete = req.get_argument('delete', '')

    if delete:
        script_id = int(req.get_argument('script_id'))
        if script_id in mm.script.own_script:
            mm.script.own_script.remove(script_id)
    else:
        return select(req, **{'msg': 'fail'})

    mm.script.save()

    return select(req, **{'msg': 'success'})
