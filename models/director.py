#! --*-- coding: utf-8 --*--

__author__ = 'ljm'



import time

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.core.environ import ModelManager

from gconfig import game_config
from gconfig import get_str_words
from lib.utils import weight_choice


class Director(ModelBase):
    """导演类
        directors： 所有导演
            {'1-1535098928-2fMmYB':
                {
                  'id': 1,          # 配置中的id
                  'lv': 1,          # 等级
                  'oid': '1-1535098928-2fMmYB', # 唯一id
                  'star': 1
                  }
              }
        """

    _need_diff = ('directors', 'director_box')
    TYPEMAPPING = {1: 'web', 2: 'introduce', 3: 'headhunter'}

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'directors': {},  # 所有导演
            'director_box': 1,  # 导演格子
            'web_times': 0,  # 网站招聘次数
            'web_recover_time': 0,  # 网站招聘刷新时间
            'introduce_times': 0,  # 熟人介绍次数
            'introduce_recover_time': 0,  # 熟人介绍刷新时间
            'headhunter_times': 0,  # 猎头招聘次数
            'refresh_date': '',  # 刷新日期
            'gacha_pool': {},  # gacha
            'add_gacha_times': 0,
        }
        super(Director, self).__init__(self.uid)

    @classmethod
    def _make_oid(cls, director_id):
        """ 生成导演only id

        :param director_id:
        :return:
        """
        return '%s-%s-%s' % (director_id, int(time.time()), salt_generator())

    @classmethod
    def generate_director(cls, director_id, director_config=None, lv=1,pos=0):
        director_oid = cls._make_oid(director_id)
        director_config = director_config or game_config.director[director_id]

        director_dict = {
            'id': director_id,  # 配置id
            'oid': director_oid,  # 唯一id
            'star': director_config.get('star', 1),   # 星级
            'lv': lv,   # 等级
            'pos': pos,
        }

        return director_oid, director_dict

    def add_director(self,director_id,lv=None):
        init_lv = lv or 1
        if director_id in self.all_director:
            return False
        director_oid, director_dict = self.generate_director(director_id,lv=init_lv)
        self.directors[director_oid] = director_dict
        return director_oid

    def pre_use(self):
        today = time.strftime('%F')
        if self.refresh_date != today:
            self.refresh_date = today
            self.web_times = 0
            self.headhunter_times = 0
            self.introduce_times = 0
            self.web_recover_time = int(time.time())
            self.introduce_recover_time = int(time.time())
            self.add_gacha_times = 0
            self.save()



    @property
    def total_times(self):
        return self.web_times + self.headhunter_times + self.introduce_times

    @property
    def all_director_pos(self):
        result = {}
        for director_id, info in self.directors.iteritems():
            if info['pos']:
                result[info['pos']] = director_id
        return result

    @property
    def empty_pos(self):
        all_pos = range(1, self.director_box + 1)
        director_pos = self.all_director_pos.keys()
        return list(set(all_pos) - set(director_pos))


    def recover_need_time(self, tp):
        gacha_cd = game_config.director_gacha_cost[tp]['cd']
        gacha_type = '%s_times'%(self.TYPEMAPPING[tp])
        times = getattr(self,gacha_type)
        if times == 0:
            return 0
        if times >= len(gacha_cd):
            times = -1
        else:
            times -= 1
        return gacha_cd[times] * 60

    def remain_time(self, tp):
        if tp == 3:
            return 0
        now = int(time.time())
        gacha_recover_type = '%s_recover_time' % (self.TYPEMAPPING[tp])
        gacha_recover_time = getattr(self, gacha_recover_type)
        need_time = self.recover_need_time(tp)
        remain_time = gacha_recover_time + need_time - now
        return remain_time if remain_time > 0 else 0

    @property
    def total_gacha_times(self):
        return self.add_gacha_times + game_config.common[86]

    @property
    def all_director(self):
        all_directors = []
        for i, j in self.directors.iteritems():
            all_directors.append(j['id'])
        return all_directors


    def get_director_info(self,director_dict):
        if isinstance(director_dict, str):
            director_dict = self.directors[director_dict]
        config = game_config.director[director_dict['id']]
        pro_base = config['pro']
        att_base = config['att']
        # todo 导演升级属性加成
        pro = [i * 1 for i in pro_base]
        att = att_base * 1


        director_dict['pro'] = pro
        director_dict['att'] = att
        return director_dict



    def refresh_gacha(self, tp):

        gacha_config = game_config.get_director_gacha_mapping().get(tp)
        gacha = []
        g_pool = []
        for id, weight in gacha_config:
            if id not in self.all_director:
                g_pool.append([id, weight])
        if len(g_pool) <= 0:
            return []
        max_num = min(len(g_pool), 3)
        while len(gacha) < max_num:
            gahca_id = []
            while not gahca_id or (gahca_id and gahca_id[0] in gacha):
                gahca_id = weight_choice(g_pool)
            gacha.append(gahca_id[0])
        self.gacha_pool[tp] = gacha
        times = getattr(self,'%s_times' % (self.TYPEMAPPING[tp])) + 1
        setattr(self,'%s_times' % (self.TYPEMAPPING[tp]), times)
        setattr(self,'%s_recover_time' % (self.TYPEMAPPING[tp]), int(time.time()))

        return gacha

ModelManager.register_model('director', Director)


