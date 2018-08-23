#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import os
import importlib


CUR_PATH = os.path.abspath(os.path.dirname(__file__))
_exclude_files = ['__init__']


def register():
    """
    """
    import settings

    if settings.REGISTER_MODELS_STATUS:
        return
    settings.REGISTER_MODELS_STATUS = True
    for _root, _dirs, _files in os.walk(CUR_PATH):
        for _f in _files:
            _name, _ext = os.path.splitext(_f)
            if _ext == '.py' and _name not in _exclude_files:
                module = importlib.import_module('models.%s' % _name)
                # print 'register: ', module

register()
