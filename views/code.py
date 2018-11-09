#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from gconfig import game_config
import settings
from logics.code import check_time
from logics.code import CodeLogic
from return_msg_config import get_msg_str


def index(hm):
    """激活码页面
    """
    mm = hm.mm

    return 0, {
        'codes': mm.code.codes,
    }


def use_code(hm):
    """使用激活码
    args:
        code: 激活码
    """
    mm = hm.mm

    code = hm.get_argument('code')
    code = code.encode('utf-8')
    code_data = mm.code.activation_code.get_code(code)

    if not code_data or code_data['code_id'] not in game_config.code:
        return 1, {}    # 没有这个激活码所对应的活动

    config = game_config.code[code_data['code_id']]
    if config['type'] != 1:
        # type -- 0: 一人用一个码 1：多人可用一个码
        # 这个激活码已经被使用过了
        used_uid = code_data['used_uid']
        if used_uid:
            if used_uid == mm.uid:
                return -1, {}   # 您已经领过这个礼包了
            else:
                return 3, {}    # 这个激活码已经被使用过了

    need_vip = config.get('vip', 0)
    if need_vip and mm.user.vip < need_vip:
        return 2, {}    # vip等级不足

    # 获取用户的config_type 1 是新服 2 是老服 3 是老老服
    config_type = game_config.get_config_type(mm.user._server_name)
    # 激活码的应用的服
    server_label_list = config.get('server','').split(',')
    if server_label_list != [''] and str(config_type) not in server_label_list:
        return 6, {} # 不符合领取条件。

    # refresh 0: 一个人一类型领取一次， <0 ：一人一类型领取多个， >0： 一人一类型按周期重复领取
    if config['refresh'] < 0:
        if code_data['code_id'] in mm.code.codes:
            if code in mm.code.codes[code_data['code_id']]['codes']:
                return -1, {}    # 您已经领过这个礼包了

    # 您的这个账号已经领取过奖励了
    method_param = hm.get_argument('method')
    refresh_status = mm.code.check_code_refresh_status(code_data['code_id'])
    if refresh_status:
        if refresh_status == -1:
            msg = get_msg_str(mm.user.language_sort).get(method_param, {}).get(refresh_status)
        else:
            msg = get_msg_str(mm.user.language_sort).get(method_param, {}).get(5)
            if msg and '%s' in msg:
                msg = msg % refresh_status
        return refresh_status, {'custom_msg': msg}

    # 这个活动已经过期了
    if not check_time(config):
        return 4, {}

    award = CodeLogic(mm).use_code(code, code_data, config)

    return 0, {
        'codes': mm.code.codes,
        'reward': award,
    }
