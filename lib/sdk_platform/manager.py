# -*- coding: utf-8 -*-

"""
sdk管理器
"""
import settings


class SDKManager(object):

    all_model_cls = {}

    def __init__(self):
        self.attrs = {}

    @classmethod
    def register(cls, model_name, model_cls):
        cls.all_model_cls[model_name] = model_cls

    @classmethod
    def get_attr_key(cls, sdk, pf):
        return "_%s_%s" % (sdk, pf)

    def get_sdk(self, sdk, pf, *args, **kwargs):
        attr_key = self.get_attr_key(sdk, pf)

        if attr_key in self.attrs:
            obj = self.attrs[attr_key]
        else:
            model_cls = self.all_model_cls.get(sdk)
            obj = model_cls(pf, *args, **kwargs)

            self.attrs[attr_key] = obj

        return obj


sdk_manager = SDKManager()
