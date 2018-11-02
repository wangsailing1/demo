# -*- coding: utf-8 –*-
import time
from lib.core.environ import ModelManager
from gconfig import game_config, get_str_words
from models.ranking_list import BlockRank
from models.block import REWARD_TIME, get_date

rank_mapping = {1: 'appeal_rank', 2: 'output_rank', 3: 'alloutput_rank'}
block_mapping = {1: 'script', 2: 'income'}


def rank_index(hm):
    mm = hm.mm
    rank_id = int(hm.get_argument('rank_id', 1))
    start = int(hm.get_argument('start_num', 1))
    end = int(hm.get_argument('end_num', 100))
    if start > end:
        start = 1
        end = 100
    ar = mm.get_obj_tools(rank_mapping[rank_id])

    rank_list = ar.get_all_user(withscores=True, start=start, end=end)

    appeal_rank_list = []
    output_rank_list = []
    alloutput_rank_list = []

    if rank_id == 1:
        rank_own_list = []
        for uid_group_id, score in rank_list:
            uid, group_id = uid_group_id.split('|')
            umm = ModelManager(uid)
            group_id = int(group_id)
            if group_id not in umm.card.group_ids:
                continue
            card_id = umm.card.group_ids[group_id]
            cid = int(card_id.split('-')[0])
            card_name = game_config.card_basis[cid]['name']
            name = umm.user.name
            appeal_rank_list.append({'uid': uid,
                                     'name': name,
                                     'group_id': group_id,
                                     'score': score,
                                     'card_name': card_name})
        for group_id, card_id in mm.card.group_ids.iteritems():
            uid_group_id = '%s|%s' % (mm.uid, group_id)
            rank = ar.get_rank(uid_group_id)
            if not rank:
                continue
            cid = int(card_id.split('-')[0])
            card_name = game_config.card_basis[cid]['name']
            score = ar.get_score(uid_group_id)
            rank_own_list.append({'uid': mm.uid,
                                  'name': mm.user.name,
                                  'group_id': group_id,
                                  'score': score,
                                  'rank_own': rank,
                                  'card_name': card_name})
        return 0, {
            'rank_list': appeal_rank_list,
            'rank_own': sorted(rank_own_list,key=lambda x:x['rank_own'])
        }

    elif rank_id == 2:
        output_rank_own_list = []
        for uid, score in rank_list:
            umm = ModelManager(uid)
            name = umm.user.name
            if umm.script.top_all:
                script_id = umm.script.top_all['id']
            else:
                continue
            script_name = umm.script.top_all.get('name', '')
            if not script_name:
                script_name = game_config.script[script_id]['name']
                script_name = get_str_words(mm.user.language_sort, script_name)

            output_rank_list.append({'uid': uid,
                                     'name': name,
                                     'script_id': script_id,
                                     'score': score,
                                     'script_name': script_name})
        if mm.script.top_all:
            script_id = mm.script.top_all['id']
            script_name = mm.script.top_all.get('name', '')
            if not script_name:
                script_name = game_config.script[script_id]['name']
                script_name = get_str_words(mm.user.language_sort, script_name)
            output_rank_own_list.append({'uid': mm.uid,
                                         'name': mm.user.name,
                                         'script_id': script_id,
                                         'score': ar.get_score(mm.uid),
                                         'rank_own': ar.get_rank(mm.uid),
                                         'script_name': script_name})
        return 0, {
            'rank_list': output_rank_list,
            'rank_own': output_rank_own_list,
        }

    else:
        alloutput_rank_own_list = []
        for uid, score in rank_list:
            umm = ModelManager(uid)
            name = umm.user.name
            group_id = umm.script.get_top_group_id_sequel()
            if not group_id:
                continue
            script_id = umm.script.top_sequal[group_id]['top_script']['id']

            alloutput_rank_list.append({'uid': uid,
                                        'name': name,
                                        'script_id': script_id,
                                        'group_id': group_id,
                                        'score': score,
                                        'group_name': game_config.script_group_object.get(group_id, {}).get('name',
                                                                                                            '')})
        group_id = mm.script.get_top_group_id_sequel()
        script_id = mm.script.top_sequal.get(group_id,{}).get('top_script',{}).get('id',0)
        if script_id:
            alloutput_rank_own_list.append({'uid': mm.uid,
                                            'name': mm.user.name,
                                            'group_id': group_id,
                                            'score': ar.get_score(mm.uid),
                                            'script_id': script_id,
                                            'rank_own': ar.get_rank(mm.uid),
                                            'group_name': game_config.script_group_object.get(group_id, {}).get(
                                                'name', '')})

        return 0, {
            'rank_list': alloutput_rank_list,
            'rank_own': alloutput_rank_own_list
        }


def get_script_info(hm):
    mm = hm.mm
    script_id = hm.get_argument('script_id', 0)
    uid = hm.get_argument('uid', '')
    if uid:
        mm = ModelManager(uid)
    if not script_id:
        return 1, {}
    return 0, {'script_info': mm.script.get_script_info(int(script_id)),
               'name': mm.user.name,
               'vip': mm.user.vip,
               'guild_name': mm.user.guild_name,
               'actor_num': len(mm.card.cards),
               'level': mm.user.level,
               'uid': uid,
               'cup_log_script': mm.block.cup_log_script}


def get_group_info(hm):
    mm = hm.mm
    group_id = hm.get_argument('group_id', 0)
    uid = hm.get_argument('uid', '')
    if uid:
        mm = ModelManager(uid)
    if not group_id:
        return 1, {}
    m_script = mm.script.get_max_script_by_group(int(group_id))
    return 0, {'group_info': mm.script.get_script_info(int(m_script)),
               'group_id': mm.script.get_top_group_id_sequel(),
               'name': mm.user.name,
               'vip': mm.user.vip,
               'guild_name': mm.user.guild_name,
               'actor_num': len(mm.card.cards),
               'level': mm.user.level,
               'uid': uid,
               'cup_log_script': mm.block.cup_log_script}


def get_user_info(hm):
    mm = hm.mm
    uid = hm.get_argument('uid', '')
    if uid:
        mm = ModelManager(uid)
    return 0, {
        'group_info': mm.script.get_scrip_info_by_num(is_type=2),
        'script_info': mm.script.get_scrip_info_by_num(),
        'name': mm.user.name,
        'vip': mm.user.vip,
        'guild_name': mm.user.guild_name,
        'actor_num': len(mm.card.cards),
        'level': mm.user.level,
        'block': mm.block.block_num,
        'all_income': mm.user.script_income,
        'script_num': len(mm.script.own_script),
        'top_cards': mm.card.get_better_card(),
        'uid': uid,
        'role': mm.user.role}



def block_index(hm):
    """
    rank_id:1单片票房，2总排行
    :param hm: 
    :return: 
    """
    mm = hm.mm
    rank_id = hm.get_argument('rank_id', 1, is_int=True)
    start = hm.get_argument('start_num', 1, is_int=True)
    end = hm.get_argument('end_num', 100, is_int=True)
    rank_type = block_mapping[rank_id]

    block_rank_uid = mm.block.get_key_profix(mm.block.block_num, mm.block.block_group,
                                             rank_type)
    br = BlockRank(block_rank_uid, mm.block._server_name)
    date = get_date()

    rank_list = br.get_all_user(withscores=True,start=start,end=end)

    script_list = []
    income_list = []
    remain_time = mm.block.get_remain_time()
    own_info = {'block_num': mm.block.block_num,
                'cup': mm.block.cup,
                'need_cup': game_config.dan_grading_list[mm.block.block_num]['promotion_cup_num'],
                'remain_time': remain_time,
                'reward_daily': time.strftime('%F') == mm.block.reward_daily}
    if rank_id == 1:
        rank_own_list = []
        for uid_script_id, score in rank_list:
            uid, script_id = uid_script_id.split('_')
            umm = ModelManager(uid)
            script_id = int(script_id)
            name = umm.user.name
            script_name = umm.block.top_script.get(date, {}).get(script_id, {}).get('name', '')

            script_list.append({'uid': uid,
                                'name': name,
                                'script_id': script_id,
                                'score': score,
                                'role': umm.user.role,
                                'script_name': script_name})
        for script_id,value in mm.block.top_script.get(date, {}).iteritems():
            uid_script_id = '%s_%s'%(mm.uid,script_id)
            script_name = mm.block.top_script.get(date, {}).get(script_id, {}).get('name', '')
            rank_own_list.append({'uid': mm.uid,
                                  'name': mm.user.name,
                                  'script_id': script_id,
                                  'score': br.get_score(uid_script_id),
                                  'role': mm.user.role,
                                  'rank_own': br.get_rank(uid_script_id),
                                  'script_name': script_name})
        return 0, {
            'rank_list': script_list,
            'rank_own': sorted(rank_own_list,key=lambda x:x['rank_own']),
            'own_info': own_info
        }
    elif rank_id == 2:
        income_rank_own_list = []
        for uid, score in rank_list:
            umm = ModelManager(uid)
            name = umm.user.name

            income_list.append({'uid': uid,
                                'role': umm.user.role,
                                'name': name,
                                'score': score, })
        income_rank_own_list.append({'uid': mm.uid,
                                     'role': mm.user.role,
                                     'name': mm.user.name,
                                     'score': br.get_score(mm.uid),
                                     'rank_own': br.get_rank(mm.uid), })

        return 0, {
            'rank_list': income_list,
            'rank_own': income_rank_own_list,
            'own_info': own_info
        }
