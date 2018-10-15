# -*- coding: utf-8 –*-

import time
import random
import copy

from models.ranking_list import BlockRank
from lib.core.environ import ModelManager
from models.block import get_date_before
from gconfig import game_config, get_str_words

rank_list = [1, 2, 3, 'nv', 'nan', 'medium', 'audience']


class Block(object):
    def __init__(self, mm):
        self.mm = mm

    def join_award_ceremony(self):
        data = {}
        for tp in rank_list:
            rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
                                                    tp)
            data.setdefault(tp, {'win': {}, 'nomination': {}})
            date = time.strftime('%F')
            br = BlockRank(rank_uid, self.mm.block._server_name, date)
            nomination = br.get_all_user(0, 4, withscores=True)
            if tp in ['nv', 'nan']:
                id = 1
                for uid_card_id, score in nomination:
                    uid, card_id = uid_card_id.split('_')
                    umm = ModelManager(uid)
                    name = umm.user.name
                    card_cid = umm.card.cards[card_id]['id']
                    card_name = umm.card.cards[card_id]['name']
                    if not data[tp]['win']:
                        data[tp]['win'] = {
                            'name': name,
                            'card_cid': card_cid,
                            'card_name': card_name,
                            'score': score
                        }
                    data[tp]['nomination'][id] = {
                        'name': name,
                        'card_cid': card_cid,
                        'card_name': card_name,
                        'score': score
                    }
                    id += 1
            else:
                id = 1
                for uid_script_id, score in nomination:
                    uid, script_id = uid_script_id.split('_')
                    umm = ModelManager(uid)
                    name = umm.user.name
                    script_id = int(script_id)
                    script_name = umm.block.top_script.get(date, {}).get(script_id, {}).get('name', '')
                    if not data[tp]['win']:
                        data[tp]['win'] = {
                            'name': name,
                            'script_id': script_id,
                            'script_name': script_name,
                            'score': score
                        }
                    data[tp]['nomination'][id] = {
                        'name': name,
                        'script_id': script_id,
                        'script_name': script_name,
                        'score': score
                    }
                    id += 1
        big_sale_info = self.get_big_sale_info()
        data['big_sale_info'] = big_sale_info
        self.mm.block.award_ceremony = 1
        self.mm.block.save()
        return data

    def get_big_sale_info(self):
        data = []
        check_data = {}
        date = get_date_before()
        info = copy.deepcopy(self.mm.block.top_script.get(date, {}))
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
            for _ in range(robot_num):
                name = game_config.get_random_name(self.mm.user.language_sort)
                script_id = random.choice(script_list)
                script_list.remove(script_id)
                script_name = game_config.script[script_id]['name']
                script_name = get_str_words(self.mm.user.language_sort, script_name)
                robot_data.append([name, script_name])
        return {'own': data, 'robot': robot_data}
