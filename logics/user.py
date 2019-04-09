#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import random
import itertools

from tools.user import user_info
from gconfig import game_config
from tools.gift import add_gift, del_goods, add_mult_gift
from lib.utils.sensitive import is_sensitive
from tools.user import user_rank_info, guild_rank_info
from tools.hero import hero_info
from tools.pay import get_buy_point_need_diamond
from lib.utils.active_inreview_tools import active_inreview_open_and_close
import settings
from lib.utils.time_tools import server_active_inreview_open_and_close
from models import server as serverM
from lib.utils import weight_choice
from tools.hero import format_hero_info
from lib.core.environ import ModelManager
from lib.utils import fake_deepcopy
from models.ranking_list import BlockRank
from logics.mission import Mission
from return_msg_config import i18n_msg


def refresh_roulette_ranktime():
    print '\n\n', 2222222222, '\n\n'


class UserLogic(object):

    PRE_PLAYER_TIME = 60    # 一分钟产x经验

    def __init__(self, mm):
        self.mm = mm
        self.user = self.mm.user

    def main(self):
        result = {}

        # result['daily'] = {
        #     'biography': self.mm.biography.get_rest_times(),
        #     'daily_advance': self.mm.daily_advance.get_all_remainder_times(),
        #     'rally': self.mm.rally.remainder_reset_times(),
        #     'dark_street': self.mm.dark_street.remain_point(),
        #     'doomsday_hunt': self.mm.doomsday_hunt.remain_battle_times(),
        #     'clone': self.mm.clone.remain_battle_times(),
        #     'teams_chapter': self.mm.teams_chapter.get_remain_times(),
        #     'awaken_chapter': self.mm.awaken_chapter.remain_battle_times(),
        #     'high_ladder': self.mm.high_ladder.remain_battle_times(),
        #     'wormhole': self.mm.worm_hole.get_rest_battle_times(),
        # }
        #
        # activity_status = {
        #     'first_charge': self.get_first_charge(),                    # 首充活动标志
        #     'level_limit_gift': self.mm.user.level_gift,                # 限时等级礼包
        #     'sevenday_pop_flag': self.mm.seven_scripture.pop_flag(),    # 七日盛典弹窗标志
        #     'sevenday_flag': not self.mm.seven_scripture.active_is_end(),    # 七日盛典活动标志
        #     'stage_task_flag': self.mm.stage_task.is_open(),            # 前者之路图标
        #     'seven_login_flag': self.mm.seven_login.is_open(),          # 七日登录图标
        #     'growth_fund_flag': self.mm.growth_fund.is_open(),          # 成长基金图标
        # }
        # result['activity_status'] = activity_status
        result.update(self.get_daily_and_activity())

        # 活动开关
        server_num = settings.get_server_num(self.user._server_name)
        result['active_switch'], result['active_remain_time'] = active_inreview_open_and_close(server_num=server_num)
        has_reward = self.mm.foundation.has_reward()
        if not has_reward and not self.mm.foundation.is_open():
            if 2009 in result['active_switch']:
                result['active_switch'].pop(2009)
            if 2009 in result['active_remain_time']:
                result['active_remain_time'].pop(2009)
        # 处理过的新服活动表
        result['server_inreview'], result['server_active_remain_time'] = server_active_inreview_open_and_close(self.mm)

        # ###### 小红点 start ########

        result['alerts'] = self.get_red_dot()

        # ###### 小红点 end ########

        # # 跑马灯数据
        # scroll_bar = self.mm.scroll_bar
        # msg = scroll_bar.get_message()
        # result['scroll_bar'] = msg

        result['play_help'] = self.get_play_help()
        result['blacklist'] = self.user.blacklist
        result['guild_name'] = self.user.name
        result['server_open_time'] = serverM.get_server_config(self.mm.user._server_name)['open_time']
        result['question_done'] = self.user.question_done

        result['script_continued_summary'] = self.mm.script.script_continued_summary()

        # 竞技场第一
        high_ladder_top_one_info = self.get_high_ladder_top_one()
        result.update(high_ladder_top_one_info)

        return result

    def get_daily_and_activity(self):
        result = {}
        result['daily'] = {
        }

        activity_status = {
            'first_charge_open': self.mm.user_payment.get_first_charge(),  # 首充活动标志
            'first_charge_pop': self.mm.user_payment.get_first_charge_pop(),  # 首充弹板
            # 'first_remain_time': self.mm.user_payment.get_first_charge_remain_time(),   # 首充倒计时
            'level_limit_gift': self.mm.user.level_gift,  # 限时等级礼包
            'level_gift_open':self.mm.user.level_gift_red_dot()
        }
        result['activity_status'] = activity_status

        return result

    def talk_npc(self, npc_id, word_id):
        """
        和npc谈话
        :param npc_id:
        :param word_id:
        :return:
        """
        # 和npc谈话任务
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('talk_to_npc', npc_id=npc_id, word_id=word_id)

        result = {}

        # 主城任务
        ml = MissionLogic(self.mm)
        result.update(ml.mission_index())
        result.update(ml.side_index())

        return 0, result

    def get_high_ladder_top_one(self):
        """
        竞技场第一
        :return:
        """

        data = {
            'top_one_user': {
                'name':'',
                'role': 1,
                'lv': 1,
                'hero_id': 1,
                'uid': '',
            },
        }

        return data

    def npc_info(self):
        """
        主城npc信息
        :return:
        """
        num = 5
        online_users = self.mm.get_obj_tools('online_users')
        high_ladder_rank = self.mm.get_obj_tools('high_ladder_rank')
        uids = online_users.get_online_uids_by_num(num)
        npc_info = []

        for uid in uids:
            if uid == self.mm.uid:
                continue
            mm = self.mm.get_mm(uid)
            u_info = user_info(mm)
            if not settings.CN_NAME_PATTERN(u_info['name']):
                name = game_config.get_random_name(self.mm.user.language_sort)
                u_info['name'] = name
            u_info['high_ladder_rank'] = high_ladder_rank.get_rank(self.mm.uid)
            u_info['grade_lv'] = mm.king_war.grade_lv
            u_info['grade_star'] = mm.king_war.grade_star
            npc_info.append(u_info)

        return 0, {
            'npc_info': npc_info,
        }

    def get_red_dot(self, module_name=''):
        """
        获取小红点
        :return:
        """
        red_dot_func = {
            # 红点名: (model模块名, 方法名[可选，默认get_red_dot], 参数[可选])
            # 'task_main': ('task', 'get_task_main_red_dot'),
            # 'task_daily': ('daily_task', 'get_daily_task_red_dot'),
            # 'task_achievement': ('task', 'get_get_achievement_red_dot'),
            'gacha': ('gacha', 'get_gacha_red_dot', ),      #可抽艺人
            # 'hero_summon': ('hero', 'get_hero_summon_red_dot'),
            # 'adventure': ('private_city', 'get_chapter_red_dot'),
            # 'chapter_mile': ('private_city', 'get_chapter_mile_red_dot'),
            # 'explore': ('private_city', 'get_exploaration_red_dot'),
            # 'welfare': ('gift_center', 'get_gift_center_red_dot'),
            # 'sevenday': ('seven_scripture', 'get_sevenday_red_dot'),
            # 'stage_task': ('stage_task', 'get_red_dot'),
            'mail': ('mail', 'get_mail_red_dot'),
            'friend': ('friend', 'get_friend_red_dot'),
            # 'mercenary': ('mercenary', 'get_mercenary_red_dot'),
            # 'active_center': ('active_hot_dot', 'hot_dot'),
            # 'star_reward': ('star_reward', 'alert'),
            # 'server_star_reward': ('server_star_reward', 'alert'),
            # 'prison': ('prison', 'get_red_dot'),
            # 'box_gacha': ('gacha', 'box_gacha_red_dot'),
            # 'daily_advance': ('daily_advance', 'is_alert'),
            # 'biography': ('biography', 'alert'),
            # 'guild': ('guild_hot_dot', 'is_alert_main'),
            # 'home': ('home', 'home_dot'),

            # 'arena': {
            #     'high_ladder': ('high_ladder', ),
            #     'dark_street': ('dark_street', 'is_alert'),
            #     'rally': ('rally', ),
            #     'decisive_battle': ('decisive_battle', 'is_alert'),
            # },
            # 'bounty_hunter': {
            #     'doomsday_hunt': ('doomsday_hunt',),
            #     'clone': ('clone',),
            # },

            # 'high_ladder': ('high_ladder', ),
            # 'dark_street': ('dark_street', 'is_alert'),
            # 'rally': ('rally', ),
            # 'decisive_battle': ('decisive_battle', 'is_alert'),
            #
            # 'doomsday_hunt': ('doomsday_hunt', ),
            # 'clone': ('clone', ),

            'first_charge': ('user_payment', 'first_charge_alert'),
            # 'limit_hero': ('limit_hero', 'is_alert'),
            # 'server_limit_hero': ('server_limit_hero', 'is_alert'),
            # 'team_skill': ('team_skill', 'get_red_dot'),
            # 'welfare_level': ('gift_center', 'get_level_gift_dot'),
            # 'daily_active': ('daily_active', 'alert'),
            'seven_login': ('seven_login', 'get_red_dot'),
            # 'server_celebrate': ('rank_reward_show', 'alert'),  # 开服狂欢小红点
            # 'star_array': ('star_array', 'main_page_dot'),      # 星图小红点
            # 'leading_role': ('role_info', ),                 # 队长红点
            # 'tech_tree': ('tech_tree',),                        # 科技树红点
            # 'growth_fund': ('growth_fund', 'is_alert'),     # 福利基金
            # 'vip_gift': ('user', 'has_vip_gift'),  # 福利基金
            # 'free_sign': ('free_sign', 'is_alert'),     # 普通签到
            # 'pay_sign': ('pay_sign', 'is_alert'),       # 超值签到
            'actor': ('friend', 'get_times'),  # 旅游聊天约会
            'monthly_sign': ('monthly_sign', 'today_can_sign'),  # 签到
            'has_ceremony': ('block', 'ceremony_red_dot'),  # 颁奖典礼
            'script_gacha': ('script_gacha', 'gacha_times_enough'),  # 可抽剧本
            'up_gacha': ('gacha', 'get_can_up_red_hot'),  # 星探升级
            'block_reward': ('block', 'block_reward_red_hot'),  # 世界循环赛奖励
            'book_card': ('card_book', 'get_book_card_red_dot'),  # 艺人组合
            'book_script': ('script_book', 'get_book_script_red_dot'),  # 单个剧本
            'script_group': ('script_book', 'get_script_group_red_dot'),  # 剧本组合
            'continued_script': ('script', 'get_continued_script'),  # 持续收益
            'liveness': ('mission', 'get_liveness_red_dot'),  # 活跃度
            'license_recover_expire': ('user', 'get_license_recover_red_dot'),  # 拍摄许可证倒计时
            'has_new_dialogue': ('chapter_stage', 'get_chapter_red_dot'),  # 新剧情聊天
            'has_actor_dialogue': ('friend', 'get_actor_chat'),  # 有艺人聊天
            'business': ('business', 'get_red_dot'),  # 公司事务
            'company_vip_red_dot': ('user', 'get_company_vip_red_dot'),  # 公司事务
            'performance': ('mission', 'get_performance_red_dot'),  # 业绩目标红点
        }

        # 特殊的几个红点,todo
        # 区分新老服
        # if self.mm.user.config_type == 1:
        #     red_dot_func['soul_box'] = ('server_soul_box', 'get_remain_time')
        #     red_dot_func['roulette'] = ('server_roulette', 'get_red_dot')
        #     red_dot_func['charge_roulette'] = ('server_charge_roulette', 'get_red_dot')
        #     red_dot_func['limit_discount'] = ('server_limit_discount', 'get_red_dot')
        # else:
        #     red_dot_func['soul_box'] = ('soul_box', 'get_remain_time')
        #     red_dot_func['roulette'] = ('roulette', 'get_red_dot')
        #     red_dot_func['limit_discount'] = ('limit_discount', 'get_red_dot')

        if module_name:
            module_list = [module_name]
        else:
            module_list = red_dot_func.keys()

        data = {}
        mm = self.mm
        for m in module_list:
            args = red_dot_func.get(m, ())
            module = getattr(mm, args[0], None) if args else None
            func_name = args[1] if len(args) > 1 and args[1] else 'get_red_dot'
            func = getattr(module, func_name, None)
            params = args[2] if len(args) > 2 and args[2] else {}

            if func:
                red_dot = func(**params)
                # if params:
                #     red_dot = func(**params)
                # else:
                #     red_dot = func()
            else:
                red_dot = False
            # if red_dot is not False:
            data[m] = red_dot

        # 特殊的几个红点,todo
        mission = Mission(mm)
        data['dailymission'] = mission.mission_red_dot()   #每日任务红点
        if mission.mission_red_dot(type = 'guide') or mission.mission_red_dot(type = 'randmission'):
            data['randomemission'] = True  # 随机任务红点
        else:
            data['randomemission'] = False
        if mission.mission_red_dot(type = 'achieve_mission'):
            data['achieve_mission'] = True  # 业绩目标红点
        else:
            data['achieve_mission'] = False

        # 英雄和装备的红点
        if not module_name or module_name in ['hero', 'gene']:
            pass
            # hero, gene = self.mm.hero.get_hero_red_dot()
            # data['hero'] = hero
            # data['gene'] = gene


        return data

    def get_play_help(self):
        """
        机器人提示功能
        :return:
        """
        help_ids = []
        for help_id, _ in game_config.get_play_help_mapping():
            play_help_config = game_config.play_help.get(help_id, {})
            if not play_help_config:
                continue
            sort = play_help_config['sort']
            show_lvl = play_help_config['show_lvl']
            if not show_lvl or not show_lvl[0] <= self.user.level <= show_lvl[1]:
                continue

            # 解锁功能预告
            if sort == 1:
                help_ids.append(help_id)

            # 奖励未领取提示
            elif sort == 2:
                if help_id == 12:       # 星级奖励
                    if self.mm.private_city.get_chapter_red_dot():
                        help_ids.append(help_id)
                elif help_id == 13:     # 主线任务奖励
                    if self.mm.task.get_task_main_red_dot():
                        help_ids.append(help_id)
                elif help_id == 14:     # 每日任务奖励
                    if self.mm.daily_task.get_daily_task_red_dot():
                        help_ids.append(help_id)
                elif help_id == 15:     # 成就奖励
                    if self.mm.task.get_get_achievement_red_dot():
                        help_ids.append(help_id)
                elif help_id == 16:     # 体力领取
                    if self.mm.gift_center.get_welfare_energy_red_dot():
                        help_ids.append(help_id)

            # 副本剩余次数
            elif sort == 3:
                # if help_id == 21:       # 银币副本
                #     if self.mm.daily_boss.remainder_times():
                #         help_ids.append(help_id)
                if help_id == 17:     # 徽章副本
                    if self.mm.daily_advance.get_all_remainder_times():
                        help_ids.append(help_id)
                # elif help_id == 23:     # 经验副本
                #     if self.mm.daily_nightmares.remainder_times():
                #         help_ids.append(help_id)
                elif help_id == 18:     # 战队技能副本
                    if self.mm.teams_chapter.get_remain_times():
                        help_ids.append(help_id)
                # elif help_id == 25:     # 组队boss副本
                #     if self.user.get_team_boss_coin():
                #         help_ids.append(help_id)
                # elif help_id == 26:     # 统帅
                #     if self.mm.commander.energy > 10:
                #         help_ids.append(help_id)
                elif help_id == 19:     # 血尘拉力赛
                    if self.mm.rally.remainder_reset_times():  # 剩余重置次数
                        help_ids.append(help_id)
                elif help_id == 20:     # 末日狩猎
                    if self.mm.doomsday_hunt.remain_battle_times():
                        help_ids.append(help_id)
                elif help_id == 21:  # 黑街擂台
                    if self.mm.dark_street.remain_point():
                        help_ids.append(help_id)
                elif help_id == 22:  # 巅峰竞技
                    if self.mm.high_ladder.remain_battle_times():
                        help_ids.append(help_id)
                elif help_id == 23:  # 公会副本
                    if self.user.guild_id:
                        coin_boss = self.mm.get_obj_by_id('coin_boss', self.user.guild_id)
                        exp_boss = self.mm.get_obj_by_id('exp_boss', self.user.guild_id)
                        if coin_boss.has_remain_times() or exp_boss.has_remain_times():
                            help_ids.append(help_id)

            # 主线任务指引
            elif sort == 4:
                if help_id == 29:       # 主线任务指引
                    if self.mm.task.has_not_done_task():
                        help_ids.append(help_id)

            # 每日任务指引
            elif sort == 5:
                if help_id == 30:       # 每日任务指引
                    if self.mm.daily_task.has_not_done_task():
                        help_ids.append(help_id)

            # 对话
            elif sort == 6:
                help_ids.append(help_id)

        return help_ids

    def guide(self, sort, guide_id, skip):
        """
        新手引导
        :param sort:
        :param guide_id:
        :param skip:
        :return:
        """
        # print sort, guide_id, skip
        flag = self.do_guide(sort, guide_id, skip, save=False)

        data = {'sort': sort, 'guide_id': guide_id}
        # if flag:
        #     guide_config = game_config.guide.get(guide_id)
        #     gift = guide_config.get('mission_reward', [])
        #     if gift and guide_id not in self.user.mission_reward_log:
        #         self.user.mission_reward_log.append(guide_id)
        #         reward = add_mult_gift(self.mm, gift)
        #         data['reward'] = reward
        #
        #     self.user.save()

        return 0, data

    def do_guide(self, sort, guide_id, skip, save=True):
        """ 记录新手引导步骤

        :param sort: 模块分类
        :param guide_id: guide配置id
        :param skip: 是否跳过
        :param save: 是否保存
        :return:
        """
        if skip:
            if not self.user.finish_guide():
                return False
        else:
            if guide_id > self.user.guide.get(sort, 0):
                guide_config = game_config.guide.get(guide_id)
                if guide_config is None:
                    return False

                if sort != guide_config['sort']:
                    return False

                self.user.guide[sort] = guide_id

        if save:
            self.user.save()
        #新手引导解锁建筑
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('level_upgrade', self.user.level)

        return True

    def blacklist(self):
        """
        黑名单首页
        :return:
        """
        users_list = []
        for uid in self.user.blacklist:
            mm = self.mm.get_mm(uid)
            # user_dict = user_info(mm)
            user_dict = {
                'uid': uid,
                'name': mm.user.name,
            }
            users_list.append(user_dict)

        return {
            'users_list': users_list,
            'max_len': self.user.MAX_CHAT_BLACK_LIST,
        }

    def blacklist_add(self, user_id):
        """
        添加黑名单
        :param user_id:
        :return:
        """
        if len(self.user.blacklist) >= self.user.MAX_CHAT_BLACK_LIST:
            return 0, {
                'is_full': 1
            }  # 黑名单人数已经满了, 无法添加

        if user_id in self.user.blacklist:
            return 1, {}  # 已经在屏蔽名单中

        self.user.blacklist.append(user_id)
        self.user.save()

        return 0, self.blacklist()

    def blacklist_delete(self, user_id):
        """
        移除黑黑名单
        :param user_id:
        :return:
        """
        if user_id not in self.user.blacklist:
            return 1, {}  # 您要移除的玩家并不存在

        self.user.blacklist.remove(user_id)
        self.user.save()

        return 0, self.blacklist()

    def player_info(self, user_id, flag):
        """
        获取用户信息
        :param user_id:
        :param flag: 1：巅峰战力榜，2：天梯排行榜，3：关卡星级榜
        :return:
        """
        # user_dict = {}
        mm = self.mm.get_mm(user_id)
        user_dict = user_info(mm)
        user_dict['is_friend'] = self.mm.friend.has_friend(user_id)
        user_dict['is_black'] = user_id in self.user.blacklist
        user_dict['block'] = mm.block.block_num
        user_dict['script_info'] = mm.script.get_scrip_info_by_num()
        user_dict['top_cards'] = mm.card.get_better_card()

        block_rank_uid = mm.block.get_key_profix(mm.block.block_num, mm.block.block_group,
                                                 'income')
        br = BlockRank(block_rank_uid, mm.block._server_name)
        user_dict['block_rank'] = br.get_rank(self.mm.uid)
        user_dict['like'] = self.mm.friend.friends_info.get(user_id,{}).get('like',0)
        # if not self.mm.high_ladder.is_robot(user_id):
        #     mm = self.mm.get_mm(user_id)
        #     user_dict = user_info(mm)
        #     user_dict['is_friend'] = self.mm.friend.has_friend(user_id)
        #     user_dict['is_black'] = user_id in self.user.blacklist
        #
        #     if flag == 1:
        #         info = hero_info(mm.hero, mm.hero.max_combat_heros.keys())
        #     elif flag == 2:
        #         info = hero_info(mm.hero, mm.high_ladder.def_heros)
        #     elif flag == 3:
        #         info = hero_info(mm.hero, mm.hero.max_combat_heros.keys())
        #     else:
        #         info = []
        #
        #     user_dict['team_info'] = info
        # else:
        #     user_dict = self.mm.high_ladder.generate_robot_info(user_id, self.mm)
        #     user_dict['level'] = user_dict['lv']
        #     heros = user_dict.pop('heros', {})
        #
        #     team_info = format_hero_info(heros)
        #     user_dict['team_info'] = team_info

        return {
            'user_info': user_dict,
        }

    def exchange_currency(self, ce_id, num):
        """ 兑换银币

        :param ce_id:
        :param num:
        :return:
        """
        # 玩家主英雄达到40级才可进行兑换
        if self.user.level < self.user.EXCHANGE_LEVEL:
            return 1, {}

        currency_exchange_config = game_config.currency_exchange.get(ce_id)
        if currency_exchange_config is None:
            return 2, {}

        if currency_exchange_config['limit_up'] < num:
            return 3, {}

        exchange_cost = currency_exchange_config['exchange_cost']
        exchange_get = currency_exchange_config['exchange_get']
        proportion = currency_exchange_config['proportion']

        rc, data = del_goods(self.mm, exchange_cost, [[0, num]])
        if rc != 0:
            return rc, {}

        get_num = int(proportion * num)

        reward = add_gift(self.mm, exchange_get, [[0, get_num]])

        self.user.save()

        return 0, {'reward': reward}

    def receive_player_exp(self):
        """
        领取战队经验
        :return:
        """
        exp_pot = self.user.exp_pot
        if not exp_pot:
            return 1, {}    # 没有经验领取

        self.user.receive_exp(save=True)

        return 0, {'exp_pot': self.user.exp_pot}

    def buy_privilege_gift(self, gift_id):
        """ 购买特权礼包

        :param gift_id:
        :return:
        """
        charge_privilege_config = game_config.charge_privilege.get(gift_id)
        if charge_privilege_config is None:
            return 1, {}

        currency = charge_privilege_config['type']
        price = charge_privilege_config['price']

        if currency == 1:  # rmb
            return 2, {}
        elif currency == 2:  # 钻石
            if not self.user.is_diamond_enough(price):
                return 'error_diamond', {}
            self.user.deduct_diamond(price)
        elif currency == 3:  # 金币
            if not self.user.is_coin_enough(price):
                return 'error_coin', {}
            self.user.deduct_coin(price)
        else:
            return 3, {}

        self.user.record_privilege_gift(gift_id=gift_id)

        self.user.save()

        return 0, {'privileges': self.user.privileges}

    def charge_name(self, name):
        """ 改名字

        :param name:
        :return:
        """
        if is_sensitive(name, self.mm.lan):
            return 1, {}
        if name == self.user.name:
            return 2, {}  #名字已使用

        # cost_list = game_config.get_value(15, [200])
        # if self.user.change_name < len(cost_list):
        #     cost = cost_list[self.user.change_name]
        # else:
        #     cost = cost_list[-1]
        cost = game_config.common.get(29, 500)
        if not self.user.is_diamond_enough(cost):
            return 'error_diamond', {}
        if self.user.set_name_unique(name):
            return 5, {}   # 名字存在
        self.user.del_name_unique(self.user.name)

        self.user.name = name
        self.user.change_name += 1
        self.user.deduct_diamond(cost)

        self.user.save()

        return 0, {}

    def register_name(self, name, role):
        """
        起名字
        :param name:
        :return:
        """
        if not name:
            return 3, {}    # 名字不能为空
        if is_sensitive(name, self.mm.lan):
            return 1, {}    # 名字不合法

        if self.user.reg_name:
            return 'error_21', {'custom_msg': i18n_msg.get(1209, self.mm.lan)}    # 已经有名字了
        if not role:
            return 4, {}    # 请选择一个角色
        if self.user.set_name_unique(name):
            return 5, {}   # 名字存在
        self.user.name = name
        self.user.role = role
        self.user.got_icon.append(role)
        # if role not in game_config.main_hero:
        #     return 4, {}    # 角色ID错误
        # self.mm.role_info.init_role(role)
        self.user.reg_name = True
        # todo 初定默认发卡牌，是否根据配置发其他东西再定
        self.new_account_init()
        self.user.save()

        return 0, {}

    def new_account_init(self):
        mp = {1: 13, 2: 15}
        role = self.mm.user.role
        sex = game_config.main_hero[role]['sex']
        cid = mp[sex]
        self.mm.user.add_dollar(50000)
        self.mm.card.add_card(cid)
        self.mm.card.save()

    def buy_point(self):
        """
        购买体力
        :return:
        """
        max_point_buy_times = self.user.get_max_point_buy_times()
        if self.user.buy_point_times >= max_point_buy_times:
            return 1, {}    # 今日已达购买上限

        diamond = get_buy_point_need_diamond(self.mm)

        if not self.user.is_diamond_enough(diamond):
            return 'error_diamond', {}    # 钻石不足

        self.user.deduct_diamond(diamond)
        reward = add_mult_gift(self.mm, [[3, 0, self.user.PUR_BUY_POINT]])
        self.user.add_buy_point_times()

        # self.mm.task_data.add_task_data('other_chapter', 108)
        # 触发购买体力任务
        # task_event_dispatch = self.mm.get_event('task_event_dispatch')
        # task_event_dispatch.call_method('buy_action_point')

        self.user.save()

        return 0, {'reward':reward}

    def opera_awards_index(self):
        """
        剧情奖励index
        :return:
        """
        data = {
            'opera_awards': list(self.user.opera_awards),   # 已领取的奖励id
        }

        return data

    def receive_opera_awards(self, reward_id):
        """
        领取剧情奖励
        :param reward_id:
        :return:
        """
        opera_awards = self.user.get_opera_awards()
        if reward_id in opera_awards:
            return 1, {}    # 已领取

        award = game_config.opera_awards.get(reward_id, {}).get('award', [])
        if not award:
            return 2, {}    # 没有奖励配置

        self.user.add_opera_awards(reward_id)
        reward = add_mult_gift(self.mm, award)

        result = self.opera_awards_index()
        result['reward'] = reward

        return 0, result

    def top_rank(self, page=0, num=10, tp='', only_rank=False):
        """
        最强排行
        :param page:
        :param num:
        :param tp:
        :return:
        """
        if tp == 'combat':
            rank_obj = self.mm.get_obj_tools('combat_rank')
        elif tp == 'endless':
            rank_obj = self.mm.get_obj_tools('endless_rank')
        elif tp == 'level':
            rank_obj = self.mm.get_obj_tools('level_rank')
        elif tp == 'single_hero':
            rank_obj = self.mm.get_obj_tools('top_hero_rank')
        elif tp == 'high_ladder':
            rank_obj = self.mm.get_obj_tools('high_ladder_rank')
        elif tp == 'home_flower':
            rank_obj = self.mm.get_obj_tools('flower_rank')
        elif tp == 'guild_level':
            rank_obj = self.mm.get_obj_tools('guild_level_rank')
        elif tp == 'private_city_star':
            rank_obj = self.mm.get_obj_tools('private_city_star_rank')
        elif tp == 'dark_street':
            rank_obj = self.mm.get_obj_tools('dark_battle_rank')

        elif tp == 'dark_battle_win':
            rank_obj = self.mm.get_obj_tools('dark_battle_win_rank')

        elif tp == 'doomsday_hunt':
            rank_obj = self.mm.get_obj_tools('doomsday_hunt_rank')

        elif tp == 'teams_chapter':
            rank_obj = self.mm.get_obj_tools('teams_chapter_rank')

        elif tp == 'rally':
            rank_obj = self.mm.get_obj_tools('rally_rank')

        elif tp == 'big_world_power':
            rank_obj = self.mm.get_obj_tools('big_world_power_rank')

        elif tp == 'king_of_song_rank':
            rank_obj = self.mm.get_obj_tools('king_of_song_rank')

        else:
            rank_obj = None

        if not rank_obj:
            return -1, {}   # 没有该类排行榜

        start_rank = page * num + 1
        end_rank = start_rank + num - 1
        users = []

        ranks = rank_obj.get_all_user(start_rank - 1, end_rank - 1, withscores=True)
        self_score = rank_obj.get_score(self.mm.uid)
        self_rank = rank_obj.get_rank(self.mm.uid)

        for rank, (uid, score) in enumerate(ranks, start_rank):
            if tp == 'guild_level':
                score = self.mm.get_obj_by_id('guild', uid).get_guild_lv()
                user_info = guild_rank_info(self.mm, uid, rank, score)
            else:
                user_info = user_rank_info(self.mm, uid, rank, score)
            if tp == 'single_hero':
                mm = self.mm.get_mm(uid)
                info = hero_info(mm.hero, [mm.hero.hero_rank])
                if info:
                    user_info['hero'] = info[0]
                else:
                    user_info['hero'] = {}
            users.append(user_info)

        if tp == 'guild_level':
            self_guild_id = self.mm.user.guild_id
            self_rank = rank_obj.get_rank(self_guild_id)
            self_score = self.mm.get_obj_by_id('guild', self_guild_id).get_guild_lv()
            self_info = guild_rank_info(self.mm, self_guild_id, self_rank, self_score)
        else:
            self_info = user_rank_info(self.mm, self.mm.uid, self_rank, self_score)
        if tp == 'single_hero':
            info = hero_info(self.mm.hero, [self.mm.hero.hero_rank])
            if info:
                self_info['hero'] = info[0]
            else:
                self_info['hero'] = {}

        # 歌王 积分转换成star，rank
        if tp == 'king_of_song_rank':
            for user_info in itertools.chain(users, [self_info]):
                star, rank = rank_obj.parse_star_rank(user_info['score'])
                user_info['king_of_song_star'], user_info['king_of_song_rank'] = star, rank

        data = {
            'top': users,
            'self_info': self_info,
        }
        if not only_rank:
            data['rank_change'] = -10
            data['cur_page'] = page
            data['count'] = rank_obj.get_count()

        return 0, data

    def show_hero_detail(self, uid, hero_oid):
        """
        查看单英雄战力排行榜
        :param uid:
        :param hero_oid:
        :return:
        """
        mm = self.mm.get_mm(uid)

        if not mm.hero.has_hero(hero_oid):
            return 1, {}    # 没有该英雄

        return 0, {
            'hero_info': mm.hero.heros[hero_oid],
        }

    def buy_vip_gift(self, vip):
        """
        购买特权礼包
        :param vip:
        :return:
        """
        if vip in self.user.vip_gift:
            return 1, {}    # 已购买该特权礼包

        if vip > self.user.vip:
            return 2, {}    # vip等级不够

        vip_config = game_config.vip.get(vip)
        if not vip_config:
            return 'error_config', {}

        cost = vip_config['price_real']
        if not self.user.is_diamond_enough(cost):
            return 'error_diamond', {}

        self.user.deduct_diamond(cost)

        gift = vip_config['vip_buy_reward']
        reward = add_mult_gift(self.mm, gift)

        self.user.vip_gift.append(vip)

        self.user.save()

        return 0, {
            'reward': reward,
            'vip_gift': self.user.vip_gift,  # 已购买的特权礼包id
        }

    def level_award(self, lv):
        """
        等级礼包领取奖励
        :param lv:
        :return:
        """
        config = game_config.level_gift.get(lv)
        level_gift_dict = self.user.level_gift.get(lv)
        if not config or not level_gift_dict or level_gift_dict['status'] == 2:
            return 1, {}    # 奖励已领取或者已过期

        if level_gift_dict['status'] == 0:
            return 2, {}    # 充值才能获得

        # if not self.user.is_diamond_enough(config['coin']):
        #     return 'error_diamond', {}

        self.user.level_gift[lv]['status'] = 2
        # self.user.deduct_diamond(config['coin'])

        reward = add_mult_gift(self.mm, config['reward'])

        return 0, {
            'reward': reward,
            'level_limit_gift': self.mm.user.level_gift,  # 限时等级礼包

        }

    def get_player_icon(self):
        """
        获取解锁的头像
        :return:
        """
        unlock_icon = self.unlock_icon()

        return {
            'unlock_icon': unlock_icon,
        }

    def unlock_icon(self):
        """
        获取解锁的icon id
        :return:
        """
        unlock_icon = set()
        for i, j in game_config.player_icon.iteritems():
            sort = j['sort']
            value = j['value']
            flag = False
            if sort == 1:
                flag = True
            elif sort == 2:
                if value in self.mm.hero.father_ids:
                    flag = True
            elif sort == 3:
                if self.mm.user_payment.charge_price >= value:
                    flag = True
            elif sort == 4:
                if self.user.vip >= value:
                    flag = True
            elif sort == 5:
                if self.user.level >= value:
                    flag = True
            elif sort == 6:
                pass    # todo 特定活动

            if flag:
                unlock_icon.add(i)
        unlock_icon = unlock_icon | set(self.user.got_icon)
        return unlock_icon

    def set_got_icon(self,icon):

        config = game_config.main_hero.get(icon,{})
        if not config:
            return 1, {} #没有头像
        if icon in self.user.got_icon:
            return 2, {}  #头像已解锁
        if config['sex'] != game_config.main_hero.get(self.user.role,{})['sex']:
            return 3, {}  #性别不符
        need_diamond = config['price']
        if not self.user.is_diamond_enough(need_diamond):
            return 'error_diamond', {}
        self.user.deduct_diamond(need_diamond)
        self.user.got_icon.append(icon)
        self.user.save()
        return 0, {'got_icon':self.user.got_icon}


    def change_icon(self, icon):
        """
        更换头像
        :param icon:
        :return:
        """
        unlock_icon = self.unlock_icon()

        if icon not in unlock_icon:
            return 1, {}    # 该头像未解锁
        # config = game_config.main_hero.get(icon,{})
        # if not config:
        #     return 1, {} #没有头像
        # need_diamond = config['price']
        # if not self.user.is_diamond_enough(need_diamond):
        #     return 'error_diamond', {}
        # self.user.deduct_diamond(need_diamond)
        self.user.role = icon
        self.user.save()

        return 0, {}

    def title_index(self):
        """
        称号首页
        :return:
        """
        lead_title = self.mm.lead_title
        series = {}

        for i, j in lead_title.has.iteritems():
            config = game_config.title.get(i)
            if not config:
                continue
            s = config['series']
            if s not in series:
                series[s] = i
            elif i > series[s]:
                series[s] = i

        return 0, {
            'series': series.values(),
        }

    def set_title(self, title, down):
        """
        更换称号
        :param title:
        :param down:
        :return:
        """
        lead_title = self.mm.lead_title

        if not down:
            if not lead_title.can_set_cur(title):
                return 1, {}    # 还没有该称号

            if lead_title.cur and lead_title.cur == title:
                return 2, {}    # 该称号正在使用

            lead_title.set_cur(title)
            is_save = True

        else:
            if not lead_title.cur:
                return 3, {}    # 没有称号可卸载

            lead_title.set_cur(0)
            is_save = True

        if is_save:
            lead_title.save()

        return 0, {}

    def buy_silver_index(self):
        """
        点金手index
        :return:
        """
        data = {
            'buy_times': self.user.buy_silver_times,  # 金币购买次数
            'buy_log': self.user.buy_silver_log,     # 金币购买记录
        }

        return data

    def buy_silver(self):
        """
        购买金币
        :return:
        """
        vip = self.user.vip
        can_buy_times = game_config.vip[vip].get('gold_exchange_times', 0)
        buy_times = self.user.get_buy_silver_times()

        if buy_times >= can_buy_times:
            return 1, {}    # 没有购买次数

        gold_exchange_config = game_config.gold_exchange
        if not gold_exchange_config.get(1):
            config = gold_exchange_config
        else:
            for i in sorted(gold_exchange_config.keys()):
                config = gold_exchange_config[i]
                if self.mm.user.level <= config['level']:
                    break
            else:
                return 'error_config', {}

        weight1 = config['weight1']
        weight2 = config['weight2']
        get_coin = config['coin']
        get_coin = random.randint(*get_coin)
        times = config['times']
        cost = config['cost']

        if buy_times % times + 1 == times:
            crit = weight_choice(weight2)[0]
        else:
            crit = weight_choice(weight1)[0]
        if crit:
            get_coin *= crit

        if buy_times >= len(cost):
            cost_diamond = cost[-1]
        else:
            cost_diamond = cost[buy_times]

        if not self.user.is_diamond_enough(cost_diamond):
            return 'error_diamond', {}

        data = {
            'diamond': cost_diamond,  # 花费钻石
            'silver': get_coin,  # 获得金币
            'crit': crit,  # 暴击
        }
        self.user.add_buy_silver_times()
        self.user.add_buy_silver_log(data)

        self.user.deduct_diamond(cost_diamond)
        self.user.add_silver(get_coin)

        self.user.save()

        self.mm.task_data.add_task_data('other_chapter', 110)
        # 点金次数任务
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('buy_silver_times')

        data = {
            'reward': {'silver': get_coin},
        }
        data.update(self.buy_silver_index())

        return 0, data

    def player_detail(self, player_id):
        """
        查看玩家详情
        :param player_id:
        :return:
        """
        if not settings.check_uid(player_id):
            return 'error_100', {}

        mm = ModelManager(player_id)
        hero_obj = mm.hero
        gene_obj = mm.gene

        heros = {}
        genes = {}
        for hoid in hero_obj.max_combat_heros:
            hd = hero_obj.heros.get(hoid)
            if not hd:
                continue
            heros[hoid] = format_hero_info({hoid: hd}, show_attr=True)[0]
            heros[hoid]['gene_pos'] = hd['gene_pos']

            gene_pos = hd['gene_pos']
            for gene_oid in gene_pos:
                if not gene_oid:
                    continue
                gd = gene_obj.genes[gene_oid]
                genes[gene_oid] = fake_deepcopy(gd)
                genes[gene_oid]['combat'] = hero_obj.calc_combat(genes[gene_oid]['effect'])

        data = {
            'heros': heros,
            'genes': genes,
        }

        return 0, data
