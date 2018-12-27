# -*- coding: utf-8 –*-

"""
Created on 2018-06-01

@author: sm
"""
"""

参数简称	字段类型	完整含义	备注
ldt	Bigint	logDate: 游戏日志生成时间	Linux时间戳
gid	Varchar(20)	gameId: 游戏编号ID	由英雄互娱配置，请勿自行定义
cid	Bigint	channelId: 游戏渠道ID	请使用英雄互娱统一渠道ID配置表
cpd	Varchar(20)	cpsId: 预留CPS ID	没有请填写-1，此字段与cid共同组合用于区分cps渠道，自定义
pid	int	platformId: 游戏平台ID	11 IOS;12 越狱;13 安卓;14 EFUN;15 WP;16 PC;17 Mac;18 混服
mac	Varchar(50)	mac: 游戏设备编号	IOS请填写idfa，安卓请填写IMEI - Android ID
aid	Varchar(100)	AccountId: 游戏账号ID	研发提供唯一账号
anm	Varchar(100)	AccountName: 登陆账号名称	渠道标识+渠道openid+其他
sid	Bigint	ServerId: 游戏服务器ID	请使用英雄互娱统一服务器ID配置表
rid	Varchar(20)	roleId: 游戏角色ID	单服务器ID必须唯一，玩家界面可见，请尽量配置为短ID
rky	Varchar(50)	roleKey: 游戏角色Key	全服务器必须唯一，方便合服以及IPO操作
rnm	Varchar(20)	roleKey: 游戏角色中文名称	单服务器名称必须唯一
rlv	int	roleLevel: 游戏角色等级	玩家等级需大于等于1
vip	int	vipLevel: 游戏角色vip等级	VIP等级需大于等于0，没有vip等级请填写为-1
slv	int	specialLevel: 预留游戏特殊等级	天梯等级，竞技等级，军港等级等等，没有请填写-1
sex	int	sex: 游戏角色性别	女性角色填写0，男性角色填写1，无角色区分填写-1
uid	Varchar(50)	unionID: 游戏角色公会、军团ID	无公会或未加入公会请填写-1
rip	Varchar(50)	registerIP: 玩家注册IP	账号注册时的IP


4.0 UserActionInfo 用户行为日志
业务要求： 每天提取一次。每天0点导出成文本文件，所有日志导入到一个文本中，除第一个字段外，其他公共、业务字段均为 varchar(200) 类型。公共字段、业务字段中间的“，”，请最终用“|”替代。最后一列“日志备注”为注释列，正式日志生成时，请忽略勿生成此列
举例如下：
文本格式：| ldt | DEV_REGISTER | rip,cid,mac | 客户端版本号,客户端类型 |设备注册(新增)| 实际日志：|896132145 | DEV_REGISTER | 112.15.22.45 | 180140000001|akc08s92mnd9s| v1.0.2 | ios |

==业务日志全表==
时间	日志标志	公共字段	业务字段	日志备注
ldt	DEV_REGISTER	rip,cid,mac	客户端版本号1,客户端类型2	设备注册(新增)                                   done 
ldt	ACCOUNT_REGISTER	sid,aid,mac,anm,rip,cid	客户端版本号1,客户端类型2,检测到的客户端手机号3,	账户注册    done 
ldt	CREATE_ROLE	sid,aid,rid,rnm,mac,rip,cid	性别/职业4	角色注册                                        done 
ldt	ACCOUNT_LOGIN	sid,aid,mac,anm,cid	账号当前一级代币余量5,登录IP	账户登录                            done 
ldt	ROLE_LOGIN	sid,aid,anm,rid,rnm,mac,rlv,vip,cid	角色当前一级代币余量,登录IP	角色登录                    done 
ldt	ROLE_LOGOUT	sid,aid,rid	在线时长（秒）,退出类型6	角色退出
ldt	KEY_POINT	sid,aid,rid	功能点ID7	功能点                                                          暂时不做
ldt	GET_ITEM	sid,aid,rid,rlv,vip	物品ID串8,获得物品前数量,获得物品后数量,关联ID9,物品原因10	获得物品        done
ldt	REMOVE_ITEM	sid,aid,rid,rlv,vip	物品ID串8,获得物品前数量,获得物品后数量,关联ID,物品原因10	扣除物品        done
ldt	GET_MONEY	sid,aid,rid,rlv,vip	获得之前的数值,获得之后的数值,代币类型11,关联ID,货币原因12	获得代币        done
ldt	REMOVE_MONEY	sid,aid,rid,rlv,vip	扣除之前的数值,扣除之后的数值,代币类型,关联ID,货币原因12	扣除代币    done
ldt	EXP_CHANGE	sid,aid,rid	经验值类型13,获得之前的数值,获得之后的数值,经验值原因14	经验值变化              done
ldt	LEVEL_CHANGE	sid,aid,rid	级别类型15,升级前级别,升级前经验,升级后级别,升级后经验	级别变化                done
ldt	RECEIVE_QUEST	sid,aid,rid	任务类型16,任务ID17	领取任务  （rpg类的游戏才有，暂时先不管）                 无，不做
ldt	FINISH_QUEST	sid,aid,rid	任务类型16,任务ID17,奖励18,完成条件	完成任务                                done

ldt	PVE_INSTANCE	sid,aid,rid,rlv	副本类型19,副本ID20,副本名称,组队ID21	进入PVE副本                     done
ldt	PVE_FINISH	sid,aid,rid,rlv	副本类型19,副本ID20,组队ID21,是否胜利22,扫荡次数23,通关时长,通关评级	完成PVE副本 done
ldt	PVP_INSTANCE	sid,aid,rid,rlv	战斗ID24,战斗模式ID,战斗类型ID	进入PVP战斗                                 无
ldt	PVP_FINISH	sid,aid,rid,rlv	战斗ID24,战斗模式ID,战斗类型ID,场景ID,组队人数25,是否胜利,战斗时长,排名	完成PVP战斗 done
ldt	SHOPBUY	sid,aid,rid,rlv,vip	物品ID串8,物品数量,代币类型11,花费代币数量,商城类型26	商城购买                    done
ldt	NEWG	sid,aid,rid	引导类型id27,步骤N28	新手引导                                                        done
ldt	LOTTERY	sid,aid,rid,rlv,vip	抽奖类型29,获得物品30,花费代币类型11,扣除代币数	抽奖



1. 通过api接口抓取的日志  在dmp.py中的 bdc_logger 函数被调用

def module_funcname(hm, args, result_data):
    '''# module_funcname: module中的funcname接口的统计方法, 此函数命名规则：views中模块名_函数名
                            比如views.cards.open的统计方法命名为：cards_open
    args:
        env:
        args: 请求参数
        return_data: 比如views层函数处理后的result_data,
    returns:
        0    ---
        data:     需要记录的结果
    '''
    data={}
    return data


2. 通过 special_bdc_log 抓取的自定义日志，函数名以下划线 _ 开头，参数看具体需求自定义

def _xxx(user, *args, **kwargs):
    pass    

"""

import os
import time
import json
import uuid
from itertools import chain

import settings
from lib.utils.loggings import get_log, StatLoggingUtil
from lib.utils.encoding import force_unicode
from celery_app.aliyun_bdc_log import send_bdc_log_to_aliyun

from gconfig import game_config
from gconfig import get_str_words


BDC_EVENT_MAPPING = {
    ######## 非api接口，special_bdc_log 里自定义的动作类型 ########
    'account_login': '10004',
    'new_account': '10005',
    'role_logout': '10007',
    'get_money': '10008',
    'remove_money': '10009',
    'online_scene': '10010',

    'get_item': '10013',
    'remove_item': '10014',
    'level_change': '10017',
    'exp_change': '10017',

    ######## 非api接口，special_bdc_log 里自定义的动作类型 ########

    # 'user_register_name': 'CREATE_ROLE',
    'user_main': '10006',
    'user_guide': '10011',

    'shop_buy': '10015',
    'shop_gift_buy': '10015',
    'shop_resource_buy': '10015',
    'shop_mystical_buy': '10015',
    'shop_period_buy': '10015',
    'gacha_get_gacha': '10016',

    'mission_get_reward': '10019',
    'chapter_stage_chapter_stage_fight': '10021',
    'chapter_stage_auto_sweep': '10021',

    # 'mission_side_award': 'FINISH_QUEST',
    # 'private_city_battle_data': 'PVE_INSTANCE',
    # 'private_city_battle_end': 'PVE_FINISH',
    # 'high_ladder_battle_data': 'PVP_FINISH',
    # 'user_guide': 'NEWG',
}


def bdc_log_file(server_name):
    bdc_server_id = settings.get_bdc_server_id(server_name)
    bdc_game_id = settings.BDC_GAME_ID

    f_name = '%s_%s_%s-%s_%s.log' % (
        bdc_game_id,
        bdc_server_id,
        'eventinfo',
        os.getpid(),
        time.strftime('%F')
    )
    return 'bdc_event/%s' % f_name


def get_anm(account_name, tpid, cid=None):
    cid = cid or settings.get_bdc_channel_id(tpid)
    return '_'.join((cid, account_name.split('_')[-1]))


def get_bdc_api_base_info():
    """bdc 接口通用参数"""
    appkey = settings.BDC_APP_KEY
    platform = settings.BDC_PLATFORM
    return {
        'event_uuid': str(uuid.uuid1()),
        'event_time': int(time.time()),
        'event_time2': time.strftime('%F'),
        'appkey': appkey,
        'platform': platform,
        'buess_time': int(time.time()),
    }


def get_game_base_info(user, **kwargs):
    """bdc 业务通用参数"""
    cid = settings.get_bdc_channel_id(user.tpid)

    if user.__class__.__name__ == 'Account':
        # todo
        mm = None
        server_id = ''
        client_os = kwargs.get('client_os', 'ANDROID').upper()
        user_id = user.uid
        role_id = ''
        role_key = ''
        user_ip = kwargs.get('ip', '')
        device_id = kwargs.get('device', '')
    else:
        mm = user.mm
        server_id = user._server_name
        client_os = user.appid.upper() or 'ANDROID'
        user_id = user.account
        role_id = user.role
        role_key = user.uid
        user_ip = kwargs.get('ip', user.active_ip)
        device_id = kwargs.get('device', user.device)

    appkey = settings.BDC_APP_KEY
    platform = settings.BDC_PLATFORM
    # todo 账号ID（聚合SDK关联ID） 聚合SDK关联ID(HeroSDK返回的uid)
    return {
        # 'sid': sid,
        # 'cid': cid,
        # 'aid': user.account,
        # 'anm': anm,
        # 'rid': user.uid,
        # 'rlv': user.level,
        # 'vip': user.vip,

        'event_id': '',
        'event_uuid': str(uuid.uuid1()),
        'event_time': int(time.time()),
        'event_time2': time.strftime('%F'),
        'appkey': appkey,
        'platform': platform,

        'client_os': client_os,   # IOS|ANDROID|PAD|WEB
        'server_id': server_id,
        'channel_id': cid,              # todo 使用英雄互娱统一渠道ID配置表
        'app_channel_id': cid,          # todo 使用英雄互娱统一渠道ID配置表
        'device_id': device_id,

        'user_id': user_id,       # todo 账号ID（聚合SDK关联ID） 聚合SDK关联ID(HeroSDK返回的uid)
        'open_id': user_id,
        'role_id': role_id,
        'role_key': role_key,
        'transaction_id': mm.get_transaction_id() if mm else '',    # 事件关联ID
        'user_ip': user_ip,
        'buess_time': int(time.time()),

    }


def generate_log(data):
    return settings.BDC_LOG_DELITIMER.join((force_unicode(i) for i in data))


####################### 通过api接口抓取的动作 start ###############################


def user_guide(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)
    # sort = hm.get_argument('sort', is_int=True)
    # guide_id = hm.get_argument('guide_id', is_int=True)

    content = {
        'guide_id': data['sort'],
        'guide_num': data['guide_id'],
    }
    content.update(base_info)
    return content


def user_register_name(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)

    return [
        base_info['sid'],
        base_info['aid'],
        user.uid,
        user.name,
        user.device,
        user.register_ip,
        base_info['cid'],
        '-1',  # sex
    ]


def user_main(hm, args, data, **kwargs):
    """
    return
    :param hm:
    :param args:
    :param data:
    :param kwargs:
    :return:
    """
    user = hm.mm.user
    base_info = get_game_base_info(user)

    content = {
        'free_diamond_balance': user.diamond_free,
        'donate_diamond_balance': 0,
        'charge_diamond_balance': user.diamond_charge,
        'gold_balance': user.coin,
        'login_situation': user.appid.upper(),      # 登录场景
        'role_level': user.level,
        'vip_level': user.vip,

    }
    # content = {'user_balance': {'coin': user.coin}}
    content.update(base_info)
    return content


def _role_logout(user, **kwargs):
    base_info = get_game_base_info(user)

    content = {
        'role_level': user.level,
        'vip_level': user.vip,
        'free_diamond_balance': user.diamond_free,
        'donate_diamond_balance': 0,
        'charge_diamond_balance': user.diamond_charge,
        'gold_balance': user.coin,
        'final_scene': '',                          # 登出场景
        'final_action': kwargs['final_action'],     # 登出前操作
        'online_time': kwargs['duration'],          # 登出前操作
    }
    content.update(base_info)
    return content


def change_method_name_type(method):
    """修改函数名命名规则，改成驼峰命名，给bdc用"""
    d = []
    for i in method.split('.'):
        d.extend(i.split('_'))
    return ''.join((i.capitalize() for i in d))


def shop_buy(hm, args, data, **kwargs):
    """
    return [sid, aid, rid, rlv, vip, goods_id, goods_num, coin_type, coin_num, shop_type]
    :param hm:
    :param args:
    :param data:
    :param _client_cache:
    :param kwargs:
    :return:
    """
    user = hm.mm.user
    base_info = get_game_base_info(user)

    _bdc_event_info = data.pop('_bdc_event_info')
    cost = _bdc_event_info['cost'][0]

    method = change_method_name_type(hm.mm.action)
    content = {
        'role_level': user.level,
        'vip_level': user.vip,
        'product_id': _bdc_event_info['goods_id'],
        'product_num': _bdc_event_info['num'],
        'money_type': cost[0],
        'buy_cost': cost[2],
        'shop_type': method,

    }
    content.update(base_info)
    return content


shop_gift_buy = shop_buy
shop_resource_buy = shop_buy
shop_mystical_buy = shop_buy
shop_period_buy = shop_buy


def mission_get_reward(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)
    # 1每日任务 2档期任务 3新手任务 4随机任务  5活跃度 6 成就任务 7 新手引导任务
    tp_id = hm.get_argument('tp_id', 0, is_int=True)
    mission_id = hm.get_argument('mission_id', 0, is_int=True)
    content = {
        'task_type': tp_id,
        'task_id': mission_id,
        'rewards_info': json.dumps(data.get('reward', {})),
    }
    content.update(base_info)
    return content


def chapter_stage_chapter_stage_fight(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)

    stage = hm.get_argument('stage', '')
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    align = hm.get_argument('align', '')

    chapter_id, stage_id = [int(i) for i in stage.split('-')]
    align = align.split('_')
    # {pos_id: card_id}
    align = [(int(align[i * 2]), align[i * 2 + 1]) for i in range(len(align) / 2)]
    align.sort(key=lambda x: x[0])

    lineup = ';'.join([i[1] for i in align])
    iswin = 0 if data.get('win', True) else 1

    chapter_cfg = game_config.chapter[chapter_id]
    name = get_str_words(1, chapter_cfg['chapter_name'])
    content = {
        'pve_type': type_hard,
        'pve_id': stage,            # chapter_id-stage_id
        'pve_name': name,
        'team_id': 0,              # 组队id,  我们没有多人组队pve，队伍id就用0代替
        'iswin': iswin,             # 0 胜利 1 失败
        'lineup': lineup,           # 阵容，英雄id;英雄id;英雄id
        'complete_type': 0,         # 扫荡次数，扫荡次数：0，手动通关；1，扫荡一次；5，扫荡五次；以游戏实际情况分类
    }
    content.update(base_info)
    return content


def chapter_stage_auto_sweep(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)

    stage = hm.get_argument('stage', '')
    times = hm.get_argument('times', 1, is_int=True)
    type_hard = hm.get_argument('type_hard', 0, is_int=True)

    chapter_id, stage_id = [int(i) for i in stage.split('-')]
    # {pos_id: card_id}

    lineup = ''
    iswin = 0 if data.get('win', True) else 1

    chapter_cfg = game_config.chapter[chapter_id]
    name = get_str_words(1, chapter_cfg['chapter_name'])
    content = {
        'pve_type': type_hard,
        'pve_id': stage,            # chapter_id-stage_id
        'pve_name': name,
        'team_id': -1,              # 组队id,  我们没有多人组队pve，队伍id就用-1代替
        'iswin': iswin,             # 0 胜利 1 失败
        'lineup': lineup,           # 阵容，英雄id;英雄id;英雄id
        'complete_type': times,         # 扫荡次数，扫荡次数：0，手动通关；1，扫荡一次；5，扫荡五次；以游戏实际情况分类
    }
    content.update(base_info)
    return content


def private_city_battle_end(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)

    chapter_id = hm.get_argument('chapter_id', is_int=True)
    stage_id = hm.get_argument('stage_id', is_int=True)
    team = hm.get_mapping_argument('team', is_int=False, num=0)
    win = hm.get_argument('win', is_int=True)
    total_time = hm.get_argument('total_time', is_int=True)

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        base_info['rlv'],

        chapter_id,         # 副本类型
        stage_id,           # 副本id
        '-1',               # 组队id

        win,
        '0',                 # 扫荡次数
        total_time,         # 通关时长
        data['chapter_star'],                 # 通关评级

    ]


def high_ladder_battle_data(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)

    team = hm.get_mapping_argument('team', is_int=False, num=0)
    team_len = len([i for i in team if i])

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        base_info['rlv'],

        '',                 # 战斗id
        hm.mm.action,       # 战斗模式
        '',                 # 战斗类型
        '',                 # 场景id
        team_len,           # 组队人数
        data['win'],        # 是否胜利
        '',                 # 战斗时长
        data['new_rank'],   # 排名
    ]


def gacha_get_gacha(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_game_base_info(user)

    sort = hm.get_argument('sort', is_int=True)

    reward = {}
    _bdc_event_info = data.pop('_bdc_event_info')
    content = {
        'role_level': user.level,
        'vip_level': user.vip,
        'action_type': sort,
        'rewards_info': reward,
        'money_type': _bdc_event_info['cost_type'],
        'buy_cost': _bdc_event_info['cost_num'],
    }
    content.update(base_info)
    return content


####################### 通过api接口抓取的动作  end ###############################


####################### 通过 special_bdc_log 调用的自定义的动作  start###############################


def _account_login(account, **kwargs):
    """账号登录"""
    base_info = get_game_base_info(account, **kwargs)
    content = {'user_balance': {}}

    content.update(base_info)
    return content


def _new_account(hm, args, data, **kwargs):
    """创建角色"""
    user = hm.mm.user
    base_info = get_game_base_info(user, **kwargs)

    content = {
        'character_id': user.role,
        'role_name': user.name,
        'role_extra': '',
    }
    content.update(base_info)
    return content


def _money_change(user, **kwargs):
    base_info = get_game_base_info(user)

    content = {
        'role_level': user.level,
        'vip_level': user.vip,
        'before_balance': kwargs['before'],
        'after_balance': kwargs['after'],
        'money_type': kwargs['obj'],
        'reason_id': user.mm.action,
        'reason_info': {},
    }
    content.update(base_info)
    return content


def _level_change(user, **kwargs):
    old_lv, cur_lv = kwargs['old_lv'], kwargs['cur_lv']
    if old_lv == cur_lv:
        return {}
    base_info = get_game_base_info(user)

    content = {
        'point': kwargs['change_type'],
        'point_before': old_lv,
        'point_after': cur_lv,
    }
    content.update(base_info)
    return content


def _exp_change(user, **kwargs):
    base_info = get_game_base_info(user)
    content = {
        'point': kwargs['change_type'],
        'point_before': kwargs['old_exp'],
        'point_after': kwargs['cur_exp'],
    }
    content.update(base_info)
    return content


def _device_register(hm, args, data, **kwargs):
    return 
    user = hm.mm.user
    base_info = get_game_base_info(user)

    return [
        user.register_ip,
        base_info['cid'],
        user.device,
        hm.get_argument('version'),
        user.appid,
    ]


def _item_change(user, **kwargs):
    base_info = get_game_base_info(user)

    content = {
        'role_level': user.level,
        'vip_level': user.vip,
        'product_id': kwargs['obj'],
        'product_num': abs(kwargs['diff']),
        'reason_id': user.mm.action,
        'reason_info': {},

    }
    content.update(base_info)
    return content


####################### 通过 special_bdc_log 调用的自定义的动作  end ###############################


def bdc_online_scence_log(online_info):
    """在线统计，run_timer 里每五分钟调用一次
    :param online_info: [(server_id, role_info)]
    :return:
    """
    logs = []
    base_info = get_bdc_api_base_info()
    for server_id, role_num in online_info:
        content = {
            'event_id': BDC_EVENT_MAPPING['online_scene'],
            'server_id': server_id,
            'role_num': role_num
        }
        content.update(base_info)
        logs.append(content)
        if not len(logs) % 100:
            send_bdc_log_to_aliyun(logs)
            logs = []

    send_bdc_log_to_aliyun(logs)


def special_bdc_log(user, sort, **kwargs):
    """一些需要特殊处理的日志接口，直接在逻辑中调用。
    sort:
        - new_user: 新建用户
        - payment: 充值
    """
    ldt = kwargs.get('ldt') or time.strftime('%F %T')
    logger = bdc_log_file(user._server_name)
    # TODO generate_log

    if sort == 'new_account':
        hm = kwargs.pop('hm')
        data = _new_account(hm, {}, {}, **kwargs)

    elif sort == 'new_device':
        hm = kwargs.pop('hm')
        data = _device_register(hm, {}, {}, **kwargs)

    elif sort == 'role_logout':
        data = _role_logout(user, **kwargs)

    elif sort == 'exp_change':
        data = _exp_change(user, **kwargs)

    elif sort == 'level_change':
        data = _level_change(user, **kwargs)

    elif sort == 'account_login':
        data = _account_login(user, **kwargs)

    elif sort == 'get_item':
        data = _item_change(user, **kwargs)

    elif sort == 'remove_item':
        data = _item_change(user, **kwargs)

    elif sort == 'get_money':
        data = _money_change(user, **kwargs)

    elif sort == 'remove_money':
        data = _money_change(user, **kwargs)

    else:
        print 'no sort:---', sort
        return

    # TODO account login登录没有对应的server是master，默认走1服id ？
    f_name = bdc_log_file(user._server_name)
    log = get_log(f_name, logging_class=StatLoggingUtil, propagate=0)
    if not data:
        return

    event = BDC_EVENT_MAPPING[sort]
    if isinstance(data, list):
        for d in data:
            d['event_id'] = event
            log.info(json.dumps(d, separators=(',', ':')))
    else:
        data['event_id'] = event
        log.info(json.dumps(data, separators=(',', ':')))

    send_bdc_log_to_aliyun(data)



## TODO LIST
#  PVE_FINISH 扫荡次数怎么记录的
# ldt	PVE_FINISH	sid,aid,rid,rlv	副本类型19,副本ID20,组队ID21,是否胜利22,扫荡次数23,通关时长,通关评级	完成PVE副本

# pvp 没有战斗场景、id之类的
# ldt	PVP_INSTANCE	sid,aid,rid,rlv	战斗ID24,战斗模式ID,战斗类型ID	进入PVP战斗
# pvp 后端自动战斗，几百毫秒结束
# ldt	PVP_FINISH	sid,aid,rid,rlv	战斗ID24,战斗模式ID,战斗类型ID,场景ID,组队人数25,是否胜利,战斗时长,排名



# ldt	NEWG	sid,aid,rid	引导类型id27,步骤N28	新手引导
# ldt	LOTTERY	sid,aid,rid,rlv,vip	抽奖类型29,获得物品30,花费代币类型11,扣除代币数	抽奖
