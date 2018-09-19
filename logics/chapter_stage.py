# -*- coding: utf-8 –*-

import random

from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils import weight_choice
import copy
import random


class Chapter_stage(object):
    MAPPING = {5: 'special_rate2', 6: 'special_rate1'}

    def __init__(self, mm):
        self.mm = mm
        self.chapter_stage = self.mm.chapter_stage

    def chapter_stage_fight(self, stage, type_hard, align='', auto=False, times=1):
        config = game_config.get_chapter_mapping()
        chapter, stage = [int(i) for i in stage.split('-')]
        config_s = game_config.chapter_stage
        if chapter not in config:
            return 11, {}  # 章节错误
        if type_hard not in config[chapter]:
            return 12, {}  # 难度错误
        if stage > len(config[chapter][type_hard]['stage_id']):
            return 13, {}  # 关卡错误
        stage_id = config[chapter][type_hard]['stage_id'][stage - 1]
        if not config:
            return 14, {}  # 配置错误
        if not stage_id:
            stage_id = config[chapter][type_hard]['dialogue_id'][stage - 1]
            config = game_config.avg_dialogue
            if stage_id not in config:
                return 25, {}
            config_reward = config[stage_id]['add_value']
            data = {}
            if chapter not in self.chapter_stage.chapter:
                self.chapter_stage.chapter[chapter] = {}
            if type_hard not in self.chapter_stage.chapter[chapter]:
                self.chapter_stage.chapter[chapter][type_hard] = {}
            if stage in self.chapter_stage.chapter[chapter][type_hard]:
                data['next_chapter'] = self.chapter_stage.next_chapter
                data['chapter'] = self.chapter_stage.chapter
                return 0, data
            next_chapter = self.unlock_chapter(chapter, type_hard, stage)
            if next_chapter and not set(next_chapter) - set(self.chapter_stage.next_chapter):
                self.chapter_stage.next_chapter.extend(next_chapter)
            self.chapter_stage.chapter[chapter][type_hard][stage] = {}
            if not auto:
                next_chapter = self.unlock_chapter(chapter, type_hard, stage)
                if next_chapter and not set(next_chapter) - set(self.chapter_stage.next_chapter):
                    self.chapter_stage.next_chapter.extend(next_chapter)
            data['next_chapter'] = self.chapter_stage.next_chapter
            data['chapter'] = self.chapter_stage.chapter
            reward = add_mult_gift(self.mm, config_reward)
            data['reward'] = reward
            self.chapter_stage.save()
            return 0, data
        if stage_id not in config_s:
            return 15, {}  # 关卡错误
        if self.mm.user.level < config_s[stage_id]['lv_unlocked']:
            return 24, {}  # 等级不够

        if auto:
            if chapter not in self.chapter_stage.chapter or type_hard not in self.chapter_stage.chapter[chapter] \
                    or stage not in self.chapter_stage.chapter[chapter][type_hard]:
                return 21, {}  # 尚未通关
            if config[chapter][type_hard]['script_end_level'] > self.chapter_stage.chapter[chapter][type_hard][
                stage].get('star', 0):
                return 22, {}  # 未达到扫荡星级
        stage_config = config_s[stage_id]
        script_id = stage_config['script_id']
        if stage_config['challenge_limit'] < self.chapter_stage.chapter.get(chapter, {}).get(type_hard, {}).get(stage,
                                                                                                                {}).get(
            'fight_times', 0) + times:
            return 16, {}  # 剩余次数不足
        need_point = stage_config['start_cost'] * times
        if need_point > self.mm.user.action_point:
            return 17, {}  # 体力不足
        is_first = self.is_first(chapter, type_hard, stage)
        if not auto:
            align = align.split('_')
            if len(align) % 2:
                return 20, {}  # 参数错误
            align = {int(align[i * 2]): align[i * 2 + 1] for i in range(len(align) / 2)}
        rc, data = self.fight(stage_id, align, auto=auto, times=times, is_first=is_first)
        if not rc:
            if data.get('win',True):
                add_player_exp = stage_config['player_exp'] * times
                add_fight_exp = stage_config['fight_exp'] * times
                script_type = game_config.script[script_id]['style']
                card_config = game_config.card_basis
                if not auto:
                    for k, v in align.iteritems():
                        if v not in self.mm.card.cards:
                            continue
                        if script_type in [i[0] for i in card_config[self.mm.card.cards[v]['id']]['tag_script']]:
                            self.mm.card.add_style_exp(v, script_type, add_fight_exp)
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
                for k, v in data['gift'].iteritems():
                    all_gift.extend(v)
                    rewards[k] = add_mult_gift(self.mm, v)
                if not auto:
                    next_chapter = self.unlock_chapter(chapter, type_hard, stage)
                    if next_chapter and not set(next_chapter) - set(self.chapter_stage.next_chapter):
                        self.chapter_stage.next_chapter.extend(next_chapter)
                reward = add_mult_gift(self.mm, all_gift)
                self.mm.user.save()
                self.chapter_stage.save()
                data['old_level'] = old_level
                data['new_level'] = self.mm.user.level
                data['reward'] = reward
                data['rewards'] = rewards
                data['next_chapter'] = self.chapter_stage.next_chapter
        return rc, data

    # 战斗（只计算战斗结果,星级过关）
    def fight(self, stage_id, align, save=True, auto=False, times=1, is_first=False):
        config = game_config.chapter_stage
        stage_config = config[stage_id]
        script_id = stage_config['script_id']

        data = {}
        if not auto:
            tag_score = {}
            script_config = game_config.script[script_id]
            chapter_enemy = {i[0]: str(i[1]) for i in stage_config['chapter_enemy']}

            for role_id, enemy_id in chapter_enemy.iteritems():
                if align.get(role_id, '') != enemy_id:
                    return 18, {}  # 助战演员错误
            for role_id, card_id in align.iteritems():
                if role_id not in script_config['role_id']:
                    return 19, {}  # 角色错误
                if role_id in chapter_enemy:
                    score = self.tag_score(script_id, role_id, card_id, is_enemy=True)
                    tag_score[card_id] = score
                    continue
                if card_id not in self.mm.card.cards:
                    return 23, {}  # 有未拥有的艺人

                # 计算擅长角色，擅长剧本得分
                score = self.tag_score(script_id, role_id, card_id)
                tag_score[card_id] = score

            fight_data = {}
            rounds = game_config.common.get(23, {}).get('value', 2)
            all_score = 0
            for round_num in range(1, rounds + 1):
                if round_num not in fight_data:
                    fight_data[round_num] = {}
                for role_id, card_id in align.iteritems():

                    # 助战卡牌
                    if role_id in chapter_enemy:
                        # 卡牌两个必触发属性伤害
                        attr = game_config.script_role[role_id]['role_attr']
                        hurts = {'more_attr': {},
                                 'attr': {}}
                        for attr_id in attr:
                            hurt = self.get_hurt(attr_id, card_id, tag_score[card_id], is_enemy=True)
                            hurts['attr'][attr_id] = hurt
                            all_score += hurt
                        fight_data[round_num][card_id] = hurts
                        # 概率触发属性伤害
                        config = game_config.chapter_enemy[int(card_id)]
                        more_attr = [[5, config[self.MAPPING[5]]], [6, config[self.MAPPING[6]]]]
                        more_attr = weight_choice(more_attr)
                        hurt = self.get_hurt(more_attr[0], card_id, tag_score[card_id], is_enemy=True)
                        hurts['more_attr'] = {}
                        hurts['more_attr'][more_attr[0]] = hurt
                        all_score += hurt
                        fight_data[round_num][card_id] = hurts
                        continue

                    # 卡牌两个必触发属性伤害
                    attr = game_config.script_role[role_id]['role_attr']
                    hurts = {'more_attr': {},
                             'attr': {}}
                    for attr_id in attr:
                        hurt = self.get_hurt(attr_id, card_id, tag_score[card_id])
                        all_score += hurt
                        hurts['attr'][attr_id] = hurt
                    fight_data[round_num][card_id] = hurts
                    # 概率触发属性伤害 special_rate2 5娱乐 special_rate1 6艺术
                    card_info = self.mm.card.get_card(card_id)
                    config = game_config.card_basis[card_info['id']]
                    more_attr = [[5, config[self.MAPPING[5]]], [6, config[self.MAPPING[6]]]]
                    more_attr = weight_choice(more_attr)
                    hurt = self.get_hurt(more_attr[0], card_id, tag_score[card_id])
                    hurts['more_attr'][more_attr[0]] = hurt
                    all_score += hurt
                    fight_data[round_num][card_id] = hurts

            # 总熟练度，以后添加
            all_pro = 10
            m = game_config.common[10]['value']
            all_score = int(all_score * (1 + all_pro / m)) * 10
            score_config = script_config['stage_score']
            star = self.get_star(all_score, score_config)
            data['win'] = star >= 2
            data['gift'] = []
            data['fight_data'] = fight_data
            data['all_score'] = all_score
            data['star'] = star
            if not data['win']:
                return 0, data

        gift = self.get_reward(stage_id, times=times, is_first=is_first)
        data['gift'] = gift
        return 0, data

    def get_star(self, all_score, score_config):
        for level, score in enumerate(score_config, 1):
            if level == 1 and all_score < score:
                return level
            elif level == len(score_config) and all_score >= score:
                return level + 1
            elif score <= all_score < score_config[level]:
                return level + 1

    def get_hurt(self, attr_id, card_id, score, is_enemy=False):
        if is_enemy:
            card_info = game_config.chapter_enemy[int(card_id)]
            v = card_info['charpro'][attr_id - 1]
            rate = card_info['dps_rate']
            dps_rate = random.randint(rate[0], rate[1]) / 10000.0
            hurt = max(int(v * dps_rate), 1)
        else:
            card_info = self.mm.card.get_card(card_id)
            v = card_info['char_pro'][attr_id - 1]
            # 计算普通
            love_lv = card_info.get('love_lv', 0)
            rate = game_config.card_love_level[love_lv]['dps_rate']
            dps_rate = random.randint(rate[0], rate[1]) / 10000.0
            hurt = max(int(v * dps_rate), 1)
        # 是否暴击
        if self.is_crit(card_id, score, is_enemy=is_enemy):
            # 暴击伤害
            hurt = self.crit_hurt(hurt, score)
        return hurt

    def crit_hurt(self, hurt, score):
        crit = 1.1 + score / 100.0
        hurt = int(hurt * crit)
        return hurt

    def is_crit(self, card_id, score, is_enemy=False):
        if is_enemy:
            crit_rate_base = game_config.chapter_enemy[int(card_id)]['crit_rate_base']
        else:
            card_info = self.mm.card.get_card(card_id)
            crit_rate_base = game_config.card_basis[card_info['id']]['crit_rate_base']
        crit_rate = crit_rate_base + score / 100
        return crit_rate > random.randint(1, 10000)

    def tag_score(self, script_id, role_id, card_id, is_enemy=False):
        score = 0
        if is_enemy:
            id = game_config.chapter_enemy[int(card_id)]['card_id']
            card_info = game_config.card_basis[id]
            card_tag = self.mm.card.card_tag(card_info)
        else:
            card_info = self.mm.card.get_card(card_id)
            card_tag = self.mm.card.card_tag(card_info)
        tag_role = game_config.script_role[role_id]['tag_role']
        script_config = game_config.script[script_id]
        tag_script = script_config['tag_script']
        for tag in tag_role:
            if tag in card_tag['tag_role']:
                tag_num = card_tag['tag_role'][tag]
                score += game_config.tag_score.get(tag_num, {}).get('score', 0)
        for tag in tag_script:
            if tag in card_tag['tag_script']:
                tag_num = card_tag['tag_script'][tag]
                score += game_config.tag_score.get(tag_num, {}).get('score', 0)
        return score

    # 是否首通
    def is_first(self, chapter, type_hard, stage):
        if chapter in self.chapter_stage.chapter and type_hard in self.chapter_stage.chapter[chapter] \
                and stage in self.chapter_stage.chapter[chapter][type_hard]:
            return False
        return True

    # 奖励
    def get_reward(self, stage_id, times=1, is_first=False):
        config = game_config.chapter_stage
        stage_config = config[stage_id]
        gift = {}

        for times_ in xrange(1, times + 1):
            for i in range(1, 4):
                random_num = 'random_num%s' % i
                random_reward = 'random_reward%s' % i
                for _ in xrange(stage_config[random_num]):
                    gift[times_] = [(weight_choice(stage_config[random_reward])[:-1])]

        if is_first:
            gift['first_reward'] = (stage_config['first_reward'])

        return gift

    def get_dialogue_reward(self, now_stage, choice_stage, card_id):
        config = game_config.avg_dialogue
        card_config = game_config.card_basis
        if now_stage not in config:
            return 11, {}  # 剧情关配置错误
        if choice_stage not in config[now_stage]['option_team']:
            return 12, {}  # 剧情选择错误
        if card_id not in card_config:
            return 13, {}  # 卡牌id错误
        group_id = card_config[card_id]['group']

        gift = config[choice_stage]['reward']
        add_val = config[choice_stage]['add_value']
        self.chapter_stage.got_reward_dialogue.append(now_stage)
        add_value = {}
        for k, v in add_val:
            if group_id not in self.mm.card.attr:
                self.mm.card.attr[group_id] = {}
            attr = self.chapter_stage.MAPPING[k]
            self.mm.card.attr[group_id][attr] = self.mm.card.attr[group_id].get(attr, 0) + v
            add_value[attr] = add_value.get(attr, 0) + v
        reward = add_mult_gift(self.mm, gift)
        self.mm.card.save()
        self.chapter_stage.save()

        return 0, {
            'add_value': add_value,
            'reward': reward
        }

    # 解锁章节
    def unlock_chapter(self, chapter, type_hard, stage, save=False):
        config = game_config.get_chapter_mapping()
        all_stage = len(config[chapter][type_hard]['stage_id'])
        if stage >= all_stage:
            return config[chapter][type_hard]['next_chapter']
        return []
