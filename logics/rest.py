# -*- coding: utf-8 –*-

import time
from gconfig import game_config


class Rest(object):
    MAPPING = {1: 'rest_restaurant', 2: 'rest_bar', 3: 'rest_hospital'}
    ATTRMAPPING = {1: 'physical', 2: 'mood', 3: 'health'}
    SORTCOMMONMAPING = {1: 83, 2: 84, 3: 85}

    def __init__(self, mm=None, sort=1):
        self.mm = mm
        self.obj = getattr(self.mm, self.MAPPING[sort])
        self.attrtype = self.ATTRMAPPING[sort]
        self.sort = sort

    def rest_index(self):
        build_id = self.obj.get_build_id()
        if not build_id:
            return 17, {}  # 尚未拥有建筑
        data = {}
        data['extra_pos'] = self.obj.extra_pos
        data['max_pos'] = self.obj.get_max_pos()
        data['log'] = self.obj.rest_log

        return 0, data

    def card_rest(self, pos, card):
        if pos > self.obj.get_max_pos():
            return 11, {}  # 位置尚未开启
        if self.obj.rest_log.get(pos, {}):
            return 12, {}  # 位置有艺人休息中
        if card not in self.mm.card.cards:
            return 13, {}  # 未拥有此卡牌
        if card in self.mm.rest_restaurant.get_rest_cards():
            return 14, {}  # 卡牌已在餐厅中
        if card in self.mm.rest_bar.get_rest_cards():
            return 15, {}  # 卡牌已在酒吧中
        if card in self.mm.rest_hospital.get_rest_cards():
            return 16, {}  # 卡牌已在医院中
        if card in self.mm.fans_activity.get_fans_cards():
            return 20, {}  # 卡牌正在进行粉丝活动
        if card in self.mm.script.get_used_cards():
            return 21, {}  # 卡牌正在拍摄中
        build_id = self.obj.get_build_id()
        if not build_id:
            return 17, {}  # 尚未拥有建筑
        card_info = self.mm.card.cards[card]
        if card_info['health'] <= 0 and self.sort != 3:
            return 22, {}  # 艺人健康值不足
        card_config = game_config.card_basis[card_info['id']]
        max_num = card_config[self.attrtype]
        now_num = card_info.get(self.attrtype, 0)
        if now_num >= max_num:
            return 19, {}  # 艺人状态良好，不需休息
        recover_time_type = '%s_%s' % (self.attrtype, 'recovery')
        cost_type = '%s_%s' % (self.attrtype, 'cost')
        recover_time = card_config[recover_time_type]
        recover_num = min(max_num - now_num, card_info['health']) if self.sort != 3 else max_num - now_num
        per_dollar = card_config[cost_type]
        config = game_config.get_functional_building_mapping()
        effect = config.get(build_id, {}).get('build_effect', [1, 0])[1]
        need_dollar = int((recover_num) * per_dollar * (100 - effect) / 100.0)
        if not self.mm.user.is_dollar_enough(need_dollar):
            return 18, {}  # 美元不足
        self.mm.user.deduct_dollar(need_dollar)
        now = int(time.time())
        self.obj.rest_log[pos] = {
            'card_id': card,
            'last_recover_time': now,
            'status': 0,
            'end_time': now + recover_time * recover_num,
        }
        card_info['rest_field'] = self.sort
        self.obj.save()
        self.mm.user.save()
        self.mm.card.save()
        _, data = self.rest_index()
        return 0, data

    def get_rest_card(self, pos):
        if pos > self.obj.get_max_pos():
            return 11, {}  # 位置尚未开启
        if not self.obj.rest_log.get(pos, {}):
            return 12, {}  # 位置没有艺人休息
        # if not self.obj.rest_log.get(pos, {}).get('status', 0):
        #     return 13, {}  # 艺人尚在休息中
        build_id = self.obj.get_build_id()
        if not build_id:
            return 17, {}  # 尚未拥有建筑
        self.mm.card.cards[self.obj.rest_log[pos]['card_id']]['rest_field'] = 0
        self.obj.rest_log.pop(pos)
        self.obj.save()
        self.mm.card.save()
        _, data = self.rest_index()
        return 0, data

    def done_now(self, pos):
        if pos > self.obj.get_max_pos():
            return 11, {}  # 位置尚未开启
        if not self.obj.rest_log.get(pos, {}):
            return 12, {}  # 位置没有艺人休息
        if self.obj.rest_log.get(pos, {}).get('status', 0):
            return 13, {}  # 艺人已经休息好了
        card = self.obj.rest_log[pos]['card_id']
        card_info = self.mm.card.cards[card]
        card_config = game_config.card_basis[card_info['id']]
        build_id = self.obj.get_build_id()
        if not build_id:
            return 17, {}  # 尚未拥有建筑
        cost_type = '%s_%s' % (self.attrtype, 'diamondcost')
        per_diamondcost = card_config[cost_type]
        config = game_config.get_functional_building_mapping()

        max_num = card_config[self.attrtype]
        now_num = card_info.get(self.attrtype, 0)
        recover_num = min(max_num - now_num, card_info['health']) if self.sort != 3 else max_num - now_num
        effect = config.get(build_id, {}).get('build_effect', [1, 0])[1]
        need_diamondcost = int((recover_num) * per_diamondcost * (100 - effect) / 100.0)

        if not self.mm.user.is_diamond_enough(need_diamondcost):
            return 18, {}  # 钻石不足
        self.mm.user.deduct_diamond(need_diamondcost)
        self.obj.rest_log[pos]['status'] = 1
        self.obj.rest_log[pos]['last_recover_time'] = int(time.time())
        card_info[self.attrtype] += recover_num
        if self.sort != 3:
            card_info['health'] -= recover_num
        self.mm.card.save()
        self.obj.save()
        self.mm.user.save()
        _, data = self.rest_index()
        return 0, data

    def buy_extra_pos(self):
        config = game_config.common
        need_diamond_list = config[self.SORTCOMMONMAPING[self.sort]]
        if self.obj.extra_pos >= len(need_diamond_list):
            return 11, {}  # 已购买到最大
        need_diamond = need_diamond_list[self.obj.extra_pos]
        if not self.mm.user.is_diamond_enough(need_diamond):
            return 18, {}  # 钻石不足
        self.mm.user.deduct_diamond(need_diamond)
        self.obj.extra_pos += 1
        self.obj.save()
        self.mm.user.save()
        _, data = self.rest_index()
        return 0, data