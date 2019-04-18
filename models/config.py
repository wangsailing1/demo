#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import re
import time

import settings
from lib.sdk_platform.helper import http
from lib.utils import md5, config_md5
from lib.db import ModelBase, ModelTools
from lib.db import get_redis_client


class ConfigRefresh(object):
    FLAG_KEY = 'config_refresh_key'
    TEXT_KEY = 'config_refresh_text_key'
    CLIENT = get_redis_client(settings.SERVERS['master']['redis'])

    @classmethod
    def set_updated(cls):
        cls.CLIENT.delete(cls.FLAG_KEY)

    @classmethod
    def refresh(cls, flag, msg):
        if flag:
            cls.CLIENT.set(cls.FLAG_KEY, 1)
        else:
            cls.CLIENT.delete(cls.FLAG_KEY)
        cls.CLIENT.set(cls.TEXT_KEY, msg)

    @classmethod
    def check(cls):
        from gconfig import front_game_config

        refresh_flag = cls.CLIENT.get(cls.FLAG_KEY)
        all_config_version = front_game_config.ver_md5
        refresh_msg = cls.CLIENT.get(cls.TEXT_KEY) or ''
        refresh_msg = refresh_msg.decode('utf-8')

        return refresh_flag or 0, all_config_version, refresh_msg

class ConfigMd5(ModelBase):
    """

    :var ver_md5: 所有配置版本号生成的MD5
    """
    SERVER_NAME = 'master'

    def __init__(self, uid=None):
        self.uid = 'config_md5'
        self._attrs = {
            'ver_md5': '',
        }
        super(ConfigMd5, self).__init__(self.uid)

    @classmethod
    def get(cls, **kwargs):
        return super(ConfigMd5, cls).get('config_md5', cls.SERVER_NAME, **kwargs)

    @classmethod
    def generate_md5(cls, versions):
        """ 根据配置版本号生成md5

        :param versions:
        :return:
        """
        versions_sort = sorted(versions.iteritems(), key=lambda x: x[0])
        return md5(versions_sort)

    def update_md5(self, versions, gen_md5=None, save=False):
        """ 更新MD5

        :return:
        """
        self.ver_md5 = gen_md5 or self.generate_md5(versions)

        if save:
            self.save()

    def generate_custom_md5(self, data):
        """ 生成自定义MD5, 用于自定义数据, data中支持复杂类型 dict, set, list, tuple

        :param data:
        :return:
        """
        if not isinstance(data, (dict, set, list, tuple)):
            return md5(data)
        else:
            return config_md5(repr(data))


class ConfigVersion(ModelBase):
    """ 配置版本号

    """
    SERVER_NAME = 'master'

    def __init__(self, uid=None):
        self.uid = 'config_version'
        self._attrs = {
            'versions': {},
        }
        super(ConfigVersion, self).__init__(self.uid)

    @classmethod
    def get(cls, **kwargs):
        return super(ConfigVersion, cls).get('config_version', cls.SERVER_NAME, **kwargs)

    def update_version(self, config_name, hex_version, save=False):
        """ 更新配置版本号

        """
        self.versions[config_name] = hex_version

        if save:
            self.save()


class Config(ModelBase):
    """

    """
    SERVER_NAME = 'master'

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'value': {},
            'version': '',
            'last_update_time': '',
        }
        super(Config, self).__init__(self.uid)

    def update_config(self, value, version, save=False):
        """ 更新配置

        :param value:
        :param version:
        :param save:
        :return:
        """
        self.value = value
        self.version = version
        self.last_update_time = time.strftime('%F %T')

        if save:
            self.save()


class FrontConfigMd5(ConfigMd5):
    """ 前端ConfigMd5

    """
    def __init__(self, uid=None):
        super(FrontConfigMd5, self).__init__(uid)


class FrontConfigVersion(ConfigVersion):
    """ 前端ConfigVersion

    """
    def __init__(self, uid=None):
        super(FrontConfigVersion, self).__init__(uid)


class FrontConfig(Config):
    """ 前端config

    """
    def __init__(self, uid=None):
        super(FrontConfig, self).__init__(uid)


class ChangeTime(ModelTools):
    SERVER_NAME = 'master'

    @classmethod
    def get(cls):
        client = cls.get_redis_client(cls.SERVER_NAME)
        key = cls.make_key_cls('changetime', cls.SERVER_NAME)
        return client.get(key)

    @classmethod
    def set(cls, value):
        client = cls.get_redis_client(cls.SERVER_NAME)
        key = cls.make_key_cls('changetime', cls.SERVER_NAME)
        client.set(key, value)


class ResourceVersion(ModelBase):
    SERVER_NAME = 'master'
    KEY = 'resource_version'

    def __init__(self, uid=''):
        self.uid = self.KEY
        self._attrs = {
            'hot_update_switch': 0,     # 是否屏蔽前端热更开关
            'can_hot_update_ip': '',    # 灰度热更白名单
            'limit_version': '',        # 版本限制
            'recent_version': '',       # 最新版本号
        }
        super(ResourceVersion, self).__init__(self.uid)

    @classmethod
    def get(cls, uid='', server_name='', **kwargs):
        o = super(ResourceVersion, cls).get(cls.KEY, server_name=cls.SERVER_NAME, **kwargs)
        return o

    def set_switch(self, flag, is_save=False):
        """
        设置是否屏蔽前端热更开关
        :param flag:
        :param is_save:
        :return:
        """
        if flag > 0:
            self.hot_update_switch = 1
        else:
            self.hot_update_switch = 0

        if is_save:
            self.save()

    def set_update_ip(self, update_ip, is_save=False):
        """
        设置灰度热更白名单
        :param update_ip: ['127.0.0.1']
        :param is_save:
        :return:
        """
        self.can_hot_update_ip = update_ip

        if is_save:
            self.save()

    def get_can_hot_update_ip(self):
        """
        灰度热更白名单
        :return:
        """
        if self.can_hot_update_ip:
            # return [i.strip() for i in self.can_hot_update_ip.split(',')]
            return re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self.can_hot_update_ip)
        else:
            return []

    def set_limit_version(self, limit_version, is_save=False):
        """
        设置版本限制
        """
        self.limit_version = limit_version

        if is_save:
            self.save()

    def set_recent_version(self, recent_version, is_save=False):
        """
        设置最新版本号
        """
        self.recent_version = recent_version

        if is_save:
            self.save()
