#! --*-- encoding: utf-8 --*--
import weakref
class ModelManager(object):
    _register_base = {}
    def __init__(self, uid, async_save=False):
        self.uid = uid
        self.async_save = async_save
        self._model = {}
        self._mm = {}

    @classmethod
    def register_model(cls, model_name, model):
        """ 注册modelbase, 异步保存
        :param model_name:
        :param model:
        :return:
        """
        cls._register_base[model_name] = model
        setattr(cls, model_name, property(**cls.property_template(model_name)))


    @classmethod
    def property_template(cls, model_name):
        doc = 'The %s property.' % model_name
        def fget(self):
            return self._get_obj(model_name)
        def fset(self, value):
            key = '%s_%s' % (self.uid, model_name)
            self._model[key] = value
        def fdel(self):
            key = '%s_%s' % (self.uid, model_name)
            del self._model[key]
        return {
            'doc':doc,
            'fget':fget,
            'fset':fset,
            'fdel':fdel,
        }

    def _get_obj(self, model_name):
        """ 获取model对象
        :param model_name:
        :return:
        """
        key = '%s_%s' % (self.uid, model_name)
        if key in self._model:
            obj = self._model[key]
        elif model_name in self._register_base:
            mm_proxy= weakref.proxy(self)
            obj = self._register_base[model_name].get(self.uid, mm=mm_proxy)
            obj.aslync = self.async_save
            obj._model_name= model_name
            setattr(obj, 'mm', mm_proxy)
            self._model[key] = obj
            if hasattr(obj, 'pre_use'):
                obj.pre_use()
        else:
            obj = None
        return obj

    def do_save(self, is_save=True):
        for obj in self._model.itervalues():
            print self._model
            obj._save()
        for mm_obj in self._mm.itervalues():
            print self._mm
            mm_obj.do_save(is_save)

class HandlerManager(object):
    """ 请求管理类

    """

    def __init__(self, request_handler):
        """

        :param request_handler:
        :return:
        """
        self.req = request_handler
        self.get_arguments = self.req.get_arguments
        uid = self.get_argument('uid', '')
        if uid:
            self.mm = ModelManager(uid)
        else:
            self.mm = None
    _ARG_DEFAULT  =[]
    def get_argument(self, name, default=_ARG_DEFAULT, is_int=False, strip=True):
        """

        :param name:
        :param default:
        :param is_int:
        :param strip:
        :return:
        """
        value = self.req.get_argument(name, default=default, strip=strip)
        if not value:
            return 0 if is_int else ''

        return abs(int(float(value))) if is_int else value

