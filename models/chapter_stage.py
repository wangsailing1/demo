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

    UNLOCK_STORY_CHAPTER_ID = 7

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'chapter': {},
            'last_time': 0,  # 最近操作时间
            'next_chapter': [1],  # 解锁章节
            'got_reward_dialogue': [],  # 已领奖剧情关
            'done_chapter_log': [],
            'story_can_unlock': [],  # 可解锁故事
            'story_unlock': [],  # 已解锁故事
            'got_reward_story': [], # 已经领奖的故事
            'story_done': [],  # 已通关故事
        }
        super(Chapter_stage, self).__init__(self.uid)


    def pre_use(self):
        now = time.strftime(self.FORMAT)
        save = False
        if self.unlock_story():
            save = True
        if not self.next_chapter:
            self.next_chapter = [1]
        if now != self.last_time:
            self.last_time = now
            for chapter_id, value in self.chapter.iteritems():
                for type_hard, type_v in value.iteritems():
                    for stage_id, s_v in type_v.iteritems():
                        s_v['fight_times'] = 0
            save = True
        if save:
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
                stage_list = [i for i in stage_config['stage_id'] if i != -1]
                if stage_id < len(stage_list) and stage_config['dialogue_id'][stage_id]:
                    dialogue_list.append(stage_config['dialogue_id'][stage_id])
        return dialogue_list

    def unlock_story(self):
        if self.story_can_unlock:
            return False
        if self.UNLOCK_STORY_CHAPTER_ID not in self.next_chapter:
            return False
        sex = self.mm.user.get_sex()
        config = game_config.story_stage
        for story_id, value in config.iteritems():
            if value['preid'] != -1 or value['gender'] != sex:
                continue
            self.story_can_unlock.append(story_id)
            self.story_unlock.append(story_id)
        return True

    # 第一次听故事
    def first_listen_story(self, chapter_id):
        if chapter_id in self.got_reward_story:
            return False
        return True

    def get_chapter_value(self):
        sum_value = 0
        for j, v in self.chapter.iteritems():
            if v.get(0) and len(v.get(0)) >= len([i for i in game_config.get_chapter_mapping()[j][0]['stage_id'] if i != -1]):
                sum_value += game_config.body_value[41]['value']
            if v.get(1) and len(v.get(1)) >= len([i for i in game_config.get_chapter_mapping()[j][1]['stage_id'] if i != -1]):
                sum_value += game_config.body_value[42]['value']
        return sum_value * 0.0001    # 返回自身加百分比



ModelManager.register_model('chapter_stage', Chapter_stage)
