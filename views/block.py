# -*- coding: utf-8 –*-
from tools.gift import add_mult_gift
from gconfig import game_config
from models.ranking_list import BlockRank
from lib.core.environ import ModelManager
import time

rank_list = [1,2,3,'nv','nan','medium','audience']

def join_award_ceremony(hm):
    mm = hm.mm
    data = {}
    if mm.block.award_ceremony:
        return 1, {}
    for tp in rank_list:
        rank_uid = mm.block.get_key_profix(mm.block.block_num, mm.block.block_group,
                                                             tp)
        data.setdefault(tp,{'win':{},'nomination':{}})
        date = time.strftime('%F')
        br = BlockRank(rank_uid, mm.block._server_name,date)
        nomination = br.get_all_user(0,4,withscores=True)
        if tp in ['nv','nan']:
            id = 1
            for uid_card_id,score in nomination:
                uid,card_id = uid_card_id.split('_')
                mm=ModelManager(uid)
                name = mm.user.name
                card_cid = mm.card.cards[card_id]['id']
                card_name = mm.card.cards[card_id]['name']
                if not data[tp]['win']:
                    data[tp]['win'] = {
                        'name':name,
                        'card_cid':card_cid,
                        'card_name':card_name,
                        'score':score
                    }
                data[tp]['nomination'][id] = {
                        'name':name,
                        'card_cid':card_cid,
                        'card_name':card_name,
                        'score': score
                    }
                id += 1
        else:
            id = 1
            for uid_script_id, score in nomination:
                uid, script_id = uid_script_id.split('_')
                mm = ModelManager(uid)
                name = mm.user.name
                script_id = int(script_id)
                script_name = mm.block.top_script.get(date,{}).get(script_id,{}).get('name','')
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
                    'score':score
                }
                id += 1
    return 0, {}





def get_reward(hm):
    mm = hm.mm
    return 0, {}


def get_daily_reward(hm):
    mm = hm.mm
    return 0, {}