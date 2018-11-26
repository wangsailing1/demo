#! --*-- coding: utf-8 --*--

__author__ = 'sm'


from admin import render
from lib.utils.debug import print_log
from models.questionnaire import Questionnaire


def select(req, **kwargs):
    """

    :param req:
    :return:
    """
    if 'msg' not in kwargs:
        kwargs['msg'] = ''

    return render(req, 'admin/questionnaire/index.html', **kwargs)


def commit(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    data = {}
    for i in xrange(1, 25):
        key = 's%s' % i
        if i == 24:
            value = req.get_arguments(key)
            value = ','.join(value)
        else:
            value = req.get_argument(key, '')
        data[key] = value

    questionnaire = Questionnaire()
    questionnaire.insert_quest(data)

    kwargs['msg'] = 'commit success'

    return select(req, **kwargs)


def find(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    questionnaire = Questionnaire()

    quest = [q for q in questionnaire.find('1', '1')]

    result = {
        'quest': quest,
    }

    return render(req, 'admin/questionnaire/find.html', **result)
