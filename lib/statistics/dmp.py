#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import json
import os
import copy
import time
from functools import wraps
from itertools import chain

from lib.statistics import logger_result_funcs, logger_funcs, bdc_event_funcs
from lib.utils import clear_log_dir
from lib.utils.loggings import get_log, StatLoggingUtil
from lib.utils.encoding import force_unicode
from lib.utils.debug import print_log
from lib.sdk_platform.sdk_hero import save_gold_obtain_log, save_gold_consume_log, save_item_obtain_log, \
    save_item_consume_log
from celery_app.aliyun_bdc_log import send_bdc_log_to_aliyun

import settings


path = os.path.join(settings.BASE_ROOT, 'logs/action/')
bdc_path = os.path.join(settings.BASE_ROOT, 'logs/bdc_event/')

os.system("""[ ! -d '%s' ] && mkdir -p %s"""%(path, path))
os.system("""[ ! -d '%s' ] && mkdir -p %s"""%(bdc_path, bdc_path))

clear_log_dir(path, recursion=True)
clear_log_dir(bdc_path, recursion=True)

# 需要监控的属性列表
CARDS_MONITOR_ATTRS = ['id', 'lv', 'love_lv', 'star', 'evo', 'is_cold']
EQUIP_MONITOR_ATTRS = ['id', 'lv', 'evo', 'star', 'owner', 'remove_times']

IGNORE_ARG = ['device_mk', 'platform_channel', 'pt', 'version', 'appid', 'uuid', '__ts', 'cjyx2', 'lan']


def aliyun_bdc_logger(hm, args, data):
    """记录新版英雄互娱新版 bdc的 eventinfo, 直接对接阿里云"""

    # 接口动作
    method = hm.get_argument('method')
    func_name = '_'.join(method.split('.'))
    if func_name not in bdc_event_funcs.BDC_EVENT_MAPPING:
        return
    func = getattr(bdc_event_funcs, func_name, None)
    if callable(func):
        # bdc_server_id = settings.get_bdc_server_id(hm.mm.user._server_name)
        # bdc_game_id = settings.BDC_GAME_ID

        # python生成时候的日志命名格式如下 方便后期shell合并时候截取处理
        # gameid_serverid_eventinfo-pid_date.log
        #
        # file=105_130105010001_eventinfo-9527_2017-01-01.log
        # 需要合并上传的日志命名格式 105_130105010001_eventinfo_2017-01-01.log

        f_name = bdc_event_funcs.bdc_log_file(hm.mm.user._server_name)
        # f_name = '%s_%s_%s' % (settings.ENV_NAME, os.getpid(), time.strftime('%F'))
        data = func(hm, args, data)
        # prefix = [time.strftime('%F %T'), bdc_event_funcs.BDC_EVENT_MAPPING[func_name]]

        event_id = bdc_event_funcs.BDC_EVENT_MAPPING[func_name]
        log = get_log(f_name, logging_class=StatLoggingUtil, propagate=0)

        # bdc文件记录
        if isinstance(data, list):
            for d in data:
                d['event_id'] = event_id
                log.info(json.dumps(d, separators=(',', ':')))
        else:
            data['event_id'] = event_id
            log.info(json.dumps(data, separators=(',', ':')))

        # bdc发给阿里云
        send_bdc_log_to_aliyun(data)


def bdc_logger(hm, args, data):
    """记录英雄互娱bdc的 eventinfo 老版的，已废弃 2018.12.11"""

    # TODO 检查 client_cache变动

    # 接口动作
    method = hm.get_argument('method')
    func_name = '_'.join(method.split('.'))
    if func_name not in bdc_event_funcs.BDC_EVENT_MAPPING:
        return
    func = getattr(bdc_event_funcs, func_name, None)
    if callable(func):
        # bdc_server_id = settings.get_bdc_server_id(hm.mm.user._server_name)
        # bdc_game_id = settings.BDC_GAME_ID

        # python生成时候的日志命名格式如下 方便后期shell合并时候截取处理
        # gameid_serverid_eventinfo-pid_date.log
        #
        # file=105_130105010001_eventinfo-9527_2017-01-01.log
        # 需要合并上传的日志命名格式 105_130105010001_eventinfo_2017-01-01.log

        f_name = bdc_event_funcs.bdc_log_file(hm.mm.user._server_name)
        # f_name = '%s_%s_%s' % (settings.ENV_NAME, os.getpid(), time.strftime('%F'))
        data = func(hm, args, data)
        prefix = [time.strftime('%F %T'), bdc_event_funcs.BDC_EVENT_MAPPING[func_name]]
        log = get_log(f_name, logging_class=StatLoggingUtil, propagate=0)
        if isinstance(data[0], list):
            for d in data:
                log.info(settings.BDC_LOG_DELITIMER.join((force_unicode(i) for i in chain(prefix, d))))
        else:
            log.info(settings.BDC_LOG_DELITIMER.join((force_unicode(i) for i in chain(prefix, data))))


def logger(hm, args, data):
    from models.logging import Logging
    method = hm.get_argument('method')
    if method:
        func_name = '_'.join(method.split('.'))
        func = getattr(logger_funcs, func_name, None)
        if callable(func):
            copy_args = copy.deepcopy(args)
            for i in IGNORE_ARG:
                copy_args.pop(i, None)
            result = func(hm, copy_args, data)
            Logging(hm.uid).add_logging(method, copy_args, result or data)


def get_stat(mm):
    """ 玩家身上数据的统计
    :param mm:
    """
    return {
        'coin': mm.user.coin,
        'dollar': mm.user.dollar,
        'silver': mm.user.silver,
        'diamond_free': mm.user.diamond_free,
        'diamond_charge': mm.user.diamond_charge,
        'energy': mm.user.action_point,
        'exp': mm.user.exp,
        'vip': mm.user.vip,
        'vip_exp': mm.user.vip_exp,
        'level': mm.user.level,
        'diamond': mm.user.diamond,
    }


def stat(func):
    """

    :param func:
    :return:
    """
    @wraps(func)
    def decorator(self, *args, **kwargs):

        ###########################################################
        has_hm = getattr(self, 'hm', None)

        if has_hm:
            arguments = copy.deepcopy(self.hm.req.summary_params())
            mm = self.hm.mm
        else:
            arguments = copy.deepcopy(self.summary_params())
            mm = None

        method = arguments.get('method')
        method = method[0] if method else ''
        device_mark = arguments.pop('device_mark', [''])[0]
        platform = arguments.pop('pt', [''])[0]

        ignore_arg_name = ['method', 'user_token', 'mk', 'kqg_cjxy', 'ks', '__ts', 'cjyx2']

        for arg_name in ignore_arg_name:
            if arg_name in arguments:
                del arguments[arg_name]

        user_stat_before = get_stat(mm)

        ###########################################################

        rc, data, msg, mm = func(self, *args, **kwargs)

        ###########################################################
        if data.get('goods_config_id', 0):
            arguments['goods_config_id'] = data.get('goods_config_id', 0)

        body = {
            'a_rst': [],
            'a_tar': arguments,
            'return_code': '0',
            'a_typ': method,
            'a_usr': '%s@%s' % (mm.user._server_name, mm.uid),
        }

        modify_args = data.pop('modify_args', None)
        if modify_args:
            delete_args = modify_args.get('delete')
            update_args = modify_args.get('update')
            if delete_args:
                for arg_name in delete_args:
                    if arg_name in arguments:
                        del arguments[arg_name]
            if update_args:
                arguments.update(update_args)

        # 非0返回将 return_code 记录用来分析常见错误返回
        if rc != 0:
            body['return_code'] = str(rc)
            return rc, data, msg, mm

        # 0 返回分析资源变化
        else:
            # reward = data.get('reward', {})
            # if reward:
            #     params['result']['reward'] = reward
            # func_name = '_'.join(method.split('.'))
            # result_func = getattr(logger_result_funcs, func_name, None)
            # if result_func and callable(result_func):
            #     params['result'].update(result_func(data))

            user_stat_after = get_stat(mm)
            resource_diff = []      # 资源变化列表
            gold_consume = 0

            ldt = time.strftime('%F %T')
            for k, v in user_stat_after.iteritems():
                _v = user_stat_before[k]
                if v != _v:
                    diff = v - _v
                    info = {
                        'obj': k,
                        'before': str(_v),
                        'after': str(v),
                        'diff': str(diff)
                    }
                    resource_diff.append(info)
                    if k == 'diamond':
                        if v > _v:  # 获得钻石
                            save_gold_obtain_log(mm, gold_charge=v-_v)
                        else:       # 消耗钻石
                            save_gold_consume_log(mm, gold_charge=_v-v)
                            gold_consume = _v-v

                    # bdc eventinfo 代币数量变动
                    if k in {'diamond', 'coin', 'silver', 'dollar'}:
                        event_sort = 'get_money' if diff > 0 else 'remove_money'
                        _kwargs = {'obj': k, 'before': _v, 'after': v, 'ldt': ldt}
                        bdc_event_funcs.special_bdc_log(mm.user, sort=event_sort, **_kwargs)

            # #### 从_client_cache_update中获取卡牌、装备、道具的变化 #########
            # 结构：
            # '_client_cache_update': {
            #   model_name: {
            #       diff_name: {
            #           'remove': set(),
            #           'update': {},
            #       },
            #   },
            # }
            #   'item': {
            #       'items': {
            #           'remove': set(),
            #           'update': {20003: 20},
            #       },
            #   },
            #   'grade_item': {
            #       'items': {
            #           'remove': set(),
            #           'update': {20003: 20},
            #       },
            #   },
            #   'hero': {
            #       'heros': {
            #           'remove': set(),
            #           'update': {20003: 20},
            #       },
            #       'pieces': {
            #           'remove': set(),
            #           'update': {20003: 20},
            #       },
            #   },
            #   'equip': {
            #       'equips': {
            #           'remove': set(),
            #           'update': {20003: 20},
            #       },
            #   },

            client_cache_udpate = data.get('_client_cache_update', {})
            old_data = data.pop('old_data', {})
            for class_type, class_type_value in client_cache_udpate.iteritems():
                old_data_key = mm.get_model_key(mm.uid, class_type)
                _old_data = old_data.get(old_data_key, {})

                # 道具, 进阶道具， 觉醒道具
                if class_type in ['item', 'grade_item', 'awaken_item']:
                    for attr_type, attr_type_value in class_type_value.iteritems():
                        # 道具数量
                        if attr_type == 'items':
                            for item_id, new_item_count in attr_type_value['update'].iteritems():
                                old_item_count = _old_data.get(attr_type, {}).get(item_id, 0)
                                diff_count = new_item_count - old_item_count
                                resource_diff.append({
                                    'obj': 'Item@%s' % item_id,
                                    'before': str(old_item_count),
                                    'after': str(new_item_count),
                                    'diff': str(diff_count),
                                })
                                if diff_count > 0:
                                    save_item_obtain_log(mm, gold_charge=gold_consume, item_id=item_id, item_count=diff_count,
                                                         item_type=class_type, current_num=new_item_count)
                                elif diff_count < 0:
                                    save_item_consume_log(mm, item_id=item_id, item_count=-diff_count,
                                                         item_type=class_type, current_num=new_item_count)

                                # bdc eventinfo 变动
                                event_sort = 'get_item' if diff_count > 0 else 'remove_item'
                                _kwargs = {'obj': 'Item@%s' % item_id, 'ldt': ldt,
                                           'before': old_item_count, 'after': new_item_count, 'diff': diff_count}
                                bdc_event_funcs.special_bdc_log(mm.user, sort=event_sort, **_kwargs)

                            for item_id in attr_type_value['remove']:
                                old_item_count = _old_data.get(attr_type, {}).get(item_id, 0)
                                new_item_count = 0
                                diff_count = new_item_count - old_item_count
                                resource_diff.append({
                                    'obj': 'Item@%s' % item_id,
                                    'before': str(old_item_count),
                                    'after': str(new_item_count),
                                    'diff': str(diff_count),
                                })
                                save_item_consume_log(mm, item_id=item_id, item_count=-diff_count,
                                                      item_type=class_type, current_num=new_item_count)

                                # bdc eventinfo 变动
                                _kwargs = {'obj': 'Item@%s' % item_id, 'ldt': ldt,
                                           'before': old_item_count, 'after': new_item_count, 'diff': diff_count}
                                bdc_event_funcs.special_bdc_log(mm.user, sort='remove_item', **_kwargs)

                # 卡牌和碎片
                if class_type == 'card':
                    for attr_type, attr_type_value in class_type_value.iteritems():
                        if attr_type == 'cards':
                            new_keys = set(attr_type_value['update']) - set(_old_data.get(attr_type, {}))
                            true_update_keys = set(attr_type_value['update']) - new_keys
                            # 新增卡牌记录
                            for card_id in new_keys:
                                card_info = attr_type_value['update'][card_id]
                                resource_diff.append({
                                    'obj': 'Card@%s' % card_id,
                                    'before': {},
                                    'after': {attr: card_info[attr] for attr in CARDS_MONITOR_ATTRS},
                                })

                                # bdc eventinfo 变动
                                _kwargs = {'obj': 'Card@%s' % card_info['id'], 'ldt': ldt, 'diff': 1}
                                bdc_event_funcs.special_bdc_log(mm.user, sort='get_item', **_kwargs)

                            # 删除卡牌记录
                            for card_id in attr_type_value['remove']:
                                card_info = _old_data.get(attr_type, {}).get(card_id, {})
                                resource_diff.append({
                                    'obj': 'Card@%s' % card_id,
                                    'before': {attr: card_info.get(attr, '') for attr in CARDS_MONITOR_ATTRS},
                                    'after': {},
                                })

                                # bdc eventinfo 变动
                                _kwargs = {'obj': 'Card@%s' % card_info['id'], 'ldt': ldt, 'diff': 1}
                                bdc_event_funcs.special_bdc_log(mm.user, sort='remove_item', **_kwargs)

                            # 更新卡牌记录
                            for card_id in true_update_keys:
                                new_card_info = attr_type_value['update'][card_id]
                                old_card_info = _old_data[attr_type][card_id]
                                attrs_before = {}
                                attrs_after = {}
                                for attr in CARDS_MONITOR_ATTRS:
                                    if attr == 'id' or new_card_info[attr] != old_card_info[attr]:
                                        attrs_before[attr] = str(old_card_info[attr])
                                        attrs_after[attr] = str(new_card_info[attr])
                                if attrs_before:
                                    resource_diff.append({
                                        'obj': 'Card@%s' % card_id,
                                        'before': attrs_before,
                                        'after': attrs_after,
                                    })

                                    if old_card_info['id'] != new_card_info['id']:
                                        # bdc eventinfo 变动
                                        _kwargs = {'obj': 'Card@%s' % old_card_info['id'], 'ldt': ldt, 'diff': 1}
                                        bdc_event_funcs.special_bdc_log(mm.user, sort='remove_item', **_kwargs)

                                        # bdc eventinfo 变动
                                        _kwargs = {'obj': 'Card@%s' % new_card_info['id'], 'ldt': ldt, 'diff': 1}
                                        bdc_event_funcs.special_bdc_log(mm.user, sort='get_item', **_kwargs)

                        elif attr_type == 'pieces':
                            for piece_id, new_piece_count in attr_type_value['update'].iteritems():
                                old_piece_count = _old_data.get(attr_type, {}).get(piece_id, 0)
                                resource_diff.append({
                                    'obj': 'Card_pieces@%s' % piece_id,
                                    'before': str(old_piece_count),
                                    'after': str(new_piece_count),
                                    'diff': str(new_piece_count - old_piece_count),
                                })

                                # bdc eventinfo 变动
                                _kwargs = {'obj': 'CardPiece@%s' % piece_id, 'ldt': ldt, 'diff': new_piece_count - old_piece_count}
                                event_sort = 'get_item' if _kwargs['diff'] > 0 else 'remove_item'
                                bdc_event_funcs.special_bdc_log(mm.user, sort=event_sort, **_kwargs)

                            for piece_id in attr_type_value['remove']:
                                old_piece_count = _old_data.get(attr_type, {}).get(piece_id, 0)
                                new_piece_count = 0
                                resource_diff.append({
                                    'obj': 'Card_pieces@%s' % piece_id,
                                    'before': str(old_piece_count),
                                    'after': str(new_piece_count),
                                    'diff': str(new_piece_count - old_piece_count),
                                })
                                # bdc eventinfo 变动
                                _kwargs = {'obj': 'CardPiece@%s' % piece_id, 'ldt': ldt, 'diff': new_piece_count - old_piece_count}
                                bdc_event_funcs.special_bdc_log(mm.user, sort='remove_item', **_kwargs)

                # 装备和碎片
                if class_type == 'equip':
                    for attr_type, attr_type_value in class_type_value.iteritems():
                        # 装备数量
                        if attr_type in ['equips', 'equip_pieces']:
                            for item_id, new_item_count in attr_type_value['update'].iteritems():
                                old_item_count = _old_data.get(attr_type, {}).get(item_id, 0)
                                diff_count = new_item_count - old_item_count
                                resource_diff.append({
                                    'obj': '%s@%s' % (attr_type.capitalize(), item_id),
                                    'before': str(old_item_count),
                                    'after': str(new_item_count),
                                    'diff': str(diff_count),
                                })

                                # bdc eventinfo 变动
                                event_sort = 'get_item' if diff_count > 0 else 'remove_item'
                                _kwargs = {'obj': '%s@%s' % (attr_type.capitalize(), item_id), 'ldt': ldt,
                                           'before': old_item_count, 'after': new_item_count, 'diff': diff_count}
                                bdc_event_funcs.special_bdc_log(mm.user, sort=event_sort, **_kwargs)

                            for item_id in attr_type_value['remove']:
                                old_item_count = _old_data.get(attr_type, {}).get(item_id, 0)
                                new_item_count = 0
                                diff_count = new_item_count - old_item_count
                                resource_diff.append({
                                    'obj': '%s@%s' % (attr_type.capitalize(), item_id),
                                    'before': str(old_item_count),
                                    'after': str(new_item_count),
                                    'diff': str(diff_count),
                                })
                                save_item_consume_log(mm, item_id=item_id, item_count=-diff_count,
                                                      item_type=class_type, current_num=new_item_count)

                                # bdc eventinfo 变动
                                _kwargs = {'obj': '%s@%s' % (attr_type.capitalize(), item_id), 'ldt': ldt,
                                           'before': old_item_count, 'after': new_item_count, 'diff': diff_count}
                                bdc_event_funcs.special_bdc_log(mm.user, sort='remove_item', **_kwargs)

            # #### 从_client_cache_update中获取卡牌、装备、道具和合体金刚的变化 #########

        body['a_rst'] = resource_diff
        dmp_data = {
            'body': body,
            'log_t': time.strftime('%F %T'),
            'device_mac': device_mark,
            'platform': platform,
            'account': mm.user.account,
            # 'app_id': '13001229',
            # 'app_ver': appver,
            # 'device_id': device_id,
            'level': str(mm.user.level),
            'exp': str(mm.user.exp),
            'vip_exp': str(mm.user.vip_exp),
            'company_vip_exp': str(mm.user.company_vip_exp),
            'silver': str(mm.user.silver),
            'coin': str(mm.user.coin),
            'diamond': str(mm.user.diamond),
            'sex':mm.user.get_sex()
        }

        f_name = '%s_%s_%s' % (settings.ENV_NAME, os.getpid(), time.strftime('%Y%m%d'))
        log = get_log('action/%s' % f_name, logging_class=StatLoggingUtil, propagate=0)
        log.info(json.dumps(dmp_data, separators=(',', ':')))
        # log.info('\t'.join([str(params.get(i, '')) for i in FORMAT]))

        # TODO 写一个英雄互娱bdc需要的eventinfo log
        if rc == 0 and has_hm:
            logger(has_hm, arguments, data)
            # bdc_logger(self.hm, arguments, data)

            # 新版英雄互娱bdc
            aliyun_bdc_logger(self.hm, arguments, data)

        ###########################################################

        return rc, data, msg, mm
    return decorator
