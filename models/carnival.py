#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice
from lib.utils.time_tools import get_server_days, str2timestamp, timestamp_different_days

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


# 成就
def mission_args(hm, data, mission):
    mm = hm.mm
    achieve = mm.mission.achieve
    return {mission._ACHIEVE: {'target1': 0, 'value': achieve}}



# =================================需要自检的数值类任务func=================================

def target_sort1():
    pass


TYPE_MAPPING = {12: 'type', 14: 'style'}  # 剧本拍摄
CHANGE_NUM = [1, 19, 21]  # 纯数值 玩家等级  公司市值
CARD_LEVEL = 2  # 艺人等级
FIRST_CHAPTER = 7  # 首次通关
NUM_CHAPTER = 8  # 通关次数


class Carnival(ModelBase):
    """各种奖励数据模型

        
        """
    # 接口名到内置函数的映射
    _METHOD_FUNC_MAP = {
        'chapter_stage.chapter_stage_fight': chapter_stage_args,  # 通关
        'script.finished_summary': script_make,  # 剧本拍摄
        'chapter_stage.auto_sweep': chapter_stage_auto_args,  # 自动推图 增加通关次数
        'script_gacha.get_gacha': script_gacha,  # 抽剧本
        'gacha.receive': card_gacha,  # 抽卡
        'card.card_level_up': card_lv,  # 艺人升级
        'friend.sent_gift': send_gift,  # 好友送礼
        'friend.sent_gift_all': send_gift,  # 一键送礼
        'fans_activity.activity': fans_activity,  # 粉丝活动
        'card.card_train': card_train,  # 卡牌训练
        'card.equip_piece_exchange': equip_piece_exchange,  # 装备碎片合成
        'card.card_quality_up': card_quality_up,  # 艺人格调提升
        'shop.shop': shop_args,  # 商店购买
        # 'mission.get_reward': mission_args,                           # 成就

    }
    # mission_mapping
    MISSIONMAPPING = {1: 'daily', 2: 'box_office', 3: 'guide', 4: 'randmission', 6: 'achieve_mission'}
    BOXOFFICEREFRESHTIME = '05:00:00'

    # 数值类任务初始化时需要自检的
    NEEDCHECKMISSIONID = [1, 2, 7, 15, 16, 19, 23]

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
    _ACHIEVE = 21  # 成就

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'server_carnival_data': {},
            'server_carnival_done': {},
            'server_dice_num': 0,
            'server_carnival_days': 0,
            'server_carnival_step': 0,
            'carnival_data': {},
            'carnival_done': {},
            'dice_num': 0,
            'carnival_days': 0,
            'carnival_step': 0,
        }

    def pre_use(self, save=False):
        server_carnival_days = self.server_carvical_open()
        carnival_active_days = self.server_carvical_open(tp=2)
        if not server_carnival_days and self.server_carnival_days:
            self.server_carnival_data = {}
            self.server_carnival_done = {}
            self.server_dice_num = 0
            self.server_carnival_days = 0
            self.server_carnival_step = 0
            save = True
        if not carnival_active_days and self.carnival_days:
            self.carnival_data = {}
            self.carnival_done = {}
            self.dice_num = 0
            self.carnival_days = 0
            self.carnival_step = 0
            save = True
        if server_carnival_days and server_carnival_days != self.server_carnival_days:
            self.server_carnival_days = server_carnival_days
            self.server_carnival_data = {}
            mission_config = game_config.carnival_mission
            for mission_id, value in mission_config.iteritems():
                if value['days_new'] == server_carnival_days:
                    self.server_carnival_data[mission_id] = 0
                    # todo 自检数值类任务完成程度
                    mission_sort = value['sort']
                    if mission_sort in self.NEEDCHECKMISSIONID:
                        func = globals()['target_sort%s' % mission_sort]

        if carnival_active_days and carnival_active_days != self.carnival_days:
            self.carnival_days = carnival_active_days
            self.carnival_data = {}
            mission_config = game_config.carnival_mission
            for mission_id, value in mission_config.iteritems():
                if value['days_old'] == server_carnival_days:
                    self.carnival_data[mission_id] = 0
                    # todo 自检数值类任务完成程度
                    mission_sort = value['sort']
                    if mission_sort in self.NEEDCHECKMISSIONID:
                        pass

        if save:
            self.save()

    def server_carvical_open(self, tp=1):
        server_days = get_server_days(self._server_name)
        config = game_config.carnival_days[tp]
        if tp == 1:
            start = int(config['open'].split(' ')[0])
            end = int(config['close'].split(' ')[0])
            if start <= server_days <= end:
                return server_days
            return 0
        elif tp == 2:
            start = str2timestamp(config['open'])
            end = str2timestamp(config['close'])
            now = int(time.time())
            if start <= now <= end:
                return timestamp_different_days(start, now) + 1
            return 0

    @property
    def server_arnival(self):
        if not hasattr(self, '_server_carnival'):
            self._server_carnival = ServerCarnival(self)
        return self._server_carnival

    @property
    def carnival_active(self):
        if not hasattr(self, '_carnival_active'):
            self._carnival_active = CarnivalActive(self)
        return self._carnival_active

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
        for k, value in self.server_carnival_data.iteritems():
            sort = game_config.liveness[k]['sort']
            if sort in kwargs:
                self.server_arnival.add_count(k, kwargs[sort])

        for k, value in self.carnival_data.iteritems():
            sort = game_config.achieve_mission[k]['sort']
            if sort in kwargs:
                self.carnival_active.add_count(k, kwargs[sort])

        self.save()


class ServerCarnival(object):
    def __init__(self, obj):
        """初始化
        """
        self.uid = obj.uid
        self.done = obj.server_carnival_done
        self.data = obj.server_carnival_data
        self.num = obj.server_dice_num
        self.config = game_config.carnival_mission

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

        # 任意艺人达到特定等级
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
            config = game_config.carnival_mission[mission_id]
            next_id = config['next_id']
            self.data[next_id] = self.data[mission_id]
            if config['sort'] == CARD_LEVEL:
                self.data[next_id] = []
                for k, v in self.mm.card.cards.iteritems():
                    if v['lv'] >= config['target'][0]:
                        self.data[next_id].append(k)
            self.data.pop(mission_id)


class CarnivalActive(object):
    def __init__(self, obj):
        """初始化
        """
        self.uid = obj.uid
        self.done = obj.carnival_done
        self.data = obj.carnival_data
        self.num = obj.dice_num
        self.config = game_config.carnival_mission

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

        # 任意艺人达到特定等级
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
            config = game_config.carnival_mission[mission_id]
            next_id = config['next_id']
            self.data[next_id] = self.data[mission_id]
            if config['sort'] == CARD_LEVEL:
                self.data[next_id] = []
                for k, v in self.mm.card.cards.iteritems():
                    if v['lv'] >= config['target'][0]:
                        self.data[next_id].append(k)
            self.data.pop(mission_id)
