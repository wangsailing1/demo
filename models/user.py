#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import time
import datetime
import inspect
import MySQLdb
import copy
import itertools

import settings
from lib.db import ModelBase, ModelTools
from gconfig import game_config, MUITL_LAN
from lib.core.environ import ModelManager
from lib.utils import get_it
from lib.utils import weight_choice
from lib.statistics.bdc_event_funcs import special_bdc_log
from lib.utils.debug import print_log
from lib.utils import time_tools
from return_msg_config import i18n_msg
from lib.utils import sid_generate
from lib.utils import get_last_refresh_time
from tools.user import VipInfo
from models import server as serverM
from models import vip_company
from lib.utils.time_tools import relative_activity_remain_time
from tools.gift import add_mult_gift, calc_gift
from lib.sdk_platform.sdk_uc import send_role_data_uc
from lib.db import get_redis_client
from lib.utils.crypto import md5
# from models.mission import building

BAN_INFO_MESSAGE = {
    'expire': u'我们已对您的账号封停至 {} ！\n',
    'forever': u'我们已对您的账号进行永久封停！\n',
    'reason': u'由于您{}，',
    'no_reason': u'由于您在游戏中进行了违规操作，',
    'basic_start': u'亲爱的玩家，您好：',
    'basic_end': u'如有疑问，请联系官方客服Q群：{}，感谢您的支持！',
}

# 建筑解锁条件（等级）
def lvlup_condition_1(mm,num):
    if mm.user.level < num:
        return 101
    return 0



class User(ModelBase):
    """ 玩家类

    :var buy_silver_times: 0,   购买银币次数
    :var buy_silver_log: [
        {
            'diamond': 0,      # 花费钻石
            'silver': 0,    # 获得金币
            'crit': 0,      # 暴击
        },
    ],
    :var account: 账号
    :var account_reg: 账号注册时间
    :var reg_name: 是否注册过名字
    :var appid: ios或android
    :var package_appid: 包id
    :var register_ip: 注册ip
    :var uuid: 设备唯一标识
    :var channel: 渠道
    :var device: 设备号
    :var status: 账号状态, 0为正常 1为封号
    :var is_new: 是否是新用户
    :var name: 角色名称
    :var level: 角色等级, 通过主英雄等级更新
    :var exp: 战队经验
    :var exp_pot: 战队经验存储罐
    :var update_exp_pot: 更新战斗经验槽时间
    :var privileges: {  特权数据
        1: [{'value': 0, 'rtime': 0, 'ptime': 0}],   类型:  [{特权值: 0, 剩余时间: 0, 战斗经验使用时间: 0}]  剩余时间为秒
    },
    :var diamond: 钻石
    :var coin: 金币
    :var silver: 银币
    :var total_silver: 累积银币
    :var role: 角色id, 主英雄的性别
    :var icon: 主英雄的头像
    :var vip: vip等级
    :var vip_exp: vip经验
    :var active_time: 最后活跃时间
    :var login_days: 登录日期记录
    :var reg_time: 注册时间
    :var guide: 新手引导
    :var guild_id: 公会id
    :var exit_guild_time: 退工会时间
    :var guild_guard: 公会护卫列表
    :var utime: 更新时间 '2015-12-15'
    :var sid: session_id attention
    :var attention: 关注度
    :var expired: session过期时间
    :var mk: 登录+1, 用于验证多点登录
    :var unlock_build: [], 解锁建筑物id
    :var action_point: 0, 体力
    :var action_point_updatetime: 0, 上次体力更新时间
    :var buy_point_times: 0, 购买体力次数
    :var buy_point_date: 0, 购买体力日期
    :var guild_invite: {},    公会邀请信息
    :var apply_guilds: [],    申请的公会记录, 公会id
    :var hunt_coin: 0,          # 末日狩猎挑战券
    :var refresh_date: '',     刷新日期
    :var guild_coin_times: {    # 公会金币副本挑战次数
        coin_id: 0                   # 据点id:使用的次数
    },
    :var guild_exp_times: {    # 公会经验副本挑战次数
        coin_id: 0                   # 据点id:使用的次数
    },
    :var got_icon: [],   # 已解锁icon
    :var opera_awards: [],   # 剧情奖励领取记录
    :var level_mail_done: [],   # 已领取的等级奖励邮件id
    :var coin_log: [],          # 钻石获取记录
    :var ios_payment: {},       # ios 6,30元充值此时做限制
    :var vip_gift: [],          # 已购买的vip特权礼包id
    :var level_gift: {          # 等级限时礼包
        'expire': 0,            # 过期时间
        'status': 0,            # 0未领取，1可领取，2已领取
    },
    :var add_guild_exp: 0       # 每天为公会增加的经验
    :var 'donate': {     # 捐献的三个档次的花费
        1: {             # 科技id
            1: [],        # 档次id：花费
        },
    },
    :var donate_cooling_time: 0,   # 冷却时间
    :var is_donate_cooling: False, # 是否正在冷却中，不能捐献
    :var guild_coin: 0.         # 公会币
    :var vip_daily_reward: False,   # vip每日礼包是否发放
    :var vip_exclusive_notice,   # vip专属通知邮件是否发放
    :var login_reward_id: {},   # 玩家登陆奖励 奖励id和奖励次数
    """
    FREE_CHAT_TIMES = 10  # 聊天每天最多10条免费
    MAX_CHAT_BLACK_LIST = 100  # 最大聊天黑名单人数
    QUIT_LIMIT = 24 * 60 * 60  # 公会申请时限
    MAX_EXCHANGE_NUM = 10000  # 最大兑换上线
    EXCHANGE_LEVEL = 40  # 兑换等级
    EXCHANGE_PROPORTION = 100  # 1钻石兑换多少银币
    MAX_ACTION_POINT = 120  # 最大体力上限
    ADD_POINT_TIME = 60 * 6  # 6分钟恢复一点体力
    PUR_BUY_POINT = 120  # 每次购买体力120点
    MAX_GUILD_COIN_TIMES = 2  # 公会金币副本挑战次数累积上限
    MAX_GUILD_EXP_TIMES = 2  # 公会经验副本挑战次数累积上限
    MAX_HUNT_COIN = 24  # 末日狩猎挑战券每日最多24
    LEVEL_GIFT_EXPIRE = 3600 * 12  # 等级奖励有效期
    MAX_GUILD_EXP = 600  # 每天给公会增加的经验最多600
    MAX_DONATE_COOLING_TIME = 3600 * 8  # 公会捐献最大冷却时间
    SESSION_EXPIRED = 24 * 3600  # session过期时间
    REFRESH_TIME1 = '05:00:00'  # 刷新时间
    SERVER_OPENING_AWARD_EXPIRE = 7  # 开服奖励有效期 天数
    ONLINE_USERS_TIME_RANGE = 5 * 60  # 判断用户在线的时间参考
    INIT_VIP_BUILD_ID = 2201

    # 和前端协定1:android,2:iOS
    APPID_OS_MAPPING = {
        '2': 'ios',
        '1': 'android',
    }

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'tpid': 0,  # 英雄互娱给的 渠道id, 0为母包，母包不上线
            'chat_times': {},
            'buy_silver_times': 0,
            'buy_silver_log': [],
            'question_done': False,  # 是否已发问卷奖励
            'account': '',
            'account_reg': 0,
            'appid': '',
            'package_appid': '',
            'register_ip': '',
            'active_ip': '',
            'final_action': '',
            'uuid': '',
            'reg_name': False,
            'change_name': 0,  # 改名次数
            'channel': '',
            'device': '',
            'status': 0,
            'is_new': 1,
            # 'name': '',
            '_name': '',
            'level': 1,
            'exp': 0,
            'exp_pot': 0,
            'update_exp_pot': 0,
            'privileges': {},
            'update_privilege': 0,
            'got_icon': [],
            # 'diamond': 0,
            'consume_diamond': 0,  # 历史消费钻石
            'consume_silver': 0,  # 历史消费钻石
            'diamond_free': 0,
            'diamond_charge': 0,
            'coin': 0,
            'silver': 0,
            'dollar': 0,  # 美元
            'script_income': 0,  # 拍片总票房
            'script_license': game_config.common[20],  # 拍片许可证
            'license_update_time': int(time.time()),  # 拍片许可证恢复时间
            'license_recover_times': 0,  # 许可证当日恢复次数
            'used_license_times': 0,  # 许可证当日使用次数

            'attention': {},
            'total_silver': 0,
            'like': 0,  # 点赞数
            'role': 0,
            'vip': 0,
            'vip_exp': 0,
            'company_vip_exp': 0,
            'company_vip': 1,
            'company_vip_reward': [], # 已领取的vip礼包
            'active_time': 0,
            'online_time': 0,
            'login_days': [],
            'reg_time': 0,
            'guide': {},
            # 公会信息
            'guild_id': '',
            'guild_name': '',
            'exit_guild_time': 0,
            'guild_guard': [],
            'guild_invite': {},
            'apply_guilds': [],
            'guild_coin_times': {},
            'guild_exp_times': {},
            # 公会信息
            'utime': '',
            'sid': '',
            'expired': '',
            'mk': 0,
            'unlock_build': [],
            'action_point': game_config.common[60],
            'action_point_updatetime': int(time.time()),
            'buy_point_times': 0,
            # 'buy_point_date': '',
            'refresh_date': '',
            'refresh_week': '',
            'hunt_coin': 0,
            'opera_awards': [],
            'level_mail_done': [],
            'coin_log': [],
            'ios_payment': {},
            'vip_gift': [],
            'level_gift': {},
            'add_guild_exp': 0,
            'donate': {},
            'donate_cooling_time': 0,  # 冷却时间
            'is_donate_cooling': False,  # 是否正在冷却中，不能捐献
            'guild_coin': 0,
            'language_sort': '1' if settings.LANGUAGE == 'ch' else '0',
            'vip_daily_reward': False,  # vip每日礼包是否发放
            'vip_exclusive_notice': False,  # vip专属通知邮件是否发放
            'login_reward_id': {},
            'refresh_date1': 0,  # 5点刷新
            'team_skill_exp': 0,  # 战队技能经验
            'blacklist': [],  # 聊天屏蔽uid
            'is_ban': 0,  # 封号，0表示不封，1表示封禁
            'ban_reason': u'',  # 封号理由
            'ban_expire': 0,  # 过期时间，0表示永久封禁，正数表示过期时间
            'ban_time': 0,  # 封停时间
            'ban_person': u'',  # 操作员
            'ban_chat': 0,  # 禁言，0表示不禁言，1表示禁言
            'bchat_reason': u'',  # 禁言理由
            'bchat_expire': 0,  # 过期时间，0表示永久禁言，正数表示过期时间
            'bchat_time': 0,  # 禁言时间
            'donate_times': 0,  # 公会科技捐献次数
            'tile_power': 0,  # 势力值
            'last_add_gs_msg': 0,  # gs客服消息时间
            'rebate_flag': False,  # 是否已返利
            '_build': {},  # 建筑信息
            'dialogue': [],  # 剧情信息
            'skip_dialouge': 0,
            'skip_battle': 0,
        }
        self._cache = {}
        self.DEFAULT_MAX_EXP_POT = game_config.get_value(11, 2000)  # 经验存储上限默认值
        super(User, self).__init__(self.uid)

    @classmethod
    def get_public_redis(cls):
        return get_redis_client(settings.public)

    @classmethod
    def get_name_unique_key(cls, name, k=None):
        if not k:
            k = int(md5(name),16) % 20
        return 'models.user||User||public||NameUnique||%s'%k


    @classmethod
    def set_name_unique(cls, name):
        if cls.is_exists_name(name):
            return 1  # 名字存在
        redis = cls.get_public_redis()
        key = cls.get_name_unique_key(name)
        redis.hset(key, name, 1)
        return 0

    @classmethod
    def is_exists_name(cls, name):
        redis = cls.get_public_redis()
        key = cls.get_name_unique_key(name)
        return redis.hexists(key, name)

    @classmethod
    def del_name_unique(cls, name):
        redis = cls.get_public_redis()
        key = cls.get_name_unique_key(name)
        redis.hdel(key, name)

    @classmethod
    def get_all_name_unique(cls, num):
        redis = cls.get_public_redis()
        key = cls.get_name_unique_key('', num)
        return redis.hgetall(key)

    def set_tpid(self, tpid):
        self.tpid = tpid
        self.cache_tpid(self._server_name, self.uid, tpid)

    @classmethod
    def cache_tpid(cls, server, uid, tpid):
        key = cls.make_key_cls('tpid_cahce', server)
        redis = cls.get_redis_client(server)
        redis.hset(key, uid, tpid)

    @classmethod
    def get_tpid_from_cache(cls, server, special_uids=None):
        key = cls.make_key_cls('tpid_cahce', server)
        redis = cls.get_redis_client(server)
        if not special_uids:
            return redis.hgetall(key)

        if isinstance(special_uids, (basestring, str)):
            special_uids = [special_uids]

        data = {}
        for uid, tpid in itertools.izip(special_uids, redis.hmget(key, special_uids)):
            if tpid is not None:
                data[uid] = tpid

        return data

    @classmethod
    def get(cls, uid, server_name='', from_req=True, **kwargs):
        o = super(User, cls).get(uid, server_name=server_name, **kwargs)
        if from_req:
            o.refresh()
        o.father_server_name = settings.get_father_server(o._server_name)
        o.config_type = game_config.get_config_type(o.father_server_name)
        o.init_build()
        return o

    def get_user_name_key(self):
        """
        :return:
        """
        key = self.make_key(uid='user_name')
        return key

    def property_name():
        doc = 'The name property'

        def fget(self):
            return self._name

        def fset(self, value):
            if not value:
                return
            name_key = self.get_user_name_key()
            uid = self.uid
            old_uids_str = self.redis.hget(name_key, self._name)
            if old_uids_str:
                old_uids = eval(old_uids_str)
            else:
                old_uids = set()
            new_uids_str = self.redis.hget(name_key, value)
            if new_uids_str:
                new_uids = eval(new_uids_str)
            else:
                new_uids = set()
            old_uids.discard(uid)
            # 将旧有的uid键值去掉
            if old_uids:
                self.redis.hset(name_key, self._name, old_uids)
            else:
                self.redis.hdel(name_key, self._name)

            # 数据库中该键值已有数据与uid拼起来
            new_uids.add(uid)
            self.redis.hset(name_key, value, new_uids)
            self._name = value

        return locals()

    name = property(**property_name())

    def get_uid_by_name(self, name):
        name_key = self.get_user_name_key()
        uids = self.redis.hget(name_key, name)
        if uids:
            uids = eval(uids)
        else:
            uids = set()
        return uids

    def refresh(self):
        """
        刷新
        :return:
        """
        # todo 数据升级，上线前删除 2019.03.14
        for lv, level_gift_dict in self.level_gift.items():
            if not isinstance(level_gift_dict, dict):
                self.level_gift.pop(lv)

        is_save = False
        now = int(time.time())
        today = time.strftime('%F')
        week = time.strftime('%W')
        if not self.company_vip:
            self.company_vip = 1
            is_save= True
        if not self.skip_dialouge:
            if vip_company.if_skip_story(self):
                self.skip_dialouge = vip_company.if_skip_story(self)
                is_save = True
        if not self.skip_battle:
            if vip_company.if_skip_battle(self):
                self.skip_battle = vip_company.if_skip_battle(self)
                is_save = True
        # 刷新体力
        div, mod = divmod(now - self.action_point_updatetime, game_config.common[59])
        if not self.is_point_max() and div > 0:
            self.add_action_point(div)
            self.action_point_updatetime = now - mod
            is_save = True

        # 刷新限时等级礼包
        for lv, level_gift_dict in self.level_gift.items():
            expire = level_gift_dict.get('expire', 0)
            status = level_gift_dict.get('status', 0)
            if now <= expire:
                continue
            if status == 1:
                continue
            # self.level_gift.pop(lv)
            is_save = True

        # if self.refresh_week != week and self.uid not in game_config.vip_exclusive_notice:
        #     self.refresh_week = week
        #     self.vip_exclusive_notice = False
        #     is_save = True
        data = int(time.mktime(time.strptime(time.strftime('%F') + ' ' + '00:00:00', '%Y-%m-%d %H:%M:%S')))
        if self.refresh_date != today:
            self.refresh_date = today
            self.add_guild_exp = 0
            self.hunt_coin = 0
            self.ios_payment = {}
            self.vip_daily_reward = False
            self.chat_times = {}
            self.buy_silver_times = 0
            self.buy_silver_log = []
            # 如果前一天有遗留未完成恢复, 直接完成, 今天的重新开始计算
            if self.can_recover_license_times():
                if not self.inited:
                    self.script_license += 1
            self.license_recover_times = 0
            self.license_update_time = now
            is_save = True

        refresh_date1 = get_last_refresh_time(self.REFRESH_TIME1)
        if self.refresh_date1 != refresh_date1:
            self.refresh_date1 = refresh_date1
            self.guild_coin_times = {}
            self.guild_exp_times = {}
            self.buy_point_times = 0
            is_save = True

        if not 0 <= now - self.donate_cooling_time <= game_config.get_value(108, 480) * 60 and self.donate_cooling_time:
            self.donate_cooling_time = 0
            self.donate_times = 0
            is_save = True

        # 许可证恢复
        if self.can_recover_license_times():
            recover_need_time = self.license_recover_need_time()
            div, mod = divmod(now - self.license_update_time, recover_need_time)
            while div and self.can_recover_license_times():
                is_save = True
                self.script_license += 1
                self.license_recover_times += 1
                self.license_update_time += recover_need_time

                recover_need_time = self.license_recover_need_time()
                if not recover_need_time:
                    break
                div, mod = divmod(now - self.license_update_time, recover_need_time)

        if not self.can_recover_license_times():
            self.license_update_time = now

        if is_save:
            self.save()

    def license_recover_need_time(self):
        cd = game_config.script_license.get('cd', [])
        if not cd:
            return 0
        times = self.license_recover_times
        if times >= len(cd):
            times = -1
        return cd[times] * 60

    def max_license(self):
        more_license = vip_company.more_license(self)
        return game_config.common[20] + more_license

    def can_recover_license_times(self):
        if self.script_license >= self.max_license():
            return False
        gacha_cd = game_config.script_license.get('cd', [])
        return self.license_recover_times < len(gacha_cd)

    def remain_recover_times(self):
        gacha_cd = game_config.script_license.get('cd', [])
        return max(len(gacha_cd) - self.license_recover_times, 0)

    def license_recover_expire(self):
        """恢复倒计时"""
        if not game_config.script_license:
            return 0

        if not self.can_recover_license_times():
            return 0

        cd = game_config.script_license['cd']
        times = self.license_recover_times
        if times >= len(cd):
            return 0

        need_time = cd[times] * 60
        return need_time - (int(time.time()) - self.license_update_time)

    def get_license_recover_red_dot(self):
        return [self.script_license, self.license_recover_expire()]

    def add_buy_silver_times(self, num=1):
        """
        增加银币购买次数
        :param num:
        :return:
        """
        self.buy_silver_times += num

    def get_buy_silver_times(self):
        """
        获取银币购买次数
        :return:
        """
        return self.buy_silver_times

    def add_buy_silver_log(self, data):
        """
        购买金币日志
        :param data:
        :return:
        """
        self.buy_silver_log.append(data)

    def get_buy_silver_log(self):
        """
        金币日志
        :return:
        """
        return self.buy_silver_log

    def get_chat_times(self, tp):
        """
        聊天次数
        :return:
        """
        return self.chat_times.get(tp, 0)

    def add_chat_times(self, tp):
        """
        记录聊天次数
        :param tp:
        :return:
        """
        from tools.pay import get_chat_need_diamond
        cur_times = self.get_chat_times(tp)
        if cur_times >= self.FREE_CHAT_TIMES:
            cost_diamond = get_chat_need_diamond(self.mm, cur_times - self.FREE_CHAT_TIMES)
            if not self.is_diamond_enough(cost_diamond):
                return False
            self.deduct_diamond(cost_diamond)
        self.chat_times[tp] = self.chat_times.get(tp, 0) + 1
        self.save()
        return True

    def diamond():
        doc = "The diamond property."

        def fget(self):
            return self.diamond_free + self.diamond_charge

        def fset(self, value):
            # 1. 加钻石，都加到免费中
            # 2. 减钻石, 先消耗charge，再消耗free
            # 实现的效果：从diamond添加都加到free；消耗优先消耗charge，再消耗free；只能手动用diamond_charge添加付费金币
            diff_diamond = value - (self.diamond_free + self.diamond_charge)
            if diff_diamond < 0:  # 减钻石
                remain_diamond = self.diamond_charge + diff_diamond
                if remain_diamond < 0:
                    self.diamond_charge = 0
                    self.diamond_free = value
                else:
                    self.diamond_charge = remain_diamond

            elif diff_diamond > 0:  # 加钻石
                self.diamond_free += diff_diamond

        return locals()

    diamond = property(**diamond())

    def add_donate_cooling_time(self, add_time):
        """
        增加捐献的冷却时间
        :param add_time: 1s
        :return:
        """
        now = int(time.time())
        if self.donate_cooling_time > 0:
            self.donate_cooling_time += add_time
        else:
            self.donate_cooling_time = now + add_time
        if self.donate_cooling_time - now >= self.MAX_DONATE_COOLING_TIME:
            self.is_donate_cooling = True

    def refresh_donate_cooling_time(self):
        """
        更新捐献的冷却时间
        :return:
        """
        now = int(time.time())
        if now > self.donate_cooling_time:
            self.reset_donate_cooling()
            return True

        return False

    def refresh_donate(self, tech_id, donate_id):
        """
        刷新可捐献项
        :param tech_id: 科技id
        :param donate_id: 档次id
        :return:
        """
        donate_dict = self.donate.get(tech_id, {})
        tech_config = game_config.guild_technology.get(tech_id)
        if not tech_config:
            return False

        if not donate_dict:
            donate_dict[1] = weight_choice(tech_config['cost'][1])[:3]
        else:
            donate_dict.pop(2, None)
            donate_dict.pop(3, None)
            guild_donate_config = game_config.guild_donate.get(donate_id)
            if not guild_donate_config:
                return False
            for i in game_config.guild_donate.keys():
                if not get_it(guild_donate_config.get('rate%s' % i, 100)):
                    continue
                donate_dict[i] = weight_choice(tech_config['cost'][i])[:3]

        self.donate[tech_id] = donate_dict
        return True

    def guild_donate(self, tech_id, donate_id):
        """
        公会捐献
        :param tech_id:
        :param donate_id:
        :return:
        """
        now = int(time.time())
        self.donate_times += 1
        max_donate_times = game_config.get_value(107, 10)
        if self.donate_times >= max_donate_times:
            self.donate_cooling_time = now

    def can_donate(self):
        """
        是否可以捐献
        :return:
        """
        max_donate_times = game_config.get_value(107, 10)
        donate_times = self.donate_times
        if donate_times >= max_donate_times:
            return False
        else:
            return True

    def reset_donate_cooling(self):
        """
        重置捐献冷却
        :return:
        """
        self.donate_times = 0
        self.donate_cooling_time = 0

    def get_donate_cooltime(self):
        """
        获取捐献冷却时间
        :return:
        """
        now = int(time.time())
        if 0 <= now - self.donate_cooling_time <= game_config.get_value(108, 480) * 60:
            return game_config.get_value(108, 480) * 60 + self.donate_cooling_time - now
        else:
            return 0

    def get_donate_rest_times(self):
        """
        获取可捐献次数
        :return:
        """
        max_donate_times = game_config.get_value(107, 10)
        donate_times = self.donate_times

        if donate_times < max_donate_times:
            return max_donate_times - donate_times
        else:
            return 0

    def update_active_time(self, req):
        """
        更新登录状态
        :return:
        """
        self.active_ip = req.headers.get('X-Real-Ip', '') or req.remote_ip
        ts = int(time.time())
        if not self.active_time:
            self.active_time = ts
        if not self.online_time:
            self.online_time = ts

        today = time.strftime('%F')
        if today not in self.login_days:
            self.login_days.append(today)

        # 重新登录，计算上次的连续在线时长
        if ts - self.active_time > self.ONLINE_USERS_TIME_RANGE:
            online_duration = self.active_time - self.online_time
            self.online_time = ts
            _kwargs = {
                'ldt': time_tools.strftimestamp(self.active_time),
                'duration': online_duration,
                'final_action': self.final_action,
            }
            special_bdc_log(self, sort='role_logout', **_kwargs)

        self.active_time = ts
        self.final_action = self.mm.action

    def decr_guild_coin_times(self, coin_id, num=1, save=False):
        """
        扣除公会金币副本挑战次数
        :param coin_id:
        :param num: 扣除次数
        :param save:
        :return:
        """
        cur_times = self.guild_coin_times.get(coin_id, 0)
        if cur_times + num > self.MAX_GUILD_COIN_TIMES:
            return False

        self.guild_coin_times[coin_id] = cur_times + num

        if save:
            self.save()

        return True

    def remain_guild_coin_times(self, coin_id):
        """
        公会金币副本剩余挑战次数
        :param coin_id:
        :return:
        """
        return max(self.MAX_GUILD_COIN_TIMES - self.guild_coin_times.get(coin_id, 0), 0)

    def decr_guild_exp_times(self, exp_id, num=1, save=False):
        """
        扣除公会经验副本挑战次数
        :param exp_id:
        :param num: 扣除次数
        :param save:
        :return:
        """
        cur_times = self.guild_exp_times.get(exp_id, 0)
        if cur_times + num > self.MAX_GUILD_EXP_TIMES:
            return False

        self.guild_exp_times[exp_id] = cur_times + num

        if save:
            self.save()

        return True

    def remain_guild_exp_times(self, coin_id):
        """
        公会经验副本剩余挑战次数
        :param coin_id:
        :return:
        """
        return max(self.MAX_GUILD_EXP_TIMES - self.guild_exp_times.get(coin_id, 0), 0)

    def regist_days(self):
        """
        计算玩家已注册天数
        """
        if 'regist_days' not in self._cache:
            regist_date = datetime.datetime.fromtimestamp(self.reg_time)
            days = (datetime.date.today() - regist_date.date()).days + 1
            self._cache['regist_days'] = days
        return self._cache['regist_days']

    def add_hunt_coin(self, coin):
        """
        增加末日狩猎挑战券
        :param coin:
        :return:
        """
        self.hunt_coin = min(self.hunt_coin + coin, self.MAX_HUNT_COIN)

    def decr_hunt_coin(self, coin):
        """
        扣除末日狩猎挑战券
        :param coin:
        :return:
        """
        self.hunt_coin = max(self.hunt_coin - coin, 0)

    def get_hunt_coin(self):
        """
        剩余末日狩猎挑战券
        :return:
        """
        return max(self.MAX_HUNT_COIN - self.hunt_coin, 0)

    def add_guild_coin(self, coin):
        """
        增加公会币
        :param coin:
        :return:
        """
        self.guild_coin += int(coin)

    def is_guild_coin_enough(self, coin):
        """
        公会币是否充足
        :param coin:
        :return:
        """
        return self.guild_coin >= int(coin)

    def deduct_guild_coin(self, coin):
        """
        扣除公会币
        """
        if self.is_guild_coin_enough(coin):
            self.guild_coin -= coin

    def add_action_point(self, point, force=False, save=False):
        """
        增加体力
        :param point: 体力值
        :param force: 是否强制加体力
        :param save:
        :return:
        """
        point = int(point)
        if not force:
            if self.action_point < game_config.common[60]:
                self.action_point = min(game_config.common[60], self.action_point + point)
        else:
            self.action_point += point

        if save:
            self.save()

    # 获取性别
    def get_sex(self):
        config = game_config.main_hero
        if not self.role:
            return 0
        if not self.role not in config:
            return 0
        return config[self.role]['sex']

    def decr_action_point(self, point, save=False):
        """
        扣除体力
        :param point:
        :param save:
        :return:
        """
        if self.action_point < point:
            return False

        # 体力从满减少到不满时,更新更新时间
        if self.action_point - point < game_config.common[60] <= self.action_point:
            self.action_point_updatetime = int(time.time())

        self.action_point -= point

        # 增加公会活跃度
        if self.guild_id and self.add_guild_exp < self.MAX_GUILD_EXP:
            add_point = min(self.MAX_GUILD_EXP - self.add_guild_exp, point)
            self.add_guild_exp += add_point
            guild = self.mm.get_obj_by_id('guild', self.guild_id)
            # guild.add_guild_exp(add_point)
            guild.add_active_value(self.uid, add_point)
            guild.save()

        if save:
            self.save()

        # 记录累积消耗体力
        self.mm.task_data.add_task_data('other_chapter', 107)

        # 消耗体力任务
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('use_action_point', point)

        return True

    def is_action_point_enough(self, point):
        """
        体力是否足够
        :param point:
        :return:
        """
        return self.action_point >= point

    def next_point_time(self):
        """
        下点体力恢复剩余时间
        :return:
        """
        if self.is_point_max():
            return 0

        now = int(time.time())
        return max(0, game_config.common[59] - (now - self.action_point_updatetime))

    def max_point_time(self):
        """
        体力恢复满剩余时间
        :return:
        """
        if self.is_point_max():
            return 0

        return (game_config.common[60] - self.action_point - 1) * game_config.common[59] + self.next_point_time()

    def is_point_max(self):
        """
        体力是否已满
        :return:
        """
        return self.action_point >= game_config.common[60]

    def add_buy_point_times(self):
        """
        购买体力
        :return:
        """
        self.buy_point_times += 1

    def add_apply_guilds(self, gid):
        """
        增加申请公会记录
        :return:
        """
        if gid not in self.apply_guilds:
            self.apply_guilds.append(gid)
            per_applymax = game_config.guild_build.get('per_applymax', 5)
            if len(self.apply_guilds) > per_applymax:
                self.apply_guilds.pop(0)

    def del_apply_guilds(self, gid):
        """
        删除申请公会记录
        :param gid:
        :return:
        """
        if gid in self.apply_guilds:
            self.apply_guilds.remove(gid)

    def record_privilege_gift(self, gift_id=None, charge_config=None, save=False):
        """
        记录特权礼包
        :param gift_id:
        :return:
        """
        if charge_config:
            if charge_config['sort'] != 3:
                return False  # 充值表中sort为3是特权礼包
            gift_id = charge_config['value']

        charge_privilege_config = game_config.charge_privilege.get(gift_id)
        if charge_privilege_config is None:
            return False

        if not self.update_privilege and not self.privileges:
            self.update_privilege = int(time.time())

        need_time = charge_privilege_config['time']
        privileges = charge_privilege_config['privilege']
        for pid, value in privileges:
            if pid in self.privileges:
                own_privilege = self.privileges[pid]
                index = None
                for i, data in enumerate(own_privilege):
                    if data['value'] == value:
                        index = i
                        break
                if index is None:
                    own_privilege.append({'value': value, 'rtime': need_time * 60, 'ptime': 0})
                    own_privilege.sort(key=lambda x: x['value'], reverse=True)
                else:
                    own_privilege[index]['rtime'] += need_time * 60
            else:
                self.privileges[pid] = [{'value': value, 'rtime': need_time * 60, 'ptime': 0}]

        if save:
            self.save()

    def refresh_exp_pot(self):
        """ 刷新经验槽
        作废
        :return:
        """
        # if not self.mm.user.check_build(EXP_POT):
        #     return

        now = int(time.time())
        if not self.update_exp_pot:
            self.update_exp_pot = now
            self.save()
            return

        diff_time = now - self.update_exp_pot
        self.update_exp_pot = now
        mod = self.add_exp_pot(diff_time)
        self.update_exp_pot -= mod
        self.save()

    def add_exp_pot(self, diff_time):
        """ 增加战斗经验槽
        exp: 挂机人数 * 0.6

        :param diff_time:
        :return:
        """
        count, mod = divmod(diff_time, 60)
        if count <= 0:
            return 0
        privilege_obj = self.mm.get_event('privilege')
        uplimit = privilege_obj.exp_pot_uplimit()
        if self.exp_pot >= uplimit:
            return 0
        exp = privilege_obj.every_miu_exp_pot()
        if exp:
            self.exp_pot += exp * count
            if self.exp_pot >= uplimit:
                self.exp_pot = uplimit
            self.save()
        return mod

    def receive_exp(self, save=False):
        """ 领取战队经验储值

        :param save:
        :return:
        """
        add_exp = self.exp_pot
        if not add_exp:
            return False

        self.add_player_exp(add_exp)
        self.exp_pot = 0

        if save:
            self.save()

        return True

    def is_diamond_enough(self, diamond):
        """ 是否钻石足够

        :param diamond:
        :return:
        """
        return self.diamond >= int(diamond)

    def deduct_diamond(self, diamond):
        """ 扣除钻石

        :param diamond:
        :return:
        """
        diamond = int(diamond)
        if self.is_diamond_enough(diamond):
            self.diamond -= diamond
            self.consume_diamond += diamond
            # 消费记录
            spend_event = self.mm.get_event('spend_event')
            spend_event.record(diamond)

            #超级大玩家
            self.mm.superplayer.add_day_spend(diamond)
            # 消耗钻石活动
            # if self.mm.action not in settings.SPEND_IGNORE_METHOD:
            #     server_type = int(self.mm.user.config_type)
            #     if server_type == 1:
            #         # 新服累计消费钻石
            #         self.mm.server_active_consume.add_consume_diamond(diamond)
            #         # 新服每日消费钻石
            #         self.mm.server_daily_consume.add_consume_diamond(diamond)
            #
            #         # 天降红包
            #         self.mm.server_red_bag.consume_trigger(diamond)
            #     else:
            #         # 累计消费钻石
            #         self.mm.active_consume.add_consume_diamond(diamond)
            #         # 每日消费钻石
            #         self.mm.active_daily_consume.add_consume_diamond(diamond)
            #         # 宇宙最强加积分
            #         self.mm.super_active.add_score(diamond)
            #         # 天降红包
            #         self.mm.red_bag.consume_trigger(diamond)
            # task_event_dispatch = self.mm.get_event('task_event_dispatch')
            # task_event_dispatch.call_method('task_consume_diamond', count=diamond)

    def add_diamond(self, diamond):
        """ 增加钻石

        :param diamond:
        :return:
        """
        self.diamond += int(diamond)
        # 获得钻石记录
        earn_event = self.mm.get_event('earn_event')
        earn_event.record(diamond)
        # frame = inspect.currentframe()
        # s = ''
        # is_skip = False
        # while frame is not None:
        #     if settings.BASE_ROOT in frame.f_code.co_filename:
        #         s += '%s %s %s\n' % (frame.f_code.co_filename, frame.f_code.co_name, frame.f_lineno)
        #     elif is_skip:
        #         s += '%s %s %s\n' % (frame.f_code.co_filename, frame.f_code.co_name, frame.f_lineno)
        #         break
        #     else:
        #         is_skip = True
        #     frame = frame.f_back
        # print_log('f: ', s)

    def is_coin_enough(self, coin):
        """ 是否金币足够

        :param coin:
        :return:
        """
        return self.coin >= int(coin)

    def deduct_coin(self, coin):
        """ 扣除金币

        :param coin:
        :return:
        """
        coin = int(coin)
        if self.is_coin_enough(coin):
            self.coin -= coin

    def add_coin(self, coin):
        """ 增加金币

        :param coin:
        :return:
        """
        self.coin += int(coin)

    def is_dollar_enough(self, num):
        """ 是否美元足够

        :param num:
        :return:
        """
        return self.dollar >= int(num)

    def deduct_dollar(self, num):
        """ 扣除美元

        :param num:
        :return:
        """
        num = int(num)
        if self.is_dollar_enough(num):
            self.dollar -= num

    def add_dollar(self, num):
        """ 增加美元

        :param num:
        :return:
        """
        self.dollar += int(num)

    def is_script_income_enough(self, num):
        """ 是否拍片票房足够

        :param num:
        :return:
        """
        return self.script_income >= int(num)

    def deduct_script_income(self, num):
        """ 扣除拍片票房

        :param num:
        :return:
        """
        num = int(num)
        if self.is_script_income_enough(num):
            self.script_income -= num

    def add_script_income(self, num):
        """ 增加拍片票房

        :param num:
        :return:
        """
        self.script_income += int(num)

    def is_like_enough(self, like):
        """ 是否点赞足够

        :param like:
        :return:
        """
        return self.like >= int(like)

    def deduct_like(self, like):
        """ 扣除点赞

        :param like:
        :return:
        """
        like = int(like)
        if self.is_like_enough(like):
            self.like -= like

    def add_like(self, like):
        """ 增加点赞

        :param like:
        :return:
        """
        self.like += int(like)

    def add_attention(self, type, attention):
        self.attention[type] = self.attention.get(type, 0) + int(attention)

    def is_silver_enough(self, silver):
        """ 是否银币足够

        :param silver:
        :return:
        """
        return self.silver >= int(silver)

    def deduct_silver(self, silver):
        """ 扣除银币

        :param silver:
        :return:
        """
        silver = int(silver)
        if self.is_silver_enough(silver):
            self.silver -= silver
            self.consume_silver += silver
            # 消耗金币任务
            task_event_dispatch = self.mm.get_event('task_event_dispatch')
            task_event_dispatch.call_method('task_consume_silver', count=silver)

    def add_silver(self, silver):
        """ 增加银币

        :param silver:
        :return:
        """
        self.silver += int(silver)

        # 触发累积金钱任务
        self.total_silver += int(silver)
        task_event_dispatch = self.mm.get_event('task_event_dispatch')
        task_event_dispatch.call_method('get_silver', add_value=int(silver))

    def set_tile_power(self, power):
        self.tile_power = power

    def is_tile_power_enough(self, num):
        """ 是否势力值足够

        :param num:
        :return:
        """
        return self.tile_power >= int(num)

    def deduct_tile_power(self, num):
        """ 扣除势力值

        :param num:
        :return:
        """
        num = int(num)
        if self.is_tile_power_enough(num):
            self.tile_power -= num

    def add_tile_power(self, num):
        """ 增加势力值

        :param num:
        :return:
        """
        self.tile_power += int(num)

    def add_king_war_score(self, num):
        """ 增加斗技商城币

        :param num:
        :return:
        """
        self.king_war_score += int(num)

    def update_session_and_expired(self, sid, expired):
        """ 更新session和过期时间

        :return:
        """
        if self.sid == sid and self.expired == expired:
            return False

        self.sid = sid
        self.expired = expired
        return True

    def session_expired(self, session):
        """ 检查session是否过期

        :param session:
        :return:
        """
        # 从sid中获取时间戳
        if not session:
            return True
        ts = session[-10:]
        if not ts.isdigit():
            return True
        ts = int(ts)
        expired = ts + self.SESSION_EXPIRED

        # 2018.05.19 缩短session长度,做个兼容
        long_value = len(session) == 42  # long value: md5 + int(time.time())
        sid = sid_generate(self.account, str(ts), long_value)
        print session, sid, long_value
        # 检验是否过期及sid正确性
        if expired < time.time():
            return True
        elif sid != session:
            return True
        else:
            return False

    def set_guild(self, gid, exit_guild_time=0, guild_name=''):
        """ 设置公会数据, 如果之前有数据需要清理之前的

        :param gid:
        :return:
        """
        self.guild_id = gid
        self.guild_name = guild_name
        self.exit_guild_time = exit_guild_time
        self.guild_guard = []
        self.apply_guilds = []
        self.add_guild_exp = 0

        if gid:
            # 加入公会任务
            task_event_dispatch = self.mm.get_event('task_event_dispatch')
            task_event_dispatch.call_method('join_guild')

    def add_vip_exp(self, add_exp, is_save=False):
        is_uplevel = False
        if not add_exp:
            return False
        cur_exp = self.vip_exp
        next_exp = self.vip_exp + add_exp
        cur_level = self.vip
        next_level = self.vip
        while 1:
            if next_level + 1 not in game_config.vip:
                is_uplevel = False
                break
            if next_exp >= game_config.vip[next_level]['need_exp']:
                next_level += 1
                is_uplevel = True
                continue
            break

        if next_level > self.vip:
            # 触发vip升级解锁建筑
            task_event_dispatch = self.mm.get_event('task_event_dispatch')
            task_event_dispatch.call_method('vip_level_upgrade', next_level)

        self.vip_exp = next_exp
        self.vip = next_level
        if cur_level < 8 <= self.vip:
            self.send_vip_exclusive_notice()

        if is_uplevel:
            vip_info = VipInfo('', self.father_server_name)
            vip_info.exchange_vip_log(next_level, self.uid)

        if is_save:
            self.save()

        kwargs = {
            'old_exp': cur_exp,
            'cur_exp': self.vip_exp,
            'old_lv': cur_level,
            'cur_lv': self.vip,
            'change_type': 'VIP_EXP',  # 级别经验类型 玩家经验、等级
        }
        special_bdc_log(self, sort='exp_change', **kwargs)
        special_bdc_log(self, sort='level_change', **dict(kwargs, change_type='VIP'))

    # 增加company_vip经验
    def add_company_vip_exp(self,add_exp, is_save=False):
        if not add_exp:
            return False
        next_exp = self.company_vip_exp + add_exp
        # next_level = self.company_vip
        config = game_config.vip_company
        # while True:
        #     if next_level + 1 not in config:
        #         break
        #     if next_exp >= config[next_level]['need_exp']:
        #         next_level += 1
        #         continue
        #     break

        self.company_vip_exp = next_exp
        # self.company_vip = next_level
        if is_save:
            self.save()

    # 公司凝聚力是否达到升级要求红点
    def get_company_vip_red_dot(self):
        config = game_config.vip_company
        if 22 not in self.group_ids:
            return True
        next_lv = self.company_vip + 1
        if next_lv not in config:
            return False
        need_company_vip = config[next_lv].get('exp', 100)
        if self.company_vip_exp >= need_company_vip:
            return True
        return False

    # 可以领取的company_vip礼包
    @property
    def can_get_company_vip_reward(self):
        reward_list = range(1, self.company_vip + 1)
        return list(set(reward_list) - set(self.company_vip_reward))


    def add_player_exp(self, add_exp):
        """ 增加战队经验

        :param add_exp: 增加的经验
        :return:
        """
        add_exp = int(add_exp)
        cur_level = self.level
        cur_exp = self.exp
        max_level = max(game_config.player_level)
        next_need_exp = game_config.player_level.get(cur_level, {}).get('exp')

        if next_need_exp is None:
            return False

        if max_level <= cur_level and cur_exp >= next_need_exp:
            return False

        exp = cur_exp + add_exp
        level = cur_level

        while exp >= next_need_exp:
            give_power = game_config.player_level.get(level, {}).get('give_power', 0)
            self.add_action_point(give_power, force=True)
            level += 1
            if max_level <= level:
                level = max_level
                exp = min(exp, game_config.player_level.get(level, {}).get('exp'))
                break
            exp -= next_need_exp
            next_need_exp = game_config.player_level.get(level, {}).get('exp')

        self.exp = exp
        self.level = level

        if self.level > cur_level:
            # 发送等级奖励邮件
            self.send_level_mail(cur_level, self.level)
            # 触发升级任务, 解锁建筑
            task_event_dispatch = self.mm.get_event('task_event_dispatch')
            task_event_dispatch.call_method('level_upgrade', self.level, add_value=self.level - cur_level)
            # 等级变化更新黑街擂台的战力排名
            # dark_street_rank = self.mm.get_obj_tools('dark_street_rank')
            # score = self.mm.dark_street.make_score(self.level, self.mm.dark_street.get_def_combat())
            # score = self.mm.dark_street.get_def_combat()
            # dark_street_rank.add_rank(self.uid, score)
            # 更新等级排行榜
            level_rank = self.mm.get_obj_tools('level_rank')
            level_rank.add_rank(self.uid, self.level)
            # 激活限时等级礼包
            level_gift_config = game_config.level_gift
            for _lv in xrange(cur_level + 1, self.level + 1):
                # 升级送道具
                hero_exp_config = game_config.player_level.get(_lv, {})
                add_mult_gift(self.mm, hero_exp_config.get('gifts', []))

                if _lv not in level_gift_config:
                    continue
                self.level_gift[_lv] = {
                    'expire': int(time.time()) + level_gift_config[_lv].get('time', 24) * 3600,
                    'status': 0,
                }
                # if not game_config.level_gift[_lv]['buy']:
                #     self.level_gift[_lv]['status'] = 1

            # 新手引导处理
            if cur_level < 10 <= self.level:
                for gid in [13, 14]:
                    guide_ids = game_config.get_guide_mapping(gid)
                    if guide_ids and gid not in self.guide:
                        self.guide[gid] = guide_ids[-1]

            # if self.guide:
            #     cur_guide_sort = max(self.guide)
            #     while True:
            #         guide_team_config = game_config.guide_team.get(cur_guide_sort)
            #         if not guide_team_config:
            #             break
            #         if guide_team_config['type'] != 1:    #如果是弱引导，直接给玩家完成
            #             open_level = guide_team_config['open_level']
            #             if self.level > open_level + 1:
            #                 guide_ids = game_config.get_guide_mapping(cur_guide_sort)
            #                 if guide_ids:
            #                     self.guide[cur_guide_sort] = guide_ids[-1]
            #                 else:
            #                     self.guide[cur_guide_sort] = 0
            #         cur_guide_sort += 1
            # 增加科技点重置点
            # self.mm.tech_tree.incr_all_point(level)
            # 上传uc玩家数据
            send_role_data_uc(self)

        kwargs = {
            'old_exp': cur_exp,
            'cur_exp': self.exp,
            'old_lv': cur_level,
            'cur_lv': self.level,
            'change_type': 'EXP',  # 级别经验类型 玩家经验、等级
        }
        gift = []
        for i in xrange(cur_level +1 , self.level + 1):
            level_gift = game_config.player_level.get(i, {}).get('award')
            gift.extend(level_gift)
        add_mult_gift(self.mm, gift)
        special_bdc_log(self, sort='exp_change', **kwargs)
        special_bdc_log(self, sort='level_change', **dict(kwargs, change_type='PLE'))
        return True

    def can_buy_level_gift(self, level_id):
        if level_id not in self.level_gift:
            return 0   # 可充值
        if self.level_gift[level_id]['status'] != 0:
            return 11   # 已充值
        now = int(time.time())
        if now > self.level_gift[level_id]['expire'] :
            return 12   # 已过期
        return 0

    def level_gift_red_dot(self):
        now = int(time.time())
        for lv, level_gift_dict in self.level_gift.items():
            expire = level_gift_dict.get('expire', 0)
            status = level_gift_dict.get('status', 0)
            if now <= expire or status == 1:
                return True
        return False

    def add_player_exp_for_config(self, action_id, times=1):
        """
        根据动作id，增加战队经验
        :param action_id: action_exp配置id
        :param times: 次数
        :return:
        """
        gifts = []
        action_exp = game_config.action_exp.get(action_id, {}).get('action_exp', 0)
        action_coin = game_config.action_exp.get(action_id, {}).get('action_coin', 0)
        if action_exp:
            add_exp = action_exp * times
            gifts.append([17, 0, add_exp])
        if action_coin:
            add_coin = action_coin * times
            gifts.append([1, 0, add_coin])

        return gifts

    def add_team_skill_exp(self, exp):
        """ 增加战队技能经验
        :param exp:
        :return:
        """
        self.team_skill_exp += int(exp)
        self.mm.team_skill.add_team_skill_exp(exp)
        self.mm.team_skill.save()

    def is_team_skill_enough(self, silver):
        """ 战队技能经验是否足够

        :param silver:
        :return:
        """
        return self.team_skill_exp >= int(silver)

    def send_level_mail(self, min_lv, max_lv):
        """
        发送等级奖励邮件
        :param min_lv: 升级前等级
        :param max_lv: 升级后等级
        :return:
        """
        level_mail_mapping = game_config.get_level_mail_mapping()
        is_save = False

        level_mail_list = set()
        for lv in xrange(min_lv + 1, max_lv + 1):
            if lv not in level_mail_mapping:
                continue
            level_mail_list.update(level_mail_mapping[lv])

        for level_mail_id in level_mail_list:
            if level_mail_id in self.level_mail_done:
                continue
            level_mail_config = game_config.level_mail.get(level_mail_id)
            if not level_mail_config:
                continue
            content = game_config.get_language_config(MUITL_LAN[self.language_sort])[level_mail_config['des']]
            title = game_config.get_language_config(MUITL_LAN[self.language_sort])[level_mail_config['name']]
            gift = level_mail_config['reward']
            mail_dict = self.mm.mail.generate_mail(content, title=title, gift=gift)
            self.mm.mail.add_mail(mail_dict, save=True)
            self.level_mail_done.append(level_mail_id)
            is_save = True

        if is_save:
            self.save()

    def check_build(self, unlock_build_id):
        """
        检查建筑物是否解锁
        :param unlock_build_id:
        :return:
        """
        if unlock_build_id in self.unlock_build:
            return True
        else:
            return False

    def add_guild_invite(self, gid, msg_dict):
        """
        增加公会邀请信息
        :param gid:
        :param msg_dict: {'uid': '', 'name': u'', 'gname': u''}
        :return:
        """
        if gid not in self.guild_invite:
            self.guild_invite[gid] = msg_dict
            return True

        return False

    def del_guild_invite(self, gid, is_save=False):
        """
        删除公会邀请信息
        :param gid:
        :param is_save:
        :return:
        """
        if gid in self.guild_invite:
            self.guild_invite.pop(gid)
            if is_save:
                self.save()
            return True

        return False

    def add_opera_awards(self, reward_id):
        """
        记录剧情领奖
        :param reward_id:
        :return:
        """
        if reward_id not in self.opera_awards:
            self.opera_awards.append(reward_id)

    def get_opera_awards(self):
        """
        剧情领奖记录
        :return:
        """
        return self.opera_awards

    def ban_user(self, ban, ban_expire, ban_time=None, uname=u'', ban_reason=u''):
        """
        封号
        :return:
        """
        self.is_ban = ban
        self.ban_reason = ban_reason
        self.ban_expire = ban_expire
        self.ban_time = int(time.time()) if ban_time is None else ban_time
        self.ban_person = uname

    def get_ban_info(self):
        '''获取封禁信息
        returns:
            - 如果未封禁，返回False
            - 如果已封禁，返回封禁理由
        '''
        ban_info_message = BAN_INFO_MESSAGE
        if self.is_ban == 0:
            return False
        if 0 < self.ban_expire < time.time():
            return False
        if self.ban_expire == 0:
            msg_expire = ban_info_message['forever']
        else:
            msg_expire = ban_info_message['expire'].format(datetime.datetime.fromtimestamp(int(self.ban_expire)))
        if self.ban_reason:
            msg_reason = ban_info_message['reason'].format(self.ban_reason)
        else:
            msg_reason = ban_info_message['no_reason']
        info_with_qq = ban_info_message['basic_end'].format(getattr(settings, 'GM_QQ', 783837240))
        return u'{}{}{}{}'.format(ban_info_message['basic_start'],
                                  msg_reason, msg_expire,
                                  info_with_qq)

    def get_banip_info(self, uip):
        '''获取封禁信息
        returns:
            - 如果未封禁，返回False
            - 如果已封禁，返回封禁理由
        '''
        if uip in game_config.ban_ip:
            ban_expire = game_config.ban_ip[uip]['expire']
            ban_reason = game_config.ban_ip[uip]['reason']
            if '0' < ban_expire < time.strftime("%Y-%m-%d %H:%M:%S") or ban_expire == '':
                return False
            ban_info_message = BAN_INFO_MESSAGE
            if ban_expire == '0':
                msg_expire = ban_info_message['forever']
            else:
                msg_expire = ban_info_message['expire'].format(ban_expire)
            if ban_reason:
                msg_reason = ban_info_message['reason'].format(ban_reason)
            else:
                msg_reason = ban_info_message['no_reason']
            info_with_qq = ban_info_message['basic_end'].format(getattr(settings, 'GM_QQ', 583052846))
            return u'{}{}{}{}'.format(ban_info_message['basic_start'],
                                      msg_reason, msg_expire,
                                      info_with_qq)
        else:
            return False

    def is_ban_chat(self):
        """
        是否禁言
        :return:
        """
        if self.ban_chat == 0:
            return False

        if 0 < self.bchat_expire < time.time():
            return False

        return True

    def bchat_user(self, ban, ban_expire, ban_time=None, uname=u'', ban_reason=u''):
        """
        禁言
        :return:
        """
        self.ban_chat = ban
        self.bchat_reason = ban_reason
        self.bchat_expire = ban_expire
        self.bchat_time = int(time.time()) if ban_time is None else ban_time
        self.bchat_person = uname

    def get_max_point_buy_times(self):
        """
        获取体力最大购买次数
        :return:
        """
        # privilege_obj = self.mm.get_event('privilege')
        # max_point_buy_times = privilege_obj.max_point_buy_times()
        # return max_point_buy_times
        return vip_company.buy_point(self)

    def finish_guide(self):
        """
        跳过新手引导
        :return:
        """
        value = {}

        for k, v in game_config.guide.iteritems():
            sort = v['sort']
            if sort not in value:
                value[sort] = k
            elif value[sort] < k:
                value[sort] = k

        old_guide = copy.deepcopy(self.guide)
        self.guide.update(value)
        if old_guide == self.guide:
            return False

        return True

    def check_guide_done(self,guide_id):
        guide_step = self.guide.get(guide_id, 0)
        config = game_config.guide.get(guide_step, {})
        if not config:
            return 0
        return config['aim']


    def send_vip_daily_reward(self):
        """
        vip每日礼包
        :return:
        """
        if self.vip_daily_reward:
            return

        vip_config = game_config.vip.get(self.vip, {})
        gifts = vip_config.get('vip_daily_reward', [])
        if not gifts:
            return

        mail_dict = self.mm.mail.generate_mail(
            i18n_msg.get(33, self.mm.user.language_sort),
            title=i18n_msg.get(33, self.mm.user.language_sort),
            gift=gifts,
        )
        self.mm.mail.add_mail(mail_dict)
        self.vip_daily_reward = True
        self.save()

    def send_vip_exclusive_notice(self):
        """
        vip专属通知
        :return:
        """
        if settings.ENV_NAME in ['ios_inreview'] or self.vip_exclusive_notice or self.vip < 8:
            return

        mail_dict = self.mm.mail.generate_mail(
            i18n_msg.get(40, self.mm.user.language_sort),
            title=i18n_msg.get(39, self.mm.user.language_sort),
        )
        self.mm.mail.add_mail(mail_dict)
        self.vip_exclusive_notice = True
        self.save()

    def send_system_mail(self):
        """
        发送系统邮件
        :return:
        """
        notify_save = False
        now_new = time.strftime('%F %T')
        login_config = sorted(game_config.login_reward_id.iteritems(), key=lambda x: x[0])
        if not login_config:
            return

        for k, v in login_config:
            if self.login_reward_id.get(k, 0):
                continue

            level = v.get('level', [])
            if level and not level[0] <= self.level <= level[1]:
                continue

            vip = v.get('vip', [])
            if vip and not vip[0] <= self.vip <= vip[1]:
                continue

            uid_list = v.get('uid_list', [])
            if uid_list and self.uid not in uid_list:
                continue

            server = v.get('server', [])
            if server and self._server_name not in server and 'all' not in server:
                continue

            if v.get('time_format', 0) == 1 and self.config_type == 1:
                server_open_time = serverM.get_server_config(self._server_name)['open_time']
                time_count_down = relative_activity_remain_time(server_open_time, v['open'], v['close'])
                if not time_count_down:
                    continue

            elif v.get('time_format', 0) == 2 and self.config_type == 2:
                # 在有效时间内
                if not v['open'] <= now_new <= v['close']:
                    continue
            else:
                continue
            des = game_config.get_language_config(MUITL_LAN[self.language_sort])[v['des']]
            title = game_config.get_language_config(MUITL_LAN[self.language_sort])[v['title']]
            message = self.mm.mail.generate_mail(des, title, v['reward'], url=v['url'])
            self.mm.mail.add_mail(message, save=False)
            self.login_reward_id[k] = self.login_reward_id.get(k, 0) + 1
            notify_save = True

        if notify_save:
            self.save()
            self.mm.mail.save()

    def new_server(self):
        """
        判断是否新服
        1   新服
        2   老服
        :return:
        """
        return self.config_type == 1

    def server_opening_time_info(self):
        """获取开服时间相关
        """
        today = datetime.datetime.today()
        today_str = today.strftime('%F')
        server_opening_award_expire = self.SERVER_OPENING_AWARD_EXPIRE
        server_open_time = serverM.get_server_config(self._server_name)['open_time']
        open_time = datetime.datetime.fromtimestamp(server_open_time)
        close_time = open_time + datetime.timedelta(days=server_opening_award_expire - 1)

        open_times_str = open_time.strftime('%F')
        close_time_str = close_time.strftime('%F')
        return {'open_time': open_times_str,  # 开服时间
                'close_time': close_time_str,  # 开服奖励结束时间
                'open_days': (today.date() - open_time.date()).days + 1,  # 此服已开天数
                'opening_award_expired': not open_times_str <= today_str <= close_time_str,  # 开服奖励是否过期
                }

    def has_vip_gift(self):
        """是否有未购买的vip礼包"""
        for i in xrange(0, self.vip + 1):
            if i in self.vip_gift:
                continue
            return True

        return False

    def rebate_recharge(self):
        """
        公测返利
        :return:
        """
        return

        server_id = settings.get_server_num(self._server_name)
        if server_id not in [1, 2, 3]:
            return

        if self.rebate_flag:
            return

        money = game_config.rebate_recharge.get(self.account, {}).get('money', 0)
        if not money:
            return

        title = i18n_msg.get(37, self.language_sort)
        des = i18n_msg.get(38, self.language_sort)
        mail_dict = self.mm.mail.generate_mail(
            des,
            title=title,
            gift=[[2, 0, int(money * 20)]]
        )
        self.mm.mail.add_mail(mail_dict)

        self.add_vip_exp(int(money * 10))

        self.rebate_flag = True

        self.save()

    def init_build(self):
        save = False
        if not self._build:
            for build_id, value in game_config.building.iteritems():
                if value['default']:
                    self.add_build(build_id, value['field_id'], save=False)
                    save = True
        if save:
            self.save()

    # @building
    def add_build(self, build_id, field_id, save=True):
        if build_id in self._build:
            return
        self._build[build_id] = {'field_id': field_id,
                                 'build_time': int(time.time())}
        if save:
            self.save()

    @property
    def group_ids(self):
        _group_ids = {}
        config = game_config.building
        for build_id, value in self._build.iteritems():
            group = config[build_id]['group']
            _group_ids[group] = {'build_id': build_id,
                                 'field_id': value['field_id'],
                                 'lock_status': self.mm.user.level < config[build_id]['unlock_lv'],
                                 'build_status': self.get_build_status(build_id)
                                 }
        return _group_ids

    @property
    def get_pos_info(self):
        pos_info = {}
        for build_id, value in self._build.iteritems():
            pos_info[value['field_id']] = build_id
        return pos_info

    # 检查城建建筑
    def check_build_id(self, build_id):
        config = game_config.building
        if build_id not in config:
            return 1  # 配置错误
        group = config[build_id]['group']
        if group not in self.group_ids:
            return 2  # 还未拥有建筑
        if build_id in self._build:
            return 3  # 已拥有建筑
        return 0

    def up_build(self, build_id, is_save=False):
        config = game_config.building
        group_id = config[build_id]['group']
        if group_id not in self.group_ids:
            return 1  # 请先建造建筑
        old_build_id = self.group_ids[group_id]['build_id']
        self._build[build_id] = self._build[old_build_id]
        self._build[build_id]['build_time'] = int(time.time())
        self._build.pop(old_build_id)
        if is_save:
            self.save()

    def build_get_fans_activity(self, build_id):
        for key, value in game_config.fans_activity.iteritems():
            if value['build_id'] == build_id:
                return key
        return 0

    def get_build_status(self, build_id):
        fans_activity_id = self.build_get_fans_activity(build_id)
        if not fans_activity_id:
            return -1
        return self.mm.fans_activity.activety_status(fans_activity_id)

    def can_unlock(self, build_id):
        if build_id in game_config.get_functional_building_mapping():
            config = game_config.get_functional_building_mapping()[build_id]
            lvlup_condition = config['lvlup_condition']
            for tp, num in lvlup_condition:
                func = globals()['lvlup_condition_%s' % tp]
                stats = func(self.mm, num)
                if stats:
                    return stats
        elif build_id in game_config.building:
            config = game_config.building[build_id]
            func = globals()['lvlup_condition_%s' % 1]  # 1 为等级限制
            stats = func(self.mm, config['unlock_lv'])
            if stats:
                return stats
        else:
            return 201 # 没有配置
        return 0

    @property
    def build_effect(self):
        """
        1:战斗属性加成（[type,rate],属性，加成百分比）
        2:公司事务恢复速度（秒）
        3:外出拍摄金币收益（万分比）
        4:全服金榜额外金币（group_rank，绝对值）
        5:世界循环赛额外收益 （block_rank, 万分比）
        6:抽取剧本cd减少（秒）
        7:储藏室食品栏数量
        8:持续收益增加比例（万分比）
        9:艺人会所艺人数量上限
        :return: 
        """
        effect = {}
        config = game_config.get_functional_building_mapping()
        # 艺人会所艺人上限与食品栏上限初始值
        effect[7] = game_config.common[76]
        effect[9] = game_config.common[75]
        for build_id in self._build:
            if build_id not in config:
                continue
            build_effect = config[build_id]['build_effect'] if config[build_id]['build_effect'] else 0
            b_effect_type = config[build_id]['effect_type']
            if b_effect_type == 1:
                if b_effect_type not in effect:
                    effect[b_effect_type] = {}
                for effect_type, effect_num in build_effect:
                    effect[b_effect_type][effect_type] = effect.get(b_effect_type, {}).get(effect_type, 0) + effect_num
            elif b_effect_type in [7, 9]:
                effect[b_effect_type] = build_effect
            elif b_effect_type in [10, 11, 12, 13, 14]:
                effect[b_effect_type] = build_effect
            else:
                effect[b_effect_type] = effect.get(b_effect_type, 0) + build_effect
        return effect


class OnlineUsers(ModelTools):
    """
    活跃玩家
    """
    ONLINE_USERS_PREFIX = 'online_users'
    DELETED_USER_PREFIX = 'deleted_users'    # redis 中 存放已经删除的用户的key

    ONLINE_USERS_TIME_RANGE = 5 * 60  # 判断用户在线的时间参考
    FORMAT = '%Y%m%d'

    def __init__(self, uid='', server='', *args, **kwargs):
        super(OnlineUsers, self).__init__()
        self._key = self.make_key(self.ONLINE_USERS_PREFIX, server_name=server)
        self.redis = self.get_redis_client(server)
        self.server_name = server

    def deleted_user_key(self):
        return '%s_%s' % (self.DELETED_USER_PREFIX, self.server_name)

    def get_deleted_uids(self):
        return self.redis.zrange(self.deleted_user_key(), 0, -1, withscores=False)

    def update_deleted_status(self, uid, ts=None):
        """
        存储已经删除的用户的记录
        :param ts:
        :return:
        """
        self.redis.zadd(self.deleted_user_key(), **{uid: ts or int(time.time())})

    def get_online_key(self):
        """

        :return:
        """
        return self._key

    def get_online_user_count(self):
        """
        获取在线人数
        :return:
        """
        now = int(time.time())
        return self.redis.zcount(self._key, now - self.ONLINE_USERS_TIME_RANGE, now)

    def backup_online_user_count(self, count=0, today=None):
        """
        备份在线人数
        :return:
        """
        count = count or self.get_online_user_count()
        today = today or datetime.datetime.today()

        online_key = '%s_%s_%s' % (self._key, 'backup', today.strftime(self.FORMAT))
        if count:
            self.redis.hset(online_key, today.strftime('%H:%M'), count)
            self.redis.expire(online_key, 24 * 3600 * 7)

    def get_recent_online_info(self, today=None):
        today = today or datetime.datetime.today()
        online_key = '%s_%s_%s' % (self._key, 'backup', today.strftime(self.FORMAT))
        return self.redis.hgetall(online_key)

    def update_online_status(self, uid, ts=None):
        """
        更新用户在线状态
        :param uid:
        :param ts:
        :return:
        """
        self.redis.zadd(self._key, **{uid: ts or int(time.time())})

    def get_uids_by_active_days(self, active_days=0):
        """
        按登录时间获取所有用户
        :param active_days: -1: 当天登录过
                            0: 不限制
                            >0: 最近多少天登录过
        :return:
        """
        today = datetime.datetime.now().date()
        start_ts = int(time.mktime(today.timetuple()))
        end_ts = int(time.time())

        if not active_days:
            start_ts = 0
        elif active_days > 0:
            start_ts -= 3600 * 24 * active_days

        return self.redis.zrangebyscore(self._key, start_ts, end_ts)

    def get_user_count_by_active_days(self, active_days=0):
        """
        按登录时间获取用户人数
        :param active_days: -1: 当天登录过
                            0: 不限制
                            >0: 最近多少天登录过
        :return:
        """
        today = datetime.datetime.now().date()
        start_ts = int(time.mktime(today.timetuple()))
        end_ts = int(time.time())

        if not active_days:
            start_ts = 0
        elif active_days > 0:
            start_ts -= 3600 * 24 * active_days

        return self.redis.zcount(self._key, start_ts, end_ts)

    def get_user_by_start_end(self, start, end, withscore=False):
        """
        获取活跃用户
        :param start:
        :param end:
        :return:
        """
        return self.redis.zrevrange(self._key, start, end, withscores=withscore)

    def get_all_online_count(self, server_name=''):
        """
        获取所有在线人数
        :param server_name:
        :return:
        """
        if not server_name:
            return self.redis.zcard(self._key)
        else:
            r = self.get_redis_client(server_name)
            key = self.make_key(self.ONLINE_USERS_PREFIX, server_name=server_name)
            return r.zcard(key)

    def get_online_uids(self):
        """
        获取在线用户
        :return:
        """
        now = int(time.time())
        return self.redis.zrevrangebyscore(self._key, now, now - self.ONLINE_USERS_TIME_RANGE, withscores=True)

    def uid_exists(self, uid):
        """
        判断uid是否存在
        :return:
        """
        return self.redis.zrank(self._key, uid) is not None

    def get_online_uids_by_num(self, num):
        """
        获取当前在线的几个人
        :param num:
        :return:
        """
        return self.redis.zrange(self._key, -num, -1)


class CheckinUsers(ModelTools):
    """
    每日活跃玩家
    """
    USERS_CHECKIN_PREFIX = 'checkin_users'

    def __init__(self, uid='', server='', *args, **kwargs):
        super(CheckinUsers, self).__init__()
        # self._key = self.make_key(self.ONLINE_USERS_PREFIX, server_name=self.SERVER_NAME)
        self.server_name = server
        self.redis = self.get_redis_client(self.server_name)

    def get_users_checkin_key(self, str_date=None):
        """
        每日活跃玩家的key
        :param str_date:
        :return:
        """
        str_date = str_date or time.strftime('%Y%m%d')
        key = '%s_%s' % (self.USERS_CHECKIN_PREFIX, str_date)
        return self.make_key(key, server_name=self.server_name)

    def update_checkin_status(self, uid):
        """
        更新用户当天在线状态
        :param uid:
        :param ts:
        :return:
        """
        key = self.get_users_checkin_key()
        self.redis.hset(key, uid, int(time.time()))

    def get_checkin_user_count(self, str_date=None):
        """
        获取每日活跃人数
        :param ts:
        :return:
        """
        key = self.get_users_checkin_key(str_date)
        return self.redis.hlen(key)

    def get_checkin_user(self, str_date=None, withscores=False):
        """
        获取每日活跃玩家
        :param ts:
        :return:
        """
        key = self.get_users_checkin_key(str_date)

        if withscores:
            return self.redis.hgetall(key).items()
        else:
            return self.redis.hkeys(key)


class RegistUsers(ModelTools):
    """
    每日注册玩家
    """
    USERS_REGIST_PREFIX = 'regist_users'

    def __init__(self, uid='', server='', *args, **kwargs):
        super(RegistUsers, self).__init__()
        self._key = self.make_key(self.USERS_REGIST_PREFIX, server_name=server)
        self.redis = self.get_redis_client(server)

    def get_regist_time_key(self):
        """

        :return:
        """
        return self._key

    def update_regist_status(self, uid, ts=None):
        """
        更新用户注册
        :param uid:
        :param ts:
        :return:
        """
        self.redis.zadd(self._key, **{uid: ts or int(time.time())})

    def get_register_count(self, start_ts=None, end_ts=None, only_count=False, withscores=False):
        """
        获取某天的注册用户数
        :param start_ts:
        :param end_ts:
        :param only_count:
        :return:
        """
        if end_ts is None:
            end_ts = time.time()
        if start_ts is None:
            today = datetime.datetime.now().date()
            start_ts = int(time.mktime(today.timetuple()))

        if only_count:
            return self.redis.zcount(self._key, start_ts, end_ts)
        else:
            return self.redis.zrangebyscore(self._key, start_ts, end_ts, withscores=withscores)

    def get_all_regist_count(self, server_name=''):
        """
        获取所有注册人数
        :param server_name:
        :return:
        """
        if not server_name:
            return self.redis.zcard(self._key)
        else:
            r = self.get_redis_client(server_name)
            key = self.make_key(self.USERS_REGIST_PREFIX, server_name=server_name)
            return r.zcard(key)

    def get_today_new_uids(self, t_ts=None, end_ts=None, only_count=False, withscores=True):
        """
        获取当天新增用户
        :param t_ts: 起始时间戳
        :param only_count: 只返回总数
        :return:
        """
        r = self.redis
        if t_ts is None:
            today = datetime.datetime.now().date()
            t_ts = int(time.mktime(today.timetuple()))
        # 删除前两天的注册信息
        # r.zremrangebyscore(self.USERS_REGIST_PREFIX, 0, t_ts - 3600 * 24 * 2)
        end_ts = end_ts or time.time()
        if only_count:
            return r.zcount(self._key, t_ts, end_ts)
        else:
            return r.zrangebyscore(self._key, t_ts, end_ts, withscores=withscores)


class GSMessage(object):
    """ 玩家反应的客服问题相关信息
    """
    PAGE_NUM = 20
    TABLE_COUNT = 1

    def __init__(self):
        self.last_info = ""
        self.last_info_ts = ""
        self.host_config = settings.GS_HOST
        self.table_prefix = self.host_config['table_prefix']
        self.conn = MySQLdb.connect(
            host=self.host_config['host'],
            user=self.host_config['user'],
            passwd=self.host_config['passwd'],
            db=self.host_config['db'],
            charset="utf8"
        )
        self.cursor = self.conn.cursor()

    def __enter__(self, ):
        return self

    def __del__(self, ):
        self.conn.close()
        self.cursor.close()

    def add_msg(self, user, msg, msg_type):
        """
        kwargs:
        | user_id          | varchar(32)  | YES  |     | NULL    |                |
        | vip_level        | int(32)      | YES  |     | 0       |                |
        | platform         | varchar(32)  | YES  |     | 0       |                |
        | msg_type         | int(12)      | YES  |     | 0       |消息类型 1:意见 2: bug反馈 3:举报
        | msg              | varchar(255) | YES  |     | NULL    |                |
        | status           | int(12)      | YES  |     | 0       |回复状态 0:未回复 1:已回复
        #| gs_name          | varchar(32)  | YES  |     | NULL    |                |
        #| reply_title      | varchar(255) | YES  |     | NULL    |                |
        #| last_update_date | int(32)      | YES  |     | NULL    |                |
        | ask_time         | varchar(32)  | NO   |     |         |                |
        #| reply_content   | varchar(200) | NO   |     |         |                |
        #| reply_time      | varchar(32)  | NO   |     |         |                |
        #| solve_status     | int(10)      | NO   |     | 0       |                |
        #| solve_time
        """
        ask_time = time_tools.strftimestamp(time.time())
        platform = user.account.split('_')[0] if user.account.split('_')[0] else ''
        data = {
            'user_id': "'" + user.uid + "'",
            'vip_level': user.vip,
            'msg': "'" + msg + "'",
            'msg_type': msg_type,
            'ask_time': "'" + ask_time + "'",
            'platform': "'" + platform + "'",
        }
        sql = "insert into %s_%s set %s" % (
            self.host_config['table_prefix'],
            "0",
            ",".join(["%s=%s" % (k, v) for k, v in data.iteritems()]),
        )
        print 'x' * 20, sql
        conn = self.get_conn()

        conn.cursor().execute(sql)
        conn.commit()

    def get_conn(self):
        """ 创建mysql连接
        """
        conn = MySQLdb.connect(
            host=self.host_config['host'],
            user=self.host_config['user'],
            passwd=self.host_config['passwd'],
            db=self.host_config['db'],
            charset="utf8"
        )
        return conn

    def select_msg(self, query_dict, page=0, order_flag=1):
        """ 获取消息
        """
        from lib.utils.debug import print_log
        page = max(page, 0)

        if order_flag:
            order = "DESC"
        else:
            order = "ASC"
        start = page * self.PAGE_NUM
        end = (page + 1) * self.PAGE_NUM
        if query_dict:
            sql = "select * from %s_%s where %s order by ID  %s limit %d, %d " % (
                self.host_config['table_prefix'],
                "0",
                " and ".join(["%s=%s" % (k, v) for k, v in query_dict.iteritems()]),
                order,
                start,
                end,
            )
        else:
            sql = "select * from %s_%s order by ID  %s limit %d, %d " % (
                self.host_config['table_prefix'],
                "0",
                order,
                start,
                end,
            )
        # print_log('----11111--', sql)
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    def select_one_msg(self, ques_id):
        """ 获取一条消息信息
        """
        if not ques_id:
            return []
        sql = "select * from %s_%s where ID=%s " % (
            self.host_config['table_prefix'],
            "0",
            ques_id,
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        # result = cursor.fetchall()
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result

    def update_one_msg(self, ques_id, data):
        """ 更新一条消息信息
        """
        from lib.utils.debug import print_log
        if not ques_id:
            return []

        data['reply_time'] = "'" + time_tools.strftimestamp(time.time()) + "'"
        data['status'] = 1
        if data['solve_status']:
            data['solve_time'] = "'" + time_tools.strftimestamp(time.time()) + "'"

        sql = "update %s_%s set %s where ID=%s " % (
            self.host_config['table_prefix'],
            "0",
            ",".join(["%s=%s" % (k, v) for k, v in data.iteritems()]),
            ques_id,
        )
        # print_log('----33333----', sql)
        conn = self.get_conn()
        conn.cursor().execute(sql)
        conn.commit()
        conn.close()

        return []

    def close_question(self, qid):
        """ 关闭问题
        """
        sql = "update %s_%s set status=1 where ID=%d" % (
            self.host_config['table_prefix'],
            "0",
            int(qid),
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def delete_question(self, qid):
        """ 删除问题
        delete from MyClass where id=1;
        """
        sql = "delete from %s_%s where ID=%d" % (
            self.host_config['table_prefix'],
            "0",
            int(qid),
        )

        conn = self.get_conn()
        conn.cursor().execute(sql)
        conn.commit()
        conn.close()

    def tables(self):
        """ 返回所有表

        :return:
        """
        for table in ['%s_%s' % (self.table_prefix, x) for x in xrange(self.TABLE_COUNT)]:
            yield table


ModelManager.register_model('user', User)
ModelManager.register_model_base_tools('online_users', OnlineUsers)
ModelManager.register_model_base_tools('checkin_users', CheckinUsers)
ModelManager.register_model_base_tools('regist_users', RegistUsers)
