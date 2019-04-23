#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import os
import copy
import time
from functools import wraps

from lib.statistics import logger_result_funcs, logger_funcs
from lib.utils.loggings import get_log, StatLoggingUtil
from lib.utils.debug import print_log

import settings

FORMAT = [
    'date',                         # 1
    'time',                         # 2
    'env',                          # 3
    'server',                       # 4
    'uid',                          # 5
    'account',                      # 6

    'pre_level',                   # 7
    'pre_exp',                     # 8
    'pre_vip',                     # 9
    'pre_vip_exp',                 # 10

    'pre_silver',                  # 11
    'pre_coin',                    # 12
    'pre_diamond',                 # 13

    'post_level',                  # 14
    'post_exp',                    # 15
    'post_vip',                    # 16
    'post_vip_exp',                # 17

    'post_silver',                 # 18
    'post_coin',                   # 19
    'post_diamond',                # 20

    'action',                      # 21
    'rc',                          # 22
    'args',                        # 23
    'result',                      # 24
]

path = os.path.join(settings.BASE_ROOT, 'logs/action/')

os.system("""[ ! -d '%s' ] && mkdir -p %s"""%(path, path))


def logger(hm, args, data):
    from models.logging import Logging
    method = hm.get_argument('method')
    if method:
        func_name = '_'.join(method.split('.'))
        func = getattr(logger_funcs, func_name, None)
        if callable(func):
            result = func(hm, args, data)
            Logging(hm.uid).add_logging(method, args, result or data)


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

        ignore_arg_name = ['method', 'user_token', 'mk', 'kqg_cjxy', 'ks']

        for arg_name in ignore_arg_name:
            if arg_name in arguments:
                del arguments[arg_name]

        params = {
            'env': settings.ENV_NAME,
            'server': settings.SERVER_SORT,
            'date': time.strftime("%Y-%m-%d"),
            'time': time.strftime("%H:%M:%S"),
            'action': method,
            'args': arguments,
        }

        if mm is not None:
            params.update({
                'uid': mm.uid,
                'account': mm.user.account,
                'pre_level': mm.user.level,
                'pre_exp': mm.user.exp,
                'pre_vip': mm.user.vip,
                'pre_vip_exp': mm.user.vip_exp,
                'pre_silver': mm.user.silver,
                'pre_coin': mm.user.coin,
                'pre_diamond': mm.user.diamond,
            })
        ###########################################################

        rc, data, msg, mm = func(self, *args, **kwargs)

        ###########################################################
        params.update({
            'rc': rc,
            'result': {},
        })

        modify_args = data.pop('modify_args', None)
        if modify_args:
            delete_args = modify_args.get('delete')
            update_args = modify_args.get('update')
            if delete_args:
                for arg_name in delete_args:
                    if arg_name in params['args']:
                        del params['args'][arg_name]
            if update_args:
                params['args'].update(update_args)

        if rc == 0:
            reward = data.get('reward', {})
            if reward:
                params['result']['reward'] = reward
            func_name = '_'.join(method.split('.'))
            result_func = getattr(logger_result_funcs, func_name, None)
            if result_func and callable(result_func):
                params['result'].update(result_func(data))

        if mm is None:
            hm = getattr(self, 'hm', None)
            if hm and hm.mm:
                mm = hm.mm
                params.update({
                    'uid': mm.uid,
                    'account': mm.user.account,
                    'pre_level': mm.user.level,
                    'pre_exp': mm.user.exp,
                    'pre_vip': mm.user.vip,
                    'pre_vip_exp': mm.user.vip_exp,
                    'pre_silver': mm.user.silver,
                    'pre_coin': mm.user.coin,
                    'pre_diamond': mm.user.diamond,
                })

        if mm is not None:
            params.update({
                'post_level': mm.user.level,
                'post_exp': mm.user.exp,
                'post_vip': mm.user.vip,
                'post_vip_exp': mm.user.vip_exp,
                'post_silver': mm.user.silver,
                'post_coin': mm.user.coin,
                'post_diamond': mm.user.diamond,
            })

        file_name = '%s_%s_%s' % (settings.ENV_NAME, os.getpid(), time.strftime('%Y%m%d'))

        log = get_log('action/%s' % file_name, logging_class=StatLoggingUtil, propagate=0)

        log.info('\t'.join([str(params.get(i, '')) for i in FORMAT]))

        if rc == 0 and has_hm:
            logger(has_hm, arguments, data)

        ###########################################################

        return rc, data, msg, mm
    return decorator
