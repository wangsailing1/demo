#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import time
import datetime

from gconfig import game_config
from logics.user import UserLogic
from tools.unlock_build import refresh_unlock_build
from lib.sdk_platform.sdk_uc import send_role_data_uc
from models.user import GSMessage
from models import server as serverM
from models.config import ConfigRefresh
from logics.block import Block
from logics.mission import Mission
from tools.gift import del_mult_goods, add_mult_gift
from logics.fans_activity import FansActivity



def main(hm):
    """ 主场景请求

    :param hm: HandlerManager
    :return:
    """
    mm = hm.mm
    tpid = hm.get_argument('tpid', 0, is_int=True)
    # 英雄互娱给的 渠道id, 0为母包，母包不上线
    if not mm.user.tpid and tpid:
        mm.user.set_tpid(tpid)

    ul = UserLogic(mm)

    # 记录在线时间
    online_users = mm.get_obj_tools('online_users')
    online_users.update_online_status(mm.user.uid)

    # 用户每日最后登录时间记录
    checkin_users = mm.get_obj_tools('checkin_users')
    checkin_users.update_checkin_status(mm.user.uid)

    # 每天登陆激活普通签到
    # mm.gift_center.enter_game()

    # 刷新解锁建筑物
    refresh_unlock_build(mm)
    mm.fans_activity.check_unlock_build()

    # 触发通关任务
    task_event_dispatch = mm.get_event('task_event_dispatch')
    task_event_dispatch.call_method('daily_login')

    # # vip每日礼包
    # mm.user.send_vip_daily_reward()

    # vip专属通知
    # mm.user.send_vip_exclusive_notice()

    # 全服邮件
    mm.user.send_system_mail()
    mm.limit_sign.is_open()
    mm.server_limit_sign.is_open()


    result = ul.main()

    fa = FansActivity(mm)
    _, fans_data = fa.fans_index()

    # 配置更新
    config_refresh, _, config_refresh_text = ConfigRefresh.check()
    result['config_refresh'] = 0 if mm.user.level < 6 else config_refresh
    result['config_refresh_text'] = config_refresh_text
    result['award_ceremony'] = mm.block.award_ceremony
    result['get_award_ceremony'] = mm.block.get_award_ceremony
    result['has_ceremony'] = mm.block.has_ceremony
    result['ceremony_remain_time'] = mm.block.get_remain_time()
    mission = Mission(mm)
    result['box_office'] = mission.mission_index(2)['box_office']
    result['new_guide'] = mission.mission_index(7)['new_guide']
    result['phone_daily_times'] = mm.friend.phone_daily_times
    result['appointment_times'] = mm.friend.appointment_times
    # result['tourism_times'] = mm.friend.tourism_times
    result['seven_login'] = mm.seven_login.is_open()
    result['fans_activity_info'] = mm.fans_activity.fans_activity_info()
    result['fans_activity_data'] = {k: {'remian_time': v['remian_time'], 'items': [i for i in v['items'] if i[2] != 0]}
                                    for k, v in fans_data['activity_log'].iteritems()}

    return 0, result


def npc_info(hm):
    """
    主城npc信息
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)
    rc, data = ul.npc_info()

    return rc, data


def get_daily_and_activity(hm):
    """
    竞技和挑战的次数等
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)

    data = ul.get_daily_and_activity()

    return 0, data


def get_red_dot(hm):
    """
    获取主页小红点
    :param hm:
    :return:
    """
    mm = hm.mm

    module_name = hm.get_argument('module_name', '')

    ul = UserLogic(mm)
    data = ul.get_red_dot(module_name)

    return 0, data


def game_info(hm):
    """ 获取用户数据

    :param hm:
    :return:
    """
    mm = hm.mm

    info = dict()

    user_info = dict(is_new=mm.user.is_new, name=mm.user.name)
    info.update(**user_info)

    info.update(dict(cards=mm.card.cards, pieces=mm.card.pieces))
    info.update(dict(equips=mm.equip.equips, equip_pieces=mm.equip.equip_pieces))
    info.update(dict(own_script=mm.script.own_script))
    info.update(dict(directors=mm.director.directors))

    # item_info = dict(item=mm.item.items, gitem=mm.grade_item.items,
    #                  citem=mm.coll_item.items, ggitem=mm.guild_gift_item.items,
    #                  aitem=mm.awaken_item.items, )
    item_info = dict(item=mm.item.items)
    # block = Block(mm)
    # block.check_has_ceremony()
    # block.count_cup(is_save=True)
    info.update(**item_info)
    info['card_attr'] = mm.card.attr
    info['skip_dialouge'] = mm.user.skip_dialouge
    info['chapter_stage'] = {'chapter': mm.chapter_stage.chapter,
                             'next_chapter': mm.chapter_stage.next_chapter,
                             'top_income': mm.script.top_all.get('finished_summary', {}).get('income', 0)}
    info['training_room'] = mm.card.training_room

    return 0, info


def person_doc(hm):
    """ 个人档案

    :param hm:
    :return:
    """
    mm = hm.mm

    info = dict()

    info['arena_point'] = mm.arena.point

    return 0, info


def guide(hm):
    """ 新手引导

    :param hm:
    :return:
    """
    mm = hm.mm

    guide_team = hm.get_argument('guide_team', is_int=True)
    guide_id = hm.get_argument('guide_id', is_int=True)
    skip = hm.get_argument('skip', is_int=True)
    sort = hm.get_argument('sort', is_int=True)
    # 前端容错
    if not guide_team:
        guide_team = sort

    ul = UserLogic(mm)
    rc, data = ul.guide(guide_team, guide_id, skip)

    return rc, data


def dialogue(hm):
    mm = hm.mm
    dialogue_id = hm.get_argument('dialogue_id', is_int=True)
    mm.user.dialogue.append(dialogue_id)
    mm.user.save()
    return 0, {}


def blacklist(hm):
    """
    黑名单首页
    """
    mm = hm.mm

    ul = UserLogic(mm)
    data = ul.blacklist()

    return 0, data


def blacklist_add(hm):
    """
    添加黑名单
    """
    mm = hm.mm

    user_id = hm.get_argument('user_id')

    if not user_id:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.blacklist_add(user_id)

    if rc != 0:
        return rc, {}

    return 0, data


def blacklist_delete(hm):
    """
    移除黑黑名单
    """
    mm = hm.mm

    user_id = hm.get_argument('user_id')

    if not user_id:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.blacklist_delete(user_id)

    if rc != 0:
        return rc, {}

    return 0, data


def player_info(hm):
    """
    获取用户信息
    :param hm:
    :return:
    """
    mm = hm.mm

    user_id = hm.get_argument('user_id')
    flag = hm.get_argument('flag', is_int=True)  # 标志，1：巅峰战力榜，2：天梯排行榜，3：关卡星级榜

    if not user_id:
        return 'error_100', {}

    ul = UserLogic(mm)
    data = ul.player_info(user_id, flag)

    return 0, data


def talk_npc(hm):
    """
    和npc谈话
    :param hm:
    :return:
    """
    mm = hm.mm

    npc_id = hm.get_argument('npc_id', is_int=True)
    word_id = hm.get_argument('word_id', is_int=True)

    if npc_id <= 0 or word_id <= 0:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.talk_npc(npc_id, word_id)

    return rc, data


def exchange_currency(hm):
    """ 兑换币种

    :param hm:
    :return:
    """
    mm = hm.mm

    ce_id = hm.get_argument('ce_id', is_int=True)
    num = hm.get_argument('num', is_int=True)

    if num <= 0:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.exchange_currency(ce_id, num)
    if rc != 0:
        return rc, {}

    return 0, data


def receive_player_exp(hm):
    """
    领取战队经验储值
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)
    rc, data = ul.receive_player_exp()
    if rc != 0:
        return rc, {}

    return 0, data


def buy_privilege_gift(hm):
    """ 购买特权礼包

    :param hm:
    :return:
    """
    mm = hm.mm
    gift_id = hm.get_argument('gift_id', is_int=True)

    ul = UserLogic(mm)
    rc, data = ul.buy_privilege_gift(gift_id)
    if rc != 0:
        return rc, {}

    return 0, data


def register_name(hm):
    """起名字

    :param hm:
    :return:
    """
    mm = hm.mm

    name = hm.get_argument('name', mm.uid)
    role = hm.get_argument('role', 1, is_int=True)

    ul = UserLogic(mm)
    rc, data = ul.register_name(name, role)
    if rc != 0:
        return rc, {}
    return 0, data


def charge_name(hm):
    """ 改名字

    :param hm:
    :return:
    """
    mm = hm.mm
    name = hm.get_argument('name', mm.uid)

    if not name:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.charge_name(name)
    if rc != 0:
        return rc, {}

    return 0, data


def buy_point(hm):
    """
    购买体力
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)
    rc, data = ul.buy_point()

    if rc != 0:
        return rc, {}

    return 0, data


def opera_awards_index(hm):
    """
    剧情奖励index
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)
    data = ul.opera_awards_index()

    return 0, data


def receive_opera_awards(hm):
    """
    领取剧情奖励
    :param hm:
    :return:
    """
    mm = hm.mm

    reward_id = hm.get_argument('reward_id')

    if not reward_id:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.receive_opera_awards(reward_id)

    if rc != 0:
        return rc, {}

    return 0, data


def top_rank(hm):
    """ 最强排行
        sort: 'combat': 总战力榜, 'level': 战队等级榜, 'single_hero': 单英雄战力榜,
              'high_ladder': 天梯排行榜, 'home_flower': 家园花朵榜,
              'guild_level': 公会等级榜, 'private_city_star': 关卡星级榜,
        page: 页面默认为0, 首页

        -1: 没有该类排行榜

    :param env:
    :return:
    """
    mm = hm.mm
    NEW_RANK_KEY = {'combat', 'endless', 'level', 'single_hero', 'high_ladder', 'home_flower', 'guild_level',
                    'private_city_star',
                    'decisive_battle', 'dark_street', 'big_world_power', 'king_of_song_rank'}

    sort = hm.get_argument('sort', '')
    page = hm.get_argument('page', is_int=True)
    num = hm.get_argument('num', default=20, is_int=True)

    if sort not in NEW_RANK_KEY:
        return -1, {}  # 没有该类排行榜

    if page < 0:
        page = 0

    ul = UserLogic(mm)
    rc, data = ul.top_rank(page, num, sort)

    if rc != 0:
        return rc, {}

    return 0, data


def show_hero_detail(hm):
    """
    查看单英雄战力排行榜
    :param hm:
    :return:
    """
    mm = hm.mm

    uid = hm.get_argument('uid')
    hero_oid = hm.get_argument('hero_oid')

    if not uid or not hero_oid:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.show_hero_detail(uid, hero_oid)

    if rc != 0:
        return rc, {}

    return 0, data


def buy_vip_gift(hm):
    """
    购买特权礼包
    :param hm:
    :return:
    """
    mm = hm.mm

    vip = hm.get_argument('vip', is_int=True)

    if vip < 0:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.buy_vip_gift(vip)

    if rc != 0:
        return rc, {}

    return 0, data


def level_award(hm):
    """
    等级礼包领取奖励
    :param hm:
    :return:
    """
    mm = hm.mm

    lv = hm.get_argument('lv', is_int=True)

    if lv <= 0:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.level_award(lv)
    if rc != 0:
        return rc, {}

    return 0, data


def get_player_icon(hm):
    """
    获取解锁的头像
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)
    data = ul.get_player_icon()

    return 0, data


def unlock_icon(hm):
    mm = hm.mm

    icon = hm.get_argument('icon', is_int=True)
    if icon <= 0:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.set_got_icon(icon)

    if rc != 0:
        return rc, {}

    return 0, data


def change_icon(hm):
    """
    更换头像
    :param hm:
    :return:
    """
    mm = hm.mm

    icon = hm.get_argument('icon', is_int=True)
    if icon <= 0:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.change_icon(icon)

    if rc != 0:
        return rc, {}

    return 0, data


def title_index(hm):
    """
    称号首页
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)
    rc, data = ul.title_index()

    return rc, data


def set_title(hm):
    """
    更换称号
    :param hm:
    :return:
    """
    mm = hm.mm

    title = hm.get_argument('title', is_int=True)  # 称号id
    down = hm.get_argument('down', is_int=True)  # 是否卸下称号，1:卸下，其他不处理

    if title <= 0:
        return 'error_100', {}

    ul = UserLogic(mm)
    rc, data = ul.set_title(title, down)

    return rc, data


def buy_silver_index(hm):
    """
    点金手index
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)

    data = ul.buy_silver_index()

    return 0, data


def buy_silver(hm):
    """
    购买金币
    :param hm:
    :return:
    """
    mm = hm.mm

    ul = UserLogic(mm)

    rc, data = ul.buy_silver()

    if rc != 0:
        return rc, {}

    return 0, data


def gs_msg(hm):
    """
    客服接口
    """
    mm = hm.mm
    msg = hm.get_argument('msg', '')
    msg_type = hm.get_argument('msg_type', is_int=True)  # 1:意见 2: bug反馈 3:举报

    now = int(time.time())
    if now - mm.user.last_add_gs_msg < 20:
        return 1, {}  # 您提出的建议太频繁了, 请稍后再提

    if len(msg) > 100:
        return 2, {}  # 建议在100个字符内

    gs_message = GSMessage()
    gs_message.add_msg(mm.user, msg, msg_type)
    mm.user.last_add_gs_msg = now
    mm.user.save()

    return 0, {}


def player_detail(hm):
    """
    查看玩家详情
    :param hm:
    :return:
    """
    mm = hm.mm

    player_id = hm.get_argument('player_id')

    if not player_id:
        return 'error_100', {}

    ul = UserLogic(mm)

    rc, data = ul.player_detail(player_id)

    if rc != 0:
        return rc, {}

    return 0, data


def slg_index(hm):
    """
    slg开启条件
    :param hm:
    :return:
    """
    slg_open_remain_days = 2  # 开服几天后开启slg
    hours = 12

    # config_id = 143
    # config = game_config.value.get(config_id, {}).get('value', [2, 12])
    config = game_config.slg_server_addr.get(hm.mm.server, {}).get('open_time', [3, 12])
    if isinstance(config, list):
        slg_open_remain_days = config[0]
        hours = config[1]
    elif isinstance(config, int):
        slg_open_remain_days = config

    mm = hm.mm
    now = datetime.datetime.now()
    server_open_time = serverM.get_server_config(mm.user._server_name)['open_time']
    server_open_date = datetime.datetime.fromtimestamp(server_open_time)
    server_open_date = server_open_date.replace(hour=0, minute=0, second=0)

    slg_open_date = server_open_date + datetime.timedelta(days=slg_open_remain_days, hours=hours)

    config = game_config.building_unlock.get(SLG_BIG_WORLD, {})
    expire = int(max(0, (slg_open_date - now).total_seconds()))

    if mm.user._server_name == 'gt1':
        expire = 0

    data = {
        'expire': expire,
        'level': config.get('unlock_limit', 100)
    }
    return 0, data


def user_info(hm):
    mm = hm.mm
    all_info = mm.script.count_info()
    ar = mm.get_obj_tools('output_rank')
    data = {'group_info': mm.script.get_scrip_info_by_num(is_type=2),
            'script_info': mm.script.get_scrip_info_by_num(),
            'end_level': all_info['end_level'],
            'style_log': all_info['style_log'],
            'type_log': all_info['type_log'],
            'cup': mm.block.cup_log,
            'block_num': mm.block.block_num,
            'rank': ar.get_rank(mm.uid),
            'chapter': mm.chapter_stage.get_now_stage(),
            'cup_log_card': mm.block.cup_log_card,
            'cup_log_script': mm.block.cup_log_script}
    return 0, data


def build(hm):
    mm = hm.mm
    build_id = hm.get_argument('build_id', is_int=True)
    field_id = hm.get_argument('field_id', is_int=True)
    if not build_id or not field_id:
        return 4, {}  # 参数错误
    build_status = mm.user.check_build_id(build_id)
    if build_status and build_status != 2:
        return build_status, {}
    config = game_config.building[build_id]
    if field_id != config['field_id']:
        return 5, {}  # 地块错误
    group_id = config['group']
    # unlock_config = game_config.homepage_button
    # unlock_lv = 0
    # for value in unlock_config.values():
    #     if value['group'] == group_id:
    #         unlock_lv = value['unlock_lvl']
    #         break
    stats = mm.user.can_unlock(build_id)
    if stats:
        return stats, {}  # 不能解锁
    cost = config['cost']
    rc, _ = del_mult_goods(mm, cost)
    if rc:
        return rc, {}
    mm.user.add_build(build_id,field_id)
    return 0, {'build_effect': mm.user.build_effect,
               'group_id': group_id}

def up_build(hm):
    mm = hm.mm
    build_id = hm.get_argument('build_id', is_int=True)
    if not build_id:
        return 4, {}  # 参数错误
    build_status = mm.user.check_build_id(build_id)
    if build_status and build_status != 3:
        return build_status, {}
    config = game_config.building[build_id]
    next_id = config['next_id']
    if not next_id:
        return 5, {}  # 已到达最大等级
    stats = mm.user.can_unlock(next_id)
    if stats:
        return stats, {}  # 不能解锁
    next_config = game_config.building[next_id]
    cost = next_config['cost']
    rc, _ = del_mult_goods(mm, cost)
    if rc:
        return rc, {}
    if config['group'] == 22:
        if not mm.user.get_company_vip_red_dot():
            return 6, {}  # 未达到升级条件
        mm.user.company_vip += 1
        mm.gift_shop.add_vip_goods()  # 刷新礼包商店vip商品
        mm.resource_shop.add_vip_goods()  # 刷新资源商店vip商品
    mm.user.up_build(next_id, is_save=True)
    return 0, {'group_id': config['group'],
               'build_effect': mm.user.build_effect}


def get_company_vip_reward(hm):
    mm = hm.mm
    company_vip = hm.get_argument('company_vip', 1, is_int=True)
    config = game_config.vip_company
    if company_vip not in config:
        return 3, {}  # vip等级错误
    if company_vip > mm.user.company_vip:
        return 1, {}  # vip等级未达到
    if company_vip in mm.user.company_vip_reward:
        return 2, {}  # 礼包已领取
    reward = add_mult_gift(mm,config[company_vip]['reward'])
    mm.user.company_vip_reward.append(company_vip)
    mm.user.save()
    return 0, {'reward': reward}


def can_buy_level_gift(hm):
    mm = hm.mm
    level_id = hm.get_argument('lv', is_int=True)
    if not level_id:
        return 1 , {}  # 等级礼包id错误
    rc =  mm.user.can_buy_level_gift(level_id)
    level_gift_data = mm.user.level_gift
    return 0, {'level_limit_gift':level_gift_data,
               'level_flag': rc}


def gift_award(hm):
    """登录有奖
    args:
        award_id: reward_gift奖励配置id
    """
    award_id = hm.get_argument('award_id', is_int=True)
    mm = hm.mm

    userL = UserLogic(mm)
    config = game_config.reward_gift.get(award_id)
    if not config:
        return 1, {}    # 没这个奖励的配置

    if not userL.has_gift_award(award_id):
        return 2, {}    # 没这个奖励的配置

    reward = userL.get_gift_award(award_id, config)

    return 0, {
        'reward': reward,
    }
