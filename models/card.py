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

    CHAR_PRO_MAPPING = ['演技', '歌艺', '娱乐', '艺术', '气质', '动感']
    LOVE_GIFT_MAPPING = ['酸', '甜', '苦', '辣', '冰', '饮']
    ADD_VALUE_MAPPING = {1: 'like'}  # 策划添加新属性的时候添加
    # 策划配置的属性与 程序属性列表下标对应，配置表里从1开始计数，程序数组从0开始计数
    PRO_IDX_MAPPING = {i: i - 1 for i in xrange(1, 7)}

    _need_diff = ('cards', 'pieces')

    # 新用户给的卡牌
    INIT_CARDS = [1, 2, 3, 4, 5]

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'cards': {

            },
            'pieces': {

            },
            'attr': {}

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
    def generate_card(cls, card_id, card_config=None, lv=1, love_lv=0, love_exp=0, evo=0, star=0, mm=None):
        card_oid = cls._make_oid(card_id)
        card_config = card_config or game_config.card_basis[card_id]

        card_dict = {
            'popularity': 0,  # 人气

            'name': '',  # 卡牌名字
            'id': card_id,  # 配置id
            'oid': card_oid,  # 唯一id
            'is_cold': False,  # 是否雪藏

            'exp': 0,  # 经验
            'lv': lv,  # 等级

            'love_exp': love_exp,  # 羁绊经验、好感度
            'love_lv': love_lv,  # 羁绊等级
            'gift_count': 0,  # 礼物数量
            'equips': [],  # 装备id

            'evo': evo,
            'star': card_config.get('star_level', 1),
            '_source': mm.action if mm else '',  # 记录来源

            'train_times': 0,  # 培训次数
            'train_ext_pro': [0] * len(cls.PRO_IDX_MAPPING),  # 训练属性加成

            'love_gift_pro': {},  # 味觉   {pro_id: {'exp': 0, 'lv': )}}
            'style_pro': {},  # 擅长类型{pro_id: {'exp': 0, 'lv': )}}
            'style_income': {},  # 拍片类型票房
            'style_film_num': {}  # 拍片类型数量

        }
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
            v.setdefault('name', '')
            v.setdefault('popularity', 0)

            if 'train_times' not in v:
                v['train_times'] = 0
            if 'train_ext_pro' not in v:
                v['train_ext_pro'] = [0] * len(self.PRO_IDX_MAPPING)

            if 'love_exp' not in v:
                v['love_exp'] = 0
                v['love_lv'] = 0

            if 'gift_count' not in v:
                v['gift_count'] = 0

            if 'love_gift_pro' not in v:
                v['love_gift_pro'] = {}
            if 'equips' not in v:
                v['equips'] = []

            if 'style_pro' not in v:
                v['style_pro'] = {}

            if 'style_income' not in v:
                v['style_income'] = {}
            if 'style_film_num' not in v:
                v['style_film_num'] = {}

            v.setdefault('is_cold', False)

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

        if self.has_card_with_group_id(card_id):
            self.add_piece(card_config['piece_id'], card_config['star_giveback'])
            return True

        card_oid, card_dict = self.generate_card(card_id,
                                                 lv=init_lv,
                                                 evo=init_evo,
                                                 star=init_star,
                                                 love_lv=init_love_lv,
                                                 love_exp=init_love_exp,
                                                 mm=self.mm
                                                 )
        self.mm.card_book.add_book(group_id)
        self.mm.friend.new_actor(group_id,is_save=True)
        self.cards[card_oid] = card_dict
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
        if not self.has_hero(card_oid):
            return False

        self.cards.pop(card_oid)

        return True

    def get_card(self, card_oid, for_battle=False):
        """获取卡牌详情 """
        card_info = dict(self.cards[card_oid])
        cur_lv = card_info['lv']

        card_config = game_config.card_basis[card_info['id']]
        base_char_pro = card_config['char_pro']
        grow_id = card_config['lv_growid']
        grow_config = game_config.card_level_grow[grow_id]

        if cur_lv % 2:
            pro_grow_add = grow_config['pro_grow_odd']
        else:
            pro_grow_add = grow_config['pro_grow_even']

        # 格调加成
        char_pro = []
        for base_pro, grow_add_pro in itertools.izip(base_char_pro, pro_grow_add):
            # 只计算卡牌拥有的属性
            if base_pro > 0:
                char_pro.append(base_pro + grow_add_pro / 10000)
            else:
                char_pro.append(base_pro)

        # 羁绊属性加成, 所有属性加成百分比
        love_grow_config = game_config.card_love_grow[grow_id]
        grow_love = love_grow_config['grow_love']

        idx = bisect.bisect_left([x[0] for x in grow_love], card_info['love_lv'])
        if idx == len(grow_love):
            idx = -1
        add_percent = grow_love[idx][1]

        # 礼物属性加成
        for gift_id, info in card_info['love_gift_pro'].iteritems():
            gift_config = game_config.card_love_gift.get(info['lv'])
            if not gift_config:
                continue
            attr_id = game_config.card_love_gift_taste[gift_id]
            if base_char_pro[self.PRO_IDX_MAPPING[attr_id]] > 0:
                gift_attr = game_config.common.get(2, 10)
                char_pro[self.PRO_IDX_MAPPING[attr_id]] += gift_attr
                pass

        # 擅长剧本，角色  先读配置 以后有擅长培养了 再改
        card_info['tag_script'] = card_config['tag_script']
        card_info['tag_role'] = card_config['tag_role']

        char_pro = [x * add_percent / 100 if x > 0 else x for x in char_pro]
        char_pro = [math.ceil(i) for i in char_pro]
        card_info['char_pro'] = char_pro
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
        info = card_dict['love_gift_pro'].setdefault(gift_type, {'exp': 0, 'lv': 1})
        next_exp = info['exp'] + add_exp
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
        :return:
        """
        add_num = int(add_num)
        card_dict = card_dict or self.cards[card_oid]
        card_dict['popularity'] += add_num

    def add_value(self, card_id, add_value_config, is_save=False):
        """
        :param card_id: 传唯一id或者传group_id
        :param add_value_config: [[1,100],[2,200]]
        :param is_save: 
        :return: 
        """
        if isinstance(card_id, str) and '-' in card_id:
            card_config = game_config.card_basis
            group_id = card_config[int(card_id.split('-')[0])]['group']
        else:
            group_id = card_id
        add_value = {}
        for k, v in add_value_config:
            if group_id not in self.attr:
                self.attr[group_id] = {}
            attr = self.ADD_VALUE_MAPPING[k]
            self.attr[group_id][attr] = self.attr[group_id].get(attr, 0) + v
            add_value[attr] = add_value.get(attr, 0) + v
        if is_save:
            self.save()
        return add_value

    # 获取最佳艺人
    def get_better_card(self, num=5):
        card_info = self.cards
        for card_id, value in card_info:
            card_info[card_id]['max_income'] = sum(value['style_income'].values())
        card_list = sorted(card_info.items(), key=lambda x: sum(x[1]['style_income'].values()), reverse=True)
        if len(card_list) > num:
            card_list = card_list[:num]
        card_info = {i: j for i, j in card_list}
        return card_info


ModelManager.register_model('card', Card)
