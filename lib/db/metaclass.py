# coding: utf-8

ATTRIBUTE_NAME = 'FIELDS'
ATTRIBUTE_FETCHER = 'selects'
ATTRIBUTE_LOADERS = 'loaders'
ATTRIBUTE_LOADER = 'load_%s'
IMPORTANT_KEY = 'important'

ATTRIBUTE_BASE_INT = 2

def loader_method(name):
    def wrapper(self, **kwargs):
        self._loads[name] = kwargs

    return wrapper

def loadall(methods):
    def wrapper(self, env):
        for method in methods:
            method(self)

        self.load(env)

    return wrapper

class DynamicModel(type):
    """
    """

    def __new__(cls, name, bases, attrs):
        """
        """

        super_new = super(DynamicModel, cls).__new__

        fields = attrs.pop(ATTRIBUTE_NAME)
        important = set()
        fetchers = {}
        loaders = {}
        methods = []

        for field in fields:
            method = loader_method(field)
            attrs[ATTRIBUTE_LOADER % field] = method
            methods.append(method)

            important.add(field)

        attrs[IMPORTANT_KEY] = important
        attrs[ATTRIBUTE_FETCHER] = fetchers

        return super_new(cls, name, bases, attrs)
