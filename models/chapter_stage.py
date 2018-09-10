# -*- coding: utf-8 –*-

import time
import copy
import bisect
import itertools


from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import add_dict
from lib.core.environ import ModelManager

from gconfig import game_config


class Chapter_stage(ModelBase):

    FORMAT = '%Y-%m-%d'

    def __init__(self,uid=None):
        self.uid = uid
        self._attrs = {
            'chapter':{},
            'last_time':0,#最近操作时间
            'next_chapter':[1],  #解锁章节
        }
        super(Chapter_stage,self).__init__(self.uid)

    def pre_use(self):
        now = time.strftime(self.FORMAT)
        if not self.next_chapter:
            self.next_chapter = [1]
        if now != self.last_time:
            self.last_time = now
            for chapter_id,value in self.chapter.iteritems():
                for type_hard,type_v in value.iteritems():
                    for stage_id,s_v in type_v.iteritems():
                        s_v['fight_times'] = 0
            self.save()

ModelManager.register_model('chapter_stage', Chapter_stage)