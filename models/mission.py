#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice
from tools.gift import calc_gift


def chapter_stage_args(hm, data, reward):
    return {}


class Mission(ModelBase):
    """各种奖励数据模型

        奖励分为每日、新手、随机，存储在此模块，调用分别MissionDaily、MissionGuide、MissionRandom两个对象封装

        @property
        def daily(self):
            if not hasattr(self, '_daily'):
                self._daily = MissionDaily(self)
            return self._daily

        @property
        def once(self):
            if not hasattr(self, '_guide'):
                self._guide = MissionGuide(self)
            return self._guide

        @property
        def once(self):
            if not hasattr(self, '_random'):
                self._random = MissionRandom(self)
            return self._random
        """
    # 接口名到内置函数的映射
    _METHOD_FUNC_MAP = {
        # todo dataosha, survice
        'chapter_stage.chapter_stage_fight': chapter_stage_args,
    }

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'date': '',  # 登陆时间
            'guide_done': [],  # 新手任务
            'guide_data': {},
            'daily_done': [],  # 每日任务
            'daily_data': {},
            'random_done': [],  # 随机任务
            'random_data': {},
            'live_done': [],  # 每日活跃
            'liveness': 0,
            'box_office': {},
        }
        super(Mission, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        if self.date != today:
            config = game_config.liveness
            self.daily_done = []
            self.daily_data = {i: 0 for i in config.keys()}
            self.live_done = []
            self.liveness = 0
            self.box_office = {self.get_box_office(): 0} if self.get_box_office() else {}
            self.save()

    def get_box_office(self):
        config = game_config.box_office
        box_id = []
        for k, v in config.iteritems():
            if v['level'] == self.mm.user.level:
                box_id.append(k)
        if not box_id:
            return 0
        return min(box_id)

    @property
    def daily(self):
        if not hasattr(self, '_daily'):
            self._daily = MissionDaily(self)
        return self._daily

    @property
    def guide(self):
        if not hasattr(self, '_guide'):
            self._guide = MissionGuide(self)
        return self._guide

    @property
    def randmission(self):
        if not hasattr(self, '_randmission'):
            self._randmission = MissionRandom(self)
        return self._randmission

    def get_random_mission(self):
        config = game_config.random_mission
        pool = [[k, config[k]['weight']] for k in config.keys()]
        rand_id = weight_choice(pool)[0]
        return rand_id

    def get_guide_mission(self,is_save=True):
        done_mission = self.guide_done
        all_mission = game_config.guide_mission.keys()
        while True:
            doing_mission = self.guide_data.keys()
            if len(doing_mission) >= 4:
                break
            if len(done_mission) + len(doing_mission) >= len(all_mission):
                break
            open_mission = min(set(all_mission) - set(doing_mission) - set(done_mission))
            self.guide_data[open_mission] = 0
        if is_save:
            self.save()

    #判断新手任务是否已结束
    def check_guide_over(self):
        return len(self.guide_done) == len(game_config.guide_mission.keys())










class MissionDaily(ModelBase):
    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.daily_done
        self.data = obj.daily_data
        self.config = game_config.liveness

    def get_count(self, sort):
        return self.data.get(sort, 0)

    def add_count(self, sort, value):
        if sort in self.data:
            self.data[sort] += value
        else:
            self.data[sort] = value

    def done_task(self, award_id):
        """完成任务
        """
        if award_id not in self.done:
            self.done.append(award_id)


class MissionGuide(ModelBase):
    COUNTTYPE = [11, 9, 13, 12]
    NUMTYPE = [19, 1, 7, 2]

    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.guide_done
        self.data = obj.guide_data
        self.config = game_config.guide_mission

    def get_count(self, sort):
        return self.data.get(sort, 0)

    def add_count(self, sort, value):
        if self.config[sort]['sort'] in self.COUNTTYPE:
            if sort in self.data:
                self.data[sort] += value
            else:
                self.data[sort] = value
        elif self.config[sort]['sort'] in self.NUMTYPE:
            self.data[sort] = value

    def done_task(self, award_id):
        """完成任务
        """
        if award_id not in self.done:
            self.done.append(award_id)


class MissionRandom(ModelBase):

    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.random_done
        self.data = obj.random_data
        self.config = game_config.random_mission

    def get_count(self, sort):
        return self.data.get(sort, 0)

    def add_count(self, sort, value):
        if sort in self.data:
            self.data[sort] += value
        else:
            self.data[sort] = value

    def done_task(self, award_id):
        """完成任务
        """
        if award_id not in self.done:
            self.done.append(award_id)


ModelManager.register_model('mission', Mission)
