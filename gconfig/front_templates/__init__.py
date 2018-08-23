#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import os
import importlib
import types

# 前端模板

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
_exclude_files = ['__init__']


def load():
    """
    """
    import gconfig
    import settings

    if gconfig.FRONT_CONFIG_TEMPLATES_STATUS:
        return
    gconfig.FRONT_CONFIG_TEMPLATES_STATUS = True
    for _root, _dirs, _files in os.walk(CUR_PATH):
        for _f in _files:
            _name, _ext = os.path.splitext(_f)
            if _ext == '.py' and _name not in _exclude_files:
                module = importlib.import_module('gconfig.front_templates.%s' % _name)
                for func_name in dir(module):
                    if func_name.startswith('__'):
                        continue
                    func = getattr(module, func_name)
                    if isinstance(func, (types.DictionaryType, types.TupleType)):
                        if func_name in globals():
                            print 'front_templates %s repeat' % func_name
                        globals()[func_name] = func
                        if func_name not in settings.FRONT_CONFIG_NAME_LIST:
                            settings.FRONT_CONFIG_NAME_LIST.append(func_name)

load()
