#! --*-- coding: utf-8 --*--

__author__ = 'sm'


import settings
import weakref


def func_type(value):
    try:
        return abs(int(value))
    except:
        return value


class HandlerManager(object):
    """ 请求管理类

    """

    def __init__(self, request_handler):
        """

        :param request_handler:
        :return:
        """
        self.req = request_handler
        self.params = self.req.params
        self.get_arguments = self.req.get_arguments
        self.uid = self.req.get_argument('user_token', '')
        if not settings.check_uid(self.uid):
            self.uid = ''
        self.mm_class = ModelManager
        if self.uid:
            self.mm = ModelManager(self.uid, async_save=True)
            self.mm.action = self.req.get_argument('method', '')
            self.mm.args = self.params()
        else:
            self.mm = None

    _ARG_DEFAULT = []

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

    PARAMS_TYPE = (int, int)

    def get_mapping_arguments(self, name, params_type=PARAMS_TYPE, split='_', result_type=list):
        """ 获取多个参数, 仅支持arg=1_1&arg=1_2 或 arg=x_1&arg=y_1

        :param name: 参数名
        :param params_type: 参数默认类型
        :param num: 分割数量
        :param split: 分隔符
        :param result_type: 返回的类型 list, dict
        :return: [(1: 1), (1: 2)]
        """
        args = self.get_arguments(name)
        values = []
        num = len(params_type)
        func = lambda x: [v(x[k]) for k, v in enumerate(params_type)]
        for arg in args:
            if arg.startswith('nil_'):  # 过滤前端战斗的召唤物
                continue
            arg_list = arg.split(split)
            if arg_list and len(arg_list) == num:
                if params_type:
                    values.append(func(arg_list))
                else:
                    values.append(arg_list)
        if not isinstance(values, result_type):
            values = result_type(values)
        return values

    def get_mapping_argument(self, name, is_int=True, num=2, split='_'):
        """ 获取参数, 仅支持arg=1_1 或 arg=1_1_2

        :param name: 参数名
        :param is_int: 是否值都为int
        :param num: 值的个数, 不支持1个
        :param split:
        :return: [1, 2, 3]
        """
        arg_value = self.get_argument(name)
        values = []

        if not arg_value:
            return values

        arg_list = arg_value.split(split)

        arg_list = arg_list if arg_list else values

        if num and len(arg_list) != num:
            return values

        if is_int:
            return map(int, arg_list)
        else:
            return arg_list


class ModelManager(object):
    """ 管理类

    :var uid: 用户uid
    :var _model: model模块对象
    :var _register: 注册model类
    :var async_save: 是否异步保存
    :var action: 动作
    :var args: 参数
    :var _model_tools: model_tools模块对象
    :var _model_ids: 特殊的model模块对象, 例如公会guild
    :var _mm: ModelManager对象
    """
    _register_base = {}
    _register_base_tools = {}
    _register_base_iids = {}
    _register_events = {}

    def __init__(self, uid, async_save=False):
        self.uid = uid
        self.server = self.uid[:-7]
        self.async_save = async_save
        self.action = ''
        self.args = {}
        self._model = {}
        self._model_tools = {}
        self._model_ids = {}
        self._mm = {}
        self._events = {}

    @classmethod
    def register_model(cls, model_name, model):
        """ 注册modelbase, 异步保存

        :param model_name:
        :param model:
        :return:
        """
        from tools.task_event import TaskEventDispatch, TaskEventBase

        if model_name not in cls._register_base:
            cls._register_base[model_name] = model
            setattr(cls, model_name, property(**cls.property_template(model_name)))

            for base_class in model.__bases__:
                if issubclass(base_class, TaskEventBase):
                    TaskEventDispatch.register_model(model_name, model)
        else:
            old_model = cls._register_base[model_name]
            raise RuntimeError('model [%s] already exists \n'
                               'Conflict between the [%s] and [%s]' %
                               (model_name, old_model, model))

    @classmethod
    def register_model_base_tools(cls, model_name, model):
        """注册modeltools, 随时保存

        :param model_name:
        :param model:
        :return:
        """
        if model_name not in cls._register_base_tools:
            cls._register_base_tools[model_name] = model
        else:
            old_model = cls._register_base_tools[model_name]
            raise RuntimeError('model [%s] already exists \n'
                               'Conflict between the [%s] and [%s]' %
                               (model_name, old_model, model))

    @classmethod
    def register_model_iids(cls, model_name, model):
        """ 注册modelbase或者别的父类, 随时保存

        :param model_name:
        :param model:
        :return:
        """
        if model_name not in cls._register_base_iids:
            cls._register_base_iids[model_name] = model
        else:
            old_model = cls._register_base_iids[model_name]
            raise RuntimeError('model [%s] already exists \n'
                               'Conflict between the [%s] and [%s]' %
                               (model_name, old_model, model))

    @classmethod
    def register_events(cls, model_name, model):
        """ 注册object, 异步保存

        :param model_name:
        :param model:
        :return:
        """
        if model_name not in cls._register_events:
            cls._register_events[model_name] = model
        else:
            old_model = cls._register_events[model_name]
            raise RuntimeError('model [%s] already exists \n'
                               'Conflict between the [%s] and [%s]' %
                               (model_name, old_model, model))

    def get_model_key(self, uid, name):
        return "%s_%s" % (uid, name)

    # def __getitem__(self, model_name):
    #     """ 获取model对象
    #
    #     :param model_name: 字符串 user, hero
    #     :return:
    #     """
    #     return self._get_obj(model_name)

    # def __getattr__(self, model_name):
    #     """ 获取model对象
    #
    #     :param model_name:
    #     :return:
    #     """
    #     return self._get_obj(model_name)

    @classmethod
    def property_template(cls, model_name):
        doc = "The %s property." % model_name
        def fget(self):
            return self._get_obj(model_name)
        def fset(self, value):
            # key = self.get_model_key(self.uid, model_name)
            key = '%s_%s' % (self.uid, model_name)
            self._model[key] = value
        def fdel(self):
            # key = self.get_model_key(self.uid, model_name)
            key = '%s_%s' % (self.uid, model_name)
            del self._model[key]
        return {
            'doc': doc,
            'fget': fget,
            # 'fset': fset,
            'fdel': fdel,
        }

    def _get_obj(self, model_name):
        """ 获取model对象

        :param model_name: 字符串 user, hero
        :return:
        """
        # key = self.get_model_key(self.uid, model_name)
        key = '%s_%s' % (self.uid, model_name)
        if key in self._model:
            obj = self._model[key]
        elif model_name in self._register_base:
            mm_proxy = weakref.proxy(self)
            obj = self._register_base[model_name].get(self.uid, self.server, mm=mm_proxy)
            obj.async_save = self.async_save
            obj._model_name = model_name
            setattr(obj, 'mm', mm_proxy)
            self._model[key] = obj
            if hasattr(obj, 'pre_use'):
                obj.pre_use()
        else:
            obj = None

        return obj

    def get_obj_tools(self, model, **kwargs):
        """ 获取model_tools对象

        :param model: 字符串 user, hero
        :return:
        """
        key = self.get_model_key(self.uid, model)
        if key in self._model_tools:
            obj = self._model_tools[key]
        elif model in self._register_base_tools:
            obj = self._register_base_tools[model](self.uid, self.server, **kwargs)
            setattr(obj, 'mm', weakref.proxy(self))
            self._model_tools[key] = obj
        else:
            obj = None

        return obj

    def get_obj_by_id(self, model, iid=''):
        """ 获取models对象, 区别于get_obj, 用于公共的数据, 如公会类

        :param model: 字符串 build
        :param iid: 代表models的key
        :return:
        """
        key = self.get_model_key(iid, model)
        if key in self._model_ids:
            obj = self._model_ids[key]
        elif model in self._register_base_iids:
            mm_proxy = weakref.proxy(self)
            obj = self._register_base_iids[model].get(iid, self.server, mm=mm_proxy)
            setattr(obj, 'mm', mm_proxy)
            if hasattr(obj, 'pre_use'):
                obj.pre_use()
            self._model_ids[key] = obj
        else:
            obj = None

        return obj

    def get_mm(self, uid):
        """ 获取ModelManager对象

        :param uid:
        :return:
        """
        if self.uid == uid:
            return self
        if uid in self._mm:
            mm_obj = self._mm[uid]
        else:
            self._mm[uid] = mm_obj = self.__class__(uid, self.async_save)

        return mm_obj

    def get_event(self, model):
        """ 获取处理函数

        :param model:
        :return:
        """
        if model in self._events:
            obj = self._events[model]
        elif model in self._register_events:
            mm_proxy = weakref.proxy(self)
            obj = self._register_events[model](mm=mm_proxy)
            obj.async_save = self.async_save
            setattr(obj, 'mm', mm_proxy)
            self._events[model] = obj
        else:
            obj = None

        return obj

    def do_save(self, is_save=True):
        """ 保存对象信息, 仅支持self.get_obj中得对象

        :return:
        """
        if not is_save:
            return

        # 事件处理
        for event_obj in self._events.itervalues():
            if event_obj and hasattr(event_obj, 'handler'):
                event_obj.handler()

        for obj in self._model.itervalues():
            if settings.DEBUG:
                print 'ModelManager.do_save', obj._model_key, getattr(obj, 'model_status', 0)
            if obj and getattr(obj, 'model_status', 0) == 1:
                obj._save()

        for mm_obj in self._mm.itervalues():
            mm_obj.do_save(is_save)

    def __getstate__(self):
        state = {}
        for k, v in self.__dict__.iteritems():
            if not isinstance(v, dict):
                state[k] = v
            elif k == '_model':
                state[k] = [(k2, v2._model_name, v2.dumps()) for k2, v2 in v.iteritems()]
        return state

    def __setstate__(self, state):
        uid = state['uid']
        for k, v in state.iteritems():
            if k == '_model':
                self.__dict__['_model'] = {}
                for k1, k2, k3 in v:
                    self.__dict__['_model'][k1] = self._register_base[k2].loads(uid, k3)
            else:
                self.__dict__[k] = v


class EventBase(object):

    def __init__(self, *args, **kwargs):
        self.async_save = False

    def record(self, *args, **kwargs):
        pass

    def handler(self, *args, **kwargs):
        pass
