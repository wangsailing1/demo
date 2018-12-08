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
    TYPEMAPPING = {1: 'phone_dialogue', 2: 'tour_dialogue', 3: 'tour_dialogue'}

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'friends': [],
            'messages': [],
            'friends_info': {},

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
            'newest_friend': [],
            'appointment_times': 0,  # 约会次数
            'appointment_log': {},  # 约会记录
            'tourism_times': 0,  # 旅游次数
            'tourism_log': {},  # 旅游记录
            'last_week': '',
            'got_point_daily': 0,
            'unlocked_appointment': [],

        }
        super(Friend, self).__init__(self.uid)

    def pre_use(self):
        """
        每日点赞更新、工作台打扫更新
        :return:
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        week = datetime.datetime.now().strftime('%Y-%W')
        is_save = False
        # if week != self.last_week:
        #     self.last_week = week
        #     self.tourism_times = 0
        #     self.tourism_log = {}
        #     is_save = True
        if now != self.last_refresh_date:
            self.battle_friend = []
            self.parised_friend = []
            self.sweep_workbench = {}
            self.send_gift = []
            self.received_gift = []
            self.last_refresh_date = now
            self.phone_daily_times = 0
            self.got_point_daily = 0
            self.phone_daily_log = {}
            self.appointment_times = 0
            self.appointment_log = {}
            is_save = True
        if not hasattr(self, 'friends_info'):
            self.friends_info = {}
            is_save = True
        if not self.unlocked_appointment:
            for k, v in game_config.date_chapter.iteritems():
                if v['preid'] == -1:
                    self.unlocked_appointment.append(k)
            is_save = True
        if is_save:
            self.save()

    # 按性别获取能开启的聊天场景
    def get_own_dialogue(self):
        pre_str = 'date_dialogue'
        sex = game_config.main_hero.get(self.mm.user.role, {}).get('sex', 1)
        key_word = '%s%s' % (pre_str, sex)
        config = game_config.phone_daily_dialogue
        all_list = []
        for _, v in config.iteritems():
            if v[key_word]:
                all_list.extend(v[key_word])
        all_list = list(set(all_list))
        return all_list

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

    def new_actor(self, group_id, is_save=False):
        if group_id not in self.actors:
            self.actors[group_id] = {'show': 1, 'chat_log': {}, 'nickname': ''}
            if is_save:
                self.save()

    def get_chat_choice(self, group_id, type=1):
        chat_config = game_config.phone_daily_dialogue
        times = self.phone_daily_times
        common_config = game_config.common
        max_times = common_config[24]
        like_need = 0
        point_need = 0
        pre_str = 'daily_dialogue'
        # if type == 2:
        #     times = self.appointment_times
        #     max_times = common_config[44]
        #     like_need = common_config[45]
        #     point_need = common_config[48]
        #     pre_str = 'date_dialogue'
        # elif type == 3:
        #     times = self.tourism_times
        #     max_times = common_config[46]
        #     like_need = common_config[47]
        #     point_need = common_config[49]
        #     pre_str = 'travel_dialogue'
        if self.mm.user.action_point < point_need:
            return -1
        if times >= max_times:
            return -3
        like = self.mm.card.attr.get(group_id, {}).get('like', 0)
        if like < like_need:
            return -2
        sex = game_config.main_hero.get(self.mm.user.role, {}).get('sex', 1)
        key_word = '%s%s' % (pre_str, sex)
        chat_list = chat_config.get(group_id, {}).get(key_word, [])
        chat_choice = []
        for chat in chat_list:
            if chat[2] <= like < chat[3]:
                chat_choice.append([chat[0], chat[1]])
        if not chat_choice:
            return 0
        choice_id = weight_choice(chat_choice)[0]
        if type == 1:
            self.phone_daily_times += 1
            self.phone_daily_log[self.phone_daily_times] = {'group_id': group_id,
                                                            'log': [choice_id]}
        # elif type == 2:
        #     self.appointment_times += 1
        #     self.appointment_log[self.appointment_times] = {'group_id': group_id,
        #                                                     'log': [choice_id]}
        # elif type == 3:
        #     self.tourism_times += 1
        #     if self.tourism_times not in self.tourism_log:
        #         self.tourism_log[self.tourism_times] = {'group_id': group_id,
        #                                                 'log': [choice_id]}
        self.save()
        return choice_id

    def check_chat_end(self, group_id=0, type=1):
        tp = self.TYPEMAPPING[type]
        config = getattr(game_config, tp)
        info = self.phone_daily_log
        if type == 2:
            info = self.appointment_log
        # elif type == 3:
        #     info = self.tourism_log
        times = 0
        has_chat = []
        for key, value in info.iteritems():
            if not group_id:
                e_id = value['log'][-1] if len(value['log']) > 0 else 0
                if not config.get(e_id, {}).get('is_end', 1):
                    has_chat.append(value['group_id'])
            elif value['group_id'] == group_id and key > times:
                times = key
        info_ = info.get(times, {}).get('log', [])

        end_id = info_[-1] if len(info_) > 0 else 0
        return times, config.get(end_id, {}).get('is_end', 1), has_chat

    def add_newest_uid(self, uid, is_save=False):
        if uid in self.newest_friend:
            self.newest_friend.remove(uid)
        self.newest_friend.append(uid)
        self.newest_friend = self.newest_friend[-10:]
        if is_save:
            self.save()

    def get_times(self):
        data = {}
        data['phone_daily_remain_times'] = game_config.common[24] - self.phone_daily_times
        data['appointment_remain_times'] = game_config.common[44] - self.appointment_times
        # data['tourism_remain_times'] = game_config.common[46] - self.tourism_times
        data['phone_daily_remain'] = self.check_chat_end()[-1]
        data['appointment_remain'] = self.check_chat_end(type=2)[-1]
        # data['tourism_remain'] = self.check_chat_end(type=3)[-1]
        return data

    def add_friend_like(self, uid, is_save=False):
        if uid not in self.friends_info:
            self.friends_info[uid] = {}
        if self.friends_info[uid].get('like', 0) >= game_config.common[55]:
            return
        self.friends_info[uid]['like'] = self.friends_info[uid].get('like', 0) + game_config.common[56]
        if is_save:
            self.save()

    # 新约会开始
    def add_rapport_first(self, group_id, now_stage, chapter_id, save=True):
        config = game_config.date_chapter[chapter_id]
        if now_stage != config['avg']:
            return -1
        times = self.appointment_times
        common_config = game_config.common
        max_times = common_config[44]
        if times >= max_times:
            return -3
        like = self.mm.card.attr.get(group_id, {}).get('like', 0)
        if like < config['like']:
            return -2
        for _, v in self.appointment_log.iteritems():
            if group_id != v['group_id']:
                continue
            rapport_id = v.get('log', [])
            rapport_id = rapport_id[-1] if rapport_id else 0
            tour_dialogue_config = game_config.tour_dialogue
            is_end = tour_dialogue_config.get(rapport_id, {}).get('is_end', 1)
            if not is_end:
                return -4  # 上次约会尚未完成
        if config['unlockid'] not in self.unlocked_appointment:
            self.unlocked_appointment.append(config['unlockid'])
        self.appointment_times += 1
        self.appointment_log[self.appointment_times] = {'group_id': group_id,
                                                        'log': [now_stage],
                                                        'chapter_id': chapter_id}
        if save:
            self.save()
        return 0

    def get_actor_chat(self):
        data = {}
        for group_id, value in self.actors.iteritems():
            for chapter_id, dialogue in value['chat_log'].iteritems():
                if chapter_id in self.chat_over.get(group_id, []):
                    continue
                if dialogue:
                    data[group_id] = dialogue
        return data


ModelManager.register_model('friend', Friend)
