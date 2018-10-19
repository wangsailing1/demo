#! --*-- coding: utf-8 --*--

from gconfig import game_config
import time


class FansActivity(object):
    def __init__(self, mm=None):
        self.mm = mm

    def event(self, activity_id, cards):
        now = time.time()
        cards = cards.split('_')
        if cards.count('0') == len(cards):
            return 12, {}  # 没有艺人参加
        config = game_config.fans_activity.get(activity_id, {})
        cost = config['cost']
        if self.mm.user.dollar < cost:
            return 17, {}  #美元不足
        card_config = game_config.card_basis
        for k, card_id in enumerate(cards):
            if card_id in ['0']:
                continue
            if card_id not in self.mm.card.cards:
                return 11, {}  # 卡牌错误
            card_info = self.mm.card.get_card(card_id)
            need = config['card_need']
            for tp, need_num in need[k]:
                if tp <= 6:
                    if card_info['char_pro'][tp - 1] < need_num:
                        return 13, {}  # 有卡牌属性值不够
                elif tp == 7:
                    if need_num != card_config[card_info['id']]['sex_type']:
                        return 14, {}  # 有卡牌性别不符
                elif tp in [8, 9]:
                    tp_key = self.mm.fans_activity.NEED_MAPPING[tp - 1]
                    if need_num != card_config[card_info['id']][tp_key]:
                        return 15, {}  # 有卡牌类型不符
                else:
                    if self.mm.card.cards[card_id]['popularity'] < need_num:
                        return 16, {}  # 有卡牌人气不足
        self.mm.fans_activity.activity_log[activity_id] = {
            'start_time': now,
            'item_produce': {'items': [], 'last_time': now},
            'gold_produce': {'last_time': now},
            'attention_produce': {'last_time': now},
            'cards': cards
        }
        self.mm.user.dollar -= cost
        self.mm.fans_activity.save()
        self.mm.user.save()
        return 0, {}
