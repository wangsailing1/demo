#! --*-- encoding: utf-8 --*--
from tornado.web import RequestHandler
import importlib

class BaseRequestHandler(RequestHandler):
    """
    所有请求的基类
    """
    @property
    def handers(self):

        return self.request.handers

    @property
    def body(self):
        return self.request.body




class User(BaseRequestHandler):

    def api(self):
        method_params = self.get_argument('method')
        module_name, method_name = method_params.split('.')
        try:
            module = importlib.import_module('views.%s' % module_name)
        except Exception as e:
            print(e)
            return self.result_info('error_module')
        method = getattr(module, method_name, None)
        if method is None:
            return self.result_info('err_method')

        if callable(method):
            rc, data = method(self)
            if rc != 0:
                self.result_info('err', data)
            self.result_info(rc, data)

        return self.result_info('error_not_call_method')

    def result_info(self, rc, data=None):
        msg = ''
        if data is None:
            data = {}

        return rc,data






