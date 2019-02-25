#! --*-- coding: utf-8 --*--

__author__ = 'sm'

try:
    import jieba
except:
    jieba = None

from gconfig import game_config
import settings

# 敏感词

WORDS = getattr(game_config, 'dirtyword_ch', {})


def is_sensitive(word):
    """ 是否敏感词

    :param word:
    :return:
    """
    str_or_unicode = isinstance(word, (str, unicode))
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


def replace_sensitive(word, use_jieba=True):
    """ 替换敏感词

    :param word:
    :return:
    """
    if jieba and use_jieba:
        d = []
        for i in jieba.cut(word):
            d.append('**' if i in WORDS else i)
        return ''.join(d)

    for v in WORDS:
        if v in word:
            word = word.replace(v, u'**')

    return word
