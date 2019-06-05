#! --*-- encoding: utf-8 --*--
from kombu.utils import json
from tornado.web import RequestHandler
import importlib
from logics import HandlerManager
from pycket.session import SessionMixin
class BaseRequestHandler(RequestHandler, SessionMixin):
    """
    所有请求的基类
    """
    @property
    def handers(self):

        return self.request.handers

    @property
    def body(self):
        return self.request.body

    def get_current_user(self):
        current_user = self.get_secure_cookie('account')
        if current_user:
            return current_user
        return None



class APIRequestHandler(BaseRequestHandler):
    """
    全部api处理数据公共接口
    """
    def get(self):
        self.api()

    def post(self, *args, **kwargs):
        self.api()

    def initialize(self):
        self.hm = HandlerManager(self)

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
            rc, data = method(self.hm)
            if rc != 0:
                self.result_info('err', data)
            rc, data = self.result_info(rc, data)
            r = {'status':rc, 'data':data}
            result = json.dumps(r, separators=(',', ':'), encoding="utf-8",)
            try:
                self.write(result)
            finally:
                self.finish()
        return self.result_info('error_not_call_method')


    def result_info(self, rc, data=None):
        msg = ''
        if data is None:
            data = {'msg':''}
        return rc, data

class TempLateHandler(APIRequestHandler):
    """
    用来返回各种页面
    """
    def get(self):
        template = self.hm.get_argument('template', '')
        if not template:
            rc, data = 1, {'msg':'静态文件错误'}
            r = {'status': rc, 'data': data}
            result = json.dumps(r, separators=(',', ':'), encoding="utf-8", )
            self.write(result)
            self.finish()
        return TempLateHandler.render(self, template)

class IndexHandler(BaseRequestHandler):
    """
    用来返回首页
    :param BaseRequestHandler:
    :return:
    """
    def get(self):
        return IndexHandler.render(self, 'index.html')















