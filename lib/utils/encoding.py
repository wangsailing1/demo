#! --*-- coding: utf-8 --*--

__author__ = 'sm'


def force_str(text, encoding="utf-8", errors='strict'):
    t_type = type(text)
    if t_type == str:
        return text
    elif t_type == unicode:
        return text.encode(encoding, errors)
    return str(text)


def force_unicode(text, encoding="utf-8", errors='strict'):
    t_type = type(text)
    if t_type == unicode:
        return text
    elif t_type == str:
        return text.decode(encoding, errors)
    elif hasattr(text, '__unicode__'):
        return unicode(text)
    return unicode(str(text), encoding, errors)
