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
    MAPPING = {1: 'like'}

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'chapter': {},
            'last_time': 0,  # 最近操作时间
            'next_chapter': [1],  # 解锁章节
            'got_reward_dialogue': [],  # 已领奖剧情关
            'done_chapter_log': []
        }
        super(Chapter_stage, self).__init__(self.uid)

    def pre_use(self):
        now = time.strftime(self.FORMAT)
        if not self.next_chapter:
            self.next_chapter = [1]
        if now != self.last_time:
            self.last_time = now
            for chapter_id, value in self.chapter.iteritems():
                for type_hard, type_v in value.iteritems():
                    for stage_id, s_v in type_v.iteritems():
                        s_v['fight_times'] = 0
            self.save()

    def get_now_stage(self):
        chapter = max([i for i in self.next_chapter if not game_config.chapter[i]['hard_type']])
        stage = self.chapter.get(chapter, {}).get(0, {}).keys()
        if not stage:
            stage = 1
        else:
            stage = max(stage)
        return '%s-%s' % (chapter, stage)

    def get_chapter_red_dot(self):
        dialogue_list = []
        config = game_config.get_chapter_mapping()
        for chapter, value in self.chapter.iteritems():
            for type_hard, info in value.iteritems():
                stage_id = max(info.keys() if info.keys else [0])
                stage_config = config[chapter][type_hard]
                if stage_id < len(stage_config['stage_id']) and stage_config['dialogue_id'][stage_id]:
                    dialogue_list.append(stage_config['dialogue_id'][stage_id])
        return dialogue_list




ModelManager.register_model('chapter_stage', Chapter_stage)
