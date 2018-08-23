#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import os
import sys
import traceback
import time
import datetime
import openpyxl
import cStringIO
import json

import settings
from admin import render
from admin.decorators import require_permission
from gconfig.back_contents import mapping_config as back_mapping_config
from gconfig.front_contents import mapping_config as front_mapping_config
from models.config import Config, FrontConfig
from gconfig import game_config, front_game_config
from lib.utils import change_time
from models.config import ChangeTime, ResourceVersion, ConfigRefresh
from models.server import ServerConfig, ServerUidList, ServerUid
from lib.utils.timelib import datetime_str_to_timestamp, timestamp_to_datetime_str
from handler_tools import to_json
from lib.utils.debug import print_log


# ###### cdn配置定期删除多的配置
path = settings.CONFIG_RESOURCE_PATH

os.system("""[ ! -d '%s' ] && mkdir -p %s"""%(path, path))

now = time.time()
config_data = {}
for abs_path, dirs, files in os.walk(path):
    for file_name in files:
        config_name, _ = file_name.rsplit('_', 1)
        file_path = os.path.join(abs_path, file_name)
        try:
            st = os.stat(file_path)
            if config_name not in config_data:
                config_data[config_name] = {
                    'mtime': st.st_mtime,
                    'path': file_path,
                }
            if st.st_mtime > config_data[config_name]['mtime']:
                os.remove(config_data[config_name]['path'])
                config_data[config_name] = {
                    'mtime': st.st_mtime,
                    'path': file_path,
                }
            elif st.st_mtime < config_data[config_name]['mtime']:
                os.remove(file_path)
        except Exception, e:
            print_log(e)

# ###### cdn配置定期删除多的配置

config_types = {1: unicode('新服', 'utf-8'), 2: unicode('老服', 'utf-8'), 3: unicode('老老服', 'utf-8'), 4: unicode('新区', 'utf-8')}

# @require_permission
# def force_update(req):
#     message = req.get_argument('config_refresh_text', '')
#     flag = int(req.get_argument('config_refresh_flag', 0))
#     ConfigRefresh.refresh(flag)

#     return flag, message

@require_permission
def select(req, **kwargs):
    """

    :param req:
    :return:
    """
    from views.config import check_version
    config_key = req.get_argument('config_key', '')
    limit_version = str(req.get_argument('hot_version_limit', ''))

    c = Config.get(config_key)
    config_data = c.value
    last_update_time = c.last_update_time

    if not config_data and config_key:
        config_data = getattr(game_config, config_key)

    refresh_text = req.get_argument('config_refresh_text', '')
    flag = int(req.get_argument('config_refresh_flag', 0))
    if flag or refresh_text:
        ConfigRefresh.refresh(flag, refresh_text)
    refresh_flag, _, refresh_text = ConfigRefresh.check()

    resource = ResourceVersion.get()
    res_flag = int(req.get_argument('test_res_version_flag', -1))
    white_ip = req.get_argument('white_ip', '-1')
    if res_flag != -1 and res_flag != resource.hot_update_switch:
        resource.set_switch(res_flag, is_save=True)
    if white_ip != '-1' and white_ip != resource.can_hot_update_ip:
        resource.set_update_ip(white_ip, is_save=True)

    version_dirs = os.path.join(settings.BASE_ROOT, 'logs', 'client_resource')
    check_limit_version, recent_version = check_version(version_dirs, limit_version)
    if check_limit_version != resource.limit_version and limit_version:
        resource.set_limit_version(check_limit_version, is_save=True)
    if recent_version != resource.recent_version:
        resource.set_recent_version(recent_version, is_save=True)

    msg = kwargs.get('msg', '')

    return render(req, 'admin/config/index.html', **{
        'mapping_config': back_mapping_config,
        'config_key': config_key,
        'config_data': config_data,
        'config_refresh_flag': refresh_flag,
        'config_refresh_text': refresh_text,
        'last_update_time': last_update_time,
        'test_res_version_flag': resource.hot_update_switch,
        'can_hot_update_ip': resource.can_hot_update_ip,
        'limit_version': resource.limit_version,
        'recent_version': resource.recent_version,
        'msg': msg,
    })


@require_permission
def front_select(req, **kwargs):
    """ 前端配置

    :param req:
    :return:
    """
    config_key = req.get_argument('config_key', '')


    c = FrontConfig.get(config_key)
    config_data = c.value
    last_update_time = c.last_update_time

    if not config_data and config_key:
        config_data = getattr(front_game_config, config_key)

    msg = kwargs.get('msg', '')

    return render(req, 'admin/config/front_index.html', **{
        'mapping_config': front_mapping_config,
        'config_key': config_key,
        'config_data': config_data,
        'last_update_time': last_update_time,
        'msg': msg,
    })


@require_permission
def upload(req):
    """

    :param req:
    :return:
    """
    front_warning_msg = []
    file_obj = req.request.files.get('xls', None)

    if not file_obj:
        return select(req, msg=u"哥们，求文件")

    file_name = file_obj[0]['filename']
    platform = settings.PLATFORM
    if False and not settings.DEBUG and platform and platform not in file_name:
        return select(req, msg=u"检查配置文件是否为 %s 平台的" % platform)

    # 获取当前时分秒
    file_name_part = time.strftime('%Y-%m-%d-%H-%M-%S')

    # 保存文件
    file_dir = os.path.join(settings.BASE_ROOT, 'upload_xls')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    name, suffix = os.path.splitext(file_name)

    file_name = os.path.join(file_dir, '%s_%s%s' % (name, file_name_part, suffix))
    filebody = file_obj[0]['body']
    hfile = open(file_name, 'wb+')
    hfile.write(filebody)
    hfile.close()

    xl = openpyxl.load_workbook(filename=file_name, use_iterators=True)

    try:
        back_save_list, back_warning_msg = game_config.upload(file_name, xl)
    except:
        etype, value, tb = sys.exc_info()
        line = traceback.format_exception_only(etype, value)
        line_str = '-'.join(line)
        return select(req, **{'msg': 'back error: (%s)' % line_str.replace('\\', '')})

    if front_game_config:
        try:
            front_save_list, save_file_data, front_warning_msg = front_game_config.upload(file_name, xl)
        except:
            etype, value, tb = sys.exc_info()
            line = traceback.format_exception_only(etype, value)
            line_str = '-'.join(line)
            return select(req, **{'msg': 'front error: (%s)' % line_str.replace('\\', '')})

        # # 配置cdn文件
        # if settings.CONFIG_RESOURCE_OPEN:
        #     for config_name, m, config in save_file_data:
        #         filename = '%s%s_%s.json' % (settings.CONFIG_RESOURCE_PATH, config_name, m)
        #         with open(filename, 'wb+') as f:
        #             r = json.dumps(config, ensure_ascii=False, separators=(',',':'), encoding='utf-8', default=to_json)
        #             f.write(r)
    else:
        front_save_list = []
    if back_warning_msg or front_warning_msg:
        return select(req,  **{'msg': 'warning: back(%s) front(%s) ,done: back(%s) front(%s)' % (','.join(back_warning_msg), ','.join(front_warning_msg), ','.join(back_save_list), ','.join(front_save_list))})
    ConfigRefresh.set_updated()
    return select(req, **{'msg': 'done: back(%s) front(%s)' % (','.join(back_save_list), ','.join(front_save_list))})


@require_permission
def refresh(req):

    back_status = game_config.refresh()
    front_status = front_game_config.refresh()

    if back_status or front_status:
        return select(req, **{'msg': 'update success'})
    else:
        return select(req, **{'msg': 'no update'})


@require_permission
def modify_time_index(req, **kwargs):
    real_time = change_time.REAL_DATETIME_FUNC().strftime('%F %T')
    real_week = change_time.REAL_DATETIME_FUNC().weekday() + 1
    sys_time = datetime.datetime.now().strftime('%F %T')
    sys_week = datetime.datetime.now().weekday() + 1

    msg = kwargs.get('msg', '')

    return render(req,  'admin/sys_time_index.html', **{
        'real_time': real_time,
        'real_week': real_week,
        'sys_time': sys_time,
        'sys_week': sys_week,
        'msg': msg,
    })


@require_permission
def modify_time(req):
    if not settings.DEBUG:
        return modify_time_index(req, msg='fail')

    sys_time = req.get_argument('sys_time', '').strip('')
    add_day = req.get_argument('add_day', '')
    sub_day = req.get_argument('sub_day', '')

    real_time = change_time.REAL_TIME_FUNC()
    if add_day:
        sys_time = (datetime.datetime.now() + datetime.timedelta(1)).strftime('%F %T')
    elif sub_day:
        sys_time = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%F %T')

    if sys_time == '0' or not sys_time:
        new_time = 0
        delta_seconds = 0
    else:
        new_time = datetime_str_to_timestamp(sys_time)
        delta_seconds = int(new_time - real_time)

    change_time.change_time(new_time)   # 更改系统时间
    ChangeTime.set(delta_seconds)

    return modify_time_index(req, msg='success')


@require_permission
def modify_server_start_time_index(req, **kwargs):

    sc = ServerConfig.get()
    info = []
    for server in ServerUidList.all_server():
        server_uid = ServerUid(server)
        online_user_count = server_uid.get_online_user_count()
        total_count = server_uid.owned_count()
        info.append({'server': server, 'online_user_count': online_user_count, 'total_count': total_count})

    info_sorted = sorted(info, key=lambda x: x['server'])

    msg = kwargs.get('msg', '')

    return render(req, 'admin/server_config_index.html', **{
        'start_time': timestamp_to_datetime_str(sc.start_time),
        'server_info': info_sorted,
        'msg': msg,
    })


@require_permission
def modify_server_start_time(req):

    start_time = req.get_argument('start_time', '').strip('')

    if start_time == '0' or not start_time:
        start_time = 0
    else:
        start_time = datetime_str_to_timestamp(start_time)

    sc = ServerConfig.get()
    sc.modify_start_time(start_time)

    return modify_server_start_time_index(req, msg='success')


@require_permission
def server_change(req):
    """# server_change: 修改一个服务的属性，name和是否开放
    """
    msg = []
    server_key = req.get_argument('server_key')
    sc = None
    if server_key == 'master':
        msg.append(u'master不能被修改')
    else:
        server_name = req.get_argument('server_name', u'')
        is_open = int(req.get_argument('is_open'))
        flag = int(req.get_argument('flag'))
        sort_id = int(req.get_argument('sort_id'))
        include_pt = req.get_argument('include_pt', '').encode('utf-8').replace(' ', '')
        exclude_pt = req.get_argument('exclude_pt', '').encode('utf-8').replace(' ', '')
        # elites_account = req.get_argument('elites_account', '').encode('utf-8').replace(' ', '')
        include_pt = [int(x) for x in include_pt.replace('，', ',').split(',')] if include_pt else []
        exclude_pt = [int(x) for x in exclude_pt.replace('，', ',').split(',')] if exclude_pt else []
        # elites_account = [x for x in elites_account.replace('，', ',').split(',')] if elites_account else []

        if is_open and not server_name:
            msg.append(u'赐名方可开放')
        else:
            sc = ServerConfig.get()
            sc.config_value[server_key]['name'] = server_name
            if not sc.config_value[server_key]['is_open'] and bool(is_open):
                if sc.config_value[server_key]['open_time'] <= 0:
                    sc.config_value[server_key]['open_time'] = int(time.time())
            sc.config_value[server_key]['is_open'] = bool(is_open)
            sc.config_value[server_key]['flag'] = flag
            sc.config_value[server_key]['sort_id'] = sort_id
            sc.config_value[server_key]['include_pt'] = include_pt
            sc.config_value[server_key]['exclude_pt'] = exclude_pt
            # sc.config_value[server_key]['elites_account'] = elites_account

            msg.append(u'%s-%s changed' % (server_key, server_name))
            sc.save()
    return server_list(req, server_config_obj=sc, msg=msg)


@require_permission
def server_list(req, server_config_obj=None, msg=None, server_config_type=None):
    """
    server_config: 分服方面的设置
    """
    if server_config_obj is None:
        l = ServerConfig.get().server_list(need_filter=False)
    else:
        l = server_config_obj.server_list(need_filter=False)
    a = []
    b = []
    for i in l:
        if i['is_open']:
            a.append(i)
        else:
            b.append(i)

    return render(req, 'admin/server_config_index.html', **{
        'server_open': a,
        'server_notopen': b,
        'server_list': l,
        'config_types': config_types,
        'server_config_type': server_config_type,
        'msg': msg if msg is not None else [],
    })


@require_permission
def upload_local_config(req):
    """通过后台下载的 local_config.py 文件直接上传所有配置
    """
    import hashlib
    from models.config import ConfigVersion, FrontConfigVersion

    if not settings.DEBUG:
        return render(req, 'admin/config/notice.html',
                      **{'msg': unicode('哥们，只有测试环境可用', 'utf-8')}
                      )

    back_config = int(req.get_argument('back_config', '1'))
    file_obj = req.request.files.get('local_config', None)
    if not file_obj:
        return render(req, 'admin/config/notice.html',
                      **{'msg': unicode('哥们，求文件', 'utf-8')}
                      )

    # 备份一下进入配置页面首页的函数 @require_permission
    #                            def config(req, **msg):
    # 因为导入的 local_config文件里有个变量名也叫config，会冲突
    # config_index = config

    body = file_obj[0]['body']
    if not body:
        return render(req, 'admin/config/notice.html',
                      **{'msg': unicode('哥们，求内容', 'utf-8')}
                      )

    f = cStringIO.StringIO()
    f.write(body)        # eg: 'config={"name1": value1, "name2": value2, ...}
    # exec(f.getvalue())
    import cPickle as pickle
    config_data = pickle.loads(f.getvalue())
    f.close()

    done_list = []

    if back_config:
        cv = ConfigVersion.get()
        ConfigModel = Config
    else:
        cv = FrontConfigVersion.get()
        ConfigModel = FrontConfig
    for config_name, config in config_data.iteritems():
        m = hashlib.md5(repr(config)).hexdigest()
        if cv.versions.get(config_name) == m:
            continue
        c = ConfigModel.get(config_name)
        c.update_config(config, m, save=True)
        cv.update_version(config_name, m)
        done_list.append(config_name)
    cv.save()

    return select(req, **{'msg': 'num: %s, done: ' % len(done_list) + ', '.join(done_list)})


@require_permission
def get_all_config(req):
    """# get_all_config: docstring
    args:
        req:    ---    arg
    returns:
        0    ---
    """
    req.set_header('Content-Type', 'application/txt')
    req.set_header('Content-Disposition', 'attachment;filename=local_config_back.py')
    from test.get_all_configs import get_all_config
    file_name = get_all_config()
    file_obj = open(file_name, 'r')
    req.write(file_obj.read())


@require_permission
def get_all_config_front(req):
    """# get_all_config: docstring
    args:
        req:    ---    arg
    returns:
        0    ---
    """
    req.set_header('Content-Type', 'application/txt')
    req.set_header('Content-Disposition', 'attachment;filename=local_config_front.py')
    from test.get_all_configs import get_all_config
    file_name = get_all_config(back_config=False)
    file_obj = open(file_name, 'r')
    req.write(file_obj.read())


@require_permission
def deploy_download(req):
    """
    下载配置
    :param req:
    :return:
    """
    import os, sys
    file_name = req.get_argument('name', '')
    req.set_header('Content-Type', 'application/txt')
    req.set_header('Content-Disposition', 'attachment;filename=%s'% file_name)

    if not file_name:
        return None
    cur_dir = settings.BASE_ROOT
    sys.path.append(os.path.join(cur_dir))
    file_path_name = cur_dir + 'upload_xls/%s' % file_name
    with open(file_path_name, 'r') as f:
        req.write(f.read())


@require_permission
def get_deploy(req):
    """
    配置下载功能
    :param req:
    :return:
    """
    import os, sys

    cur_dir = settings.BASE_ROOT
    # sys.path.insert(0, os.path.join(cur_dir, ".."))
    sys.path.append(os.path.join(cur_dir))
    file_address = cur_dir + 'upload_xls'
    file_name = []
    file_dict = {}
    for dirpaths, dirnames, filenames in os.walk(file_address):
        for filename in filenames:
            if "." in filename:
                filename_list = filename.split("_")
                filename_time = filename_list.pop()
                filename_name = "_".join(filename_list)
                if filename_name not in file_name:
                    file_name.append(filename_name)
                    file_dict[filename_name] = [filename_time]
                else:
                    file_dict[filename_name].append(filename_time)

    file_name_sort = []
    for k, v in file_dict.items():
        time_sort = sorted(v, reverse=True)
        if len(v) > 3:
            time_sort = time_sort[0:3]
        for t in time_sort:
            file_name_sort.append(k+'_'+t)

    return render(req, 'admin/config/deploy_download.html', **{
        'file_name': file_name_sort,
    })
