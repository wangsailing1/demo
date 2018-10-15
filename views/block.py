# -*- coding: utf-8 –*-
import time
from tools.gift import add_mult_gift
from gconfig import game_config
from models.ranking_list import BlockRank
from lib.core.environ import ModelManager
from logics.block import Block

rank_list = [1, 2, 3, 'nv', 'nan', 'medium', 'audience']


def join_award_ceremony(hm):
    mm = hm.mm
    if mm.block.award_ceremony:
        return 0, {'award_ceremony': mm.block.award_ceremony,
                   'get_award_ceremony': mm.block.get_award_ceremony}
    block = Block(mm)
    data = block.join_award_ceremony()
    return 0, data


def get_reward(hm):
    mm = hm.mm
    return 0, {}


def get_daily_reward(hm):
    mm = hm.mm
    return 0, {}
