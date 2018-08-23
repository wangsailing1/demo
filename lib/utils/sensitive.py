#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from gconfig import game_config
import settings

# 敏感词

WORDS = getattr(game_config, 'dirtyword_ch', {}).get('dirtyword', [])


def is_sensitive(word):
    """ 是否敏感词

    :param word:
    :return:
    """
    for i, v in enumerate(WORDS):
        if isinstance(word, (str, unicode)):
            if v in word:
                return True
        elif isinstance(word, (list, tuple)):
            for m, n in enumerate(word, 1):
                if v in n:
                    return m

    return False


def replace_sensitive(word):
    """ 替换敏感词

    :param word:
    :return:
    """
    for i, v in enumerate(WORDS):
        if v in word:
            word = word.replace(v, u'**')

    return word
