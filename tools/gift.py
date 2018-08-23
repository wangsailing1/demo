#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from collections import Counter

from lib.utils import weight_choice
from lib.utils import add_dict
from gconfig import game_config


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


def add_mult_gift(mm, gift_config, cur_data=None):
    """ 获取统一多项奖励

    :param mm:
    :param gift_config: [[类型, id, 数量]], [[类型, id, 数量, 权重]]
    :param cur_data:
    :param save:
    :return:
    """
    data = cur_data if cur_data is not None else {}
    if not gift_config:
        return data

    for pkg in gift_config:
        sort = pkg[0]
        add_gift(mm, sort, [pkg[1:]], cur_data=data)

    return data


def add_gift(mm, gift_sort, gift_config, cur_data=None):
    """ 获取统一奖励

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
            27  天梯竞技场币种
            28  vip经验
            29  觉醒宝箱碎片
            30  荣耀币
            31  觉醒钥匙
            33  斗技商城币
            41  荣誉币
            106 通过装备属性增加装备
    :param gift_config: [[id, 数量]], [[id, 数量, 权重]]
    :param cur_data:
    :return:
    """
    data = cur_data if cur_data is not None else {}

    if gift_sort == 1:  # 银币
        for pkg in gift_config:
            add_silver = pkg[1]
            if not add_silver:
                continue
            mm.user.add_silver(add_silver)
            add_dict(data, 'silver', add_silver)
        mm.user.save()
    elif gift_sort == 2:  # 钻石
        for pkg in gift_config:
            add_diamond = pkg[1]
            if not add_diamond:
                continue
            mm.user.add_diamond(add_diamond)
            add_dict(data, 'diamond', add_diamond)
        mm.user.save()
    elif gift_sort == 3:  # 道具
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            mm.item.add_item(item_id, item_num)
            add_dict(data.setdefault('item', {}), item_id, item_num)
        mm.item.save()
    elif gift_sort == 4:  # 灵魂石
        for pkg in gift_config:
            stone_id = pkg[0]
            stone_num = pkg[1]
            if not stone_num:
                continue
            mm.hero.add_stone(stone_id, stone_num)
            add_dict(data.setdefault('stones', {}), stone_id, stone_num)
        mm.hero.save()
    elif gift_sort == 5:  # 采集物
        for pkg in gift_config:
            citem_id = pkg[0]
            citem_num = pkg[1]
            if not citem_num:
                continue
            mm.coll_item.add_item(citem_id, citem_num)
            add_dict(data.setdefault('citem', {}), citem_id, citem_num)
        mm.coll_item.save()
    # elif gift_sort == 6:  # 装备
    #     for pkg in gift_config:
    #         equip_id = pkg[0]
    #         equip_num = pkg[1]
    #         if not equip_num:
    #             continue
    #         if len(pkg) == 3:
    #             kwargs = pkg[2]
    #         else:
    #             kwargs = {}
    #         for i in xrange(equip_num):
    #             equip_oid = mm.equip.add_equip(equip_id, force=True, **kwargs)
    #             if equip_oid:
    #                 data.setdefault('equips', []).append(equip_oid)
    #     mm.equip.save()
    elif gift_sort == 6:  # 基因
        for pkg in gift_config:
            gene_id = pkg[0]
            gene_num = pkg[1]
            if not gene_num:
                continue
            if len(pkg) == 4:
                kwargs = {
                    'star': pkg[2],
                    'evo': pkg[3],
                }
            else:
                kwargs = {}
            for i in xrange(gene_num):
                gene_oid = mm.gene.add_gene(gene_id, force=True, **kwargs)
                if gene_oid:
                    data.setdefault('genes', []).append(gene_oid)
        mm.gene.save()
    elif gift_sort == 7:  # 进阶材料
        for pkg in gift_config:
            gitem_id = pkg[0]
            gitem_num = pkg[1]
            if not gitem_num:
                continue
            mm.grade_item.add_item(gitem_id, gitem_num)
            add_dict(data.setdefault('gitem', {}), gitem_id, gitem_num)
        mm.grade_item.save()
    elif gift_sort == 8:  # 增加英雄经验, 需要在调用地方单独加
        for pkg in gift_config:
            hero_exp = pkg[1]
            if not hero_exp:
                continue
            add_dict(data, 'hero_exp', hero_exp)
    elif gift_sort == 9:  # 英雄
        for pkg in gift_config:
            hero_id = pkg[0]
            hero_num = pkg[1]
            if not hero_num:
                continue
            for i in xrange(hero_num):
                status = mm.hero.add_hero(hero_id)
                if isinstance(status, bool) and status:
                    hero_config = game_config.hero_basis.get(hero_id)
                    add_dict(data.setdefault('to_stones', {}), hero_id,
                             mm.hero.get_hero_to_stone_num(hero_config))
                elif not isinstance(status, bool):
                    data.setdefault('heros', []).append(status)

        mm.hero.save()
    elif gift_sort == 10:  # 公会经验, 需要在调用地方单独加, 有些逻辑多个用户操作公会数据
        for pkg in gift_config:
            guild_exp = pkg[1]
            if not guild_exp:
                continue
            add_dict(data, 'guild_exp', guild_exp)
    elif gift_sort == 11:  # 公会礼物道具
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            mm.guid_gift_item.add_item(item_id, item_num)
            add_dict(data.setdefault('ggitem', {}), item_id, item_num)
        mm.guild_gift_item.save()
    elif gift_sort == 12:  # 觉醒材料
        for pkg in gift_config:
            awaken_id = pkg[0]
            awaken_num = pkg[1]
            if not awaken_num:
                continue
            mm.awaken_item.add_item(awaken_id, awaken_num)
            add_dict(data.setdefault('aitem', {}), awaken_id, awaken_num)
        mm.awaken_item.save()
    elif gift_sort == 13:  # 金币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_coin(add_coin)
            add_dict(data, 'coin', add_coin)
        mm.user.save()
    elif gift_sort == 14:   # 生产配方
        pass
    elif gift_sort == 15:   # 防守道具
        pass
    elif gift_sort == 16:   # 昆特牌
        for pkg in gift_config:
            gcard_id = pkg[0]
            if not gcard_id:
                continue
            mm.gwent_card.add_gcard(gcard_id)
            add_dict(data.setdefault('gcard', {}), gcard_id, 1)
        mm.gwent_card.save()
    elif gift_sort == 17:   # 战斗经验
        for pkg in gift_config:
            add_exp = pkg[1]
            if not add_exp:
                continue
            mm.user.add_player_exp(add_exp)
            add_dict(data, 'exp', add_exp)
        mm.user.save()
    elif gift_sort == 18:   # 挑战卡, 血尘拉力赛
        for pkg in gift_config:
            add_challenge = pkg[1]
            if not add_challenge:
                continue
            mm.user.add_challenge(add_challenge)
            add_dict(data, 'challenge', add_challenge)
        mm.user.save()
    elif gift_sort == 19:  # 能量, 战斗道具
        for pkg in gift_config:
            add_energy = pkg[1]
            if not add_energy:
                continue
            mm.battle_item.add_energy(add_energy)
            add_dict(data, 'energy', add_energy)
        mm.battle_item.save()
    elif gift_sort == 20:   # 体力
        for pkg in gift_config:
            add_point = pkg[1]
            if not add_point:
                continue
            mm.user.add_action_point(add_point, force=True)
            add_dict(data, 'point', add_point)
        mm.user.save()
    elif gift_sort == 21:  # 黑街货币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_dark_coin(add_coin)
            add_dict(data, 'dark_coin', add_coin)
        mm.user.save()
    elif gift_sort == 22:  # 战队技能碎片
        for pkg in gift_config:
            part_id = pkg[0]
            part_num = pkg[1]
            if not part_num:
                continue
            mm.team_skill.add_skill_part(part_id, part_num)
            add_dict(data.setdefault('team_skill_stone', {}), part_id, part_num)
        mm.team_skill.save()
    elif gift_sort == 23:  # 公会币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_guild_coin(add_coin)
            add_dict(data, 'guild_coin', add_coin)
        mm.user.save()
    elif gift_sort == 24:  # 普通飞机票
        for pkg in gift_config:
            add_ticket = pkg[1]
            if not add_ticket:
                continue
            mm.user.add_silver_ticket(add_ticket)
            add_dict(data, 'silver_ticket', add_ticket)
        mm.user.save()
    elif gift_sort == 25:  # 高级飞机票
        for pkg in gift_config:
            add_ticket = pkg[1]
            if not add_ticket:
                continue
            mm.user.add_diamond_ticket(add_ticket)
            add_dict(data, 'diamond_ticket', add_ticket)
        mm.user.save()
    elif gift_sort == 26:   # 特殊类道具
        gene_save = False
        hero_save = False
        for pkg in gift_config:
            gift_id = pkg[0]
            gift_num = pkg[1]
            if gift_num <= 0:
                continue
            item_config = game_config.special_use_item.get(gift_id, {})
            if not item_config:
                continue
            sort = item_config['sort']
            for i in xrange(gift_num):
                if sort == 1:   # 装备
                    gene_id = item_config['use_item_id']
                    kwargs = {
                        'evo': item_config['evo'],
                        'star': item_config['star'],
                        'lv': item_config['lvl'],
                    }
                    gene_oid = mm.gene.add_gene(gene_id, force=True, **kwargs)
                    # equip_oid = mm.equip.add_equip(equip_id, force=True, **kwargs)
                    if gene_oid:
                        data.setdefault('genes', []).append(gene_oid)
                        gene_save = True
                elif sort == 2:  # 英雄
                    hero_id = item_config['use_item_id']
                    status = mm.hero.add_hero(hero_id, lv=item_config['lvl'], star=item_config['star'])
                    hero_save = True
                    if isinstance(status, bool) and status:
                        hero_config = game_config.hero_basis.get(hero_id)
                        add_dict(data.setdefault('to_stones', {}), hero_id,
                                 mm.hero.get_hero_to_stone_num(hero_config))
                    elif not isinstance(status, bool):
                        data.setdefault('heros', []).append(status)
                    else:
                        hero_save = False
        if gene_save:
            mm.gene.save()
        if hero_save:
            mm.hero.save()
    elif gift_sort == 27:  # 巅峰币
        for pkg in gift_config:
            add_ladder_coin = pkg[1]
            if not add_ladder_coin:
                continue
            mm.user.add_ladder_coin(add_ladder_coin)
            add_dict(data, 'ladder_coin', add_ladder_coin)
        mm.user.save()
    elif gift_sort == 28:  # vip经验
        for pkg in gift_config:
            add_exp = pkg[1]
            if not add_exp:
                continue
            mm.user.add_vip_exp(add_exp)
            add_dict(data, 'vip_exp', add_exp)
        mm.user.save()
    elif gift_sort == 29:  # 觉醒宝箱碎片
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_box_coin(add_coin)
            add_dict(data, 'box_coin', add_coin)
        mm.user.save()
    elif gift_sort == 30:  # 荣耀币
        for pkg in gift_config:
            add_donate_coin = pkg[1]
            if not add_donate_coin:
                continue
            mm.user.add_donate_coin(add_donate_coin)
            add_dict(data, 'donate_coin', add_donate_coin)
        mm.user.save()
    elif gift_sort == 31:  # 觉醒宝箱钥匙
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_box_key(add_coin)
            add_dict(data, 'box_key', add_coin)
        mm.user.save()
    elif gift_sort == 32:  # 战队技能经验
        for pkg in gift_config:
            add_team_skill_exp = pkg[1]
            if not add_team_skill_exp:
                continue
            mm.user.add_team_skill_exp(add_team_skill_exp)
            add_dict(data, 'team_skill_exp', add_team_skill_exp)
        mm.user.save()
    elif gift_sort == 33:  # 斗技商城币
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_king_war_score(add_num)
            add_dict(data, 'king_war_score', add_num)
        mm.user.save()
    elif gift_sort == 34:  # 虫洞商城币
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_wormhole_score(add_num)
            add_dict(data, 'wormhole_score', add_num)
    elif gift_sort == 35:  # 星座点
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.star_array.add_star_point(add_num)
            add_dict(data, 'star_array_point', add_num)
        mm.star_array.save()
    elif gift_sort == 36:  # 主角技能
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            mm.role_info.add_role_skill(item_id, item_num)
            add_dict(data.setdefault('leading_skill', {}), item_id, item_num)
        mm.role_info.save()
    elif gift_sort == 37:  # 无尽币
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_endless_coin(add_coin)
            if 'endless_coin' not in data:
                data['endless_coin'] = str(add_coin)
            else:
                data['endless_coin'] = str(add_coin + int(data['endless_coin']))
            # add_dict(data, 'endless_coin', str(add_coin))
        mm.user.save()
    elif gift_sort == 106:  # 通过装备属性增加装备
        for equip_dict in gift_config:
            equip_oid = mm.equip.add_equip_by_value(equip_dict)
            if equip_oid:
                data.setdefault('equips', []).append(equip_oid)
        mm.equip.save()

    elif gift_sort == 38:  # 装备碎片
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            mm.gene.add_piece(item_id, item_num)
            add_dict(data.setdefault('gene_piece', {}), item_id, item_num)
        mm.gene.save()

    elif gift_sort == 39:  # 无尽积分
        for pkg in gift_config:
            add_coin = pkg[1]
            if not add_coin:
                continue
            mm.user.add_endless_score(add_coin)
            add_dict(data, 'endless_score', add_coin)
        mm.user.save()

    elif gift_sort == 40:  # 装备币
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_equip_coin(add_num)
            add_dict(data, 'equip_coin', add_num)

    elif gift_sort == 41:  # 荣誉币
        for pkg in gift_config:
            add_num = pkg[1]
            if not add_num:
                continue
            mm.user.add_honor_coin(add_num)
            add_dict(data, 'honor_coin', add_num)

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
    if goods_sort == 1:  # 银币
        for pkg in goods_config:
            del_silver = pkg[1]
            if not mm.user.is_silver_enough(del_silver):
                return 'error_silver', 0
            mm.user.deduct_silver(del_silver)
        mm.user.save()
    elif goods_sort == 2:  # 钻石
        for pkg in goods_config:
            del_diamond = pkg[1]
            if not mm.user.is_diamond_enough(del_diamond):
                return 'error_diamond', 0
            mm.user.deduct_diamond(del_diamond)
        mm.user.save()
    elif goods_sort == 3:  # 道具
        for pkg in goods_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not mm.item.del_item(item_id, item_num):
                return 'error_item', 0
            item_config = game_config.use_item.get(item_id, {})
            if not item_config:
                return 'error_config', 0
            silver_count += item_config.get('quality', 0) * item_num * 100
        mm.item.save()
    elif goods_sort == 4:  # 灵魂石
        for pkg in goods_config:
            stone_id = pkg[0]
            stone_num = pkg[1]
            if not mm.hero.del_stone(stone_id, stone_num):
                return 'error_stone', 0
            silver_count += stone_num * 100
        mm.hero.save()
    elif goods_sort == 5:  # 采集物
        for pkg in goods_config:
            citem_id = pkg[0]
            citem_num = pkg[1]
            if not mm.coll_item.del_item(citem_id, citem_num):
                return 'error_citem', 0
            citem_config = game_config.collection_resource
            if not citem_config:
                return 'error_config', 0
            silver_count += citem_config.get(citem_id, {}).get('quality', 0) * citem_num * 100
        mm.coll_item.save()
    # elif goods_sort == 6:  # 装备
    #     for pkg in goods_config:
    #         equip_id = pkg[0]
    #         e_id, e_dict = mm.equip.del_equip(equip_id)
    #         if not e_id:
    #             return 'error_equip', 0
    #         silver_count += e_dict['quality'] * 100
    #     mm.equip.save()
    elif goods_sort == 6:  # 基因
        for pkg in goods_config:
            gene_id = pkg[0]
            g_id, g_dict = mm.gene.del_gene(gene_id)
            if not g_id:
                return 'error_gene', 0
        mm.gene.save()
    elif goods_sort == 7:  # 进阶材料
        for pkg in goods_config:
            gitem_id = pkg[0]
            gitem_num = pkg[1]
            if not mm.grade_item.del_item(gitem_id, gitem_num):
                return 'error_gitem', 0
            gitem_config = game_config.grade_lvlup_item
            if not gitem_config:
                return 'error_config', 0
            silver_count += gitem_config.get(gitem_id, {}).get('quality', 0) * gitem_num * 100
        mm.grade_item.save()
    elif goods_sort == 8:  # 增加英雄经验, 需要在调用地方单独加
        return 'error_hero_exp', 0
    elif goods_sort == 9:  # 英雄, 英雄不能删除
        return 'error_hero', 0
    elif goods_sort == 10:  # 公会经验, 不能减
        return 'error_guild_exp', 0
    elif goods_sort == 11:  # 公会礼物道具, 不能减
        return 'error_ggitem', 0
    elif goods_sort == 12:  # 觉醒材料
        for pkg in goods_config:
            awaken_id = pkg[0]
            awaken_num = pkg[1]
            if not mm.awaken_item.del_item(awaken_id, awaken_num):
                return 'error_aitem', 0
        mm.awaken_item.save()
    elif goods_sort == 13:  # 金币
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_coin_enough(del_coin):
                return 'error_coin', 0
            mm.user.deduct_coin(del_coin)
        mm.user.save()
    elif goods_sort == 14:   # 生产配方
        pass
    elif goods_sort == 15:   # 防守道具
        pass
    elif goods_sort == 16:  # 昆特牌
        for pkg in goods_config:
            gcard_id = pkg[0]
            if not mm.gwent_card.delete_gcard(gcard_id):
                return 'error_gcard', 0
            gcard_config = game_config.card_detail.get(gcard_id, {})
            if not gcard_config:
                return 'error_config', 0
        mm.gwent_card.save()
    elif goods_sort == 17:  # 战队经验
        return 'error_exp', 0
    elif goods_sort == 18:  # 挑战卡, 血尘拉力赛
        for pkg in goods_config:
            del_challenge = pkg[1]
            if not mm.user.is_challenge_enough(del_challenge):
                return 'error_challenge', 0
            mm.user.deduct_challenge(del_challenge)
        mm.user.save()
    elif goods_sort == 19:  # 能量 战斗道具
        for pkg in goods_config:
            del_energy = pkg[1]
            if not mm.battle_item.is_energy_enough(del_energy):
                return 'error_energy', 0
            mm.battle_item.deduct_energy(del_energy)
        mm.battle_item.save()
    elif goods_sort == 20:  # 体力
        for pkg in goods_config:
            del_point = pkg[1]
            if not mm.user.decr_action_point(del_point):
                return 'error_point', 0
        mm.user.save()
    elif goods_sort == 21:  # 黑街货币
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_dark_coin_enough(del_coin):
                return 'error_dark_coin', 0
            mm.user.deduct_dark_coin(del_coin)
        mm.user.save()
    elif goods_sort == 22:  # 战队技能碎片
        for pkg in goods_config:
            part_id = pkg[0]
            part_num = pkg[1]
            if not mm.team_skill.del_part(part_id, part_num):
                return 'error_team_skill', 0
        mm.team_skill.save()
    elif goods_sort == 23:  # 公会币
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_guild_coin_enough(del_coin):
                return 'error_guild_coin', 0
            mm.user.deduct_guild_coin(del_coin)
        mm.user.save()
    elif goods_sort == 24:  # 普通飞机票
        for pkg in goods_config:
            del_ticket = pkg[1]
            if not mm.user.is_silver_ticket_enough(del_ticket):
                return 'error_silver_ticket', 0
            mm.user.deduct_silver_ticket(del_ticket)
        mm.user.save()
    elif goods_sort == 25:  # 高级飞机票
        for pkg in goods_config:
            del_ticket = pkg[1]
            if not mm.user.is_diamond_ticket_enough(del_ticket):
                return 'error_diamond_ticket', 0
            mm.user.deduct_diamond_ticket(del_ticket)
        mm.user.save()

    elif goods_sort == 27:  # 巅峰币
        for pkg in goods_config:
            del_ladder_coin = pkg[1]
            if not mm.user.is_ladder_coin_enough(del_ladder_coin):
                return 'error_ladder_coin', 0
            mm.user.deduct_ladder_coin(del_ladder_coin)
        mm.user.save()

    elif goods_sort == 28:  # vip经验
        pass

    elif goods_sort == 29:  # 觉醒宝箱碎片
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_box_coin_enough(del_coin):
                return 'error_box_coin', 0
            mm.user.deduct_box_coin(del_coin)
        mm.user.save()

    elif goods_sort == 30:  # 荣耀币
        for pkg in goods_config:
            del_donate_coin = pkg[1]
            if not mm.user.is_donate_coin_enough(del_donate_coin):
                return 'error_donate_coin', 0
            mm.user.deduct_donate_coin(del_donate_coin)
        mm.user.save()

    elif goods_sort == 31:  # 觉醒宝箱钥匙
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_box_key_enough(del_coin):
                return 'error_box_key', 0
            mm.user.deduct_box_key(del_coin)
        mm.user.save()

    elif goods_sort == 32:  # 战队技能经验
        return 'error_team_skill_exp', 0

    elif goods_sort == 33:  # 斗技商城积分
        for pkg in goods_config:
            del_king_war_score = pkg[1]
            if not mm.user.is_king_war_score_enough(del_king_war_score):
                return 'error_king_war_score', 0
            mm.user.deduct_king_war_score(del_king_war_score)
    elif goods_sort == 34:  # 虫洞商城积分
        for pkg in goods_config:
            del_wormhole_score = pkg[1]
            if not mm.user.is_wormhole_score_enough(del_wormhole_score):
                return 'error_wormhole_score', 0
            mm.user.deduct_wormhole_score(del_wormhole_score)
        mm.user.save()

    elif goods_sort == 35:  # 星座点
        for pkg in goods_config:
            del_star_array_point = pkg[1]
            if not mm.star_array.is_star_point_enough(del_star_array_point):
                return 'error_star_array_point', 0
            mm.star_array.deduct_star_point(del_star_array_point)
        mm.star_array.save()

    elif goods_sort == 37:  # 无尽币
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_endless_coin_enough(del_coin):
                return 'error_endless_coin', 0
            mm.user.deduct_endless_coin(del_coin)
        mm.user.save()

    elif goods_sort == 38:  # 装备碎片
        for pkg in goods_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not mm.gene.del_piece(item_id, item_num):
                return 'error_gene_piece', 0
        mm.gene.save()

    elif goods_sort == 39:  # 无尽积分
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_endless_score_enough(del_coin):
                return 'error_endless_score', 0
            mm.user.deduct_endless_score(del_coin)
        mm.user.save()

    elif goods_sort == 40:  # 装备币
        for pkg in goods_config:
            del_equip_coin = pkg[1]
            if not mm.user.is_equip_coin_enough(del_equip_coin):
                return 'error_equip_coin', 0
            mm.user.deduct_equip_coin(del_equip_coin)
        mm.user.save()

    elif goods_sort == 41:  # 荣誉币
        for pkg in goods_config:
            del_coin = pkg[1]
            if not mm.user.is_honor_coin_enough(del_coin):
                return 'error_honor_coin', 0
            mm.user.deduct_honor_coin(del_coin)
        mm.user.save()

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
    elif gift_sort == 3:  # 道具
        for pkg in gift_config:
            item_id = pkg[0]
            item_num = pkg[1]
            if not item_num:
                continue
            if mm.item.get_item(item_id) < item_num:
                return False
    elif gift_sort == 4:  # 灵魂石
        for pkg in gift_config:
            stone_id = pkg[0]
            stone_num = pkg[1]
            if not stone_num:
                continue
            if mm.hero.get_stone(stone_id) < stone_num:
                return False
    elif gift_sort == 5:  # 采集物
        for pkg in gift_config:
            citem_id = pkg[0]
            citem_num = pkg[1]
            if not citem_num:
                continue
            if mm.coll_item.get_item(citem_id) < citem_num:
                return False
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
    elif gift_sort == 14:   # 生产配方
        return False

    elif gift_sort == 15:   # 防守道具
        return False

    elif gift_sort == 16:   # 昆特牌
        return False

    elif gift_sort == 17:   # 战斗经验
        return False

    elif gift_sort == 18:   # 挑战卡, 血尘拉力赛
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
    elif gift_sort == 20:   # 体力
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
    elif gift_sort == 26:   # 特殊类道具
        return False

    elif gift_sort == 27:  # 巅峰币
        for pkg in gift_config:
            ladder_coin = pkg[1]
            if not ladder_coin:
                continue
            if not mm.user.is_ladder_coin_enough(ladder_coin):
                return False

    elif gift_sort == 28:   # vip经验
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
    if gift_sort == 32:     # 战队技能经验
        for pkg in gift_config:
            add_team_skill_exp = pkg[1]
            if not add_team_skill_exp:
                continue
            if not mm.user.is_team_skill_enough(add_team_skill_exp):
                return False
    elif gift_sort == 34:     # 虫洞矿坑币
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

    elif gift_sort == 40:     # 装备币
        for pkg in gift_config:
            equip_coin = pkg[1]
            if not equip_coin:
                continue
            if not mm.user.is_equip_coin_enough(equip_coin):
                return False

    elif gift_sort == 41:     # 荣誉币
        for pkg in gift_config:
            honor_coin = pkg[1]
            if not honor_coin:
                continue
            if not mm.user.is_honor_coin_enough(honor_coin):
                return False

    return True
