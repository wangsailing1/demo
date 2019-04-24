#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice
from models.vip_company import task_cd

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


# # 推图
# def chapter_stage_args(hm, data, mission):
#     type_hard = hm.get_argument('type_hard', 0, is_int=True)
#     stage_id = data.get('stage_id', 0)
#     star = data.get('star', 0)
#     target_sort_first = mission._CHAPTER_FIRST
#     target_sort_num = mission._CHAPTER_NUM
#     return {target_sort_first: {'target1': type_hard, 'value': 1 if data.get('win', 0) else 0, 'stage_id': stage_id,
#                                 'star': star},
#             target_sort_num: {'target1': type_hard, 'value': 1 if data.get('win', 0) else 0, 'stage_id': stage_id,
#                               'star': star}, }

# 推图
def chapter_stage_args(hm, data, mission):
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    stage_id = data.get('stage_id', 0)
    target_sort_first = mission._CHAPTER_FIRST
    target_sort_num = mission._CHAPTER_NUM
    return {target_sort_first: {'target1': type_hard, 'value': 1 , 'stage_id': stage_id,},
            target_sort_num: {'target1': type_hard, 'value': 1 , 'stage_id': stage_id,},}

# 拍摄（type，style，income）
def script_make(hm, data, mission):
    script_id = data['cur_script']['id']
    end_lv = data['cur_script']['end_lv']
    target_sort_type = mission._SCRIPT_TYPE
    target_sort_style = mission._SCRIPT_STYLE
    target_sort_income = mission._INCOME
    target_limit_actor = mission._LIMIT_ACTOR
    target_once = mission._ONCE
    target_first_income = mission._FIRST_INCOME
    target_top_income = mission._TOPINCOME
    ids = [int(card_id.split('-')[0]) for card_id in data['cur_script']['card'].values()]
    return {target_sort_type: {'target1': script_id, 'end_lv': end_lv, 'value': 1},
            target_sort_style: {'target1': script_id, 'end_lv': end_lv, 'value': 1, 'style': data['cur_script']['style']},
            target_sort_income: {'target1': 0, 'end_lv': end_lv,
                                 'value': data['cur_script']['finished_summary']['income']},
            target_top_income: {'target1': data['cur_script']['finished_summary']['income'], 'end_lv': end_lv,
                                 'value': 1},
            target_limit_actor: {'target1': script_id, 'end_lv': end_lv, 'value': ids,
                                 'style': data['cur_script']['style']},
            target_once: {'target1': script_id, 'end_lv': end_lv,
                          'value': data['cur_script']['finished_summary']['income'],
                          'style': data['cur_script']['style']},
            target_first_income: {'target1': script_id, 'end_lv': end_lv, 'style': data['cur_script']['style'],
                                  'value': data['cur_script']['finished_first_income']['first_income']}, }


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
    gacha_id = hm.get_argument('gacha_id', is_int=True)
    reward = game_config.coin_gacha[gacha_id]['reward']
    target_sort = mission._CARD_GACHA
    num = len(data.get('reward', {}).get('cards', []))
    return {target_sort: {'target1': sort, 'value': count, 'info': reward, 'tp': 1},
            mission._CARD_NUM: {'target1': 0, 'value': num}}


# 抓娃娃
def get_toy(hm, data, mission):
    reward_id = hm.get_argument('reward_id', is_int=True)
    sort = hm.get_argument('sort', is_int=True)
    if sort == 1:
        config = game_config.rmb_gacha
    else:
        config = game_config.free_gacha
    card = []
    script = []
    if data['got']:
        gift = config[reward_id]['award']
        for item_id in gift:
            if item_id[0] in [8, 9]:  # 卡牌整卡，碎片
                card.append(item_id)
            elif item_id[0] == 15:
                script.append(item_id[1])
    target_card_sort = mission._CARD_GACHA
    target_script_sort = mission._SCRIPT_GACHA
    return {target_card_sort: {'target1': 0, 'value': 1, 'info': card, 'tp': 2},
            target_script_sort: {'target1': 0, 'value': 1, 'info': script, 'tp': 2}, }


# 抽剧本
def script_gacha(hm, data, mission):
    sort = hm.get_argument('sort', is_int=True)
    count = hm.get_argument('count', 1, is_int=True)
    target_sort = mission._SCRIPT_GACHA
    script_id = data['reward'].get('own_script', [])
    return {target_sort: {'target1': sort, 'value': count, 'info': script_id, 'tp': 1}}


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
    sort = data.get('sort', 2)
    return {mission._SHOP: {'target1': sort, 'value': 1}}


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


# 购买体力
def buy_point(hm, data, mission):
    mm = hm.mm
    return {mission._SHOP: {'target1': 1, 'value': 1}}

# 完成任务次数
def mission_num(hm, data, mission):
    mm = hm.mm
    tp_id = hm.get_argument('tp_id', 0, is_int=True)
    return {mission._MISSIONNUM: {'target1': tp_id, 'value': 1}}


# 建筑任务 所有建筑都通过models.user里的add_build完成，直接用装饰器对add_build处理
# def building(func):
#     def wrapper(*args, **kwargs):
#         mm = args[0].mm
#         if mm.mission.new_guide_data:
#             save = False
#             for mission_id in mm.mission.new_guide_data.keys():
#                 print mission_id
#                 try:
#                     build_id = args[1]
#                     group_id = game_config.building[build_id]['group']
#                     target = game_config.new_guide_mission[mission_id]['target']
#                     if group_id == target[0]:
#                         mm.mission.new_guide_data[mission_id] = 1
#                         save = True
#                 except:
#                     print 'building config is error'
#             if save:
#                 mm.mission.save()
#         return func(*args, **kwargs)
#     return wrapper

# 建筑任务
def build(hm, data, mission):
    mm = hm.mm
    group_id = data['group_id']
    return {mission._BUILD: {'target1': group_id, 'value': 1}}


# 约餐
def card_add_love_exp(hm, data, mission):
    items = hm.get_mapping_arguments('items')
    config = game_config.use_item
    data = {}
    for item_id, item_num in items:
        item_config = config[item_id]
        star = item_config['star']
        if star not in data:
            data[star] = item_num
        else:
            data[star] += item_num
    return {mission._DINNER: {'target1': 0, 'value': data}}

# 装备
def equip(hm, data, mission):
    equip_ids = hm.get_mapping_argument('equip_ids', num=0)
    config = game_config.equip
    data = {}
    for equip_id in equip_ids:
        equip_config = config[equip_id]
        star = equip_config['star']
        if star not in data:
            data[star] = 1
        else:
            data[star] += 1

    return {mission._EQUIP: {'target1': 0, 'value': data}}

# 处理公务
def business(hm, data, mission):
    return {mission._BUSINESS: {'target1': 0, 'value': 1}}


# =================================需要自检的数值类任务func=================================

# 玩家等级
def target_sort1(mm, mission_obj, target):
    value = mm.user.level
    return {mission_obj._PLAYER_LV: {'target1': 0, 'value': value}}


# 艺人等级
def target_sort2(mm, mission_obj, target):
    info = []
    for card_id, value in mm.card.cards.iteritems():
        if value['lv'] >= target[0]:
            info.append(card_id)
    return {mission_obj._CARD_LV: {'target1': 0, 'value': target[0], 'card_id': info}}

#
# # 关卡通关
# def target_sort7(mm, mission_obj, target):
#     config = game_config.chapter
#     chapter = 0
#     type_hard = 0
#     stage = 0
#     for value in config.values():
#         if target[0] in value['stage_id']:
#             chapter = value['num']
#             type_hard = value['hard_type']
#             stage = value['stage_id'].index(target[0]) + 1
#     info = stage in mm.chapter_stage.chapter.get(chapter, {}).get(type_hard, {})
#     info1 = mm.chapter_stage.chapter.get(chapter, {}).get(type_hard, {}).get(stage, {})
#     return {mission_obj._CHAPTER_FIRST: {'target1': type_hard, 'value': 1 if info else 0, 'stage_id': target[0],
#                                          'star': info1.get('star', 0)}}


# 关卡通关
def target_sort7(mm, mission_obj, target):
    config = game_config.chapter
    chapter = 0
    type_hard = 0
    stage = 0
    for value in config.values():
        if target[0] in value['stage_id']:
            chapter = value['num']
            type_hard = value['hard_type']
            stage = value['stage_id'].index(target[0]) + 1
    info = stage in mm.chapter_stage.chapter.get(chapter, {}).get(type_hard, {})
    info1 = mm.chapter_stage.chapter.get(chapter, {}).get(type_hard, {}).get(stage, {})
    return {mission_obj._CHAPTER_FIRST: {'target1': type_hard, 'value': 1 if info else 0, 'stage_id': target[0],
                                         }}


# 艺人数量
def target_sort15(mm, mission_obj, target):
    num = 0
    config = game_config.card_basis
    for card_id, value in mm.card.cards.iteritems():
        star = config[value['id']]['star_level']
        if star >= target[0]:
            num += 1
    return {mission_obj._CARD_NUM: {'target1': target[0], 'value': num}}


# 剧本数量
def target_sort16(mm, mission_obj, target):
    num = 0
    config = game_config.script
    for script_id in mm.script_book.scripts:
        if config[script_id]['star'] >= target[0]:
            num += 1
    return {mission_obj._SCRIPT_NUM: {'target1': target[0], 'value': num}}


# 公司市值
def target_sort19(mm, mission_obj, target):
    return {mission_obj._COMPANY_VALUE: {'target1': target[1], 'value': 1}}


# 艺人好感度
def target_sort23(mm, mission_obj, target):
    num = 0
    config = game_config.card_basis
    group_ids = []
    for card_id, value in mm.card.cards.iteritems():
        group_id = config[value['id']]['group']
        group_ids.append(group_id)
        if value['love_exp'] >= target[0]:
            num += 1
    for g_id in mm.card.attr:
        if g_id not in group_ids and mm.card.attr[g_id].get('like', 0) >= target[0]:
            num += 1
    return {mission_obj._ACTOR_LOVE: {'target1': target[0], 'value': num}}


# 建造任务
def target_sort26(mm, mission_obj, target):
    build_info = mm.user.group_ids
    info = target[0] in build_info
    return {mission_obj._BUILD: {'target1': target[0], 'value': 1 if info else 0}}


TYPE_MAPPING = {12: 'type', 14: 'style'}  # 剧本拍摄
MULT_TYPE = 22  # 剧本拍摄多要求
TYPE_STYLE = [24, 25]
CHANGE_NUM = [1, 19, 21, 15]  # 纯数值 玩家等级  公司市值
CARD_LEVEL = 2  # 艺人等级
FIRST_CHAPTER = 7  # 首次通关
NUM_CHAPTER = 8  # 通关次数
GACHA = [3, 4]
GACHA_MAPPING = {8: 1, 9: 2}  # 8整卡 9碎片
FANS_ACTIVITY = [10, 17]  # 粉丝活动，商店购物
BUILD = 26  # 建筑
MISSIONNUM = 27  # 任务完成次数
TOPINCOME = 28 # 单片最大票房次数
CONTRAST = [30, 31]  # 任务目标比较大小 返回的value {target1:0 ,value :{key:num}}


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
        'chapter_stage.chapter_stage_fight': chapter_stage_args,  # 通关
        'script.finished_summary': script_make,  # 剧本拍摄
        'chapter_stage.auto_sweep': chapter_stage_auto_args,  # 自动推图 增加通关次数
        'script_gacha.get_gacha': script_gacha,  # 抽剧本
        'gacha.receive': card_gacha,  # 抽卡
        'toy.get_toy': get_toy,  # 抓娃娃
        'card.card_level_up': card_lv,  # 艺人升级
        'friend.sent_gift': send_gift,  # 好友送礼
        'friend.sent_gift_all': send_gift,  # 一键送礼
        'fans_activity.activity': fans_activity,  # 粉丝活动
        'card.card_train': card_train,  # 卡牌训练
        'card.equip_piece_exchange': equip_piece_exchange,  # 装备碎片合成
        'card.card_quality_up': card_quality_up,  # 艺人格调提升
        'shop.buy': shop_args,  # 商店购买
        'shop.gift_buy': shop_args,  # 礼品商店购买
        'shop.resource_buy': shop_args,  # 资源商店购买
        'shop.mystical_buy': shop_args,  # 神秘商店购买
        'shop.period_buy': shop_args,  # 限时商店购买
        'user.buy_point': buy_point,  # 购买体力
        'fans_activity.unlock_activity': build,  # 建筑任务
        'user.build': build,  # 建筑任务
        'mission.get_reward': mission_num,  # 完成任务个数
        # 'mission.get_reward': mission_args,                           # 成就
        'business.handling': business,  # 处理公务
        'card.card_add_love_exp': card_add_love_exp,  # 约餐
        'card.set_equip': equip,  # 装备

    }
    # mission_mapping
    MISSIONMAPPING = {1: 'daily', 2: 'box_office', 3: 'guide', 4: 'randmission', 6: 'achieve_mission', 7: 'new_guide'}
    BOXOFFICEREFRESHTIME = '05:00:00'
    _need_diff = ('achieve_data')

    # 数值类任务初始化时需要自检的
    NEEDCHECKMISSIONID = [1, 2, 7, 15, 16, 19, 23, 26]

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
    _LIMIT_ACTOR = 22  # 自制艺人限制型
    _ACTOR_LOVE = 23  # 艺人好感度
    _ONCE = 24  # 单次自制票房
    _FIRST_INCOME = 25  # 首映票房/收视
    _BUILD = 26  # 建筑任务
    _MISSIONNUM = 27  # 完成任务次数
    _TOPINCOME = 28  # 单片最大收入
    _BUSINESS = 29  # 处理公务
    _EQUIP = 30  # 装备
    _DINNER = 31  # 约餐

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
            'achieve_done': [],
            'achieve_data': {},
            'achieve': 0,
            'new_guide_data': {},
            'new_guide_done': [],
            'performance': 0, # 业绩
            'performance_done': []  #

        }
        super(Mission, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        box_office_time = time.strftime('%T')
        is_save = False
        if self.get_achieve_mission():
            is_save = True
        if not self.new_guide_data and not self.new_guide_done:
            for i in range(1,4):
                self.new_guide_data[i] = 0
                self.check_new_guide_mission(i)
            is_save = True
        if self.get_all_random_mission():
            is_save = True
        if self.date != today:
            self.date = today
            self.daily_done = []
            self.daily_data = self.get_daily_mission()
            self.live_done = []
            self.liveness = 0
            self.refresh_times = 0
            self.performance = 0
            self.performance_done = []
            # if not self.guide_done and not self.guide_data:
            #     self.get_guide_mission()
            # if not self.achieve_done and not self.achieve_data:
            self.get_achieve_mission()
            is_save = True
        if self.mm.user.level >= 5 and not self.box_office_last_date:
            self.box_office_done = []
            self.box_office_last_date = today
            self.box_office_data = {self.get_box_office(): 0, 'time': int(time.time())} if self.get_box_office() else {}
            is_save = True

        if self.box_office_last_date != today and box_office_time >= self.BOXOFFICEREFRESHTIME and self.mm.user.level >= 5:
            self.box_office_done = []
            self.box_office_last_date = today
            self.box_office_data = {self.get_box_office(): 0, 'time': int(time.time())} if self.get_box_office() else {}
            is_save = True
        if int(time.time()) > self.box_office_data.get('time', 0) + game_config.common[57]:
            is_save = self.init_box_office()
        if is_save:
            self.save()

    def get_achieve_mission(self):
        own_group = []
        config = game_config.achieve_mission
        save = False
        for a_id in self.achieve_data:
            group_id = config.get(a_id,{}).get('group', 0)
            if group_id and group_id not in own_group:
                own_group.append(group_id)
        for a_id in self.achieve_done:
            group_id = config.get(a_id, {}).get('group', 0)
            if group_id and group_id not in own_group:
                own_group.append(group_id)

        for group, value in game_config.get_achieve_mission_mapping().iteritems():
            if group in own_group:
                continue
            if value['unlock_lvl'] > self.mm.user.level:
                continue
            self.achieve_data[min(value.keys())] = 0
            self.check_and_do_achive_mission(min(value.keys()))
            save= True
        return save

    # 获取成就目标id
    def get_achieve_id(self):
        config = game_config.achieve_mission
        for k, v in self.achieve_data.iteritems():
            if config[k]['sort'] == self._ACHIEVE:
                return k

    def get_daily_mission(self):
        config = game_config.liveness
        return {i: 1 if i == 1001 else 0 for i in config.keys()}

    def get_liveness_red_dot(self):
        config = game_config.liveness_reward
        for k, v in config.iteritems():
            need_liveness = v['need_liveness']
            if self.liveness >= need_liveness and k not in self.live_done:
                return True
        return False

    def get_performance_red_dot(self):
        config = game_config.random_reward
        for k, v in config.iteritems():
            need_liveness = v['need_random']
            if self.performance >= need_liveness and k not in self.performance_done:
                return True
        return False

    # 到时间刷新任务目标
    def init_box_office(self):
        config = game_config.box_office
        for m_id, value in self.box_office_data.iteritems():
            if isinstance(m_id, basestring) and 'time' in m_id:
                continue
            if value < config[m_id]['target1']:
                self.box_office_data[m_id] = 0
                self.box_office_data['time'] = int(time.time())
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

    @property
    def new_guide(self):
        if not hasattr(self, '_new_guide'):
            self._new_guide = NewGuideMission(self)
        return self._new_guide

    @property
    def achieve_mission(self):
        if not hasattr(self, '_achieve_mission'):
            self._achieve_mission = Achieve(self)
        return self._achieve_mission

    # 增加成就点
    def add_achieve_point(self, point, save=False):
        self.achieve += point
        # 完成成就任务
        a_id = self.get_achieve_id()
        self.achieve_data[a_id] = self.achieve
        if save:
            self.save()

    # 增加目标
    def add_liveness(self, point, save=False):
        self.liveness += point
        if save:
            self.save()

    # 增加业绩
    def add_performance(self, point, save=False):
        self.performance += point
        if save:
            self.save()

    def refresh_performance(self, mission_id, save=False):
        config = game_config.random_reward
        if not config:
            return
        if mission_id != max(config.keys()):
            return
        self.performance = 0
        self.performance_done = []
        if save:
            self.save()

    def get_all_random_mission(self):
        save = False
        if not self.random_data:
            for _ in xrange(4):
                while True:
                    mission_id = self.get_random_mission()
                    if mission_id in self.random_data:
                        continue
                    self.random_data[mission_id] = 0
                    break
                self.check_and_do_random_mission(mission_id)
                save = True
        else:
            now = int(time.time())
            del_dict = {}
            for k, v in self.random_data.iteritems():
                if isinstance(k, (str, unicode)) and 'refresh_ts' in k and now >= v + self.refresh_time():
                    while True:
                        mission_id = self.get_random_mission()
                        if mission_id in self.random_data or mission_id in del_dict:
                            continue
                        del_dict[mission_id] = k
                        break
                    save = True
            if del_dict:
                for add_key, del_key in del_dict.iteritems():
                    self.random_data.pop(del_key)
                    self.random_data[add_key] = 0
                    self.check_and_do_random_mission(add_key)
                    save = True
        return save

    def refresh_time(self):
        return self.RANDOMREFRESHTIME - task_cd(self.mm.user) * 60

    def refresh_random_misstion(self, mission_id, is_save=False):
        new_mission_id = mission_id
        while new_mission_id == mission_id or new_mission_id in self.random_data:
            new_mission_id = self.get_random_mission()
        self.random_data.pop(mission_id)
        self.random_data[new_mission_id] = 0
        self.refresh_times += 1
        self.check_and_do_random_mission(new_mission_id)
        if is_save:
            self.save()

    # 自检数值类新手引导任务是否完成
    def check_new_guide_mission(self, mission_id):
        config = game_config.new_guide_mission[mission_id]
        mission_sort = config['sort']
        if mission_sort in self.NEEDCHECKMISSIONID:
            func = globals()['target_sort%s' % mission_sort]
            target_data = config['target']
            kwargs = func(self.mm, self, target_data)
            self.do_task(kwargs)

    # 自检数值类随机任务是否完成
    def check_and_do_random_mission(self, mission_id):
        config = game_config.random_mission[mission_id]
        mission_sort = config['sort']
        if mission_sort in self.NEEDCHECKMISSIONID:
            func = globals()['target_sort%s' % mission_sort]
            target_data = config['target']
            kwargs = func(self.mm, self, target_data)
            self.do_task(kwargs)

    # 自检数值类成就任务是否完成
    def check_and_do_achive_mission(self, mission_id):
        config = game_config.achieve_mission[mission_id]
        mission_sort = config['sort']
        if mission_sort in self.NEEDCHECKMISSIONID:
            func = globals()['target_sort%s' % mission_sort]
            target_data = config['target']
            kwargs = func(self.mm, self, target_data)
            self.do_task(kwargs)

    def get_random_mission(self):
        config = game_config.random_mission
        pool = [[k, config[k]['weight']] for k in config.keys() if config[k]['unlock_lvl'] <= self.mm.user.level]
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

        for k, value in self.achieve_data.iteritems():
            config = game_config.achieve_mission[k]
            sort = config['sort']
            target_data = config['target']
            if sort in kwargs:
                if sort == 15:
                    func = globals()['target_sort%s' % sort]
                    kwargs.update(func(self.mm, self, target_data))
                self.achieve_mission.add_count(k, kwargs[sort])

        # for k, value in self.guide_data.iteritems():
        #     sort = game_config.guide_mission[k]['sort']
        #     if sort in kwargs:
        #         self.guide.add_count(k, kwargs[sort])

        for k, value in self.random_data.iteritems():
            if isinstance(k, (str, unicode)) and 'refresh_ts' in k:
                continue
            sort = game_config.random_mission[k]['sort']
            if sort in kwargs:
                self.randmission.add_count(k, kwargs[sort])

        for k, value in self.box_office_data.iteritems():
            if isinstance(k, basestring) and 'time' in k:
                continue
            sort = game_config.box_office[k]['sort']
            if sort in kwargs and sort == self._INCOME:
                self.box_office.add_count(k, kwargs[sort])

        for k, value in self.new_guide_data.iteritems():
            sort = game_config.new_guide_mission[k]['sort']
            if sort in kwargs:
                self.new_guide.add_count(k, kwargs[sort])
        self.save()


class DoMission(object):
    def __init__(self, obj):
        super(DoMission, self).__init__()
        self.uid = obj.uid
        self.done = obj.done
        self.data = obj.data
        self.num = obj.num
        self.days = obj.days
        self.config = obj.config

    def add_count(self, mission_id, value):

        target_data = self.config[mission_id]['target']
        if self.config[mission_id]['sort'] in TYPE_MAPPING:
            type = TYPE_MAPPING[self.config[mission_id]['sort']]
            if type == 'style':
                script_type = value['style']
            else:
                script_type = game_config.script[value['target1']][type]
            if (script_type == target_data[0] or not target_data[0]) and value['end_lv'] >= target_data[2]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        # 单次自制票房,首映票房/收视
        elif self.config[mission_id]['sort'] in TYPE_STYLE:
            script_type = game_config.script[value['target1']]['type']
            script_style = value['style']
            if script_type == target_data[0] and script_style == target_data[3] and \
                            value['end_lv'] >= target_data[2] and value['value'] >= target_data[4]:
                if mission_id in self.data:
                    self.data[mission_id] += 1
                else:
                    self.data[mission_id] = 1

        # 自制艺人限制型
        elif self.config[mission_id]['sort'] == MULT_TYPE:
            script_type = game_config.script[value['target1']]['type']
            script_style = value['style']
            if (script_type == target_data[0] or not target_data[0]) and (
                            script_style == target_data[3] or not target_data[3]) and \
                            value['end_lv'] >= target_data[2] and self.check_limit_actor(target_data[4],
                                                                                         value['value']):
                if mission_id in self.data:
                    self.data[mission_id] += 1
                else:
                    self.data[mission_id] = 1

        # 任意艺人达到特定等级
        elif self.config[mission_id]['sort'] == CARD_LEVEL:
            card_id = value['card_id']
            if isinstance(self.data[mission_id], int):
                self.data[mission_id] = []
            if isinstance(card_id, list):
                for card_oid in card_id:
                    if card_oid not in self.data[mission_id] and value['value'] >= target_data[0]:
                        self.data[mission_id].append(card_oid)
            else:
                if card_id not in self.data[mission_id] and value['value'] >= target_data[0]:
                    self.data[mission_id].append(card_id)

        elif self.config[mission_id]['sort'] == FIRST_CHAPTER:
            # if value['stage_id'] >= target_data[0] and value['value'] >= target_data[1] and value['star'] >= \
            #         target_data[2]:
            if value['stage_id'] >= target_data[0] and value['value'] >= target_data[1]:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] == NUM_CHAPTER:
            # star = value.get('star', 0)
            type_hard = value['target1']
            # if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
            if ((type_hard and type_hard == target_data[0]) or not type_hard) and value['value'] > 0:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']
        elif self.config[mission_id]['sort'] in GACHA:
            gacha_type = value['target1']
            info = value['info']
            tp = value['tp']  # 来源
            num = self.check_gacha(target_data, gacha_type, self.config[mission_id]['sort'], info, tp)
            if mission_id in self.data:
                self.data[mission_id] += num
            else:
                self.data[mission_id] = num
        elif self.config[mission_id]['sort'] in CHANGE_NUM:
            self.data[mission_id] = value['value']

        elif self.config[mission_id]['sort'] in FANS_ACTIVITY:
            num = 0
            if not target_data[0] or (target_data[0] and target_data[0] == value['target1']):
                num = value['value']
            if mission_id in self.data:
                self.data[mission_id] += num
            else:
                self.data[mission_id] = num
        # 建筑任务
        elif self.config[mission_id]['sort'] == BUILD:
            if target_data[0] and target_data[0] == value['target1']:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        # 完成任务次数
        elif self.config[mission_id]['sort'] == MISSIONNUM:
            if not target_data[0] or (target_data[0] and target_data[0] == value['target1']):
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']

        # 单片最大票房次数
        elif self.config[mission_id]['sort'] == TOPINCOME:
            if target_data[0] <= value['target1']:
                if mission_id in self.data:
                    self.data[mission_id] += value['value']
                else:
                    self.data[mission_id] = value['value']


        elif self.config[mission_id]['sort'] in CONTRAST:
            v = value['value']
            num_ = 0
            for target , num in v.iteritems():
                if target >= target_data[0]:
                    num_ += num

            if mission_id in self.data:
                self.data[mission_id] += num_
            else:
                self.data[mission_id] = num_

        else:
            if mission_id in self.data:
                self.data[mission_id] += value['value']
            else:
                self.data[mission_id] = value['value']

                # # 判断任务是否完成 自动领奖
                # if self.data[mission_id] >= target_data[1]:
                #     if mission_id in self.done.get(self.days, []) and not self.config[mission_id]['if_reuse']:
                #         return
                #     self.done.setdefault(self.days, []).append(mission_id)
                #     self.num += self.config[mission_id]['reward']
                #     self.data[mission_id] = 0


    # 判断抽卡与抽剧本
    def check_gacha(self, target, gacha_type, sort, info, tp):
        if sort == GACHA[0]:
            # config = game_config.coin_gacha[info]
            if (isinstance(target[4], int) and (not target[4] or target[4] == tp)) or (
                        isinstance(target[4], list) and tp in target[4]):
                if info[0][0] == 8:  # 整卡 道具类型
                    star = game_config.card_basis[info[0][1]]['star_level']
                    if star >= target[2] and (not target[3] or target[3] == GACHA_MAPPING[8]) and (
                                    gacha_type == target[0] or not target[0]):
                        return 1
                else:
                    star = game_config.card_piece[info[0][1]]['star']
                    if star >= target[2] and (not target[3] or target[3] == GACHA_MAPPING[9]) and (
                                    gacha_type == target[0] or not target[0]):
                        return 1
        else:
            script_id = info[0] if info else 0
            star = game_config.script.get(script_id, {}).get('star', 0)
            if star >= target[2]:
                return 1
        return 0

    # 判断自制艺人限制型任务
    def check_limit_actor(self, target, cards):
        data = {}
        if not target:
            return True
        for num, _target in enumerate(target, 1):
            data[num] = _target[3]
        for oid in cards:
            config = game_config.card_basis[int(oid)]
            sex = config['sex_type']
            profession_type = config['profession_type']
            profession_class = config['profession_class']
            for num, _target in enumerate(target, 1):
                if (sex == _target[0] or not _target[0]) and (profession_type == _target[1] or not _target[1]) and (
                                profession_class == _target[2] or not _target[2]):
                    data[num] -= 1
        for k, v in data.iteritems():
            if v > 0:
                return False
        return True


class Achieve(DoMission):
    def __init__(self, obj):
        """初始化
        """
        super(DoMission, self).__init__()
        self.mm = obj.mm
        self.uid = obj.uid
        self.done = obj.achieve_done
        self.data = obj.achieve_data
        self.config = game_config.achieve_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    # def add_count(self, mission_id, value):
    #
    #     if self.config[mission_id]['sort'] in TYPE_MAPPING:
    #         type = TYPE_MAPPING[self.config[mission_id]['sort']]
    #         target_data = self.config[mission_id]['target']
    #         script_type = game_config.script[value['target1']][type]
    #         if script_type == target_data[0] and value['end_lv'] >= target_data[2]:
    #             if mission_id in self.data:
    #                 self.data[mission_id] += value['value']
    #             else:
    #                 self.data[mission_id] = value['value']
    #
    #     # 任意艺人达到特定等级
    #     elif self.config[mission_id]['sort'] == CARD_LEVEL:
    #         # self.data[mission_id] = value['value']
    #         target_data = self.config[mission_id]['target']
    #         card_id = value['card_id']
    #         if isinstance(self.data[mission_id], int):
    #             self.data[mission_id] = []
    #         if card_id not in self.data[mission_id] and value['value'] >= target_data[0]:
    #             self.data[mission_id].append(card_id)
    #
    #     elif self.config[mission_id]['sort'] == FIRST_CHAPTER:
    #         target_data = self.config[mission_id]['target']
    #         if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
    #             if mission_id in self.data:
    #                 self.data[mission_id] += value['value']
    #             else:
    #                 self.data[mission_id] = value['value']
    #
    #     elif self.config[mission_id]['sort'] == NUM_CHAPTER:
    #         target_data = self.config[mission_id]['target']
    #         star = value.get('star', 0)
    #         type_hard = value['target1']
    #         if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
    #             if mission_id in self.data:
    #                 self.data[mission_id] += value['value']
    #             else:
    #                 self.data[mission_id] = value['value']
    #     elif self.config[mission_id]['sort'] in CHANGE_NUM:
    #         self.data[mission_id] = value['value']
    #
    #     else:
    #         if mission_id in self.data:
    #             self.data[mission_id] += value['value']
    #         else:
    #             self.data[mission_id] = value['value']

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)
            config = game_config.achieve_mission[mission_id]
            next_id = config['next_id']
            if next_id:
                self.data[next_id] = self.data[mission_id]
            if config['sort'] == CARD_LEVEL and next_id:
                self.data[next_id] = []
                for k, v in self.mm.card.cards.iteritems():
                    if v['lv'] >= config['target'][0]:
                        self.data[next_id].append(k)
            self.data.pop(mission_id)


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
        self.data.pop(mission_id)
        if next_id:
            self.data[next_id] = 0
            self.data['time'] = int(time.time())


class NewGuideMission(DoMission):
    def __init__(self, obj):
        super(DoMission, self).__init__()
        self.obj = obj
        self.uid = obj.uid
        self.done = obj.new_guide_done
        self.data = obj.new_guide_data
        self.config = game_config.new_guide_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)
            self.data.pop(mission_id)
            self.start_next(mission_id)

    def start_next(self, mission_id):
        next_id = self.config[mission_id]['next_id']
        if next_id and next_id not in self.data:
            self.data[next_id] = 0
            self.obj.check_new_guide_mission(next_id)


class MissionDaily(DoMission):
    def __init__(self, obj):
        super(DoMission, self).__init__()
        self.uid = obj.uid
        self.done = obj.daily_done
        self.data = obj.daily_data
        self.config = game_config.liveness

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)
            self.data.pop(mission_id)


class MissionGuide(DoMission):
    def __init__(self, obj):
        super(DoMission, self).__init__()
        self.uid = obj.uid
        self.done = obj.guide_done
        self.data = obj.guide_data
        self.config = game_config.guide_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def done_task(self, mission_id):
        """完成任务
        """
        if mission_id not in self.done:
            self.done.append(mission_id)
            self.data.pop(mission_id)


class MissionRandom(DoMission):
    def __init__(self, obj):
        super(DoMission, self).__init__()
        self.uid = obj.uid
        self.done = obj.random_done
        self.data = obj.random_data
        self.config = game_config.random_mission

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)

    def done_task(self, mission_id):
        """完成任务
        """
        now = int(time.time())
        # self.done.append(mission_id)
        for key in range(1, 5):
            refresh_key = '%s%s' % ('refresh_ts', key)
            if refresh_key not in self.data:
                break
        self.data[refresh_key] = now
        self.data.pop(mission_id)


ModelManager.register_model('mission', Mission)
