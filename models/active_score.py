#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase, ModelTools
from lib.core.environ import ModelManager
from gconfig import game_config, MUITL_LAN
from lib.utils import weight_choice
from lib.utils.active_inreview_tools import get_version_by_active_id, active_inreview_open_and_close, \
    get_inreview_version
from lib.db import get_redis_client
from lib.utils import generate_rank_score, round_float_or_str
from lib.utils.time_tools import server_active_inreview_open_and_close

import settings

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
    return {target_sort_first: {'target1': type_hard, 'value': 1, 'stage_id': stage_id, },
            target_sort_num: {'target1': type_hard, 'value': 1, 'stage_id': stage_id, }, }


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
            target_sort_style: {'target1': script_id, 'end_lv': end_lv, 'value': 1,
                                'style': data['cur_script']['style']},
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

def card_gacha_times(hm, data, mission):
    return {mission._GACHA_TIMES: {'target1': 0, 'value': 1}}

def card_love_lvup(hm, data, mission):
    return {mission._LOVE_LVUP: {'target1': 0, 'value': 1}}


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
TOPINCOME = 28  # 单片最大票房次数


class ActiveScore(ModelBase):
    """
    老服活动积分活动
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
        'mission.get_reward': mission_num,  # 建筑任务
        # 'mission.get_reward': mission_args,                           # 成就
        'gacha.get_gacha': card_gacha_times,  # 艺人探寻
        'gacha.clear_gacha_cd': card_gacha_times,  # 艺人探寻
        'card.card_love_lvup': card_love_lvup,  # 卡牌提升羁绊

    }
    # mission_mapping

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
    _GACHA_TIMES = 32  # 艺人探寻次数
    _LOVE_LVUP = 33  # 艺人提升羁绊

    ACTIVE_TYPE = 2031

    def __init__(self, uid=''):
        self.uid = uid
        self._attrs = {
            'version': 0,  # 版本号
            'score_daily': 0,  # 每日积分
            'score_total': 0,  # 总积分
            'data': {},  # 任务数据
            'last_date': '',  # 最近登陆日期
            'got_reward_daily': [],  # 已领每日奖励
            'got_reward_total': [],  # 已领累充奖励
            'got_rank_reward': False
        }
        super(ActiveScore, self).__init__(self.uid)

    def pre_use(self):
        today = time.strftime('%F')
        version = self.get_version()
        save = False
        flag = self.send_mail_all()
        if flag:
            save = True
        if version > self.version:
            self.version = version
            self.score_total = 0
            self.got_reward_total = []
            self.data = self.get_data()
            self.got_rank_reward = False
        if version and today != self.last_date:
            self.send_mail_all(daily=True)
            self.last_date = today
            self.score_daily = 0
            self.got_reward_daily = []
            save = True
        if save:
            self.save()



    def get_data(self):
        return {mission_id: 0 for mission_id in
                         game_config.active_score.get(self.version, {}).get('mission', [])}

    def send_mail_all(self, daily=False):
        flag = False
        if not daily:
            if self.get_inreview():
                return False
            if not self.get_reward_total_red_dot() and self.got_rank_reward:
                return False
            if not self.got_rank_reward:
                flag = True
                rank = self.get_rank()
                if rank:
                    config_id = 0
                    for k, v in self.config_rank.iteritems:
                        if v['rank'][0] <= rank <= v['rank'][1] and self.version in v['active_id']:
                            config_id = k
                            break
                    if config_id:
                        lan = getattr(self.mm, 'lan', 1)
                        lan = MUITL_LAN[lan]
                        title = self.config_rank[config_id].get('title', '')
                        content = self.config_rank[config_id].get('content', '')
                        gift = self.config_rank[config_id]['award']
                        title = game_config.get_language_config(lan).get(title, '')
                        content = game_config.get_language_config(lan).get(content, '')
                        msg = self.mm.mail.generate_mail(content, title=title, gift=gift)
                        self.mm.mail.add_mail(msg)
                self.got_rank_reward = True
            if self.get_reward_total_red_dot():
                flag = True
                for step in self.get_reward_total_red_dot():
                    lan = getattr(self.mm, 'lan', 1)
                    lan = MUITL_LAN[lan]
                    title = self.config_score[self.version]['mail_title']
                    content = self.config_score[self.version]['mail']
                    gift = self.config_score[self.version]['award_total'][step - 1]
                    title = game_config.get_language_config(lan)[title]
                    content = game_config.get_language_config(lan)[content]
                    msg = self.mm.mail.generate_mail(content, title=title, gift=gift)
                    self.mm.mail.add_mail(msg)
                    self.got_reward_total.append(step)
        else:
            if self.get_reward_daily_red_dot():
                flag = True
                for step in self.get_reward_daily_red_dot():
                    lan = getattr(self.mm, 'lan', 1)
                    lan = MUITL_LAN[lan]
                    title = self.config_score[self.version]['mail_title']
                    content = self.config_score[self.version]['mail']
                    gift = self.config_score[self.version]['award_daily'][step - 1]
                    title = game_config.get_language_config(lan)[title]
                    content = game_config.get_language_config(lan)[content]
                    msg = self.mm.mail.generate_mail(content, title=title, gift=gift)
                    self.mm.mail.add_mail(msg)
                    self.got_reward_daily.append(step)
        if flag:
            self.mm.mail.save()
            return True
        return False

    @property
    def config(self):
        """任务配置"""
        return game_config.active_score_mission

    @property
    def config_score(self):
        """任务奖励配置"""
        return game_config.active_score

    @property
    def config_rank(self):
        return game_config.active_score_rank

    def get_version(self):
        a_id, version = get_version_by_active_id(active_id=self.ACTIVE_TYPE)
        return version

    def get_inreview(self):
        server_num = settings.get_server_num(self.mm.user._server_name)
        active_switch, _ = active_inreview_open_and_close(server_num=server_num)
        if self.ACTIVE_TYPE in active_switch:
            return True
        return False

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

        if hm.mm.user.config_type == 1:
            active_score = hm.mm.server_active_score
        else:
            active_score = hm.mm.active_score

        kwargs = cls._METHOD_FUNC_MAP[method](hm, data, active_score)
        if kwargs:

            if not active_score.get_version():
                return
            active_score.do_task(kwargs)

    def do_task(self, kwargs):
        for k, value in self.data.iteritems():
            sort = self.config[k]['sort']
            if sort in kwargs:
                self.add_count(k, kwargs[sort])
        self.save()

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
            if type_hard == target_data[0] and value['value'] > 0:
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

        else:
            if mission_id in self.data:
                self.data[mission_id] += value['value']
            else:
                self.data[mission_id] = value['value']

        # 判断任务是否完成 自动领奖
        if self.data[mission_id] >= target_data[1]:
            config = self.config[mission_id]
            self.score_daily += config['reward']
            self.score_total += config['reward']
            self.data[mission_id] = 0
            # 更新排行
            self.update_rank(self.score_total)

    @property
    def active_rank(self):
        server = 'public'
        return ActiveScoreRank(self.version, server)

    def update_rank(self, score):
        self.active_rank.add_rank(self.uid, score)

    def get_rank_all(self, start=0, end=-1, withscores=False):
        return self.active_rank.get_all_user(start=start, end=end, withscores=withscores)

    def get_score(self):
        return self.active_rank.get_score(self.uid)

    def get_rank(self):
        return self.active_rank.get_rank(self.uid)

    def get_reward_daily_red_dot(self):
        config = self.config_score.get(self.version, {}).get('need_daily', [])
        if not config:
            return []
        can_get_reward = [i for i, j in enumerate(config, 1) if self.score_daily >= j]
        return list(set(can_get_reward) - set(self.got_reward_daily))

    def get_reward_total_red_dot(self):
        config = self.config_score.get(self.version, {}).get('need_total', [])
        if not config:
            return []
        can_get_reward = [i for i, j in enumerate(config, 1) if self.score_total >= j]
        return list(set(can_get_reward) - set(self.got_reward_total))

    def get_reward_rank_red_dot(self):
        if self.get_version():
            return False
        return not self.got_rank_reward

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
            if star >= target[2] or target[3] == 1:
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


class ServerActiveScore(ActiveScore):
    """
    新服积分活动
    """
    ACTIVE_TYPE = 2032


    def get_data(self):
        return {mission_id: 0 for mission_id in
                         game_config.active_score_new.get(self.version, {}).get('mission', [])}

    @property
    def config(self):
        return game_config.active_score_mission_new

    @property
    def config_score(self):
        """任务奖励配置"""
        return game_config.active_score_new

    @property
    def config_rank(self):
        return game_config.active_score_rank_new

    def get_version(self):
        version, new_server, s_time, e_time = get_inreview_version(self.mm.user, self.ACTIVE_TYPE)
        return version

    def get_inreview(self):
        active_switch, _ = server_active_inreview_open_and_close(self.mm)
        if self.ACTIVE_TYPE in active_switch:
            return True
        return False

    @property
    def active_rank(self):
        server = self._server_name
        return ActiveScoreRank(self.version, server)


class ActiveScoreRank(ModelTools):
    def __init__(self, uid='', server='', *args, **kwargs):
        super(ActiveScoreRank, self).__init__()
        server_name = server
        pre_fix = '%s_%s' % (self.__class__.__name__, uid)
        self._key = self.make_key_cls(pre_fix, server_name=server_name)
        self.fredis = get_redis_client(settings.public)

    def add_rank(self, uid, score):
        """
        增加排名
        :param uid:
        :param rank:
        :return:
        """
        self.fredis.zadd(self._key, uid, generate_rank_score(score))
        self.fredis.expire(self._key, 7 * 24 * 3600)

    def del_rank(self, uid):
        """
        删除排名
        :param uid:
        :return:
        """
        self.fredis.zrem(self._key, uid)

    def get_all_user(self, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str):
        """
        获取排名所有玩家
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        return self.fredis.zrevrange(self._key, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_score(self, uid, score_cast_func=round_float_or_str):
        """
        获取积分
        :param uid:
        :return:
        """
        score = self.fredis.zscore(self._key, uid) or 0
        score = score_cast_func(score)

        return score

    def get_rank(self, uid):
        """
        获取排名
        :param uid:
        :return:
        """
        rank = self.fredis.zrevrank(self._key, uid)
        if rank is None:
            rank = -1
        return rank + 1


ModelManager.register_model('active_score', ActiveScore)
ModelManager.register_model('server_active_score', ServerActiveScore)
