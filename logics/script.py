# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
import random
import itertools
from gconfig import game_config

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import weight_choice


class ScriptLogic(object):
    def __init__(self, mm):
        self.mm = mm

    def get_step(self):
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

                step += script.cur_script['finished_step']
        return step

    def index(self):
        script = self.mm.script

        return 0, {
            'own_script': script.own_script,
            'step': self.get_step(),
            'script_pool': script.script_pool,
            'cur_script': script.cur_script,
            'scripts': script.scripts,
            'style_log': script.style_log,
            'cur_market': script.cur_market,
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
        self.mm.script_book.add_book(script_id)
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
        effect = self.calc_film_card_effect()
        script.save()
        rc, data = self.index()
        data['effect'] = effect
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

        script_config = game_config.script[cur_script['id']]
        style_effect = dict(script_config['style_effect'])
        if style in style_effect:
            suit = style_effect[style]
        else:
            suits = game_config.script_style_suit.keys()
            suit = suits[len(suits) / 2]

        cur_script['style'] = style
        cur_script['step'] = 3
        cur_script['suit'] = suit
        script.style_log.append(style)

        effect = self.calc_film_card_effect()
        finished_reward = self.check_finished_reward()

        rc, data = self.index()
        data['effect'] = effect
        if finished_reward:
            data['finished_reward'] = finished_reward
        script.save()
        # todo 选择类型之后的关注度增加， script 表的 style_effect 字段里取 script_style_suit
        return rc, data

    def check_finished_reward(self):
        """todo 检查杀青奖励"""
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script
        reward = {'coin': 1}
        if 'finished_reward' not in cur_script:
            cur_script['finished_reward'] = reward
        return reward

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
        # todo 公司经验 script, 类型经验fight_exp
        # if not film_info.get('result'):
        #     film_info['result'] = result        # 奖励
        #     # todo 艺人人气关注度
        #
        #     # todo 拍摄属性结算
        #     add_attr = {}
        #     film_info['add_attr'] = []
        return result

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

        skilled_rate = game_config.common[10]
        add_char_pro = [0] * len(card.CHAR_PRO_MAPPING)

        script_config = game_config.script[cur_script['id']]
        add_attr = {}
        # pro_id: [add_value, limit_value]
        for idx, (min_attr, good_attr) in enumerate(itertools.izip(script_config['min_attr'], script_config['good_attr']), start=1):
            if good_attr < 0:
                continue
            add_attr[idx] = [random.randint(1, 100), random.randint(100, 150)]

        return {'add_attr': add_attr}

    # 3.计算影片关注度
    def calc_attention(self, film_info=None):
        """计算影片关注度"""
        script = self.mm.script
        film_info = film_info or script.cur_script

        # 1.实际观众之和
        N = attention = sum(script.cur_market)

        card_popularity = 0
        if film_info:
            script_id = film_info['id']
            # 2.各个市场类型都符合剧本要求，增加额外关注度
            script_config = game_config.script[script_id]
            script_market = list(script_config['market'])
            for need, cur in itertools.izip(script_market, script.cur_market):
                if need > cur:
                    break
            else:
                attention += game_config.common[18]

            # 3.选择类型之后，类型带来观众需求增量x，读script_style的market_num
            style = film_info['style']
            if style:
                attention += game_config.script_style.get(int(style), {}).get('market_num', 0)

            # 3.类型人口增量
            if film_info['style']:
                script_need = sum(script_config['market'])
                market_num = game_config.script_style.get(int(style), {}).get('market_num', 0)
                if N - script_need >= market_num:
                    attention += market_num

            # 4.题材与类型
            suit = film_info['suit']
            attention += game_config.script_style_suit.get(suit, {}).get('attention', 0)

            # 5.连续拍摄类型
            recent_style = script.style_log[-3:]
            if film_info['style'] and len(recent_style) == 3:
                if set(recent_style) == 1:
                    attention -= game_config.common[17]

            # todo 6.剧本人气属性要求，艺人总人气除以人气要求，所得到的值就是关注度增量
            standard_popularity = script_config['standard_popularity']
            for role_id, card_oid in film_info['card'].iteritems():
                card_popularity += random.randint(0, 100)

        return {
            'attention': attention,         # 关注度
            'card_effect': card_popularity / standard_popularity,     # 艺人人气对关注度影响
        }

    # 8.首映票房、收视计算
    def calc_first_income(self):
        # todo
        script = self.mm.script
        cur_script = script.cur_script

        first_income = 100
        script_config = game_config.script[cur_script['id']]

        return {'first_income': first_income}

    def calc_medium_judge(self):
        """专业评价"""
        # todo
        script = self.mm.script
        cur_script = script.cur_script
        # todo 得到点赞数
        return {'score': 100, 'like': 10}

    def calc_audience_judge(self):
        """观众评价"""
        # todo
        script = self.mm.script
        cur_script = script.cur_script
        return {'score': 200}

    def calc_curve(self):
        # todo 需要计算： 票房曲线参数 = 观众评分+(专业评分-专业评分影响线)/专业评分影响率

        script = self.mm.script
        cur_script = script.cur_script

        curve_id = 1
        curve_config = game_config.script_curve[curve_id]
        finished_first_income = cur_script['finished_first_income']
        first_income = finished_first_income['first_income']

        return {'curve': [first_income * i / 100 for i in curve_config['curve_rate']]}

    def summary(self):
        """票房总结"""
        # todo
        return {
            'income': 123,          # 总票房
            'user_rank_up': 3       # 用户排名上升
        }

    def finished_analyse(self):
        """票房分析"""
        return {

        }

    def get_func_mapping(self, finished_step):
        if finished_step == 1:
            return self.calc_curve


    def check_finished_step(self, finished_step):
        """

        :param finished_step:
            1： 经验、熟练度什么的通用奖励
            2： 拍摄属性结算
            3： 弹出新闻关注度
            4： 首日上映
            5： 专业评价
            6： 持续上映
            7： 观众评价
            8： 票房总结
            # 9： 票房分析
        :return:
        """
        script = self.mm.script
        cur_script = script.cur_script
        if not cur_script:
            return 1, {}

        data = {}
        if finished_step == 1:
            key = 'finished_common_reward'
            func = self.calc_result

        elif finished_step == 2:
            key = 'finished_attr'
            func = self.calc_script_attr

        elif finished_step == 3:
            key = 'finished_attention'
            func = self.calc_attention

        elif finished_step == 4:
            key = 'finished_first_income'
            func = self.calc_first_income

        elif finished_step == 5:
            key = 'finished_medium_judge'
            func = self.calc_medium_judge

        elif finished_step == 6:
            key = 'finished_curve'
            func = self.calc_curve

        elif finished_step == 7:
            key = 'finished_audience_judge'
            func = self.calc_medium_judge

        elif finished_step == 8:
            key = 'finished_summary'
            func = self.summary

        elif finished_step == 9:
            key = 'finished_analyse'
            func = self.finished_analyse

        result = cur_script.get(key)
        if not result:
            cur_script['finished_step'] = finished_step
            result = func()
            cur_script[key] = result
            script.save()
        data[key] = result

        data['cur_script'] = script.cur_script
        data['step'] = self.get_step()
        return 0, data

    # 4 市场观众 选剧本时显示
    def market_num(self):
        """选片时计算"""
        pass

    # 5.艺人适配剧本和角色总分
    def calc_card_film_match_score(self, film_info):
        """"""
        all_score = 0
        card = self.mm.card
        script_config = game_config.script[film_info['id']]
        for role_id, card_oid in film_info['card'].iteritems():
            # role_config = game_config.script_role[role_id]
            card_info = card.cards[card_oid]
            quality = game_config.card_basis[card_info['id']]['qualityid']
            if quality in game_config.tag_score:
                score = game_config.tag_score[quality]['score']
                all_score += score
            else:
                print 'quality "%s" not exists in game_config' % quality, card_oid

        return all_score

    # 6.艺人的拍摄发挥,选卡算一次，选类型算一次
    def calc_film_card_effect(self):
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script

        pro = cur_script['pro']
        match_score = self.calc_card_film_match_score(cur_script)

        # todo
        match_script = {}
        match_style = {}        # 演员对应类型熟练度
        effect = {}
        # 计算攻击伤害
        for role_id, card_oid in cur_script['card'].iteritems():
            match_script[role_id] = random.randint(1, 10)
            card_info = card.get_card(card_oid)
            love_lv = card_info['love_lv']
            love_config = game_config.card_love_level[love_lv]
            card_config = game_config.card_basis[card_info['id']]

            dps_rate = random.randint(*love_config['dps_rate'])      # 伤害系数 万分之

            role_config = game_config.script_role[role_id]
            role_attr = list(role_config['role_attr'])
            # 随机属性
            if random.randint(0, 10000) <= card_config['ex_special_rate']:
                special_attr = weight_choice(card_config['special_quality'])[0]
                role_attr.append(special_attr)

            role_effect = effect[role_id] = {}
            # 计算属性
            for attr in role_attr:
                base_value = card_info['char_pro'][card.PRO_IDX_MAPPING[attr]]
                if base_value < 0:
                    continue
                value = base_value * dps_rate / 10000.0
                if attr in role_effect:
                    role_effect[attr] += value
                else:
                    role_effect[attr] = value

            # todo 判断是否暴击
            c1 = card_config['crit_rate_base'] / 10000.0
            c2 = match_score / 100.0
            crit_rate = c1 + c2
            if random.random() < crit_rate:
                pass
            else:
                pass
            # 计算输出

        return {'effect': effect, 'match_script': match_script, 'match_style': match_style}



