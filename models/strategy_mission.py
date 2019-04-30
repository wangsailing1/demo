# -*- coding: utf-8 –*-

import time
import datetime
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from tools.user import user_info
from lib.utils import weight_choice, not_repeat_weight_choice_2

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


class MissionTools(object):

    # 推图
    @staticmethod
    def chapter_stage_args(hm, data, mission):
        type_hard = hm.get_argument('type_hard', 0, is_int=True)
        stage_id = data.get('stage_id', 0)
        target_sort_first = mission._CHAPTER_FIRST
        target_sort_num = mission._CHAPTER_NUM
        return {target_sort_first: {'target1': type_hard, 'value': 1 , 'stage_id': stage_id,},
                target_sort_num: {'target1': type_hard, 'value': 1 , 'stage_id': stage_id,},}
    # 拍摄（type，style，income）
    @staticmethod
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
    @staticmethod
    def chapter_stage_auto_args(hm, data, mission):
        times = hm.get_argument('times', 1, is_int=True)
        type_hard = hm.get_argument('type_hard', 0, is_int=True)
        stage_id = data['stage_id']
        target_sort_num = mission._CHAPTER_NUM
        return {target_sort_num: {'target1': type_hard, 'value': times, 'stage_id': stage_id,
                                  'star': 1}, }

    # 抽卡
    @staticmethod
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
    @staticmethod
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
    @staticmethod
    def script_gacha(hm, data, mission):
        sort = hm.get_argument('sort', is_int=True)
        count = hm.get_argument('count', 1, is_int=True)
        target_sort = mission._SCRIPT_GACHA
        script_id = data['reward'].get('own_script', [])
        return {target_sort: {'target1': sort, 'value': count, 'info': script_id, 'tp': 1}}

    # 等级
    @staticmethod
    def user_lv(hm, data, mission):
        lv = hm.mm.user.level
        return {mission._PLAYER_LV: {'target1': lv, 'value': lv}}

    # 卡牌等级
    @staticmethod
    def card_lv(hm, data, mission):
        card_oid = hm.get_argument('card_oid')
        return {mission._CARD_LV: {'target1': 0, 'value': hm.mm.card.cards[card_oid]['lv'], 'card_id': card_oid}}

    # 好友送礼
    @staticmethod
    def send_gift(hm, data, mission):
        return {mission._FRIEND_GIFT: {'target1': 0, 'value': len(data['send_gift'])}}

    # 粉丝活动
    @staticmethod
    def fans_activity(hm, data, mission):
        activity_id = hm.get_argument('activity_id', 0, is_int=True)
        config = game_config.fans_activity[activity_id]
        group = config['groupid']
        return {mission._FANS_ACTIVITY: {'target1': group, 'value': 1}}

    # 艺人培养
    @staticmethod
    def card_train(hm, data, mission):
        is_dimaond = hm.get_argument('is_dimaond', is_int=True)
        return {mission._CARD_TRAIN: {'target1': is_dimaond + 1, 'value': 1}}

    # 武器合成
    @staticmethod
    def equip_piece_exchange(hm, data, mission):
        return {mission._EQUIP_COMPOSE: {'target1': 0, 'value': 1}}

    # 格调进阶
    @staticmethod
    def card_quality_up(hm, data, mission):
        return {mission._GROW: {'target1': 0, 'value': 1}}

    # 艺人数量
    @staticmethod
    def card_get(hm, data, mission):
        return {mission._CARD_NUM: {'target1': 0, 'value': len(hm.mm.card.cards)}}

    # 剧本数量
    @staticmethod
    def scrip_get(hm, data, mission):
        return {mission._SCRIPT_NUM: {'target1': 0, 'value': len(hm.mm.script.own_script)}}

    # 购物
    @staticmethod
    def shop_args(hm, data, mission):
        sort = data.get('sort', 2)
        return {mission._SHOP: {'target1': sort, 'value': 1}}

    # 剧本重写
    @staticmethod
    def script_rewrite(hm, data, mission):
        return {mission._SCRIPT_REWRITE: {'target1': 0, 'value': 1}}

    # 公司市值
    @staticmethod
    def compamy_value(hm, data, mission):
        v = 20
        return {mission._COMPANY_VALUE: {'target1': v, 'value': 1}}

    # 成就
    @staticmethod
    def mission_args(hm, data, mission):
        mm = hm.mm
        achieve = mm.mission.achieve
        return {mission._ACHIEVE: {'target1': 0, 'value': achieve}}

    # 购买体力
    @staticmethod
    def buy_point(hm, data, mission):
        mm = hm.mm
        return {mission._SHOP: {'target1': 1, 'value': 1}}

    # 完成任务次数
    @staticmethod
    def mission_num(hm, data, mission):
        mm = hm.mm
        tp_id = hm.get_argument('tp_id', 0, is_int=True)
        return {mission._MISSIONNUM: {'target1': tp_id, 'value': 1}}

    # 建筑任务
    @staticmethod
    def build(hm, data, mission):
        mm = hm.mm
        group_id = data['group_id']
        return {mission._BUILD: {'target1': group_id, 'value': 1}}

    # 约餐
    @staticmethod
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
    @staticmethod
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
    @staticmethod
    def business(hm, data, mission):
        return {mission._BUSINESS: {'target1': 0, 'value': 1}}

    # =================================需要自检的数值类任务func=================================

    # 玩家等级
    @staticmethod
    def target_sort1(mm, mission_obj, target):
        value = mm.user.level
        return {mission_obj._PLAYER_LV: {'target1': 0, 'value': value}}

    # 艺人等级
    @staticmethod
    def target_sort2(mm, mission_obj, target):
        info = []
        for card_id, value in mm.card.cards.iteritems():
            if value['lv'] >= target[0]:
                info.append(card_id)
        return {mission_obj._CARD_LV: {'target1': 0, 'value': target[0], 'card_id': info}}

    # 关卡通关
    @staticmethod
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
    @staticmethod
    def target_sort15(mm, mission_obj, target):
        num = 0
        config = game_config.card_basis
        for card_id, value in mm.card.cards.iteritems():
            star = config[value['id']]['star_level']
            if star >= target[0]:
                num += 1
        return {mission_obj._CARD_NUM: {'target1': target[0], 'value': num}}

    # 剧本数量
    @staticmethod
    def target_sort16(mm, mission_obj, target):
        num = 0
        config = game_config.script
        for script_id in mm.script_book.scripts:
            if config[script_id]['star'] >= target[0]:
                num += 1
        return {mission_obj._SCRIPT_NUM: {'target1': target[0], 'value': num}}

    # 公司市值
    @staticmethod
    def target_sort19(mm, mission_obj, target):
        return {mission_obj._COMPANY_VALUE: {'target1': target[1], 'value': 1}}

    # 艺人好感度
    @staticmethod
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
    @staticmethod
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

        奖励分为 战略合作，存储在此模块，调用 MissionStrategy 对象封装

        @property
        def daily(self):
            if not hasattr(self, '_strategy_mission'):
                self._strategy_mission = Strategy(self)
            return self._strategy_mission
        """
    # 接口名到内置函数的映射
    _METHOD_FUNC_MAP = {
        'chapter_stage.chapter_stage_fight': MissionTools.chapter_stage_args,  # 通关
        'script.finished_summary': MissionTools.script_make,  # 剧本拍摄
        'chapter_stage.auto_sweep': MissionTools.chapter_stage_auto_args,  # 自动推图 增加通关次数
        'script_gacha.get_gacha': MissionTools.script_gacha,  # 抽剧本
        'gacha.receive': MissionTools.card_gacha,  # 抽卡
        'toy.get_toy': MissionTools.get_toy,  # 抓娃娃
        'card.card_level_up': MissionTools.card_lv,  # 艺人升级
        'friend.sent_gift': MissionTools.send_gift,  # 好友送礼
        'friend.sent_gift_all': MissionTools.send_gift,  # 一键送礼
        'fans_activity.activity': MissionTools.fans_activity,  # 粉丝活动
        'card.card_train': MissionTools.card_train,  # 卡牌训练
        'card.equip_piece_exchange': MissionTools.equip_piece_exchange,  # 装备碎片合成
        'card.card_quality_up': MissionTools.card_quality_up,  # 艺人格调提升
        'shop.buy': MissionTools.shop_args,  # 商店购买
        'shop.gift_buy': MissionTools.shop_args,  # 礼品商店购买
        'shop.resource_buy': MissionTools.shop_args,  # 资源商店购买
        'shop.mystical_buy': MissionTools.shop_args,  # 神秘商店购买
        'shop.period_buy': MissionTools.shop_args,  # 限时商店购买
        'user.buy_point': MissionTools.buy_point,  # 购买体力
        'fans_activity.unlock_activity': MissionTools.build,  # 建筑任务
        'user.build': MissionTools.build,  # 建筑任务
        'mission.get_reward': MissionTools.mission_num,             # 完成任务个数
        'business.handling': MissionTools.business,                 # 处理公务
        'card.card_add_love_exp': MissionTools.card_add_love_exp,   # 约餐

    }
    # mission_mapping
    MISSIONMAPPING = {1: 'strategy_mission'}
    BOXOFFICEREFRESHTIME = '05:00:00'

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

    RANDOM_NUM = 5                      # 默认 5个 合作任务    # TODO 先写死5个, 后期走commen表
    QUICK_DONE = 1                      # 快速完成数量
    TITLE = 31410195                    # 升级后奖励邮件标题
    CONTENT = 31410196                  # 升级后奖励邮件内容

    GIFT_TITLE = 31411068               # 合作伙伴送礼邮件标题
    GIFT_CONTENT = 31411069             # 合作伙伴送礼邮件内容

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'day_str': '',              # 每日刷新时间
            'strategy_info': {},        # 合作信息
            'strategy_data': {},        # 任务数据
            'strategy_done': [],        # 已完成的任务记录
            'level': 1,                 # 合作等级
            'tacit': 0,                 # 默契值
            'point': 0,                 # 任务积分
            'ts': 0,                    # 合作开始时间
            'done_num': 0,              # 完成数量
            'all_done_reward': {},      # all 完成奖励
            'quick_done': 0,            # 快速完成
        }
        super(Mission, self).__init__(self.uid)

    def pre_use(self):
        is_save = False
        today = time.strftime('%F')
        if self.day_str != today:
            self.daily_fresh()
            self.day_str = today
            is_save = True
        if not self.strategy_data:
            self.fresh_strategy_mission()
            is_save = True
        if is_save:
            self.save()

    def daily_fresh(self):
        self.quick_done = 0
        uid1, uid2 = self.uid.split('_')
        mm1 = ModelManager(uid1)
        mm2 = ModelManager(uid2)
        strategy_info = {
            mm1.uid: user_info(mm1),
            mm2.uid: user_info(mm2),
        }
        # y_income = self.get_yesterday_income(mm1, mm2)
        # strategy_info[mm1.uid]['y_income'] = y_income[mm1.uid]
        # strategy_info[mm2.uid]['y_income'] = y_income[mm2.uid]
        self.strategy_info = strategy_info

    @staticmethod
    def get_yesterday():
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        return yesterday

    def get_yesterday_income(self, mm1=None, mm2=None):
        if not mm1 or not mm2:
            uid1, uid2 = self.uid.split('_')
            mm1 = ModelManager(uid1)
            mm2 = ModelManager(uid2)
        y_str = self.get_yesterday().strftime('%F')

        top_script1 = mm1.block.top_script.get(y_str, {})
        top_script2 = mm2.block.top_script.get(y_str, {})
        income1 = 0 if not top_script1 else sum([v['finished_summary']['income'] for v in top_script1.itervalues()])
        income2 = 0 if not top_script1 else sum([v['finished_summary']['income'] for v in top_script2.itervalues()])

        y_income = {
            mm1.uid: income1,
            mm2.uid: income2,
        }
        return y_income

    def start_strategy(self, mm1, mm2):
        """ 合作开始
        """
        strategy_info = {
            mm1.uid: user_info(mm1),
            mm2.uid: user_info(mm2),
        }
        # y_income = self.get_yesterday_income(mm1, mm2)
        # strategy_info[mm1.uid]['y_income'] = y_income[mm1.uid]
        # strategy_info[mm2.uid]['y_income'] = y_income[mm2.uid]
        self.strategy_info = strategy_info
        self.ts = int(time.time())
        self.point = 0
        self.done_num = 0

    def update_user_info(self, mm):
        self.strategy_info[mm.uid] = user_info(mm)

    def fresh_strategy_mission(self):
        """ 刷新战略任务
        """
        missions = game_config.get_strategy_mission_mapping().get(self.level, {})
        all_keys = [[k, v['weight']] for k, v in missions.iteritems()]
        all_num = len(all_keys)
        if self.RANDOM_NUM > all_num:
            mission_list = all_keys
        else:
            choice_list = not_repeat_weight_choice_2(all_keys, num=self.RANDOM_NUM)
            mission_list = [m[0] for m in choice_list]

        mission_data = {m_id: self.gener_mission_data(m_id) for m_id in mission_list}
        self.strategy_data = mission_data
        return mission_data

    def gener_mission_data(self, m_id):
        """ 生成单个任务数据
        """

        mission_dict = {
            'status': 0,
            'value': 0,
            'do_uid': [],
            'owner': '',
        }
        return mission_dict

    def add_done_num(self, task_id, num=1):
        """ 领取奖励做记录
        """
        self.point += num
        self.done_num += num
        self.strategy_done.append(task_id)

    def quick_done_func(self, task_id, uid):
        self.quick_done += 1
        self.strategy_data[task_id]['status'] = 3
        self.strategy_data[task_id]['quick_uid'] = uid
        self.add_done_num(task_id)

    def get_quik_done_times(self):
        """ 本日剩余快速完成次数
        """
        return max(self.QUICK_DONE - self.quick_done, 0)

    def add_tacit(self, num):
        self.tacit += num

    def lvl_up(self, next_lv):
        """ 升级
        """
        self.level = next_lv or self.get_next_lv()
        self.point = 0
        self.strategy_done = []
        self.fresh_strategy_mission()

    def get_next_lv(self):
        strategy_lv = game_config.strategy_lv
        return self.level +1 if self.level < max(strategy_lv.keys()) else 1

    # 获取成就目标id
    def get_strategy_id(self):
        config = game_config.strategy_mission
        for k, v in self.strategy_data.iteritems():
            if config[k]['sort'] == self._ACHIEVE:
                return k

    @property
    def strategy_mission(self):
        if not hasattr(self, '_strategy_mission'):
            self._strategy_mission = StrategyMission(self)
        return self._strategy_mission

    # 自检数值类随机任务是否完成
    def check_and_do_achive_mission(self, mission_id):
        config = game_config.strategy_mission[mission_id]
        mission_sort = config['sort']
        if mission_sort in self.NEEDCHECKMISSIONID:
            func = globals()['target_sort%s' % mission_sort]
            target_data = config['target']
            kwargs = func(self.mm, self, target_data)
            self.do_task(kwargs)

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
            mission = hm.mm.strategy.strategy_mission
            if not mission:
                return
            mission.do_task(kwargs, hm)

    def do_task(self, kwargs, hm=None):
        """ 做任务
        """
        hm_uid = hm.mm.uid if hm else ''
        is_save = 0
        for k, value in self.strategy_data.iteritems():
            if not value['owner']:      # 无主的任务不计数
                continue
            if value['status'] != 0:    # 完成的任务不计数
                continue
            sort = game_config.strategy_mission[k]['sort']
            if sort in kwargs:
                self.strategy_mission.add_count(k, kwargs[sort], hm_uid=hm_uid)
                is_save = 1
        if is_save:
            self.save()


class DoMission(object):
    def __init__(self, obj):
        super(DoMission, self).__init__()
        self.uid = obj.uid
        self.done = obj.done
        self.data = obj.data
        self.num = obj.num
        self.days = obj.days
        self.config = game_config.carnival_mission

    def add_count(self, mission_id, value, **kwargs):

        target_data = self.config[mission_id]['target']
        if self.config[mission_id]['sort'] in MissionTools.TYPE_MAPPING:
            type = MissionTools.TYPE_MAPPING[self.config[mission_id]['sort']]
            script_type = game_config.script[value['target1']][type]
            if (script_type == target_data[0] or not target_data[0]) and value['end_lv'] >= target_data[2]:
                self.add_times(mission_id, value['value'], **kwargs)

        # 单次自制票房,首映票房/收视
        elif self.config[mission_id]['sort'] in MissionTools.TYPE_STYLE:
            script_type = game_config.script[value['target1']]['type']
            script_style = value['style']
            if script_type == target_data[0] and script_style == target_data[3] and \
                            value['end_lv'] >= target_data[2] and value['value'] >= target_data[4]:
                self.add_times(mission_id, 1, **kwargs)

        # 自制艺人限制型
        elif self.config[mission_id]['sort'] == MissionTools.MULT_TYPE:
            script_type = game_config.script[value['target1']]['type']
            script_style = value['style']
            if (script_type == target_data[0] or not target_data[0]) and (
                            script_style == target_data[3] or not target_data[3]) and \
                            value['end_lv'] >= target_data[2] and self.check_limit_actor(target_data[4],
                                                                                         value['value']):
                self.add_times(mission_id, 1, **kwargs)

        # 任意艺人达到特定等级        # TODO 以后处理
        elif self.config[mission_id]['sort'] == MissionTools.CARD_LEVEL:
            card_id = value['card_id']

            task_data = self.data[mission_id].setdefault('data', [])
            if isinstance(card_id, list):
                for card_oid in card_id:
                    if card_oid not in self.data[mission_id] and value['value'] >= target_data[0]:
                        task_data.append(card_oid)
            else:
                if card_id not in self.data[mission_id] and value['value'] >= target_data[0]:
                    task_data.append(card_id)
            if len(task_data) != self.data[mission_id]['value']:
                self.set_value(mission_id, len(task_data), **kwargs)

        elif self.config[mission_id]['sort'] == MissionTools.FIRST_CHAPTER:
            if value['stage_id'] >= target_data[0] and value['value'] > target_data[1]:
                self.add_times(mission_id, value['value'], **kwargs)

        elif self.config[mission_id]['sort'] == MissionTools.NUM_CHAPTER:
            star = value.get('star', 0)
            type_hard = value['target1']
            # if type_hard == target_data[0] and star >= target_data[2] and value['value'] > 0:
            if ((target_data[0] and type_hard == target_data[0]) or not target_data[0]) and value['value'] > 0:
                self.add_times(mission_id, value['value'], **kwargs)

        elif self.config[mission_id]['sort'] in MissionTools.GACHA:
            gacha_type = value['target1']
            info = value['info']
            tp = value['tp']  # 来源
            num = self.check_gacha(target_data, gacha_type, self.config[mission_id]['sort'], info, tp)
            self.add_times(mission_id, num, **kwargs)

        elif self.config[mission_id]['sort'] in MissionTools.CHANGE_NUM:
            self.set_value(mission_id, value['value'], **kwargs)

        elif self.config[mission_id]['sort'] in MissionTools.FANS_ACTIVITY:
            if not target_data[0] or (target_data[0] and target_data[0] == value['target1']):
                self.add_times(mission_id, value['value'], **kwargs)

        # 建筑任务
        elif self.config[mission_id]['sort'] == MissionTools.BUILD:
            if target_data[0] and target_data[0] == value['target1']:
                self.add_times(mission_id, value['value'], **kwargs)

        # 完成任务次数
        elif self.config[mission_id]['sort'] == MissionTools.MISSIONNUM:
            if not target_data[0] or (target_data[0] and target_data[0] == value['target1']):
                self.add_times(mission_id, value['value'], **kwargs)

        # 单片最大票房次数
        elif self.config[mission_id]['sort'] == MissionTools.TOPINCOME:
            if target_data[0] <= value['target1']:
                self.add_times(mission_id, value['value'], **kwargs)

        elif self.config[mission_id]['sort'] == MissionTools.CONTRAST:
            v = value['value']
            num_ = 0
            for target , num in v.iteritems():
                if target >= target_data[0]:
                    num_ += num
            self.add_times(mission_id, num_, **kwargs)

        else:
            self.add_times(mission_id, value['value'], **kwargs)

    # 判断抽卡与抽剧本
    def check_gacha(self, target, gacha_type, sort, info, tp):
        if sort == MissionTools.GACHA[0]:
            # config = game_config.coin_gacha[info]
            if (isinstance(target[4], int) and (not target[4] or target[4] == tp)) or (
                        isinstance(target[4], list) and tp in target[4]):
                if info[0][0] == 8:  # 整卡 道具类型
                    star = game_config.card_basis[info[0][1]]['star_level']
                    if star > target[2] and (not target[3] or target[3] == MissionTools.GACHA_MAPPING[8]) and (
                                    gacha_type == target[0] or not target[0]):
                        return 1
                else:
                    star = game_config.card_piece[info[0][1]]['star']
                    if star > target[2] and (not target[3] or target[3] == MissionTools.GACHA_MAPPING[9]) and (
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

    def add_times(self, task_id, times=1, **kwargs):
        pass

    def set_value(self, task_id, times=1, **kwargs):
        pass


class StrategyMission(DoMission):
    def __init__(self, obj):
        """初始化
        """
        super(DoMission, self).__init__()
        self.uid = obj.uid
        self.done = obj.strategy_done
        self.data = obj.strategy_data
        self.config = game_config.strategy_mission

    def add_times(self, task_id, times=1, **kwargs):
        self.data[task_id]['value'] += 1
        target2 = self.config[task_id]['target2']
        if self.data[task_id]['value'] >= target2:
            self.data[task_id]['status'] = 1
            hm_uid = kwargs.get('hm_uid', '')
            if hm_uid and hm_uid not in self.data[task_id]['do_uid']:
                self.data[task_id]['do_uid'].append(hm_uid)

    def set_value(self, task_id, times=1, **kwargs):
        self.data[task_id]['value'] = times
        target2 = self.config[task_id]['target2']
        if self.data[task_id]['value'] >= target2:
            self.data[task_id]['status'] = 1
            hm_uid = kwargs.get('hm_uid', '')
            if hm_uid and hm_uid not in self.data[task_id]['do_uid']:
                self.data[task_id]['do_uid'].append(hm_uid)

    def get_count(self, mission_id):
        return self.data.get(mission_id, 0)


ModelManager.register_model_iids('strategy_mission', Mission)
