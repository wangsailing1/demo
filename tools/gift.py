#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from collections import Counter

from lib.utils import weight_choice
from lib.utils import add_dict
from gconfig import game_config
from return_msg_config import i18n_msg
from gconfig import get_str_words


def calc_gift(gift_config, num=3):
    ''' 计算整合多个奖励配置, 如[[5, 0, 15], [5, 0, 1], [1, 23, 2], [1, 23, 4]]
        相同项合并，结果为[[5, 0, 16], [1, 23, 6]]

    >>> calc_gift([[5, 0, 15], [5, 0, 1], [1, 23, 2], [1, 23, 4]])
    [[5, 0, 16], [1, 23, 6]]
    '''
    q = Counter()
    nl = range(num)
    for i in gift_config:
        q.update({tuple([i[x] for x in nl[:-1]]): i[nl[-1]]})
    return [[i[0][j] for j in range(num - 1)] + [i[-1]] for i in q.iteritems()]


def add_mult_gift_by_weights(mm, gift_config, cur_data=None):
    """ 获取随机礼包多项奖励

    :param mm:
    :param gift_config:
    :param cur_data:
    :param save:
    :return:
    """
    cur_data = cur_data if cur_data is not None else {}
    if not gift_config:
        return cur_data
    _gift_config = weight_choice(gift_config)
    return add_mult_gift(mm, [_gift_config[:-1]], cur_data=cur_data)


def add_gift_by_weights(mm, gift_sort, gift_config, cur_data=None):
    """ 获取随机礼包

    :param mm:
    :param gift_sort:
    :param gift_config:
    :param cur_data:
    :param save:
    :return:
    """
    cur_data = cur_data if cur_data is not None else {}
    if not gift_config:
        return cur_data
    _gift_config = weight_choice(gift_config)
    return add_gift(mm, gift_sort, [_gift_config[:-1]], cur_data=cur_data)

def check_item_enough(func):
    def wrapper(mm,gift_config,*args,**kwargs):
        config =game_config.use_item
        add_food_num = 0
        for item in gift_config:
            if item[0] == 3 and config[item[1]]['type'] == 2:
                add_food_num += item[2]
        if mm.item.check_food_enough(add_food_num):
            return 'error_food_enough'
        data = func(mm,gift_config,*args,**kwargs)
        return data
    return wrapper

def add_mult_gift(mm, gift_config, cur_data=None,source=0):
    """ 获取统一多项奖励

    :param mm:
    :param gift_config: [[类型, id, 数量]], [[类型, id, 数量, 权重]]
    :param cur_data:
    :param source:  来源 1 代表充值
    :param save:
    :return:
    """
    data = cur_data if cur_data is not None else {}
    if not gift_config:
        return data

    for pkg in gift_config:
        sort = pkg[0]
        add_gift(mm, sort, [pkg[1:]], cur_data=data,source=source)

    return data


"""
    1: "coin",          # 金币
    2: "diamond",       # 钻石
    3: "item",          # 道具
    4: "dollar"         # 美元
    5: "item"           # 道具
    6: "equip"          # 装备
    7: "like"           # 点赞
    8: "cards"          # 艺人
    9: "pieces"         # 艺人碎片
    10:
    11: "exp"           # 玩家经验
    12: "guild_coin"    # 公会资金
    13: ""              # 公会贡献
    14: "vip_exp"       # vip经验
    19:关注度
    

"""


def add_gift(mm, gift_sort, gift_config, cur_data=None,source=0):
    """ 获取统一奖励

    :param mm:
    :param gift_sort: 奖励类型
                1   金币
                2   钻石
                3   体力
                4   美元
                5   道具(礼物)
                6   资产(装备)
                7   点赞
                8   艺人
                9   艺人碎片
                10  装备碎片
                11  玩家经验
                12  公会资金
                13  公会贡献
                14  VIP经验
                15
                16 点赞
                17
                18  艺人名片
                996 艺人经验
                997 好感
                998 味道(1=酸,2=甜,3=苦,4=辣,5=冰,6=饮)
                999 类型经验(包括喜剧片经验、动作片经验、选秀类经验⋯⋯)
    :param gift_config: [[id, 数量]], [[id, 数量, 权重]]
    :param cur_data:
    :return:
    """
    data = cur_data if cur_data is not None else {}

    if gift_sort == 1:  # 金币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_coin(add_coin)
            add_dict(data, 'coin', add_coin)
        mm.user.save()
    elif gift_sort == 2:  # 钻石
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_diamond(add_num)
            add_dict(data, 'diamond', add_num)
        mm.user.save()
    elif gift_sort == 3:  # 体力
        for pkg in gift_config:
            add_point = pkg[1]
            if not add_point:
                continue
            mm.user.add_action_point(add_point, force=True)
            add_dict(data, 'point', add_point)
        mm.user.save()
    elif gift_sort == 4:  # 美元
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_dollar(add_num)
            add_dict(data, 'dollar', add_num)
        mm.user.save()
    elif gift_sort == 5:  # 道具
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            stats = mm.item.add_item(item_id, item_num)
            if not stats:
                add_dict(data.setdefault('item', {}), item_id, item_num)
                mm.item.save()
            else:
                add_dict(data.setdefault('mail_food_enough', {}), item_id, item_num)
                mm.mail.save()
    elif gift_sort == 6:  # 装备（资产）
        for pkg in gift_config:
            equip_id = pkg[0]
            num = pkg[1]
            if not num:
                continue
            mm.equip.add_equip(equip_id, num)
            add_dict(data.setdefault('equip', {}), equip_id, num)
        mm.equip.save()
    elif gift_sort == 7:  # 点赞数
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_like(add_num)
            add_dict(data, 'like', add_num)
        mm.user.save()
    elif gift_sort == 8:  # 艺人
        for pkg in gift_config:
            hero_id = pkg[0]
            hero_num = pkg[1]
            if not hero_num:
                continue
            for i in xrange(hero_num):
                status = mm.card.add_card(hero_id,source=source)
                if isinstance(status, bool) and status:
                    card_config = game_config.card_basis.get(hero_id)
                    p_num = card_config['star_cost'] if source == 1 else card_config['star_giveback']
                    add_dict(data.setdefault('pieces', {}), card_config['piece_id'],
                             p_num)
                elif not isinstance(status, bool):
                    data.setdefault('cards', []).append(status)
        mm.card.save()
    elif gift_sort == 9:  # 卡牌碎片
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            mm.card.add_piece(item_id, item_num)
            add_dict(data.setdefault('pieces', {}), item_id, item_num)
        mm.card.save()
    elif gift_sort == 10:  # 装备碎片
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            mm.equip.add_piece(item_id, item_num)
            add_dict(data.setdefault('equip_pieces', {}), item_id, item_num)
        mm.equip.save()
    elif gift_sort == 11:  # 玩家经验
        for pkg in gift_config:
            num = pkg[1]
            if not num:
                continue
            mm.user.add_player_exp(num)
            add_dict(data, 'exp', num)
        mm.item.save()
    elif gift_sort == 12:  # 公会资金
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_guild_coin(add_coin)
            add_dict(data, 'guild_coin', add_coin)
        mm.user.save()
    elif gift_sort == 13:  # 公会贡献
        pass

    elif gift_sort == 14:  # vip经验
        for pkg in gift_config:
            add_exp = pkg[1]
            if not add_exp:
                continue
            mm.user.add_vip_exp(add_exp)
            add_dict(data, 'vip_exp', add_exp)
        mm.user.save()

    elif gift_sort == 15:  # 获得可拍摄剧本
        save = False
        for pkg in gift_config:
            script_id = pkg[0]
            if not script_id:
                continue
            stats = mm.script.add_own_script(script_id)
            save = save or stats
            if stats:
                data.setdefault('own_script', []).append(script_id)
        if save:
            mm.script.save()

    if gift_sort == 16:  # 点赞
        for pkg in gift_config:
            add_like = pkg[1]
            if not add_like:
                continue
            mm.user.add_like(add_like)
            add_dict(data, 'like', add_like)
        mm.user.save()

    elif gift_sort == 18:  # 增加艺人名片
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not mm.friend.check_actor(item_id):
                mm.friend.actors[item_id] = {'show': 1, 'chat_log': {}, }
                add_dict(data.setdefault('actors', {}), item_id, item_num)
        mm.friend.save()

    elif gift_sort == 19:  # 关注度
        for pkg in gift_config:
            add_type = pkg[0]
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_attention(add_type,add_num)
            add_dict(data.setdefault('attention', {}), add_type, add_num)
        mm.user.save()

    elif gift_sort == 20:  # 卡牌人气
        for pkg in gift_config:
            add_type = pkg[0]
            add_num = pkg[1]
            if not add_num:
                continue
            mm.card.add_card_popularity(add_type,add_num)
            add_dict(data.setdefault('popularity', {}), add_type, add_num)
        mm.card.save()

    elif gift_sort == 21:  # 导演
        for pkg in gift_config:
            director_id = pkg[0]
            director_num = pkg[1]
            if not director_num:
                continue
            status = mm.director.add_director(director_id)
            if not status:
                continue
            data.setdefault('directors', []).append(status)
        mm.director.save()

    elif gift_sort == 102:  # 成就点
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.mission.add_achieve_point(add_num)
            add_dict(data, 'achieve', add_num)
        mm.mission.save()

    elif gift_sort == 101:  # 目标点
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.mission.add_liveness(add_num)
            add_dict(data, 'liveness', add_num)
        mm.mission.save()

    elif gift_sort == 103:  # 业绩
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.mission.add_performance(add_num)
            add_dict(data, 'performance', add_num)
        mm.mission.save()

    # elif gift_sort == 10:  # 公会经验, 需要在调用地方单独加, 有些逻辑多个用户操作公会数据
    #     for pkg in gift_config:
    #         guild_exp = pkg[1]
    #         if not guild_exp:
    #             continue
    #         add_dict(data, 'guild_exp', guild_exp)

    return data


def del_mult_goods(mm, goods_config):
    """
    统一删除物品
    :param mm:
    :param goods_config: [[类型, id, 数量]]
    :return:
    """
    all_silver = 0
    for pkg in goods_config:
        sort = pkg[0]
        rc, silver_count = del_goods(mm, sort, [pkg[1:]])
        if rc != 0:
            return rc, 0
        all_silver += silver_count

    return 0, all_silver


def del_goods(mm, goods_sort, goods_config):
    """ 删除物品

    :param mm:
    :param item_sort: 物品类型
    :param item_config: [[id, 数量]]
    :return:
    """
    silver_count = 0
    if goods_sort == 1:  # 金币
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_coin_enough(del_coin):
                return 'error_coin', 0
            mm.user.deduct_coin(del_coin)
        mm.user.save()
    elif goods_sort == 2:  # 钻石
        for pkg in goods_config:
            del_num = pkg[1]
            if not mm.user.is_diamond_enough(del_num):
                return 'error_diamond', 0
            mm.user.deduct_diamond(del_num)
        mm.user.save()
    elif goods_sort == 3:  # 体力
        for pkg in goods_config:
            del_point = pkg[1]
            if not mm.user.decr_action_point(del_point):
                return 'error_point', 0
        mm.user.save()
    elif goods_sort == 4:  # 美元
        for pkg in goods_config:
            del_num = pkg[1]
            if not mm.user.is_dollar_enough(del_num):
                return 'error_dollar', 0
            mm.user.deduct_dollar(del_num)
        mm.user.save()
    elif goods_sort == 5:  # 道具
        for pkg in goods_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not mm.item.del_item(item_id, item_num):
                return 'error_item', 0
            item_config = game_config.use_item.get(item_id, {})
            if not item_config:
                return 'error_config', 0
        mm.item.save()
    elif goods_sort == 6:  # 装备 资产
        for pkg in goods_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not mm.equip.del_equip(item_id, item_num):
                return 'error_equip', 0
    elif goods_sort == 7:  # 点赞
        for pkg in goods_config:
            del_num = pkg[1]
            if not mm.user.is_like_enough(del_num):
                return 'error_like', 0
            mm.user.deduct_like(del_num)
        mm.user.save()
    elif goods_sort == 8:  # 减卡牌,不能删除
        return 'error_hero', 0
    elif goods_sort == 9:  # 卡牌碎片
        for pkg in goods_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not mm.card.del_piece(item_id, item_num):
                return 'error_piece', 0
        mm.card.save()
    elif goods_sort == 10:  #
        for pkg in goods_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not mm.equip.del_piece(item_id, item_num):
                return 'error_equip_piece', 0
        mm.equip.save()
    elif goods_sort == 11:  # 玩家经验
        return 'error_exp', 0
    elif goods_sort == 12:  # 公会币
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_guild_coin_enough(del_coin):
                return 'error_guild_coin', 0
            mm.user.deduct_guild_coin(del_coin)
        mm.user.save()

    elif goods_sort == 13:  # 公会贡献
        pass

    elif goods_sort == 14:  # vip经验
        pass

    elif goods_sort == 20:  # 卡牌人气
        for pkg in goods_config:
            # if not mm.card.is_enough_popularity(pkg[0], pkg[1]):
            #     return 'error_popularity', 0
            mm.card.delete_card_popularity(pkg[0], pkg[1])
        mm.card.save()

    return 0, silver_count


def has_mult_goods(mm, goods_config):
    """
    判断物品是否足够
    :param mm:
    :param goods_config: [[类型, id, 数量]]
    :return:
    """
    for pkg in goods_config:
        sort = pkg[0]
        rc = has_goods(mm, sort, [pkg[1:]])
        if not rc:
            return rc

    return True


def has_goods(mm, gift_sort, gift_config):
    """ 物品是否足够

    :param mm:
    :param gift_sort: 奖励类型
            1   银币
            2   钻石
            3   道具
            4   灵魂石
            5   采集物
            6   装备
            7   进阶材料
            8   英雄经验
            9   英雄
            10  公会经验
            11  公会礼物道具
            12  觉醒材料
            13  金币
            14  生产配方
            15  防守道具
            16  昆特牌
            17  战斗经验
            18  挑战卡
            19  能量
            20  体力
            21  黑街货币
            22  战队技能碎片
            23  公会币
            24  普通飞机票
            25  高级飞机票
            26  特殊类道具: 指定装备,英雄属性
            106 通过装备属性增加装备
    :param gift_config: [[id, 数量]], [[id, 数量, 权重]]
    :param cur_data:
    :return:
    """
    if gift_sort == 1:  # 银币
        for pkg in gift_config:
            add_silver = pkg[1]
            if not add_silver:
                continue
            if not mm.user.is_silver_enough(add_silver):
                return False
    elif gift_sort == 2:  # 钻石
        for pkg in gift_config:
            add_diamond = pkg[1]
            if not add_diamond:
                continue
            if not mm.user.is_diamond_enough(add_diamond):
                return False
    elif gift_sort == 5:  # 道具
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            if mm.item.get_item(item_id) < item_num:
                return False
    elif gift_sort == 4:  # 美元
        for pkg in gift_config:
            stone_num = pkg[1]
            if not stone_num:
                continue
            if not mm.user.is_dollar_enough(stone_num):
                return False
    # elif gift_sort == 5:  # 采集物
    #     for pkg in gift_config:
    #         citem_id = pkg[0]
    #         citem_num = pkg[1]
    #         if not citem_num:
    #             continue
    #         if mm.coll_item.get_item(citem_id) < citem_num:
    #             return False
    # elif gift_sort == 6:  # 装备
    #     return False
    elif gift_sort == 6:  # 基因
        return False

    elif gift_sort == 7:  # 进阶材料
        for pkg in gift_config:
            gitem_id = pkg[0]
            gitem_num = pkg[1]
            if not gitem_num:
                continue
            if mm.grade_item.get_item(gitem_id) < gitem_num:
                return False
    elif gift_sort == 8:  # 增加英雄经验, 需要在调用地方单独加
        return False

    elif gift_sort == 9:  # 英雄
        return False

    elif gift_sort == 10:  # 公会经验, 需要在调用地方单独加, 有些逻辑多个用户操作公会数据
        return False

    elif gift_sort == 11:  # 公会礼物道具
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            if mm.guid_gift_item.get_item(item_id) < item_num:
                return False
    elif gift_sort == 12:  # 觉醒材料
        for pkg in gift_config:
            awaken_id = pkg[0]
            awaken_num = pkg[1]
            if not awaken_num:
                continue
            if mm.awaken_item.get_item(awaken_id) < awaken_num:
                return False
    elif gift_sort == 13:  # 金币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            if not mm.user.is_coin_enough(add_coin):
                return False
    elif gift_sort == 14:  # 生产配方
        return False

    elif gift_sort == 15:  # 防守道具
        return False

    elif gift_sort == 16:  # 昆特牌
        return False

    elif gift_sort == 17:  # 战斗经验
        return False

    elif gift_sort == 18:  # 挑战卡, 血尘拉力赛
        for pkg in gift_config:
            add_challenge = pkg[1]
            if not add_challenge:
                continue
            if not mm.user.is_challenge_enough(add_challenge):
                return False
    elif gift_sort == 19:  # 能量, 战斗道具
        for pkg in gift_config:
            add_energy = pkg[1]
            if not add_energy:
                continue
            if not mm.battle_item.is_energy_enough(add_energy):
                return False
    elif gift_sort == 20:  # 体力
        for pkg in gift_config:
            add_point = pkg[1]
            if not add_point:
                continue
            if not mm.user.is_action_point_enough(add_point):
                return False
    elif gift_sort == 21:  # 黑街货币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            if not mm.user.is_dark_coin_enough(add_coin):
                return False
    elif gift_sort == 22:  # 战队技能碎片
        return False

    elif gift_sort == 23:  # 公会币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            if not mm.user.is_guild_coin_enough(add_coin):
                return False
    elif gift_sort == 24:  # 普通飞机票
        for pkg in gift_config:
            add_ticket = pkg[1]
            if not add_ticket:
                continue
            if not mm.user.is_silver_ticket_enough(add_ticket):
                return False
    elif gift_sort == 25:  # 高级飞机票
        for pkg in gift_config:
            add_ticket = pkg[1]
            if not add_ticket:
                continue
            if not mm.user.is_diamond_ticket_enough(add_ticket):
                return False
    elif gift_sort == 26:  # 特殊类道具
        return False

    elif gift_sort == 27:  # 巅峰币
        for pkg in gift_config:
            ladder_coin = pkg[1]
            if not ladder_coin:
                continue
            if not mm.user.is_ladder_coin_enough(ladder_coin):
                return False

    elif gift_sort == 28:  # vip经验
        return False

    elif gift_sort == 29:  # 觉醒宝箱碎片
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            if not mm.user.is_box_coin_enough(add_coin):
                return False

    elif gift_sort == 30:  # 荣耀币
        for pkg in gift_config:
            donate_coin = pkg[1]
            if not donate_coin:
                continue
            if not mm.user.is_donate_coin_enough(donate_coin):
                return False

    elif gift_sort == 31:  # 觉醒宝箱钥匙
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            if not mm.user.is_box_key_enough(add_coin):
                return False
    if gift_sort == 32:  # 战队技能经验
        for pkg in gift_config:
            add_team_skill_exp = pkg[1]
            if not add_team_skill_exp:
                continue
            if not mm.user.is_team_skill_enough(add_team_skill_exp):
                return False
    elif gift_sort == 34:  # 虫洞矿坑币
        for pkg in gift_config:
            wormhole_score = pkg[1]
            if not wormhole_score:
                continue
            if not mm.user.is_wormhole_score_enough(wormhole_score):
                return False
    elif gift_sort == 35:  # 占星点
        for pkg in gift_config:
            add_star_array_point = pkg[1]
            if not add_star_array_point:
                continue
            if not mm.star_array.is_star_point_enough(add_star_array_point):
                return False

    elif gift_sort == 106:  # 通过装备属性增加装备
        return False

    elif gift_sort == 38:  # 道具
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            if mm.gene.get_piece(item_id) < item_num:
                return False

    elif gift_sort == 39:  # 无尽积分
        for pkg in gift_config:
            add_diamond = pkg[1]
            if not add_diamond:
                continue
            if not mm.user.is_endless_score_enough(add_diamond):
                return False

    elif gift_sort == 40:  # 装备币
        for pkg in gift_config:
            equip_coin = pkg[1]
            if not equip_coin:
                continue
            if not mm.user.is_equip_coin_enough(equip_coin):
                return False

    elif gift_sort == 41:  # 荣誉币
        for pkg in gift_config:
            honor_coin = pkg[1]
            if not honor_coin:
                continue
            if not mm.user.is_honor_coin_enough(honor_coin):
                return False

    return True


def get_reward_and_num(mm, gifts):
    msg = ''
    lan = mm.lan
    for gift in gifts:
        _sort = gift[0]
        item_id = gift[1]
        gift_num = gift[2]
        reward = u''

        if _sort == 1:  # 金币
            reward = i18n_msg.get(1001, lan)
        elif _sort == 2:  # 钻石
            reward = i18n_msg.get(1002, lan)
        elif _sort == 3:  # 体力
            reward = i18n_msg.get(1003, lan)
        elif _sort == 4:  # 美元
            reward = i18n_msg.get(1004, lan)
        elif _sort == 5:  # 道具
            item_name = game_config.use_item[item_id]['name']
            reward = get_str_words(mm.user.language_sort, item_name)
        elif _sort == 6:  # 装备（资产）
            equip_name = game_config.equip[item_id]['name']
            reward = get_str_words(mm.user.language_sort, equip_name)
        elif _sort == 7:  # 点赞数
            reward = i18n_msg.get(1007, lan)
        elif _sort == 8:  # 艺人
            card_name = game_config.card_basis[item_id]['name']
            reward = get_str_words(mm.user.language_sort, card_name)
        elif _sort == 9:  # 卡牌碎片
            card_piece_name = game_config.card_piece[item_id]['name']
            reward = get_str_words(mm.user.language_sort, card_piece_name)
        elif _sort == 10:  # 装备碎片
            equip_piece_name = game_config.equip_piece[item_id]['name']
            reward = get_str_words(mm.user.language_sort, equip_piece_name)
        elif _sort == 11:  # 玩家经验
            reward = i18n_msg.get(1011, lan)
        elif _sort == 12:  # 公会资金
            reward = i18n_msg.get(1012, lan)
        elif _sort == 13:  # 公会贡献
            reward = i18n_msg.get(1013, lan)
        elif _sort == 14:  # vip经验
            reward = i18n_msg.get(1014, lan)
        elif _sort == 15:  # 获得可拍摄剧本
            reward = i18n_msg.get(1015, lan)
        if _sort == 16:  # 点赞
            reward = i18n_msg.get(1016, lan)
        elif _sort == 18:  # 增加艺人名片
            reward = i18n_msg.get(1018, lan)
        elif _sort == 19:  # 关注度
            reward = i18n_msg.get(1019, lan)
        elif _sort == 20:  # 卡牌人气
            reward = i18n_msg.get(1020, lan)
        elif _sort == 21:  # 导演
            director_name = game_config.director[item_id]['name']
            reward = get_str_words(mm.user.language_sort, director_name)
        elif _sort == 102:  # 成就点
            reward = i18n_msg.get(1102, lan)
        elif _sort == 101:  # 目标点
            reward = i18n_msg.get(1101, lan)

        if reward:
            msg += u'%(reward)s * %(gift_num)s ' % {'reward': reward, 'gift_num': gift_num}

    return msg