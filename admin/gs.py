#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import datetime

import settings
from admin.decorators import require_permission
from admin import render
from admin.admin_models import Admin
from admin import admin_config
from admin import auth
from admin.admin_config import menu_config, menu_name
from models.user import GSMessage
from lib.utils.debug import print_log
from lib.core.environ import ModelManager


def login(req):
    """ 登录

    :param req:
    :return:
    """
    msgs = []
    d = {'msgs': msgs}
    if req.request.method == 'POST':
        username = req.get_argument('username', '')
        password = req.get_argument('password', '')
        if not username or not password:
            msgs.append(u'用户名或密码错误')
            return render(req, 'admin/gs/login.html', **d)

        admin = Admin.get(username)
        if not admin:
            msgs.append(u'密码错误')
            return render(req, 'admin/gs/login.html', **d)
        elif not admin.check_password(password):
            msgs.append(u'密码错误')
            return render(req, 'admin/gs/login.html', **d)
        elif admin.disable:
            msgs.append(u'该用户已被禁用')
            return render(req, 'admin/gs/login.html', **d)
        auth.set_cookie(req, admin)
        return req.redirect('/%s/admin/index/' % settings.URL_PARTITION)
    return render(req, 'admin/gs/login.html', **d)


@require_permission
def logout(req):
    """ 退出

    :param req:
    :return:
    """
    auth.logout(req)
    return req.redirect('/%s/admin/index/' % settings.URL_PARTITION)


@require_permission
def select(req, **kwargs):
    """ 首页

    :param req:
    :return:
    """
    result = {'msg': ''}
    result.update(kwargs)
    all_user = Admin.get_all_user()
    result['all_user'] = all_user
    return render(req, 'admin/gs/select.html', **result)


@require_permission
def change_password(req):
    d = {'msg': ''}
    if req.request.method == 'GET':
        return render(req, 'admin/gs/change_password.html', **d)
    else:
        old = req.get_argument('old_password', 'old_password').strip()
        pwd1 = req.get_argument('password1', 'password1').strip()
        pwd2 = req.get_argument('password2', 'password2').strip()

        if not (pwd1 and pwd2):
            d['msg'] = u'密码不能为空'
        elif pwd1 != pwd2:
            d['msg'] = u'两次输入密码不同'
        else:
            admin = auth.get_admin_by_request(req)
            if admin:
                if not admin.check_password(old):
                    d['msg'] = u'原始密码错误'
                else:
                    d['msg'] = u'success'
                    admin.set_password(pwd1)
                    admin.save()
            else:
                d['msg'] = u'username not exist'

        return render(req, 'admin/gs/change_password.html', **d)


@require_permission
def gs_admin(req, **kwargs):
    """ 查看一个账号信息

    :param req:
    :return:
    """
    username = req.get_argument('username', '')
    admin = Admin.get(username)
    if not admin:
        return select(req, msg=u'账号不存在')

    permissions = admin.permissions
    result = {
        'msg': '',
        'username': admin.username,
        'permissions': permissions,
        'menu_name': menu_name,
        'menu_config': menu_config,
    }
    result.update(kwargs)
    return render(req, 'admin/gs/gs_admin.html', **result)



@require_permission
def add_admin(req):
    """
     新建管理员
    """
    result = {
        'msg': '',
        'menu_name': menu_name,
        'menu_config': menu_config,
    }

    if req.request.method == "POST":
        username = req.get_argument("username", '').strip()
        password = req.get_argument("password", '').strip()
        password1 = req.get_argument("password1", '').strip()
        email = req.get_argument("email", '').strip()

        admin = Admin.get(username)
        if admin:
            req.write(u'帐号已存在')
        elif password != password1:
            req.write(u'两次密码输入不同')
        else:
            permissions = req.get_argument("permissions", '').strip()
            permissions_dict = {}
            if permissions:
                permissions_list = [i.split('=') for i in permissions.split('&') if i]
                for k, v in permissions_list:
                    if k not in permissions_dict:
                        permissions_dict[k] = []
                    permissions_dict[k].append(v)

            admin = Admin()
            admin.username = username
            admin.set_password(password)
            admin.email = email
            admin.last_login = datetime.datetime.now()

            admin.permissions = permissions_dict
            # 这步是存储了
            admin.save()
            req.write(u'添加成功')
    else:
        return render(req, "admin/gs/add_admin.html", **result)


@require_permission
def modify_admin(req):
    """修改管理员权限"""
    if req.request.method == "POST":
        username = req.get_argument("username", '').strip()
        permissions = req.get_argument("permissions", '').strip()
        permissions_dict = {}
        if permissions:
            permissions_list = [i.split('=') for i in permissions.split('&') if i]
            for k, v in permissions_list:
                if k not in permissions_dict:
                    permissions_dict[k] = []
                permissions_dict[k].append(v)

        admin = Admin.get(username)
        if not admin:
            req.write(u'username not exist')
        else:
            admin.permissions = permissions_dict
            admin.save()
            req.write(u'success')


@require_permission
def delete_admin(req):
    """删除管理员"""
    username = req.get_argument("username", '').strip()

    admin = Admin.get(username)
    if not admin:
        return select(req, msg='admin not exist')
    else:
        admin.delete()
        return select(req, msg='success')


def game_service(req):
    """
    客服回复首页
    """
    page = int(req.get_argument('page', 0))
    user_id = req.get_argument('user_id', '')
    gs_name = req.get_argument('gs_name', '')
    status = req.get_argument('status', '2')
    solve_status = req.get_argument('solve_status', '2')
    gs_message = GSMessage()
    close_qid = req.get_argument('close_qid', '')
    is_desc = 1
    if close_qid:
        gs_message.delete_question(close_qid)

    query_dict = {}
    if user_id:
        query_dict['user_id'] = "'"+user_id+"'"
    if gs_name:
        query_dict['gs_name'] = "'"+gs_name+"'"
    if status in ('0', '1'):
        query_dict['status'] = int(status)
    if solve_status in ('0', '1'):
        query_dict['solve_status'] = int(solve_status)
    query_result = gs_message.select_msg(query_dict, page, is_desc)
    if query_result:
        gs_data = query_result
    else:
        gs_data = []
    # print_log('-----1111---', status, solve_status)
    return render(req,
                  'admin/gs/game_service.html',
                  gs_data=gs_data,
                  page=page,
                  user_id=user_id,
                  gs_name=gs_name,
                  status=status,
                  solve_status=solve_status,
                  )


@require_permission
def send_gs_notify(req):
    """
    客服回复页
    :param req:
    :return:
    """
    msg = ''
    gifts = []
    send_flag = False
    ques_id = req.get_argument('ques_id')
    if req.request.method == 'POST':
        reply_title = req.get_argument('reply_title')
        reply_content = req.get_argument('reply_content')
        solve_status = req.get_argument('solve_status', 0)
        uid = req.get_argument('uid')
        mm = ModelManager(uid)
        mail_dict = mm.mail.generate_mail(
            reply_content,
            title=reply_title,
            gift=[] if gifts is None else gifts,
        )
        mm.mail.add_mail(mail_dict)
        send_flag = True

        # 保存回复数据
        gs_name = auth.get_admin_by_request(req)
        data = {
            'solve_status': 1 if solve_status else 0,
        }
        if gs_name:
            data['gs_name'] = "'"+gs_name.username+"'"
        if reply_title:
            data['reply_title'] = "'"+reply_title+"'"
        if reply_content:
            data['reply_content'] = "'"+reply_content+"'"

        gs_message = GSMessage()
        gs_message.update_one_msg(ques_id, data)

    gs_data = query_one_gs_message(ques_id)
    return render(req, 'admin/gs/send_gs_notify.html', **{
            'msg': msg,
            'gifts': gifts,
            'send_flag':  send_flag,
            'gs_data': gs_data,
        })


def query_one_gs_message(ques_id):
    """
    查询一条消息
    :param ques_id:
    :return:
    """
    gs_data = {
        'ques_id': ques_id,
        'uid': '',
        'name': '',
        'vip_level': 0,
        'coin': 0,
        'food': 0,
        'msg': '',
        'reply_title': '',
        'reply_content': '',
        'solve_status': '',
    }
    gs_message = GSMessage()
    query_result = gs_message.select_one_msg(ques_id)
    if query_result:
        gs_data['uid'] = query_result[1]
        try:
            mm = ModelManager(gs_data['uid'])
            user = mm.user
            gs_data['name'] = user.name
            gs_data['coin'] = user.diamond
            gs_data['food'] = user.silver
        except:
            print_log('uid error', )

        gs_data['vip_level'] = query_result[2]
        gs_data['msg'] = query_result[5] if query_result[5] else ''
        gs_data['reply_title'] = query_result[8] if query_result[8] else ''
        gs_data['reply_content'] = query_result[11] if query_result[11] else ''
        gs_data['solve_status'] = 'checked=checked' if query_result[13] else ''
    return gs_data
