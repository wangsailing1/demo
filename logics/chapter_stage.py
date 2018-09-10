# -*- coding: utf-8 –*-

import random

from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils import weight_choice
import copy
import random

class Chapter_stage(object):

    def __init__(self,mm):
        self.mm = mm
        self.chapter_stage = self.mm.chapter_stage

    def chapter_stage_fight(self,stage,type_hard,align='',auto=False,times=1):
        config = game_config.get_chapter_mapping()
        chapter,stage = [int(i) for i in stage.split('-')]
        print chapter,stage
        config_s = game_config.chapter_stage
        if chapter not in config:
            return 11, {}  #章节错误
        if type_hard not in config[chapter]:
            return 12, {}  #难度错误
        if stage > len(config[chapter][type_hard]['stage_id']):
            return 13, {}  #关卡错误
        stage_id = config[chapter][type_hard]['stage_id'][stage-1]
        if not config:
            return 14, {}  #配置错误
        if stage_id  and stage_id not in config_s:
            return 15, {}  #关卡错误
        if self.mm.user.level < config_s[stage_id]['lv_unlocked']:
            return 24, {}  #等级不够
        if not stage_id:
            if chapter not in self.chapter_stage.chapter:
                self.chapter_stage.chapter[chapter] = {}
            if type_hard not in self.chapter_stage.chapter[chapter]:
                self.chapter_stage.chapter[chapter][type_hard] = {}
            if stage in self.chapter_stage.chapter[chapter][type_hard]:
                return 0, {}
            next_chapter = self.unlock_chapter(chapter, type_hard, stage)
            if next_chapter and not set(next_chapter) - set(self.chapter_stage.next_chapter):
                self.chapter_stage.next_chapter.extend(next_chapter)
            self.chapter_stage.chapter[chapter][type_hard][stage] = {}
            self.chapter_stage.save()
            return 0, {}
        if auto:
            if chapter not in self.chapter_stage.chapter or type_hard not in self.chapter_stage.chapter[chapter] \
                    or stage not in self.chapter_stage.chapter[chapter][type_hard]:
                return 21, {}  #尚未通关
            if config[chapter][type_hard]['script_end_level'] > self.chapter_stage.chapter[chapter][type_hard][stage].get('star',0):
                return 22, {}  #未达到扫荡星级
        stage_config = config_s[stage_id]
        script_id = stage_config['script_id']
        if stage_config['challenge_limit'] < self.chapter_stage.chapter.get(chapter,{}).get(type_hard,{}).get(stage,{}).get('fight_times',0) + times:
            return 16, {}  #剩余次数不足
        need_point = stage_config['start_cost'] * times
        if need_point > self.mm.user.action_point:
            return 17, {}  #体力不足
        is_first = self.is_first(chapter, type_hard,stage)
        if not auto:
            align = align.split('_')
            if len(align) % 2:
                return 20, {}  # 参数错误
            align = {int(align[i * 2]): align[i * 2 + 1] for i in range(len(align) / 2)}
        rc,data = self.fight(stage_id,align,auto=auto,times=times,is_first=is_first)
        if not rc:
            if data['win']:
                add_player_exp = stage_config['player_exp'] * times
                add_fight_exp = stage_config['fight_exp'] * times
                script_type = game_config.script[script_id]['style']
                card_config = game_config.card_basis
                if not  auto:
                    for k,v in align.iteritems():
                        if v not in self.mm.card.cards:
                            continue
                        if script_type in [i[0] for i in card_config[self.mm.card.cards[v]['id']]['tag_script']]:
                            self.mm.card.add_style_exp(v,script_type,add_fight_exp)
                self.mm.user.action_point -= need_point
                if chapter not in self.chapter_stage.chapter:
                    self.chapter_stage.chapter[chapter] = {}
                if type_hard not in self.chapter_stage.chapter[chapter]:
                    self.chapter_stage.chapter[chapter][type_hard] = {}
                if stage not in self.chapter_stage.chapter[chapter][type_hard]:
                    self.chapter_stage.chapter[chapter][type_hard][stage] = {}
                fight_time = self.chapter_stage.chapter[chapter][type_hard][stage].get('fight_times', 0)
                self.chapter_stage.chapter[chapter][type_hard][stage]['fight_times'] = fight_time + times
                old_level = copy.copy(self.mm.user.level)
                if not auto:
                    if data['star'] > self.chapter_stage.chapter[chapter][type_hard][stage]['star']:
                        self.chapter_stage.chapter[chapter][type_hard][stage]['star'] = data['star']

                self.mm.user.add_player_exp(add_player_exp)
                rewards = {}
                all_gift = []
                for k,v in data['gift'].iteritems():
                    all_gift.extend(v)
                    rewards[k] = add_mult_gift(self.mm,v)
                if not auto:
                    next_chapter = self.unlock_chapter(chapter,type_hard,stage)
                    if next_chapter and not set(next_chapter) - set(self.chapter_stage.next_chapter):
                        self.chapter_stage.next_chapter.extend(next_chapter)
                reward =  add_mult_gift(self.mm,all_gift)
                self.mm.user.save()
                self.chapter_stage.save()
                data['old_level'] = old_level
                data['new_level'] = self.mm.user.level
                data['reward'] = reward
                data['rewards'] = rewards
                data['next_stage'] = self.chapter_stage.next_chapter
        return rc,data


    #战斗（只计算战斗结果,星级过关）
    def fight(self,stage_id,align,save=True,auto=False,times=1,is_first=False):
        config = game_config.chapter_stage
        stage_config = config[stage_id]
        script_id = stage_config['script_id']

        data = {}
        if not auto:
            script_config = game_config.script[script_id]
            chapter_enemy = {i[0]:str(i[1]) for i in stage_config['chapter_enemy']}
            for role_id,enemy_id in chapter_enemy.iteritems():
                if align.get(role_id,'') != enemy_id:
                    return 18, {}  #助战演员错误
            for role_id,card_id in align.iteritems():
                if role_id not in script_config['role_id']:
                    return 19, {}  #角色错误
                if role_id in chapter_enemy:
                    continue
                if card_id not in self.mm.card.cards:
                    return 23, {}  #有未拥有的艺人


            #战斗
            pass
            #失败
            data['win'] = random.choice((False,True))
            if not data['win']:
                return 0, data
            star = random.choice(range(1,11))
            data['star'] = star
        gift = self.get_reward(stage_id, times=times, is_first=is_first)
        data['win'] = True
        data['gift'] = gift
        return 0, data

    #是否首通
    def is_first(self,chapter, type_hard ,stage):
        if chapter in self.chapter_stage.chapter and type_hard in self.chapter_stage.chapter[chapter] \
                and stage in self.chapter_stage.chapter[chapter][type_hard]:
            return False
        return True


    #奖励
    def get_reward(self,stage_id,times=1,is_first=False):
        config = game_config.chapter_stage
        stage_config = config[stage_id]
        gift = {}

        for times_ in xrange(1,times + 1):
            for i in range(1,4):
                random_num = 'random_num%s'%i
                random_reward = 'random_reward%s'%i
                for _ in xrange(stage_config[random_num]):
                    gift[times_] = [(weight_choice(stage_config[random_reward])[:-1])]

        if is_first:
            gift['first_reward'] = (stage_config['first_reward'])

        return gift

    #解锁章节
    def unlock_chapter(self,chapter,type_hard,stage,save=False):
        config = game_config.get_chapter_mapping()
        all_stage = len(config[chapter][type_hard]['stage_id'])
        if stage >= all_stage:
            return config[chapter][type_hard]['next_chapter']
        return []

