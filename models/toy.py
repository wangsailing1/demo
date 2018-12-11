#! --*-- coding: utf-8 --*--


from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config
from lib.utils import weight_choice
from lib.utils import generate_rank_score, round_float_or_str
import settings



class Toy(ModelBase):

    def __init__(self,uid):
        self.uid = uid
        self._attrs = {
            'toy_list': {},  # 奖池
            'version': 0,  # 版本号
            'toy_num': 0,  # 本次抓取次数
            'all_toy_num': 0, # 总抓取次数
        }
        server = self.get_server_name(self.uid)
        father_server = settings.get_father_server(server)
        self._key = self.make_key(self.__class__.__name__, server_name=father_server)
        self.fredis = self.get_father_redis(father_server)
        super(Toy, self).__init__(self.uid)

    def pre_use(self):
        version = self.get_version()
        save = False
        if version != self.version:
            self.version = version
            self.init_reward()
            self.toy_num = 0
            self.all_toy_num = 0
            save = True
        if save:
            self.save()

    def get_version(self):
        return 1

    def init_reward(self, save=False):
        """
        :param save: 
        :return: 
        """
        config = game_config.rmb_gacha_control[self.version]
        toy_reward_weight = game_config.toy_rmb_reward_weight_mapping()
        num = 1
        for group_id, group_num in config['group_num']:
            for _ in range(group_num):
                weight_config = toy_reward_weight[group_id]
                reward_id = weight_choice(weight_config)[0]
                self.toy_list[num] = {'reward_id': reward_id, 'num': 0}
                num += 1
        if save:
            self.save()

    def refresh_reward(self, save=False):
        self.init_reward()
        self.toy_num = 0
        if save:
            self.save()

    def add_rank(self,uid,score):
        self.fredis.zadd(self._key, uid, generate_rank_score(score))

    def get_all_user(self, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str):
        return self.fredis.zrevrange(self._key, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_score(self, uid, score_cast_func=round_float_or_str):
        score = self.fredis.zscore(self._key, uid) or 0
        score = score_cast_func(score)

        return score

    def get_rank(self, uid):
        rank = self.fredis.zrevrank(self._key, uid)
        if rank is None:
            rank = -1
        return rank + 1

class FreeToy(Toy):

    def __int__(self,uid):
        super(Toy, self).__init__(self.uid)

    def get_version(self):
        return 2

    def init_reward(self, save=False):
        """
        :param save: 
        :return: 
        """
        config = game_config.rmb_gacha_control[self.version]
        toy_reward_weight = game_config.toy_rmb_reward_weight_mapping()
        num = 1
        for group_id, group_num in config['group_num']:
            for _ in range(group_num):
                weight_config = toy_reward_weight[group_id]
                reward_id = weight_choice(weight_config)[0]
                self.toy_list[num] = {'reward_id': reward_id, 'num': 0}
                num += 1
        if save:
            self.save()



ModelManager.register_model('toy', Toy)
ModelManager.register_model('freetoy', FreeToy)





