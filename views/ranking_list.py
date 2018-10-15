# -*- coding: utf-8 –*-
from lib.core.environ import ModelManager
from gconfig import game_config
from models.ranking_list import BlockRank,get_date

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
            if umm.script.top_all:
                script_id = umm.script.top_all['id']

            if mm.uid == uid:
                output_rank_own_list.append({'uid': uid,
                                             'name': name,
                                             'script_id': script_id,
                                             'score': score,
                                             'rank_own': ar.get_rank(uid),
                                             'script_name': mm.script.top_all['name']})
            output_rank_list.append({'uid': uid,
                                     'name': name,
                                     'script_id': script_id,
                                     'score': score,
                                     'script_name': umm.script.top_all['name']})
        return 0, {
            'rank_list': output_rank_list[start - 1:end],
            'rank_own': output_rank_own_list,
        }

    else:
        alloutput_rank_own_list = []
        for uid, score in rank_list:
            umm = ModelManager(uid)
            name = umm.user.name
            group_id = umm.script.get_top_group_id()
            if mm.uid == uid:
                alloutput_rank_own_list.append({'uid': uid,
                                                'name': name,
                                                'group_id': group_id,
                                                'score': score,
                                                'rank_own': ar.get_rank(uid),
                                                'group_name': game_config.script_group_object[group_id]['name']})
            alloutput_rank_list.append({'uid': uid,
                                        'name': name,
                                        'group_id': group_id,
                                        'score': score,
                                        'group_name': game_config.script_group_object[group_id]['name']})

        return 0, {
            'rank_list': alloutput_rank_list[start - 1:end],
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
               'uid': uid}


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
               'group_id': mm.script.get_top_group_id(),
               'name': mm.user.name,
               'vip': mm.user.vip,
               'guild_name': mm.user.guild_name,
               'actor_num': len(mm.card.cards),
               'level': mm.user.level,
               'uid': uid}


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

    rank_list = br.get_all_user(withscores=True)

    script_list = []
    income_list = []
    if rank_id == 1:
        rank_own_list = []
        for uid_script_id, score in rank_list:
            uid, script_id = uid_script_id.split('_')
            umm = ModelManager(uid)
            script_id = int(script_id)
            name = umm.user.name
            script_name = umm.block.top_script.get(date, {}).get(script_id)['name']
            if mm.uid in uid_script_id:
                rank_own_list.append({'uid': uid,
                                      'name': name,
                                      'script_id': script_id,
                                      'score': score,
                                      'rank_own': br.get_rank(uid_script_id),
                                      'script_name': script_name})
            script_list.append({'uid': uid,
                                'name': name,
                                'script_id': script_id,
                                'score': score,
                                'script_name': script_name})
        return 0, {
            'rank_list': script_list[start - 1:end],
            'rank_own': rank_own_list
        }
    elif rank_id == 2:
        income_rank_own_list = []
        for uid, score in rank_list:
            umm = ModelManager(uid)
            name = umm.user.name
            if mm.uid == uid:
                income_rank_own_list.append({'uid': uid,
                                                'name': name,
                                                'score': score,
                                                'rank_own': br.get_rank(uid),})
            income_list.append({'uid': uid,
                                'name': name,
                                'score': score,})

        return 0, {
            'rank_list': income_list[start - 1:end],
            'rank_own': income_rank_own_list
        }
