#! --*-- coding: utf-8 --*--

__author__ = 'ljm'

import time

from lib.db import ModelBase
from lib.utils import salt_generator
from lib.core.environ import ModelManager

from gconfig import game_config
from gconfig import get_str_words
from lib.utils import weight_choice
import random


class Director(ModelBase):
    """导演类
        directors： 所有导演
            {'1-1535098928-2fMmYB':
                {
                  'id': 1,          # 配置中的id
                  'lv': 1,          # 等级
                  'oid': '1-1535098928-2fMmYB', # 唯一id
                  'star': 1
                  }
              }
        """

    _need_diff = ('directors', 'director_box')
    TYPEMAPPING = {1: 'web', 2: 'introduce', 3: 'headhunter'}

    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            'directors': {},  # 所有导演
            'director_box': 1,  # 导演格子
            'web_times': 0,  # 网站招聘次数
            'web_recover_time': 0,  # 网站招聘刷新时间
            'introduce_times': 0,  # 熟人介绍次数
            'introduce_recover_time': 0,  # 熟人介绍刷新时间
            'headhunter_times': 0,  # 猎头招聘次数
            'refresh_date': '',  # 刷新日期
            'gacha_pool': {},  # gacha
            'add_gacha_times': 0,
        }
        super(Director, self).__init__(self.uid)

    @classmethod
    def _make_oid(cls, director_id):
        """ 生成导演only id

        :param director_id:
        :return:
        """
        return '%s-%s-%s' % (director_id, int(time.time()), salt_generator())

    @classmethod
    def generate_director(cls, director_id, director_config=None, lv=1, pos=0):
        """
        生成导演信息
        :param director_id: 
        :param director_config: 
        :param lv: 
        :param pos: 
        :return: 
        """
        director_oid = cls._make_oid(director_id)
        director_config = director_config or game_config.director[director_id]

        director_dict = {
            'id': director_id,  # 配置id
            'oid': director_oid,  # 唯一id
            'star': director_config.get('star', 1),  # 星级
            'lv': lv,  # 等级
            'pos': pos,
        }

        return director_oid, director_dict

    def add_director(self, director_id, lv=None):
        """
        添加导演
        :param director_id: 
        :param lv: 
        :return:  director_oid
        """
        init_lv = lv or 1
        if director_id in self.all_director:
            return False
        director_oid, director_dict = self.generate_director(director_id, lv=init_lv)
        self.directors[director_oid] = director_dict
        return director_oid

    def pre_use(self):
        today = time.strftime('%F')
        if self.refresh_date != today:
            self.refresh_date = today
            self.web_times = 0
            self.headhunter_times = 0
            self.introduce_times = 0
            self.web_recover_time = int(time.time())
            self.introduce_recover_time = int(time.time())
            self.add_gacha_times = 0
            self.save()

    @property
    def total_times(self):
        """
        总招聘次数
        :return: 
        """
        return self.web_times + self.headhunter_times + self.introduce_times

    @property
    def all_director_pos(self):
        """
        所有位置信息
        :return: {pos:director_id}
        """
        result = {}
        for director_id, info in self.directors.iteritems():
            if info['pos']:
                result[info['pos']] = director_id
        return result

    @property
    def empty_pos(self):
        """
        闲置的导演位置
        :return: [1, 2]
        """
        all_pos = range(1, self.director_box + 1)
        director_pos = self.all_director_pos.keys()
        return list(set(all_pos) - set(director_pos))

    def recover_need_time(self, tp):
        """
        gacha cd时间
        :param tp: 
        :return: 
        """
        gacha_cd = game_config.director_gacha_cost[tp]['cd']
        gacha_type = '%s_times' % (self.TYPEMAPPING[tp])
        times = getattr(self, gacha_type)
        if times == 0:
            return 0
        if times >= len(gacha_cd):
            times = -1
        else:
            times -= 1
        return gacha_cd[times] * 60 - self.mm.user.build_effect.get(14, [0, 0])[0]

    def remain_time(self, tp):
        """
        gacha恢复剩余时间
        :param tp: 
        :return: 
        """
        if tp == 3:
            return 0
        now = int(time.time())
        gacha_recover_type = '%s_recover_time' % (self.TYPEMAPPING[tp])
        gacha_recover_time = getattr(self, gacha_recover_type)
        need_time = self.recover_need_time(tp)
        remain_time = gacha_recover_time + need_time - now
        return remain_time if remain_time > 0 else 0

    @property
    def total_gacha_times(self):
        """
        招聘次数上限
        :return: 
        """
        return self.add_gacha_times + game_config.common[86] + self.mm.user.build_effect.get(14, [0, 0])[1]

    @property
    def all_director(self):
        """
        :return: 
            [13, 12]
        """
        all_directors = []
        for i, j in self.directors.iteritems():
            all_directors.append(j['id'])
        return all_directors

    def get_director_info(self, director_dict):
        """
        :param director_dict: 
        :return: {
            'att': 3,
             u'id': 12,
             u'lv': 2,
             u'oid': u'12-1550160540-DsuaSs',
             u'pos': 0,
             'pro': [0, 1, 0, 0, 0, 0],  # 属性加成值
             u'star': 1
        """
        if isinstance(director_dict, basestring):
            director_dict = self.directors[director_dict]
        config = game_config.director[director_dict['id']]
        pro_base = config['pro']
        att_base = config['att']
        lv = director_dict['lv']
        param_config = game_config.director_lv.get(lv, {})
        att = int(att_base * (param_config.get('att_param', 0) / 10000.0 + 1))
        pro_param = param_config.get('pro_param', 0) / 10000.0
        pro = [int(i * (pro_param + 1)) for i in pro_base]
        director_dict['pro'] = pro
        director_dict['att'] = att
        return director_dict

    def refresh_gacha(self, tp):
        """
        刷新gacha
        :param tp: 
        :return: 
        """

        gacha_config = game_config.get_director_gacha_mapping().get(tp)
        gacha = []
        g_pool = []
        for id, weight in gacha_config:
            if id not in self.all_director:
                g_pool.append([id, weight])
        if len(g_pool) <= 0:
            return []
        max_num = min(len(g_pool), 3)
        while len(gacha) < max_num:
            gahca_id = []
            while not gahca_id or (gahca_id and gahca_id[0] in gacha):
                gahca_id = weight_choice(g_pool)
            gacha.append(gahca_id[0])
        self.gacha_pool[tp] = gacha
        times = getattr(self, '%s_times' % (self.TYPEMAPPING[tp])) + 1
        setattr(self, '%s_times' % (self.TYPEMAPPING[tp]), times)
        setattr(self, '%s_recover_time' % (self.TYPEMAPPING[tp]), int(time.time()))

        return gacha

    def get_directing_id(self, script_id):
        """
        :param script_id: 
        :return: [1,2,3]
        """
        if not self.all_director_pos:
            return []
        config = game_config.script[script_id].get('directing_policy',[])
        num = min(len(config),3)
        return random.sample(config, num)

    def director_skill_effect(self, directing_id, script_id):
        """
        导演组技能效果
        :param directing_id: 指导方针id
                script_id: 剧本id
        :return: 
        {'pro': [0, 1, 1, 0, 0, 0],  # 导演自己加成属性
             'skill_12_effect': {1: {'profession_type': 1, 'sex_type': 2},  # role_id:{} 效果12生效后的 角色要求
                                  2: {'profession_class': 2, 'sex_type': 2},  
                                  3: {'sex_type': 2},
                                  4: {'sex_type': 1},
                                  6: {'profession_class': 2, 'profession_type': 2}},
             'skill_effect': {1: 30,  # key 是skill_effect id
                          2: 30,
                          4: 30,
                          5: 30,
                          6: 30,
                          7: 30,
                          8: 30,
                          9: 30,
                          10: 30,
                          11: 30,
                          12: 30,
                          'skill_pro': [30, 30, 0, 30, 30, 0]},  # 技能加成属性 把skill_effect里<=6的值改成通用格式后的值
             'skills': [1, 2, 4, 5]}  # 生效技能
        skill_pro 对应艺人属性格式
        skill_effect key对应影响类型
            1全体艺人演技加成
            2全体艺人歌艺加成
            3全体艺人气质加成
            4全体艺人动感加成
            5全体艺人艺术加成
            6全体艺人娱乐加成
            7增加首映票房万分比
            8增加持续收益万分比
            9增加后续收益万分比
            10增加点赞获取万分比
            11增加人气数值
            12随机减少角色要求数量
        """
        result = {}
        config = game_config.directing_policy
        director_config = game_config.director
        director_skillid = config[directing_id]['director_skillid']
        skill_config = game_config.director_skill
        script_config = game_config.script[script_id]
        script_tag = script_config['tag_script']
        director_att = 0
        director_pro = [0, 0, 0, 0, 0, 0]

        # 导演执导能力，属性加成
        for pos, directer_oid in self.all_director_pos.iteritems():
            d_config = director_config[self.directors[directer_oid]['id']]
            d_tag = d_config['tag']
            director_dict = self.get_director_info(directer_oid)
            tag_effect = 1 if len(set(d_tag) - set(script_tag)) == len(set(d_tag)) else 0
            d_att = director_dict['att']
            d_pro = director_dict['pro']
            d_att = int(d_att * 0.85) if tag_effect else d_att
            director_att += d_att
            director_pro = [director_pro[i] + d_pro[i] for i in range(6)]

        # 生效技能
        skills = []
        for skill_id, weight in director_skillid:
            if weight >= random.randint(1, 10000):
                skills.append(skill_id)

        # 技能加成
        skill_effect = {'skill_pro': [0, 0, 0, 0, 0, 0]}
        if director_att:
            for skill_id in skills:
                s_config = skill_config[skill_id]
                if s_config['skill_type'] <= 6:
                    skill_effect['skill_pro'][s_config['skill_type'] - 1] += int(
                    (1 + director_att * 1.0 / s_config['dskill_param']) * s_config['value'])
                if s_config['skill_type'] not in skill_effect:
                    skill_effect[s_config['skill_type']] = 0
                skill_effect[s_config['skill_type']] += int(
                    (1 + director_att * 1.0 / s_config['dskill_param']) * s_config['value'])
        result['pro'] = director_pro
        result['skill_effect'] = skill_effect
        result['skills'] = skills
        result['skill_12_effect'] = self.director_skill_effect12(script_id,skill_effect.get(12, 0))

        return result

    def director_skill_effect12(self, script_id, skill_effect):
        """
        导演技能效果12 生效
        script_id :1
        skill_effect: 1  # 导演技能效果里 12 的值
        :return: 
        """
        roles = game_config.script[script_id]['role_id']
        tps = ['sex_type', 'profession_class', 'profession_type']
        config = game_config.script_role
        role_class = {'effect':{}}
        for role_id in roles:
            if role_id not in role_class:
                role_class[role_id] = {}
            for tp in tps:
                if config[role_id].get(tp, 0):
                    role_class[role_id][tp] = config[role_id].get(tp, 0)
        for _ in range(skill_effect):
            ct = 0
            for role, value in role_class.iteritems():
                if sum(value.values()):
                    ct = 1
                    break
            if not ct:
                break
            role_id = 0
            while not role_id:
                role_id = random.choice(roles)
                if not sum(role_class[role_id].values()):
                    role_id = 0
            r_tp = random.choice(role_class[role_id].keys())
            role_class[role_id].pop(r_tp)
            if role_id not in role_class['effect']:
                role_class['effect'][role_id] = []
            role_class['effect'][role_id].append(r_tp)
        return role_class

    def get_directors_value(self):
        directors_value_dict = {}
        for i, v in self.directors.iteritems():
            sum_value = 0
            if not v['pos']:
                continue
            sum_value += game_config.body_value[v['star']+19]['value']
            sum_value += v['lv'] * game_config.body_value[v['star']+13]['value']
            directors_value_dict[i] = sum_value
        return directors_value_dict



ModelManager.register_model('director', Director)
