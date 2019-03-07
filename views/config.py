#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

import os
import re

import settings
import datetime
from gconfig import front_game_config
from models.config import ResourceVersion
from lib.utils.debug import print_log
import json


def resource_version(hm):
    """ 获取前端热更资源数据

    :param hm: HandlerManager
    :return:
    """
    res_version = hm.get_argument('res_version', '')
    ip = hm.req.request.headers.get('X-Real-Ip', '')
    tpid = hm.get_argument('tpid', 0, is_int=True)
    appid = hm.get_argument('appd', '')

    if appid == '2':    # 和前端协定1:android,2:iOS
        version_dirs = os.path.join(settings.BASE_ROOT, 'logs', 'client_resource', 'ios')
    else:
        version_dirs = os.path.join(settings.BASE_ROOT, 'logs', 'client_resource', 'android')

    current_version = res_version

    # # ios补丁tag
    # if tpid == 56:
    #     version_path = ''
    #     if settings.ENV_NAME == 'dev' and current_version < 't1.2.740':
    #         version_path = os.path.join(version_dirs, 'pih1.0.002_pih1.0.001.json')
    #
    #     elif settings.ENV_NAME == 'release_test3' and current_version < 'ph1.1.151':
    #         version_path = os.path.join(version_dirs, 'pih1.1.151_pih1.1.054.json')
    #
    #     if version_path:
    #         try:
    #             if os.path.exists(version_path):
    #                 fp = open(version_path, 'rb')
    #                 data = eval(fp.read())
    #                 fp.close()
    #                 return 0, data
    #         except (OSError, ValueError):
    #             return 0, {
    #                 'current_version': current_version,
    #                 'different_files': [],
    #                 'md5': '',
    #                 'sum_size': '0K',
    #             }

    if os.path.exists(version_dirs):
        try:
            resource = ResourceVersion.get()
            current_version, recent_version = check_version(version_dirs, current_version)
            # 不属于灰度时  外网玩家
            # print_log('current_version', current_version)
            if resource.hot_update_switch and ip not in resource.get_can_hot_update_ip():
                if resource.limit_version and current_version < resource.limit_version:
                    version_path = os.path.join(version_dirs, '%s_%s.json' % (resource.limit_version, current_version))
                # 已更新 但中间又开灰度时
                else:
                    version_path = os.path.join(version_dirs, '%s_%s.json' % (current_version, current_version))
            else:
                version_path = os.path.join(version_dirs, '%s_%s.json' % (recent_version, current_version))
            if os.path.exists(version_path):
                fp = open(version_path, 'rb')
                data = eval(fp.read())
                fp.close()
                return 0, data
        except (OSError, ValueError):
            pass
    return 0, {
        'current_version': current_version,
        'different_files': [],
        'md5': '',
        'sum_size': '0K',
    }


def all_config(hm):
    """ 获取配置

    :param hm:
    :return:
    """
    config_name = hm.get_argument('config_name')
    result = {}
    config_version = front_game_config.versions.get(config_name)
    if config_version is None:
        return 1, {}

    result[config_name] = getattr(front_game_config, config_name, {})
    result['config_version'] = config_version

    return 0, result


def config_version(hm):
    """ 获得所有配置的版本号

    :param hm:
    :return:
    """
    version_size = {}
    for name in front_game_config.versions.keys():
        config = getattr(front_game_config, name, {})
        s = round(len(json.dumps(config, separators=(',', ':'))) / 1024.0, 2)
        if s == 0:
            continue
        version_size[name] = '%sK' % (s)
    return 0, {
        'game_config_version': front_game_config.versions,
        'all_config_version': front_game_config.ver_md5,
        'version_size': version_size
    }


def server_env(hm):
    """ 获取服务器环境

    :param hm:
    :return:
    """
    result = {
        'env_name': settings.ENV_NAME,
        'server_time': datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'),
        'X-Real-Ip': hm.req.headers.get('X-Real-Ip', ''),
        'X-Forwarded-For': hm.req.headers.get('X-Forwarded-For', ''),
    }

    return 0, result


def check_version(version_dirs, client_version):
    """
    检测版本号是否存在
    版本号小于最小的版本取最小的版本
    版本号不存在时  向下匹配
    """
    # 2017.5.26添加  避免删前端tag时错误的问题
    if not os.path.exists(version_dirs):
        os.mkdir(version_dirs)
    version_prefix = re.match('^[a-zA-Z]*', client_version).group() #re.split('\d', client_version, 1)[0]
    if not version_prefix:
        return client_version, ''
    file_list = [i for i in os.listdir(version_dirs) if re.match('%s\d+' % version_prefix, i)]
    all_version_file = sorted(file_list, key=lambda x: x.split('_')[0])
    # all_version_file = sorted(os.listdir(version_dirs), key=lambda x: x.split('_')[0])

    max_version = ''
    recent_version_list = []
    if all_version_file:
        max_version = all_version_file[-1].split('_')[0]
        recent_version_list = [i for i in all_version_file if i.startswith(max_version)]

    all_json = []
    if recent_version_list:
        for version_file in recent_version_list:
            if not version_file.endswith('.json'):
                continue
            _, version_file = version_file.split("_")
            if version_file not in all_json:
                all_json.append(version_file.split('.json')[0])
    else:
        for version_file in os.listdir(version_dirs):
            if not version_file.endswith('json'):
                continue
            end_json, start_json = version_file.split("_")
            start_version, _ = start_json.split(".json")
            if start_version not in all_json:
                all_json.append(start_version)

    current_version = client_version
    if all_json:
        all_json = sorted(all_json)
        # recent_version = max(all_json)
        if client_version not in all_json:
            # 版本号小于最小的版本时向上匹配
            if client_version < all_json[0]:
                current_version = all_json[0]
            if client_version > all_json[-1]:
                current_version = current_version
            # 版本号不存在时  向下匹配
            else:
                # all_json.reverse()
                for i in all_json[::-1]:
                    if current_version > i:
                        current_version = i
                        break

    return current_version, max_version
