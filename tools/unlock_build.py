#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from lib.core.environ import ModelManager
from task_event import TaskEventBase, TaskEventDispatch
from gconfig import game_config

# 解锁建筑物
GACHA_SORT = 1  # 招募处
COLLECTION_SORT = 2  # 采集中心
MANUFACTURE_SORT = 3  # 生产中心
SHOP_SORT = 4  # 商店
MARKET_SORT = 5  # 拍卖行
GUILD_SORT = 6  # 公会
REMAKE_CENTER = 7  # 改造中心
HIGH_LADDER = 8  # 竞技场
AREA_SORT = 76  # 竞技场
EXPLORATION_SORT = 9  # 指挥中心, 章节挂机
TASK_SORT = 10  # 任务版
MAIL_SORT = 11  # 邮箱
EQUIP_PACKAGE = 14  # 英雄背包
FRIEND_SORT = 17  # 好友
GUILD_GUARD_SORT = 18  # 公会护卫
GUILD_FIGHT_SORT = 19  # 公会战
GUILD_CHAPTER_SORT = 20  # 公会副本
GUILD_TECH_SORT = 21  # 公会科技
GUILD_SHOP_SORT = 22  # 公会商店
PRIVATE_CITY_HARD = 23  # 困难关卡
PRIVATE_CITY_CRAZY = 24  # 地狱关卡
PRIVATE_CITY = 25  # 普通关卡 后端不做判断
EXP_POT = 26  # 战队可通过挂机得经验
DAILY_NIGHTMARES_SORT = 27  # 每日玩法-无尽梦靥
DAILY_BOSS_SORT = 28  # 每日玩法-战争工厂
DAILY_RALLY = 29  # 每日玩法-拉力赛(血尘拉力赛)
COLL_QUEUE_2 = 30  # 采集开启第二队列
PERIOD_SHOP = 31  # 开启时空商人最低等级
COLL_POSITION_2 = 32  # 开启采集英雄位2
COLL_POSITION_3 = 33  # 开启采集英雄位3
COLL_POSITION_4 = 34  # 开启采集英雄位4
COLL_POSITION_5 = 35  # 开启采集英雄位5
MANU_QUEUE_2 = 36  # 生产开启第二队列
MANU_POSITION_2 = 37  # 开启生产英雄位2
MANU_POSITION_3 = 38  # 开启生产英雄位3
MANU_POSITION_4 = 39  # 开启生产英雄位4
MANU_POSITION_5 = 40  # 开启生产英雄位5
EQUIP_ST_LVUP = 41  # 装备精炼
EXPLORATION_QUEUE_2 = 42  # 探索第二队列
DAILY_ADVANCE = 43  # 每日玩法-进阶副本
AWAKEN_CHAPTER = 44  # 觉醒副本
DOOMSDAY_HUNT = 45  # 末日狩猎
TEAM_SKILL = 46  # 战队技能
EQUIP_STRENGTHEN_SORT = 47  # 装备强化
EQUIP_REFINE = 48  # 装备洗练
OUTLAND = 49  # 外域
OUTLAND_ESCORT = 50  # 外域押镖
WORLD_BOSS = 51  # 世界boss
OUTLAND_PYRAMID = 52  # 外域金字塔
HERO_AWAKEN = 53  # 英雄觉醒
HERO_MILESTONE = 54  # 英雄里程碑
DARK_STREET = 55  # 黑街擂台
COMMANDER = 56  # 统率
GODLAND = 57  # 神域
GODLAND_AREAN = 58  # 神域竞技场
FRONT_MAP = 59  # 前线推图
GODLAND_ZODIAC = 60  # 12宫
GODLAND_ESCORE = 61  # 神域押镖
POKEDEX = 62  # 图鉴
BATTLE_POS3 = 63  # 解锁3号出战位
BATTLE_POS4 = 64  # 解锁4号出战位
BATTLE_POS5 = 65  # 解锁5号出战位
HERO_EVO = 66  # 英雄进阶
HERO_EQUIP = 67  # 英雄装备
HERO_MAJOR = 68  # 英雄专业
HERO_LVLUP = 69  # 英雄升级
HERO_STORY = 70  # 英雄传记
DAILY_TASK = 71  # 每日任务
Team_Boss = 72  # 预言之战
HERO_CHAIN = 73  # 英雄宿命
AUTO_BATTLE = 74  # 自动战斗（前端用）
PRISON = 75  # 监狱
MERCENARY = 77  # 佣兵营地
DONATE_SHOP = 78  # 荣耀商店
BOX_SHOP = 79  # 觉醒商店
CLONE = 80  # 克隆人
BIOGRAPHY = 81  # 传记
EQUIP_OPEN1 = 83  # 基因开启1,4,5
EQUIP_OPEN2 = 84  # 基因开启6,7
EQUIP_OPEN3 = 85  # 基因开启2
DUEL = 89  # 大对决

GENE_STAR = 86  # 装备升星
GENE_EVO = 87  # 装备进阶
GENE_REFINE = 88  # 装备洗练

GENE_ALL_LVLUP = 90  # 装备全身升级
HOME_TOWN = 91  # 家园
LEAD_TITLE = 93  # 称号
TECH_TREE = 94  # 科技树
LEADDER_ROLE = 95  # 队长详情
LEADDER_POS2 = 96  # 队长详情技能位置2
LEADDER_POS3 = 97  # 队长详情技能位置3

EQUIP_SHOP = 101  # 装备商店
PROFITEER_SHOP = 102  # 军需商店
HONOR_SHOP = 103  # 荣誉商店

ENDLESS = 104  # 无尽远征
SLG_BIG_WORLD = 105  # slg功能


def check_unlock(mm, unlock_type, unlock_limit):
    """ 检查解锁

    :param mm:
    :param unlock_type:
    :param unlock_limit:
    :return: True: 解锁
             False: 未解锁
    """
    if unlock_type == 1:
        # 主角卡等级解锁
        if mm.user.level >= unlock_limit:
            return True
    elif unlock_type == 2:
        # vip等级解锁
        if mm.user.vip >= unlock_limit:
            return True
    elif unlock_type == 3:
        # 公会等级解锁
        if mm.user.guild_id and mm.get_obj_by_id('guild', mm.user.guild_id).lv >= unlock_limit:
            return True
    elif unlock_type == 4:
        # 英雄好感度等级解锁
        pass

    return False


def check_build(mm, build_unlock_id):
    """ 检查建筑

    :param mm:
    :param build_unlock_id:
        建筑功能编号	建筑

        1	        酒馆
        2	        采集中心
        3	        生产中心
        4	        商店
        5	        拍卖行
        6	        好友建筑
        7	        公会
        8	        铁匠铺
        9	        邮箱
        10	        招募处
        11	        公会护卫
        12	        公会任务
        13	        公会贸易
        14	        公会采集
        15	        吧台点酒
        16	        矿场
        17	        伐木场
        18	        狩猎场
        19	        交易所
        23          困难关卡
        24          地狱关卡
    :return:
    """
    building_unlock_config = game_config.building_unlock.get(build_unlock_id)
    if building_unlock_config is None:
        return True

    unlock_type = building_unlock_config['unlock_type']
    unlock_limit = building_unlock_config['unlock_limit']

    return check_unlock(mm, unlock_type, unlock_limit)


unlock_build_type = {
    'LEVEL_SORT': 1,  # 战队等级升级
    'VIP_SORT': 2,  # vip等级升级
    'GUILD_LEVEL_SORT': 3,  # 公会等级升级
    'PRIVATE_CITY_SORT': 5,  # 通关关卡
}


def refresh_unlock_build(mm):
    """
    刷新解锁建筑物
    :param mm:
    :return:
    """
    is_save = False
    for unlock_type in unlock_build_type.values():
        unlock_mapping = game_config.get_building_unlock_mapping(unlock_type)
        for unlock_id, unlock_config in unlock_mapping.iteritems():
            unlock_limit = unlock_config['unlock_lvl']
            if unlock_id not in mm.user.unlock_build:
                if unlock_type == 5:  # 通关关卡
                    stage_id = unlock_limit
                    chapter_id = game_config.get_chapter(stage_id)
                    degree = game_config.get_degree(stage_id)
                    if not mm.private_city.is_first_use_building(chapter_id, stage_id, degree):
                        mm.user.unlock_build.append(unlock_id)
                    is_save = True
                elif check_unlock(mm, unlock_type, unlock_limit):
                    mm.user.unlock_build.append(unlock_id)
                    is_save = True

    if is_save:
        mm.user.save()


class UnlockBuild(TaskEventBase):
    """
    解锁建筑物
    """

    def __init__(self, mm):
        self.mm = mm

    def level_upgrade(self, level, *args, **kwargs):
        """
        战队升级
        :param level: 战队当前等级
        :param args:
        :param kwargs:
        :return:
        """
        unlock_type = unlock_build_type.get('LEVEL_SORT')
        unlock_mapping = game_config.get_building_unlock_mapping(unlock_type)
        for unlock_id, unlock_config in unlock_mapping.iteritems():
            unlock_limit = unlock_config['unlock_lvl']
            guide_team = unlock_config['unlock_guide_team']
            if level >= unlock_limit and unlock_id not in self.mm.user.unlock_build and guide_team in self.mm.user.check_guide_done(
                    guide_team):
                self.mm.user.unlock_build.append(unlock_id)
                self.mm.user.save()

    def vip_level_upgrade(self, vip_level, *args, **kwargs):
        """
        vip升级
        :param vip_level: vip当前等级
        :param args:
        :param kwargs:
        :return:
        """
        unlock_type = unlock_build_type.get('VIP_SORT')
        unlock_mapping = game_config.get_building_unlock_mapping(unlock_type)
        for unlock_id, unlock_config in unlock_mapping.iteritems():
            unlock_limit = unlock_config['unlock_lvl']
            if vip_level >= unlock_limit and unlock_id not in self.mm.user.unlock_build:
                self.mm.user.unlock_build.append(unlock_id)
                self.mm.user.save()

    def guild_level_upgrade(self, guild_level, *args, **kwargs):
        """
        公会升级
        :param guild_level: 公会当前等级
        :param args:
        :param kwargs:
        :return:
        """
        unlock_type = unlock_build_type.get('GUILD_LEVEL_SORT')
        unlock_mapping = game_config.get_building_unlock_mapping(unlock_type)
        for unlock_id, unlock_config in unlock_mapping.iteritems():
            unlock_limit = unlock_config['unlock_lvl']
            if guild_level >= unlock_limit and unlock_id not in self.mm.user.unlock_build:
                self.mm.user.unlock_build.append(unlock_id)
                self.mm.user.save()

    def pass_private_city(self, stage_team, stage_id, *args, **kwargs):
        """
        攻打关卡
        :param stage_team:
        :param stage_id: 当前通关关卡id
        :param args:
        :param kwargs: win=True or False
        :return:
        """
        unlock_type = unlock_build_type.get('PRIVATE_CITY_SORT')
        unlock_mapping = game_config.get_building_unlock_mapping(unlock_type)
        for unlock_id, unlock_config in unlock_mapping.iteritems():
            unlock_limit = unlock_config['unlock_lvl']
            if stage_id == unlock_limit and unlock_id not in self.mm.user.unlock_build:
                self.mm.user.unlock_build.append(unlock_id)
                self.mm.user.save()


TaskEventDispatch.register_model('unlock_build', UnlockBuild)
