# -*- coding: utf-8 –*-

"""
Created on 2018-08-24

@author: sm
"""

import time
import copy
import random
import bisect
import itertools

from gconfig import game_config
from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import add_dict
from tools.gift import del_mult_goods


class CardLogic(object):
    def __init__(self, mm):
        self.mm = mm

    def card_level_up(self, card_oid):
        """卡牌升级

        :param card_oid:
        :return:
        """
        user = self.mm.user
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        if not card_dict:
            return 1, {}

        if card_dict['is_cold']:
            return 'error_card_cold', {}

        if user.coin <= 0:
            return 'error_coin', {}

        card_config = game_config.card_basis[card_dict['id']]
        if card_dict['lv'] >= card_config['lvmin']:
            return 2, {}        # 请升级格调等级

        level_config = game_config.card_level[card_dict['lv']]
        add_exp = min(user.coin, level_config['level_gold'])
        if user.coin < add_exp:
            return 'error_coin', {}

        if not card.add_card_exp(card_oid, add_exp, card_dict):
            return 3, {}

        card.save()
        user.deduct_coin(add_exp)
        user.save()

        return 0, {}

    def card_add_love_exp(self, card_oid, items):
        """卡牌羁绊经验

        :param card_oid:
        :param items: [[2, 1], [3, 2]]  [[item_id, item_num]]
        :return:
        """
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        card_config = game_config.card_basis[card_dict['id']]
        if not card_dict:
            return 1, {}

        if card_dict['is_cold']:
            return 'error_card_cold', {}

        item = self.mm.item
        add_gift_count = 0
        add_exp = 0
        add_love_gift_pro = []

        love_config = game_config.card_love_level[card_dict['love_lv']]
        gift_lv_max = love_config['gift_lv_max']
        for item_id, item_num in items:
            add_gift_count += item_num
            if item.get_item(item_id) < item_num:
                return 'error_item', {}
            item_config = game_config.use_item[item_id]
            # is_use 13 好感食物
            if item_config['is_use'] != 13:
                return 2, {}    # 道具类型不符

            for tp, num in item_config['use_effect']:
                # 好感经验
                if tp == 0:
                    add_exp += num
                else:
                    # 味道类型
                    if tp in card_config['love_gift_type']:
                        card_dict = card_dict or self.cards[card_oid]
                        info = card_dict['love_gift_pro'].setdefault(tp, {'exp': 0, 'lv': 1})
                        next_lv = info['lv']
                        if next_lv >= gift_lv_max:
                            return 4, {}  #赠送礼物已达上限，属性不再提升，请升级羁绊后再来

                        add_love_gift_pro.append((tp, num))

        gift_count = card_dict['gift_count'] + add_gift_count
        if gift_count > gift_lv_max:
            return 3, {}            # 超出送礼上限

        for item_id, item_num in items:
            item.del_item(item_id, item_num)
        for tp, num in add_love_gift_pro:
            card.add_love_gift_exp(card_oid, tp, num, card_dict=card_dict)

        # card_dict['gift_count'] = gift_count
        card_dict['love_exp'] += add_exp
        card_dict['love_exp'] = min(card_dict['love_exp'], love_config['exp'])
        card.save()
        item.save()

        return 0, {}

    def card_love_level_up(self, card_oid):
        """卡牌羁绊升级

        :param card_oid:
        :return:
        """
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        if not card_dict:
            return 1, {}

        if card_dict['is_cold']:
            return 'error_card_cold', {}

        card_config = game_config.card_basis[card_dict['id']]
        love_config = game_config.card_love_level[card_dict['love_lv']]
        if card_dict['love_exp'] < love_config['exp']:
            return 2, {}    # 经验不足，无法升级
        if card_dict['love_lv'] + 1 not in game_config.card_love_level:
            return 3, {}    # 已到最大等级

        star_lv_cost = love_config['star_cost']
        star_lv = card_config['star_level']

        lvs = [x[0] for x in star_lv_cost]
        cost_idx = bisect.bisect_left(lvs, star_lv)
        if cost_idx == len(lvs):
            cost_idx = -1

        cost_num = star_lv_cost[cost_idx][1]
        piece_id = card_config['piece_id']

        if card.get_piece(piece_id) < cost_num:
            return 'error_piece', {}
        card.del_piece(piece_id, cost_num)

        card_dict['love_lv'] += 1
        card.save()

        return 0, {}

    def card_quality_up(self, card_oid):
        """卡牌进阶/格调

        :param card_oid:
        :return:
        """
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        if not card_dict:
            return 1, {}

        if card_dict['is_cold']:
            return 'error_card_cold', {}

        card_config = game_config.card_basis[card_dict['id']]
        next_id = card_config['nextid']
        next_config = game_config.card_basis.get(next_id)
        if not next_config:
            return 2, {}

        if set(card_dict['equips']) != set(card_config['quality_cost']):
            return 3, {}    # 卡牌装备不足

        if card_dict['lv'] < card_config['lvmin']:
            return 4, {}    # 卡牌等级不足

        card_dict['equips'] = []
        card_dict['id'] = next_id
        card.save()

        return 0, {}

    def card_train(self, card_oid, pro_ids, is_diamond=0):
        """卡牌培训

        :param card_oid:
        :param pro_ids: [1,2,3] 属性类型， 三选二
        :return:
        """
        user = self.mm.user
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        if not card_dict:
            return 1, {}

        if card_dict['is_cold']:
            return 'error_card_cold', {}

        train_times = card_dict['train_times'] + 1
        train_config = game_config.card_train_cost.get(train_times)
        if not train_config:
            return 2, {}        # 已达到最大培养次数

        if is_diamond:
            cost = train_config['diamond_cost']
            if not user.is_diamond_enough(cost):
                return 'error_diamond', {}
            user.deduct_diamond(cost)
        else:
            cost = train_config['cost']
            rc, _ = del_mult_goods(self.mm, cost)
            if rc:
                return rc, {}

        # 随机二种属性加成
        random.shuffle(pro_ids)

        card_config = game_config.card_basis[card_dict['id']]
        train_grow = card_config['train_grow']
        idx = bisect.bisect_left([x[0] for x in train_grow], train_times)
        if idx == len(train_grow):
            return 2, {}
            # idx = -1
        train_grow_id = train_grow[idx][1]

        add_pros = {}
        cur_train_ext_pro = card_dict['train_ext_pro']
        train_grow_config = game_config.card_train_grow[train_grow_id]['pro_grow_train']

        for idx in pro_ids:
            pro_idx = idx - 1
            grow_add_pro = train_grow_config[pro_idx]
            if grow_add_pro:
                add_pro = random.randint(*grow_add_pro)
                cur_train_ext_pro[pro_idx] += add_pro
                add_pros[idx] = add_pro
                if len(add_pros) >= 2:
                    break

        card_dict['train_times'] = train_times
        card.save()
        user.save()
        return 0, {}

    def set_equip(self, card_oid, equip_ids):
        """穿装备
        :param card_oid:
        :param equip_ids:
        :return:
        """
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        if not card_dict:
            return 1, {}

        if card_dict['is_cold']:
            return 'error_card_cold', {}

        card_config = game_config.card_basis[card_dict['id']]
        cost = card_config['quality_cost']
        equip = self.mm.equip
        cur_equips = card_dict.setdefault('equips', [])
        for equip_id in equip_ids:
            if equip_id not in cost:
                return 4, {}        # 不是所需装备
            if equip_id in cur_equips:
                return 2, {}    # 已有此类装备
            if len(cur_equips) >= len(cost):
                return 3, {}    # 超出所需上限

            if not equip.get_equip(equip_id):
                return 'error_equip', {}

            equip.del_equip(equip_id, 1)
            cur_equips.append(equip_id)

        card.save()
        equip.save()
        return 0, {}

    def set_cold(self, card_oid, cold=False):
        """雪藏/解冻
        :param card_oid:
        :param equip_ids:
        :return:
        """
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        if not card_dict:
            return 1, {}
        group_id = self.mm.card.get_group_id_by_oid(card_oid)
        cost_like = 0
        # 取消雪藏 消耗点赞数
        if not cold:
            if self.mm.friend.check_actor(group_id):
                self.mm.friend.actors[group_id]['show'] = 1
            else:
                self.mm.friend.actors[group_id] = {'show':1,'chat_log':{}}
            star = game_config.card_basis[card_dict['id']]['star_level']
            cost_like = game_config.card_repick[star]['cost']

        else:
            if self.mm.friend.check_actor(group_id):
                self.mm.friend.actors[group_id]['show'] = 0
            else:
                self.mm.friend.actors[group_id] = {'show':0,'chat_log':{}}

        if cost_like:
            if not self.mm.user.is_like_enough(cost_like):
                return 'error_like', {}
            self.mm.user.deduct_like(cost_like)
            self.mm.user.save()

        card_dict['is_cold'] = cold
        card.save()
        return 0, {}

    def card_piece_exchange(self, card_id):
        """卡牌碎片合成
        :param card_id:
        :return:
        """
        card = self.mm.card
        if card.has_card_with_group_id(card_id):
            return 1, {}        # 已有此类艺人

        card_config = game_config.card_basis[card_id]
        piece_id = card_config['piece_id']
        cost = card_config['star_cost']
        print piece_id, card.pieces
        if card.get_piece(piece_id) < cost:
            return 'error_card_piece', {}

        card_id = card.add_card(card_id)
        card.del_piece(piece_id, cost)
        card.save()
        return 0, {'reward': {'cards': [card_id]}}

    def equip_piece_exchange(self, equip_piece_id, num=1):
        """装备碎片合成
        :param equip_piece_id:
        :return:
        """
        equip = self.mm.equip

        piece_config = game_config.equip_piece.get(equip_piece_id)
        if not piece_config:
            return 1, {}

        equip_id = piece_config['equip_id']
        cost = piece_config['use_num']
        print equip_id, equip.equip_pieces
        if equip.get_piece(equip_piece_id) < cost * num:
            return 'error_equip_piece', {}

        equip.add_equip(equip_id, num)
        equip.del_piece(equip_piece_id, cost * num)
        equip.save()
        reward = {}
        add_dict(reward.setdefault('equip', {}), equip_id, num)
        return 0, {'reward': reward}

    def equip_piece_auto_exchange(self):
        """装备碎片一键合成
        :param equip_piece_id:
        :return:
        """
        equip = self.mm.equip

        reward = {}
        for piece_id, num in equip.equip_pieces.items():
            piece_config = game_config.equip_piece[piece_id]

            equip_id = piece_config['equip_id']
            cost = piece_config['use_num']
            cur_num = equip.get_piece(piece_id)
            exchange_num = cur_num / cost
            if not exchange_num:
                continue

            equip.add_equip(equip_id, exchange_num)
            equip.del_piece(piece_id, cost * exchange_num)
            add_dict(reward.setdefault('equip', {}), equip_id, exchange_num)
        equip.save()
        return 0, {'reward': reward}

    def set_name(self, card_oid, name):
        card = self.mm.card
        card_dict = card.cards.get(card_oid)
        if not card_dict:
            return 1, {}
        card_dict['name'] = name
        card.save()
        return 0, {}





