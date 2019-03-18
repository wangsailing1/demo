#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice
from tools.gift import calc_gift
from models.vip_company import bussiness_gold


class FansActivity(ModelBase):
    # NEED_MAPPING = ['演技', '歌艺', '气质', '动感', '艺术'，'娱乐',性别，类型，分类，人气]
    NEED_MAPPING = ['performance', 'song', 'temperament', 'sports', 'art', 'entertainment', 'sex', 'profession_class',
                    'profession_type', 'popularity']

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'activity': {},
            'unlocked_activity': [],
            # 'can_unlock_activity': [],
            'activity_log': {},  # {1:{'start_time':11,item_produce:{items:[],last_time:111},
            # gold_produce:{last_time:111},attention_produce:{last_time:111},},'cards':[]}
            'card_mapping': {},  # 记录卡牌所在活动
        }
        super(FansActivity, self).__init__(self.uid)

    def pre_use(self):
        # 数据更正 开发环境用
        save = False
        for card_id, value in self.card_mapping.iteritems():
            if isinstance(value, int):
                self.card_mapping[card_id] = [value, 0]
                save = True

        # if not self.can_unlock_activity:
        #     all_id = game_config.fans_activity.keys()
        #     all_lock_id = [i['fans_activity'] for i in game_config.chapter_stage.values()]
        #     self.can_unlock_activity = list(set(all_id) - set(all_lock_id))
        #     save = True
        # else:
        #     all_id = game_config.fans_activity.keys()
        #     all_lock_id = [i['fans_activity'] for i in game_config.chapter_stage.values()]
        #     can_unlock_id = list(set(all_id) - set(all_lock_id))
        #     new_can_unlock_id = list(set(can_unlock_id) - set(self.can_unlock_activity))
        #     if new_can_unlock_id:
        #         self.can_unlock_activity.extend(new_can_unlock_id)

        if save:
            self.save()

    def count_produce(self, get_reward=False, activity_id=0, is_save=True):
        if activity_id not in self.activity_log:
            return []
        now = int(time.time())
        config = game_config.fans_activity
        value = self.activity_log[activity_id]
        if not value:
            return []
        config_id = config[activity_id]
        item_produce = value['item_produce']
        gold_produce = value['gold_produce']
        attention_produce = value['attention_produce']
        all_time = config_id['time'] * 60
        now = min(now, all_time + value['start_time'])
        item_remain_time = (now - item_produce['last_time']) % config_id['ratio_per_time']
        item_choice_times = int((now - item_produce['last_time']) / config_id['ratio_per_time'])
        gold_remain_time = (now - gold_produce['last_time']) % config_id['gold_per_time']
        gold_per_time = config_id['gold_per_time']
        attention_per_time = config_id['attention_per_time']
        attention_remain_time = (now - attention_produce['last_time']) % config_id['attention_per_time']
        all_items = []
        item_produce_new = []
        old_items = item_produce['items']

        for card in value['cards']:
            if card in ['0']:
                continue
            # 计算item
            items = []
            card_effect = {}
            for _ in range(item_choice_times):
                can_choice = random.randint(1, 10000) <= config_id['ratio_per_card']
                if can_choice:
                    item = weight_choice(config_id['item'])[:-1]
                    items.append(item)
            item_produce_new = calc_gift(items)
            skill_effect = self.mm.card.get_skill_effect({card:0}, 2, 0).get(card, {}).get('effect', {})
            # 计算金币
            card_effect[card] = skill_effect.get(17, {}).get(2, 0) + bussiness_gold(self.mm.user)
            increase = (value.get('effect_id') + bussiness_gold(self.mm.user) +
                        skill_effect.get(17, {}).get(2, 0)) / 10000.0  # 活动加成
            gold_per_card = config_id['gold_per_card'] * (1 + increase )
            god_num = int((now - gold_produce['last_time']) / gold_per_time * gold_per_card)
            new_items = [[1, 0, god_num]]

            # 计算关注度
            attention_per_card = config_id['attention_per_card'] * (1 + increase)
            attention_num = int((now - attention_produce['last_time']) / attention_per_time * attention_per_card)
            new_items.append([19, 1, attention_num])
            all_items.extend(new_items)
        item_produce_new.extend(old_items)
        all_items.extend(item_produce_new)
        all_items = calc_gift(all_items)

        if item_produce_new:
            item_produce_new = calc_gift(item_produce_new)
        item_produce['last_time'] = now - item_remain_time
        item_produce['items'] = item_produce_new
        if get_reward:
            if now == all_time + value['start_time']:
                # self.delete_card_mapping(self.activity_log[activity_id]['cards'])
                self.activity_log[activity_id] = {}
            else:
                gold_produce['last_time'] = now - gold_remain_time
                attention_produce['last_time'] = now - attention_remain_time
                item_produce['items'] = []
        if is_save:
            self.save()

        return all_items, card_effect

    # 添加可解锁粉丝活动
    # def add_can_unlock_activity(self, activity_id, is_save=False):
    #     if activity_id and activity_id not in self.can_unlock_activity:
    #         self.can_unlock_activity.append(activity_id)
    #         if is_save:
    #             self.save()

    @property
    def can_unlock_activity(self):
        info = []
        # 需要推图解锁的
        config = game_config.get_chapter_mapping()
        stage_config = game_config.chapter_stage
        all_stage = self.mm.chapter_stage.chapter
        for chapter_id ,value in all_stage.iteritems():
            for type_hard, s_value in value.iteritems():
                for stage_id in s_value.keys():
                    stage = config[chapter_id][type_hard]['stage_id'][stage_id - 1]
                    if stage:
                        fans_id = stage_config[stage].get('fans_activity',0)
                        if fans_id and fans_id not in info:
                            info.append(fans_id)
        # 不需要解锁条件的
        all_id = game_config.fans_activity.keys()
        all_lock_id = [i['fans_activity'] for i in game_config.chapter_stage.values()]
        can_unlock_id = list(set(all_id) - set(all_lock_id))
        new_can_unlock_id = list(set(can_unlock_id) - set(info))
        info.extend(new_can_unlock_id)
        return info




    def get_card_effect(self, cards):
        group_list = set()
        config = game_config.card_basis
        for card in cards:
            if card in ['0']:
                continue
            group_list.add(config[self.mm.card.cards[card]['id']]['group'])
        effect_dict = {}
        for k, value in game_config.card_book.iteritems():
            if len(group_list & set(value['card'])) == len(value['card']):
                effect_dict[k] = value['fans_ativity']
        return max(effect_dict.items(), key=lambda x: x[1])[0] if effect_dict else 0

    def add_card_mapping(self, cards, activity_id, is_save=False):
        for card in cards:
            if card not in ['0']:
                self.card_mapping[card] = [activity_id, cards.index(card) + 1]
        if is_save:
            self.save()

    def delete_card_mapping(self, cards, is_save=False):
        for card in cards:
            if card not in ['0'] and card in self.card_mapping:
                self.card_mapping.pop(card)
        if is_save:
            self.save()

    def change_card_mapping(self, old_id, new_id, is_save=False):
        for card_id, value in self.card_mapping.iteritems():
            if value[0] == old_id:
                value[0] = new_id
        if is_save:
            self.save()

    def fans_activity_info(self):
        data = {'unlocked_activity': self.unlocked_activity,
                'can_unlock_activity': self.can_unlock_activity,
                'activity': self.activity}
        return data

    def activety_status(self,activity_id):
        """
        0未开启 1开启没人 2开启有人
        :return: 
        """
        data = self.activity_log.get(activity_id, {})
        if not data:
            return 0
        else:
            for i in data['cards']:
                if i in self.mm.card.cards:
                        return 2
        return 1

    def get_fans_cards(self):
        cards = []
        for id, value in self.activity_log.iteritems():
            for card_id in value.get('cards',[]):
                cards.append(card_id)
        return cards




ModelManager.register_model('fans_activity', FansActivity)
