#! --*-- coding: utf-8 --*--

__author__ = 'sm'


import tornado

import settings
import admin.admin_config
from admin import render
from admin.decorators import require_permission, ApprovalPayment
from admin.admin_models import Admin

@require_permission
def approval_index(req, msg=None):
    """ 审批首页

    :param req:
    :param msg:
    :return:
    """

    record = ApprovalPayment().get_all_payment()

    args = {
        'record': record,
        'message': msg if msg else '',
    }

    return render(req, 'admin/approval/index.html', **args)

@require_permission
def for_approval(req):
    """ 进行审批

    :param req:
    :param msg:
    :return:
    """
    checkbox_unrefuses = req.get_arguments('checkbox_unrefuse')
    checkbox_refuses = req.get_arguments('checkbox_refuse')

    approval_payment = ApprovalPayment()

    for key in checkbox_unrefuses:
        approval_payment.approval_payment(req.uname, key, refuse=False)

    for key in checkbox_refuses:
        approval_payment.approval_payment(req.uname, key, refuse=True)

    return approval_index(req, msg=u'成功')

@require_permission
def search_approval(req, msg=None):
    """ 查询审批后的数据

    :param req:
    :return:
    """
    approval_payment = ApprovalPayment()

    record = approval_payment.get_all_approval_log()

    args = {
        'record': record,
        'message': msg if msg else '',
    }

    return render(req, 'admin/approval/search.html', **args)
