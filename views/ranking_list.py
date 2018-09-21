# -*- coding: utf-8 –*-
from lib.core.environ import ModelManager


def rank_index(hm):
    mm = hm.mm

    ar = mm.get_obj_tools('appeal_rank')
    otr = mm.get_obj_tools('output_rank')
    aotr = mm.get_obj_tools('alloutput_Rank')

    appeal_rank = ar.get_all_user(withscores=True)
    output_rank = otr.get_all_user(withscores=True)
    alloutput_Rank = aotr.get_all_user(withscores=True)

    appeal_rank_list = []
    output_rank_list = []
    alloutput_Rank_list = []

    for uid_card_id, score in appeal_rank:
        uid, card_id = uid_card_id.split('|')
        umm = ModelManager(uid)
        group_id = umm.card.get_group_id(card_id)
        name = umm.user.name
        appeal_rank_list.append((uid, name, group_id, score))

    for uid_script_id, score in output_rank:
        uid, script_id = uid_card_id.split('|')
        umm = ModelManager(uid)
        name = umm.user.name
        output_rank_list.append((uid, name, script_id, score))

    for uid_group_id, score in alloutput_Rank:
        uid, group_id = uid_card_id.split('|')
        umm = ModelManager(uid)
        name = umm.user.name
        alloutput_Rank_list.append((uid, name, group_id, score))

    return 0, {
        'appeal_rank': appeal_rank_list,
        'output_rank_list': output_rank_list,
        'alloutput_Rank': alloutput_Rank_list
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
