#!usr/bin/python
# -*- coding: utf-8 -*-

from gconfig import game_config
from lib.utils import weight_choice
import copy
from return_msg_config import i18n_msg
from tools.gift import add_mult_gift, get_reward_and_num


class ServerEgg(object):

    def __init__(self, mm=None):
        self.mm = mm
        self.serveregg = self.mm.serveregg

    def is_open(self):
        if self.serveregg.get_version():
            return True
        return False

    def index(self):
        egg_item_info = game_config.server_egg_item.get(self.serveregg.version)
        egg_diamond_info = game_config.server_egg_diamond.get(self.serveregg.version)
        data = {'egg_item': {}, 'egg_diamond': {}}
        data['version'] = self.serveregg.version
        data['egg_item']['reward_show_item'] = [i[:3] for i in self.serveregg.egg_item_reward_list]
        data['egg_item']['reward_best_item'] = [i[:3] for i in egg_item_info.get('reward_1')]
        data['egg_item']['egg_times_item'] = self.serveregg.egg_item_times - self.serveregg.egg_item_used_times
        data['egg_item']['egg_used_times_item'] = self.serveregg.egg_item_used_times % egg_item_info.get('number')
        data['egg_item']['egg_num_item'] = egg_item_info.get('number')
        data['egg_item']['egg_super_times_item'] = self.serveregg.egg_item_super_times
        data['egg_item']['cost_current_item'] = egg_item_info.get('need_recharge')
        data['egg_item']['egg_sort_used_item'] = self.serveregg.egg_sort_used[2]
        data['egg_diamond']['reward_show_diamond'] = [i[:3] for i in self.serveregg.egg_diamond_reward_list]
        data['egg_diamond']['reward_best_diamond'] = [i[:3] for i in egg_diamond_info.get('reward_1')]
        data['egg_diamond']['egg_diamond'] = int(self.mm.user.diamond)
        data['egg_diamond']['egg_used_times_diamond'] = self.serveregg.egg_diamond_times % egg_diamond_info.get('number')
        data['egg_diamond']['egg_num_diamond'] = egg_diamond_info.get('number')
        data['egg_diamond']['egg_super_times_diamond'] = self.mm.item.get_item(
            egg_diamond_info.get('super_item_higher')[0][1])
        data['egg_diamond']['cost_current_diamond'] = egg_diamond_info.get('need_recharge')
        data['egg_diamond']['egg_sort_used_diamond'] = self.serveregg.egg_sort_used[1]
        return data

    def add_payment_and_item_times(self, diamond):
        if not self.is_open():
            return
        # payment = 0
        config_item = game_config.server_egg_item.get(self.serveregg.get_version(), {})
        if not config_item:
            return  # 没有配置
        need_recharge = config_item.get('need_recharge', 0)
        if not need_recharge:
            return  # 配置错误
        # if config_item.get('need_sort') == 2:
        # payment = diamond

        self.serveregg.payment += diamond
        t_number = self.serveregg.payment / need_recharge
        self.serveregg.egg_item_times = t_number
        self.serveregg.save()

    def init_reward(self, egg_type=0, save=False):
        config_item = game_config.server_egg_item.get(self.serveregg.version, {})
        config_diamond = game_config.server_egg_diamond.get(self.serveregg.version, {})
        config_item_list = []
        config_diamond_list = []
        if egg_type == 0 or egg_type == 2:
            for num_ in range(1, 4):
                keys = 'reward_' + str(num_)
                reward = copy.copy(weight_choice(config_item.get(keys)))
                weight_reward = config_item.get('reward_chance')
                if len(reward) != 4:
                    return 2, {}  # 奖品配置错误
                reward[3] = weight_reward[num_ - 1]
                if num_ == 1:
                    self.serveregg.egg_item_reward_best = reward[:3]
                config_item_list.append(reward)
            self.serveregg.egg_item_reward_list = config_item_list
            self.serveregg.egg_sort_used[2] = 0
        if egg_type == 0 or egg_type == 1:
            for num_ in range(1, 4):
                keys = 'reward_' + str(num_)
                reward = copy.copy(weight_choice(config_diamond.get(keys)))
                weight_reward = config_diamond.get('reward_chance')
                if len(reward) != 4:
                    return 2, {}  # 奖品配置错误
                reward[3] = weight_reward[num_ - 1]
                if num_ == 1:
                    self.serveregg.egg_diamond_reward_best = reward[:3]
                config_diamond_list.append(reward)
            self.serveregg.egg_diamond_reward_list = config_diamond_list
            self.serveregg.egg_sort_used[1] = 0
        if save:
            self.serveregg.save()
        return 0, {}

    def open_egg(self, egg_type, is_super, egg_sort):
        if not self.is_open():
            return 4, {}  # 活动未开启
        reward = []
        # data = {'refresh_flog': 0}
        data = {}
        if egg_type == 1:  # 金蛋
            egg_diamond_info = game_config.server_egg_diamond.get(self.serveregg.version)
            if is_super:
                item_id = egg_diamond_info.get('super_item_higher')[0][1]
                num_ = self.mm.item.get_item(item_id)
                need_num = egg_diamond_info.get('super_item_higher')[0][2]
                if num_ < need_num:
                    return 6, {}  # 高级金锤数量不足
                reward = copy.copy(self.serveregg.egg_diamond_reward_list)
                reward_best = copy.copy(self.serveregg.egg_diamond_reward_best)
                reward = [i[:3] for i in reward]
                self.mm.item.del_item(item_id, need_num)
                rc, _ = self.init_reward(egg_type=egg_type)
                if rc != 0:
                    return rc, {}
                # data['refresh_flog'] = 1
                reward_msg = get_reward_and_num(self.mm, [reward_best])
                log_ = i18n_msg.get(1301, self.mm.lan) % (self.mm.user.name, reward_msg)
                self.serveregg.add_log(log_)
            else:
                need_diamond = egg_diamond_info.get('need_recharge')
                if not self.mm.user.is_diamond_enough(need_diamond):
                    return 3, {}  # 钻石不足
                if egg_sort == self.serveregg.egg_sort_used[egg_type]:
                    return 11, {}  # 已经开过这个了

                self.mm.user.deduct_diamond(need_diamond)
                self.serveregg.egg_diamond_times += 1
                num_ = egg_diamond_info.get('number')
                self.serveregg.egg_sort_used[egg_type] = egg_sort
                super_item_higher = copy.copy(egg_diamond_info.get('super_item_higher')[0])
                super_item_higher[2] = 1

                if self.serveregg.egg_diamond_times / num_ and not self.serveregg.egg_diamond_times % num_:
                    reward.append(super_item_higher)
                reward_choice = copy.copy(weight_choice(self.serveregg.egg_diamond_reward_list))
                self.serveregg.egg_diamond_reward_list.pop(self.serveregg.egg_diamond_reward_list.index(reward_choice))
                reward_choice = reward_choice[:3]
                reward.append(reward_choice)
                if len(self.serveregg.egg_diamond_reward_list) < 2:
                    rc, _ = self.init_reward(egg_type=egg_type)
                    if rc != 0:
                        return rc, {}
                    # data['refresh_flog'] = 1
                if reward_choice == self.serveregg.egg_diamond_reward_best:
                    reward_msg = get_reward_and_num(self.mm, reward)
                    log_ = i18n_msg.get(1302, self.mm.lan) % (self.mm.user.name, reward_msg)
                    self.serveregg.add_log(log_)

        elif egg_type == 2:  # 彩蛋
            egg_item_info = game_config.server_egg_item.get(self.serveregg.version)
            if is_super:
                if not self.serveregg.egg_item_super_times:
                    return 7, {}  # 高级彩锤不足
                reward = copy.copy(self.serveregg.egg_item_reward_list)
                reward_best = copy.copy(self.serveregg.egg_item_reward_best)
                reward = [i[:3] for i in reward]
                self.serveregg.egg_item_super_times -= 1
                rc, _ = self.init_reward(egg_type=egg_type)
                if rc != 0:
                    return rc, {}
                # data['refresh_flog'] = 1
                reward_msg = get_reward_and_num(self.mm, [reward_best])
                log_ = i18n_msg.get(1303, self.mm.lan) % (self.mm.user.name, reward_msg)
                self.serveregg.add_log(log_)
            else:
                # need_num = egg_item_info.get('need_recharge')
                if not self.serveregg.egg_item_times - self.serveregg.egg_item_used_times:
                    return 5, {}  # 彩锤不足
                if egg_sort == self.serveregg.egg_sort_used[egg_type]:
                    return 11, {} # 已经开过了
                self.serveregg.egg_item_used_times += 1
                # self.serveregg.egg_item_open_times += 1
                self.serveregg.egg_sort_used[egg_type] = egg_sort
                num_ = egg_item_info.get('number')
                if self.serveregg.egg_item_used_times / num_ and not self.serveregg.egg_item_used_times % num_:
                    self.serveregg.egg_item_super_times += 1
                reward = copy.copy(weight_choice(self.serveregg.egg_item_reward_list))
                self.serveregg.egg_item_reward_list.pop(self.serveregg.egg_item_reward_list.index(reward))

                reward = [reward[:3]]
                if len(self.serveregg.egg_item_reward_list) < 2:
                    rc, _ = self.init_reward(egg_type=egg_type)
                    if rc != 0:
                        return rc, {}
                    # data['refresh_flog'] = 1
                if reward[0] == self.serveregg.egg_item_reward_best:
                    reward_msg = get_reward_and_num(self.mm, [self.serveregg.egg_item_reward_best])
                    log_ = i18n_msg.get(1304, self.mm.lan) % (self.mm.user.name, reward_msg)
                    self.serveregg.add_log(log_)
        gift = add_mult_gift(self.mm, reward)
        data['gift'] = gift
        self.mm.item.save()
        self.mm.user.save()
        self.serveregg.save()
        return 0, data