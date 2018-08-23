#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from models.server import ServerUidList


@require_permission
def select_name(req, **kwargs):
    """

    :param req:
    :return:
    """

    name = req.get_argument('name', '')
    server_id = req.get_argument('server_id', '')
    result = {'name': name, 'server_id': server_id, 'uid_list': [], 'msg': ''}
    result.update(kwargs)
    uid_list = {}
    if name and server_id:
        mm = ModelManager('%s1234567' % server_id)
        uids = mm.user.get_uid_by_name(name)
        for uid in uids:
            uid_list[uid] = name
        result['uid_list'] = uid_list

    return render(req, 'admin/user/select_name.html', **result)
