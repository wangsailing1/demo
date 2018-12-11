#! --*-- coding: utf-8 --*--


from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice



class Toy(ModelBase):

    def __init__(self,uid):
        self.uid = uid
        self._attrs = {
            'toy_list': {},  # 奖池
            'version': 0,  # 版本号
            'toy_num': 0,  # 本次抓取次数
            'all_toy_num': 0 # 总抓取次数
        }
        super(Toy, self).__init__(self.uid)

    def pre_use(self):
        version = 1
        save = False
        if version != self.version:
            self.version = version
            self.init_reward()
            self.toy_num = 0
            self.all_toy_num = 0
            save = True
        if save:
            self.save()

    def init_reward(self, save=False):
        config = game_config.rmb_gacha_control[1]
        num = 1
        toy_reward_weight = game_config.toy_reward_weight_mapping()
        for group_id, group_num in config['group_num']:
            for _ in range(group_num):
                weight_config = toy_reward_weight[group_id]
                reward_id = weight_choice(weight_config)[0]
                self.toy_list[num] = {'reward_id': reward_id, 'num': 0}
                num += 1
        if save:
            self.save()

    def refresh_reward(self,save=False):
        self.init_reward()
        self.toy_num = 0
        if save:
            self.save()

ModelManager.register_model('toy', Toy)





