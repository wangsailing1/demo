#! --*-- encoding:utf8 --*--
from models.chat import Content

class Chat(object):
    USER_QUEUE_DICT = {}
    def __init__(self, mm):
        self.mm = mm
        self.content = Content.get(self.mm.user.account)

    def send_message(self, account, msg):
        """
        发送消息
        :param account:
        :param msg:
        :return:
        """
        self.content.send_msg(account, msg)
        self.content.save()

    def accept_message(self, account, msg):
        """
        接收消息
        :param account:
        :param msg:
        :return:
        """
        self.content.accept_msg(account, msg)
        self.content.save()

    def add_friend_msg(self, account):
        """
        发送好友申请
        :param account:
        :return:
        """
        rc, data = self.content.add_message(account)
        return rc, data

    def agree_add(self, account, bool=True):
        """
        是否同意添加好友
        :param account:
        :param bool:
        :return:
        """
        self.content.agree_add(account, bool)

