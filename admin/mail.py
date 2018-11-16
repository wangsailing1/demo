#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config
from gconfig import check


@require_permission
def select(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'mail': [], 'msg': '', 'uid': uid}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['mail'] = mm.mail.mail
        result['mm'] = mm

    return render(req, 'admin/mail/index.html', **result)


@require_permission
def mail_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')
    mail_id = req.get_argument('mail_id')

    if modify:
        pass
    elif delete:
        mm.mail.remove_mail(mail_id)
    else:
        return select(req, **{'msg': 'fail'})

    return select(req, **{'msg': 'success'})


@require_permission
def add_mail(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    result = {'msg': '', 'uids': '', 'content': '', 'gifts': [], 'title': ''}

    if req.request.method == 'POST':
        uids = req.get_argument('uids', '')
        if not uids:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/mail/add_mail.html', **result)

        str_uids = uids.replace('\r', '')
        o_uids = str_uids.split("\n")

        uids = set(o_uids)

        user_not_exist = []
        success_uids = []

        title = req.get_argument('title', '')
        content = req.get_argument('content', '')
        gifts = eval(req.get_argument('gifts', ''))
        result['title'] = title
        result['content'] = content
        result['gifts'] = gifts
        result['uids'] = str_uids

        check_msg = check.check_reward()(gifts)
        if check_msg:
            result['msg'] = check_msg
        else:
            mail_dict = None

            if len(uids) > 100:
                result['msg'] = u'一次发送的 UID 数不能大于 100'
            else:
                for uid in uids:
                    if not uid:
                        continue

                    mm = ModelManager(uid)

                    if mm.user.inited:
                        user_not_exist.append(uid)
                        continue

                    if mail_dict is None:
                        mail_dict = mm.mail.generate_mail(content, title=title, gift=gifts)

                    mm.mail.add_mail(mail_dict)
                    success_uids.append(uid)

                result['msg'] = 'success uids: %s, fail uids: %s' % (success_uids, user_not_exist)

    return render(req, 'admin/mail/add_mail.html', **result)
