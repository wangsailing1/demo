# -*- coding: utf-8 –*-
from lib.core.environ import ModelManager
from gconfig import game_config


def rank_index(hm):
    mm = hm.mm

    ar = mm.get_obj_tools('appeal_rank')
    otr = mm.get_obj_tools('output_rank')
    aotr = mm.get_obj_tools('alloutput_rank')

    appeal_rank = ar.get_all_user(withscores=True)
    output_rank = otr.get_all_user(withscores=True)
    alloutput_rank = aotr.get_all_user(withscores=True)

    appeal_rank_list = []
    output_rank_list = []
    alloutput_rank_list = []

    for uid_group_id, score in appeal_rank:
        uid, group_id = uid_group_id.split('|')
        umm = ModelManager(uid)
        print uid, group_id
        group_id = int(group_id)
        card_id = umm.card.group_ids[group_id]
        cid = int(card_id.split('-')[0])
        card_name = game_config.card_basis[cid]['name']
        name = umm.user.name
        appeal_rank_list.append({'uid': uid,
                                 'name': name,
                                 'group_id': group_id,
                                 'score': score,
                                 'card_name': card_name})

    output_rank_own_list = []
    for uid_script_id, score in output_rank:
        uid, script_id = uid_script_id.split('|')
        umm = ModelManager(uid)
        name = umm.user.name
        script_id = int(script_id)
        if mm.uid in uid_script_id:
            output_rank_own_list.append({'uid': uid,
                                         'name': name,
                                         'script_id': script_id,
                                         'score': score,
                                         'uid_script_id': uid_script_id})
        output_rank_list.append({'uid': uid,
                                 'name': name,
                                 'script_id': script_id,
                                 'score': score, })

    alloutput_rank_own_list = []
    for uid_group_id, score in alloutput_rank:
        uid, group_id = uid_group_id.split('|')
        umm = ModelManager(uid)
        name = umm.user.name
        group_id = int(group_id)
        if mm.uid in uid_group_id:
            alloutput_rank_own_list.append({'uid': uid,
                                            'name': name,
                                            'group_id': group_id,
                                            'score': score,
                                            'uid_group_id': uid_group_id})
        alloutput_rank_list.append({'uid': uid,
                                    'name': name,
                                    'group_id': group_id,
                                    'score': score, })

    for uid_dict in output_rank_own_list:
        uid = uid_dict['uid_script_id']
        uid_dict['rank_own'] = otr.get_rank(uid)
    for uid_dict in alloutput_rank_own_list:
        uid = uid_dict['uid_group_id']
        uid_dict['rank_own'] = aotr.get_rank(uid)
    return 0, {
        'appeal_rank': appeal_rank_list,
        'output_rank_list': output_rank_list,
        'output_rank_own': output_rank_own_list,
        'alloutput_rank_list': alloutput_rank_list,
        'alloutput_rank_own': alloutput_rank_own_list
    }


def get_script_info(hm):
    mm = hm.mm
    script_id = hm.get_argument('script_id', 0)
    return 0, {'script_info': mm.script.own_script}


def get_user_info(hm):
    mm = hm.mm
    uid = hm.get_argument('uid', '')
    umm = ModelManager(uid)

    return 0, {
        'info': umm.user.name
    }
