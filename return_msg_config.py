#! --*-- coding: utf-8 --*--

__author__ = 'sm'


import settings
from lib.utils.encoding import force_unicode

MUITL_LAN = {'0': 'tw', '1': 'ch'}

module_name = "return_msg_" + settings.LANG

module = __import__('lang_config.%s' % module_name, globals(), locals(), ["return_msg_config", "i18n"])
return_msg_config = getattr(module, "return_msg_config")
i18n = getattr(module, "i18n")


class I18nMsg(object):
    def __init__(self, i18n):
        self.i18n = i18n

    def __call__(self, flag, *args, **kwargs):
        msg = self.i18n.get(flag)
        if not msg:
            return u''

        return force_unicode(msg)

    def __getitem__(self, item):
        msg = self.i18n.get(item)
        if not msg:
            return u''

        return force_unicode(msg)

    def get(self, item, lan_sort):
        if lan_sort in MUITL_LAN:
            lan = MUITL_LAN[lan_sort]
        else:
            lan = MUITL_LAN['0']
        module_name = "return_msg_" + lan
        module = __import__('lang_config.%s' % module_name, globals(), locals(), ["i18n"])
        i18n = getattr(module, "i18n")
        msg = i18n.get(item)
        if not msg:
            return u''

        return force_unicode(msg)


def get_msg_str(lan_sort):
    """

    :param msg_sort: 0: return_msg_config,1: i18n_msg
    :param lan_sort:
    :return:
    """
    if lan_sort in MUITL_LAN:
        lan = MUITL_LAN[lan_sort]
    else:
        lan = MUITL_LAN['0']
    module_name = "return_msg_" + lan
    module = __import__('lang_config.%s' % module_name, globals(), locals(), ["return_msg_config"])
    return_msg_config = getattr(module, "return_msg_config")
    return return_msg_config


def get_error_14_msg(lan, lv):
    """
    获取级别不足的全局提示信息
    :param lan: 语言 sort
    :param lv: 需要的等级
    :return:
    """
    msg = get_msg_str(lan).get('error_14', '%s') % lv
    return msg

i18n_msg = I18nMsg(i18n)
