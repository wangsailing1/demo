# -*- coding: utf-8 –*-

import random
import copy

from models.ranking_list import BlockRank
from lib.core.environ import ModelManager
from models.block import get_date_before
from gconfig import game_config, get_str_words
from tools.gift import add_mult_gift


class Block(object):
    def __init__(self, mm):
        self.mm = mm
        self.block = self.mm.block
        self.card = self.mm.card

    def join_award_ceremony(self):
        data = {}
        for tp in self.block.rank_list:
            rank_uid = self.block.get_key_profix(self.block.block_num, self.block.block_group,
                                                 tp)
            date = get_date_before()
            br = BlockRank(rank_uid, self.block._server_name, date)
            nomination = br.get_all_user(0, 4, withscores=True)
            if tp in ['nv', 'nan']:
                tp_num = self.block.RANKMAPPING[tp]
                id = 1
                if tp_num not in data:
                    data[tp_num] = {'win': {}, 'nomination': {}}
                for uid_card_id, score in nomination:
                    uid, card_id = uid_card_id.split('_')
                    umm = ModelManager(uid)
                    name = umm.user.name
                    card_cid = umm.card.cards[card_id]['id']
                    card_name = umm.card.cards[card_id]['name']
                    if not data[tp_num]['win']:
                        data[tp_num]['win'] = {
                            'uid':uid,
                            'name': name,
                            'card_cid': card_cid,
                            'card_name': card_name,
                            'score': score
                        }
                    data[tp_num]['nomination'][id] = {
                        'uid': uid,
                        'name': name,
                        'card_cid': card_cid,
                        'card_name': card_name,
                        'score': score
                    }
                    id += 1
            else:
                tp_num = tp
                if tp in ['medium', 'audience']:
                    tp_num = self.block.RANKMAPPING[tp]
                id = 1
                if tp_num not in data:
                    data[tp_num]= {'win': {}, 'nomination': {}}
                for uid_script_id, score in nomination:
                    uid, script_id = uid_script_id.split('_')
                    umm = ModelManager(uid)
                    name = umm.user.name
                    script_id = int(script_id)
                    script_name = umm.block.top_script.get(date, {}).get(script_id, {}).get('name', '')

                    if not data[tp_num]['win']:
                        data[tp_num]['win'] = {
                            'uid': uid,
                            'name': name,
                            'script_id': script_id,
                            'script_name': script_name,
                            'score': score
                        }
                    data[tp_num]['nomination'][id] = {
                        'uid': uid,
                        'name': name,
                        'script_id': script_id,
                        'script_name': script_name,
                        'score': score
                    }
                    id += 1
        big_sale_info = self.get_big_sale_info()
        data['big_sale_info'] = big_sale_info
        if not self.block.award_ceremony:
            self.block.award_ceremony = 1
            self.block.save()
        return data

    def get_big_sale_info(self):
        data = []
        check_data = {}
        date = get_date_before()
        info = copy.deepcopy(self.block.top_script.get(date, {}))
        while len(data) < 10:
            for script_id, value in info.iteritems():
                if value['big_sale_num'] >= 1:
                    data.append([self.mm.user.name, value['name']])
                    value['big_sale_num'] -= 1
                    check_data[script_id] = value['big_sale_num']
                if len(data) >= 10:
                    break
            if sum(check_data.values()) <= 0:
                break
        robot_num = 10 - len(data)
        robot_data = []
        if robot_num >= 0:
            script_list = game_config.script.keys()
            print script_list
            for _ in range(robot_num):
                name = game_config.get_random_name(self.mm.user.language_sort)
                script_id = random.choice(script_list)
                script_list.remove(script_id)
                script_name = game_config.script[script_id]['name']
                script_name = get_str_words(self.mm.user.language_sort, script_name)
                robot_data.append([name, script_name])
        return {'own': data, 'robot': robot_data}

    def get_reward(self):
        data = {}
        info = self.mm.block.reward_data
        cup = 0
        for k, v in info.iteritems():
            if k == 'big_sale_cup':
                cup += v
            else:
                cup += info['cup']  # 类型奖杯奖励读配置
        data['old_block_num'] = self.block.block_num
        data['old_block_group'] = self.block.block_group
        self.block.get_award_ceremony = 1
        self.block.has_ceremony = 0
        self.block.up_block(cup)
        key_uid = self.block.get_key_profix(self.block.block_num)
        b = BlockRank(key_uid, self.block._server_name)
        if not b.check_user_exist_by_block(self.mm.uid):
            num = b.get_num()
            b.add_user_by_block(self.mm.uid, num)
            group = b.get_group(self.mm.uid)
            self.block.block_group = group
        reward = {}
        if self.block.block_num > data['old_block_num']:
            gift = game_config.dan_grading_list.get(self.block.block_num).get('reach_rewards', [])
            reward = add_mult_gift(self.mm, gift)
        data['new_block_num'] = self.block.block_num
        data['new_block_group'] = self.block.block_group
        data['cup'] = cup
        data['reward'] = reward
        self.block.save()

        return data

    def count_cup(self,is_save=False):
        data = {}
        if self.block.is_count:
            return
        for tp in self.block.rank_list:
            rank_uid = self.block.get_key_profix(self.block.block_num, self.block.block_group,
                                                 tp)
            data = {}
            date = get_date_before()
            br = BlockRank(rank_uid, self.block._server_name, date)
            nomination = br.get_all_user(0, 4, withscores=True)
            if tp in ['nv', 'nan']:
                tp_num = self.block.RANKMAPPING[tp]
                for uid_card_id, score in nomination:
                    uid, card_id = uid_card_id.split('_')
                    if self.mm.uid != uid:
                        continue
                    rank = br.get_rank(uid)
                    card_cid = self.card.cards[card_id]['id']
                    card_name = self.card.cards[card_id]['name']
                    reward_type = 'win_cup_num'
                    if rank > 1:
                        reward_type = 'nomi_cup_num'

                    cup = game_config.cup_num[int(tp_num)].get(reward_type,1)
                    data[tp_num] = {
                        'name': self.mm.user.name,
                        'card_cid': card_cid,
                        'card_name': card_name,
                        'score': score,
                        'reward_type':reward_type,
                        'cup':cup

                    }
                    self.block.cup_log[tp_num] = self.block.cup_log.get(tp_num,0) + 1
            else:
                tp_num = tp
                if tp in ['medium', 'audience']:
                    tp_num = self.block.RANKMAPPING[tp]
                for uid_script_id, score in nomination:
                    uid, script_id = uid_script_id.split('_')
                    if self.mm.uid != uid:
                        continue
                    rank = br.get_rank(uid)
                    script_id = int(script_id)
                    script_name = self.block.top_script.get(date, {}).get(script_id, {}).get('name', '')
                    reward_type = 'win_cup_num'
                    if rank > 1:
                        reward_type = 'nomi_cup_num'
                    cup = game_config.cup_num[int(tp_num)].get(reward_type, 1)
                    data[tp_num] = {
                        'name': self.mm.user.name,
                        'script_id': script_id,
                        'script_name': script_name,
                        'score': score,
                        'reward_type': reward_type,
                        'cup': cup
                    }
                    self.block.cup_log[tp_num] = self.block.cup_log.get(tp_num, 0) + 1
            data['big_sale_cup'] = self.block.big_sale
        self.block.reward_data = data
        if is_save:
            self.block.save()

    def check_has_ceremony(self):
        date = get_date_before()
        block_rank_uid = self.block.get_key_profix(self.block.block_num, self.block.block_group,
                                                   'script')
        br = BlockRank(block_rank_uid, self.block._server_name, date)
        if br.get_all_user():
            self.block.has_ceremony = 1
            self.block.save()
