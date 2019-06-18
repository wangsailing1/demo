model层
#! --*-- encoding:utf8 --*--

import time
from gconfig import game_config
from lib.core.environ import ModelManager
from lib.db import ModelBase
from lib.utils.active_inreview_tools import active_inreview_version, get_active_inreview_start_end_time, \
    get_server_active_start_end_time

class DiamondGacha(ModelBase):
    def __init__(self, uid):
        self.uid = uid
        self.config = game_config.diamond_limit_gacha_control
        self._attrs = {
            'gacha_times':{},
            'version':self.get_version(),
            'can_reward':{},
            'got_card':0,
            'cur_free_times':self.get_start_and_end_time()[0],
            'get_num_reward':{},
        }
        super(DiamondGacha, self).__init__(uid)

    def pre_use(self):
        self.gacha_times = {}
        self.can_reward = {}
        self.got_card = 0
        self.cur_free_times = self.get_start_and_end_time()[0],
        self.get_num_reward = {}
        self.version = self.get_version()


    def get_version(self):
        return active_inreview_version(self.config)

    def get_start_and_end_time(self):
        """获取活动起止时间戳"""
        config = game_config.diamond_limit_gacha_control[self.get_version()]
        return time.mktime(time.strptime(config['start_time'], "%Y-%m-%d %H:%M:%S")),time.mktime(time.strptime(config['end_time'], "%Y-%m-%d %H:%M:%S"))

    def get_reward(self):
        """获取有没有达到应援次数可领取的奖励"""
        for i, v in self.gacha_times.iteritems():
            if i not in self.can_reward:
                self.can_reward[i] = {}
            num_list = [z['num'] for j, z in game_config.get_diamond_limit_gacha_award_mapping()[i].iteritems() if v >= z['num'] and z['num'] not in self.get_num_reward.get(i,[])]
            self.can_reward[i] = num_list
        return self.can_reward

    def is_open(self):
        return True if self.get_version() else False

    def get_free_times(self):
        """获取有没有免费次数"""
        return time.mktime(time.localtime()) - game_config.diamond_limit_gacha_control[self.get_version()]['cd'] * 60 >= self.cur_free_times


ModelManager.register_model('diamondgacha', DiamondGacha)

logic层
#! --*-- encoding:utf8 --*--
import time

from gconfig import game_config
from lib.utils import weight_choice
from tools.gift import add_mult_gift, del_mult_goods

class DiamondCardGacha(object):
    def __init__(self, mm):
        self.mm = mm
        self.diamondgacha = self.mm.diamondgacha

    def get_gacha(self, library_id, is_ten):
        if not self.diamondgacha.is_open():
            return 1, {}    # 活动未开启
        if library_id not in game_config.diamond_limit_gacha_control[self.diamondgacha.version]['library_id']:
            return 2, {}    # library_id 错误
        cost = game_config.diamond_limit_gacha_cost[library_id]['cost']
        times = 1
        if is_ten:
            cost = game_config.diamond_limit_gacha_cost[library_id]['cost10']
        if self.diamondgacha.get_free_times() and times == 1:
            self.diamondgacha.cur_free_times = time.mktime(time.localtime())
            rc = 0
        else:
            rc, _ = del_mult_goods(self.mm, cost)
        # if rc:
        #     return rc, {}    # 扣除道具失败
        special_mapping = {v['weight_special']:i for i, v in game_config.get_diamond_limit_gacha_mapping()[library_id].iteritems()}
        id_weights = [(i, v['weight']) for i, v in game_config.get_diamond_limit_gacha_mapping()[library_id].iteritems()]
        gift = []
        if library_id not in self.diamondgacha.gacha_times:
            self.diamondgacha.gacha_times[library_id] = 0
        for i in range(times):
            self.diamondgacha.gacha_times[library_id] += 1
            if self.diamondgacha.gacha_times[library_id] in special_mapping:
                reward_id = special_mapping[self.diamondgacha.gacha_times[library_id]]
            else:
                reward_id = weight_choice(id_weights)[0]
            gift += game_config.get_diamond_limit_gacha_mapping()[library_id][reward_id]['reward']
        reward = add_mult_gift(self.mm, gift)
        self.diamondgacha.gacha_times[library_id] = times
        self.diamondgacha.save()
        data = {'reward': reward}
        data.update(self.index()[1])
        return 0, data

    def get_num_ward(self, library_id, num):
        if library_id not in self.diamondgacha.can_reward:
            return 1, {}    # 库id错误
        unum = self.diamondgacha.can_reward[library_id]
        if unum < num:
            return 2, {}    # 应援次数不够
        if num in self.diamondgacha.get_num_reward.get(library_id, []):
            return 3, {}    # 已经领取过奖
        gift = {v['num']:v['award'] for i, v in game_config.get_diamond_limit_gacha_award_mapping()[library_id].iteritems()}.get(num, [])
        reward = add_mult_gift(self.mm, gift)
        if library_id not in self.diamondgacha.get_num_reward:
            self.diamondgacha.get_num_reward[library_id] = []
        self.diamondgacha.get_num_reward[library_id].append(num)
        self.diamondgacha.save()
        data = {'reward':reward}
        data.update(self.index()[1])
        return 0, data

    def index(self):
        start_time, end_time = self.diamondgacha.get_start_and_end_time()
        self.diamondgacha.get_reward()
        return 0, {
            'start_time':start_time,
            'end_time': end_time,
            'is_free_times':self.diamondgacha.get_free_times(),
            'can_get_reward':self.diamondgacha.can_reward,
            'versing' : self.diamondgacha.get_version(),
            'gacha_times':self.diamondgacha.gacha_times,
            'get_num_reward':self.diamondgacha.get_num_reward,
        }

views层
from logics.script_diamond_gacha import DiamondCardGacha

def index(hm):
    mm = hm.mm
    diamondcard = DiamondCardGacha(mm)
    rc, data = diamondcard.index()
    return rc, data

def get_num_reward(hm):
    mm = hm.mm
    library_id = hm.get_argument('library_id', 1,is_int=True)
    num = hm.get_argument('num', 0, is_int=True)
    diamondcard = DiamondCardGacha(mm)
    rc, data = diamondcard.get_num_ward(library_id, num)
    return rc, data

def get_gacha(hm):
    mm = hm.mm
    library_id = hm.get_argument('library_id', 1, is_int=True)
    is_ten = hm.get_argument('is_ten', 0, is_int=int)
    diamondcard = DiamondCardGacha(mm)
    rc, data = diamondcard.get_gacha(library_id, is_ten)
    return rc, data



