#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import os
import importlib
import types

# sdk平台

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
_exclude_files = ['__init__', 'sdk_manager']


def load():
    """
    """
    import lib

    if lib.SDK_PLATFORM_STATUS:
        return
    lib.SDK_PLATFORM_STATUS = True
    for _root, _dirs, _files in os.walk(CUR_PATH):
        for _f in _files:
            _name, _ext = os.path.splitext(_f)
            if _ext == '.py' and _name not in _exclude_files:
                module = importlib.import_module('lib.sdk_platform.%s' % _name)
                # for func_name in dir(module):
                #     if func_name.startswith('__'):
                #         continue
                #     print 'func_name: ', func_name
                #     func = getattr(module, func_name)
                #     if isinstance(func, (types.DictionaryType, types.TupleType)):
                #         globals()[func_name] = func

# load()
