#! --*-- coding: utf-8 --*--

__author__ = 'ljm'



import time
import math
import copy
import bisect
import itertools

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import add_dict
from lib.core.environ import ModelManager

from gconfig import game_config
from gconfig import get_str_words


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

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'directors': {}, # 所有导演
            'director_box': 0,  # 导演格子
            'web_times': 0,  # 网站招聘次数
            'web_recover_time': 0,  # 网站招聘刷新时间
            'introduce_times': 0,  # 熟人介绍次数
            'introduce_recove_times': 0,  # 熟人介绍刷新时间
            'headhunter_times': 0,  # 猎头招聘次数
        }

    @classmethod
    def _make_oid(cls, director_id):
        """ 生成导演only id

        :param director_id:
        :return:
        """
        return '%s-%s-%s' % (director_id, int(time.time()), salt_generator())

    @classmethod
    def generate_director(cls, director_id, director_config=None, lv=1):
        director_oid = cls._make_oid(director_id)
        director_config = director_config or game_config.director[director_id]

        director_dict = {
            'id': director_id,  # 配置id
            'oid': director_oid,  # 唯一id
            'star': director_config.get('star', 1),   # 星级
            'lv': lv,   # 等级
        }

        return director_oid, director_dict

    def add_director(self,director_id,lv=None):
        init_lv = lv or 1
        director_oid, director_dict = self.generate_director(director_id,lv=init_lv)
        self.directors[director_oid] = director_dict
        return director_oid

    def pre_use(self):
        pass
