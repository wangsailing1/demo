#! --*-- coding: utf-8 --*--

from gconfig import game_config
from tools.gift import add_mult_gift, del_mult_goods

class Business(object):
    def __init__(self,mm):
        self.mm = mm
        self.business = self.mm.business


    def index(self):
        data = {}
        data['business_id'] = self.business.business_id
        data['business_times'] = self.business.business_times
        return 0, data

    def handling(self, select_id, auto):
        config = game_config.business.get(self.business.business_id, {})
        if not config:
            return 11, {}  # 配置错误
        if auto:
            select_id = config['select0']
        if select_id <= 0 or select_id > len(config['select_cost']):
            return 12, {}  # 选项错误
        cost = config['select_cost'][select_id - 1]
        rc, _ = del_mult_goods(self.mm, cost)
        if rc:
            return rc, {}
        gift = config['select_award'][select_id - 1]
        reward = add_mult_gift(self.mm, gift)
        self.business.business_times -= 1
        self.business.business_done.append(self.business.business_id)
        self.business.business_id = self.business.get_business_id()
        self.business.save()
        _ , data = self.index()
        data['reward'] = reward
        return 0, data
