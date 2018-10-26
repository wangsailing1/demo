#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice


# 推图
def chapter_stage_args(hm, data, mission):
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    stage_id = data['stage_id']
    star = data['star']
    target_sort_first = mission._CHAPTER_FIRST
    target_sort_num = mission._CHAPTER_NUM
    return {target_sort_first: {'type_hard': type_hard, 'value': 1 if data['win'] else 0, 'stage_id': stage_id,
                                'star': star},
            target_sort_num: {'type_hard': type_hard, 'value': 1 if data['win'] else 0, 'stage_id': stage_id,
                              'star': star}, }


# 拍摄（type，style，income）
def script_make(hm, data, mission):
    script_id = data['cur_script']['id']
    end_lv = data['cur_script']['end_lv']
    target_sort_type = mission._SCRIPT_TYPE
    target_sort_style = mission._SCRIPT_STYLE
    return {target_sort_type: {'script_id': script_id, 'end_lv': end_lv, 'value': 1},
            target_sort_style: {'script_id': script_id, 'end_lv': end_lv, 'value': 1}}


# 推图次数
def chapter_stage_auto_args(hm, data, mission):
    times = hm.get_argument('times', 1, is_int=True)
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    stage_id = data['stage_id']
    target_sort_num = mission._CHAPTER_NUM
    return {target_sort_num: {'type_hard': type_hard, 'value': times, 'stage_id': stage_id}, }


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
        'script.finished_analyse': script_make,
        'chapter_stage.auto_sweep': chapter_stage_auto_args,
    }

    # 配置target_sort映射
    _PLAYER_LV = 1  # 玩家等级
    _CARD_LV = 2  # 艺人等级
    _CARD_GACHA = 3  # 艺人抽取
    _SCRIPT_GACHA = 4  # 剧本抽取
    _INCOME = 5  # 总票房
    _FRIEND_GIFT = 6  # 好友送礼
    _CHAPTER_FIRST = 7  # 关卡首次通关
    _CHAPTER_NUM = 8  # 关卡通关次数
    _CARD_TRAIN = 9  # 艺人培养
    _FANS_ACTIVITY = 10  # 粉丝活动
    _EQUIP_COMPOSE = 11  # 武器合成
    _SCRIPT_TYPE = 12  # 剧本type
    _GROW = 13  # 格调进阶
    _SCRIPT_STYLE = 14  # 剧本style
    _CARD_NUM = 15  # 艺人数量
    _SCRIPT_NUM = 16  # 剧本数量
    _SHOP = 17  # 购物
    _SCRIPT_REWRITE = 18  # 剧本重写
    _COMPANY_VALUE = 19  # 公司市值

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
            'randmission_refresh_time': 0,
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
            self.daily_data = {i: 1 if i == 1001 else 0 for i in config.keys()}
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

    def get_guide_mission(self, is_save=True):
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

    # 判断新手任务是否已结束
    def check_guide_over(self):
        return len(self.guide_done) == len(game_config.guide_mission.keys())

    @classmethod
    def do_task_api(cls, mm, method, hm, rc, data):
        """做任务, 从 RequestHandler中调用
        args:
            method: 接口名字
            hm: 运行环境
            rc: 返回标识
            data: 返回数据
        """
        if rc != 0 or method not in cls._METHOD_FUNC_MAP:
            return

        kwargs = cls._METHOD_FUNC_MAP[method](hm, data, mm.mission)
        if kwargs:
            mm.mission.do_task(kwargs)

    def do_task(self, kwargs):
        for k, value in self.daily_data:
            sort = game_config.liveness[k]['sort']
            if sort in kwargs:
                self.daily.add_count(k, kwargs[k])

        for k, value in self.guide_data:
            sort = game_config.guide_mission[k]['sort']
            if sort in kwargs:
                self.guide.add_count(k, kwargs[k])

        for k, value in self.random_data:
            sort = game_config.random_mission[k]['sort']
            if sort in kwargs:
                self.randmission.add_count(k, kwargs[k])


class MissionDaily(ModelBase):
    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.daily_done
        self.data = obj.daily_data
        self.config = game_config.liveness

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def add_count(self, mission_id, value):
        if self.config[mission_id]['sort'] == 12:
            target_data = self.config[mission_id]['target']
            script_type = game_config.script[value['script_id']]['type']
            if script_type == target_data[1] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value

        elif self.config[mission_id]['sort'] == 14:
            target_data = self.config[mission_id]['target']
            script_style = game_config.script[value['script_id']]['style']
            if script_style == target_data[1] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value

        elif self.config[mission_id]['sort'] == 7:
            target_data = self.config[mission_id]['target']
            if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
                self.data[mission_id] = value['stage_id']

        elif self.config[mission_id]['sort'] == 8:
            target_data = self.config[mission_id]['target']
            star = value['star']
            type_hard = value['type_hard']
            if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value

        else:
            if mission_id in self.data:
                self.data[mission_id] += value
            else:
                self.data[mission_id] = value

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)


class MissionGuide(ModelBase):
    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.guide_done
        self.data = obj.guide_data
        self.config = game_config.guide_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def add_count(self, mission_id, value):
        if self.config[mission_id]['sort'] == 12:
            target_data = self.config[mission_id]['target']
            script_type = game_config.script[value['script_id']]['type']
            if script_type == target_data[1] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value
        elif self.config[mission_id]['sort'] == 14:
            target_data = self.config[mission_id]['target']
            script_style = game_config.script[value['script_id']]['style']
            if script_style == target_data[1] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value

        elif self.config[mission_id]['sort'] == 7:
            target_data = self.config[mission_id]['target']
            if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
                self.data[mission_id] = value['stage_id']

        elif self.config[mission_id]['sort'] == 8:
            target_data = self.config[mission_id]['target']
            star = value['star']
            type_hard = value['type_hard']
            if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value

        else:
            if mission_id in self.data:
                self.data[mission_id] += value
            else:
                self.data[mission_id] = value

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)


class MissionRandom(ModelBase):
    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.random_done
        self.data = obj.random_data
        self.config = game_config.random_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def add_count(self, mission_id, value):
        if self.config[mission_id]['sort'] == 12:
            target_data = self.config[mission_id]['target']
            script_type = game_config.script[value['script_id']]['type']
            if script_type == target_data[1] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value
        elif self.config[mission_id]['sort'] == 14:
            target_data = self.config[mission_id]['target']
            script_style = game_config.script[value['script_id']]['style']
            if script_style == target_data[1] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value

        elif self.config[mission_id]['sort'] == 7:
            target_data = self.config[mission_id]['target']
            if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
                self.data[mission_id] = value['stage_id']

        elif self.config[mission_id]['sort'] == 8:
            target_data = self.config[mission_id]['target']
            star = value['star']
            type_hard = value['type_hard']
            if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
                if mission_id in self.data:
                    self.data[mission_id] += value
                else:
                    self.data[mission_id] = value

        else:
            if mission_id in self.data:
                self.data[mission_id] += value
            else:
                self.data[mission_id] = value

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)


ModelManager.register_model('mission', Mission)
