#! --*-- encoding:utf8 --*--
from models.user import UserData, md5
from logics import ModelManager
def register_user(hm):
    account = hm.get_argument('account', '')
    password = hm.get_argument('password', '')
    name = hm.get_argument('name', '')
    if not password:
        return 1, {'msg':'密码不允许为空'}    # 密码有误
    user = UserData.get(account)
    if not user.inited:
        return 2, {'msg':'账号已存在'}    # 账号已存在
    user.set_pwd(password)
    user.rename(name)
    mm = ModelManager(user.uid)
    mm.user = user
    user.save()
    mm.do_save()
    hm.mm = user
    return 0,{'msg':'注册成功'}
def reset_pwd(hm):
    old_pwd = hm.get_argument('old_pwd', '')
    new_pwd = hm.get_argument('new_pwd', '')
    account = hm.get_argument('account', '')
    if account.inited:
        return 2, {'msg':'用户不存在'}
    if not old_pwd or not new_pwd:
        return 1, {'msg':'新密码、旧密码都不允许为空'}    # 新密码、旧密码都不允许为空
    user = UserData.get(account)
    rc,data = user.resetpwd(old_pwd, new_pwd)
    return rc, data

def reset_name(hm):
    account = hm.get_argument('account', '')
    if account.inited:
        return 2, {'msg':'用户不存在'}
    new_name = hm.get_argument('new_name', '')
    if not new_name:
        return 1, {'msg':'请输入正确的名称'}
    user = UserData.get(account)
    rc, data = user.rename(new_name)
    return rc, data

def login(hm):
    mm = hm.mm
    account = hm.get_argument('account', '')
    password = hm.get_argument('password', '')
    user = UserData.get(account)
    if user.inited:
        return 1, {'msg':'账号不存在'}
    if not user.check_pwd(password):
        return 2, {'msg':'密码不正确'}
    if user.online:
        return 3, {'msg':'账号已经在登陆状态'}
    user.online = True
    user.save()
    hm.req.set_secure_cookie('account', account)
    return 0, {'msg': '登陆成功'}

def index(hm):
    account = hm.req.get_current_user()
    user = UserData.get(account)
    if not user.inited:
        return 0, {'msg':'已经登陆', 'name':user.name, 'uid':user.account}
    return 1,{'msg':'没有登陆'}

def logout(hm):
    mm = hm.mm
    user = UserData.get(mm.user.account)
    if not user.online:
        return 1,{'msg':'当前没在登陆状态'}
    user.online = False
    user.save()
    hm.req.clear_cookie('account')
    return 0, {'msg':"退出成功"}

