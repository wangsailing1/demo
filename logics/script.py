# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
import math
import bisect
import random
import itertools
from collections import Counter
from gconfig import game_config
from tools.gift import add_mult_gift, del_mult_goods

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.utils import weight_choice

from models.script import Script
from models.card import Card
from models.ranking_list import BlockRank


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

    def get_recommend_card(self, script_id):
        return self.mm.script.top_end_lv_card.get(script_id, {})

    def index(self):
        script = self.mm.script
        self.calc_attention_by_step(script.cur_script.get('step', 0), is_save=True)

        return 0, {
            'recommend_card': self.get_recommend_card(script.cur_script.get('id')),

            # 'own_script': script.own_script,
            # 'sequel_script': script.group_sequel.values(),
            'step': self.get_step(),
            'script_pool': script.script_pool,
            'sequel_script_pool': script.sequel_script_pool,
            'cur_script': script.cur_script,
            'scripts': script.scripts,
            'style_log': script.style_log,
            'cur_market': script.cur_market,
            'cur_market_show': script.cur_market_show,
            'top_all': script.top_all,
            'attr_total': self.attr_total(),
            'script_license': self.mm.user.script_license
        }

    # 统计总的effect
    def attr_total(self):
        attr_total = {}
        style_effect = self.mm.script.cur_script.get('style_effect', {}).get('effect', {})
        card_effect = self.mm.script.cur_script.get('card_effect', {}).get('effect', {})
        for k, v in style_effect.iteritems():
            for attr_id, value in v.iteritems():
                if isinstance(value, list):
                    value = value[0]
                attr_total[attr_id] = attr_total.get(attr_id, 0) + math.ceil(value)
        for k, v in card_effect.iteritems():
            for attr_id, value in v.iteritems():
                if isinstance(value, list):
                    value = value[0]
                attr_total[attr_id] = attr_total.get(attr_id, 0) + math.ceil(value)
        return attr_total

    def pre_filming(self, ):
        # todo 许可证判断 use_item

        script = self.mm.script
        if not self.mm.script.cur_market or self.mm.script.cur_market and not self.mm.script.script_pool:
            script.pre_filming()
            if self.mm.user.script_license > 0:
                self.mm.user.script_license -= 1
            else:
                cost = game_config.script_license['cost']
                del_mult_goods(self.mm, cost)
            script.save()
            self.mm.user.save()
        rc, data = self.index()
        return rc, data

    def filming(self, script_id, name, is_sequel=False):
        """拍片

        :param script_id:
        :param name:
        :param is_sequel:   是否续集
        :return:
        """
        user = self.mm.user
        script = self.mm.script
        script_config = game_config.script[script_id]
        cost = script_config['cost']
        if not user.is_dollar_enough(cost):
            return 'error_dollar', {}

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
        film['cost'] = cost

        pool[script_id] = 1
        self.mm.script_book.add_book(script_id)
        user.deduct_dollar(cost)
        self.calc_attention_by_step(1)
        script.save()
        user.save()

        rc, data = self.index()
        return rc, data

    def set_card(self, role_card):
        """

        :param script_id:
        :param role_card:  [(role, card_id), (role, card_id)]
        :return:
        """
        user = self.mm.user
        script = self.mm.script
        card = self.mm.card

        cur_script = script.cur_script
        if not cur_script:
            return 1, {}  # 没有拍摄中的剧本
        if cur_script['card']:
            return 2, {}  # 已选完角色

        cost = 0
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

            card_info = card.cards[card_id]
            card_config = game_config.card_basis[card_info['id']]
            cost += card_config['paycheck_base'] * script_config['paycheck_ratio'] / 100

            used_card.add(card_id)
            used_role.add(role)
            cur_script['card'][role] = card_id

        if not used_role:
            return 4, {}
        if not user.is_dollar_enough(cost):
            return 'error_dollar', {}

        user.deduct_dollar(cost)
        cur_script['step'] = 2
        cur_script['cost'] += cost
        effect = self.calc_film_card_effect()
        cur_script['card_effect'] = effect
        self.calc_attention_by_step(2)

        script.save()
        user.save()
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
        cur_script['style_effect'] = effect
        finished_reward = self.check_finished_reward()

        result = self.calc_attention_by_step(3)
        rc, data = self.index()
        data.update(effect)
        data['cur_script']['attention'] = result['attention_initial']
        if finished_reward:
            data['finished_reward'] = finished_reward

        script.save()

        return rc, data

    def check_finished_reward(self):
        """todo 检查杀青奖励"""
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[script.cur_script['id']]
        min_attr = script_config['min_attr']
        attr_total = self.attr_total()
        gift = []
        for attr_id, value in enumerate(min_attr, 1):
            if value == -1:
                continue
            if attr_total.get(attr_id, 0) < value:
                gift = []
                break
            gift = script_config['award']

        reward = add_mult_gift(self.mm, gift)
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
        result = self.calc_attention_by_step(1)
        attention = self.calc_attention()
        result['reward'] = reward
        result['attention_initial'] = attention['attention_initial']
        result['attention_end'] = attention['attention']
        return result

    # 7.剧本属性计算
    def calc_script_attr(self):
        """
        总熟练度 = Σ【参演演员的熟练度等级】
        每项属性值 = 拍摄结果属性值 × [1+总熟练度/熟练度系数m]
        partA=（(（艺术/含艺术属性的角色数量/艺术基准系数）^属性作用指数+（气质/含气质属性的角色数量/气质基准系数）^属性作用指数)/生效属性数量）*（1+平均熟练度等级加成）
        partB=（(（娱乐/含娱乐属性的角色数量/娱乐基准系数）^属性作用指数+（动感/含动感属性的角色数量/动感基准系数）^属性作用指数+（歌艺/含歌艺属性的角色数量/歌艺基准系数）^属性作用指数+（演技/含演技属性的角色数量/演技基准系数）^属性作用指数)/生效属性数量）*（1+平均熟练度）
        熟练度除以系数走common表数据id10，m=25
        :return:
        """
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script

        skilled = 0  # 总熟练度
        role_num = 0

        role_count_by_attr = Counter()
        for role_id, card_oid in cur_script['card'].iteritems():
            card_info = card.cards[card_oid]
            role_config = game_config.script_role[role_id]
            role_count_by_attr.update(role_config['role_attr'])

            role_num += 1
            for style, lv_info in card_info['style_pro'].iteritems():
                skilled += lv_info['lv']

        avg_skilled = skilled / role_num

        if avg_skilled in game_config.card_script_exp:
            skilled_lv_addition = game_config.card_script_exp[avg_skilled]['lv_addition'] / 10000.0
        else:
            skilled_lv_addition = 0

        # 熟练度系数
        skilled_rate = game_config.common[10]

        # 选卡、设置类型两轮操作艺人发挥，累计得出拍摄结果属性
        # {role_id: {attr: value}}
        card_effect = cur_script['card_effect']
        style_effect = cur_script['style_effect']

        attrs = {}  # 拍摄结果
        for per_effect in [card_effect, style_effect]:
            for _, info in per_effect['effect'].iteritems():
                for attr, value in info.iteritems():
                    if isinstance(value, list):
                        value = value[0]
                    attrs[attr] = attrs.get(attr, 0) + value

        script_config = game_config.script[cur_script['id']]
        add_attr = {}
        # pro_id: [add_value, limit_value]
        # 战斗属性显示上限 = 最高的单项标准数值*系数1+系数2
        # 系数1 common 27， 系数2 28
        limit_value = max(script_config['good_attr']) * game_config.common[27] + game_config.common[28]
        for pro_id, (min_attr, good_attr) in enumerate(
                itertools.izip(script_config['min_attr'], script_config['good_attr']), start=1):
            if good_attr < 0:
                attrs.pop(pro_id, '')
                continue
            add_attr[pro_id] = [attrs.get(pro_id, 0), limit_value]

        # CHAR_PRO_NAME = ['演技',         '歌艺', '气质',         '动感',   '艺术', '娱乐']
        # CHAR_PRO_NAME = ['performance', 'song', 'temperament', 'sports', 'art', 'entertainment']

        name_pro_mapping = Card.CHAR_PRO_NAME_PRO_ID_MAPPING
        pro_id_mapping = Card.PRO_IDX_MAPPING

        standard_attr = script_config['standard_attr']

        performance_pro_id = name_pro_mapping['performance']
        song_pro_id = name_pro_mapping['song']
        entertainment_pro_id = name_pro_mapping['entertainment']
        art_pro_id = name_pro_mapping['art']
        temperament_pro_id = name_pro_mapping['temperament']
        sports_pro_id = name_pro_mapping['sports']

        # 属性作用指数
        attr_rate = game_config.common[33] / 100.0
        # 属性作用上升率
        attr_up_rate = game_config.common[53] / 10000.0
        # 属性作用上升指数
        attr_up_index = game_config.common[54] / 10000.0

        # partA = （part艺术 + part气质） / 生效属性数量） * （1 + 平均熟练度等级加成）
        # 艺术、气质计算规则如下
        # 【 当艺术 / 含艺术属性角色数量 < 艺术基准系数】
        #       part艺术 =（艺术 / 含艺术属性的角色数量 / 艺术基准系数） ^ 属性作用指数
        # else:
        #       part艺术 = （1 +（艺术 / 含艺术属性的角色数量 - 艺术基准系数）*属性作用上升率 /（1 + 属性作用上升率 *（艺术 / 含艺术属性的角色数量 - 艺术基准系数））） ^ 属性作用上升指数

        # 增加事件和全球影响事件buff
        # 属性 = 属性 * （1 + 影响比例）（最大5%）
        event_buff = script.check_event_effect()
        event_buff = min(event_buff, 5)

        base_a = 0
        pro_count = 0
        for pro_id in [art_pro_id, temperament_pro_id]:
            # 系数为 0 表示无此属性不生效
            if not standard_attr[pro_id_mapping[pro_id]] > 0:
                continue
            else:
                pro_count += 1
            if not role_count_by_attr[pro_id]:
                continue

            standard_pro_rate = standard_attr[pro_id_mapping[pro_id]]
            if 1.0 * attrs.get(pro_id, 0) / role_count_by_attr[pro_id] < standard_pro_rate:
                d = (1.0 * attrs.get(pro_id, 0) / role_count_by_attr[pro_id] / standard_attr[pro_id_mapping[pro_id]]) \
                    ** attr_rate
            else:
                attr_value = attrs.get(pro_id, 0)
                d = (1 + (1.0 * attr_value / role_count_by_attr[pro_id] - standard_pro_rate) * attr_up_rate
                     / (1 + attr_up_rate * (1.0 * attr_value / role_count_by_attr[pro_id] - standard_pro_rate))) ** attr_up_index

            d = d * (1 + event_buff / 100.0)
            base_a += d

        part_a = (base_a / pro_count) * (1 + skilled_lv_addition)

        # partB = （part娱乐+part动感+part歌艺+part演技）/生效属性数量）*（1+平均熟练度等级加成）
        # 各属性计算规则如下
        # 【 当娱乐 / 含娱乐属性角色数量 < 娱乐基准系数】
        #       part娱乐 =（娱乐 / 含娱乐属性的角色数量 / 娱乐基准系数） ^ 属性作用指数
        # else:
        #       part娱乐 = （1 +（娱乐 / 含娱乐属性的角色数量 - 娱乐基准系数）*属性作用上升率 /（1 + 属性作用上升率 *（娱乐 / 含娱乐属性的角色数量 - 娱乐基准系数））） ^ 属性作用上升指数

        base_b = 0
        pro_count = 0
        for pro_id in [entertainment_pro_id, sports_pro_id, song_pro_id, performance_pro_id]:
            # 系数为 0 表示无此属性不生效
            if not standard_attr[pro_id_mapping[pro_id]] > 0:
                continue
            else:
                pro_count += 1
            if not role_count_by_attr[pro_id]:
                continue

            standard_pro_rate = standard_attr[pro_id_mapping[pro_id]]
            if 1.0 * attrs.get(pro_id, 0) / role_count_by_attr[pro_id] < standard_pro_rate:
                d = (1.0 * attrs.get(pro_id, 0) / role_count_by_attr[pro_id] / standard_attr[pro_id_mapping[pro_id]]) \
                    ** attr_rate
            else:
                attr_value = attrs.get(pro_id, 0)
                d = (1 + (1.0 * attr_value / role_count_by_attr[pro_id] - standard_pro_rate) * attr_up_rate
                     / (1 + attr_up_rate * (1.0 * attr_value / role_count_by_attr[pro_id] - standard_pro_rate))) ** attr_up_index

            d = d * (1 + event_buff / 100.0)
            base_b += d

        part_b = (base_b / pro_count) * (1 + skilled_lv_addition)

        min_part = game_config.common[37] / 10.0
        result = self.calc_attention_by_step(1)
        return {
            'add_attr': add_attr,
            'part_a': max(min_part, part_a),
            'part_b': max(min_part, part_b),
            'attention': result['attention'],
            'card_effect': result.get('card_effect', 0)
        }

    # 按step计算关注度 (主要是计算加成后的关注度)
    def calc_attention_by_step(self, step, film_info=None, is_save=False):
        if not self.mm.script.cur_script:
            return
        if step > 3:
            return
        if step == 3:
            resoult = self.calc_attention(film_info)
            self.mm.script.cur_script['attention'] = resoult['attention']
            if is_save:
                self.mm.script.save()
            return resoult
        script = self.mm.script
        film_info = film_info or script.cur_script

        # 1.实际观众之和
        L = N = M = style_suit_effect = 0
        market_enough = True
        # todo 当前初始关注度
        init_attention = sum([j for i,j in self.mm.user.attention.iteritems() if i != 3])
        card_popularity = 0
        if film_info:
            script_id = film_info['id']
            script_config = game_config.script[script_id]
            script_market = list(script_config['market'])
            for market, (need, cur) in enumerate(itertools.izip(script_market, script.cur_market), start=1):
                # 各类型市场人口都>=剧本需要，关注度额外+L，L读表id 8
                market_enough = market_enough & (cur >= need)
                N += min(cur, need)
            if market_enough:
                L = game_config.common[8]
            population_rate = game_config.common[50]  # 人口关注度系数
            if step == 1:
                attention = init_attention + (L + N) * population_rate
                # 保底关注度
                min_attection = game_config.common[40] / 10000.0
                if attention < min_attection:
                    attention = min_attection
                script.cur_script['attention'] = int(attention)
                if is_save:
                    script.save()
                return {'attention': int(attention)}
            card = self.mm.card
            standard_popularity = script_config['standard_popularity']
            for role_id, card_oid in film_info['card'].iteritems():
                card_info = card.cards[card_oid]
                card_popularity += card_info['popularity']
        if step == 1:
            self.mm.user.add_attention(3, L)
        all_popularity = 0
        for role_id, card_oid in script.cur_script['card'].iteritems():
            card_info = card.cards[card_oid]
            all_popularity += card_info['popularity']
        all_popularity_rate = game_config.common[34] / 100.0
        popularity_constant = game_config.common[35] / 100.0
        popularity_rate = game_config.common[36] / 100.0
        population_rate = game_config.common[50]  # 人口关注度系数

        standard_popularity = script_config['standard_popularity']
        attention_rate = 1 + (all_popularity ** all_popularity_rate /
                              (
                                  all_popularity ** all_popularity_rate + standard_popularity) - popularity_constant) * popularity_rate

        attention = init_attention + (L + N) * population_rate + style_suit_effect - M

        # 保底关注度
        min_attection = game_config.common[40] / 10000.0
        if attention < min_attection:
            attention = min_attection
        script.cur_script['attention'] = int(attention)
        if is_save:
            script.save()
            self.mm.user.save()
        return {'attention': int(attention),
                'card_effect': card_popularity / standard_popularity, }

    # 3.计算影片关注度
    def calc_attention(self, film_info=None):
        """计算影片关注度"""
        script = self.mm.script
        film_info = film_info or script.cur_script

        # 1.实际观众之和
        L = N = M = style_suit_effect = 0
        market_enough = True
        init_attention = sum([j for i,j in self.mm.user.attention.iteritems() if i != 3])

        card_popularity = 0
        if film_info:
            script_id = film_info['id']
            # 2.各个市场类型都符合剧本要求，增加额外关注度
            script_config = game_config.script[script_id]

            style = film_info['style']
            style_config = game_config.script_style.get(int(style), {})

            # 剧本人口预估
            script_market = list(script_config['market'])
            for market, (need, cur) in enumerate(itertools.izip(script_market, script.cur_market), start=1):
                # 各类型市场人口都>=剧本需要，关注度额外+L，L读表id 8
                market_enough = market_enough & (cur >= need)

                # 3.选择类型之后，类型带来观众需求增量x，读script_style的market_num
                if style_config and style_config['market'] == market:
                    need += style_config['market_num']
                N += min(cur, need)

            if market_enough:
                L = game_config.common[8]

            # 4.题材与类型
            suit = film_info['suit']
            style_suit_effect = game_config.script_style_suit.get(suit, {}).get('attention', 0)

            # 5.连续拍摄类型
            recent_style = script.style_log[-3:]
            if film_info['style'] and len(recent_style) == 3:
                if set(recent_style) == 1:
                    M = game_config.common[17]

            card = self.mm.card
            standard_popularity = script_config['standard_popularity']
            for role_id, card_oid in film_info['card'].iteritems():
                card_info = card.cards[card_oid]
                card_popularity += card_info['popularity']

        # 总人气
        all_popularity = 0
        for role_id, card_oid in script.cur_script['card'].iteritems():
            card_info = card.cards[card_oid]
            all_popularity += card_info['popularity']

        # 总人气指数、人气计算常数、人气系数
        all_popularity_rate = game_config.common[34] / 100.0
        popularity_constant = game_config.common[35] / 100.0
        popularity_rate = game_config.common[36] / 100.0
        population_rate = game_config.common[50]  # 人口关注度系数

        standard_popularity = script_config['standard_popularity']
        # 6、最后结算人气时
        # 读取剧本的人气要求属性，(1+(艺人总人气^总人气指数/(艺人总人气^总人气指数+剧本人气要求)- 人气计算常数)* 人气系数)
        # 所得到的值就是关注度加成系数。
        # 总人气指数，人气计算常数，人气系数读取common表/100，（common表34,35,36行，计算后结果值为1.5,0.49，0.2）

        attention_rate = 1 + (all_popularity ** all_popularity_rate /
                              (
                                  all_popularity ** all_popularity_rate + standard_popularity) - popularity_constant) * popularity_rate

        attention_initial = init_attention + (L + N) * population_rate + style_suit_effect - M
        attention = attention_initial * attention_rate

        # 保底关注度
        min_attection = game_config.common[40] / 10000.0
        if attention < min_attection:
            attention = min_attection
        return {
            'attention': int(attention),  # 关注度
            'card_effect': card_popularity / standard_popularity,  # 艺人人气对关注度影响
            'attention_initial': int(attention_initial)
        }

    # 8.首映票房、收视计算
    def calc_first_income(self):
        """
        首映票房=票房基数×(1+关注度等级/10）×(PartA+PartB)/2/首播票房固定参数z
        票房基数读取剧本表output字段
        首播票房参数z走common数据id9
        如果作品类型是电视剧、综艺节目，则
        首映收视 = 首映票房/首播收视系数，小数点后保留4位，
        首播收视系数走common表数据id11

        :return:
        """
        # 首映票房
        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[cur_script['id']]

        attention = cur_script['finished_attention'].get('attention', 0)
        finished_attr = cur_script['finished_attr']
        part_a = finished_attr.get('part_a', 0)
        part_b = finished_attr.get('part_b', 0)

        # first_income = random.randint(1000, 10000)
        lv_attentions = [(lv, v['max_attention']) for lv, v in game_config.attention_level.items()]
        lv_attentions.sort()
        lv_idx = bisect.bisect_left([x[1] for x in lv_attentions], attention)
        if lv_idx >= len(lv_attentions):
            lv_idx = -1
        attention_lv = lv_attentions[lv_idx][0]

        z = game_config.common[9]
        first_income = script_config['output'] * (1 + attention_lv / 10.0) * (part_a + part_b) / 2 / z
        first_income = int(first_income)
        # 如果作品类型是电视剧、综艺节目, 让前端算 区分展示单位
        # if script_config['type'] != 1:
        #     first_income = 1.0 * first_income / game_config.common[11]
        #     first_income = round(first_income, 4)

        # 检查全服总票房
        luck_info = script.check_luck_income(script_config['type'], first_income)
        # buff广播
        if luck_info['first_luck'] or luck_info['step_luck']:
            self.mm.scroll_bar.script_luck_buff(self.mm, cur_script['id'], script_config)
        elif luck_info['debuff']:
            luck_info['debuff_msg'] = self.mm.scroll_bar.script_luck_debuff(self.mm, cur_script['id'], script_config)
        return luck_info

    def calc_medium_judge(self):
        """
        专业评分 = PartA/剧本难度系数*专业评分系数A + 题材类型匹配度加成/10，（如果PartA<1,则难度系数为1）
        观众评分 = PartB/剧本难度系数*观众评分系数B + 题材类型匹配度加成/10，（如果PartB<1,则难度系数为1）
        
        剧本难度系数读取script表的字段hard_rate
        题材类型匹配度加成读取script_style_suit表的rate字段
        评分系数AB读取common表数据id12、13
        """

        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[cur_script['id']]

        finished_attr = cur_script['finished_attr']
        hard_rate = script_config['hard_rate']
        part_a = finished_attr.get('part_a', 0)
        if part_a < 1:
            hard_rate = 1
        score_rate = game_config.common[12]
        suit_config = game_config.script_style_suit[cur_script['suit']]

        score = part_a / hard_rate * score_rate + suit_config['rate'] / 10.0
        # 保底值
        min_score = game_config.common[38] / 10.0
        if score < min_score:
            score = min_score
        score = min(round(score, 2), game_config.common[43])
        # 点赞数 = 专业评分×点赞数系数k【这里的专业评分保留小数点后2位】
        like_rate = game_config.common[14]
        return {'score': score, 'like': int(score * like_rate)}

    def calc_audience_judge(self):
        """观众评分 = PartB/剧本难度系数*观众评分系数B + 题材类型匹配度加成/10，（如果PartB<1,则难度系数为1）
        """

        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[cur_script['id']]

        finished_attr = cur_script['finished_attr']
        hard_rate = script_config['hard_rate']
        part_b = finished_attr.get('part_b', 0)
        if part_b < 1:
            hard_rate = 1
        score_rate = game_config.common[13]
        suit_config = game_config.script_style_suit[cur_script['suit']]

        score = part_b / hard_rate * score_rate + suit_config['rate'] / 10.0
        # 保底值
        min_score = game_config.common[39] / 10.0
        if score < min_score:
            score = min_score
        score = min(round(score, 1), game_config.common[43])
        audi_grade = score * 100

        star = 0
        for k, v in game_config.audi_comment_choice.iteritems():
            audi_grade_range = v['audi_grade_range']
            if audi_grade_range[0] <= audi_grade <= audi_grade_range[1]:
                star = k
                break
        return {'score': score, 'star': star}

    def calc_curve(self):
        """
        票房曲线参数 = 观众评分+(专业评分-专业评分影响线)/专业评分影响率

        其中专业评分影响线、影响率走common表数据id15、16
        根据计算出的票房曲线参数读取script_curve表
        每日上映票房收益 =  首映票房 × 今日曲线参数/固定参数X
        总票房=首映票房 + Σ（每日上映票房收益）
        其中每日上映票房收益固定参数X走common表数据id18

        """

        script = self.mm.script
        cur_script = script.cur_script

        finished_medium_judge = cur_script['finished_medium_judge']
        finished_audience_judge = cur_script['finished_audience_judge']

        medium_score = finished_medium_judge['score']
        audience_score = finished_audience_judge['score']

        curve_id = audience_score + float(medium_score - game_config.common[15]) / game_config.common[16]
        curve_id = math.ceil(curve_id)
        max_config_id = max(game_config.script_curve)
        min_config_id = min(game_config.script_curve)
        if curve_id >= max_config_id:
            curve_id = max_config_id
        if curve_id < min_config_id:
            curve_id = min_config_id

        curve_config = game_config.script_curve[curve_id]
        finished_first_income = cur_script['finished_first_income']
        first_income = finished_first_income['first_income']

        rate = game_config.common[18]
        curve = [first_income * i / rate for i in curve_config['curve_rate']]
        curve = [int(i) for i in curve]
        return {
            'curve_id': curve_id,
            'curve': curve,
        }

    def summary(self):
        """票房总结"""
        # todo 需计算项目
        # 1。艺人对角色和剧本的发挥 card_effect, style_effect 字段存储
        #   {'match_role': {card_id: score}， 'match_script': {card_id: score}}
        # 2.

        # 公司经验player_exp
        # script_config['fight_exp']
        # script_config['player_exp']

        # 剧本人气属性要求，艺人总人气除以人气要求，所得到的值就是关注度增量
        # "finished_attention": {
        #                           "card_effect": 14,  # 艺人人气对关注度影响
        #                           "attention": 50  # 关注度
        #                       },

        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script
        style = cur_script['style']
        script_config = game_config.script[cur_script['id']]

        # 杀青步骤的 reward
        finished_common_reward = cur_script['finished_common_reward']
        finished_medium_judge = cur_script['finished_medium_judge']
        reward = add_mult_gift(self.mm, finished_common_reward['reward'])

        # 卡牌类型经验fight_exp
        for role_id, card_oid in cur_script['card'].iteritems():
            if card_oid in card.cards:
                card.add_style_exp(card_oid, style, script_config['fight_exp'])

        # 玩家经验player_exp
        self.mm.user.add_player_exp(script_config['player_exp'])

        # 专业评级点赞数
        self.mm.user.add_like(finished_medium_judge['like'])

        # 总票房 给美金
        finished_first_income = cur_script['finished_first_income']
        finished_curve = cur_script['finished_curve']
        all_income = int(finished_first_income['first_income'] + sum(finished_curve['curve']))
        self.mm.user.add_dollar(all_income)

        ticket_line = script_config['ticket_line']
        ticket_rate = 10000.0 * all_income / ticket_line

        # 票房评级
        end_lv_rate = [(k, v['line']) for k, v in game_config.script_end_level.iteritems()]
        end_lv_rate.sort(key=lambda x: x[0])
        idx = bisect.bisect_left([i[1] for i in end_lv_rate], ticket_rate)
        if idx >= len(end_lv_rate):
            idx = -1
        end_lv = end_lv_rate[idx][0]

        cur_script['end_lv'] = end_lv
        next_attention = game_config.script_end_level[end_lv]['next_attention']
        self.user.attention = {}
        self.user.add_attention(2, next_attention)

        # 记录街区总排行（显示用,按票房）
        block_income_rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
                                                             'income')
        bir = BlockRank(block_income_rank_uid, self.mm.script._server_name)
        old_rank = bir.get_rank(self.mm.uid)
        old_score = bir.get_score(self.mm.uid)
        bir.incr_rank(self.mm.uid, all_income)
        new_rank = bir.get_rank(self.mm.uid)
        new_score = bir.get_score(self.mm.uid)
        if new_rank > 0:
            near_rank = new_rank - 1
        if new_rank == 1:
            near_rank = 2
        rank_list = bir.get_all_user(start=near_rank - 1, end=near_rank - 1,withscores=True)
        near_score = rank_list[0][1] if rank_list else 0

        cur_script['old_rank'] = [old_rank, old_score]
        cur_script['new_rank'] = [new_rank, new_score]
        cur_script['near_rank'] = [near_rank, near_score]

        card.save()
        script.save()
        self.mm.user.save()

        return {
            'user_rank_up': 3,  # 用户排名上升



            'reward': reward,  # 获得的杀青奖励
            'income': all_income,  # 总票房
            'end_lv': end_lv,  # 票房评级
        }

    def finished_analyse(self):
        """票房分析"""
        return {

        }

    def check_finished_step(self, finished_step):
        """
        :param finished_step:
            1： 经验、熟练度什么的通用奖励
            2： 拍摄属性结算
            3： 弹出新闻关注度
            4： 首日上映
            5： 专业评价
            6： 观众评价
            7： 持续上映
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
            key = 'finished_audience_judge'
            func = self.calc_audience_judge

        elif finished_step == 7:
            key = 'finished_curve'
            func = self.calc_curve

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

    # 6.艺人的拍摄发挥,选卡算一次，选类型算一次
    def calc_film_card_effect(self, action='set_card'):
        card = self.mm.card
        script = self.mm.script
        cur_script = script.cur_script
        script_config = game_config.script[cur_script['id']]

        pro = cur_script['pro']

        match_score = 0
        match_script = {}  # 艺人对剧本发挥
        match_role = {}  # 艺人对角色发挥
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

            dps_rate = random.randint(*love_config['dps_rate'])  # 伤害系数 万分之

            role_config = game_config.script_role[role_id]
            role_attr = list(role_config['role_attr'])
            # 随机属性
            more_attr = []
            if random.randint(0, 10000) <= card_config['ex_special_rate']:
                special_attr = weight_choice(card_config['special_quality'])[0]
                more_attr.append(special_attr)

            role_effect = effect[role_id] = {}
            # 计算属性
            for attr in role_attr:
                base_value = card_info['char_pro'][card.PRO_IDX_MAPPING[attr]]
                if base_value < 0:
                    continue
                value = math.ceil(base_value * dps_rate / 10000.0)
                if attr in role_effect:
                    role_effect[attr][0] += value
                else:
                    role_effect[attr] = [value, False]

            # 判断是否暴击
            c1 = card_config['crit_rate_base'] / 10000.0
            c2 = (role_score + script_score) / 100.0
            crit_rate = c1 + c2
            if random.random() < crit_rate:
                # 暴击效果
                d = (role_score + script_score) / 100.0
                for attr in role_effect:
                    role_effect[attr][0] = math.ceil(role_effect[attr][0] * (1.1 + d))
                    role_effect[attr][1] = True

            for attr in more_attr:
                base_value = card_info['char_pro'][card.PRO_IDX_MAPPING[attr]]
                if base_value < 0:
                    value = 1
                else:
                    value = math.ceil(base_value * dps_rate / 10000.0)
                if attr in role_effect:
                    role_effect[attr][0] += value
                else:
                    role_effect[attr] = [value, False]

        return {
            'effect': effect,
            'match_script': match_script,
            'match_role': match_role
        }

    def upgrade_continued_level(self, script_id):
        script = self.mm.script
        if script_id not in script.continued_script:
            return 1, {}

        script_info = script.continued_script[script_id]
        now = int(time.time())
        if script_info['continued_expire'] - now <= 60:
            return 3, {}  #推广时间已过
        continued_lv = script_info['continued_lv']
        if continued_lv + 1 not in game_config.script_continued_level:
            return 2, {}  # 已是最大等级

        continued_lv_config = game_config.script_continued_level[continued_lv + 1]
        upgrade_cost = continued_lv_config['upgrade_cost']
        rc, _ = del_mult_goods(self.mm, upgrade_cost)
        if rc:
            return rc, {}


        continued_start = script_info['continued_start']
        div, mod = divmod(now - continued_start, 60)
        last_dollar = 0
        if div:
            last_dollar = div * script_info['continued_income_unit']
            continued_start = now - mod

        # 开发环境改时间可能会出负数，处理下
        last_dollar = max(last_dollar, 0)

        finished_summary = script_info['finished_summary']
        all_income = finished_summary['income']

        continued_income = continued_lv_config['parm'] * all_income / 100
        continued_time = game_config.common[19]
        continued_income_unit = continued_income / continued_time

        script_info['continued_lv'] = continued_lv + 1
        script_info['continued_income_unit'] = continued_income_unit
        script_info['continued_start'] = continued_start
        script_info['continued_income'] += last_dollar

        self.mm.user.add_dollar(last_dollar)
        self.mm.user.save()
        script.save()
        return 0, {
            'reward': {'dollar': last_dollar},
            'continued_script': script.continued_script
        }

    def get_continued_reward(self, script_id):
        script = self.mm.script
        if script_id not in script.continued_script:
            return 1, {}

        script_info = script.continued_script[script_id]
        now = int(time.time())
        if now >= script_info['continued_expire']:
            now = script_info['continued_expire']

        continued_start = script_info['continued_start']
        div, mod = divmod(now - continued_start, 60)
        last_dollar = 0
        if div:
            last_dollar = div * script_info['continued_income_unit']
            continued_start = now - mod

        # 开发环境改时间可能会出负数，处理下
        last_dollar = max(last_dollar, 0)
        script_info['continued_start'] = continued_start
        script_info['continued_income'] += last_dollar
        if now <= continued_start or script_info['continued_expire'] - continued_start < 60:
            script.continued_script.pop(script_id)
            script.save()

        self.mm.user.add_dollar(last_dollar)
        self.mm.user.save()
        script.save()

        return 0, {
            'reward': {'dollar': last_dollar},
            'continued_script': script.continued_script
        }


def genearte_random_event():
    """随机事件"""
    Script.set_random_event()


def genearte_global_event():
    """全服事件"""
    Script.set_global_event()
