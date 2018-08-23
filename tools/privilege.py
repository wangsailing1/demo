#! --*-- coding: utf-8 --*--

__author__ = 'sm'


import time

from lib.core.environ import ModelManager
from gconfig import game_config

EXP_POT_LIMIT = 1                   # 经验存储上限增量
USER_EXP = 2                        # 增加挂机获得经验(战队)
CHALLENGE_NUM_LIMIT = 3             # 挑战副本次数上限增量
BATTLE_NUM_RECOVERY_TIME = 4        # 战斗次数回复提速增量
ADD_PRIVATE_CITY_SILVER = 5         # 增加挑战关卡获得银币的数量
ADD_PRIVATE_CITY_HERO_EXP = 6       # 增加挑战关卡获得经验(英雄)
ADD_EXPLORATION_SILVER = 7          # 增加挂机获得银币的数量
# ADD_EXPLORATION_HERO_EXP = 8        # 增加挂机获得经验的数量(英雄)
# COLL_POS = 9                        # 增加采集位置
# ADD_COLL_HERO_EXP = 10              # 增加采集挂机采集人员获得的经验增量
# MANU_POS = 11                       # 增加生产位置
# INCREASE_MANU_RATE = 12             # 提高生产效率
# INCREASE_MANU_HERO_EXP = 13         # 增加生产人员生产获得的经验
ARENA_RECOVERY_TIME = 14            # 竞技场次数回复提速
MARKET_NUM = 15                     # 增加拍卖行所挂物品件数
MARKET_RATE = 16                    # 减少拍卖行收税百分比
MARKET_BOOTH_FEE = 17               # 减少拍卖行摊位费百分比
# TEAM_POS = 18                       # 预设位置全部开启（默认为3，最高为6）
# COLL_PACKAGE_LIMIT = 19             # 采集背包上限
COLL_QUEUE_LIMIT = 20               # 采集队列上限
MANU_QUEUE_LIMIT = 21               # 生产队列上限
# NIGHTMARES_ROUND = 22               # 无尽梦靥上限战斗波数为20
# DAILY_BOSS_TIMES = 23               # 战争工厂攻打次数+3


class Privilege(object):
    """ 特权

    """

    def __init__(self, mm):
        self.mm = mm
        self.vip_config = game_config.vip.get(self.mm.user.vip, {})
        # self.update()

    def __del__(self):
        self.mm = None

    def update(self):
        """ 更新特权

        :return:
        """
        now = int(time.time())
        if not self.mm.user.privileges:
            return None
        diff_time = now - self.mm.user.update_privilege
        self.mm.user.update_privilege = now
        keys = self.mm.user.privileges.keys()
        keys.sort()     # 需要先执行"经验存储上限增量"在执行"增加挂机获得经验(战队)"
        for sort in keys:
            sort_diff_time = diff_time
            privileges = self.mm.user.privileges[sort]
            remove_privilege = []
            for privilege in privileges:
                if sort_diff_time <= 0:
                    break
                rtime = privilege['rtime']
                pri_diff_time = rtime - sort_diff_time  # 时间为负数时间已过期,是否为正未过期
                if pri_diff_time <= 0:
                    sort_diff_time -= rtime             # 去掉当前特权后还有多长时间
                    remove_privilege.append(privilege)
                else:
                    privilege['rtime'] = pri_diff_time
                    break

            if remove_privilege:
                for p in remove_privilege:
                    self.mm.user.privileges[sort].remove(p)
                if not self.mm.user.privileges[sort]:
                    del self.mm.user.privileges[sort]

        if not self.mm.user.privileges:
            self.mm.user.update_privilege = 0

    def exp_pot_uplimit(self):
        """ 获取经验存储上限

        :return:
        """
        gifts = self.mm.user.privileges.get(EXP_POT_LIMIT)
        if gifts:
            return self.mm.user.DEFAULT_MAX_EXP_POT + gifts[0]['value']
        else:
            return self.mm.user.DEFAULT_MAX_EXP_POT

    def every_miu_exp_pot(self):
        """ 获取每分钟经验

        :return:
        """
        gifts = self.mm.user.privileges.get(USER_EXP)
        explorer_hero_num = self.mm.private_city.explorer_hero_num()
        if not explorer_hero_num:
            return 0

        if gifts:
            return min(20, explorer_hero_num) * 0.6 * (1 + gifts[0]['value'] * 0.01)
        else:
            return min(20, explorer_hero_num) * 0.6

    def challenge_num_limit(self, max_point):
        """ 调整副本次数限制

        :return:
        """
        gifts = self.mm.user.privileges.get(CHALLENGE_NUM_LIMIT)
        if gifts:
            return max_point + gifts[0]['value']
        else:
            return max_point

    def battle_num_recovery_time(self, point_refresh_time):
        """ 战斗次数回复提速增量

        :return:
        """
        gifts = self.mm.user.privileges.get(BATTLE_NUM_RECOVERY_TIME)
        if gifts:
            return point_refresh_time * (1 - gifts[0]['value'] * 0.01)
        else:
            return point_refresh_time

    def add_private_city_silver(self, fight_reward):
        """ 增加挑战关卡获得银币的数量

        :param fight_reward:
        :return:
        """
        gifts = self.mm.user.privileges.get(ADD_PRIVATE_CITY_SILVER)
        if gifts:
            result = []
            for reward in fight_reward:
                if reward[0] == 1:
                    result.append([reward[0], reward[1], reward[2] * (1 + gifts[0]['value'] * 0.01)])
                else:
                    result.append(reward)
            return result
        else:
            return fight_reward

    def add_private_city_hero_exp(self, hero_exp):
        """ 增加关卡英雄经验

        :param hero_exp:
        :return:
        """
        gifts = self.mm.user.privileges.get(ADD_PRIVATE_CITY_HERO_EXP)
        if gifts:
            return hero_exp * (1 + gifts[0]['value'] * 0.01)
        else:
            return hero_exp

    def add_exploration_silver(self, fix_reward):
        """ 增加挂机获得银币的数量

        :return:
        """
        gifts = self.mm.user.privileges.get(ADD_EXPLORATION_SILVER)
        if gifts:
            result = []
            for reward in fix_reward:
                if reward[0] == 1:
                    result.append([reward[0], reward[1], reward[2] * (1 + gifts[0]['value'] * 0.01)])
                else:
                    result.append(reward)
            return result
        else:
            return fix_reward

    def arena_recovery_time(self, default_time):
        """ 竞技场次数回复提速

        :param rate:
        :return:
        """
        gifts = self.mm.user.privileges.get(ARENA_RECOVERY_TIME)
        if gifts:
            return default_time * (1 - gifts[0]['value'] * 0.01)
        else:
            return default_time

    def market_num(self):
        """ 增加拍卖行所挂物品件数

        :return:
        """
        gifts = self.mm.user.privileges.get(MARKET_NUM)
        if gifts:
            return gifts[0]['value']
        else:
            return 0

    def market_rate(self, cost):
        """ 减少拍卖行收税百分比

        :return:
        """
        gifts = self.mm.user.privileges.get(MARKET_RATE)
        if gifts:
            return cost * (1 - gifts[0]['value'] * 0.01)
        else:
            return cost

    def market_booth_fee(self, cost):
        """ 减少拍卖行收税百分比

        :return:
        """
        gifts = self.mm.user.privileges.get(MARKET_BOOTH_FEE)
        if gifts:
            return cost * (1 - gifts[0]['value'] * 0.01)
        else:
            return cost

    def coll_queue_limit(self):
        """ 采集队列上限

        :return:
        """
        gifts = self.mm.user.privileges.get(COLL_QUEUE_LIMIT)
        if gifts:
            return gifts[0]['value']
        else:
            return []

    def manu_queue_limit(self):
        """ 生产队列上限

        :return:
        """
        gifts = self.mm.user.privileges.get(MANU_QUEUE_LIMIT)
        if gifts:
            return gifts[0]['value']
        else:
            return []

    def max_point_buy_times(self):
        """
        体力最大购买次数
        :return:
        """
        buy_times = self.vip_config.get('buy_point', 1)
        return buy_times

    def max_slg_point_buy_times(self):
        """
        行动力最大购买次数
        :return:
        """
        buy_times = self.vip_config.get('buy_slgpoint', 1)
        return buy_times

    def get_max_whip_num(self):
        """
        皮鞭恢复上限
        :return:
        """
        max_whip_num = self.vip_config.get('whip_num', 4)
        return max_whip_num

    def get_max_buy_whip_times(self):
        """
        最大购买皮鞭次数
        :return:
        """
        max_whip_buy_num = self.vip_config.get('whip_times', 0)
        return max_whip_buy_num

    def get_max_buy_tempt_times(self):
        """
        最大购买诱惑次数
        :return:
        """
        max_tempt_buy_num = self.vip_config.get('tempt_times', 0)
        return max_tempt_buy_num

    def get_max_reset_dungeon_times(self):
        """
        最大可重置地城次数
        :return:
        """
        max_reset_dungeon = self.vip_config.get('rest_times', 1)
        return max_reset_dungeon

    def get_max_high_ladder_buy_times(self):
        """
        最大竞技场购买次数
        :return:
        """
        max_arena_buy_times = self.vip_config.get('arena_buy_times', 0)
        return max_arena_buy_times

    def get_max_dark_street_buy_times(self):
        """
        最大黑街购买次数
        :return:
        """
        max_dark_buy_times = self.vip_config.get('dark_num', 0)
        return max_dark_buy_times

    def get_max_high_ladder_refresh_def_times(self):
        """
        最大竞技场刷新敌人次数
        :return:
        """
        max_arena_refresh_times = self.vip_config.get('arena_refresh_times', 0)
        return max_arena_refresh_times

    def get_max_biography_select_num(self):
        """
        传记副本每日可选择数
        :return:
        """
        max_biography_num = self.vip_config.get('biography_num', 1)
        return max_biography_num

    def get_max_dark_point(self):
        """
        黑街擂台挑战券上限
        :return:
        """
        max_dark_point = self.vip_config.get('dark_point', 0)
        return max_dark_point

    def get_max_friend_num(self):
        """
        好友数量上限
        :return:
        """
        friend_num = self.vip_config.get('friend_num', 30)
        return friend_num

    def open_sweep10(self):
        """
        是否开启扫荡10次的功能
        :return:
        """
        sweep10_flag = self.vip_config.get('ten_times', 0)
        return 1 if sweep10_flag > 0 else 0

    def get_clone_max_times(self):
        max_battle_times = game_config.vip.get(self.mm.user.vip, {}).get('clone_times', 0)
        return max_battle_times

    def get_rally_sweep_layer(self, rally_id):
        """血沉vip可扫荡层数"""
        rally_km = self.vip_config.get('rally_km', {})
        if not rally_km:
            return 0

        layer = rally_km.get(0, 48)
        lv = rally_km.get(rally_id, 100)
        if self.mm.user.level < lv:
            return 0
        else:
            return layer

    def get_texas_refresh_num(self):
        """
        德州扑克刷新次数限制
        :return:
        """
        change_num = self.vip_config.get('guild_Texas_change_times', 0)
        return change_num

    def get_texas_reset_num(self):
        """
        德州扑克付费换牌次数限制
        :return:
        """
        change_num = self.vip_config.get('guild_Texas_times', 0)
        return change_num

    def get_doomsday_hunt_num(self):
        """
        猛兽通缉令挑战次数限制
        :return:
        """
        hunt_times = self.vip_config.get('hunt_times', 0)
        return hunt_times

    def get_challenge_battle_num(self):
        """
        极限挑战挑战次数限制
        :return:
        """
        battle_times = self.vip_config.get('ulchallenge_times', 0)
        return battle_times

    def get_max_open_box_times(self):
        """最多开宝箱次数"""
        open_times = self.vip_config.get('hunt_box_times', 0)
        return open_times

    def get_team_skill_buy_num(self):
        """
        猛兽通缉令挑战次数限制
        :return:
        """
        buy_times = self.vip_config.get('team_skill', 0)
        return buy_times

    def dragon_buy_times(self):
        """
        巨龙购买挑战次数限制
        :return:
        """
        buy_times = self.vip_config.get('dragon_times', 0)
        return buy_times


ModelManager.register_events('privilege', Privilege)
