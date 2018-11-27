#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice

"""
任务对应个个接口的返回数据
def func(hm, data, mission):
    :param hm:      运行环境
    :param data:    接口返回数据
    :param mission: 任务类
    :return: {target_sort:{'target1': type_hard, 'value': times, 'stage_id': stage_id,
                              'star': 1},}} 
    target_sort:任务类型
    target1：任务目标
    value： 任务完成值
    stage_id，star：根据任务目标 返回的其他目标数据值
    
"""
# 推图
def chapter_stage_args(hm, data, mission):
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    stage_id = data.get('stage_id', 0)
    star = data.get('star', 0)
    target_sort_first = mission._CHAPTER_FIRST
    target_sort_num = mission._CHAPTER_NUM
    return {target_sort_first: {'target1': type_hard, 'value': 1 if data.get('win', 0) else 0, 'stage_id': stage_id,
                                'star': star},
            target_sort_num: {'target1': type_hard, 'value': 1 if data.get('win', 0) else 0, 'stage_id': stage_id,
                              'star': star}, }


# 拍摄（type，style，income）
def script_make(hm, data, mission):
    script_id = data['cur_script']['id']
    end_lv = data['cur_script']['end_lv']
    target_sort_type = mission._SCRIPT_TYPE
    target_sort_style = mission._SCRIPT_STYLE
    target_sort_income = mission._INCOME
    return {target_sort_type: {'target1': script_id, 'end_lv': end_lv, 'value': 1},
            target_sort_style: {'target1': script_id, 'end_lv': end_lv, 'value': 1},
            target_sort_income: {'target1': 0, 'value': data['cur_script']['finished_summary']['income']}}


# 推图次数
def chapter_stage_auto_args(hm, data, mission):
    times = hm.get_argument('times', 1, is_int=True)
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    stage_id = data['stage_id']
    target_sort_num = mission._CHAPTER_NUM
    return {target_sort_num: {'target1': type_hard, 'value': times, 'stage_id': stage_id,
                              'star': 1}, }


# 抽卡
def card_gacha(hm, data, mission):
    sort = hm.get_argument('sort', is_int=True)
    count = hm.get_argument('count', 1, is_int=True)
    target_sort = mission._CARD_GACHA
    return {target_sort: {'target1': sort, 'value': count}}


# 抽剧本
def script_gacha(hm, data, mission):
    sort = hm.get_argument('sort', is_int=True)
    count = hm.get_argument('count', 1, is_int=True)
    target_sort = mission._SCRIPT_GACHA
    return {target_sort: {'target1': sort, 'value': count}}


# 等级
def user_lv(hm, data, mission):
    lv = hm.mm.user.level
    return {mission._PLAYER_LV: {'target1': lv, 'value': lv}}


# 卡牌等级
def card_lv(hm, data, mission):
    card_oid = hm.get_argument('card_oid')
    return {mission._CARD_LV: {'target1': 0, 'value': hm.mm.card.cards[card_oid]['lv'], 'card_id': card_oid}}


# 好友送礼
def send_gift(hm, data, mission):
    return {mission._FRIEND_GIFT: {'target1': 0, 'value': len(data['send_gift'])}}


# 粉丝活动
def fans_activity(hm, data, mission):
    activity_id = hm.get_argument('activity_id', 0, is_int=True)
    config = game_config.fans_activity[activity_id]
    group = config['groupid']
    return {mission._FANS_ACTIVITY: {'target1': group, 'value': 1}}


# 艺人培养
def card_train(hm, data, mission):
    is_dimaond = hm.get_argument('is_dimaond', is_int=True)
    return {mission._CARD_TRAIN: {'target1': is_dimaond + 1, 'value': 1}}


# 武器合成
def equip_piece_exchange(hm, data, mission):
    return {mission._EQUIP_COMPOSE: {'target1': 0, 'value': 1}}


# 格调进阶
def card_quality_up(hm, data, mission):
    return {mission._GROW: {'target1': 0, 'value': 1}}


# 艺人数量
def card_get(hm, data, mission):
    return {mission._CARD_NUM: {'target1': 0, 'value': len(hm.mm.card.cards)}}


# 剧本数量
def scrip_get(hm, data, mission):
    return {mission._SCRIPT_NUM: {'target1': 0, 'value': len(hm.mm.script.own_script)}}


# 购物
def shop_args(hm, data, mission):
    return {mission._SHOP: {'target1': 0, 'value': 1}}


# 剧本重写
def script_rewrite(hm, data, mission):
    return {mission._SCRIPT_REWRITE: {'target1': 0, 'value': 1}}


# 公司市值
def compamy_value(hm, data, mission):
    v = 20
    return {mission._COMPANY_VALUE: {'target1': v, 'value': 1}}


TYPE_MAPPING = {12: 'type', 14: 'style'}   #剧本拍摄
CHANGE_NUM = [1, 19]    #纯数值 玩家等级  公司市值
CARD_LEVEL = 2  #艺人等级
FIRST_CHAPTER = 7  #首次通关
NUM_CHAPTER = 8  #通关次数


class Mission(ModelBase):
    """各种奖励数据模型

        奖励分为每日、新手、随机，存储在此模块，调用分别MissionDaily、MissionGuide、MissionRandom 对象封装

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
        'chapter_stage.chapter_stage_fight': chapter_stage_args,   #通关
        'script.finished_summary': script_make,                    #剧本拍摄
        'chapter_stage.auto_sweep': chapter_stage_auto_args,       #自动推图 增加通关次数
        'script_gacha.get_gacha': script_gacha,                    #抽剧本
        'gacha.receive': card_gacha,                               #抽卡
        'card.card_level_up': card_lv,                             #艺人升级
        'friend.sent_gift': send_gift,                             #好友送礼
        'friend.sent_gift_all': send_gift,                         #一键送礼
        'fans_activity.activity': fans_activity,                   #粉丝活动
        'card.card_train': card_train,                             #卡牌训练
        'card.equip_piece_exchange': equip_piece_exchange,         #装备碎片合成
        'card.card_quality_up': card_quality_up,                   #艺人格调提升
        'shop.shop': shop_args,                                    #商店购买

    }
    # mission_mapping
    MISSIONMAPPING = {1: 'daily', 2: 'box_office', 3: 'guide', 4: 'randmission'}
    BOXOFFICEREFRESHTIME = '05:00:00'

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

    RANDOMREFRESHTIME = 4 * 60 * 60

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
            'box_office_done': [],
            'box_office_data': {},
            'box_office_last_date': '',
            'refresh_times': 0,
        }
        super(Mission, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        box_office_time = time.strftime('%T')
        is_save = False
        if self.date != today:
            self.date = today
            self.daily_done = []
            self.daily_data = self.get_daily_mission()
            self.live_done = []
            self.liveness = 0
            self.refresh_times = 0
            if not self.guide_done and not self.guide_data:
                self.get_guide_mission()
            is_save = True
        if self.box_office_last_date != today and box_office_time >= self.BOXOFFICEREFRESHTIME:
            self.box_office_done = []
            self.box_office_last_time = today
            self.box_office_data = {self.get_box_office(): 0, 'time': int(time.time())} if self.get_box_office() else {}
            is_save = True
        if int(time.time()) > self.box_office_data.get('time', 0) + game_config.common[57]:
            is_save = self.init_box_office()
        if is_save:
            self.save()

    def get_daily_mission(self):
        config = game_config.liveness
        return {i: 1 if i == 1001 else 0 for i in config.keys()}

    #到时间刷新任务目标
    def init_box_office(self):
        config = game_config.box_office
        for m_id, value in self.box_office_data.iteritems():
            if isinstance(m_id, basestring) and 'time' in m_id:
                continue
            if value < config[m_id]['target1']:
                self.box_office_data[m_id] = 0
                return True
        return False

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
    def box_office(self):
        if not hasattr(self, '_box_office'):
            self._box_office = BoxOffice(self)
        return self._box_office

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

    def get_all_random_mission(self):
        if not self.random_data:
            for _ in xrange(4):
                while True:
                    mission_id = self.get_random_mission()
                    if mission_id in self.random_data:
                        continue
                    self.random_data[mission_id] = 0
                    break
        else:
            now = int(time.time())
            del_dict = {}
            for k, v in self.random_data.iteritems():
                if isinstance(k, (str, unicode)) and 'refresh_ts' in k and now >= v + self.RANDOMREFRESHTIME:
                    while True:
                        mission_id = self.get_random_mission()
                        if mission_id in self.random_data or mission_id in del_dict:
                            continue
                        del_dict[mission_id] = k
                        break
            if del_dict:
                for add_key, del_key in del_dict.iteritems():
                    self.random_data.pop(del_key)
                    self.random_data[add_key] = 0

    def refresh_random_misstion(self, mission_id, is_save=False):
        new_mission_id = mission_id
        while new_mission_id == mission_id or new_mission_id in self.random_data:
            new_mission_id = self.get_random_mission()
        self.random_data.pop(mission_id)
        self.random_data[new_mission_id] = 0
        self.refresh_times += 1
        if is_save:
            self.save()

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
    def do_task_api(cls, method, hm, rc, data):
        """做任务, 从 RequestHandler中调用
        args:
            method: 接口名字
            hm: 运行环境
            rc: 返回标识
            data: 返回数据
        """

        if rc != 0 or method not in cls._METHOD_FUNC_MAP:
            return

        kwargs = cls._METHOD_FUNC_MAP[method](hm, data, hm.mm.mission)
        if kwargs:
            mission = hm.mm.mission
            mission.do_task(kwargs)

    def do_task(self, kwargs):
        for k, value in self.daily_data.iteritems():
            sort = game_config.liveness[k]['sort']
            if sort in kwargs:
                self.daily.add_count(k, kwargs[sort])

        for k, value in self.guide_data.iteritems():
            sort = game_config.guide_mission[k]['sort']
            if sort in kwargs:
                self.guide.add_count(k, kwargs[sort])

        for k, value in self.random_data.iteritems():
            if isinstance(k, (str, unicode)) and 'refresh_ts' in k:
                continue
            sort = game_config.random_mission[k]['sort']
            if sort in kwargs:
                self.randmission.add_count(k, kwargs[sort])

        for k, value in self.box_office_data.iteritems():
            sort = game_config.box_office[k]['sort']
            if sort in kwargs and sort == self._INCOME:
                self.box_office.add_count(k, kwargs[sort])
        self.save()


class BoxOffice(object):
    """
    """

    def __init__(self, obj):
        """初始化
        """
        self.uid = obj.uid
        self.done = obj.box_office_done
        self.data = obj.box_office_data
        self.config = game_config.box_office

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def add_count(self, mission_id, value):
        if mission_id in self.data:
            self.data[mission_id] += value['value']
        else:
            self.data[mission_id] = value['value']

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)
            self.start_next(mission_id)

    def start_next(self, mission_id):
        next_id = self.config[mission_id]['next_id']
        if next_id:
            self.data = {next_id: 0, 'time':int(time.time())}


class MissionDaily(ModelBase):
    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.daily_done
        self.data = obj.daily_data
        self.config = game_config.liveness

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def add_count(self, mission_id, value):

        if self.config[mission_id]['sort'] in TYPE_MAPPING:
            type = TYPE_MAPPING[self.config[mission_id]['sort']]
            target_data = self.config[mission_id]['target']
            script_type = game_config.script[value['target1']][type]
            if script_type == target_data[0] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] == CARD_LEVEL:
            target_data = self.config[mission_id]['target']
            card_id = value['card_id']
            if isinstance(self.data[mission_id], int):
                self.data[mission_id] = []
            if card_id not in self.data[mission_id] and value['value'] >= target_data[0]:
                self.data[mission_id].append(card_id)

        elif self.config[mission_id]['sort'] == FIRST_CHAPTER:
            target_data = self.config[mission_id]['target']
            if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] == NUM_CHAPTER:
            target_data = self.config[mission_id]['target']
            star = value.get('star', 0)
            type_hard = value['target1']
            if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']
        elif self.config[mission_id]['sort'] in CHANGE_NUM:
            self.data[mission_id] = value['value']

        else:
            if mission_id in self.data:
                self.data[mission_id] += value['value']
            else:
                self.data[mission_id] = value['value']

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)
            self.data.pop(mission_id)


class MissionGuide(ModelBase):
    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.guide_done
        self.data = obj.guide_data
        self.config = game_config.guide_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def add_count(self, mission_id, value):
        if self.config[mission_id]['sort'] in TYPE_MAPPING:
            type = TYPE_MAPPING[self.config[mission_id]['sort']]
            target_data = self.config[mission_id]['target']
            script_type = game_config.script[value['target1']][type]
            if script_type == target_data[0] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] == CARD_LEVEL:
            target_data = self.config[mission_id]['target']
            card_id = value['card_id']
            if isinstance(self.data[mission_id], int):
                self.data[mission_id] = []
            if card_id not in self.data[mission_id] and value['value'] >= target_data[0]:
                self.data[mission_id].append(card_id)

        elif self.config[mission_id]['sort'] == FIRST_CHAPTER:
            target_data = self.config[mission_id]['target']
            if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] == NUM_CHAPTER:
            target_data = self.config[mission_id]['target']
            star = value.get('star', 0)
            type_hard = value['target1']
            if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']
        elif self.config[mission_id]['sort'] in CHANGE_NUM:
            self.data[mission_id] = value['value']

        else:
            if mission_id in self.data:
                self.data[mission_id] += value['value']
            else:
                self.data[mission_id] = value['value']

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)
            self.data.pop(mission_id)


class MissionRandom(ModelBase):
    def __init__(self, obj):
        self.uid = obj.uid
        self.done = obj.random_done
        self.data = obj.random_data
        self.config = game_config.random_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def add_count(self, mission_id, value):
        if self.config[mission_id]['sort'] in TYPE_MAPPING:
            type = TYPE_MAPPING[self.config[mission_id]['sort']]
            target_data = self.config[mission_id]['target']
            script_type = game_config.script[value['target1']][type]
            if script_type == target_data[0] and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] == CARD_LEVEL:
            target_data = self.config[mission_id]['target']
            card_id = value['card_id']
            if isinstance(self.data[mission_id], int):
                self.data[mission_id] = []
            if card_id not in self.data[mission_id] and value['value'] >= target_data[0]:
                self.data[mission_id].append(card_id)

        elif self.config[mission_id]['sort'] == FIRST_CHAPTER:
            target_data = self.config[mission_id]['target']
            if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] == NUM_CHAPTER:
            target_data = self.config[mission_id]['target']
            star = value.get('star', 0)
            type_hard = value['target1']
            if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']
        elif self.config[mission_id]['sort'] in CHANGE_NUM:
            self.data[mission_id] = value['value']

        else:
            if mission_id in self.data:
                self.data[mission_id] += value['value']
            else:
                self.data[mission_id] = value['value']

    def done_task(self, mission_id):
        """完成任务
        """
        now = int(time.time())
        self.done.append(mission_id)
        for key in range(1, 5):
            refresh_key = '%s%s' % ('refresh_ts', key)
            if refresh_key not in self.data:
                break
        self.data[refresh_key] = now
        self.data.pop(mission_id)


ModelManager.register_model('mission', Mission)
