#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import importlib

from lib.core.handlers.htornado import BaseRequestHandler


class AdminHandler(BaseRequestHandler):

    def get(self, module_name, func_name=None):
        """ get请求

        :param module_name:
        :param func_name:
        :return:
        """
        if func_name:
            module = importlib.import_module('admin.%s' % module_name)
            method = getattr(module, func_name)
            self.module_name = module_name
            self.method_name = func_name
        else:
            module = importlib.import_module('admin.menu')
            method = getattr(module, module_name)
            self.module_name = 'menu'
            self.method_name = module_name
        return method(self)

    def post(self, module_name, func_name=None):
        """ post请求

        :param module_name:
        :param func_name:
        :return:
        """
        return self.get(module_name, func_name=func_name)
