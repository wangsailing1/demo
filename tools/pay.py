#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import math


from gconfig import game_config


def coll_speed_up_cost(mm, remainder_time):
    """ 采集加速花费

    :param mm:
    :param remainder_time: 剩余时间
    :return:
    """
    value = sorted(game_config.speed_up_cost.iteritems(), key=lambda x: x[0])
    sum_cost = 0
    cost_1s = 1
    time_step = 0
    for t, value in value:
        if t > remainder_time:
            cost_1s = value['cost_1s']
            break
        time_step = t
        sum_cost = value['sum_cost']
    return int(math.ceil(sum_cost + (remainder_time - time_step) * cost_1s))


def manu_speed_up_cost(mm, remainder_time):
    """ 生产加速花费

    :param mm:
    :param remainder_time: 剩余时间
    :return:
    """
    value = sorted(game_config.speed_up_cost.iteritems(), key=lambda x: x[0])
    sum_cost = 0
    cost_1s = 1
    time_step = 0
    for t, v in value:
        if t > remainder_time:
            cost_1s = v['cost_1s']
            break
        time_step = t
        sum_cost = v['sum_cost']
    return int(math.ceil(sum_cost + (remainder_time - time_step) * cost_1s))


def coll_team_pos_cost(mm):
    """ 采集队伍花费

    :param mm:
    :return:
    """
    return 0


def get_chat_need_diamond(mm, cur_times):
    """
    获取聊天需要消耗的钻石
    :param mm:
    :return:
    """
    need_diamond = game_config.get_value(88, [10])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_shop_refresh_need_diamond(mm):
    """
    获取商店刷新商品需要消耗的钻石
    :param mm:
    :return:
    """
    cur_times = mm.shop.refresh_times
    need_diamond = game_config.get_value(29, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_exchange_shop_refresh_need_diamond(mm):
    """
    获取兑换商店刷新商品需要消耗的钻石
    :param mm:
    :return:
    """
    cur_times = mm.exchange_shop.refresh_times
    need_diamond = game_config.get_value(30, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_period_shop_refresh_need_diamond(mm):
    """
    获取限时商店刷新商品需要消耗的钻石
    :param mm:
    :return:
    """
    cur_times = mm.period_shop.refresh_times
    need_diamond = game_config.get_value(31, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_guild_shop_refresh_need_guild_coin(mm):
    """
    获取公会商店刷新商品需要消耗的公会币
    :param mm:
    :return:
    """
    cur_times = mm.guild_shop.refresh_times
    need_diamond = game_config.get_value(28, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_dark_shop_refresh_need_dark_coin(mm):
    """
    获取黑街商店刷新商品需要消耗的黑街币
    :param mm:
    :return:
    """
    cur_times = mm.dark_shop.refresh_times
    need_diamond = game_config.get_value(32, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_ladder_shop_refresh_need_ladder_coin(mm):
    """
    获取天梯商店刷新商品需要消耗的天梯币
    :param mm:
    :return:
    """
    cur_times = mm.high_ladder_shop.refresh_times
    need_diamond = game_config.get_value(69, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_wormhole_shop_refresh_need_wormhole_coin(mm):
    """
    获取虫洞矿坑商店刷新商品需要消耗的矿坑币
    :param mm:
    :return:
    """
    cur_times = mm.wormhole_shop.refresh_times
    need_diamond = game_config.get_value(111, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_equip_shop_refresh_need_equip_coin(mm):
    """
    获取装备商店刷新商品需要消耗的装备币
    :param mm:
    :return:
    """
    cur_times = mm.equip_shop.refresh_times
    need_diamond = game_config.get_value(128, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]
    
    
def get_profiteer_shop_refresh_need_coin(mm):
    """
    获取军需商店刷新商品需要消耗的钻石
    :param mm:
    :return:
    """
    cur_times = mm.profiteer_shop.refresh_times
    need_diamond = game_config.get_value(127, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_honor_shop_refresh_need_coin(mm):
    """
    获取荣誉商店刷新商品需要消耗的荣誉币
    :param mm:
    :return:
    """
    cur_times = mm.honor_shop.refresh_times
    need_diamond = game_config.get_value(140, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_donate_shop_refresh_need_coin(mm):
    """
    获取荣耀商店刷新商品需要消耗的荣耀
    :param mm:
    :return:
    """
    cur_times = mm.donate_shop.refresh_times
    need_diamond = game_config.get_value(68, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_rally_shop_refresh_need_rally_coin(mm):
    """
    获取游骑兵商店刷新商品需要消耗的挑战币
    :param mm:
    :return:
    """
    cur_times = mm.rally_shop.refresh_times
    need_diamond = game_config.get_value(20, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_darkstreet_refresh_need_diamond(mm):
    """
    获取黑街擂台刷新对手需要消耗的钻石
    :param mm:
    :return:
    """
    cur_times = mm.dark_street.refresh_times
    need_diamond = game_config.get_value(27, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_teams_chapter_need_silver(mm):
    """
    获取战队技能碎片副本挑战消耗银币
    :param mm:
    :return:
    """
    cur_times = mm.teams_chapter.battle_times
    need_silver = game_config.get_value(34, [1000])
    if cur_times >= len(need_silver):
        return need_silver[-1]
    else:
        return need_silver[cur_times]


def get_reset_dungeon_need_diamond(mm, chapter_id):
    """
    获取地城重置消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.private_city.reset_dungeon_times.get(chapter_id, 0)
    need_diamond = game_config.get_value(33, [60])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_reset_hard_need_diamond(mm, chapter_id, stage_id, degree):
    """
    获取困难地狱副本重置消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.private_city.hard_reset_times.get(chapter_id, {}).get(stage_id, {}).get(degree, 0)
    if degree > 1:
        need_diamond = game_config.get_value(33, [60])
    else:
        need_diamond = game_config.get_value(105, [60])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_buy_whip_need_diamond(mm):
    """
    获取购买皮鞭消耗钻石
    :param mm:
    :return:
    """
    cur_times = mm.prison.buy_whip_times
    need_diamond = game_config.get_value(38, [10])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_buy_tempt_need_diamond(mm):
    """
    获取购买诱惑消耗钻石
    :param mm:
    :return:
    """
    cur_times = mm.prison.buy_tempt_times
    need_diamond = game_config.get_value(39, [10])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_arena_buy_times_need_diamond(mm):
    """
    获取竞技场购买挑战次数消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.high_ladder.battle_buy_times
    need_diamond = game_config.get_value(41, [20])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_arena_refresh_enemy_need_diamond(mm):
    """
    获取竞技场刷新敌人消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.high_ladder.refresh_def_enemy_times
    need_diamond = game_config.get_value(42, [10])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_dark_street_buy_attr_need_diamond(mm):
    """
    获取竞技场刷新敌人消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.dark_street.buy_attr_times
    need_diamond = game_config.get_value(37, [20])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_dark_street_buy_point_need_diamond(mm):
    """
    黑街购买挑战券消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.dark_street.buy_point_times
    need_diamond = game_config.get_value(26, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_remove_gene_extra_need_diamond(mm, times):
    """
    移除基因附加属性消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    need_diamond = game_config.get_value(18, [100])
    if times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[times]


def get_buy_point_need_diamond(mm):
    """
    获取购买体力消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.user.buy_point_times
    need_diamond = game_config.get_value(55, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_buy_slg_point_need_diamond(mm):
    """
    获取购买行动力消耗钻石
    :param mm:
    :param chapter_id: 章节id
    :return:
    """
    cur_times = mm.big_world.buy_slg_point_times
    need_diamond = game_config.get_value(141, [30])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_rally_buy_box_need_diamond(mm, cur_times=None):
    """
    血沉购买宝箱消耗钻石
    :param mm:
    :return:
    """
    cur_times = mm.rally.box_buy_times if cur_times is None else cur_times
    need_diamond = game_config.get_value(53, [20])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_biography_buy_box_need_diamond(cur_times):
    """
    传记购买宝箱消耗钻石
    :param mm:
    :return:
    """
    need_diamond = game_config.get_value(62, [20])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_texas_need_diamond(mm, cur_times):
    """
    获取德州扑克刷新所需钻石
    :param mm:
    :return:
    """
    need_diamond = game_config.get_value(86, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_doomsday_need_diamond(mm, cur_times):
    """
    获取猛兽刷新所需钻石
    :param mm:
    :return:
    """
    need_diamond = game_config.get_value(95, [50])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_king_war_shop_refresh_need_score(cur_times):
    """
    获取斗技刷新所需钻石
    :param mm:
    :return:
    """
    need_diamond = game_config.get_value(96, [50])
    if isinstance(need_diamond, int):
        need_diamond = [need_diamond]

    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]


def get_team_skill_need_diamond(cur_times):
    """
    获取游骑兵次数购买所需钻石
    :return:
    """
    need_diamond = game_config.get_value(106, [20])
    if cur_times >= len(need_diamond):
        return need_diamond[-1]
    else:
        return need_diamond[cur_times]

