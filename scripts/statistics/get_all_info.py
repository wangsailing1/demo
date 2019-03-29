# encoding:utf-8

import os
import sys
import time
import datetime
import traceback
import json

# 设置程序使用的编码格式, 统一为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

env = sys.argv[1]

if len(sys.argv) == 3:
    arg_date = sys.argv[2]
else:
    arg_date = ''

import settings

if arg_date:
    today = datetime.datetime.strptime(arg_date, '%Y%m%d') + datetime.timedelta(days=1)
else:
    today = datetime.datetime.today()

create_day = today - datetime.timedelta(days=1)
create_date = create_day.date()
date_stamp = create_date.strftime('%Y%m%d')
create_date_str = create_date.strftime('%Y-%m-%d')

default_path = '../statistic/%s/redis_static/' % settings.ENV_NAME


def get_bi_logger_by_type(sort):
    from lib.utils.loggings import get_log, InfoLoggingUtil
    # 本地测试用
    if settings.ENV_NAME in ['song']:
        log_path = ''
    else:
        log_path = '/data/bi_data/%s/redis_static' % settings.ENV_NAME
    real_path = log_path if log_path else default_path

    return get_log('%s/%s_%s' % (real_path, sort, date_stamp), logging_class=InfoLoggingUtil, propagate=0)


mm_cache = {}


def info(mm, **kwargs):
    """ 玩家信息

    :param mm:
    :return:
    """
    from lib.utils import timelib
    from models.ranking_list import BlockRank
    info_log = kwargs.get('info_log') or get_bi_logger_by_type('info')

    block_rank_uid = mm.block.get_key_profix(mm.block.block_num, mm.block.block_group,
                                             'income')
    br = BlockRank(block_rank_uid, mm.block._server_name)
    income = br.get_score(mm.uid)
    user = mm.user

    name = str(user.name).replace('\n', '-n-', ).replace('\r', '-r-').replace('\t', '-t-')

    data = {
        'user_id': mm.uid,
        'account': user.account if user.account else 'Null',
        'tpid': user.tpid,
        'account_reg': user.account_reg if user.account else 'Null',
        'name': name if name else 'Null',
        'platform': user.channel if user.channel else 'Null',
        'device_mark': user.device,
        'reg_time': timelib.timestamp_to_datetime_str(user.reg_time),
        'act_time': timelib.timestamp_to_datetime_str(user.active_time),
        'vip': user.vip,
        'company_vip': user.company_vip,
        'sex': user.get_sex(),
        'level': user.level,
        'diamond_free': user.diamond_free,
        'diamond_charge': user.diamond_charge,
        'coin': user.coin,
        'silver': user.silver,
        # 'silver_ticket': user.silver_ticket,
        # 'diamond_ticket': user.diamond_ticket,
        # 'dark_coin': mm.user.dark_coin,
        # 'challenge': mm.user.challenge,
        'guide': user.guide,
        'uuid': user.uuid,  # 设备唯一标识
        # 'combat': mm.hero.get_max_combat(),
        'server': user._server_name,
        'father_server': settings.get_father_server(user._server_name),
        'ip': user.register_ip,
        'appid': user.package_appid,
        'dollar':user.dollar,
        'create_date': create_date_str,
        'block_num': mm.block.block_num,
        'income': income,
    }

    info_log.info(json.dumps(data, separators=[',', ':']))

    # info_log.info('{uid}\t{account}\t{name}\t{platform}\t{device}\t{reg_time}\t{act_time}\t'
    #               '{vip}\t{level}\t{diamond}\t{coin}\t{silver}\t{privileges}\t{create_date}\t'.format(**data))


def card(mm, **kwargs):
    """ 艺人信息

    :param mm:
    :return:
    """
    from lib.utils import timelib
    from gconfig import game_config
    cards = mm.card.cards
    config = game_config.card_basis
    card_log = kwargs.get('card_log') or get_bi_logger_by_type('card')
    for card_oid in cards:
        card_dict = cards[card_oid]
        card_aquire_time = int(card_oid.split('-')[1])
        card_aquire_time = datetime.datetime.fromtimestamp(card_aquire_time).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'user_id': mm.uid,
            'act_time': timelib.timestamp_to_datetime_str(mm.user.active_time),
            'card_aquire_time': card_aquire_time,
            'card_id': card_dict['id'],
            'card_oid': card_oid,
            'level': card_dict['lv'],
            'star': card_dict['star'],
            'evo': card_dict['evo'],
            'love_lv': card_dict['love_lv'],
            'love_exp': card_dict['love_exp'],
            'popularity': card_dict['popularity'],
            'train_times': card_dict['train_times'],
            'style_pro': card_dict['style_pro'],
            'equips': card_dict['equips'],
            'gift_count': card_dict['gift_count'],
            'is_cold': card_dict['is_cold'],
            'create_date': create_date_str,
            'qualityid': config[card_dict['id']]['qualityid']
        }

        card_log.info(json.dumps(data, separators=[',', ':']))
        # for index, value in hero_dict['skill'].iteritems():
        #     data['s%sid' % index] = value['s']
        #     data['s%slevel' % index] = 0 if value['avail'] == 0 else value['lv']
        #
        # hero_log.info('{uid}\t{act_time}\t{hero_aquire_time}\t{hero_id}\t{level}\t{star}\t{evo}\t{combat}\t'
        #               '{strength}\t{agility}\t{intelligence}\t{hp}\t{phy_atk}\t{phy_def}\t{mag_atk}\t{mag_def}\t'
        #               '{s1id}\t{s1level}\t{s2id}\t{s2level}\t{s3id}\t{s3level}\t{s4id}\t{s4level}\t{s5id}\t{s5level}\t'
        #               '{create_date}'.format(**data))


def equip(mm, **kwargs):
    """ 装备信息

    :param mm:
    :return:
    """
    from lib.utils import timelib
    from gconfig import game_config

    equip_log = kwargs.get('equip_log') or get_bi_logger_by_type('equip')
    act_time = timelib.timestamp_to_datetime_str(mm.user.active_time)
    config = game_config.equip
    for eid, num in mm.equip.equips.iteritems():

        if num <= 0:
            continue
        config_e_id = config[eid]
        data = {
            'user_id': mm.uid,
            'act_time': act_time,
            'item_id': eid,
            'item_num': num,
            'create_date': create_date_str,
            'star': config_e_id['star']
        }

        equip_log.info(json.dumps(data, separators=[',', ':']))
        # equip_log.info('{uid}\t{act_time}\t{aquire_time}\t{equip_id}\t{grade}\t{quality}\t{init_lv}\t'
        #                '{level}\t{owner}\t{base}\t{extra}\t{refined_property}\t{st_lv}\t'
        #                '{refine_count}\t{create_date}'.format(**data))

def card_pieces(mm, **kwargs):
    """ 艺人碎片信息

    :param mm:
    :return:
    """
    from lib.utils import timelib
    from gconfig import game_config

    card_pieces_log = kwargs.get('card_pieces_log') or get_bi_logger_by_type('card_pieces')
    act_time = timelib.timestamp_to_datetime_str(mm.user.active_time)
    config = game_config.card_piece
    for cid, num in mm.card.pieces.iteritems():
        if num <= 0:
            continue
        config_c_id = config[cid]
        data = {
            'user_id': mm.uid,
            'act_time': act_time,
            'item_id': cid,
            'item_num': num,
            'create_date': create_date_str,
            'star': config_c_id['star'],
        }

        card_pieces_log.info(json.dumps(data, separators=[',', ':']))
        # equip_log.info('{uid}\t{act_time}\t{aquire_time}\t{equip_id}\t{grade}\t{quality}\t{init_lv}\t'
        #                '{level}\t{owner}\t{base}\t{extra}\t{refined_property}\t{st_lv}\t'
        #                '{refine_count}\t{create_date}'.format(**data))

def equip_pieces(mm, **kwargs):
    """ 装备碎片信息

    :param mm:
    :return:
    """
    from lib.utils import timelib
    from gconfig import game_config

    equip_pieces_log = kwargs.get('equip_pieces_log') or get_bi_logger_by_type('equip_pieces')
    act_time = timelib.timestamp_to_datetime_str(mm.user.active_time)
    config = game_config.equip_piece
    for eid, num in mm.equip.equip_pieces.iteritems():

        if num <= 0:
            continue
        config_e_id = config[eid]
        data = {
            'user_id': mm.uid,
            'act_time': act_time,
            'item_id': eid,
            'item_num': num,
            'create_date': create_date_str,
            'star': config_e_id['star']
        }

        equip_pieces_log.info(json.dumps(data, separators=[',', ':']))
        # equip_log.info('{uid}\t{act_time}\t{aquire_time}\t{equip_id}\t{grade}\t{quality}\t{init_lv}\t'
        #                '{level}\t{owner}\t{base}\t{extra}\t{refined_property}\t{st_lv}\t'
        #                '{refine_count}\t{create_date}'.format(**data))


def item(mm, **kwargs):
    """ 道具信息

    :param mm:
    :return:
    """
    from lib.utils import timelib

    act_time = timelib.timestamp_to_datetime_str(mm.user.active_time)
    item_log = kwargs.get('item_log') or get_bi_logger_by_type('item')

    for item_name in ['item', 'grade_item', 'coll_item', 'guild_gift_item', 'awaken_item']:
        item_model = getattr(mm, item_name, None)
        if not item_model:
            continue

        for item_id, item_num in item_model.items.iteritems():
            if item_num <= 0:
                continue

            data = {
                'user_id': mm.uid,
                'act_time': act_time,
                'item_id': item_id,
                'item_num': item_num,
                'create_date': create_date_str,
            }

            item_log.info(json.dumps(data, separators=[',', ':']))
            # item_log.info('{uid}\t{act_time}\t{item_id}\t{item_num}\t{create_date}'.format(**data))


def script(mm, **kwargs):
    """ 剧本信息

    :param mm:
    :return:
    """
    from lib.utils import timelib
    from gconfig import game_config
    script = mm.script.own_script
    config = game_config.script
    script_log = kwargs.get('script_log') or get_bi_logger_by_type('script')
    for script_id in script:

        data = {
            'user_id': mm.uid,
            'act_time': timelib.timestamp_to_datetime_str(mm.user.active_time),
            'star': config.get(script_id, {}).get('star', 0),
            'script_id': script_id
        }

        script_log.info(json.dumps(data, separators=[',', ':']))


def building(mm, **kwargs):
    """ 建筑信息

    :param mm:
    :return:
    """
    from lib.utils import timelib
    from gconfig import game_config, get_str_words
    building = mm.user.group_ids
    config = game_config.building
    building_log = kwargs.get('building_log') or get_bi_logger_by_type('building')
    for group_id, info in building.iteritems():
        config_build = config.get(info.get('build_id', 0), {})
        data = {
            'user_id': mm.uid,
            'act_time': timelib.timestamp_to_datetime_str(mm.user.active_time),
            'group_id': group_id,
            'lv': config_build.get('lv', 0),
            'name': get_str_words('1', config_build.get('name', 0)),
        }

        building_log.info(json.dumps(data, separators=[',', ':']))


def stones(mm, **kwargs):
    """ 灵魂石信息

    :param mm:
    :return:
    """
    from lib.utils import timelib

    act_time = timelib.timestamp_to_datetime_str(mm.user.active_time)
    stones_log = kwargs.get('stones_log') or get_bi_logger_by_type('stones')

    for stone_id, stone_num in mm.hero.stones.iteritems():
        if stone_num <= 0:
            continue

        data = {
            'user_id': mm.uid,
            'act_time': act_time,
            'stone_id': stone_id,
            'stone_num': stone_num,
            'create_date': create_date_str,
        }

        stones_log.info(json.dumps(data, separators=[',', ':']))
        # item_log.info('{uid}\t{act_time}\t{item_id}\t{item_num}\t{create_date}'.format(**data))


def main():
    from scripts.statistics.tools import act_user
    from lib.core.environ import ModelManager
    from scripts.statistics.bdc_snapshot import (
        bdc_user_info, bdc_charge_info, bdc_realtime_info, create_zip_file
    )
    from celery_app.aliyun_bdc_log import send_bdc_log_to_aliyun


    all_loggers = dict(
        info_log=get_bi_logger_by_type('info'),
        card_log=get_bi_logger_by_type('card'),
        equip_log=get_bi_logger_by_type('equip'),
        item_log=get_bi_logger_by_type('item'),
        equip_pieces_log=get_bi_logger_by_type('equip_pieces'),
        card_pieces_log=get_bi_logger_by_type('card_pieces'),
        script_log=get_bi_logger_by_type('script'),
        building_log=get_bi_logger_by_type('building'),
    )
    bdc_user_info_contents = []
    act_uids = act_user.get_act_all_user(today=today)
    for uid in act_uids:
        print uid
        try:
            mm = ModelManager(uid)
            u = mm.user
        except:
            continue

        for func in (info, bdc_user_info, card, equip, item, equip_pieces, card_pieces, script, building):
            try:
                data = func(mm, **all_loggers)
                # 发bdc userinfo
                if func.func_name == 'bdc_user_info':
                    bdc_user_info_contents.append(data)
                    if not len(bdc_user_info_contents) % 50:
                        send_bdc_log_to_aliyun(bdc_user_info_contents)
                        bdc_user_info_contents = []
            except:
                traceback.print_exc()
                continue

    bdc_charge_info(today=today)
    # bdc_realtime_info(today=today)

    # create_zip_file('userinfo', create_day)
    # create_zip_file('chargeinfo', create_day)

    if bdc_user_info_contents:
        send_bdc_log_to_aliyun(bdc_user_info_contents)


if __name__ == "__main__":
    settings.set_env(env)

    main()
