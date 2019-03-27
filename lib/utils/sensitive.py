#! --*-- coding: utf-8 --*--

__author__ = 'sm'

try:
    import jieba
except:
    jieba = None

import urllib
from gconfig import game_config
from lib.utils.encoding import force_str, force_unicode


# 敏感词

LANMAPPING = {'0': 'tw', '1': 'ch', 0: 'tw', 1: 'ch'}


# WORDS = getattr(game_config, 'dirtyword_ch', {})


def is_sensitive(word, lan):
    """ 是否敏感词

    :param word:
    :return:
    """
    # 处理下前端url encode编码的字符串
    word = force_unicode(urllib.unquote(force_str(word)))

    str_or_unicode = isinstance(word, (str, unicode))
    tp = 'dirtyword_%s' % LANMAPPING[lan]
    WORDS = getattr(game_config, tp, {})
    if str_or_unicode:
        word = word.replace(' ', '')
    for v in WORDS:
        if str_or_unicode:
            if v and v in word:
                return True
        elif isinstance(word, (list, tuple)):
            for m, n in enumerate(word, 1):
                if v in n:
                    return m

    return False


def replace_sensitive(word, lan, use_jieba=True):
    """ 替换敏感词

    :param word:
    :return:
    """
    tp = 'dirtyword_%s' % LANMAPPING[lan]
    WORDS = getattr(game_config, tp, {})
    if jieba and use_jieba:
        d = []
        for i in jieba.cut(word):
            d.append('**' if i in WORDS else i)
        return ''.join(d)

    for v in WORDS:
        if v and v in word:
            word = word.replace(v, u'**')

    return word
