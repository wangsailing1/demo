# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
import random
from gconfig import game_config

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import weight_choice


class ScriptLogic(object):
    def __init__(self, mm):
        self.mm = mm

    def index(self):
        script = self.mm.script
        if not script.script_pool:
            step = 0
        else:
            step = 1
            if script.cur_script:
                step = 2
                if script.cur_script['card']:
                    step = 3
                if script.cur_script['style']:
                    step = 4

        return 0, {
            'own_script': script.own_script,
            'step': step,
            'script_pool': script.script_pool,
            'cur_script': script.cur_script,
            'scripts': script.scripts,
            'style_log': script.style_log,
        }

    def pre_filming(self, ):
        # todo 许可证判断 use_item

        script = self.mm.script
        script.pre_filming()
        script.save()
        rc, data = self.index()
        return rc, data

    def filming(self, script_id, name):
        script = self.mm.script

        if script_id not in script.script_pool:
            return 1, {}  # 不可选剧本

        if script.cur_script:
            return 2, {}  # 拍摄中

        if script.script_pool[script_id]:
            return 3, {}  # 已拍摄

        film = script.make_film(script_id, name)
        script.cur_script = film

        script.script_pool[script_id] = 1
        script.save()
        rc, data = self.index()
        return rc, data

    def set_card(self, role_card):
        """

        :param script_id:
        :param role_card:  [(role, card_id), (role, card_id)]
        :return:
        """
        script = self.mm.script

        cur_script = script.cur_script
        if not cur_script:
            return 1, {}  # 没有拍摄中的剧本
        if cur_script['card']:
            return 2, {}  # 已选完角色

        script_config = game_config.script[cur_script['id']]
        role_ids = script_config['role_id']
        used_role, used_card = set(), set()
        for role, card_id in role_card:
            if role not in role_ids:
                return 2, {}
            if card_id in used_card:
                return 3, {}
            if role in used_role:
                return 3, {}

            used_card.add(card_id)
            used_role.add(role)
            cur_script['card'][role] = card_id

        cur_script['step'] = 2
        script.save()
        rc, data = self.index()
        return rc, data

    def set_style(self, style):
        """
        设置片子类型
        :param style:
        :return:
        """
        script = self.mm.script

        cur_script = script.cur_script
        if not cur_script:
            return 1, {}  # 没有拍摄中的剧本

        if not cur_script['card']:
            return 2, {}  # 没有演员

        cur_script['style'] = style
        cur_script['step'] = 3
        script.style_log.append(style)

        # todo: 拍摄结算
        self.calc_result(cur_script)

        script.save()
        rc, data = self.index()

        return rc, data

    def calc_result(self, film_info=None):
        """拍摄结算"""
        result = {}
        script = self.mm.script
        cur_script = film_info or script.cur_script

        script_config = game_config.script[cur_script['id']]
        reward = []
        for i in xrange(1, 3):
            num = script_config['random_num%s' % i]
            random_reward = script_config['random_reward%s' % i]
            if random_reward:
                for _ in xrange(num):
                    d = weight_choice(random_reward)
                    reward.append(d)

        result['reward'] = reward
        if not film_info.get('result'):
            film_info['result'] = result        # 奖励
            # todo 艺人人气关注度

            attention_info = self.calc_attention(film_info)
            film_info['attention_info'] = attention_info

            # todo 拍摄属性结算
            add_attr = {}
            film_info['add_attr'] = []
        return result

    def calc_attention(self, film_info):
        """计算影片关注度"""
        market_people = 100
        script_need = 10
        attention = 5
        card_effect = {}
        if film_info:
            script = self.mm.script

            market_attention = 0  # todo 市场关注度
            attention += market_attention
            # 2.各类型市场人口>=剧本需要
            if film_info['card']:
                attention += game_config.common[18]

            # 3.类型人口增量
            if film_info['style']:
                market_num = game_config.script_style[int(film_info['style'])]
                if market_people - script_need >= market_num:
                    attention += market_num
            # 4.题材与类型

            # 5.连续拍摄类型
            recent_style = script.style_log[-3:]
            if film_info['style'] and len(recent_style) == 3:
                if set(recent_style) == 1:
                    attention -= game_config.common[17]

            # todo 6.剧本人气属性要求，艺人总人气除以人气要求，所得到的值就是关注度增量
            for role_id, card_oid in film_info['card'].iteritems():
                card_effect[card_oid] = random.randint(100)

        return {
            'attention': attention,         # 关注度
            'card_effect': card_effect,     # 艺人人气对关注度影响
        }

    # todo 4 市场观众 选剧本时显示
    def market_num(self):
        pass

    # 5.艺人适配剧本和角色总分
    def calc_card_film_match_score(self, film_info):
        """"""
        all_score = 0
        script_config = game_config.script[film_info['id']]
        for role_id, card_oid in film_info['card'].iteritems():
            # role_config = game_config.script_role[role_id]
            card_info = self.cards[card_oid]
            quality = game_config.card_basis[card_info['id']]['qualityid']
            if quality in game_config.tag_score:
                score = game_config.tag_score[quality]['score']
                all_score += score
            else:
                print 'quality "%s" not exists in game_config' % quality, card_oid

        return all_score

    # 6.艺人的拍摄发挥
    def calc_film_card_effect(self):
        pass

    # 7.剧本属性计算
    def calc_script_attr(self):
        # todo
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script

        skilled = 0     # 总熟练度
        for role_id, card_oid in cur_script['card'].iteritems():
            card_info = card.cards[card_oid]
            for style, lv_info in card_info['style_pro'].iteritems():
                skilled += lv_info['lv']



    # 8.首映票房、收视计算
    def calc_income(self):
        script = self.mm.script
        cur_script = script.cur_script

        first_income = 100
        script_config = game_config.script[cur_script['id']]


    # 9.观众、专业评分计算




