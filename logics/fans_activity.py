#! --*-- coding: utf-8 --*--

from gconfig import game_config
import time


class FansActivity(object):
    def __init__(self, mm=None):
        self.mm = mm

    def activity(self, activity_id, cards):
        now = int(time.time())
        cards = cards.split('_')
        if cards.count('0') == len(cards):
            return 12, {}  # 没有艺人参加
        config = game_config.fans_activity.get(activity_id, {})
        cost = config['cost']
        if self.mm.user.dollar < cost:
            return 17, {}  # 美元不足
        card_config = game_config.card_basis
        value = self.mm.fans_activity.activity_log.get(activity_id, {})
        all_time = config['time'] * 60
        remian_time = max(all_time + value.get('start_time', 0) - int(time.time()), 0)
        if remian_time > 0:
            return 18, {}  # 活动未结束
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
        _, data = self.fans_index(activity_id)
        return 0, data

    def fans_index(self, activity_id=0):
        config = game_config.fans_activity
        data = {}
        if activity_id:
            if activity_id not in self.mm.fans_activity.activity_log:
                return 11, {}  # 未举办该活动
            value = self.mm.fans_activity.activity_log[activity_id]
            items = self.mm.fans_activity.count_produce(activity_id=activity_id)
            config_id = config[activity_id]
            all_time = config_id['time'] * 60
            print all_time, value['start_time'], int(time.time())
            remian_time = max(all_time + value['start_time'] - int(time.time()), 0)
            data[activity_id] = {
                'items': items,
                'remian_time': remian_time,
                'cards': value['cards'],
            }
            data['activity'] = self.mm.fans_activity.activity
            data['unlocked_activity'] = self.mm.fans_activity.unlocked_activity
            data['can_unlock_activity'] = self.mm.fans_activity.can_unlock_activity
            return 0, data

        for id, value in self.mm.fans_activity.activity_log.iteritems():
            items = self.mm.fans_activity.count_produce(activity_id=id)
            config_id = config[id]
            all_time = config_id['time'] * 60
            remian_time = max(all_time + value['start_time'] - int(time.time()), 0)
            data[id] = {
                'items': items,
                'remian_time': remian_time,
                'cards': value['cards'],
            }
        data['unlocked_activity'] = self.mm.fans_activity.unlocked_activity
        data['can_unlock_activity'] = self.mm.fans_activity.can_unlock_activity
        data['activity'] = self.mm.fans_activity.activity
        return 0, data
