#! --*-- coding: utf-8 --*--


import time
from gconfig import game_config, MUITL_LAN
from tools.gift import add_mult_gift, has_mult_goods, del_mult_goods
import random
from lib.utils.active_inreview_tools import get_inreview_version
from lib.core.environ import ModelManager
from lib.utils.debug import print_log
from return_msg_config import i18n_msg


class ServerToy(object):
    mapping = {1: 'servertoy', 2: 'serverfreetoy'}
    pre_str_mapping = {1: 'server_rmb_', 2: 'server_free_'}
    VIP_MAPPING = {1: 'if_super_catcher', 2: 'if_catcher'}

    def __init__(self, mm, sort=1):
        self.mm = mm
        self.sort = sort
        self.toy = getattr(self.mm, self.mapping[sort])
        self.pre_str = self.pre_str_mapping[sort]

    def is_open(self):
        method = 'if_catcher' if self.sort == 2 else 'if_super_catcher'
        module = __import__('models.vip_company', globals(), locals(), ['if_catcher', 'if_super_catcher'])
        fun = getattr(module, method)
        if not fun(self.mm.user):
            return -1
        version = self.toy.get_version()
        return version

    def unlock_lv(self):
        lv = 1
        k = self.VIP_MAPPING[self.sort]
        while True:
            if game_config.vip_company[lv][k]:
                break
            lv += 1
        return lv

    def index(self):
        status = self.is_open()
        if status == -1:
            lv = self.unlock_lv()
            return 11, {'custom_msg': i18n_msg.get(1210, self.mm.lan) % lv}  # vip等级不够
        if not status:
            return 1, {}  # 活动未开启
        if self.check_done():
            self.toy.refresh_reward()
        data = {}
        data['reward_list'] = self.toy.toy_list
        data['version'] = self.toy.version
        data['remain_time'] = self.toy.remain_refresh_time()
        data['luck_num'] = self.toy.catch_num_current
        data['toy_num'] = self.toy.toy_num
        if self.sort == 1:
            data['rank'] = self.get_all_rank_user_info()
            data['own_rank'] = self.toy.get_rank(self.mm.uid)
            data['own_score'] = self.toy.get_score(self.mm.uid)
        return 0, data

    def get_all_rank_user_info(self):
        info = []
        rank_list = self.toy.get_all_user(start=0, end=99, withscores=True)
        rank = 1
        for uid, score in rank_list:
            mm = ModelManager(uid)
            info.append({'name': mm.user.name, 'score': score, 'rank': rank})
            rank += 1
        return info

    def get_toy(self, catch, reward_id):
        status = self.is_open()
        if status == -1:
            lv = self.unlock_lv()
            return 11, {'custom_msg': i18n_msg.get(1210, self.mm.lan) % lv}  # vip等级不够
        if not status:
            return 1, {}  # 活动未开启
        gacha_config = getattr(game_config, '%s%s' % (self.pre_str, 'gacha'))
        gacha_cost_config = getattr(game_config, '%s%s' % (self.pre_str, 'gacha_cost'))
        gacha_control_config = getattr(game_config, '%s%s' % (self.pre_str, 'gacha_control'))

        cost = gacha_cost_config[min(self.toy.toy_num + 1, max(gacha_cost_config.keys()))]['cost']
        rc = has_mult_goods(self.mm, cost)
        if not rc:
            return 4, {}  # 道具不足
        del_mult_goods(self.mm, cost)
        if not catch:
            gift = gacha_control_config[self.toy.version]['compensate']
            reward = add_mult_gift(self.mm, gift)
            # self.toy.toy_list[reward_id]['num'] += 1
            self.toy.toy_num += 1
            self.toy.all_toy_num += 1
            self.toy.save()
            _, data = self.index()
            data['reward'] = reward
            data['got'] = False
            return 0, data
        if reward_id not in self.toy.toy_list:
            return 3, {}  # 娃娃错误
        if self.toy.toy_list[reward_id]['flag'] == 1:
            return 2, {}  # 娃娃已经被抓走了
        group_id = gacha_config[self.toy.toy_list[reward_id]['reward_id']]['group']
        group_need = self.get_group_mustgetnum(group_id)
        if self.toy.toy_num > group_need:
            got = True
        else:
            got = self.check_got(self.toy.toy_list[reward_id]['reward_id'])
        self.toy.toy_num += 1
        self.toy.all_toy_num += 1
        self.toy.catch_num_current += 1

        if not got:
            gift = gacha_control_config[self.toy.version]['compensate']
            self.toy.toy_list[reward_id]['num'] += 1
        else:
            gift = gacha_config[self.toy.toy_list[reward_id]['reward_id']]['award']
            self.toy.toy_list[reward_id]['num'] += 1
            self.toy.catch_num += 1
            self.toy.toy_list[reward_id]['flag'] = 1
            self.toy.got_reward.append({reward_id: self.toy.toy_list[reward_id]})
            # self.toy.toy_list.pop(reward_id)

        # 抽完自动刷新
        if self.check_done():
            self.toy.refresh_reward()

        reward = add_mult_gift(self.mm, gift)
        self.toy.save()
        if self.sort == 1 and self.toy.catch_num:
            self.toy.add_rank(self.mm.uid, self.toy.catch_num)
        _, data = self.index()
        data['reward'] = reward
        data['got'] = got
        return 0, data

    def check_done(self):
        for k, v in self.toy.toy_list.iteritems():
            if not v['flag']:
                return False
        return True

    def get_group_mustgetnum(self, group_id):
        gacha_control_config = getattr(game_config, '%s%s' % (self.pre_str, 'gacha_control'))
        config = gacha_control_config[self.toy.version]
        for group, num in config['group_mustgetnum']:
            if group == group_id:
                return num

    def check_got(self, reward_id):
        gacha_config = getattr(game_config, '%s%s' % (self.pre_str, 'gacha'))
        reward_need_num = max(self.toy.catch_num_current - gacha_config[reward_id]['mustlost'], 0)
        if not reward_need_num:
            return False
        undrop_rate_dict = dict(gacha_config[reward_id]['undrop_rate'])
        reward_need_num = reward_need_num if reward_need_num <= max(undrop_rate_dict.keys()) else max(
            undrop_rate_dict.keys())
        rate = undrop_rate_dict.get(reward_need_num)
        return rate >= random.randint(1, 10000)

    def refresh(self):
        status = self.is_open()
        if status == -1:
            lv = self.unlock_lv()
            return 11, {'custom_msg': i18n_msg.get(1210, self.mm.lan) % lv}  # vip等级不够
        if not status:
            return 1, {}  # 活动未开启
        gacha_control_config = getattr(game_config, '%s%s' % (self.pre_str, 'gacha_control'))
        if self.toy.is_free_refresh():
            cost = []
            self.toy.last_refresh_time = int(time.time())
        else:
            cost = gacha_control_config[self.toy.version]['cost']
        rc = has_mult_goods(self.mm, cost)
        if not rc:
            return 2, {}  # 道具不足
        del_mult_goods(self.mm, cost)
        self.toy.refresh_reward()
        self.toy.save()
        _, data = self.index()
        return 0, data

    def get_rank_reward(self):
        status = self.is_open()
        if status == -1:
            lv = self.unlock_lv()
            return 11, {'custom_msg': i18n_msg.get(1210, self.mm.lan) % lv}  # vip等级不够
        if not status:
            return 1, {}  # 活动未开启
        gacha_rank_config = getattr(game_config, '%s%s' % (self.pre_str, 'gacha_rank'))
        if self.toy.rank_reward:
            return 3, {}  # 奖励已领
        rank = self.toy.get_rank(self.mm.uid)
        gift = []
        for id, value in gacha_rank_config:
            if value['rank'][0] <= rank <= value['rank'][1]:
                gift = value['reward']
                break
        if not gift:
            return 2, {}  # 排行没有奖励
        reward = add_mult_gift(self.mm, gift)
        self.toy.rank_reward = gift
        self.toy.save()
        return 0, {'reward': reward}


def send_rank_reward(server):
    umm = ModelManager('%s1234567' % server)
    version, new_server, s_time, e_time = get_inreview_version(umm.user, 2021)
    if version:
        return
    version, new_server, s_time, e_time = get_inreview_version(umm.user, 2021, diff_hour=1)
    if not version:
        return
    _key = umm.servertoy.get_key(version)
    all_rank = umm.servertoy.get_all_user(start=0, end=99, r_key=_key)
    config = game_config.rmb_gacha_rank
    info = {}
    for rank, uid in enumerate(all_rank, 1):
        for k, value in config.iteritems():
            if value['rank'][0] <= rank <= value['rank'][1]:
                mm = ModelManager(uid)
                gift = value['reward']
                title = value['mail_title']
                content = value['mail_content']
                lan = MUITL_LAN[mm.user.language_sort]
                title = game_config.get_language_config(lan)[title]
                content = game_config.get_language_config(lan)[content] % rank
                msg = mm.mail.generate_mail(content, title=title, gift=gift)
                mm.mail.add_mail(msg)
                info[uid] = [rank, gift]
    print_log(info)
