#! --*-- coding: utf-8 --*--


import time
import random
from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice
from tools.gift import calc_gift


class FansActivity(ModelBase):
    # NEED_MAPPING = [位置编号，性别，类型，分类，演技，歌艺，气质，动感，娱乐，人气]
    NEED_MAPPING = ['pos_id', 'sex', 'profession_class', 'profession_type', 'performance', 'song', 'temperament',
                    'entertainment', 'popularity']

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'unlocked_activity': [],
            'can_unlock_activity': [],
            'activity_log': {},  # {1:{'start_time':11,item_produce:{items:[],last_time:111},
            # gold_produce:{last_time:111},attention_produce:{last_time:111},},'cards':[]}
        }
        super(FansActivity, self).__init__(self.uid)

    def count_produce(self, get_reward=False, activity_id=0):
        if activity_id not in self.activity_log:
            return []
        now = int(time.time())
        config = game_config.fans_activity
        value = self.activity_log[activity_id]
        config_id = config[activity_id]
        item_produce = value['item_produce']
        gold_produce = value['gold_produce']
        attention_produce = value['attention_produce']
        all_time = config_id['240'] * 60
        now = min(now, all_time + value['start_time'])
        item_remain_time = (now - item_produce['last_time']) % config_id['ratio_per_time']
        item_choice_times = (now - item_produce['last_time']) / config_id['ratio_per_time']
        gold_remain_time = (now - gold_produce['last_time']) % config_id['gold_per_time']
        gold_per_time = config_id['gold_per_time']
        attention_per_time = config_id['attention_per_time']
        attention_remain_time = (now - attention_produce['last_time']) % config_id['attention_per_time']
        all_items = []
        item_produce_new = []
        old_items = item_produce['items']

        for card in value['cards']:
            # 计算item
            items = []
            for _ in range(item_choice_times):
                can_choice = random.randint(1, 10000) <= config_id['ratio_per_card']
                if can_choice:
                    item = weight_choice(config_id['item'])[:-1]
                    items.append(item)
            new_items = calc_gift(items)
            item_produce_new.extend(new_items)

            # 计算金币
            # todo 产量gold_increase 取配置
            gold_increase = 0.1
            gold_per_card = config_id['gold_per_card'] * (1 + gold_increase)
            god_num = int((now - gold_produce['last_time']) / gold_per_time * gold_per_card)
            new_items.append([1, 0, god_num])

            # 计算关注度
            # todo 产量attention_increase 取配置
            attention_increase = 0.1
            attention_per_card = config_id['attention_per_card'] * (1 + attention_increase)
            attention_num = int((now - attention_produce['last_time']) / attention_per_time * attention_per_card)
            # todo 关注度添加到统一奖励里 类型待定
            new_items.append([20, 0, attention_num])
            all_items.append(new_items)

        all_items = calc_gift(all_items)
        item_produce_new = calc_gift(item_produce_new.extend(old_items))
        item_produce['last_time'] = now - item_remain_time
        item_produce['items'] = item_produce_new
        if get_reward:
            gold_produce['last_time'] = now - gold_remain_time
            attention_produce['last_time'] = now - attention_remain_time
            item_produce['items'] = []
        self.save()

        return all_items
