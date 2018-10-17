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

from models.card import Card


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
            'sequel_script': script.sequel_script,
            'step': self.get_step(),
            'script_pool': script.script_pool,
            'sequel_script_pool': script.sequel_script_pool,
            'cur_script': script.cur_script,
            'scripts': script.scripts,
            'style_log': script.style_log,
            'cur_market': script.cur_market,
            'top_all': script.top_all,
        }

    def pre_filming(self, ):
        # todo 许可证判断 use_item

        script = self.mm.script
        script.pre_filming()
        script.save()
        rc, data = self.index()
        return rc, data

    def filming(self, script_id, name, is_sequel=False):
        """拍片

        :param script_id:
        :param name:
        :param is_sequel:   是否续集
        :return:
        """
        script = self.mm.script

        if is_sequel:
            pool = script.sequel_script_pool
        else:
            pool = script.script_pool

        if script_id not in pool:
            return 1, {}  # 不可选剧本

        if script.cur_script:
            return 2, {}  # 拍摄中

        # if pool[script_id]:
        #     return 3, {}  # 已拍摄

        film = script.make_film(script_id, name)
        script.cur_script = film

        pool[script_id] = 1
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
        cur_script['card_effect'] = effect

        script.save()
        rc, data = self.index()
        data.update(effect)
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
        data.update(effect)
        if finished_reward:
            data['finished_reward'] = finished_reward

        cur_script['style_effect'] = effect
        script.save()
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
        return result

    # 7.剧本属性计算
    def calc_script_attr(self):
        """
        总熟练度 = Σ【参演演员的熟练度等级】
        每项属性值 = 拍摄结果属性值 × [1+总熟练度/熟练度系数m]
        PartA =[艺术/艺术基准系数 +气质/气质基准系数]×[1+总熟练度/熟练度系数m]
        PartB =[娱乐/娱乐基准系数+动感/动感基准系数+歌艺/歌艺基准系数演+演技/演技基准系数] × [1+总熟练度/熟练度系数m]

        熟练度除以系数走common表数据id10，m=25
        :return:
        """
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script

        skilled = 0     # 总熟练度
        for role_id, card_oid in cur_script['card'].iteritems():
            card_info = card.cards[card_oid]
            for style, lv_info in card_info['style_pro'].iteritems():
                skilled += lv_info['lv']

        # 熟练度系数
        skilled_rate = game_config.common[10]

        # 选卡、设置类型两轮操作艺人发挥，累计得出拍摄结果属性
        # {role_id: {attr: value}}
        card_effect = cur_script['card_effect']
        style_effect = cur_script['style_effect']

        script_effect = {}  # 拍摄结果
        for per_effect in [card_effect, style_effect]:
            for _, info in per_effect['effect'].iteritems():
                for attr, value in info.iteritems():
                    script_effect[attr] = script_effect.get(attr, 0) + value

        # 每项属性值
        attrs = {}
        for attr, effect in script_effect.iteritems():
            attrs[attr] = effect * (1 + skilled / skilled_rate)

        script_config = game_config.script[cur_script['id']]
        add_attr = {}
        # pro_id: [add_value, limit_value]
        # 战斗属性显示上限 = 最高的单项标准数值*系数1+系数2
        # 系数1 common 27， 系数2 28
        limit_value = max(script_config['good_attr']) * game_config.common[27] + game_config.common[28]
        for pro_id, (min_attr, good_attr) in enumerate(itertools.izip(script_config['min_attr'], script_config['good_attr']), start=1):
            if good_attr < 0:
                attrs.pop(pro_id, '')
                continue
            add_attr[pro_id] = [attrs.get(pro_id, 0), limit_value]

        # CHAR_PRO_NAME = ['演技',        '歌艺', '娱乐',         '艺术', '气质',         '动感']
        # CHAR_PRO_NAME = ['performance', 'song', 'entertainment', 'art', 'temperament', 'sports']
        name_pro_mapping = Card.CHAR_PRO_NAME_PRO_ID_MAPPING
        pro_id_mapping = Card.PRO_IDX_MAPPING

        standard_attr = script_config['standard_attr']

        performance_pro_id = name_pro_mapping['performance']
        song_pro_id = name_pro_mapping['song']
        entertainment_pro_id = name_pro_mapping['entertainment']
        art_pro_id = name_pro_mapping['art']
        temperament_pro_id = name_pro_mapping['temperament']
        sports_pro_id = name_pro_mapping['sports']

        # PartA =[艺术/艺术基准系数 +气质/气质基准系数]×[1+总熟练度/熟练度系数m]
        base_a = 0
        for pro_id in [art_pro_id, temperament_pro_id]:
            # 系数为 0 表示无此属性不生效
            if not standard_attr[pro_id_mapping[pro_id]]:
                continue
            base_a += attrs.get(pro_id, 0) / standard_attr[pro_id_mapping[pro_id]]
        part_a = base_a + (1 + skilled / skilled_rate)

        # part_a = (
        #              attrs.get(art_pro_id, 0) / standard_attr[pro_id_mapping[art_pro_id]] +
        #              attrs.get(temperament_pro_id, 0) / standard_attr[pro_id_mapping[temperament_pro_id]]
        #
        #          ) + (1 + skilled / skilled_rate)

        # PartB =[娱乐/娱乐基准系数+动感/动感基准系数+歌艺/歌艺基准系数演+演技/演技基准系数] × [1+总熟练度/熟练度系数m]
        base_b = 0
        for pro_id in [entertainment_pro_id, sports_pro_id, song_pro_id, performance_pro_id]:
            # 系数为 0 表示无此属性不生效
            if not standard_attr[pro_id_mapping[pro_id]]:
                continue
            base_b += attrs.get(pro_id, 0) / standard_attr[pro_id_mapping[pro_id]]
        part_b = base_b + (1 + skilled / skilled_rate)

        #
        # part_b = (
        #              attrs.get(entertainment_pro_id, 0) / (standard_attr[pro_id_mapping[entertainment_pro_id]] or 1) +
        #              attrs.get(sports_pro_id, 0) / standard_attr[pro_id_mapping[sports_pro_id]] +
        #              attrs.get(song_pro_id, 0) / standard_attr[pro_id_mapping[song_pro_id]] +
        #              attrs.get(performance_pro_id, 0) / standard_attr[pro_id_mapping[performance_pro_id]]
        #
        #          ) + (1 + skilled / skilled_rate)

        return {
            'add_attr': add_attr,
            'part_a': part_a,
            'part_b': part_b,
        }

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

            card = self.mm.card
            standard_popularity = script_config['standard_popularity']
            for role_id, card_oid in film_info['card'].iteritems():
                card_info = card.cards[card_oid]
                card_popularity += card_info['popularity']

        return {
            'attention': attention,         # 关注度
            'card_effect': card_popularity / standard_popularity,     # 艺人人气对关注度影响
        }

    # 8.首映票房、收视计算
    def calc_first_income(self):
        # 首映票房
        script = self.mm.script
        cur_script = script.cur_script

        first_income = random.randint(1000, 10000)
        script_config = game_config.script[cur_script['id']]

        return {'first_income': first_income}

    def calc_medium_judge(self):
        """
        专业评分 = PartA/剧本难度系数/专业评分系数A +题材类型匹配度加成/10
        观众评分 = PartB/剧本难度系数/观众评分系数B +题材类型匹配度加成/10
        
        剧本难度系数读取script表的字段hard_rate
        题材类型匹配度加成读取script_style_suit表的rate字段
        评分系数AB读取common表数据id12、13
        """

        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[cur_script['id']]

        finished_attr = cur_script['finished_attr']
        part_a = finished_attr.get('part_a', 0)
        score_rate = game_config.common[12]
        suit_config = game_config.script_style_suit[cur_script['suit']]

        score = part_a / script_config['hard_rate'] / score_rate + suit_config['rate'] / 10
        # 点赞数 = 专业评分×点赞数系数k【这里的专业评分保留小数点后2位】
        like_rate = game_config.common[14]
        return {'score': score, 'like': int(score * like_rate)}

    def calc_audience_judge(self):
        """观众评分 = PartB/剧本难度系数/观众评分系数B +题材类型匹配度加成/10
        """

        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[cur_script['id']]

        finished_attr = cur_script['finished_attr']
        part_b = finished_attr.get('part_b', 0)
        score_rate = game_config.common[13]
        suit_config = game_config.script_style_suit[cur_script['suit']]

        score = part_b / script_config['hard_rate'] / score_rate + suit_config['rate'] / 10

        return {'score': score}

    def calc_curve(self):
        # todo 需要计算： 票房曲线参数 = 观众评分+(专业评分-专业评分影响线)/专业评分影响率

        script = self.mm.script
        cur_script = script.cur_script

        finished_medium_judge = cur_script['finished_medium_judge']
        finished_audience_judge = cur_script['finished_audience_judge']

        medium_score = finished_medium_judge['score']
        audience_score = finished_audience_judge['score']

        curve_id = 1
        curve_config = game_config.script_curve[curve_id]
        finished_first_income = cur_script['finished_first_income']
        first_income = finished_first_income['first_income']

        return {'curve': [first_income * i / 100 for i in curve_config['curve_rate']]}

    def summary(self):
        """票房总结"""
        # todo 需计算项目
        # 1。艺人对角色和剧本的发挥 card_effect, style_effect 字段存储
        #   {'match_role': {card_id: score}， 'match_script': {card_id: score}}
        # 2.

        # 公司经验player_exp
        # script_config['fight_exp']
        # script_config['player_exp']

        # .剧本人气属性要求，艺人总人气除以人气要求，所得到的值就是关注度增量
        # "finished_attention": {
        #                           "card_effect": 14,  # 艺人人气对关注度影响
        #                           "attention": 50  # 关注度
        #                       },

        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script
        style = cur_script['style']
        script_config = game_config.script[cur_script['id']]

        # 卡牌类型经验fight_exp
        for role_id, card_oid in cur_script['card'].iteritems():
            if card_oid in card.cards:
                card.add_style_exp(card_oid, style, script_config['fight_exp'])

        #  玩家经验player_exp
        self.mm.user.add_player_exp(script_config['player_exp'])

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

    # 艺人适配剧本总分
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
    def calc_film_card_effect(self, action='set_card'):
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[cur_script['id']]

        pro = cur_script['pro']
        # match_score = self.calc_card_film_match_score(cur_script)

        match_score = 0
        # todo
        match_script = {}       # 艺人对剧本发挥
        match_role = {}         # 艺人对角色发挥
        effect = {}
        # 计算攻击伤害
        for role_id, card_oid in cur_script['card'].iteritems():
            # 单个艺人的适配总分 = ∑  (适配的标签品质分数)
            card_info = self.mm.card.cards[card_oid]
            card_config = game_config.card_basis[card_info['id']]
            role_score = 0
            script_score = 0
            # 卡牌擅长角色匹配
            role_config = game_config.script_role[role_id]
            for tag_id, tag_quality in card_config['tag_role']:
                if tag_id in role_config['tag_role']:
                    role_score += game_config.tag_score[tag_quality]['score']
            match_role[card_oid] = role_score

            # 卡牌擅长剧本匹配
            for tag_id, tag_quality in card_config['tag_script']:
                if tag_id in script_config['tag_script']:
                    script_score += game_config.tag_score[tag_quality]['score']
            match_script[card_oid] = script_score

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

            # 判断是否暴击
            c1 = card_config['crit_rate_base'] / 10000.0
            c2 = (role_score + script_score) / 100.0
            crit_rate = c1 + c2
            if random.random() < crit_rate:
                # 暴击效果
                d = (role_score + script_score) / 100.0
                for attr in role_effect:
                    role_effect[attr] = role_effect[attr] * (1.1 + d)

        return {
            'effect': effect,
            'match_script': match_script,
            'match_role': match_role
        }



