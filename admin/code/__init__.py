#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from admin import render
from admin.decorators import require_permission
from gconfig import game_config
from gconfig import get_str_words

@require_permission
def code_index(req, codes=[], history=[]):
    """激活激活码页面
    """
    from logics.code import check_time
    from models.code import ActivationCode

    ac = ActivationCode()
    show_code_config = []
    show_code_status = {}

    for code_id, config in game_config.code.iteritems():
        if check_time(config):
            show_code_config.append(code_id)
            all_num = ac.count(code_id)
            non_num = ac.count(code_id, non_use=True)
            one_num = ac.count(code_id, history=True)

            show_code_status[code_id] = {
                                    'all_num': all_num,
                                    'non_num': non_num,
                                    'use_num': all_num - non_num,
                                    'one_num': one_num,
                                    'name': get_str_words('1', config['name'])}

    kwargs = dict(show_code_config=show_code_config,
                  show_code_status=show_code_status,
                  show_codes='\n'.join(codes),
                  history=history)

    render(req, 'admin/code/code.html', **kwargs)

@require_permission
def code_create(req):
    """生成激活码
    """
    from models.code import ActivationCode

    code_id = int(req.get_argument('code_id'))
    num = int(req.get_argument('num'))

    ac = ActivationCode()
    codes = ac.create_code(code_id, num)

    return code_index(req, codes=codes)


def code_show(req):
    """显示部分激活码
    """
    from models.code import ActivationCode

    code_id = int(req.get_argument('code_id'))
    create = req.get_argument('create', '')
    code_non = req.get_argument('code_non', '')
    code_one = req.get_argument('code_one', '')
    ac = ActivationCode()
    if code_non:
        codes = ac.find_keys(code_id, subhistory=create)
    elif code_one:
        codes = ac.find_keys(code_id, history=create)
    else:
        codes = ac.find_keys(code_id, True)

    return code_index(req, codes=list(codes), history=ac.history_count(code_id))


def code_history(req):
    """历史生成激活码记录
    """
    from models.code import ActivationCode

    code_id = int(req.get_argument('code_id'))
    ac = ActivationCode()

    return code_index(req, history=ac.history_count(code_id))
