# -*- coding: utf-8 –*-
import time
from tools.gift import add_mult_gift
from logics.block import Block
from gconfig import game_config
from models.ranking_list import BlockRank
from models.block import get_date_before


def join_award_ceremony(hm):
    mm = hm.mm
    block = Block(mm)
    block.count_cup(is_save=False)
    # if mm.block.award_ceremony:
    #     return 0, {'award_ceremony': mm.block.award_ceremony,
    #                'get_award_ceremony': mm.block.get_award_ceremony,
    #                'reward':mm.block.reward_data}

    data = block.join_award_ceremony()
    data['award_ceremony'] = mm.block.award_ceremony
    data['get_award_ceremony'] = mm.block.get_award_ceremony
    data['reward'] = mm.block.reward_data
    data['remain_time'] = mm.block.get_remain_time()
    mm.block.save()
    return 0, data


def choice_winner(hm):
    mm = hm.mm
    tp = hm.get_argument('tp', 0, is_int=True)
    uid = hm.get_argument('uid', '')
    if not tp:
        return 1, {}  # 选择类型错误
    if not uid:
        return 2, {}  # 未选人
    tp_rank = mm.block.RANK[tp]
    rank_uid = mm.block.get_key_profix(mm.block.block_num, mm.block.block_group,
                                       tp_rank)
    date = get_date_before()
    br = BlockRank(rank_uid, mm.block._server_name, date)
    if br.get_rank(uid) == 1:
        gift = game_config.cup_num.get(tp, {}).get('like_num', [])
        reward = add_mult_gift(mm, gift)
        return 0, {'reward': reward}
    return 0, {}


def congratulation(hm):
    mm = hm.mm
    if mm.block.award_ceremony == 2:
        return 1, {}  # 已祝贺
    gift = [[7, 0, game_config.common[32]]]
    reward = add_mult_gift(mm, gift)
    mm.block.award_ceremony = 2
    mm.block.save()
    return 0, {'reward': reward}


def get_reward(hm):
    mm = hm.mm
    if mm.block.get_award_ceremony:
        return 1, {}  # 已领奖
    block = Block(mm)
    data = block.get_reward()
    return 0, data


def get_daily_reward(hm):
    mm = hm.mm
    now = time.strftime('%F')
    if now == mm.block.reward_daily:
        return 1, {}  # 已领奖
    config = game_config.dan_grading_list
    if not config:
        return 2, {}  # 配置错误
    gift = config.get(mm.block.block_num, {}).get('daily_rewards', [])
    reward = add_mult_gift(mm, gift)
    mm.block.reward_daily = now
    mm.block.save()
    return 0, {'reward': reward}
