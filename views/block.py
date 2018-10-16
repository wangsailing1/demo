# -*- coding: utf-8 –*-
import time
from tools.gift import add_mult_gift
from logics.block import Block
from gconfig import game_config



def join_award_ceremony(hm):
    mm = hm.mm
    if mm.block.award_ceremony:
        return 0, {'award_ceremony': mm.block.award_ceremony,
                   'get_award_ceremony': mm.block.get_award_ceremony}
    block = Block(mm)
    data = block.join_award_ceremony()
    data['award_ceremony'] = 0
    data['get_award_ceremony'] = 0
    data['reward_data'] = mm.block.reward_data
    return 0, data


def get_reward(hm):
    mm = hm.mm
    if mm.block.get_award_ceremony:
        return 1, {}  #已领奖
    block = Block(mm)
    data = block.get_reward()
    return 0, data


def get_daily_reward(hm):
    mm = hm.mm
    now = time.strftime('%F')
    if now == mm.block.reward_daily:
        return 1, {}  #已领奖
    config = game_config.dan_grading_list
    if not config:
        return 2, {} #配置错误
    gift = config.get(mm.block.block_num,{}).get('daily_rewards',[])
    reward = add_mult_gift(mm,gift)
    mm.block.reward_daily = now
    mm.block.save()
    return 0, {'reward':reward}
