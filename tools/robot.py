#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import random

from gconfig import game_config
from lib.utils import weight_choice
from lib.utils import add_dict_list


class Robot(object):

    def __init__(self):
        pass

    def parse_robots(self, robot_id):
        """ 解析robots表

        :param robot_id:
        :return:
        """
        robot_team = []
        robot_heros = {}
        hero_configs = self.get_robot_attribute(robot_id)
        hero_obj = Hero('test')

        for hid, hcfg in hero_configs.iteritems():

            hero_oid, hero_dict = hero_obj.generate_hero(**hcfg)
            hero_dict['max_hp'] = hero_dict['hp']
            robot_team.append(hero_oid)
            robot_heros[hero_oid] = hero_dict

        # tools = robots_config['tools']
        # if tools:
        #     free_item = random.choice(tools)
        #     accord_items = {}
        #     for i in free_item:
        #         item_id = i[1]
        #         for num in xrange(i[2]):
        #             add_dict_list(accord_items, item_id, item_id)
        #     free_items = self.random_free_battle_item(accord_items)
        # else:
        #     free_items = []

        return {'def_team': robot_team, 'def_heros': robot_heros}

    def get_robot_attribute(self, robot_lv):
        """
        根据机器人配置,获取英雄id,等级,阶数,星级
        :param robot_lv:
        :return:
        """
        robot_data = {}
        robots_config = game_config.robots
        if not robots_config:
            return robot_data

        robot_lv = min(max(robots_config), robot_lv)
        robot_config = robots_config.get(robot_lv)
        hero_configs = robot_config['hero']

        for hid, hcfg in hero_configs.iteritems():
            if not hcfg:
                continue
            robot_data[hid] = {
                'hero_id': weight_choice(hcfg)[0],
                'lv': robot_lv,
                'evo': weight_choice(robot_config['evo'])[0],
                'star': weight_choice(robot_config['star'])[0],
            }

        return robot_data

    def get_robot_by_hero_id(self, hero_ids):
        """
        根据英雄id获得数据
        :param hero_ids:
        :return:
        """
        robot_team = []
        robot_heros = {}
        hero_obj = Hero('test')

        hero_configs = {}
        for i, hero_id in enumerate(hero_ids):
            hero_configs[i] = {
                'hero_id': hero_id,
                'lv': 1,
                'evo': 1,
                'star': 1,
            }

        for hid, hcfg in hero_configs.iteritems():
            hero_oid, hero_dict = hero_obj.generate_hero(**hcfg)
            hero_dict['max_hp'] = hero_dict['hp']
            robot_team.append(hero_oid)
            robot_heros[hero_oid] = hero_dict

        return robot_team, robot_heros

    def random_free_battle_item(self, accord_items):
        """ 随机免费战斗道具

        :param accord_items: {sort: [item_id, item_id]}
        :return:
        """
        # 进行随机道具
        own_items = []
        accord_items_keys = accord_items.keys()
        sec_random_items = []
        for i in xrange(5):
            if not accord_items_keys:
                break
            key = random.choice(accord_items_keys)
            accord_items_keys.remove(key)
            own_item = random.choice(accord_items[key])
            own_items.append(own_item)
            accord_items[key].remove(own_item)
            if accord_items[key]:
                sec_random_items.extend([(i, 50) for i in accord_items[key]])
            del accord_items[key]

        own_random_items = [(i, 100) for k, v in accord_items.iteritems() for i in v]
        random_items = own_random_items + sec_random_items
        for i in xrange(5):
            if not random_items:
                break
            item = weight_choice(random_items)
            own_items.append(item[0])
            random_items.remove(item)

        # 随机
        if random_items:
            shuffle_items = [i[0] for i in random_items]
            random.shuffle(shuffle_items)
            own_items.extend(shuffle_items)

        if own_items:
            own_items.reverse()

        return own_items


def generate_enemy_data(enemy_id, enemy_config):
    """
    构造一个enemy数据
    :param enemy_id:
    :param enemy_config:
    :return:
    """
    cfg = enemy_config.get(enemy_id)
    if not cfg:
        return {}

    enemyData = {
        'id': enemy_id,
        'lv': cfg.get('lv', 1),
        'star': cfg.get('star', 1),
        'evo': cfg.get('evo', 1),
        'hp': cfg['hp'],
        'phy_atk': cfg['phy_atk'],
        'phy_def': cfg['phy_def'],
        'mag_atk': cfg['mag_atk'],
        'mag_def': cfg['mag_def'],
        'speed': cfg['speed'],
        'crit_chance': cfg['crit_chance'],
        'crit_atk': cfg['crit_atk'],
        'hit': cfg['hit'],
        'resistance': cfg['resistance'],
    }

    # 构造技能
    skills = cfg['skill']
    enemyData['skill'] = {}
    for index, skillId in skills.iteritems():
        enemyData['skill'][index] = {
            'lv': 1,
            'avail': 1,
            's': skillId,
        }

    return enemyData


def generate_enemy_data1(enemy_id, enemy_config, lv=None, skill_lv_max=False, new_equip=False, equip_star=0):
    """
    构造一个enemy数据,等级成长
    :param enemy_id:
    :param enemy_config:
    :param lv:
    :return:
    """
    cfg = enemy_config.get(enemy_id)
    if not cfg:
        return {}

    enemyData = {
        'id': enemy_id,
        'lv': lv or cfg.get('lv', 1),
        'star': cfg.get('star', 1),
        'evo': cfg.get('evo', 1),
        'hp': cfg['hp'],
        'phy_atk': cfg['phy_atk'],
        'phy_def': cfg['phy_def'],
        'mag_atk': cfg['mag_atk'],
        'mag_def': cfg['mag_def'],
        'speed': cfg['speed'],
        'crit_chance': cfg['crit_chance'],
        'crit_atk': cfg['crit_atk'],
        'hit': cfg['hit'],
        'resistance': cfg['resistance'],
    }

    # 等级成长系数
    lvCfg = game_config.hero_growth_rate[enemyData['lv']]
    lv_rate = lvCfg['enemy']
    attrs_key = {'hp', 'phy_atk', 'phy_def', 'mag_atk', 'mag_def'}
    for v in attrs_key:
        base = cfg[v]
        enemyData[v] = base * lv_rate

    # 构造技能
    skills = cfg['skill']
    enemyData['skill'] = {}
    for index, skillId in skills.iteritems():
        if skill_lv_max:
            lv, s = get_max_skill(skillId)
        else:
            lv = 1
            s = skillId
        enemyData['skill'][index] = {
            'lv': lv,
            'avail': 1,
            's': s,
        }

    if new_equip:
        new_equip = Hero.generate_new_equip(enemy_id, equip_evo=equip_star)
        for eid, edict in new_equip.iteritems():
            config = game_config.new_equip_detail.get(eid)
            if not config:
                continue
            Hero.equip_awake_effect(enemyData, edict['awake_lv'], config)

    return enemyData

def get_max_skill(skill_id):
    next_id = skill_id
    for i in xrange(1, 10):
        if skill_id + i in game_config.skill_detail:
            next_id = skill_id + i
            continue
        else:
            break
    return next_id % 10, next_id

