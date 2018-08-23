#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 重置生产模块

import os
import sys

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings


def init_env(env):
    settings.set_env(env)


def reset_model(model_list):
    """
    重置模块
    :param model_list:
    :return:
    """
    for model_name in model_list:
        uid = None
        for server in ServerUidList.all_server():
            server_uid = ServerUid(server)
            for uid in server_uid.get_all_uid():
                mm = ModelManager(uid)
                model = getattr(mm, model_name)
                if model:
                    model.reset()
                    func = globals().get('after_reset_%s' % model_name)
                    if hasattr(func, '__call__'):   # 如果有重置后函数
                        func(uid)
        one_func = globals().get('after_reset_one_%s' % model_name)
        if hasattr(one_func, '__call__') and uid:   # 如果有重置后函数
            one_func(uid)


def after_reset_one_user_market(uid):
    mm = ModelManager(uid)
    market_obj = mm.get_obj_tools('market')
    market_obj.del_all()
    publicity_obj = mm.get_obj_tools('publicity')
    publicity_obj.del_all()


if __name__ == '__main__':
    env = sys.argv[1]
    init_env(env)
    reset_model_list = sys.argv[2:]
    if not reset_model_list:
        y = raw_input('reset all model? [Y/n]: ')
    else:
        y = raw_input('reset %s model? [Y/n]: ' % reset_model_list)

    if y in ['Y', 'y', 'yes']:
        from models.server import ServerUidList, ServerUid
        from lib.core.environ import ModelManager
        from gconfig import game_config
        reset_model(reset_model_list)
