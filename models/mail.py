#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time

from lib.utils import salt_generator
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config, MUITL_LAN


class Mail(ModelBase):
    """ 邮件

    :var mail: {} 邮件
    """
    _need_diff = ('mail',)

    SORT_SYSTEM = 'system'
    SORT_FRIEND = 'system'
    SORT_GUILD = 'system'

    AUTO_DEL_TIME = 15 * 24 * 60 * 60  # 已读(已领取)邮件, 7天后自动删除

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'mail': {},
        }
        super(Mail, self).__init__(self.uid)

    def pre_use(self):
        """
        定期清理邮件
        :return:
        """
        now = int(time.time())
        remove_mail = []
        is_save = False
        for i, j in self.mail.iteritems():
            over_time = j.get('over_time', 0)
            send_time = j.get('send_time', 0)
            read_time = j.get('read_time', 0)
            diff_time = now - send_time
            # if over_time and diff_time >= over_time:    # 有过期时间,过期就删除
            #     remove_mail.append(i)
            # elif ((not self.has_gift(i) and j.get('status', 0) == 1) or (self.has_gift(i) and j.get('status', 0) == 2))\
            #         and now-read_time >= self.AUTO_DEL_TIME:    # 没有过期时间,已读或已领取的自动删除
            if now - send_time >= self.AUTO_DEL_TIME:  # 过期后删除
                remove_mail.append(i)

        for mail_id in remove_mail:
            self.mail.pop(mail_id)
            is_save = True

        if is_save:
            self.save()

    def data_update_func_1(self):
        """刷新公会邮件改为系统邮件"""
        for i, j in self.mail.iteritems():
            if j.get('sort') == 'guild':
                j['sort'] = 'system'
        self.save()

    @classmethod
    def _make_mail_id(cls):
        """ 生成邮件唯一id

        :return:
        """
        return '%s-%s' % (int(time.time()), salt_generator())

    @classmethod
    def generate_mail(cls, content, title='', gift=None, sort=SORT_SYSTEM,
                      send_uid='', send_name='', send_role='', send_level=1, over_time=0, url='', send_block=1,
                      send_block_rank=0):
        """ 生成邮件内容

        :param content: 邮件内容
        :param title: 邮件标题啊
        :param gift:
        :param sort:
        :param send_uid:
        :param send_name:
        :param send_role:
        :param send_level:
        :param over_time: 过期时间
        :return:
        """
        mail_dict = {
            'sort': sort,
            'send_uid': send_uid,
            'send_name': send_name,
            'send_role': send_role,
            'send_level': send_level,
            'send_block':send_block,
            'send_block_rank':send_block_rank,
            'title': title,
            'send_time': 0,
            'read_time': 0,
            'over_time': over_time,
            'auto_over_time': cls.AUTO_DEL_TIME,
            'status': 0,  # 邮件读取状态,0: 未读取, 1: 已读取, 2: 已领取
            'content': content,
            'gift': [] if gift is None else gift,
            'url': url,
        }
        return mail_dict

    def generate_mail_lan(self, content, title='', gift=None, sort=SORT_SYSTEM,
                      send_uid='', send_name='', send_role='', send_level=1, over_time=0, url='', send_block=1,
                      send_block_rank=0, format_str=None):
        """ 生成邮件内容

        :param content: 邮件内容
        :param title: 邮件标题啊
        :param gift:
        :param sort:
        :param send_uid:
        :param send_name:
        :param send_role:
        :param send_level:
        :param over_time: 过期时间
        :param format_str: 格式化内容
        :return:
        """
        lan = getattr(self.mm,'lan', 1)
        lan = MUITL_LAN[lan]
        lan_language_config = game_config.get_language_config(lan)
        title = lan_language_config.get(title, '')
        content = lan_language_config.get(content, '')
        if format_str and content:
            content = content % format_str
        mail_dict = {
            'sort': sort,
            'send_uid': send_uid,
            'send_name': send_name,
            'send_role': send_role,
            'send_level': send_level,
            'send_block':send_block,
            'send_block_rank':send_block_rank,
            'title': title,
            'send_time': 0,
            'read_time': 0,
            'over_time': over_time,
            'auto_over_time': self.AUTO_DEL_TIME,
            'status': 0,  # 邮件读取状态,0: 未读取, 1: 已读取, 2: 已领取
            'content': content,
            'gift': [] if gift is None else gift,
            'url': url,
        }
        return mail_dict

    def has_gift(self, mail_id):
        """
        邮件是否有奖励
        :param mail_id:
        :return:
        """
        if mail_id not in self.mail:
            return False

        return self.mail[mail_id]['gift']

    def add_mail(self, mail_dict, save=True):
        """ 添加邮件

        :param mail_dict:
        :param save:
        :return:
        """
        now = int(time.time())

        mail_id = self._make_mail_id()

        mail_dict['send_time'] = now

        self.mail[mail_id] = mail_dict

        if save:
            self.save()

    def get_mail_status(self, mail_id):
        """
        获取邮件状态
        :param mail_id:
        :return:
        """
        return self.mail.get(mail_id, {}).get('status', 0)

    def set_mail_status(self, mail_id, status):
        """
        设置邮件状态
        :param mail_id:
        :param status: 1: 已读取, 2: 已领取
        :return:
        """
        if mail_id in self.mail:
            mail_dict = self.mail[mail_id]
            if mail_dict['status'] != status:
                mail_dict['status'] = status

    def remove_mail(self, mail_id, save=True):
        """ 删除邮件

        :param mail_id:
        :param save:
        :return:
        """
        self.mail.pop(mail_id, None)
        if save:
            self.save()

    def get_mail_red_dot(self):
        """
        邮件小红点
        :return:
        """
        for mid, m_dict in self.mail.iteritems():
            if m_dict['sort'] == 'guild':
                continue
            if (m_dict['gift'] and m_dict['status'] < 2) or \
                    (not m_dict['gift'] and m_dict['status'] < 1):
                return True

        return False


ModelManager.register_model('mail', Mail)
