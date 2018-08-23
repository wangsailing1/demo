#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import re

from tornado.web import RequestHandler
from tornado.util import unicode_type


class BaseRequestHandler(RequestHandler):
    """
    
    """

    def summary_params(self):
        """

        """

        return self.request.arguments

    @property
    def headers(self):
        """ 获取

        :return:
        """
        return self.request.headers

    @property
    def body(self):
        """

        :return:
        """
        return self.request.body

    def params(self, strip=True):
        data = {}
        for name, values in self.request.arguments.iteritems():
            vs = []
            for v in values:
                v = self.decode_argument(v, name=name)
                if isinstance(v, unicode_type):
                    v = RequestHandler._remove_control_chars_regex.sub(" ", v)
                if strip:
                    v = v.strip()
                vs.append(v)
            data[name] = vs[-1]
        return data

        # tornaod 4.x 之后才有的参数
        # query_source = self.request.query_arguments
        # body_source = self.request.body_arguments
        # for source in (query_source, body_source):
        #     for name, values in source.iteritems():
        #         vs = []
        #         for v in values:
        #             v = self.decode_argument(v, name=name)
        #             if isinstance(v, unicode_type):
        #                 v = RequestHandler._remove_control_chars_regex.sub(" ", v)
        #             if strip:
        #                 v = v.strip()
        #             vs.append(v)
        #         data[name] = vs[-1]
        # return data

    def get_reg_params(self, reg_str, key_sort=int, value_sort=int, value_filter=None):
        """ 通过正则表达式获取参数和值, 返回[(key, value)]

        :param reg_str: 正在表达式
        :param key_sort: key的类型, 默认int
        :param value_sort: value的类型, 默认int
        :param value_filter: 过滤value值, value值为0过滤掉参数
        :return:
        """
        comp = re.compile(reg_str)
        p = []
        params = self.summary_params()
        for param_name, param_value in params.iteritems():
            for name in comp.findall(param_name):
                value = value_sort(param_value[0])
                if value != value_filter:
                    name = key_sort(name)
                    p.append((name, value))

        return p
