#! --*-- coding: utf-8 --*--

import time

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config

REWARD_TIME = '22:30:00'
REFRESH_TIME = '06:00:00'


class Block(ModelBase):
    NUM = 'num'
    rank_list = [1, 2, 3, 'nv', 'nan', 'medium', 'audience']
    RANKMAPPING = {'nv': 4, 'nan': 5, 'medium': 6, 'audience': 7}
    RANK = {1: 1, 2: 2, 3: 3, 4: 'nv', 5: 'nan', 6: 'medium', 7: 'audience'}

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'block_num': 1,
            'cup': 0,
            'block_group': 1,
            'top_script': {},
            'big_sale': 0,
            'last_date': '',  # 最进操作时间
            'reward_data': {},  # 奖励
            'award_ceremony': 0,  # 是否参加过颁奖典礼
            'reward_daily': '',  # 日常奖励领取时间
            'get_award_ceremony': 0,  # 典礼奖励是否领取
            'has_ceremony': 0,
            'cup_log': {},  # 奖杯获取
            'is_count': 0,  # 是否计算奖杯
            'cup_log_card': {},
            'cup_log_script': {},
            'rank_reward_got': [], # 排行奖励
            'rank_reward_date': '',  # 领奖时间
        }

        super(Block, self).__init__(self.uid)

    def pre_use(self):
        save = False
        if self.last_date != get_date():
            self.last_date = get_date()

            self.big_sale = 0
            self.award_ceremony = 0
            self.has_ceremony = 0
            self.is_count = 0
            self.reward_data = {}
            save = True
        last_date = get_date_before(REFRESH_TIME)
        if last_date != self.rank_reward_date:
            self.rank_reward_date = last_date
            self.rank_reward_got = []
            save = True
        if save:
            self.save()

    def up_block(self, cup, is_save=False):
        config = game_config.dan_grading_list
        self.cup += cup
        if self.cup >= config[self.block_num]['promotion_cup_num']:
            self.block_num += 1
            self.cup = 0
        if is_save:
            self.save()

    def get_key_profix(self, block=1, group='', type=''):
        """
        :param block: block(记录街区所有人)  block_num(取编码)
        :param group: 
        :param type:  剧本type ，nan=男，nv=女，medium=媒体评分，audience=观众评分,income=总票房,script=单片票房
        :return: 
        """
        if not group and not type:
            return 'block_%s_all' % (block)
        if not type:
            return 'block_%s||group_%s' % (block, group)
        return 'block_%s||group_%s||type_%s' % (block, group, type)

    def get_remain_time(self):
        date = get_date()
        reward_time = date + ' ' + REWARD_TIME
        reward_time = int(time.mktime(time.strptime(reward_time, '%Y-%m-%d %H:%M:%S')))
        now_time = int(time.time())
        remain_time = reward_time - now_time
        return remain_time

    def ceremony_red_dot(self):
        cup = 0
        for k, v in self.reward_data.iteritems():
            if k == 'big_sale_cup':
                cup += v
            else:
                cup += v['cup']
        if self.has_ceremony and cup and self.is_count:
            return True
        if self.award_ceremony <= 1 and self.is_count:
            return True
        return False


    def block_reward_red_hot(self):
        now = time.strftime('%F')
        return now != self.reward_daily


# 获取日期
def get_date(dt=''):
    if not dt:
        dt = REWARD_TIME
    now = time.strftime('%F')
    now_time = time.strftime('%T')
    if now_time >= dt:
        now = time.strftime('%F', time.localtime(time.time() + 3600 * 24))
    return now


# 获取前一天日期
def get_date_before(dt=''):
    if not dt:
        dt = REWARD_TIME
    now = time.strftime('%F')
    now_time = time.strftime('%T')
    if now_time < dt:
        now = time.strftime('%F', time.localtime(time.time() - 3600 * 24))
    return now


ModelManager.register_model('block', Block)
