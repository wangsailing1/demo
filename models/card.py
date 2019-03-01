# -*- coding: utf-8 –*-

"""
Created on 2018-08-24

@author: sm
"""

import time
import math
import copy
import bisect
import itertools

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import add_dict
from lib.core.environ import ModelManager

from gconfig import game_config
from gconfig import get_str_words
from models import vip_company


class Card(ModelBase):
    """卡牌类
    cards： 所有卡牌
        {'1-1535098928-2fMmYB':
            {'_source': '',
              'evo': 1,         # 品质、进阶
              'exp': 1,         # 经验
              'id': 1,          # 配置中的id
              'lv': 1,          # 等级
              'oid': '1-1535098928-2fMmYB', # 唯一id
              'star': 1
              }
          }
    pieces: {        # 卡牌碎片
       1: 100
    }
    attr:{group_id:{attr1:1,attr2:2}}
    """

    # CHAR_PRO_NAME = ['演技', '歌艺', '气质', '动感', '艺术', '娱乐']
    CHAR_PRO_NAME = ['performance', 'song', 'temperament', 'sports', 'art', 'entertainment']

    LOVE_GIFT_MAPPING = ['酸', '甜', '苦', '辣', '冰', '饮']
    ADD_VALUE_MAPPING = {1: 'like', 2: 'popularity'}  # 策划添加新属性的时候添加
    # 策划配置的属性与 程序属性列表下标对应，配置表里从1开始计数，程序数组从0开始计数
    PRO_IDX_MAPPING = {pro_id: pro_id - 1 for pro_id in xrange(1, len(CHAR_PRO_NAME) + 1)}
    CHAR_PRO_NAME_PRO_ID_MAPPING = {name: pro_id for pro_id, name in enumerate(CHAR_PRO_NAME, start=1)}
    RESTMAPPING = {1: 'physical', 2: 'mood'}


    _need_diff = ('cards', 'pieces', 'attr', 'training_room')

    # 新用户给的卡牌
    INIT_CARDS = [1, 2, 3, 4, 5]

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'cards': {

            },
            'pieces': {

            },
            'attr': {},
            'card_building_level': 1,
            'card_box': 0,
            'training_room': {
                1: {
                    'status': 0   # 0 表示可使用，1 表示训练完成，2 表示正在训练中
                },
            },
        }
        self._group_ids = {}
        super(Card, self).__init__(self.uid)

    @classmethod
    def _make_oid(cls, card_id):
        """ 生成英雄only id

        :param card_id:
        :return:
        """
        return '%s-%s-%s' % (card_id, int(time.time()), salt_generator())

    @classmethod
    def generate_card(cls, card_id, card_config=None, lv=1, love_lv=0, love_exp=0, evo=0, star=0, mm=None, popularity=0):
        card_oid = cls._make_oid(card_id)
        card_config = card_config or game_config.card_basis[card_id]

        card_dict = {
            'popularity': popularity,  # 人气

            'name': get_str_words('1', card_config['name']),  # 卡牌名字
            'id': card_id,  # 配置id
            'oid': card_oid,  # 唯一id
            'is_cold': False,  # 是否雪藏

            'exp': 0,  # 经验
            'lv': lv,  # 等级

            'love_exp': love_exp,  # 羁绊经验、好感度
            'love_lv': love_lv,  # 羁绊等级
            'gift_count': 0,  # 礼物数量
            'equips': [],  # 装备id
            'equips_used':{}, #升格调消耗掉的装备

            'evo': evo,
            'star': card_config.get('star_level', 1),
            '_source': mm.action if mm else '',  # 记录来源

            'train_times': 0,  # 培训次数
            'train_ext_pro': [0] * len(cls.PRO_IDX_MAPPING),  # 训练属性加成

            'love_gift_pro': {},  # 味觉   {pro_id: {'exp': 0, 'lv': }}
            'style_pro': {},  # 擅长类型{pro_id: {'exp': 0, 'lv': 0}}
            'style_income': {},  # 拍片类型票房
            'style_film_num': {},  # 拍片类型数量
            'type_income':{}, #拍片种类票房
            'type_film_num':{}, #拍片种类次数
            'physical': card_config.get('physical', 1),  # 体力
            'mood': card_config.get('mood', 1),   # 心情
            'health': card_config.get('health', 1),  # 健康
            'skill': {},  # 技能
            'skill_exp': 0,  # 技能经验
        }

        for style_id in game_config.script_style.keys():
            card_dict['style_pro'][style_id] = {'exp': 0, 'lv': 0}

        return card_oid, card_dict

    @property
    def group_ids(self):
        if len(self._group_ids) != len(self.cards):
            self._group_ids = {}
            for k, v in self.cards.iteritems():
                group = self.get_group_id_by_id(v['id'])
                self._group_ids[group] = k
        return self._group_ids

    @classmethod
    def get_group_id(cls, card_id):
        if isinstance(card_id, (unicode, str)) and '-' in card_id:
            return cls.get_group_id_by_oid(card_id)
        else:
            return cls.get_group_id_by_id(card_id)

    @classmethod
    def get_group_id_by_oid(cls, oid):
        """
        根据唯一id获取父id
        :param oid:
        :return:
        """
        cid = int(oid.split('-')[0])
        return game_config.card_basis[cid]['group']

    @classmethod
    def get_group_id_by_id(cls, cid):
        """
        根据配置id获取父id
        :param oid:
        :return:
        """
        cid = int(cid)
        return game_config.card_basis[cid]['group']

    def pre_use(self):
        if not self.cards:
            self.init_card()

        for k, v in self.cards.iteritems():
            card_config = game_config.card_basis[v['id']]
            if not v.get('name'):
                v['name'] = get_str_words('1', card_config['name'])
            if 'skill' not in v:
                v['skill'] = {}
                v['skill_exp'] = 0

        # 刷新训练室状态
        self.change_training_room_status(is_save=True)

    def init_card(self):
        return

        # TODO 暂时没配置，先随便给几张写死的卡牌
        if not self.cards:
            for i in self.INIT_CARDS:
                self.add_card(i)
            self.save()

    def get_piece(self, piece_id):
        """ 获取碎片数量

        :param piece_id:
        :return:
        """
        return self.pieces.get(piece_id, 0)

    def add_piece(self, piece_id, piece_num):
        """ 增加碎片

        :param piece_id:
        :param piece_num:
        :return:
        """
        piece_num = int(piece_num)
        add_dict(self.pieces, piece_id, piece_num)

    def del_piece(self, piece_id, piece_num):
        """ 删除碎片

        :param piece_id:
        :param piece_num:
        :return:
        """
        owned_num = self.get_piece(piece_id)
        if owned_num < piece_num:
            return False
        elif owned_num == piece_num:
            self.pieces.pop(piece_id)
        else:
            add_dict(self.pieces, piece_id, -piece_num)

        return True

    def add_card(self, card_id, lv=None, evo=None, love_lv=None, love_exp=None, star=None):
        """添加卡牌
        :param card_id:
        :param lv:
        :param evo:
        :param star:
        :return:
        """

        init_lv = lv or 1
        init_evo = evo or 0
        init_star = star or 0
        init_love_lv = love_lv or 0
        init_love_exp = love_exp or 0

        card_config = game_config.card_basis[card_id]
        group_id = card_config['group']
        if group_id not in self.attr:
            self.attr[group_id] = {}
        self.attr[group_id]['like'] = self.attr.get(group_id,{}).get('like', 0) + init_love_exp
        init_love_exp = self.attr.get(group_id, {})['like']
        popularity = self.attr.get(group_id,{}).get('popularity', 0)

        if self.has_card_with_group_id(card_id):
            self.add_piece(card_config['piece_id'], card_config['star_giveback'])
            return True

        card_oid, card_dict = self.generate_card(card_id,
                                                 lv=init_lv,
                                                 evo=init_evo,
                                                 star=init_star,
                                                 love_lv=init_love_lv,
                                                 love_exp=init_love_exp,
                                                 mm=self.mm,
                                                 popularity=popularity,
                                                 )

        self.mm.card_book.add_book(group_id)
        self.mm.friend.new_actor(group_id,is_save=True)
        self.cards[card_oid] = card_dict

        if lv != 1:
            self.unlock_skill(card_oid)

        return card_oid

    def has_card(self, card_oid):
        """ 是否有英雄

        :param card_oid:
        :return:
        """
        return card_oid in self.cards

    def has_card_with_group_id(self, hero_id):
        """ 通过card_id查找是否有英雄

        :param hero_id:
        :return:
        """
        card_config = game_config.card_basis.get(hero_id, {})
        group = card_config['group']
        if group in self.group_ids:
            return True

        return False

    def del_card(self, card_oid):
        """ 删除英雄

        :param card_oid:
        :return:
        """
        # if not self.has_hero(card_oid):
        #     return False

        self.cards.pop(card_oid)

        return True

    def get_card(self, card_oid,is_battle=False):
        """获取卡牌详情 """
        card_info = dict(self.cards[card_oid])
        battle_info = self.calc_card_battle_info(card_info)
        if is_battle:
            rest_effect = self.get_rest_effect(card_oid).values()
            for effect in rest_effect:
                battle_info['char_pro'] = [int(i * (effect + 100) / 100.0) for i in battle_info['char_pro']]
                battle_info['all_char_pro'] = [int(i * (effect + 100) / 100.0) for i in battle_info['all_char_pro']]
        return battle_info

    @classmethod
    def calc_card_battle_info(cls, card_info):
        """计算卡牌战斗数据"""
        cur_lv = card_info['lv']

        card_config = game_config.card_basis[card_info['id']]
        #count_lv 用于计算格调成长等级
        count_lv = cur_lv - card_config['last_lv']

        base_char_pro = card_config['char_pro']
        grow_id = card_config['lv_growid']
        grow_config = game_config.card_level_grow[grow_id]

        # 格调加成
        char_pro = []
        for idx, base_pro in enumerate(base_char_pro):
            # 只计算卡牌拥有的属性
            if base_pro > 0:
                lv_grow_add = 0
                # 公式确定后可以优化，只是奇偶数取不同列的话 复杂度可以做成常量的
                for lv in xrange(1, count_lv + 1):
                    if lv == 1 and not card_config['last_lv']:
                        continue
                    if lv % 2:
                        pro_grow_add = grow_config['pro_grow_odd'][idx]
                    else:
                        pro_grow_add = grow_config['pro_grow_even'][idx]

                    lv_grow_add += pro_grow_add / 10000.0
                char_pro.append(base_pro * (1 + lv_grow_add))
            else:
                char_pro.append(base_pro)

        # 羁绊属性加成, 所有属性加成万分比
        grow_id = card_config['love_growid']
        love_grow_config = game_config.card_love_grow[grow_id]
        grow_love = love_grow_config['grow_love']

        idx = bisect.bisect_left([x[0] for x in grow_love], card_info['love_lv'])
        if idx == len(grow_love):
            idx = -1
        add_percent = grow_love[idx][1]
        if card_info['love_lv'] == 0:
            add_percent = 0

        #武器加成
        equip_config = game_config.equip
        for equip_id in card_info['equips']:
            equip_attr = equip_config[equip_id]['add_attr']
            char_pro = [char_pro[i] + equip_attr[i] if char_pro[i] != -1 else -1 for i in range(6)]

        for _, value in card_info['equips_used'].iteritems():
            for equip_id in value:
                equip_attr = equip_config[equip_id]['add_attr']
                char_pro = [char_pro[i] + equip_attr[i] if char_pro[i] != -1 else -1 for i in range(6)]



        # 礼物属性加成
        for gift_id, info in card_info['love_gift_pro'].iteritems():
            gift_config = game_config.card_love_gift.get(info['lv'])
            if not gift_config:
                continue
            attr_id = game_config.card_love_gift_taste[gift_id]['attr']
            if base_char_pro[cls.PRO_IDX_MAPPING[attr_id]] > 0:
                gift_attr = game_config.common.get(2, 10)
                char_pro[cls.PRO_IDX_MAPPING[attr_id]] += gift_attr
                pass

        # 擅长剧本，角色  先读配置 以后有擅长培养了 再改
        card_info['tag_script'] = card_config['tag_script']
        card_info['tag_role'] = card_config['tag_role']

        all_char_pro = [char_pro[i] + card_info['train_ext_pro'][i] for i in range(6)]

        char_pro = [x * (1 + add_percent / 10000.0) if x > 0 else x for x in char_pro]
        all_char_pro = [x * (1 + add_percent / 10000.0) if x > 0 else x for x in all_char_pro]
        char_pro = [math.ceil(i) for i in char_pro]
        all_char_pro = [math.ceil(i) for i in all_char_pro]
        card_info['char_pro'] = char_pro
        card_info['all_char_pro'] = all_char_pro
        return card_info

    def card_tag(self, card_info):
        card_tag = {'tag_role': {},
                    'tag_script': {}}
        if not isinstance(card_info, dict):
            card_info = self.mm.card.get_card(card_info)
        tag_script = card_info.get('tag_script', [])
        tag_role = card_info.get('tag_role', [])
        for tag, value in tag_script:
            card_tag['tag_script'][tag] = value
        for tag, value in tag_role:
            card_tag['tag_role'][tag] = value
        return card_tag

    def add_card_exp(self, card_oid, add_exp, card_dict=None):
        """ 增加英雄经验

        :param hero_oid: 英雄only id
        :param add_exp: 增加的经验
        :return:
        """
        add_exp = int(add_exp)
        card_dict = card_dict or self.cards[card_oid]

        next_level = cur_level = card_dict['lv']
        next_exp = card_dict['exp'] + add_exp

        while 1:
            if next_level + 1 not in game_config.card_level:
                break
            need_exp = game_config.card_level[next_level]['exp']
            if next_exp >= need_exp:
                next_level += 1
                next_exp -= need_exp
                continue
            break

        card_dict['lv'] = next_level
        card_dict['exp'] = next_exp

        if cur_level != next_level:
            pass
        return True

    def add_love_gift_exp(self, card_oid, gift_type, add_exp, card_dict=None):
        card_dict = card_dict or self.cards[card_oid]
        info = card_dict['love_gift_pro'].setdefault(gift_type, {'exp': 0, 'lv': 1, 'all_exp': 0})
        next_exp = info['exp'] + add_exp
        info['all_exp'] += add_exp
        next_lv = info['lv']
        while 1:
            if next_lv + 1 not in game_config.card_love_gift:
                break
            config = game_config.card_love_gift[next_lv]
            if next_exp >= config['gift_exp']:
                next_lv += 1
                next_exp -= config['gift_exp']
                continue
            break

        love_config = game_config.card_love_level[card_dict['love_lv']]
        # 味道最大等级受羁绊等级约束
        if next_lv >= love_config['gift_lv_max']:
            next_exp = 0
            next_lv = love_config['gift_lv_max']
        info['lv'] = next_lv
        info['exp'] = next_exp

    def add_style_exp(self, card_oid, style_type, add_exp, card_dict=None):
        card_dict = card_dict or self.cards[card_oid]
        info = card_dict['style_pro'].setdefault(style_type, {'exp': 0, 'lv': 0})
        next_exp = info['exp'] + add_exp
        next_lv = info['lv']
        while 1:
            if next_lv + 1 not in game_config.card_script_exp:
                break
            config = game_config.card_script_exp[next_lv + 1]
            if next_exp >= config['exp']:
                next_lv += 1
                next_exp -= config['exp']
                continue
            break
        info['lv'] = next_lv
        info['exp'] = next_exp

    def add_card_love_exp(self, card_oid, add_exp, card_dict=None):
        """ 增加英雄羁绊经验

        :param hero_oid: 英雄only id
        :param add_exp: 增加的经验
        :return:
        """
        add_exp = int(add_exp)
        card_dict = card_dict or self.cards[card_oid]

        next_level = cur_level = card_dict['love_lv']
        next_exp = card_dict['love_exp'] + add_exp

        while 1:
            if next_level + 1 not in game_config.card_love_level:
                break
            need_exp = game_config.card_love_level[next_level]['exp']
            if next_exp >= need_exp:
                next_level += 1
                continue
            break

        card_dict['love_lv'] = next_level
        card_dict['love_exp'] = next_exp

        if cur_level != next_level:
            pass
        return True

    def add_card_popularity(self, card_oid, add_num, card_dict=None):
        """添加卡牌人气

        :param card_oid:
        :param num:
        :return::
        """
        if isinstance(card_oid, int):
            group_id = card_oid
            card_oid = self.group_ids[card_oid]
        else:
            group_id = self.get_group_id_by_oid(card_oid)
        add_num = int(add_num)
        card_dict = card_dict or self.cards[card_oid]
        card_dict['popularity'] += add_num
        self.attr[group_id]['popularity'] = card_dict['popularity']

    def is_enough_popularity(self, card_oid, add_num, card_dict=None):
        """卡牌人气是否足够

        :param card_oid:
        :param num:
        :return::
        """
        if isinstance(card_oid, int):
            card_oid = self.group_ids[card_oid]
        add_num = int(add_num)
        card_dict = card_dict or self.cards[card_oid]
        return card_dict['popularity'] >= add_num

    def delete_card_popularity(self, card_oid, add_num, card_dict=None):
        """删除卡牌人气

        :param card_oid:
        :param num:
        :return::
        """
        if isinstance(card_oid, int):
            group_id = card_oid
            card_oid = self.group_ids[card_oid]
        else:
            group_id = self.get_group_id_by_oid(card_oid)
        add_num = int(add_num)
        card_dict = card_dict or self.cards[card_oid]
        card_dict['popularity'] -= add_num
        self.attr[group_id]['popularity'] = card_dict['popularity']

    def add_value(self, card_id, add_value_config, is_save=False):
        """
        :param card_id: 传唯一id或者传group_id
        :param add_value_config: [[1,100],[2,200]]
        :param is_save: 
        :return: 
        """
        if isinstance(card_id, int):
            group_id = card_id
        else:
            card_config = game_config.card_basis
            group_id = card_config[int(card_id.split('-')[0])]['group']
        add_value = {}
        for k, v in add_value_config:
            if group_id not in self.attr:
                self.attr[group_id] = {}
            attr = self.ADD_VALUE_MAPPING[k]
            if group_id in self.group_ids:
                card_dict = self.cards[self.group_ids[group_id]]
                if k == 1:
                    card_dict['love_exp'] += v
                else :
                    card_dict[attr] += v
            self.attr[group_id][attr] = self.attr[group_id].get(attr, 0) + v
            add_value[attr] = add_value.get(attr, 0) + v
        if is_save:
            self.save()
        return add_value

    # 获取最佳艺人
    def get_better_card(self, num=5):
        card_info = self.cards
        for card_id, value in card_info.iteritems():
            card_info[card_id]['max_income'] = sum(value['style_income'].values())
        card_list = sorted(card_info.items(), key=lambda x: sum(x[1]['style_income'].values()), reverse=True)
        if len(card_list) > num:
            card_list = card_list[:num]
        card_info = {i: j for i, j in card_list}
        return card_info

    def get_can_use_card(self):
        can_use_card = []
        for card_id, value in self.cards.iteritems():
            if value['is_cold']:
                continue
            can_use_card.append(card_id)
        return can_use_card

    def can_add_new_card(self):
        return True
        # config = game_config.card_building
        # max_num = config[self.card_building_level]['card_limit']
        max_num = self.mm.user.build_effect.get(9, 10) + vip_company.card_max(self.mm.user)
        return max_num + self.card_box > len(self.get_can_use_card())

    def get_rest_effect(self,card_id):
        card_info = self.cards[card_id]
        effect = {}
        card_config = game_config.card_basis[card_info['id']]
        rest_config = game_config.rest
        for type, attr in self.RESTMAPPING.iteritems():
            num = card_info[attr]
            max_num = card_config[attr]
            rate = int(num * 100 / max_num)
            print rate
            for _ ,value in rest_config.iteritems():
                if value['type'] == type and value['rank'][0] <= rate <= value['rank'][1]:
                    effect[attr] = value['effect']
                    break
        return effect

    def get_all_rest_card(self):
        info = {}
        for card in self.mm.rest_restaurant.get_rest_cards():
            info[card] = 1
        for card in  self.mm.rest_bar.get_rest_cards():
            info[card] = 2
        for card in self.mm.rest_hospital.get_rest_cards():
            info[card] = 3
        return info

    def unlock_skill(self, card_oid, is_save=False):
        card_info = self.cards[card_oid]
        card_id = card_info['id']
        lv = card_info['lv']
        skills = card_info['skill']
        unlock_config = game_config.card_skill_unlock
        skill_list = game_config.card_basis[card_id]['skill']

        for id in range(1, len(skill_list)+1):
            if skill_list[id-1] in skills:
                continue

            unlock_lv = unlock_config[id]['lv']
            if lv >= unlock_lv:
                skills[skill_list[id-1]] = {'lv': 1}

        if is_save:
            self.save()

    def change_training_room_status(self, is_save=False):
        training_room = self.training_room
        build_effect = self.mm.user.build_effect.get(11)
        if not build_effect:
            return

        for key, info in training_room.items():
            status = info.get('status')

            if info.get('start_train_time'):
                info.pop('start_train_time')
                info['status'] = 0
                status = 0

            if status == 2:
                end_train_time = info['end_train_time']  # 时间戳
                remain_time = end_train_time - int(time.time())
                if remain_time <= 0:
                    info['status'] = 1

        if is_save:
            self.save()

    def choice_train_card(self):
        result = []
        training_card_list = []
        for training_info in self.training_room.values():
            if training_info['status'] == 0:
                continue
            training_card_list.append(training_info['card_oid'])

        for card_oid, card_info in self.cards.items():
            if card_oid in training_card_list:
                continue

            if self.is_all_max_lv(card_oid):
                continue

            result.append(card_oid)

        return {'card_oid': result}

    def is_all_max_lv(self, card_oid):
        card_info = self.cards[card_oid]
        card_id = card_info['id']
        skill_list = game_config.card_basis[card_id]['skill']
        unlock_skill_list = card_info['skill'].keys()

        if set(skill_list) != set(unlock_skill_list):
            return False

        result = True
        for skill_id, skill_info in card_info['skill'].items():
            max_lv = game_config.card_skill[skill_id]['skill_maxlv']
            if skill_info['lv'] != max_lv:
                result = False

        return result


    def is_skill_exp_enough(self, card_oid, extra_exp=0):
        card_info = self.cards[card_oid]
        card_id = card_info['id']
        skill_list = game_config.card_basis[card_id]['skill']
        skill_exp_info = game_config.card_skill_level
        skill_exp = card_info['skill_exp']
        need_skill_exp = 0

        for skill_id in skill_list:
            skill_info = card_info['skill'].get(skill_id)
            if skill_info:
                skill_lv = skill_info['lv']
            else:
                skill_lv = 1
            max_lv = game_config.card_skill[skill_id]['skill_maxlv']
            quality = game_config.card_skill[skill_id]['quality']
            for lv in range(skill_lv, max_lv):
                skill_up_exp = skill_exp_info[lv]['exp'][quality - 1]
                need_skill_exp += skill_up_exp

        if need_skill_exp <= skill_exp + extra_exp:
            return True
        else:
            return False

    def get_end_train_time(self, start_time_stamp):
        build_effect = self.mm.user.build_effect[11]
        training_times = game_config.common[87] * 60 - build_effect[0]
        end_train_time = start_time_stamp + training_times
        return int(end_train_time)

    def is_match_single_condition(self, condition, align_list, script_id, role_id):
        '''
        :param condition: 单个条件，如[1, 0]
        :param align_list: [group_id1, group_id2, ...]  队友（可以包括自身）的组id列表
        :param script_id: 剧本id
        :param role_id: 角色id
        '''
        condition_type = condition[0]
        condition_id = condition[1]
        script = game_config.script[script_id]
        script_type = script['type']
        script_tag = script['tag_script']
        role = game_config.script_role[role_id]
        role_sex = role['sex_type']
        role_profession_class = role['profession_class']
        role_profession_type = role['profession_type']
        role_tag = role['tag_role']

        _dict = {
            1: 0,
            2: align_list,
            3: script_type,
            4: role_sex,
            5: role_profession_class,
            6: role_profession_type,
            7: script_tag,
            8: role_tag,
        }

        if condition_type in [2, 7, 8] and condition_id in _dict[condition_type]:
            return True
        if condition_type in [1, 3, 4, 5, 6] and condition_id == _dict[condition_type]:
            return True

        return False

    def is_skill_active(self, skill_id, model_type, align_list, script_id, role_id):
        '''
        :param skill_id: 技能id
        :param model_type: 系统id，1歌王、2粉丝活动、3自制拍摄、4艺人养成
        :param align_list: 队友（包括自己）组id列表
        :param script_id: 剧本id
        :param role_id: 技能所有者角色id
        :return: True|False
        '''
        skill_info = game_config.card_skill[skill_id]
        if model_type not in skill_info['triggersystem']:
            return False
        triggercondition_logic = skill_info.get('triggercondition_logic')
        if not triggercondition_logic:
            condition = skill_info['triggercondition'][0]
            return self.is_match_single_condition(condition, align_list, script_id, role_id)

        if triggercondition_logic == 1:
            for condition in skill_info['triggercondition']:
                if not self.is_match_single_condition(condition, align_list, script_id, role_id):
                    return False
            return True

        for condition in skill_info['triggercondition']:
            if self.is_match_single_condition(condition, align_list, script_id, role_id):
                return True
        return False

    def get_single_skill_effect(self, skill_id, self_card_oid, model_type, card_oid_list, script_id, role_id):
        '''
        :param skill_id: 技能id
        :param self_card_oid: 技能所有者卡牌唯一id
        :param model_type: 系统id，1歌王、2粉丝活动、3自制拍摄、4艺人养成
        :param card_oid_list: 队友（包括自己）的卡牌唯一id列表
        :param script_id: 剧本id
        :param role_id: 技能所有者角色id
        :return: {
            'skilltype': list  # 技能效果类型
            'skilltarget_oid': {
                'card_oid': {
                    3: 10,  # 效果类型和提升的数值（乘法的百分比已经被换算成了增加的点数）
                    5: 13,
                },  # 这里只有效果类型只有1-6, 大于6的类型留给非卡牌属性值的增益，如最终拍片收益的增长等
                ...
            }  # 技能影响的卡牌和效果值
            'computing_method': int  # 效果计算方法
            'skilllevel_value': int  # 技能效果数值
        }
        '''
        align_list = []
        card_oid_dict = {}
        for card_oid in card_oid_list:
            card_id = self.cards[card_oid]['id']
            card_group_id = game_config.card_basis[card_id]['group']
            align_list.append(card_group_id)
            card_oid_dict[card_oid] = card_group_id

        if not self.is_skill_active(skill_id, model_type, align_list, script_id, role_id):
            return {}

        skill_info = game_config.card_skill[skill_id]

        result = {}
        result['skilltype'] = skill_info['skilltype']
        result['computing_method'] = skill_info['computing_method']
        skill_lv = self.cards[self_card_oid]['skill'][skill_id]['lv']
        result['skilllevel_value'] = skill_info['skilllevel_value'][skill_lv-1]
        result['skilltarget_oid'] = {}
        type = skill_info['skilltarget_type']
        skilltarget_oid_list = []
        if type == 1:
            skilltarget_oid_list = card_oid_list
        elif type == 3:
            skilltarget_oid_list = [self_card_oid]
        elif type == 2:
            for card_oid, group_id in card_oid_dict:
                if group_id in skill_info['skilltarget_id']:
                    skilltarget_oid_list.append(group_id)
            if not skilltarget_oid_list:
                return {}

        for target_oid in skilltarget_oid_list:
            result['skilltarget_oid'][target_oid] = {}
            all_char_pro = self.mm.card.get_card(target_oid)['all_char_pro']
            for skilltype in skill_info['skilltype']:
                if skilltype > 6 or all_char_pro[skilltype-1] == -1:
                    continue
                if skill_info['computing_method'] == 1:
                    result['skilltarget_oid'][target_oid][skilltype] = result['skilllevel_value']
                else:
                    real_value = math.ceil(all_char_pro[skilltype - 1] * result['skilllevel_value'] / 10000)
                    result['skilltarget_oid'][target_oid][skilltype] = real_value

        return result

    def get_skill_effect(self, align, model_type, script_id):
        '''
        :param align: {
            card_oid1: role_id1,
            card_oid2: role_id2,
            ...
        }  阵型，key为card_oid，value为角色id
        :param model_type: 系统id，1歌王、2粉丝活动、3自制拍摄、4艺人养成
        :param script_id: 剧本id
        :return:
        {
            card_oid1: {
                effect: {
                    1: 10,
                    3: 20,
                    5: 23,
                },  # 该卡牌受所有生效技能影响后，最终类型值的增加值，这里只有类型只有1-6
                    # 大于6的类型留给非卡牌属性值的增益，如最终拍片收益的增长等
                skill: {
                    skill_id1: {
                        'skilltype': list  # 技能效果类型
                        'skilltarget_oid': {
                            'card_oid': {
                                3: 10,  # 效果类型和提升的数值（乘法的百分比已经被换算成了增加的点数）
                                5: 13,
                            }  # 这里只有效果类型只有1-6
                            ...
                        }  # 技能影响的卡牌和效果值
                        'computing_method': int  # 效果计算方法
                        'skilllevel_value': int  # 技能效果数值
                    },
                    skill_id2: {
                    ...
                    },
                    ...
                }
            },
            card_oid2: {
            ...
            }

        }
        '''
        result = {}
        total_effect = {}
        card_oid_list = align.keys()
        for card_oid, role_id in align.iteritems():
            skill_id_list = self.cards[card_oid]['skill'].keys()
            result[card_oid] = {}
            result[card_oid]['skill'] = {}
            for skill_id in skill_id_list:
                data = self.get_single_skill_effect(skill_id, card_oid, model_type, card_oid_list, script_id, role_id)
                result[card_oid]['skill'][skill_id] = data
                if not data:
                    del result[card_oid]['skill'][skill_id]
                    continue
                for target_oid, effect in data['skilltarget_oid'].iteritems():
                    if target_oid not in total_effect:
                        total_effect[target_oid] = {}
                    for type, value in effect.items():
                        total_effect[target_oid][type] = total_effect[target_oid].get(type, 0) + value
            if not result[card_oid]['skill']:
                del result[card_oid]['skill']

        for card_oid, effect in total_effect.iteritems():
            if effect:
                result[card_oid]['effect'] = effect

        for card_oid in card_oid_list:
            if not result[card_oid]:
                del result[card_oid]

        return result

ModelManager.register_model('card', Card)