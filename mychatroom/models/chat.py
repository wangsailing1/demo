#! --*-- encoding:utf8 --*--
from models import ModelBase
from logics import ModelManager
import websocket
from models.user import  UserData
class Content(ModelBase):
    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'friends':{},
            'messages':[],
            'blacklist':[],
            'add_applications':[],
        }
        super(Content, self).__init__(self.uid)

    def add_friend(self, account):
        if account not in self.messages:
            return 1, {'msg':'没有该好友申请'}
        del self.messages[self.messages.index(account)]
        user = UserData.get(account)
        self.friends[account] = {'msg':[],'new_msg':[], 'name':user.name,  'account':account}
        self.save()

    # def add_aplication(self, account, is_agree=False):
    #     if not is_agree:
    #         return 2, {'msg':account+"拒绝添加您为好友"}
    #     if account in self.add_aplications:
    #         self.friends[account] = {'msg':[],'new_msg':[]}
    #         self.save()
    #         return 1, {'msg':account+"已同意添加您为好友"}
    #     self.add_aplications.append(account)
    #     return 0, {"msg":"已经向"+account+"发起好友申请"}

    def add_message(self, account):
        if account in self.messages:
            return 1, {'msg':'对方还没处理请稍等'}
        self.messages.append(account)
        self.save()
        return 0,{}

    def agree_add(self, account, is_agree=True):
        if is_agree:
            self.add_friend(account)
            self.add_applications.append("账号为"+account+'同意了你的好友申请')
        else:
            self.add_applications.append("账号为"+account+'拒绝了你的好友申请')
    def send_msg(self, account, msg):
        acc = self.friends[account]
        if not acc:
            return 1, {'msg':"你没有添加该好友"}
        acc['msg'].append(msg)

    def accept_msg(self, account, msg):
        acc = self.friends[account]
        acc['msg'].append(msg)
        acc['new_msg'].append(msg)

class MyWebSocketHandler(websocket.WebSocket):
    connect_user = dict()

    def __init__(self, account):
        self.account = account
        if self.account in self.connect_user:
            self = self.connect_user[self.account]

    def open(self, account):
        self.connect_user[account] = self

    def on_message(self, account,message):
        print account,'发来的消息', message

    def on_close(self, account):
        del self.connect_user[account]

    def check_origin(self, origin):
        return True

    @classmethod
    def send_demand_updates(cls, account, message):
        print cls.connect_user
        for i,v in cls.connect_user.iteritems():
            if i == account:
                v.write_message(message)

ModelManager.register_model('myweb', MyWebSocketHandler)
ModelManager.register_model('content', Content)
