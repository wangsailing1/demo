# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
import math
import random
import itertools
import settings
from gconfig import game_config

from lib.db import ModelBase, get_redis_client
from lib.utils import salt_generator
from lib.utils import weight_choice
from lib.utils import merge_dict
from lib.core.environ import ModelManager
from models.ranking_list import AppealRank, BlockRank
from models.block import get_date
from models.vip_company import extra_script


class Script(ModelBase):
    POOL_SIZE = 3
    MAX_EVENT = 24
    RECENT_EVENT_NUM = 3

    _need_diff = ('own_script',)
    SEXMAPPING = {1: 'nv', 2: 'nan'}

    def __init__(self, uid=None):
        """

        :param uid:

            top_sequal:
                { group_id: {
                        'last_top_income': 0,
                        'cur_top_income': 0,
                        'top_script': {}
                    }
                },
            top_end_lv_card: {
                script_id: {
                    'end_lv: 1,
                    'card': {
                        role_id: card_oid
                    }
                }
            }
        """
        self.uid = uid
        self._attrs = {
            'refresh_date': '',

            'newbie': True,         # 是否新用户首次拍片
            'sequel_script': [],  # 已获得的可拍摄的续集片子
            'continued_script': {},         # 持续收益的片子
            'style_log': [],                # 连续拍片类型，保留最近10个
            'own_script': [],               # 已获得的可拍摄的片子
            'directing_times': 0,           # 当天导演次数
            'reselection_times': 0,         # 本次拍摄剧本池更新次数

            'group_sequel': {},  # 每个系列的可拍续集

            'cur_script': {},  # 当前在在拍的片子

            'scripts': {},  # 所有已拍完的片子

            'script_pool': {},
            'sequel_script_pool': {},
            'cur_market': [],  # 当前市场关注度
            'cur_market_show': [],  # 当前市场关注度显示用


            # 各种最高收入排行
            'top_script': {},               # 按剧本id
            'top_all': {},                  # 单片票房最高
            'top_end_lv_card': {},          # 剧本最高结算等级对应的演员列表 {script_id: {'env_lv': 1, 'card': {roleid: cardid}}}

            # 最高系列票房总和
            'top_sequal': {},

            'end_lv_log': {}  # 剧本大卖统计 {script_id: {end_lv: times}}

        }
        self.global_cache = self.get_global_redis_client()
        super(Script, self).__init__(self.uid)

    @classmethod
    def get_global_redis_client(cls):
        return get_redis_client(settings.SERVERS['public']['redis'])

    @classmethod
    def generate_random_event_key(cls, date_str=None):
        # key = '%s_%s' % (cls.make_key_cls('random_event', 'public'), date_str or time.strftime('%F'))
        key = '%s_%s' % (cls.make_key_cls('random_event', 'public'), '')
        return key

    @classmethod
    def generate_global_event_key(cls, date_str=None):
        # key = '%s_%s' % (cls.make_key_cls('global_event', 'public'), date_str or time.strftime('%F'))
        key = '%s_%s' % (cls.make_key_cls('global_event', 'public'), '')
        return key

    @classmethod
    def set_random_event(cls, date_str=None):
        redis = cls.get_global_redis_client()
        key = cls.generate_random_event_key(date_str)

        id_weights = [(k, v['weight']) for k, v in game_config.random_event.iteritems()]
        event_id = weight_choice(id_weights)[0]
        # 最近3条事件不能重复
        recent_events = [int(i.split('_')[1]) for i in redis.lrange(key, 0, cls.RECENT_EVENT_NUM - 1)]
        retry = 0
        while recent_events and event_id in recent_events:
            event_id = weight_choice(id_weights)[0]
            retry += 1
            if retry >= 20:
                break

        redis.lpush(key, '%s_%s' % (int(time.time()), event_id))
        redis.ltrim(key, 0, cls.MAX_EVENT)     # 留最近24条
        return event_id

    @classmethod
    def get_random_event(cls, date_str=None):
        redis = cls.get_global_redis_client()
        key = cls.generate_random_event_key(date_str)

        rs = redis.lrange(key, 0, 0)
        if not rs:
            return
        ts, event_id = rs[0].split('_')
        expire = game_config.common[61]
        if time.time() - int(ts) < expire:
            return int(event_id)

    @classmethod
    def set_global_event(cls, date_str=None):
        redis = cls.get_global_redis_client()
        key = cls.generate_global_event_key(date_str)

        id_weights = [(k, v['weight']) for k, v in game_config.global_market.iteritems()]
        event_id = weight_choice(id_weights)[0]
        # 最近3条事件不能重复
        recent_events = [int(i.split('_')[1]) for i in redis.lrange(key, 0, cls.RECENT_EVENT_NUM - 1)]
        retry = 0
        while recent_events and event_id in recent_events:
            event_id = weight_choice(id_weights)[0]
            retry += 1
            if retry >= 20:
                break

        redis.lpush(key, '%s_%s' % (int(time.time()), event_id))
        redis.ltrim(key, 0, cls.MAX_EVENT)     # 留最近24条
        return event_id

    @classmethod
    def get_global_event(cls, date_str=None):
        redis = cls.get_global_redis_client()
        key = cls.generate_global_event_key(date_str)

        rs = redis.lrange(key, 0, 0)
        if not rs:
            return
        ts, event_id = rs[0].split('_')
        expire = game_config.common[61]
        if time.time() - int(ts) < expire:
            return int(event_id)

    @classmethod
    def recent_event(cls, date_str=None):
        """给前端看的最近几条事件信息"""
        data = []
        redis = cls.get_global_redis_client()
        random_key = cls.generate_random_event_key(date_str)
        global_key = cls.generate_global_event_key(date_str)

        random_event = redis.lrange(random_key, 0, cls.RECENT_EVENT_NUM)
        for i in random_event:
            ts, event_id = map(int, i.split('_'))
            data.append((event_id, ts, 'random'))

        global_event = redis.lrange(global_key, 0, cls.RECENT_EVENT_NUM)
        for i in global_event:
            ts, event_id = map(int, i.split('_'))
            data.append((event_id, ts, 'global'))
        data.sort(key=lambda x: x[1])
        return data[-5:]

    def pre_use(self):
        today = time.strftime('%F')
        if self.refresh_date != today:
            self.refresh_date = today
            self.directing_times = 0

        # todo 开发期容错，不走数据升级， 上线后删除
        if self.cur_script:
            for i in ['director_effect', 'skill_effect']:
                if i not in self.cur_script:
                    self.cur_script[i] = {}

        # 连续拍片类型，保留最近10个
        self.style_log = self.style_log[-10:]
        # if self.cur_script:
        #     if 'finished_step' not in self.cur_script:
        #         self.cur_script['finished_step'] = 0
        #     for k in ['finished_common_reward', 'finished_attr', 'finished_attention',
        #               'finished_first_income', 'finished_summary']:
        #         if k not in self.cur_script:
        #             self.cur_script[k] = {}

        for k, v in self.top_end_lv_card.items():
            if 'env_lv' in v:
                v['end_lv'] = v.pop('env_lv')

        save = False
        # todo 拍摄完的片子结算 9 是票房分析，目前流程没有
        if self.cur_script.get('finished_step') in [8, 9]:
            cur_script = self.cur_script
            # 进入持续收益流程
            self.continued_script[cur_script['oid']] = cur_script

            finished_summary = cur_script['finished_summary']
            all_income = finished_summary['income']

            end_lv = cur_script['end_lv']
            end_lv_config = game_config.script_end_level[end_lv]
            continued_lv = end_lv_config['continued_level']
            continued_lv_config = game_config.script_continued_level[continued_lv]

            continued_income = continued_lv_config['parm'] * all_income / 100
            # 计算导演加成
            director_add_value = self.calc_director_effect(9, continued_income)
            # 技能效果
            skill_add_value = self.calc_skill_effect(13, continued_income)
            continued_income = continued_income + director_add_value + skill_add_value

            continued_time = game_config.common[19]
            continued_income_unit = continued_income / continued_time

            now = int(time.time())
            cur_script['continued_lv'] = continued_lv
            cur_script['continued_income'] = 0
            cur_script['continued_income_unit'] = continued_income_unit
            cur_script['continued_expire'] = now + continued_time * 60
            cur_script['continued_start'] = now

            # 是否有续作需要激活, 在summary接口里调用了
            # self.check_next_sequel(cur_script, cur_script['finished_summary']['income'])
            g_id, all_income = self.get_group_id_all_income(cur_script)
            auid = self.uid
            aoutput = self.mm.get_obj_tools('alloutput_rank')  # uid 格式 uid
            if all_income > aoutput.get_score(uid=auid):
                aoutput.add_rank(auid, all_income)

            self.check_top_end_lv_card(cur_script)
            self.check_top_income(cur_script)
            self.cur_script = {}
            self.script_pool = {}
            self.cur_market = []
            self.sequel_script_pool = {}

            save = True

            # if cur_script['step'] == 4:
            #     self.scripts[cur_script['oid']] = cur_script
            #     self.cur_script = {}

        # 清除过期影片
        for k, v in self.continued_script.items():
            if 'continued_income' not in v:
                v['continued_income'] = 0
            if v.get('continued_start', 0) >= v.get('continued_expire', 0):
                self.continued_script.pop(k)

        if save:
            self.save()

    def max_directing_times(self):
        return game_config.common[93]

    @property
    def top_group(self):
        """按剧本系列 {gruop_id: film_info}
        :return:
        """
        data = {}
        for script_id, info in self.top_script.iteritems():
            script_config = game_config.script[info['id']]
            group_id = script_config['group']
            if group_id not in data:
                data[group_id] = info
            elif info['finished_summary']['income'] > data[group_id]['finished_summary']['income']:
                data[group_id] = info
        return data

    def calc_director_effect(self, sort, value=0):
        """
        计算导演对拍片各个阶段的效果

        :param sort:
                    1~6 六种属性的数值加成

                    7 首映票房万分比
                    8 每日上映收益万分比
                    9 下映后持续收益万分比
                    10 点赞数获取万分比         ps: 向上取整
                    11 关注度数值， 选完导演后直接增加关注度
                    12 随机减少角色要求数量      ps： 在导演模块里已经处理完了
        :param value:
        :return:
        """
        # 计算导演加成
        director_effect = self.cur_script.get('director_effect')
        add_value = 0
        if director_effect:
            if sort in [1, 2, 3, 4, 5, 6]:
                add_value = director_effect['skill_effect'].get(sort, 0)
            elif sort in [7, 8, 9, 10]:
                rate = director_effect['skill_effect'].get(sort, 0)
                if sort == 10:
                    add_value = int(math.ceil(value * rate / 10000.0))
                else:
                    add_value = int(value * rate / 10000.0)
            elif sort == 11:
                add_value = director_effect['skill_effect'].get(sort, 0)
        return int(add_value)

    def calc_skill_effect(self, sort, value=0):
        """
        计算卡牌技能对拍片各个阶段的效果

        :param sort:
                    1~6 六种属性的数值加成

                    7暴击crit_rate_base
                    8额外触发万分比ex_special_rate
                    9艺人片酬降低
                    10关注度加成
                    11首映票房加成
                    12总票房加成
                    13持续收益加成
                    14拍摄类型经验
                    15媒体口碑加成
                    16培养花费下降
                    17粉丝活动产出金币加成

                    {card_oid1: {
                        effect: {
                            sort: {method: value},
                            3: {1: 111},,
                            5: {2: 222},,
                        },
                      }
                    }

        :param value:
        :return:
        """
        # 计算卡牌技能加成
        skill_effect = self.cur_script.get('skill_effect')
        add_value = 0
        if skill_effect:
            all_effect = {}
            for card_oid, card_effect in skill_effect.iteritems():
                for sort, effect in card_effect.get('effect', {}).iteritems():
                    sort_all_effect = all_effect.setdefault(sort, {})
                    merge_dict(sort_all_effect, effect)

            sort_effect = all_effect.get(sort, {})
            for method, method_value in sort_effect.iteritems():
                if method == 2 or sort in [7]:
                    add_value += value * method_value / 10000.0
                elif method == 1:
                    add_value += method_value

        return int(add_value)

    def script_continued_summary(self):
        """持续收入片子信息统计
        :return:
        """
        now = int(time.time())
        min_expire = 0
        has_reward = False
        for oid, info in self.continued_script.iteritems():
            has_reward = has_reward or (now - info['continued_start']) >= 60    # 按分钟恢复

            expire = info['continued_expire'] - now
            if expire < 0:
                continue
            # expire = info['continued_expire'] - info['continued_start']
            if not min_expire or expire < min_expire:
                min_expire = expire

        return {
            'count': len(self.continued_script),
            'min_expire': min_expire,
            'has_reward': has_reward,
            'continued_script': self.get_continued_script(),
        }

    def check_top_end_lv_card(self, cur_script):
        """判断影片最大结算等级对应的演员表
        :param cur_script:
        :return:
        """
        script_id = cur_script['id']
        if script_id not in self.top_end_lv_card:
            self.top_end_lv_card[script_id] = {
                'end_lv': cur_script['end_lv'],
                'card': dict(cur_script['card'])
            }
        else:
            last_script = self.top_end_lv_card[script_id]
            if cur_script['end_lv'] > last_script['end_lv']:
                last_script['end_lv'] = cur_script['end_lv']
                last_script['card'] = dict(cur_script['card'])

    def get_group_id_all_income(self, cur_script):
        '''
        获取组id，跟最大系列票房
        :param cur_script: 
        :return: 
        '''
        script_id = cur_script['id']
        script_config = game_config.script[script_id]
        group_id = script_config['group']
        income = self.top_sequal[group_id]['last_top_income']
        return group_id, income

    def check_next_sequel(self, cur_script, finished_income):
        """根据大卖与否开启续作"""
        script_id = cur_script['id']
        script_config = game_config.script[script_id]
        sequel_count = script_config['sequel_count']
        group_id = script_config['group']
        next_id = script_config['next_id']
        max_sequel_id = extra_script(self.mm.user)[script_config['star'] - 1]
        if next_id and game_config.script[next_id]['sequel_count'] > max_sequel_id:
            next_id = 0

        end_lv = cur_script['end_lv']
        end_lv_config = game_config.script_end_level[end_lv]
        group_info = self.top_sequal.setdefault(group_id, {
            'last_top_income': 0,
            'cur_top_income': 0,
            'top_script': cur_script,
        })

        has_next = False
        if end_lv_config['if_next_script']:
            # 大卖
            # 判断是否拍的续集,累计票房
            if sequel_count:
                group_info['cur_top_income'] += finished_income
            else:
                # 重新拍的第一部,先检查下已拍的总票房是否大于上一次系列
                if group_id in self.group_sequel:
                    if group_info['cur_top_income'] > group_info['last_top_income']:
                        group_info['last_top_income'] = group_info['cur_top_income']

                group_info['cur_top_income'] = finished_income

            if group_info['cur_top_income'] > group_info['last_top_income']:
                group_info['last_top_income'] = group_info['cur_top_income']
                group_info['top_script'] = cur_script

            if next_id:
                if group_id not in self.group_sequel:
                    self.group_sequel[group_id] = next_id
                    has_next = True
                else:
                    last_script_config = game_config.script[self.group_sequel[group_id]]
                    if sequel_count >= last_script_config['sequel_count']:
                        self.group_sequel[group_id] = next_id
                        has_next = True
            else:
                # 没有next_id，sequel_count不为0，当前系列最后一部
                if sequel_count:
                    # 结算系列票房
                    self.group_sequel.pop(group_id, '')
        else:
            # 未大卖
            # 判断是否拍的续集,累计票房
            if sequel_count:
                self.group_sequel.pop(group_id, '')
                group_info['cur_top_income'] += finished_income
            else:
                # 重新拍的第一部,先检查下已拍的总票房是否大于上一次系列
                if group_id in self.group_sequel:
                    if group_info['cur_top_income'] > group_info['last_top_income']:
                        group_info['last_top_income'] = group_info['cur_top_income']

                group_info['cur_top_income'] = finished_income

            if group_info['cur_top_income'] > group_info['last_top_income']:
                group_info['last_top_income'] = group_info['cur_top_income']
                group_info['top_script'] = cur_script
        return has_next and next_id

    def check_top_income(self, film_info):
        script_id = film_info['id']
        script_config = game_config.script[script_id]

        cur_top_script = self.top_script.get(script_id, {})
        income = film_info['finished_summary']['income']

        save = False
        # 按剧本id记录
        top_script_income = cur_top_script.get('finished_summary', {'income': 0})['income']
        if top_script_income < income:
            self.top_script[script_id] = dict(film_info)
            save = True

        # 单片记录
        top_income = self.top_all.get('finished_summary', {'income': 0})['income']
        if top_income < income:
            self.top_all = dict(film_info)
            save = True

        # 记录街区总排行（显示用,按剧本）
        block_rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
                                                      'script')
        br = BlockRank(block_rank_uid, self._server_name)
        date = get_date()

        # 记录当天街区拍片记录
        cur_block_top_script = self.mm.block.top_script.get(date, {}).get(script_id, {})
        top_block_script_income = cur_block_top_script.get('finished_summary', {'income': 0})['income']
        if top_block_script_income < income or film_info.get('end_lv', 0) >= 6:
            if date not in self.mm.block.top_script:
                self.mm.block.top_script[date] = {}
            big_sale = self.mm.block.top_script[date].get(script_id, {}).get('big_sale_num', 0)
            if top_block_script_income < income:
                self.mm.block.top_script[date][script_id] = dict(film_info)
            if film_info.get('end_lv', 0) >= 6:
                big_sale += 1
                self.mm.block.big_sale += 1
            self.mm.block.top_script[date][script_id]['big_sale_num'] = big_sale
            if len(self.mm.block.top_script) >= 2:
                del_date = min(self.mm.block.top_script.items(), key=lambda x: x[0])[0]
                self.mm.block.top_script.pop(del_date)
            save = True

        # uid格式 uid_scriptid
        br_uid = "%s_%s" % (self.uid, script_id)
        br_score = br.get_score(br_uid)
        if income > br_score:
            br.add_rank(br_uid, income)

        # # 记录街区总排行（显示用,按票房）
        # block_income_rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
        #                                                      'income')
        # bir = BlockRank(block_income_rank_uid, self._server_name)
        # old_rank = bir.get_rank(self.uid)
        # old_score = bir.get_score(self.uid)
        # bir.incr_rank(self.uid, income)
        # new_rank = bir.get_rank(self.uid)
        # new_score = bir.get_score(self.uid)

        # self.cur_script['old_rank'] = [old_rank,old_score]
        # self.cur_script['new_rank'] = [new_rank, new_score]

        # 按剧本类型记录排行（发奖用）
        script_type = script_config['type']
        block_type_rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
                                                           script_type)
        btr = BlockRank(block_type_rank_uid, self._server_name)
        # uid格式 uid_scriptid
        btr_score = btr.get_score(br_uid)
        if income > btr_score:
            btr.add_rank(br_uid, income)

        # 按媒体评分记录排行（发奖用）'medium'
        block_medium_rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
                                                             'medium')
        bmr = BlockRank(block_medium_rank_uid, self._server_name)
        medium_score = film_info['finished_medium_judge']['score']
        # uid格式 uid_scriptid
        bmr_score = bmr.get_score(br_uid)
        if medium_score > bmr_score:
            bmr.add_rank(br_uid, medium_score)

        # 按观众评分记录排行（发奖用）'audience'
        block_audience_rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
                                                               'audience')
        bar = BlockRank(block_audience_rank_uid, self._server_name)
        audience_score = film_info['finished_audience_judge']['score']
        # uid格式 uid_scriptid
        bar_score = bar.get_score(br_uid)
        if audience_score > bar_score:
            bar.add_rank(br_uid, audience_score)

        style_id = script_config['style']
        type_id = script_config['type']

        # 记录总的拍片总结
        if script_id not in self.end_lv_log:
            self.end_lv_log[script_id] = {}
        self.end_lv_log[script_id][film_info.get('end_lv', 0)] = self.end_lv_log[script_id].get(
            film_info.get('end_lv', 0), 0) + 1

        # 艺人拍片票房及次数记录
        for role_id, card_id in film_info['card'].iteritems():
            # 按类型记录
            card_info = self.mm.card.cards[card_id]
            card_info['style_income'][style_id] = card_info['style_income'].get(
                style_id, 0) + income
            card_info['style_film_num'][style_id] = card_info['style_film_num'].get(
                style_id, 0) + 1
            # 按种类记录
            card_info['type_income'][type_id] = card_info['type_income'].get(
                type_id, 0) + income
            card_info['type_film_num'][type_id] = card_info['type_film_num'].get(
                type_id, 0) + 1

            card_config = game_config.card_basis[card_info['id']]
            group_id = card_config['group']
            # 记录主角总票房排行
            sex = card_config['sex_type']
            block_sex_rank_uid = self.mm.block.get_key_profix(self.mm.block.block_num, self.mm.block.block_group,
                                                              self.SEXMAPPING[sex])
            bsr = BlockRank(block_sex_rank_uid, self._server_name)
            bsr_uid = "%s_%s" % (self.uid, card_id)
            bsr.incr_rank(bsr_uid, income)

            # 更新艺人号召力排行
            guid = self.uid + '|' + str(group_id)
            ar = self.mm.get_obj_tools('appeal_rank')  # uid 格式 uid + '|' + group_id
            ar.incr_rank(guid, income)

            # 记录当天拍过片的艺人
            if card_id not in self.mm.block.today_card:
                self.mm.block.today_card.append(card_id)
                save = True

        # 记录当天拍过的剧本
        self.mm.block.today_script.append(script_id)

        self.mm.script_book.add_book(script_id)
        self.mm.script_book.add_script_group(script_id, True, income)

        if save:
            self.save()
            self.mm.card.save()
            self.mm.block.save()

    def add_own_script(self, script_id):
        if script_id in self.own_script:
            return False
        self.own_script.append(script_id)
        self.mm.script_book.add_book(script_id)
        return True

    @classmethod
    def _make_oid(cls, script_id):
        """ 生成only id

        :param script_id:
        :return:
        """
        return '%s-%s-%s' % (script_id, int(time.time()), salt_generator())

    def pre_filming(self, re_selection=False):
        self.script_pool = {}
        self.sequel_script_pool = {}
        if re_selection:
            self.reselection_times += 1
        else:
            self.reselection_times = 0

        # 新手引导剧本
        first_scripts = []
        common_scripts = []
        for k, v in game_config.script.iteritems():
            if v.get('first_script'):
                first_scripts.append((k, v['rate']))
            elif k in self.own_script:
                common_scripts.append((k, v['rate']))

        # can_use_ids = [(k, v['rate']) for k, v in game_config.script.iteritems() if k in self.own_script]
        if self.newbie and first_scripts:
            can_use_ids = first_scripts
            self.newbie = False
        else:
            can_use_ids = common_scripts
        for i in xrange(self.POOL_SIZE):
            if not can_use_ids:
                break
            id_weight = weight_choice(can_use_ids)
            can_use_ids.remove(id_weight)
            self.script_pool[id_weight[0]] = 0

        # 续集
        can_use_sequel_ids = [(k, v['rate']) for k, v in game_config.script.iteritems() if
                              k in self.group_sequel.values()]
        for i in xrange(self.POOL_SIZE):
            if not can_use_sequel_ids:
                break
            id_weight = weight_choice(can_use_sequel_ids)
            can_use_sequel_ids.remove(id_weight)
            self.sequel_script_pool[id_weight[0]] = 0

        # 初始化市场关注度
        all_market = [(v['market'], v['rate']) for k, v in game_config.script_market.iteritems()]
        if all_market:
            choiced_market = weight_choice(all_market)
            cur_market = list(choiced_market[0])
            cur_market_show = copy.copy(list(choiced_market[0]))
            del_unit = game_config.common[7]
            # 随机三次减少关注度
            market_length = len(cur_market)
            for i in range(3):
                idx_list = [x for x,y in enumerate(cur_market_show) if y >= del_unit]
                if not idx_list:
                    break
                idx = random.choice(idx_list)
                if cur_market_show[idx] >= del_unit:
                    cur_market_show[idx] = cur_market_show[idx] - del_unit

            self.cur_market = cur_market
            self.cur_market_show = cur_market_show

    def make_film(self, script_id, name):
        script_config = game_config.script[script_id]
        type_config = game_config.script_type_style[script_config['type']]
        data = {
            'skill_effect': {},  # 卡牌技能效果

            're_directing': 0,               # 是否处理过了重拍流程  1： 重拍过，  -1: 跳过重拍， 0 未处理
            'director_effect': {},          # 拍片时候是否有上导演，在logics层检查director模块 director_skill_effect 方法
            'directing_ids': [],             # 导演执导方针
            'cost': 0,  # 拍摄消耗的美金
            'length': random.randint(*type_config['length']),  # 剧集时间/集数
            'step': 1,  # 拍摄进度  1: 艺人选择; 2: 类型选择 3: 宣传预热  4: 杀青
            'finished_step': 0,  # 拍摄结算进度 1: 通用奖励、艺人关注度；2：拍摄属性、熟练度；3：弹出新闻关注度
            # 4: 首日上映; 5: 专业评价; 6: 持续上映; 7: 观众评价
            'name': name,
            'card': {},  # 艺人角色 {rol_id: card_oid}
            'id': script_id,
            'oid': self._make_oid(script_id),
            'style': 0,  # 剧本类型
            'ts': int(time.time()),
            'single_style': False,  # 是否连续同样类型
            'suit': 0,  # 片子类型适合档次
            'pro': [0] * 6,  # 各个属性值

            'result_step': 0,  # 结算阶段，前端修改，前端使用
            'result': {},  # 拍片结算结果 {'reward': {}, }

            # 结算的几个阶段奖励
            'finished_common_reward': {},
            'finished_attr': {},
            'finished_attention': {},
            'finished_first_income': {},
            'finished_curve': {},  # 持续上映曲线
            'finished_medium_judge': {},  # 评价 专业评价 100
            'finished_audience_judge': {},  # 评价 观众评价 200
            'finished_summary': {},  # 票房总结{'income': 100, 'cost': 50},
            'finished_analyse': {},  # 票房分析

            'end_lv': 0,  # 结束档次
            'continued_lv': 0,  # 持续收入等级 可手动升级
            'continued_start': 0,  # 持续收入开始时间
            'continued_expire': 0,  # 持续收入结束时间
            'continued_income': 0,  # 已领取持续收入
            'continued_income_unit': 0,  # 持续收入 每分钟收入数

            'final_attention': 0,  # 关注度
        }
        return data

    def get_top_group_sequel(self):

        top_group = {}
        for group_id, info in self.top_sequal.iteritems():
            if group_id not in top_group:
                top_group[group_id] = {}
            script_id = info['top_script']['id']
            top_group[group_id]['script_info'] = info['top_script']
            top_group[group_id]['top_income'] = info['last_top_income']
            sequel_count = game_config.script[script_id]['sequel_count']
            top_group[group_id]['max_script'] = sequel_count
        return top_group

    def get_top_group_id_sequel(self):
        group_id = 0
        income = 0
        for k, v in self.get_top_group_sequel().iteritems():
            if v['top_income'] > income:
                income = v['top_income']
                group_id = k
        return group_id

    # 获取单片数据
    def get_script_info(self, script_id):
        script_info = self.mm.script.top_script.get(int(script_id), {})
        if not script_info:
            return {}
        all_card = script_info['card']
        card_info = {}
        for k, card_id in all_card.iteritems():
            card_info[card_id] = {'name': self.mm.card.cards[card_id]['name'],
                                  'id': self.mm.card.cards[card_id]['id']}

        script_info['card_info'] = card_info
        return script_info

    # 获取系列票房最大单片
    def get_max_script_by_group(self, group_id):
        group_info = self.get_top_group_sequel().get(group_id, {})
        if not group_info:
            return 0
        return group_info['script_info']['id']

    # 获取前n个数据 1是取剧本，2是去系列
    def get_scrip_info_by_num(self, num=5, is_type=1):
        if is_type == 1:
            script_infos = self.mm.script.top_script
            script_list = sorted(script_infos.items(), key=lambda x: x[1]['finished_summary']['income'], reverse=True)
            if len(script_list) > num:
                script_list = script_list[:num]
            script_info = {i: j for i, j in script_list}
            return script_info
        elif is_type == 2:
            group_infos = self.get_top_group_sequel()
            group_list = sorted(group_infos.items(), key=lambda x: x[1]['top_income'], reverse=True)
            if len(group_list) > num:
                group_list = group_list[:num]
            group_info = {i: j for i, j in group_list}
            return group_info

    # 统计
    def count_info(self):
        # 剧本大卖统计 {script_id: {end_lv: times}}
        end_level = {}
        style_log = {}
        type_log = {}
        for script_id, value in self.end_lv_log.iteritems():
            script_config = game_config.script[script_id]
            tp = script_config['type']
            style = script_config['style']
            for end_lv, times in value.iteritems():
                end_level[end_lv] = end_level.get(end_lv, 0) + times
                style_log[style] = style_log.get(style, 0) + times
                type_log[tp] = type_log.get(tp, 0) + times
        return {
            'end_level': end_level,
            'style_log': style_log,
            'type_log': type_log
        }

    def get_continued_script(self):
        info = []
        now = int(time.time())
        for script_id,value in self.continued_script.iteritems():
            if value['continued_expire'] <= now:
                info.append(script_id)
        return info

    def check_event_effect(self, film_info=None):
        """检查随机事件、全服事件buff
        """
        film_info = film_info or self.cur_script
        script_id = film_info['id']
        script_config = game_config.script[script_id]

        style = script_config['style']
        type = script_config['type']
        global_buff = random_buff = 0

        random_event = self.get_random_event()
        global_event = self.get_global_event()
        if random_event:
            event_config = game_config.random_event[random_event]
            for tp, stp, buff in event_config['effect']:
                if tp and tp != type:
                    continue
                if stp and stp != style:
                    continue
                random_buff += buff

        if global_event:
            event_config = game_config.global_market[global_event]
            for tp, stp, buff in event_config['effect']:
                if tp and tp != type:
                    continue
                if stp and stp != style:
                    continue
                global_buff += buff

        # print 'event_effect: ', all_effect, type, style
        return {
            'global_buff': global_buff,
            'random_buff': random_buff,
        }

    @classmethod
    def generate_all_type_income_key(cls):
        return cls.make_key_cls('all_type_income_%s', '')

    @classmethod
    def generate_luck_type_key(cls):
        return cls.make_key_cls('luck_type', '')

    def clear_type_income_info(self):
        redis = self.global_cache
        income_key = self.generate_all_type_income_key()
        luck_key = self.generate_luck_type_key()
        return redis.delete(income_key, luck_key)

    def set_luck_type(self, script_type):
        """触发爆款类型"""
        redis = self.global_cache
        key = self.generate_luck_type_key()
        redis.hset(key, script_type, int(time.time()))

    def get_luck_info(self):
        """获取当前爆款类型"""
        redis = self.global_cache
        key = self.generate_luck_type_key()
        luck_info = redis.hgetall(key)
        if luck_info:
            return map(int, luck_info.popitem())
        else:
            return [None, None]

    def check_luck_income(self, script_type, first_income):
        """判断本次拍片是否达成全服爆款
        :param script_type:
        :param first_income:
        :return:
        """
        now = int(time.time())
        luck_type, luck_start = self.get_luck_info()
        buff = debuff = 0
        trigge_first_luck = trigge_step_luck = False
        # 当前是否达有爆款类型
        if luck_type:
            if now - luck_start >= 5 * 60:
                # 过期了，清空各种类型票房，重新计数
                self.clear_type_income_info()
            else:
                # 爆款周期内, 按概率触发debuff
                if random.randint(1, 10000) <= game_config.common[66]:
                    debuff += game_config.common[65]
                # 非爆款类型不再计入票房总数
                if luck_type != script_type:
                    return {
                        'income': int(first_income * (1 + (buff + debuff) / 10000.0)),
                        'first_luck': trigge_first_luck,
                        'step_luck': trigge_step_luck,
                        'buff': buff,
                        'debuff': debuff,
                    }

        redis = self.global_cache
        key = self.generate_all_type_income_key()
        cur_income = redis.hincrby(key, script_type, first_income)
        last_income = cur_income - first_income

        limit = game_config.common[62]
        step_limit = game_config.common[63]

        # 首次达成爆款
        trigge_first_luck = last_income < limit <= cur_income

        # 爆款之后达成阶段性票房, 玩家按百分比增加票房
        trigge_step_luck = last_income > limit and \
                                 (cur_income // step_limit > last_income // step_limit)

        if trigge_first_luck:
            self.set_luck_type(script_type)
            buff += game_config.common[64]

        if trigge_step_luck:
            buff += game_config.common[64]
        return {
            'first_income': int(first_income * (1 + (buff + debuff) / 10000.0)),
            'first_luck': trigge_first_luck,
            'step_luck': trigge_step_luck,
            'buff': buff,
            'debuff': debuff,
        }

    # 获取正在拍片的艺人
    def get_used_cards(self):
        cards = []
        for role_id, card_id in self.cur_script.get('card',{}).iteritems():
            cards.append(card_id)
        return cards


ModelManager.register_model('script', Script)
