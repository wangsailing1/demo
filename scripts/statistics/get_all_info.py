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
    info_log = kwargs.get('info_log') or get_bi_logger_by_type('info')

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
        'level': user.level,
        'diamond_free': user.diamond_free,
        'diamond_charge': user.diamond_charge,
        'coin': user.coin,
        'silver': user.silver,
        'silver_ticket': user.silver_ticket,
        'diamond_ticket': user.diamond_ticket,
        'dark_coin': mm.user.dark_coin,
        'challenge': mm.user.challenge,
        'guide': user.guide,
        'uuid': user.uuid,  # 设备唯一标识
        'combat': mm.hero.get_max_combat(),
        'server': user._server_name,
        'father_server': settings.get_father_server(user._server_name),
        'ip': user.register_ip,
        'appid': user.package_appid,
        'create_date': create_date_str,
    }

    info_log.info(json.dumps(data, separators=[',', ':']))

    # info_log.info('{uid}\t{account}\t{name}\t{platform}\t{device}\t{reg_time}\t{act_time}\t'
    #               '{vip}\t{level}\t{diamond}\t{coin}\t{silver}\t{privileges}\t{create_date}\t'.format(**data))


def hero(mm, **kwargs):
    """ 英雄信息

    :param mm:
    :return:
    """
    from lib.utils import timelib

    heros = mm.hero.heros

    hero_log = kwargs.get('hero_log') or get_bi_logger_by_type('hero')
    for hero_oid in heros:
        hero_dict = heros[hero_oid]
        hero_aquire_time = int(hero_oid.split('-')[1])
        hero_aquire_time = datetime.datetime.fromtimestamp(hero_aquire_time).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'user_id': mm.uid,
            'act_time': timelib.timestamp_to_datetime_str(mm.user.active_time),
            'hero_aquire_time': hero_aquire_time,
            'hero_id': hero_dict['id'],
            'hero_oid': hero_oid,
            'level': hero_dict['lv'],
            'star': hero_dict['star'],
            'evo': hero_dict['evo'],
            'is_awaken': hero_dict['is_awaken'],
            'combat': hero_dict['combat'],
            'milestone': hero_dict['milestone'],
            'equip_pos': hero_dict['equip_pos'],
            'hp': hero_dict.get('hp', 0),
            'phy_atk': hero_dict.get('phy_atk', 0),
            'phy_def': hero_dict.get('phy_def', 0),
            'mag_atk': hero_dict.get('mag_atk', 0),
            'mag_def': hero_dict.get('mag_def', 0),
            'skill': hero_dict.get('skill', {}),
            'extra_skill': hero_dict.get('extra_skill', {}),
            'create_date': create_date_str,
        }

        hero_log.info(json.dumps(data, separators=[',', ':']))
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

    equip_log = kwargs.get('equip_log') or get_bi_logger_by_type('equip')
    for eid in mm.equip.equips:
        equip_dict = mm.equip.equips[eid]
        aquire_time = int(eid.split('-')[1])
        aquire_time = datetime.datetime.fromtimestamp(aquire_time).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'user_id': mm.uid,
            'act_time': timelib.timestamp_to_datetime_str(mm.user.active_time),
            'aquire_time': aquire_time,
            'equip_id': equip_dict['id'],
            'grade': equip_dict['grade'],
            'quality': equip_dict['quality'],
            'init_lv': equip_dict['init_lv'],
            'level': equip_dict.get('lv', 0),
            'owner': equip_dict.get('owner', '-').split('-', 1)[0],
            'base': equip_dict.get('base', []),  # 基础
            'extra': equip_dict.get('extra', []),  # 附加属性
            'refined_property': equip_dict.get('refined_property', None),  # 洗练的属性,extra下标
            'st_lv': equip_dict.get('st_lv', 0),  # 精炼等级
            'refine_count': equip_dict.get('refine_count', 0),
            'create_date': create_date_str,
        }

        equip_log.info(json.dumps(data, separators=[',', ':']))
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

    all_loggers = dict(
        info_log=get_bi_logger_by_type('info'),
        hero_log=get_bi_logger_by_type('hero'),
        equip_log=get_bi_logger_by_type('equip'),
        item_log=get_bi_logger_by_type('item'),
        stones_log=get_bi_logger_by_type('stones'),
    )
    act_uids = act_user.get_act_all_user(today=today)
    for uid in act_uids:
        try:
            mm = ModelManager(uid)
            u = mm.user
        except:
            continue

        for func in (info, bdc_user_info, hero, equip, item, stones):
            try:
                func(mm, **all_loggers)
            except:
                traceback.print_exc()
                continue

    bdc_charge_info(today=today)
    # bdc_realtime_info(today=today)

    create_zip_file('userinfo', create_day)
    create_zip_file('chargeinfo', create_day)


if __name__ == "__main__":
    settings.set_env(env)

    main()
