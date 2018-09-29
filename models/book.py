#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
import math

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class CardBook(ModelBase):
    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'book': {},
            'cards': []
        }
        super(CardBook, self).__init__(self.uid)

    def add_book(self, card_id):
        if card_id in self.cards:
            return
        self.cards.append(card_id)
        config_mapping = game_config.get_book_mapping()
        if card_id not in config_mapping:
            return
        book_id = config_mapping[card_id]
        config = game_config.card_book
        if book_id in config:
            if book_id not in self.book:
                self.book[book_id] = {
                    'card': [],
                    'flag': -1,
                }
            if card_id in self.book[book_id]['card']:
                return
            self.book[book_id]['card'].append(card_id)
            if sorted(self.book[book_id]['card']) == sorted(config[book_id]['card']):
                self.book[book_id]['flag'] = 0
        self.save()


class ScriptBook(ModelBase):
    TARGET = {1: 'shoot_num', 2: 'max_script', 3: 'big_sale', 4: 'output'}
    TARGETMAPPING = {'shoot_num': 1, 'max_script': 2, 'big_sale': 3, 'output': 4}

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'book': {},
            'group': {},
            'scripts': []
        }
        super(ScriptBook, self).__init__(self.uid)

    def add_book(self, script_id):
        if script_id in self.scripts:
            return
        self.scripts.append(script_id)
        config_mapping = game_config.get_book_mapping(type='script_book')
        if script_id in config_mapping:
            book_id = config_mapping[script_id]
            config = game_config.script_book
            if book_id not in self.book:
                self.book[book_id] = {
                    'script': [],
                    'flag': -1,
                }
            if script_id in self.book[book_id]['script']:
                return
            self.book[book_id]['script'].append(script_id)
            if sorted(self.book[book_id]['script']) == sorted(config[book_id]['script']):
                self.book[book_id]['flag'] = 0

        self.save()

    def add_script_group(self, script_id, big_sale, output):
        script_config = game_config.script[script_id]
        group_id = script_config['group']
        group_config = game_config.script_group_object
        if group_id not in group_config:
            return
        if group_id not in self.group:
            self.group[group_id] = {
                'shoot_num': 0,  # 拍摄次数
                'max_script': 0,  # 拍摄的最大续集
                'big_sale': 0,  # 大卖次数
                'output': 0,  # 票房
                'flag': -1,  # 目标完成标识 -1 未完成 0 完成未领奖 1已领奖
                'script_id': script_id,
                'max_output': 0  # 最大票房
            }
        self.group[group_id]['shoot_num'] += 1
        if script_config['sequel_count'] > self.group[group_id]['max_script']:
            self.group[group_id]['max_script'] = script_config['sequel_count']
            self.group[group_id]['script_id'] = script_id
        if big_sale:
            self.group[group_id]['big_sale'] += 1
        self.group[group_id]['output'] += output
        if output > self.group[group_id]['max_output']:
            self.group[group_id]['max_output'] = output
        g_config = group_config[group_id]
        for k, v in g_config['group_target']:
            if self.group[group_id][self.TARGET[k]] < v:
                break
        else:
            if self.group[group_id]['flag'] == -1:
                self.group[group_id]['flag'] = 0
        self.save()


# class ScriptGroup(ModelBase):
#     TARGET = {1: 'shoot_num', 2: 'next_id', 3: 'big_sale', 4: 'output'}
#     TARGETMAPPING = {'shoot_num': 1, 'next_id': 2, 'big_sale': 3, 'output': 4}
#
#     def __init__(self, uid):
#         self.uid = uid
#         self._attrs = {
#             'group': {}
#         }
#         super(ScriptGroup, self).__init__(self.uid)
#
#     # 添加组合目标 剧本id，续集id，是否大卖，票房
#     def add_script_group(self, script_id, big_sale, output):
#         script_config = game_config.script[script_id]
#         group_id = script_config['group']
#         group_config = game_config.script_group_object
#         if group_id not in group_config:
#             return
#         if group_id not in self.group:
#             self.group[group_id] = {
#                 'shoot_num': 0,  # 拍摄次数
#                 'max_script': 0,  # 拍摄的最大续集
#                 'big_sale': 0,  # 大卖次数
#                 'output': 0,  # 票房
#                 'flag': -1  # 目标完成标识 -1 未完成 0 完成未领奖 1已领奖
#             }
#         self.group[group_id]['shoot_num'] += 1
#         if script_id > self.group[group_id]['max_script']:
#             self.group[group_id]['max_script'] = script_id
#         if big_sale:
#             self.group[group_id]['big_sale'] += 1
#         self.group[group_id]['output'] += output
#         g_config = group_config[group_id]
#         for k, v in g_config['group_target']:
#             if self.group[group_id][self.TARGET[k]] < v:
#                 break
#         else:
#             if self.group[group_id]['flag'] == -1:
#                 self.group[group_id]['flag'] = 0
#         self.save()


ModelManager.register_model('card_book', CardBook)
ModelManager.register_model('script_book', ScriptBook)
