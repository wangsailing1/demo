#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'


from logics.mail import MailLogic


def check_unlock(func):
    def wrapper(hm):
        mm = hm.mm
        # if not mm.user.check_build(MAIL_SORT):
        #     return 'error_unlock', {}

        return func(hm)

    return wrapper


@check_unlock
def index(hm):
    """ 邮件首页

    :param hm:
    :return:
    """
    mm = hm.mm

    ml = MailLogic(mm)
    result = ml.index()

    return 0, result


@check_unlock
def receive(hm):
    """ 领取邮件奖励

    :param hm:
    :return:
    """
    mm = hm.mm

    mail_id = hm.get_argument('mail_id')

    ml = MailLogic(mm)
    rc, data = ml.receive(mail_id)
    if rc != 0:
        return rc, data

    return 0, data


@check_unlock
def read(hm):
    """
    读取邮件
    :param hm:
    :return:
    """
    mm = hm.mm

    mail_id = hm.get_argument('mail_id')

    ml = MailLogic(mm)
    rc, data = ml.read(mail_id)
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def send(hm):
    """
    发送邮件
    :param hm:
    :return:
    """
    mm = hm.mm

    uid = hm.get_argument('uid')
    content = hm.get_argument('content')
    sort = hm.get_argument('sort', is_int=True)

    if not uid or not content or not sort:
        return 'error_100', {}

    ml = MailLogic(mm)
    rc, data = ml.send(uid, content, sort)
    if rc != 0:
        return rc, {}

    return 0, data


# def receive_all_mail(hm):
#     """ 领取所有邮件
#
#     :param hm:
#     :return:
#     """
#     mm = hm.mm
#
#     ml = MailLogic(mm)
#     rc, data = ml.receive_all_mail()
#     if rc != 0:
#         return rc, data
#
#     return 0, data


@check_unlock
def receive_all(hm):
    """
    一键领取
    :param hm:
    :return:
    """
    mm = hm.mm

    ml = MailLogic(mm)
    rc, data = ml.receive_all()
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def delete_all(hm):
    """
    发送邮件
    :param hm:
    :return:
    """
    mm = hm.mm

    ml = MailLogic(mm)
    rc, data = ml.delete_all_read_mail()
    if rc != 0:
        return rc, {}

    return 0, data


@check_unlock
def delete_mail(hm):
    """
    发送邮件
    :param hm:
    :return:
    """
    mm = hm.mm
    mail_id = hm.get_argument('mail_id', '')

    ml = MailLogic(mm)
    rc, data = ml.delete_mail(mail_id)
    if rc != 0:
        return rc, {}

    return 0, data
