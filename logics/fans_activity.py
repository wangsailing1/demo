#! --*-- coding: utf-8 --*--

from gconfig import game_config

class FansActivity(object):
    def __init__(self, mm=None):
        self.mm = mm

    def event(self, activity_id, cards):
        cards = cards.split('_')
        if cards.count('0') == len(cards):
            return 12, {}  # 没有艺人参加
        config = game_config.fans_activity.get(activity_id,{})
        for k,card_id in enumerate(cards):
            if card_id in ['0']:
                continue
            if card_id not in self.mm.card.cards:
                return 11, {}  # 卡牌错误
            need = config['card_need'][k]
