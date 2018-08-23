#! --*-- coding: utf-8 --*--

__author__ = 'sm'


from lib.core.environ import ModelManager


class TaskEventBase(object):
    """

    """
    LEVEL_SORT = 1                      # 战队等级数
    PRIVATE_CITY_SORT = 2               # 通关关卡id
    HERO_SORT = 3                       # 拥有卡牌数
    HERO_EVO_SORT = 4                   # 卡牌X品级数
    HERO_STAR_SORT = 5                  # 卡牌X星级数
    HERO_LEVEL_SORT = 6                 # 卡牌X等级数
    EQUIP_SORT = 7                      # 装备数----
    EQUIP_QUALITY_SORT = 8              # 装备X品级数----
    EQUIP_STRENGTHEN_SORT = 9           # 进行装备强化次数----
    EQUIP_EVO_SORT = 10                 # 装备X强化等级数----
    MAKE_COLLECTION_SORT = 11           # 进行采集X类型数----
    MAKE_MANUFACTURE_SORT = 12          # 进行生产X类型数----
    MAKE_GACHA_SORT = 13                # 进行进行抽卡数
    GACHA_TOTAL_SORT = 14               # 累积抽卡数
    FRIEND_SORT = 15                    # 好友数
    SILVER_SORT = 16                    # 累积金钱数
    DUNGEON_ID_SORT = 17                # 通关指定地城id----
    # DUNGEON_CHAPTER_SORT = 18           # 通关指定章节地城数量
    # DUNGEON_EXPLORER_SORT = 19          # 探索指定章节地城数量
    HERO_AWAKEN_SORT = 18               # 英雄觉醒个数
    MAKE_DAILY_FIGHT_SORT = 19          # 进行日常副本次数
    MAKE_BATTLE_DUNGEON_NUM = 20        # 进行攻打X地城次数
    MAKE_BATTLE_PRIVATE_CITY_NUM = 21   # 进行攻打X副本次数
    MAKE_HERO_EVO_NUM = 22              # 进行进阶X英雄次数
    MAKE_SHOP_BUY_NUM = 23              # 进行商城购买次数
    MAKE_ARENA_BATTLE_NUM = 24          # 进行黑街竞技场次数
    MAKE_HUNT_NUM = 25                  # 进行末日狩猎次数

    HERO_LVLUP = 26                     # 英雄升级次数
    MAKE_AWAKEN_CHAPTER = 27            # 进行觉醒副本次数
    MAKE_TEAM_SKILL_CHAPTER = 28        # 进行战队技能副本次数
    MAKE_RALLY_CHAPTER = 29             # 进行血尘拉力赛次数
    BOX_GACHA = 30                      # 觉醒宝箱抽取次数
    PRISON_TORTURE = 31                 # 拷问boss
    MAKE_BUY_ACTION_POINT = 32          # 进行购买体力次数

    HERO_GRADE_SORT = 33                # 英雄x档次数
    HERO_EXPLORATION = 34               # 探索挂机时长(min)----

    GUILD_DONATE = 35  # 公会捐献
    DAILY_TASK_SCORE = 36  # 每日活跃度
    GUILD_BOSS = 37  # 攻打公会副本
    HIGH_LADDER = 38  # 巅峰竞技
    EQUIP_UPGRADE = 39  # 装备升级
    EQUIP_EVO = 40  # 装备进阶
    CLONE = 42  # 克隆人之战
    BIOGRAPHY = 43  # 传记副本,修改为历史次数
    PRESENT_FLOWER = 44  # 予人玫瑰
    CONSUME_DIAMOND = 46  # 消耗钻石0:进行，1：历史累积
    USE_ACTION_POINT = 47  # 消耗体力
    COMBAT = 48  # 总战力
    MAKE_CHARGE = 49  # 充值xx元
    TOTAL_CHARGE = 50  # 累积充值xx元

    GENE_LV_NUM = 51    # 基因xx等级数
    GENE_EVO_NUM = 52   # 基因xx品阶数
    GENE_STAR_NUM = 53  # 基因xx星级数
    HIGH_LADDER_RANK = 54   # 巅峰竞技场名次
    RALLY_MAX_LAYER = 55    # 血沉最高层数
    HAS_GUILD = 56          # 加入公会
    GUILD_TEXAS_HOLDEM = 57 # 历史玩公会德州次数
    PRISON_WHIP = 58    # 监狱鞭挞xxboss次数
    EQUIP_LV_NUM = 59   # 装备xx级数量
    EQUIP_STAR = 60     # 装备通过升星达到xx星的数量
    EQUIP_STAR_NUM = 61 # 装备xx星数量
    EQUIP_FROM_BOX_GACHA = 62   # 通过补给获得 星级/颜色 装备数量
    EQUIP_FROM_DOOMS = 63   # 通过猛兽获得 星级/颜色 装备数量
    MULT_PRIVATE_CITY = 64  # 完成多个关卡
    COLLECT_ITEM = 65   # 收集xx道具数量
    TALK_TO_NPC = 66    # 和npc谈话
    SUMMON_HERO = 67    # 通过灵魂石合成英雄
    CONSUME_SILVER = 68  # 消耗金币数量,0:进行，1：历史累积
    BUY_SILVER_TIMES = 69  # 点金次数
    TEAM_SKILL_UPGRADE = 70  # 升级战队技能xx技能xx次    历史
    HAS_TEAM_SKILL_NUM = 71  # 拥有xx个战队技能++
    HIS_DECISIVE_NUM = 72  # 参加大对决次数   历史
    HIS_PVE_RAID_NUM = 73  # 参加冒险远征次数  历史
    HIS_KING_WAR_NUM = 74  # 参加王者争霸次数  历史
    HIS_EQUIP_REFINE = 75  # 进行装备洗练次数  历史
    MAKE_CHAPTER_STAGE_NUM = 76  # 攻打或扫荡指定副本次数，xx副本次数, degree=1
    MAKE_CHAPTER_NUM = 77  # 攻打指定普通章节次数，xx章次数
    MAKE_HERO_OPERATE_NUM = 78  # 特殊类型，属于历史数据，英雄强化次数，1：进阶，2：升星，3：觉醒,4：重生，5:升级 次数

    HIS_GUILD_BOSS = 79     # 历史攻打公会副本
    HIS_HIGH_LADDER = 80  # 竞技场历史次数
    HIS_DOOMSDAY_HUNT = 81  # 猛兽历史次数
    HIS_AWAKEND_CHAPTER = 82  # 觉醒副本历史次数
    HIS_CLONE = 83  # 克隆人历史次数
    HIS_DARK_STREET = 84  # 黑街历史次数

    MAKE_GUILD_TEXAS_HOLDEM = 85  # 进行玩公会德州次数
    MAKE_HARD_CHAPTER_NUM = 86  # 攻打指定精英章节次数，xx章次数 degree=2
    MAKE_CRAZY_CHAPTER_NUM = 87  # 攻打指定困难章节次数，xx章次数 degree=3

    TEAMS_CHAPTER_HARD = 88     # 通关游骑兵突袭指定难度
    PVE_RAID_PASS = 89          # 通关冒险与远征指定关卡
    PRISON_ARTIFACT = 90        # 监狱神器总等级
    RESOLVE_GENE = 91           # 分解装备（历史）数量
    SHOP_REFRESH = 92           # 商城刷新次数
    GENE_FOR_COLOR = 93         # 拥有装备（颜色）数量
    RALLY_HIS_STAGE = 94        # 血沉历史里程数

    VIP_LEVEL = 95  # vip达到x级
    HIS_SIGN_DAYS = 96  # 累积签到天数
    HIS_HUNT_CLEAR_MAP_NUM = 97  # 累积猛兽清空地图x次
    HIS_TEAMS_CHAPTER = 98  # 游骑兵突袭累积次数
    HIS_RALLY_MAP_DONE = 99  # 累积血沉完成一张地图次数

    LOGIN_SORT = 100                    # 登录任务sort, 用于每日登录触发

    HIS_WORMHOLE = 101  # 累积参加金字塔次数
    WORMHOLE_LAYER = 102  # 达到金字塔x层
    HIS_WORMHOLE_DIG = 103  # 累积挖掘金字塔宝藏次数(幸运位置)
    PASS_BIOGRAPHY = 104  # 通关传记第几关
    HIS_SHOP_BUY = 105  # 累积商城购买
    HIS_USE_ACTION_POINT = 107  # 累积消耗体力

    HIS_BUY_ACTION_POINT = 108  # 累积购买体力次数
    HIS_PRISON_WHIP = 109       # 累积鞭挞boss次数
    HIS_BUY_SILVER_TIMES = 110  # 累积点金次数
    HIS_STAR_ARRAY_POINT_TIMES = 111  # 累积星座占星次数
    HIS_TECH_TREE_TIMES = 112   # 累积科技树点亮点数
    HIS_ADVANCE_TIMES = 113     # 累积通关徽章副本次数
    HIS_GUILD_DONATE = 114      # 公会历史捐献

    EQUIP_WEAR_EVO_NUM = 118  # 穿戴xx品质装备数量
    ROLE_GENE_LV_NUM = 121  # 指挥官勋章xx等级数量
    TEAM_SKILL_MASTER_LV = 122  # 基地支援xx级
    TEAM_SKILL_ONE_LV = 123  # 基地支援xx技能xx级
    HIS_ENDLESS_LAYER = 124  # 无尽远征xx层
    HIS_CHAPTER_STAGE_NUM = 125  # 攻打或扫荡指定副本次数，xx副本次数, degree=1
    HIS_EQUIP_UPGRADE = 126     # 历史基因升多少级

    HIS_RALLY_CHAPTER = 127  # 累积血尘拉力赛次数

    def hero_set_gene(self, *args, **kwargs):
        """
        穿戴装备
        :return:
        """
        pass

    def role_gene_lvl(self, *args, **kwargs):
        """
        指挥官勋章升级
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def up_skill_mastery(self, *args, **kwargs):
        """
        基地支援升级
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def endless_layer(self, *args, **kwargs):
        """
        无尽远征历史达到最高层
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def star_array_add_point(self, *args, **kwargs):
        """星座占星"""
        pass

    def tech_tree_add_point(self, *args, **kwargs):
        """科技树点亮点数"""
        pass

    def daily_advance_pass(self, *args, **kwargs):
        """通关徽章副本"""
        pass

    def wormhole_max_layer(self, *args, **kwargs):
        """达到金字塔x层"""
        pass

    def wormhole_battle(self, *args, **kwargs):
        """累积参加金字塔次数"""
        pass

    def wormhole_luck(self, *args, **kwargs):
        """累积挖掘金字塔宝藏次数(幸运位置)"""
        pass

    def free_sign(self, *args, **kwargs):
        """累积签到天数"""
        pass

    def hunt_clear_map(self, *args, **kwargs):
        """累积猛兽清空地图x次"""
        pass

    def pass_pve_raid(self, *args, **kwargs):
        """通关冒险远征"""
        pass

    def shop_refresh(self, *args, **kwargs):
        """商店刷新"""
        pass

    def artifact_lvlup(self, *args, **kwargs):
        """监狱神器升级"""
        pass

    def resolve_gene(self, *args, **kwargs):
        """分解装备"""
        pass

    def make_hero_operate_num(self, *args, **kwargs):
        """英雄强化次数，1：进阶，2：升星，3：觉醒,4：重生，次数"""
        pass

    def team_skill_upgrade(self, *args, **kwargs):
        """升级战队技能xx技能xx次"""
        pass

    def make_decisive_num(self, *args, **kwargs):
        """参加大对决次数"""
        pass

    def make_pve_raid_num(self, *args, **kwargs):
        """参加冒险远征次数"""
        pass

    def make_king_war_num(self, *args, **kwargs):
        """参加王者争霸次数"""
        pass

    def make_equip_refine(self, *args, **kwargs):
        """进行装备洗练次数"""
        pass

    def hero_lvlup(self, *args, **kwargs):
        """
        英雄升级次数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def task_consume_silver(self, *args, **kwargs):
        """
        消耗金币
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def buy_silver_times(self, *args, **kwargs):
        """
        点金次数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def talk_to_npc(self, *args, **kwargs):
        """
        和npc谈话
        :return:
        """
        pass

    def summon_hero(self, *args, **kwargs):
        """
        通过灵魂石合成英雄
        :return:
        """
        pass

    def collect_item(self, *args, **kwargs):
        """
        收集xx道具数量
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def texas_start(self, *args, **kwargs):
        """
        德州次数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def join_guild(self, *args, **kwargs):
        """
        加入公会
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def buy_action_point(self, *args, **kwargs):
        """
        购买体力次数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def daily_login(self, *args, **kwargs):
        """
        每日登录
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def make_daily_fight(self, sort, *args, **kwargs):
        """
        进行日常副本
        :param sort: 0: 任意, 1:银币副本, 2: 经验副本, 3: 进阶副本, 4: 觉醒副本
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def make_doomsday_hunt(self, *args, **kwargs):
        """
        进行末日狩猎
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def hero_awaken(self, *args, **kwargs):
        """
        英雄觉醒
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def level_upgrade(self, level, *args, **kwargs):
        """
        战队升级
        :param level: 战队当前等级
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def vip_level_upgrade(self, vip_level, *args, **kwargs):
        """
        vip升级
        :param vip_level: vip当前等级
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def pass_private_city(self, stage_team, stage_id, *args, **kwargs):
        """
        攻打关卡
        :param stage_team: 大关卡id
        :param stage_id: 当前通关关卡id
        :param args:
        :param kwargs: win=True or False
        :return:
        """
        pass

    def hero_num(self, hero_num, *args, **kwargs):
        """
        增加卡牌
        :param hero_num: 当前英雄数量
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def gwentcard_num(self, gcard_num, *args, **kwargs):
        """
        增加昆特牌
        :param gcard_num: 当前昆特牌数量
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def hero_evo_upgrade(self, hero_id, old_evo, new_evo, *args, **kwargs):
        """
        卡牌进阶
        :param hero_id: 进阶的英雄id
        :param old_evo: 进阶前evo
        :param new_evo: 进阶后evo
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def hero_star_upgrade(self, old_star, new_star, *args, **kwargs):
        """
        卡牌星级
        :param old_star: 升星前star
        :param new_star: 升星后star
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def hero_level_upgrade(self, old_level, new_level, *args, **kwargs):
        """
        卡牌升级
        :param old_level: 英雄升级前level
        :param new_level: 英雄升级后level
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_num(self, equip_num, *args, **kwargs):
        """
        装备数
        :param equip_num: 当前装备数量
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_quality_upgrade(self, quality, flag, *args, **kwargs):
        """
        基因进阶
        :param quality: 装备当前quality
        :param flag: 0: 删除装备, 1: 添加装备
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_strengthen_upgrade(self, *args, **kwargs):
        """
        进行装备强化
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_evo_upgrade(self, old_evo, new_evo, flag, *args, **kwargs):
        """
        基因升级
        :param old_evo:
        :param new_evo: 装备强化evo
        :param flag: 0: 删除装备, 1: 获得装备或装备强化
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_star(self, *args, **kwargs):
        """
        基因升星
        :return:
        """
        pass

    def equip_star_up(self, *args, **kwargs):
        """
        装备升星
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def make_collection(self, sort, *args, **kwargs):
        """
        采集
        :param sort: 采集类型, 0: 任意, 1: 矿, 2: 木, 3: 皮
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def make_manufacture(self, sort, *args, **kwargs):
        """
        生产
        :param sort: 生产类型, 0: 任意, 1:武器, 2: 头盔, 3: 衣服, 4: 鞋子, 5: 饰品, 6: 道具, 7: 战斗道具
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def gacha(self, sort, *args, **kwargs):
        """
        抽卡
        :param sort: 抽卡类型, 0: 任意, 1: 银币单抽, 2: 银币十连, 3: 钻石单抽, 4: 钻石十连
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def friend_num(self, num, *args, **kwargs):
        """
        好友数
        :param num: 当前好友数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def get_silver(self, *args, **kwargs):
        """
        金钱数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def pass_dungeon(self, chapter_id, dungeon_team, dungeon_id, *args, **kwargs):
        """
        攻打地城
        :param chapter_id: 当前章节
        :param dungeon_team: 大关卡id
        :param dungeon_id: 当前通关地城id
        :param args:
        :param kwargs: win=True or False
        :return:
        """
        pass

    def explore_dungeon(self, *args, **kwargs):
        """
        探索出地城
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def shop_buy(self, shop_id, *args, **kwargs):
        """
        商城购买
        :param shop_id:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def arena_battle(self, *args, **kwargs):
        """
        挑战竞技场
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def rally_battle(self, *args, **kwargs):
        """
        参加血尘拉力赛
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def awaken_chapter(self, *args, **kwargs):
        """
        参加觉醒副本
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def make_exploration(self, *args, **kwargs):
        """
        探索, 挂机
        :param args:
        :param kwargs:
        :return:
        """
        pass

    # def commander_rob(self, *args, **kwargs):
    #     """
    #     参与抢夺次数
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     pass

    def team_skill_chapter(self, *args, **kwargs):
        """
        攻打战队技能副本
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def guild_donate(self, *args, **kwargs):
        """
        公会捐献
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def daily_task_score(self, *args, **kwargs):
        """
        每日活跃度
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def guild_boss_battle(self, *args, **kwargs):
        """
        攻打公会副本
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def high_ladder(self, *args, **kwargs):
        """
        巅峰竞技
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_upgrade(self, *args, **kwargs):
        """
        基因升级
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_lvl_up(self, *args, **kwargs):
        """
        装备升级
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def equip_evo(self, *args, **kwargs):
        """
        装备进阶
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def clone_battle(self, *args, **kwargs):
        """
        克隆人之战
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def biography_battle(self, *args, **kwargs):
        """
        传记副本
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def box_gacha(self, *args, **kwargs):
        """
        觉醒宝箱次数
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def prison_torture(self, kind, *args, **kwargs):
        """
        拷问boss次数
        :param kind: 0任意，1：鞭打，2：诱惑
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def present_flower(self, *args, **kwargs):
        """
        予人玫瑰
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def task_consume_diamond(self, count, *args, **kwargs):
        """
        一本万利（消耗钻石）
        :param count: 数量
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def use_action_point(self, point, *args, **kwargs):
        """
        消耗体力
        :param point:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def max_combat(self, combat, *args, **kwargs):
        """
        总战力
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def charge_price(self, price, *args, **kwargs):
        """
        充值
        :param price:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def send_red_bag(self, *args, **kwargs):
        """
        天降红包
        :param args:
        :param kwargs:
        :return:
        """
        pass


class TaskEventDispatch(object):

    _models = []

    def __init__(self, *args, **kwargs):
        self.mm = None

    @classmethod
    def register_model(self, model_name, model_class):
        """

        :param model_name: 必须是mm中的属性
        :return:
        """
        if model_name not in self._models:
            self._models.append((model_name, model_class))

    def call_method(self, method_name, *args, **kwargs):
        """

        :param method_name:
        :return:
        """
        for model_name, model_class in self._models:
            if method_name not in model_class.__dict__:
                continue

            model = getattr(self.mm, model_name, None)
            if not model:
                model = model_class(self.mm)

            # 检查是否可以执行method_name
            check_execute_func = getattr(model_class, 'check_execute', None)
            if check_execute_func and not check_execute_func(self.mm):
                continue

            method = getattr(model, method_name, None)
            # print_log('self._models, model, method', self._models, model, method)
            if method:
                method(*args, **kwargs)


ModelManager.register_events('task_event_dispatch', TaskEventDispatch)
