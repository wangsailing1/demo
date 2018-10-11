# -*- coding: utf-8 –*-
from lib.core.environ import ModelManager
from gconfig import game_config

rank_mapping = {1: 'appeal_rank', 2: 'output_rank', 3: 'alloutput_rank'}


def rank_index(hm):
    mm = hm.mm
    rank_id = int(hm.get_argument('rank_id', 1))
    start = int(hm.get_argument('start_num', 1))
    end = int(hm.get_argument('end_num', 100))
    if start > end:
        start = 1
        end = 100
    ar = mm.get_obj_tools(rank_mapping[rank_id])

    rank_list = ar.get_all_user(withscores=True)

    appeal_rank_list = []
    output_rank_list = []
    alloutput_rank_list = []

    if rank_id == 1:
        rank_own_list = []
        for uid_group_id, score in rank_list:
            uid, group_id = uid_group_id.split('|')
            umm = ModelManager(uid)
            group_id = int(group_id)
            card_id = umm.card.group_ids[group_id]
            cid = int(card_id.split('-')[0])
            card_name = game_config.card_basis[cid]['name']
            name = umm.user.name
            if mm.uid in uid_group_id:
                rank_own_list.append({'uid': uid,
                                      'name': name,
                                      'group_id': group_id,
                                      'score': score,
                                      'rank_own': ar.get_rank(uid_group_id),
                                      'card_name': card_name})
            appeal_rank_list.append({'uid': uid,
                                     'name': name,
                                     'group_id': group_id,
                                     'score': score,
                                     'card_name': card_name})
        return 0, {
            'rank_list': appeal_rank_list[start - 1:end],
            'rank_own': rank_own_list
        }

    elif rank_id == 2:
        output_rank_own_list = []
        for uid, score in rank_list:
            umm = ModelManager(uid)
            name = umm.user.name
            script_id = umm.script.top_all.keys()[0]
            if mm.uid == uid:
                output_rank_own_list.append({'uid': uid,
                                             'name': name,
                                             'script_id': script_id,
                                             'score': score,
                                             'rank_own': ar.get_rank(uid),
                                             'script_name':''})
            output_rank_list.append({'uid': uid,
                                     'name': name,
                                     'script_id': script_id,
                                     'score': score,
                                     'script_name': ''})
        return 0, {
            'rank_list': output_rank_list[start - 1:end],
            'rank_own': output_rank_own_list,
        }

    else:
        alloutput_rank_own_list = []
        for uid, score in rank_list:
            umm = ModelManager(uid)
            name = umm.user.name
            group_id = umm.script.get_top_group()
            if mm.uid == uid:
                alloutput_rank_own_list.append({'uid': uid,
                                                'name': name,
                                                'group_id': group_id,
                                                'score': score,
                                                'rank_own': ar.get_rank(uid),
                                                'group_name':''})
            alloutput_rank_list.append({'uid': uid,
                                        'name': name,
                                        'group_id': group_id,
                                        'score': score,
                                        'group_name': ''})

        return 0, {
            'rank_list': alloutput_rank_list[start - 1:end],
            'rank_own': alloutput_rank_own_list
        }


def get_script_info(hm):
    mm = hm.mm
    script_id = hm.get_argument('script_id', 0)
    if not script_id:
        return 1, {}
    return 0, {'script_info': mm.script.top_script[script_id]}


def get_group_info(hm):
    mm = hm.mm
    group_id = hm.get_argument('group_id', 0)
    if not group_id:
        return 1, {}
    return 0, {'group_info': mm.script.top_group[group_id]}


def get_user_info(hm):
    mm = hm.mm
    uid = hm.get_argument('uid', '')
    if not uid:
        return 1, {}
    umm = ModelManager(uid)

    return 0, {
        'info': umm.user.script_income
    }
