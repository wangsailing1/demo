#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 批量导入配置

import os
import sys

# 设置程序使用的编码格式, 统一为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings


def init_env(env):
    settings.set_env(env)


def file_import(configs_file):
    """ 文件导入

    :param configs_file:
    :return:
    """
    from gconfig import game_config, front_game_config

    error_files = []
    success_files = []
    front_error_files = []
    front_success_files = []

    try:
        save_list, _ = game_config.upload(configs_file)
        success_files.extend(save_list)
    except:
        import traceback
        traceback.print_exc()
        error_files.append(configs_file)

    try:
        save_list, _, _ = front_game_config.upload(configs_file)
        front_success_files.extend(save_list)
    except:
        import traceback
        traceback.print_exc()
        front_error_files.append(configs_file)

    if success_files:
        print 'success_files: ', success_files

    if front_success_files:
        print 'front_success_files: ', front_success_files

    if error_files:
        print 'error_files:', error_files

    if front_error_files:
        print 'front_error_files:', front_error_files


def batch_import(configs_path):
    """ 批量导入

    :param configs_path:
    :return:
    """
    from gconfig import game_config, front_game_config

    error_files = []
    success_files = []
    front_error_files = []
    front_success_files = []

    for file_name in os.listdir(configs_path):
        if 'xls' not in file_name:
            continue
        file_path = os.path.join(configs_path, file_name)
        try:
            save_list, _ = game_config.upload(file_path)
            success_files.extend(save_list)
        except:
            import traceback
            traceback.print_exc()
            error_files.append(file_name)

        try:
            save_list, _, _ = front_game_config.upload(file_path)
            front_success_files.extend(save_list)
        except:
            import traceback
            traceback.print_exc()
            front_error_files.append(file_name)

    if success_files:
        print 'success_files: ', success_files

    if front_success_files:
        print 'front_success_files: ', front_success_files

    if error_files:
        print 'error_files:', error_files

    if front_error_files:
        print 'front_error_files:', front_error_files


if __name__ == '__main__':
    env = sys.argv[1]
    path = sys.argv[2]
    init_env(env)
    if os.path.isfile(path):
        file_import(path)
    else:
        batch_import(path)
