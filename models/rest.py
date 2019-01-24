#! --*-- coding: utf-8 --*--


import time
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class Rest(ModelBase):
    TYPEMAPPING = {1: 'restaurant',2: 'bar',3: 'hospital'}

    def __init__(self,uid=None):
        self.uid = uid
        self._attrs = {
            # 'hospital_extra_pos': 0,
            # 'bar_extra_pos': 0,
            # 'restaurant_extra_pos': 0,
            'extra_pos': 0,
            'rest_log': {},

        }
        super(Rest, self).__init__(self.uid)

    def pre_use(self):
        save = False
        for pos, info in self.rest_log.iteritems():
            if not info:
                continue
            self.recover_rest(info)
            save = True
        if save:
            self.save()
            self.mm.card.save()

    def recover_rest(self, info):
        card_info = self.mm.card.cards[info['card_id']]
        card_config = game_config.card_basis[card_info['id']]
        last_recover_time = info['last_recover_time']
        recover_time = card_config['physical_recovery']
        now = int(time.time())
        physical = card_info['physical']
        physical_max = card_config['physical']
        num = min((now - last_recover_time) / recover_time, physical_max - physical)
        health = card_info['health']

        if health <= num:
            card_info['health'] -= health
            card_info['physical'] += health
        else:
            card_info['health'] -= num
            card_info['physical'] += num
        if card_info['health'] <= 0 or card_info['physical'] >= physical_max:
            info['status'] = 1
            info['last_recover_time'] = now
        else:
            info['last_recover_time'] += num * recover_time

    def get_max_pos(self):
        build_id = self.mm.user.group_ids.get(19, {}).get('build_id', 0)
        config = game_config.get_functional_building_mapping()
        pos_num = config.get(build_id, {}).get('build_effect', [1, 0])[0]
        return pos_num + self.extra_pos

    def get_rest_cards(self):
        cards = []
        for pos, info in self.rest_log.iteritems():
            if info:
                cards.append(info['card_id'])
        return cards

    def get_build_id(self):
        return self.mm.user.group_ids.get(19, {}).get('build_id', 0)


class RestBar(Rest):

    def recover_rest(self, info):
        card_info = self.mm.card.cards[info['card_id']]
        card_config = game_config.card_basis[card_info['id']]
        last_recover_time = info['last_recover_time']
        recover_time = card_config['mood_recovery']
        now = int(time.time())
        mood = card_info['mood']
        mood_max = card_config['mood']
        num = min((now - last_recover_time) / recover_time, mood_max - mood)
        health = card_info['health']

        if health <= num:
            card_info['health'] -= health
            card_info['mood'] += health
        else:
            card_info['health'] -= num
            card_info['mood'] += num
        if card_info['health'] <= 0 or card_info['mood'] >= mood_max:
            info['status'] = 1
            info['last_recover_time'] = now
        else:
            info['last_recover_time'] += num * recover_time

    def get_max_pos(self):
        build_id = self.mm.user.group_ids.get(20, {}).get('build_id', 0)
        config = game_config.get_functional_building_mapping()
        pos_num = config.get(build_id, {}).get('build_effect', [1, 0])[0]
        return pos_num + self.extra_pos

    def get_build_id(self):
        return self.mm.user.group_ids.get(20, {}).get('build_id', 0)

class RestHospital(Rest):

    def recover_rest(self, info):
        card_info = self.mm.card.cards[info['card_id']]
        card_config = game_config.card_basis[card_info['id']]
        last_recover_time = info['last_recover_time']
        recover_time = card_config['health_recovery']
        now = int(time.time())
        health = card_info['health']
        health_max = card_config['health']
        num = min((now - last_recover_time) / recover_time, health_max - health)
        card_info['health'] -= num
        card_info['health'] += num
        if card_info['health'] >= health_max:
            info['status'] = 1
            info['last_recover_time'] = now
        else:
            info['last_recover_time'] += num * recover_time

    def get_max_pos(self):
        build_id = self.mm.user.group_ids.get(21, {}).get('build_id', 0)
        config = game_config.get_functional_building_mapping()
        pos_num = config.get(build_id, {}).get('build_effect', [1, 0])[0]
        return pos_num + self.extra_pos

    def get_build_id(self):
        return self.mm.user.group_ids.get(21, {}).get('build_id', 0)

ModelManager.register_model('rest_restaurant', Rest)
ModelManager.register_model('rest_bar', RestBar)
ModelManager.register_model('rest_hospital', RestHospital)


