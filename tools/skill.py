#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 技能管理模块
from lib.utils import merge_dict
from gconfig import game_config
from lib.utils import add_dict


class SkillBase(object):

    def __init__(self, sort, skill_info, skill_config):
        """

        :param sort: 3: 专业技能
        :param skill_info:
        :param skill_config: {'sort': 4, 'type': 6}
        :return:
        """
        self.sort = sort
        self.avail = skill_info['avail']
        self.lv = skill_info['lv']
        self.skill_id = skill_info['s']
        self.skill_config = skill_config

    def get_skill_effect(self):
        """ 获取技能效果

        :return:
        """
        if self.avail == 0:
            return 0

        if not self.sort:
            return 0

        return self.skill_config['skill_effect'] * self.skill_growth_rate()

    def skill_growth_rate(self):
        """ 技能成长率

        :return:
        """
        return game_config.get_skill_growth_rate(self.sort, self.lv)


class SkillNormal(SkillBase):

    def __init__(self, sort, skill_info, skill_config):
        super(SkillNormal, self).__init__(sort, skill_info, skill_config)


class SkillPassive(SkillBase):
    """ 被动技能

    """

    def __init__(self, sort, skill_info, skill_config):
        super(SkillPassive, self).__init__(sort, skill_info, skill_config)


class SkillExtra(SkillBase):
    """ 扩展技能

    """

    def __init__(self, sort, skill_info, skill_config):
        super(SkillExtra, self).__init__(sort, skill_info, skill_config)
        self.tp = self.skill_config['type']             # 类型, 1:矿石,2:木材,3:皮革
        self.config_sort = self.skill_config['sort']    # 1: 能手, 2: 爱好者, 3: 专家, 4: 大师

    def skill_growth_rate(self):
        """ 技能成长率

        :return: 1  # effect
        """
        return game_config.get_extra_skill_growth_rate(self.config_sort, self.lv)

    def get_skill_effect(self):
        """ 获取技能效果

        :return: 1  # effect
        """
        if self.avail == 0:
            return 0

        if not self.sort:
            return 0

        return self.skill_growth_rate()


class SkillFactory(object):
    SORT_NORMAL = 1
    SORT_PASSIVE = 2
    SORT_EXTRA = 3

    def __init__(self, hero_dict):
        self.skills = {}
        self.extra_skills = {}
        for skill_pos, skill_info in hero_dict.get('skill', {}).iteritems():
            if skill_info['avail'] != 1:
                continue
            skill_id = skill_info['s']
            skill_sort, skill_config = game_config.get_skill_config(skill_id)
            if not skill_sort:
                continue
            if skill_sort == self.SORT_NORMAL:
                self.skills[skill_pos] = SkillNormal(skill_sort, skill_info, skill_config)
            elif skill_sort == self.SORT_PASSIVE:
                self.skills[skill_pos] = SkillPassive(skill_sort, skill_info, skill_config)

        for skill_pos, skill_info in hero_dict.get('extra_skill', {}).iteritems():
            if skill_info['avail'] != 1:
                continue
            skill_id = skill_info['s']
            skill_sort, skill_config = game_config.get_skill_config(skill_id)
            if not skill_sort:
                continue
            if skill_sort == self.SORT_EXTRA:
                self.extra_skills[skill_pos] = SkillExtra(skill_sort, skill_info, skill_config)

    def get_passive_effect(self):
        """ 获取被动效果

        :return:
        """
        for skill_pos, skill_obj in self.skills.iteritems():
            if skill_obj.sort == self.SORT_PASSIVE and skill_obj.skill_config['target'] == 1:
                return (skill_obj.skill_config['skill_type'], skill_obj.get_skill_effect())

        return (0, 0)

    def trigger_power_value(self):
        """ 能手, 根据进阶等阶提升能力值

        :return: {
            1: 1        # tp: effect
        }
        """
        value = {}
        for skill_pos, skill_obj in self.extra_skills.iteritems():
            if skill_obj.skill_config['sort'] != 1:
                continue
            if skill_obj.tp not in value:   # tp为 1 矿石 2 木材 3 皮革 4 武器 5 头盔 6 铠甲 7 战靴
                value[skill_obj.tp] = skill_obj.get_skill_effect()
            else:
                value[skill_obj.tp] += skill_obj.get_skill_effect()

        return value

    def trigger_coll_skill_fan(self):
        """ 爱好者 提升某类资源出现权重，升级提升百分比

        :return:
        """
        fan = {}
        for skill_pos, skill_obj in self.extra_skills.iteritems():
            if skill_obj.skill_config['sort'] != 2:
                continue
            if skill_obj.tp not in fan:
                fan[skill_obj.tp] = skill_obj.get_skill_effect()
            else:
                fan[skill_obj.tp] += skill_obj.get_skill_effect()

        return fan

    def trigger_skill_master(self):
        """ 大师 提升一级采集或生产品阶

        :return:
        """
        master = {}
        for skill_pos, skill_obj in self.extra_skills.iteritems():
            if skill_obj.skill_config['sort'] != 4:
                continue
            effect = skill_obj.get_skill_effect()
            if not effect:
                continue
            if skill_obj.tp not in master:
                master[skill_obj.tp] = effect
            else:
                master[skill_obj.tp] += effect

        return master

    def trigger_manu_skill_expert(self):
        """ 专家 提升生产等级

        :return:
        """
        experts = {}
        for skill_pos, skill_obj in self.extra_skills.iteritems():
            if skill_obj.skill_config['sort'] != 3:
                continue
            effect = skill_obj.get_skill_effect()
            if not effect:
                continue
            if skill_obj.tp not in experts:
                experts[skill_obj.tp] = effect
            else:
                experts[skill_obj.tp] += effect

        return experts

    #
    # def trigger_luck_value(self, coll_sort):
    #     """ 提升矿工|伐木工|猎人幸运值
    #
    #     :param coll_sort: 采集类型 1: 矿石 2: 木材 3: 皮革
    #     :return:
    #     """
    #     mapping = {1: 103, 2: 203, 3: 303}
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 3 and skill_obj.skill_config['sort'] == mapping[coll_sort]:
    #             return skill_obj.get_skill_effect()
    #
    #     return 0
    #
    # def trigger_expert(self, coll_id, hero_level):
    #     """ 采集指定采集物时，采集能力上升
    #
    #     :param coll_id: 采集物id
    #     :return:
    #     """
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 3 and skill_obj.skill_config['sort'] == 1 and \
    #                         skill_obj.skill_config['value'] == coll_id:
    #             return max(min(10 + skill_obj.lv - hero_level, 10), 0)
    #
    #     return 0
    #
    # def trigger_hobby(self):
    #     """ 采集物爱好者, 当自动采集时，指定采集物权重增加
    #
    #     :param coll_id: 采集物id
    #     :return:
    #     """
    #     hobby = {}
    #     for skill_pos, skill_obj in self.extra_skills.iteritems():
    #         if skill_obj.skill_config['sort'] == 2:
    #             hobby[skill_obj.skill_config['type']] = skill_obj.lv
    #
    #     return hobby
    #
    # def trigger_coll_exp(self, hero_level, exp):
    #     """ 学习高手：获得经验速度增加，增加比例为（100+技能等级-玩家等级）/100
    #
    #     :param hero_level: 英雄等级
    #     :param exp: 每分钟获取经验
    #     :return:
    #     """
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 3 and skill_obj.skill_config['sort'] == 3:
    #             return (1 + max((100 + skill_obj.lv - hero_level) / 100.0, 0)) * exp
    #
    #     return exp
    #
    # def trigger_manu_hero_skill_level(self, manu_sort, hero_level):
    #     """ 武器/防护/后勤专精 提升相应等级
    #
    #     :param manu_sort: 生产类型 1: 武器 2: 防护 3: 后勤
    #     :param hero_level: 英雄等级
    #     :return:
    #     """
    #     mapping = {1: 102, 2: 202, 3: 302}
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 5 and skill_obj.skill_config['sort'] == mapping[manu_sort]:
    #             return max(min(10 + skill_obj.lv - hero_level, 10), 0)
    #
    #     return 0
    #
    # def trigger_manu_luck_value(self, manu_sort):
    #     """ 提升武器/防护/后勤幸运值
    #
    #     :param manu_sort: 采集类型 1: 武器 2: 防护 3: 后勤
    #     :return:
    #     """
    #     mapping = {1: 103, 2: 203, 3: 303}
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 5 and skill_obj.skill_config['sort'] == mapping[manu_sort]:
    #             return skill_obj.get_skill_effect()
    #
    #     return 0
    #
    # def trigger_manu_power(self, manu_sort, manu_lv):
    #     """ 武器/防护/后勤高手, 增幅相应能力
    #
    #     :param manu_sort: 生产类型 1: 武器 2: 防护 3: 后勤
    #     :param manu_lv: 生产物等阶
    #     :return:
    #     """
    #     mapping = {1: 101, 2: 201, 3: 301}
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 5 and skill_obj.skill_config['sort'] == mapping[manu_sort]:
    #             return max(min(skill_obj.lv - (manu_lv - 1) * 10, 10), 0)
    #
    #     return 0
    #
    # def trigger_manu_expert(self, skill_sort, hero_level):
    #     """ 生产指定位置生产物时，生产能力上升
    #
    #     :param skill_sort: 指定生产位置
    #     :param hero_level:
    #     :return:
    #     """
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 5 and skill_obj.skill_config['sort'] == 1 and \
    #                         skill_obj.skill_config['value'] == skill_sort:
    #             return max(min(10 + skill_obj.lv - hero_level, 10), 0)
    #
    #     return 0
    #
    # def trigger_manu_exp(self, hero_level, exp):
    #     """ 学习高手：获得经验速度增加，增加比例为（100+技能等级-玩家等级）/100
    #
    #     :param hero_level: 英雄等级
    #     :param exp: 每分钟获取经验
    #     :return:
    #     """
    #     for skill_pos, skill_obj in self.skills.iteritems():
    #         if skill_obj.sort == 5 and skill_obj.skill_config['sort'] == 3:
    #             return (1 + max((100 + skill_obj.lv - hero_level) / 100.0, 0)) * exp
    #
    #     return exp
