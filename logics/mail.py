#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import copy

from tools.gift import add_mult_gift
from return_msg_config import i18n_msg
from lib.utils.sensitive import is_sensitive


class MailLogic(object):

    def __init__(self, mm):
        self.mm = mm
        self.mail = self.mm.mail

    def index(self):
        """ 邮件首页

        :return:
        """
        result = {
            'mail': self.mail.mail,
        }

        return result

    def receive(self, mail_id):
        """ 领取邮件奖励

        :param mail_id:
        :return:
        """
        mail_dict = self.mail.mail.get(mail_id)
        if not mail_dict:
            return 1, {}    # 没有该邮件

        gift = mail_dict['gift']
        if not gift:
            return 2, {}    # 没有奖励可领取

        if self.mail.get_mail_status(mail_id) == 2:
            return 3, {}    # 邮件已领取
        stats = self.mm.item.check_item_enough(gift)
        if stats:
            return stats, {}
        reward = add_mult_gift(self.mm, gift)

        self.mail.set_mail_status(mail_id, status=2)

        self.mail.save()

        result = {
            'reward': reward,
            'mail': {mail_id: mail_dict},
        }

        return 0, result

    def read(self, mail_id):
        """
        读取邮件
        :param mail_id:
        :return:
        """
        mail_dict = self.mail.mail.get(mail_id)
        if not mail_dict:
            return 1, {}    # 没有该邮件

        if self.mail.get_mail_status(mail_id) >= 1:
            return 0, {}    # 邮件已读取

        self.mail.set_mail_status(mail_id, status=1)
        mail_dict['read_time'] = int(time.time())

        self.mail.save()

        return 0, {
            'mail': {mail_id: mail_dict},
        }

    def receive_all_mail(self):
        """ 领取所有邮件

        :return:
        """
        remove_mail_ids = []

        reward = {}
        for mail_id, mail_dict in self.mail.mail.iteritems():
            if self.mail.get_mail_status(mail_id) == 2:
                continue  # 邮件已领取
            gift = mail_dict['gift']
            if gift:
                remove_mail_ids.append(mail_id)
                add_mult_gift(self.mm, gift, cur_data=reward)

        for mail_id in remove_mail_ids:
            self.mail.remove_mail(mail_id, save=False)

        self.mail.save()

        result = {
            'reward': reward,
        }

        return 0, result

    def send(self, uid, content, sort):
        """
        发送邮件
        :param uid:
        :param content: 邮件内容
        :param sort: 1: 好友邮件, 2: 公会邮件
        :return:
        """
        if is_sensitive(content):
            return 1, {}    # 内容不合法

        if sort == 1:
            if not self.mm.friend.has_friend(uid):
                return 2, {}    # 没有该好友
            target_mm = self.mm.get_mm(uid)
            title = i18n_msg.get('friend', self.mm.user.language_sort) % self.mm.uid
            mail_sort = self.mail.SORT_FRIEND

        elif sort == 2:
            target_mm = self.mm.get_mm(uid)
            if not target_mm.guild_id:
                return 3, {}    # 该玩家没有公会
            title = i18n_msg.get('guild', self.mm.user.language_sort)
            mail_sort = self.mail.SORT_GUILD
        else:
            return 4, {}    # 不能发送该邮件

        mail_dict = target_mm.mail.generate_mail(content, title=title, sort=mail_sort)
        target_mm.mail.add_mail(mail_dict)

        return 0, {}

    def receive_all(self):
        """
        邮件一键领取
        :return:
        """
        reward = {}
        if not self.mail.mail:
            return 1, {}        # 没有邮件
        mail_dict = copy.deepcopy(self.mail.mail)
        reward_config = []
        for k, v in mail_dict.iteritems():
            if self.mail.get_mail_status(k) == 2:
                continue  # 邮件已领取
            stats = self.mm.item.check_item_enough(v['gift'])
            if stats:
                continue
            reward_config += v['gift']
            self.mail.mail[k]['gift'] = []
            self.mail.set_mail_status(k, status=2)
            self.mail.mail[k]['read_time'] = int(time.time())
        add_mult_gift(self.mm, reward_config, reward)
        self.mail.save()
        return 0, {
                'mail': self.mail.mail,
                'reward': reward,
            }

    def delete_all(self):
        """
        邮件一键删除
        :return:
        """
        reward = {}
        if not self.mail.mail:
            return 1, {}        # 没有邮件
        have_readed = False
        mail_dict = copy.deepcopy(self.mail.mail)
        reward_config = []
        for k, v in mail_dict.iteritems():
            if v['status'] >= 1:
                have_readed = True
                if v['status'] == 1:
                    reward_config += v['gift']
                self.mail.mail.pop(k, {})
        if not have_readed:
            return 2, {}        # 只能一键删除已读邮件
        add_mult_gift(self.mm, reward_config, reward)
        if mail_dict != self.mail.mail:
            self.mail.save()
            return 0, {
                'mail': self.mail.mail,
                'reward': reward,
            }
        else:
            return 0, {
                'mail': self.mail.mail,
                'reward': reward,
            }

    def delete_mail(self, mail_id):
        """
        删除单个邮件
        :param mail_id:
        :return:
        """
        reward = {}
        reward_config = []
        if not mail_id:
            return 1, {}        # 没有该邮件
        if mail_id not in self.mail.mail.keys():
            return 2, {}        # 邮件已领取
        if self.mail.get_mail_status(mail_id) != 2:
            reward_config = self.mail.mail[mail_id]['gift']
        if reward_config:
            add_mult_gift(self.mm, reward_config, reward)
        self.mail.mail.pop(mail_id, {})
        self.mail.save()
        return 0, {
                'mail': self.mail.mail,
                'reward': reward,
            }
