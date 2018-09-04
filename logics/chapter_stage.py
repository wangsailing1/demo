# -*- coding: utf-8 –*-

import random

from gconfig import game_config
from tools.gift import del_mult_goods,add_gift


class Chapter_stage(object):

    def __init__(self,mm):
        self.mm = mm
        self.chapter_stage = self.mm.chapter_stage

    def chapter_stage(self,stage,type_hard,align):
        config = game_config.get_chapter_mapping()
        chapter,stage = [int(i) for i in stage.split('-')]
        if chapter not in config:
            return 11, {}  #章节错误
        stage_ = 'stage_id'+ str(stage)
        if type_hard not in config[chapter]:
            return 12, {}  #难度错误
        if stage_ not in config[chapter][type_hard]:
            return 13, {}  #关卡错误
        stage_id = config[chapter][type_hard][stage_]
        if not stage_id:
            if chapter not in self.chapter_stage.chapter:
                self.chapter_stage.chapter[chapter]={}
            if stage in self.chapter_stage.chapter[chapter]:
                return 0, {}
            self.chapter_stage.chapter[chapter][stage] = {}
            self.chapter_stage.save()
            return 0, {}
        rc,data = self.fight(stage_id,align)

        return 0,{}

    def aotu_sweep(self):
        pass


    def fight(self,chapter,stage,type_hard,align):
        pass

    def get_reward(self):

        return