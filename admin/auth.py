#! --*-- coding: utf-8 --*--

__author__ = 'sm'


from hashlib import md5

import urllib
import time
import datetime

import settings

from admin.admin_models import Admin


def build_auth_signature(auth_fields):
    """生成auth签名"""
    payload = "&".join(k + "=" + str(auth_fields[k]) for k in sorted(auth_fields.keys()) if k != "auth_fields")

    return md5(payload).hexdigest()


def set_cookie(request, admin):
    """ 登录后设置cookie

    :param request:
    :param admin:
    :return:
    """
    login_time = datetime.datetime.now()
    login_ip = request.request.headers.get('X-Real-Ip', '')
    admin.set_last_login(login_time, login_ip)

    username = admin.username

    last_login_stamp = time.mktime(admin.last_login.timetuple())
    token = build_auth_signature({
        "username": username,
        "last_login": last_login_stamp,
        "secret_key": settings.admin_secret_key,
    })
    cv = "%s|%s|%s" % (username, last_login_stamp, token)
    cv = urllib.quote(cv.encode("ascii"))
    admin.save()
    request.set_cookie(settings.admin_cookie, cv)


def get_admin_by_request(request):
    """ 根据请求的cookie获取admin

    :param request:
    :return:
    """
    cv = request.get_cookie(settings.admin_cookie)
    # print cv, type(cv)
    if cv is None:
        return None
    else:
        cv = urllib.unquote(cv).decode("ascii")
        mid, login_stamp, token = cv.split('|')

        admin = Admin.get(mid)
        if admin is None:
            return None

        raw_last_login_stamp = time.mktime(admin.last_login.timetuple())
        new_token = build_auth_signature({
            "username": mid,
            "last_login": raw_last_login_stamp,
            "secret_key": settings.admin_secret_key,
        })
        if new_token == token:
            return admin
        return None


def logout(request):
    """ 登出后删除cookie

    :param request:
    :return:
    """
    request.clear_cookie(settings.admin_cookie)


# 初始化（或更新）某管理员账号
# 这个函数，也要被初始化脚本替代掉
def make_super_user(username, password):
    """
    给定用户名和密码直接创建管理用户 ,参数都是字符串类型
    """
    admin = Admin.get(username)
    if admin:
        if not admin.is_super:
            admin.is_super = True
            admin.save()

        return

    admin = Admin()

    admin.username = username
    admin.password = password
    admin.email = username + '@kaiqigu.com'
    admin.is_super = True

    admin.save()

    return admin

for username, password in settings.DEFAULT_BACKEND_ADMIN:
    make_super_user(username, password)
