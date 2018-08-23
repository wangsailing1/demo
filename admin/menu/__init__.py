#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from admin import render
from admin.decorators import require_permission


def logout(req):
    return render(req, 'admin/login.html', **{'msgs': []})


@require_permission
def index(req, *args, **kwargs):
    """

    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    return render(req, 'admin/main.html', **{})


@require_permission
def left(req, *args, **kwargs):
    """

    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    return render(req, 'admin/left.html', **{})


@require_permission
def top(req, *args, **kwargs):
    """

    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    menu = req.get_argument('menu', 'select')
    return render(req, 'admin/info_view.html', **{'menu': menu})


@require_permission
def content(req, *args, **kwargs):
    """

    :param req:
    :param args:
    :param kwargs:
    :return:
    """
    return render(req, 'admin/content.html')
