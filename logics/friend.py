#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import random
import math

import settings
from tools.user import user_friend_info
from tools.gift import add_gift_by_weights, add_gift, add_mult_gift
from return_msg_config import i18n_msg
from gconfig import game_config
from lib.core.environ import ModelManager
from logics.user import UserLogic
from models.user import User as UserM


class FriendLogic(object):
    UNIT_EXP = 60  # 好友实地学习 60秒获得1点经验
    PARISE_SILVER = 10  # 点赞给银币

    def __init__(self, mm):
        self.mm = mm
        self.friend = self.mm.friend

    def friends_info(self):
        """ 好友列表

        :return:
        """
        result = {
            'friends': self.get_friends(),
            'friend_len': len(self.friend.friends),
            'friend_top': self.friend.get_friend_top(self.mm.user.vip),
            'send_gift': self.friend.send_gift,
            'received_gift': self.friend.received_gift,
        }

        return result

    def sent_gift(self, friend_id):
        """
        发送时间胶囊给好友
        :param friend_id:
        :return:
        """
        if not self.friend.has_friend(friend_id):
            return 1, {}  # 没有该好友

        if friend_id in self.friend.send_gift:
            return 2, {}  # 已赠送过

        friend_mm = self.mm.get_mm(friend_id)
        friend_mm.friend.set_received_gift(self.mm.uid)
        self.friend.set_send_gift(friend_id)
        # 觉醒宝箱次数任务
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('present_flower', count=1)

        friend_mm.friend.save()
        self.friend.save()

        # 更新鲜花值排行榜
        # flower_rank = self.mm.get_obj_tools('flower_rank')
        # flower_rank.incr_rank(self.mm.uid, 1)

        return 0, {
            'send_gift': self.friend.send_gift,
        }

    def sent_gift_all(self):
        """
        一键发送时间胶囊给好友
        :return:
        """
        for friend_id in self.friend.friends:
            self.sent_gift(friend_id)

        return 0, {
            'send_gift': self.friend.send_gift,
        }

    def receive_gift(self, friend_id, reward=None):
        """
        领取好友赠送的时间胶囊
        :param friend_id:
        :param reward:
        :return:
        """
        if not self.friend.has_friend(friend_id):
            return 1, {}  # 没有该好友

        if friend_id not in self.friend.received_gift:
            return 2, {}  # 没有该好友赠送的胶囊

        item_id = self.mm.home.FLOWER_ITEM_ID  # 时间胶囊
        if reward is None:
            reward = {}
        add_mult_gift(self.mm, [[3, item_id, 1]], reward)
        self.friend.receive_gift(friend_id)

        self.friend.save()

        return 0, {
            'reward': reward,
            'received_gift': self.friend.received_gift,
        }

    def receive_gift_all(self):
        """
        一键领取好友赠送的时间胶囊
        :return:
        """
        reward = {}
        for friend_id in self.friend.friends:
            self.receive_gift(friend_id, reward)

        return 0, {
            'reward': reward,
            'received_gift': self.friend.received_gift,
        }

    def messages_info(self):
        """ 消息列表

        :return:
        """
        result = {
            'messages': self.friend.messages,
            'friend_len': len(self.friend.friends),
            'friend_top': self.friend.get_friend_top(self.mm.user.vip),
        }

        return result

    def get_friends(self):
        """ 获取好友基本数据

        :return:
        """
        info_list = []
        for uid in self.friend.friends:
            info = user_friend_info(self.mm, uid)
            info_list.append(info)

        return info_list

    def search_friend(self, uid):
        """ 查找好友, 通过uid

        :param uid:
        :return:
        """
        if not uid:
            return 1, {}

        if not settings.check_uid(uid):
            return 3, {}

        if self.mm.uid == uid:
            return 2, {}

        user = UserM.get(uid)
        if not user.reg_time:
            return 3, {}

        result = {
            'friend': user_friend_info(self.mm, uid)
        }

        return 0, result

    def recommend_friend(self):
        """ 推荐好友

        :return:
        """
        user_list = []
        apply = []
        online_users = self.mm.get_obj_tools('online_users')
        users = online_users.get_user_by_start_end(0, 100)
        random.shuffle(users)

        for uid in users:
            if uid in self.friend.friends:
                continue
            if uid == self.mm.uid:
                continue
            mm = self.mm.get_mm(uid)
            if mm.friend.is_top(mm.user.vip):
                continue

            level = mm.user.level
            if math.fabs(self.mm.user.level - level) <= 10:
                if mm.friend.has_add_friend_message(self.mm.uid):
                    continue
                # messages = mm.friend.get_messages_by_sort(self.friend.ADD_FRIEND_SORT)
                # for msg in messages:
                #     if msg['send_uid'] == self.mm.uid:
                #         apply.append(uid)
                user_list.append(user_friend_info(mm, uid))

                if len(user_list) >= 4:
                    break

        return 0, {
            'recommend_friend': user_list,
            'apply': apply,
        }

    def send_message(self, target_friend, content, sort, gift=None, **kwargs):
        """ 向好友发消息

        :param target:
        :param content:
        :param sort:
        :param gift:
        :param kwargs:
        :return:
        """
        if self.mm.user.guild_id:
            guild = self.mm.get_obj_by_id('guild', self.mm.user.guild_id)
            send_guild_name = guild.name
            send_guild_id = guild.guild_id
        else:
            send_guild_name = ''
            send_guild_id = 0

        mail_dict = self.mm.mail.generate_mail(content,
                                               title=i18n_msg.get('friend',
                                                                  self.mm.user.language_sort) % self.mm.user.name,
                                               gift=gift,
                                               sort=sort,
                                               send_uid=self.mm.user.uid,
                                               send_name=self.mm.user.name,
                                               send_role=self.mm.user.role,
                                               send_level=self.mm.user.level)
        mail_dict['send_guild_name'] = send_guild_name
        mail_dict['send_guild_id'] = send_guild_id
        mail_dict.update(kwargs)
        target_friend.add_message(mail_dict, save=True)

    def apply_friend(self, uid):
        """ 申请好友

        :param uid:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}

        if self.friend.has_friend(uid):
            return 2, {}

        # 自己的好友列表是否已达到上限
        if self.friend.is_top(self.mm.user.vip):
            return 3, {}

        f_mm = self.mm.get_mm(uid)
        # 用户是否存在
        if f_mm.user.inited:
            return 4, {}

        f_friend = f_mm.friend
        # 好友的列表已经达到上限
        if f_friend.is_top(f_mm.user.vip):
            return 5, {}

        messages = f_friend.get_messages_by_sort(self.friend.ADD_FRIEND_SORT)
        for msg in messages:
            if msg['send_uid'] == self.mm.uid:
                return 6, {}  # 已申请过

        self.apply_friend_content(f_friend)

        return 0, {}

    def agree_friend(self, uid, mid):
        """ 同意好友申请

        :param uid:
        :param mid:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}

        if self.friend.has_friend(uid):
            return 2, {}

        # 自己的好友列表是否已达到上限
        if self.friend.is_top(self.mm.user.vip):
            return 3, {}

        f_mm = self.mm.get_mm(uid)
        # 对方好友已达到上限
        if f_mm.friend.is_top(f_mm.user.vip):
            if mid:
                self.friend.del_message([int(mid)])
                messages = f_mm.friend.get_messages_by_sort(self.friend.ADD_FRIEND_SORT)
                for msg in messages:
                    if msg['send_uid'] == self.mm.uid:
                        f_mm.friend.del_message([int(msg['id'])])
                self.friend.save()
            self.friend.print_log('xx' * 10)
            return 4, {
                'messages': self.friend.messages,
                'is_alert': self.friend.get_friend_red_dot(),
                'call_status': True,
            }

        self.agree_friend_content(f_mm)
        if mid:
            self.friend.del_message([int(mid)])
            messages = f_mm.friend.get_messages_by_sort(self.friend.ADD_FRIEND_SORT)
            for msg in messages:
                if msg['send_uid'] == self.mm.uid:
                    f_mm.friend.del_message([int(msg['id'])])

        self.friend.save()
        f_mm.friend.save()

        result = {
            'messages': self.friend.messages,
            'is_alert': self.friend.get_friend_red_dot()
        }

        return 0, result

    def refuse_friend(self, mids, all_mid):
        """ 拒绝好友申请

        :param mids:
        :param all_mid:
        :return:
        """
        if all_mid:
            self.friend.del_message([], True)
        else:
            self.friend.del_message(mids)

        self.friend.save()

        result = {
            'messages': self.friend.messages,
            'is_alert': self.friend.get_friend_red_dot()
        }

        return 0, result

    def remove_friend(self, uid):
        """ 删除好友

        :param uid:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}

        if not self.friend.has_friend(uid):
            return 2, {}

        f_mm = self.mm.get_mm(uid)
        f_mm.friend.remove_friend(self.mm.uid)
        self.friend.remove_friend(uid)
        f_mm.friend.save()
        self.friend.save()

        result = {
            'friends': self.get_friends(),
        }

        return 0, result

    def apply_friend_content(self, target_friend):
        """ 向对方申请加好友

        :param target_friend:
        :return:
        """
        content = i18n_msg.get(2, self.mm.user.language_sort) % self.mm.user.name
        self.send_message(target_friend, content, self.friend.ADD_FRIEND_SORT)

    def agree_friend_content(self, target_mm):
        """同意加好友
        """
        target_friend = target_mm.friend
        target_friend.add_friend(self.mm.uid)
        # content = AGREE_FRIEND_CONTENT % self.mm.user.name
        # self.send_message(target_friend, content, self.friend.AGREE_FRIEND_SORT)
        self.friend.add_friend(target_friend.uid)

    # def send_gift_content(self, target, gift=None):
    #     """送好友礼物
    #     """
    #     self.send_message(target, '', self.friend.ACTION_POINT_SORT, gift)
    #     self.user.friend.record_send_gift(target.uid, save=True)
    #
    # def guild_invite_content(self, target):
    #     """邀请对方加入联盟
    #     """
    #     content = GUILD_INVITE_CONTENT % self.user.association_name
    #     self.send_message(target, content, self.friend.GUILD_INVITE_SORT)

    def visit_friend(self, uid):
        """
        访问好友主城
        :param uid:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}  # 不能拜访自己

        if not self.friend.has_friend(uid):
            return 2, {}  # 没有该好友

        f_mm = self.mm.get_mm(uid)
        is_parise = self.is_parise(uid)

        result = {}
        result.update(user_friend_info(f_mm, uid))
        result['is_parise'] = is_parise

        return 0, result

    def is_parise(self, uid):
        """
        判断今天能不能赞这个好友
        :param uid:
        :return:
        """
        if uid not in self.friend.parised_friend:
            return True
        else:
            return False

    def parise_friend(self, uid):
        """
        给好友点赞
        :param uid:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}  # 不能给自己点赞

        if not self.friend.has_friend(uid):
            return 2, {}  # 没有该好友

        if not self.is_parise(uid):
            return 3, {}  # 今天已经赞过了

        self.friend.parise(uid)
        self.friend.add_friendly_degree(uid)

        f_mm = self.mm.get_mm(uid)
        f_mm.friend.add_parise_count()
        f_mm.friend.add_friendly_degree(self.mm.user.uid)

        add_gift(f_mm, 1, [[0, self.PARISE_SILVER]])
        reward = add_gift(self.mm, 1, [[0, self.PARISE_SILVER]])

        self.friend.save()
        f_mm.friend.save()

        result = {}
        result['is_parise'] = False
        result['reward'] = reward

        return 0, result

    def sweep_workbench(self, uid, workbench_id):
        """
        打扫工作台
        :param uid:
        :param workbench_id:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}  # 不能打扫自己的工作台

        if not self.friend.has_friend(uid):
            return 2, {}  # 没有该好友

        f_mm = self.mm.get_mm(uid)
        if workbench_id not in f_mm.manufacture.workbenchs:
            return 3, {}  # 该好友没有解锁此工作台

        if not self.is_sweep_workbench(uid, workbench_id):
            return 4, {}  # 该工作台已被打扫

        friend_clean_config = game_config.friend_clean
        if not friend_clean_config:
            return 5, {}  # 没有好友打扫的配置

        self.friend.add_sweep_workbench(uid, workbench_id)

        data = {}
        give_item = []
        friendly_count = 0

        # 获得少量材料
        for k, v in friend_clean_config.iteritems():
            level_min = v['player_level'][0]
            level_max = v['player_level'][1]
            if level_min <= self.mm.user.level <= level_max:
                give_item = v['reward']
                friendly_count = v['friend']
                break

        reward = {}
        add_gift_by_weights(self.mm, 5, give_item, cur_data=reward)

        # 增加好友度
        self.friend.add_friendly_degree(uid, friendly_count)
        f_mm = self.mm.get_mm(uid)
        f_mm.friend.add_friendly_degree(self.mm.uid, friendly_count)

        self.friend.save()
        f_mm.friend.save()

        data['reward'] = reward
        data['friendly_count'] = friendly_count

        return 0, data

    def is_sweep_workbench(self, uid, workbench_id):
        """
        判断该好友的此工作台是否打扫过
        :param uid:
        :param workbench_id:
        :return:
        """
        if uid not in self.friend.sweep_workbench or workbench_id not in self.friend.sweep_workbench[uid]:
            return True
        else:
            return False

    def encourage_workbench(self, uid, workbench_id):
        """
        给好友生产加油鼓劲
        :param uid:
        :param workbench_id:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}  # 不能给自己生产加油鼓劲

        if not self.friend.has_friend(uid):
            return 2, {}  # 没有该好友

        f_mm = self.mm.get_mm(uid)

        workbench_dict = f_mm.manufacture.workbenchs.get(workbench_id)

        if workbench_dict is None:
            return 3, {}  # 该好友没有解锁此工作台

        if not workbench_dict:
            return 4, {}  # 该好友的此工作台没有进行生产

        if workbench_dict['encourage']:
            return 5, {}  # 该工作台已被加油鼓劲

        manu_id = workbench_dict['manu_id']
        manu_config = game_config.manufacture.get(manu_id)
        if not manu_config:
            return 7, {}  # 没有生成材料的配置

        evolution = manu_config['evolution']
        friend_cheer_config = game_config.friend_cheer.get(evolution)
        if not friend_cheer_config:
            return 6, {}  # 没有好友加油配置

        time_reduce = friend_cheer_config.get('time_reduce')
        friendly_count = friend_cheer_config.get('friend')
        f_mm.manufacture.workbenchs[workbench_id]['ext_time'] -= time_reduce

        # 增加双方友好度
        self.friend.add_friendly_degree(uid, friendly_count)
        f_mm.friend.add_friendly_degree(self.mm.uid, friendly_count)

        workbench_dict['encourage'] = self.mm.uid

        data = dict(time_reduce=time_reduce, friendly_count=friendly_count)
        # data['time_reduce'] = time_reduce
        # data['friendly_count'] = friendly_count

        self.friend.save()
        f_mm.friend.save()
        f_mm.manufacture.save()

        return 0, data

    def study_manufacture(self, uid, hero_oid, workbench_id):
        """
        在好友生产中心实地学习
        :param uid:
        :param hero_oid:
        :param workbench_id:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}  # 不能在自己生产中心实地学习

        if not self.friend.has_friend(uid):
            return 2, {}  # 没有该好友

        if not self.mm.hero.has_hero(hero_oid):
            return 6, {}

        if self.mm.hero.hero_avail(hero_oid):
            return 7, {}

        f_mm = self.mm.get_mm(uid)
        if workbench_id not in f_mm.manufacture.workbenchs:
            return 3, {}  # 该好友没有解锁此工作台

        if not f_mm.manufacture.workbenchs[workbench_id]:
            return 4, {}  # 该好友的此工作台没有进行生产

        if f_mm.manufacture.workbenchs[workbench_id]['study_hero'].get('uid'):
            return 5, {}  # 该工程已经有其他人在实地学习了

        f_mm.manufacture.workbenchs[workbench_id]['study_hero']['uid'] = self.mm.uid
        f_mm.manufacture.workbenchs[workbench_id]['study_hero']['hero_oid'] = hero_oid
        f_mm.manufacture.workbenchs[workbench_id]['study_hero']['time'] = int(time.time())
        self.mm.hero.set_hero_avail(hero_oid, avail='friend_study')
        self.friend.add_study_hero(uid, hero_oid)

        f_mm.manufacture.save()
        self.mm.hero.save()
        self.friend.save()

        return 0, {}

    def revoke_study_hero(self, uid, hero_oid, workbench_id):
        """
        取回实地学习的卡牌
        :param uid:
        :param hero_oid:
        :param workbench_id:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}  # 自己的生产中心没有自己的实地学习卡牌

        if not self.friend.has_friend(uid):
            return 2, {}  # 没有该好友

        f_mm = self.mm.get_mm(uid)
        if workbench_id not in f_mm.manufacture.workbenchs:
            return 3, {}  # 该好友没有解锁此工作台

        if not f_mm.manufacture.workbenchs[workbench_id]:
            return 4, {}  # 该好友的此工作台没有进行生产

        if not f_mm.manufacture.workbenchs[workbench_id]['study_hero'].get('uid'):
            return 5, {}  # 该工程没有实地学习的卡牌

        if hero_oid not in self.mm.hero.heros:
            return 6, {}  # 自己没有这张卡

        workbench_dict = f_mm.manufacture.workbenchs[workbench_id]
        manufacture_config = game_config.manufacture.get(workbench_dict['manu_id'])

        # 如果好友生产结束
        if f_mm.manufacture.calc_remainder_time(workbench_id,
                                                workbench_dict=workbench_dict,
                                                manufacture_config=manufacture_config) <= 0:
            start_time = f_mm.manufacture.workbenchs[workbench_id]['study_hero'].get('time')
            manufacture_id = workbench_dict['manu_id']
            manufacture_config = manufacture_config or game_config.manufacture.get(manufacture_id)
            ctime = workbench_dict['ctime']
            ext_time = workbench_dict['ext_time']
            time_config = manufacture_config['time']
            end_time = ctime + time_config + ext_time
            add_exp = (end_time - start_time) / self.UNIT_EXP
            f_mm.manufacture.workbenchs[workbench_id]['exp'] += add_exp
            self.mm.hero.add_hero_exp(hero_oid, add_exp)

        self.mm.hero.set_hero_avail(hero_oid)
        self.friend.del_study_hero(hero_oid)
        f_mm.manufacture.workbenchs[workbench_id]['study_hero'] = {'uid': '', 'hero_oid': '', 'time': 0}

        f_mm.manufacture.save()
        self.mm.hero.save()
        self.friend.save()

        return 0, {}

    def red_packet(self):
        """
        激活红包
        :return:
        """
        if self.friend.redpacket_update_time():
            return 1, {}  # 还没到激活红包的时间

        redpacket_id = 0
        lv = self.mm.user.level
        redpacket_config = game_config.redpacket
        for k, v in redpacket_config.iteritems():
            if v['level'][0] <= lv <= v['level'][1]:
                redpacket_id = k
                break
        if not redpacket_id:
            return 2, {}  # 没有红包的配置

        money = redpacket_config.get(redpacket_id)['money']
        sort = redpacket_config.get(redpacket_id)['sort']
        number = redpacket_config.get(redpacket_id)['number']
        money1 = redpacket_config.get(redpacket_id)['money1']

        money = money - number  # 保证每份红包保底1
        if money < 0:
            return 3, {}  # 红包配置有误

        redpacket_reward = []
        for i in range(number):
            if i + 1 == number:
                m = money
            else:
                m = random.randint(0, money)
            redpacket_reward.append([sort, 0, m + 1])
            money -= m

        self.friend.refresh_red_packet(reward=redpacket_reward)
        self.friend.save()

        # 生成红包得奖励
        result = {}
        reward = add_mult_gift(self.mm, [[sort, 0, money1]])
        result['reward'] = reward

        ul = UserLogic(self.mm)
        data = ul.main()
        result.update(data)

        return 0, result

    def redpacket_reward(self, f_uid):
        """
        领取红包
        :param f_uid:
        :return:
        """
        f_mm = ModelManager(f_uid)
        gift = f_mm.friend.get_red_packet()
        if not gift:
            return 2, {}  # 手慢了, 红包已被领完, 请等待下次激活

        reward_player_ids = [i['uid'] for i in f_mm.friend.red_packet['reward_player']]
        if self.mm.user.uid in reward_player_ids:
            return 3, {}  # 你已经领取过此次红包, 请等待下次激活

        redpacket_id = 0
        redpacket_config = game_config.redpacket
        for k, v in redpacket_config.iteritems():
            lv = f_mm.user.level
            if v['level'][0] <= lv <= v['level'][1]:
                redpacket_id = k
                break
        if not redpacket_id:
            return 4, {}  # 没有红包的配置

        # 好友获得被领红包奖励
        sort = redpacket_config.get(redpacket_id)['sort']
        money2 = redpacket_config.get(redpacket_id)['money2']
        add_mult_gift(f_mm, [[sort, 0, money2]])

        reward = add_mult_gift(self.mm, [gift])

        f_mm.friend.red_packet['reward_player'].append(
            {
                'uid': self.mm.user.uid,
                'name': self.mm.user.name,
                'reward_num': gift[-1],
            }
        )
        f_mm.friend.save()

        result = {}
        # rc, data = self.visit_friend(f_uid)
        # result.update(data)
        result['reward'] = reward

        return 0, result

    def hire_friend(self, uid):
        """
        雇佣好友
        :param uid:
        :return:
        """
        if not self.friend.has_friend(uid):
            return 8, {}  # 没有该好友

        if self.mm.hero.has_friend_employ(uid):
            return 9, {}  # 该好友已被雇佣过

        self.mm.hero.add_friend_employ(uid)
        # 雇佣增加友好度
        self.mm.friend.add_friendly_degree(uid, count=2)
        employ_mm = self.mm.get_mm(uid)
        employ_mm.friend.add_friendly_degree(self.mm.user.uid, count=2)

        self.mm.hero.save()
        self.mm.friend.save()
        employ_mm.friend.save()

        return 0, {}

    def receive_friendly_reward(self, uid, friend_lv):
        """
        领取友好度奖励
        :param uid:
        :param friend_lv:
        :return:
        """
        if self.mm.uid == uid:
            return 1, {}  # 不能领取自己的奖励

        if not self.friend.has_friend(uid):
            return 2, {}  # 没有该好友

        if self.friend.has_received_friendly(uid, friend_lv):
            return 3, {}  # 已领取过该奖励

        need_point = game_config.friend_point.get(friend_lv, {}).get('need_point')
        if need_point == None:
            return 4, {}  # 配置有误

        if self.friend.friendly_degree.get(uid, 0) < need_point:
            return 5, {}  # 没有达到领取条件

        self.friend.receive_friendly_reward(uid, friend_lv)
        self.friend.save()

        reward_config = game_config.friend_point.get(friend_lv, {}).get('reward', [])
        reward = add_mult_gift(self.mm, reward_config)

        result = {
            'reward': reward,
        }

        return 0, result

    def actor_chat_index(self):
        data = {}
        for group_id, value in self.friend.actors.iteritems():
            if not value['show']:
                continue
            card_id = self.mm.card.group_ids.get(group_id, '')
            if not card_id:
                data[group_id] = {'own': False, 'info': {}}
            else:
                data[group_id] = {'own': True, 'info': self.mm.card.get_card(card_id)}
            data[group_id]['like'] = self.mm.card.attr.get(group_id, {}).get('like', 0)
            data[group_id]['unfinished_chapter'] = list(
                set(value['chat_log'].keys()) - set(self.friend.chat_over.get(group_id, [])))
            data[group_id]['open_chapter'] = value['chat_log'].keys()
            data[group_id]['nickname'] = value.get('nickname','')
        return 0, data

    def actor_chat(self, group_id, chapter_id, choice_id, now_stage):
        if not chapter_id:  # 日常对话
            config = game_config.avg_dialogue
            daily_config = game_config.phone_daily_dialogue[group_id]
            if now_stage not in config:
                return 11, {}  # 当前对话id错误
            if choice_id not in config[now_stage]['option_team']:
                return 12, {}  # 对话选项错误
            if self.friend.phone_daily_times >= daily_config['daily_times']:
                return 13, {}  # 次数超出
            reward_config = config[choice_id]['reward']
            add_value_config = config[choice_id]['add_value']
            add_value = self.mm.card.add_value(group_id, add_value_config)
            reward = add_mult_gift(self.mm, reward_config)
            self.friend.phone_daily_times += 1
            self.friend.save()
            return 0, {'reward': reward,
                       'add_value': add_value}
        config = game_config.phone_dialogue
        if now_stage not in config:
            return 15, {}  # 对话配置错误
        chat_log = self.friend.actors.get(group_id, {}).get('chat_log', {}).get(chapter_id, [])
        if now_stage not in chat_log:
            return 14, {}  # 当前对话id错误
        if choice_id not in config[now_stage]['option_team'] and choice_id != config[now_stage]['next']:
            return 16, {}  # 对话选择错误
        if (choice_id in config[now_stage]['option_team'] and set(config[now_stage]['option_team']) - set(
                chat_log) != set(config[now_stage]['option_team'])) or choice_id in chat_log:
            return 17, {}   #已选择过对话
        reward_config = config[choice_id]['reward']
        add_value_config = config[choice_id]['add_value']
        add_value = self.mm.card.add_value(group_id, add_value_config)
        reward = add_mult_gift(self.mm, reward_config)
        self.friend.actors.get(group_id, {}).get('chat_log', {}).get(chapter_id, []).append(choice_id)
        if config[choice_id]['is_end']:
            if group_id not in self.friend.chat_over:
                self.friend.chat_over[group_id] = [chapter_id]
            else:
                self.friend.chat_over[group_id].append(chapter_id)

        self.friend.save()
        return 0, {'reward': reward,
                   'add_value': add_value}
