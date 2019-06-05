#! --*-- encoding: utf-8 --*--
from models import ModelBase
from logics import ModelManager
import random
import time
from models import md5
class UserData(ModelBase):
    ACCOUNT = {}
    RANDOM_ACCOUNT = (1,2,3,4,5,6,7,8,9,0)
    def __init__(self, account):
        self.account = account
        self._attrs = {
            'name':'',
            'password':'',
            'reg_time':time.strftime('%F %H:%M:%S', time.localtime()),
            'uid':self.set_uid(),
            'online':False,
        }

        super(UserData, self).__init__(self.account)

    def resetpwd(self, oldpwd, newpwd):
        if md5(oldpwd) == self.password:
            self.password = md5(newpwd)
            self.save()
            return 0,{'msg':"修改成功"}
        return 1,{'msg':'密码输入错误'}

    def set_uid(self):
        while True:
            s = ''
            if self.account in self.ACCOUNT:
                return self.ACCOUNT[self.account]
            for i in self.RANDOM_ACCOUNT:
                s += str(random.choice(self.RANDOM_ACCOUNT))
            if s not in self.ACCOUNT.values():
                self.ACCOUNT[self.account] = s
                return s[1:]
            continue

    def check_pwd(self, pwd):
        return self.password == md5(pwd)

    def set_pwd(self, pwd):
        self.password = md5(pwd)

    def rename(self, newname):
        self.name = newname
        self.save()

    def login(self):
        self.online = True
        self.save()

    def logout(self):
        self.online = False
        self.save()

    def savedata(self, data):
        self.redis.set(self.uid, data)

ModelManager.register_model('user', UserData)

