#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import datetime
import time
import random

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice


class Friend(ModelBase):
    """ 好友


    :var friends: 好友 []
    :var messages: 消息数据 []
    :var last_refresh_date: '',             上次刷新日期 %Y-%m-%d   用于每日刷新
    :var 'parised_friend': [],              今日点赞过的好友 uid
    :var 'battle_friend': [],               今日切磋过的好友 uid
    :var 'parise_count': 0,                 历史被点赞数
    :var 'friendly_degree': {},             友好度
    :var # 'friendly_degree_reward': {},    友好度奖励
    :var 'sweep_workbench': {},             打扫工作台记录
    :var 'study_hero': {},                  记录实地学习的卡牌放在了哪个好友那儿
    :var 'red_packet': {
        'last_refresh_time': 0,             上次激活红包的时间
        'reward': [],                       红包奖励
        'reward_player': [],                领过红包的玩家
    },
    :var send_gift: []  # 发送过时间胶囊的好友
    :var received_gift: []  # 好友赠送的时间胶囊
    actors:{group_id:{'show':1,'chat_log':{chapter:[]}}}  #艺人名片记录
    chat_over:{group_id:[]}}

    """
    _need_diff = ()

    ADD_FRIEND_SORT = 'add_friend'
    AGREE_FRIEND_SORT = 'agree_friend'
    COMMON_SORT = 'common'
    ACTION_POINT_SORT = 'action_point'
    GUILD_INVITE_SORT = 'guild_invite'
    MESSAGES_LEN = 100
    REFRESH_REDPACKET = 3600  # 更新红包时间1小时

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'friends': [],
            'messages': [],

            'last_refresh_date': '',
            'parised_friend': [],
            'battle_friend': [],
            'parise_count': 0,
            'friendly_degree': {},
            'friendly_degree_reward': {},
            'sweep_workbench': {},
            'study_hero': {},

            'red_packet': {
                'last_refresh_time': 0,
                'reward': [],
                'reward_player': [],
            },

            'send_gift': [],
            'received_gift': [],
            'actors': {},
            'chat_over': {},
            'phone_daily_times': 0,
            'phone_daily_log': {},
            'nickname': {},
            'newest_friend':[]

        }
        super(Friend, self).__init__(self.uid)

    def pre_use(self):
        """
        每日点赞更新、工作台打扫更新
        :return:
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if now != self.last_refresh_date:
            self.battle_friend = []
            self.parised_friend = []
            self.sweep_workbench = {}
            self.send_gift = []
            self.received_gift = []
            self.last_refresh_date = now
            self.phone_daily_times = 0
            self.phone_daily_log = {}
            self.save()

    def set_send_gift(self, friend_id):
        """
        记录已赠送时间胶囊的好友
        :param friend_id:
        :return:
        """
        if friend_id not in self.send_gift:
            self.send_gift.append(friend_id)

    def set_received_gift(self, friend_id):
        """
        记录好友赠送的时间胶囊
        :param friend_id:
        :return:
        """
        if friend_id not in self.received_gift:
            self.received_gift.append(friend_id)

    def receive_gift(self, friend_id):
        """
        领取好友的时间胶囊
        :param friend_id:
        :return:
        """
        if friend_id in self.received_gift:
            self.received_gift.remove(friend_id)

    def add_friend(self, uid, save=False):
        """ 添加一个好友

        :param uid:
        :param save:
        :return:
        """
        if uid not in self.friends:
            self.friends.append(uid)

        # 触发好友数任务
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('friend_num', len(self.friends))

        if save:
            self.save()

    def has_friend(self, uid):
        """ 是否有这个好友

        :param uid:
        :return:
        """
        return uid in self.friends

    def remove_friend(self, uid, save=False):
        """ 删除一个好友

        :param uid:
        :param save:
        :return:
        """
        if uid in self.friends:
            self.friends.remove(uid)

        # 触发好友数任务
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('friend_num', len(self.friends), add_value=-1)

        if save:
            self.save()

    def count(self):
        """ 好友数量

        :return:
        """
        return len(self.friends)

    def get_friend_top(self, vip_level):
        """ 获取好友数量上限

        :return:
        """
        privilege_obj = self.mm.get_event('privilege')
        max_friend_num = privilege_obj.get_max_friend_num()
        # friend_num = game_config.vip.get(vip_level, {}).get('friend_num', 30)
        return max_friend_num

    def is_top(self, vip_level):
        """ 是否达到上限

        :return:
        """
        return self.count() >= self.get_friend_top(vip_level)

    def add_message(self, message, save=False):
        """ 添加消息

        :param message:
        :param save:
        :return:
        """
        if len(self.messages) > self.MESSAGES_LEN:
            self.messages = self.messages[-self.MESSAGES_LEN:]

        if not self.messages:
            message['id'] = 0
        else:
            message['id'] = self.messages[-1]['id'] + 1

        self.messages.append(message)
        self.add_newest_uid(message['send_uid'])
        if save:
            self.save()

    def del_message(self, message_id_list=None, message_id_all=False, save=False):
        """ 删除消息

        :param message_id:
        :param message_id_all:
        :param save:
        :return:
        """
        if message_id_all or message_id_list is None:
            self.messages = []
        else:
            self.messages = [x for x in self.messages if x['id'] not in message_id_list]
        if save:
            self.save()

    def get_messages(self, message_ids):
        """ 获取一条消息

        :param message_ids:
        :return:
        """
        return [message for message in self.messages if message['id'] in message_ids]

    def get_messages_by_sort(self, sort):
        """ 通过类型获取一类消息

        :param sort:
        :return:
        """
        return [message for message in self.messages if message['sort'] == sort]

    def has_add_friend_message(self, uid):
        """是否已申请加好友"""
        messages = self.get_messages_by_sort(self.ADD_FRIEND_SORT)
        for msg in messages:
            if msg['send_uid'] == uid:
                return True

        return False

    def parise(self, uid, save=False):
        """
        点赞记录
        :param uid:
        :return:
        """
        self.parised_friend.append(uid)

        if save:
            self.save()

    def add_friendly_degree(self, uid, count=1, save=False):
        """
        增加友好度
        :param uid:
        :param count:
        :return:
        """
        if uid not in self.friendly_degree:
            self.friendly_degree[uid] = count
        else:
            self.friendly_degree[uid] += count

        if save:
            self.save()

    def add_parise_count(self, count=1, save=False):
        """
        增加历史被点赞数
        :param count:
        :param save:
        :return:
        """
        self.parise_count += count

        if save:
            self.save()

    def add_sweep_workbench(self, uid, workbench_id, save=False):
        """
        增加打扫好友工作间记录
        :param uid:
        :param workbench_id:
        :param save:
        :return:
        """
        if uid not in self.sweep_workbench:
            self.sweep_workbench[uid] = []

        if workbench_id not in self.sweep_workbench[uid]:
            self.sweep_workbench[uid].append(workbench_id)

        if save:
            self.save()

    def add_study_hero(self, uid, hero_oid, save=False):
        """
        记录实地学习卡牌
        :param uid:
        :param hero_oid:
        :return:
        """
        if hero_oid not in self.study_hero:
            self.study_hero[hero_oid] = uid

        if save:
            self.save()

    def del_study_hero(self, hero_id, save=False):
        """
        删除实地学习卡牌
        :param hero_id:
        :param save:
        :return:
        """
        if hero_id in self.study_hero:
            self.study_hero.pop(hero_id)

        if save:
            self.save()

    def refresh_red_packet(self, reward, save=False):
        """
        刷新红包
        :param reward:
        :return:
        """
        now = int(time.time())

        self.red_packet['last_refresh_time'] = now
        self.red_packet['reward_player'] = []
        self.red_packet['reward'] = []
        for i in reward:
            self.red_packet['reward'].append(i)

        if save:
            self.save()

    def get_red_packet(self):
        """
        领红包
        :return:
        """
        if self.red_packet['reward']:
            return self.red_packet['reward'].pop()
        else:
            return []

    def redpacket_update_time(self):
        """
        更新红包的时间
        :return:
        """
        now = int(time.time())
        # if not self.red_packet['last_refresh_time']:
        #     self.refresh_red_packet(reward=[], save=True)

        if now - self.red_packet['last_refresh_time'] >= self.REFRESH_REDPACKET:
            return 0
        else:
            return self.REFRESH_REDPACKET - (now - self.red_packet['last_refresh_time'])

    def receive_friendly_reward(self, f_uid, friend_lv):
        """
        记录领取友好度奖励
        :param f_uid:
        :param friend_lv:
        :return:
        """
        if f_uid not in self.friendly_degree_reward:
            self.friendly_degree_reward = {
                f_uid: [friend_lv],
            }
        elif friend_lv not in self.friendly_degree_reward[f_uid]:
            self.friendly_degree_reward[f_uid].append(friend_lv)

    def has_received_friendly(self, f_uid, friend_lv):
        """
        是否领取过友好度奖励
        :param f_uid:
        :param friend_lv:
        :return:
        """
        if f_uid not in self.friendly_degree_reward or friend_lv not in self.friendly_degree_reward[f_uid]:
            return False
        else:
            return True

    def add_battle_friend(self, f_uid):
        """
        记录今日切磋的好友
        :param f_uid:
        :return:
        """
        if f_uid not in self.battle_friend:
            self.battle_friend.append(f_uid)

    def has_battle_friend(self, f_uid):
        """
        该好友是否今日切磋过
        :param f_uid:
        :return:
        """
        if f_uid in self.battle_friend:
            return True
        else:
            return False

    def get_friend_red_dot(self):
        """
        好友小红点
        :return:
        """
        for message in self.messages:
            if message['sort'] == self.ADD_FRIEND_SORT:
                return True

        return False

    def check_actor(self, group):
        if group in self.actors:
            return 201
        return 0

    def trigger_new_chat(self, chat_id, is_save=False):
        config = game_config.phone_chapter_dialogue[chat_id]
        group_id = game_config.card_basis[config['hero_id']]['group']
        if group_id not in self.actors:
            self.actors[group_id] = {'show': 1, 'chat_log': {}, 'nickname': ''}
        self.actors[group_id]['chat_log'][config['chapter_id']] = [config['dialogue_id']]
        if is_save:
            self.save()

    def new_actor(self,group_id,is_save=False):
        if group_id not in self.actors:
            self.actors[group_id] = {'show': 1, 'chat_log': {}, 'nickname': ''}
            if is_save:
                self.save()

    def get_chat_choice(self, group_id):
        chat_config = game_config.phone_daily_dialogue
        chat_list = chat_config.get(group_id, {}).get('daily_dialogue', [])
        like = self.mm.card.attr.get(group_id, {}).get('like', 0)
        chat_choice = []
        for chat in chat_list:
            if chat[2] <= like < chat[3]:
                chat_choice.append([chat[0], chat[1]])
        if not chat_choice:
            return 0
        self.phone_daily_times += 1
        choice_id = weight_choice(chat_choice)[0]
        self.phone_daily_log[self.phone_daily_times] = [choice_id]
        self.save()
        return choice_id

    def add_newest_uid(self,uid):
        if uid not in self.newest_friend:
            self.newest_friend.append(uid)
            self.newest_friend = self.newest_friend[-10:]



ModelManager.register_model('friend', Friend)
