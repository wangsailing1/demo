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
from itertools import chain

import settings
from lib.utils.loggings import get_log, StatLoggingUtil
from lib.utils.encoding import force_unicode
from gconfig import game_config
from gconfig import get_str_words

BDC_EVENT_MAPPING = {
    'user_register_name': 'CREATE_ROLE',
    'user_main': 'ROLE_LOGIN',
    'shop_buy': 'SHOPBUY',
    'mission_mission_award': 'FINISH_QUEST',
    'mission_side_award': 'FINISH_QUEST',
    'private_city_battle_data': 'PVE_INSTANCE',
    'private_city_battle_end': 'PVE_FINISH',
    'high_ladder_battle_data': 'PVP_FINISH',
    'user_guide': 'NEWG',
    'gacha_get_gacha': 'LOTTERY',
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


def get_base_info(user):
    cid = settings.get_bdc_channel_id(user.tpid)
    sid = settings.get_bdc_server_id(user._server_name)
    anm = get_anm(user.account, user.tpid, cid)

    return {
        'sid': sid,
        'cid': cid,
        'aid': user.account,
        'anm': anm,
        'rid': user.uid,
        'rlv': user.level,
        'vip': user.vip,
    }


def generate_log(data):
    return settings.BDC_LOG_DELITIMER.join((force_unicode(i) for i in data))


####################### 通过api接口抓取的动作 start ###############################


def user_guide(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)
    sort = hm.get_argument('sort', is_int=True)
    guide_id = hm.get_argument('guide_id', is_int=True)

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],

        sort,
        guide_id,
    ]


def user_register_name(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)

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
    return [sid,aid,anm,rid,rnm,mac,rlv,vip,cid]
    :param hm:
    :param args:
    :param data:
    :param kwargs:
    :return:
    """
    user = hm.mm.user
    base_info = get_base_info(user)
    remote_ip = hm.req.request.headers.get('X-Real-Ip', '') or hm.req.request.remote_ip

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['anm'],
        base_info['rid'],
        user.name,
        user.device,
        user.level,
        user.vip,
        base_info['cid'],
        user.diamond,
        remote_ip,
    ]


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
    base_info = get_base_info(user)

    _bdc_event_info = data.pop('_bdc_event_info')
    cost = _bdc_event_info['cost'][0]
    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        base_info['rlv'],
        base_info['vip'],
        _bdc_event_info['goods_id'],
        _bdc_event_info['num'],
        cost[0],
        cost[2],
        hm.get_argument('method'),
    ]


def mission_mission_award(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)

    task_id = hm.get_argument('task_id', is_int=True)
    config = game_config.mission_main.get(task_id)
    sort = config['sort']

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],

        sort,               # 任务类型 主线任务
        task_id,            # 任务id
        data.get('reward', []),         # 奖励
        hm.mm.action,                 # 完成条件
    ]


def mission_side_award(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)

    task_id = hm.get_argument('task_id', is_int=True)
    config = game_config.mission_side.get(task_id)
    sort = config['sort']

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],

        sort,               # 任务类型 主线任务
        task_id,            # 任务id
        data.get('reward', []),         # 奖励
        hm.mm.action,                 # 完成条件
    ]


def private_city_battle_data(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)

    chapter_id = hm.get_argument('chapter_id', is_int=True)     # 1
    stage_id = hm.get_argument('stage_id', is_int=True)         # 10100
    team = hm.get_mapping_argument('team', is_int=False, num=0)

    chapter_cfg = game_config.chapter[chapter_id]
    name = get_str_words(0, chapter_cfg['chapter_name'])
    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        base_info['rlv'],

        chapter_id,         # 副本类型
        stage_id,           # 副本id
        name,                 # 副本名称
        '-1',               # 组队id,  我们没有多人组队pve，队伍id就用-1代替

    ]


def private_city_battle_end(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)

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
    base_info = get_base_info(user)

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
    base_info = get_base_info(user)

    sort = hm.get_argument('sort', is_int=True)
    count = hm.get_argument('count', is_int=True)

    reward = data['reward']
    _bdc_event_info = data.pop('_bdc_event_info')
    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        base_info['rlv'],
        base_info['vip'],

        sort,
        reward,
        _bdc_event_info['cost_type'],
        _bdc_event_info['cost_num']
    ]


####################### 通过api接口抓取的动作  end ###############################


####################### 通过 special_bdc_log 调用的自定义的动作  start###############################


def _device_register(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)

    return [
        user.register_ip,
        base_info['cid'],
        user.device,
        hm.get_argument('version'),
        user.appid,
    ]


def _new_account(hm, args, data, **kwargs):
    user = hm.mm.user
    base_info = get_base_info(user)

    return [
        base_info['sid'],
        base_info['aid'],
        user.device,
        base_info['anm'],
        user.register_ip,
        base_info['cid'],
        hm.get_argument('version'),
        user.appid,
        '',             # TODO telephone,
    ]


def _exp_change(user, **kwargs):
    base_info = get_base_info(user)
    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        kwargs['change_type'],       # 经验类型
        kwargs['old_exp'],
        kwargs['cur_exp'],
        user.mm.action,
    ]


def _role_logout(user, **kwargs):
    base_info = get_base_info(user)
    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],

        kwargs['duration'],
        '',                     # 退出类型
    ]


def _level_change(user, **kwargs):
    old_lv, cur_lv = kwargs['old_lv'], kwargs['cur_lv']
    if old_lv == cur_lv:
        return []
    base_info = get_base_info(user)
    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        kwargs['change_type'],            # 级别类型
        old_lv,
        kwargs['old_exp'],
        cur_lv,
        kwargs['cur_exp'],
        user.mm.action
    ]


def _account_login(account, **kwargs):
    cid = settings.get_bdc_channel_id(account.tpid)
    anm = get_anm(account.uid, account.tpid, cid)
    return [
        '',         # sid
        account.uid,
        kwargs['device'],
        anm,
        cid,
        '',
        kwargs['ip'],
    ]


def _item_change(user, **kwargs):
    base_info = get_base_info(user)

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        base_info['rlv'],
        base_info['vip'],

        kwargs['item_id'],
        kwargs['before'],
        kwargs['after'],
        '',
        user.mm.action,
    ]


def _money_change(user, **kwargs):
    base_info = get_base_info(user)

    return [
        base_info['sid'],
        base_info['aid'],
        base_info['rid'],
        base_info['rlv'],
        base_info['vip'],

        kwargs['before'],
        kwargs['after'],
        kwargs['obj'],
        '',                 # 关联id
        user.mm.action,
    ]


####################### 通过 special_bdc_log 调用的自定义的动作  end ###############################


def special_bdc_log(user, sort, **kwargs):
    """一些需要特殊处理的日志接口，直接在逻辑中调用。
    sort:
        - new_user: 新建用户
        - payment: 充值
    """
    ldt = kwargs.get('ldt') or time.strftime('%F %T')
    logger = bdc_log_file(user._server_name)
    # TODO generate_log

    prefix = [ldt]
    if sort == 'new_account':
        hm = kwargs['hm']
        data = _new_account(hm, {}, {})
        event = 'ACCOUNT_REGISTER'
        prefix.append(event)

    elif sort == 'new_device':
        hm = kwargs['hm']
        data = _device_register(hm, {}, {})
        event = 'DEV_REGISTER'
        prefix.append(event)

    elif sort == 'role_logout':
        data = _role_logout(user, **kwargs)
        event = 'ROLE_LOGOUT'
        prefix.append(event)

    elif sort == 'exp_change':
        data = _exp_change(user, **kwargs)
        event = 'EXP_CHANGE'
        prefix.append(event)

    elif sort == 'level_change':
        data = _level_change(user, **kwargs)
        event = 'LEVEL_CHANGE'
        prefix.append(event)

    elif sort == 'account_login':
        data = _account_login(user, **kwargs)
        event = 'ACCOUNT_LOGIN'
        prefix.append(event)

    elif sort == 'get_item':
        data = _item_change(user, **kwargs)
        event = 'GET_ITEM'
        prefix.append(event)

    elif sort == 'remove_item':
        data = _item_change(user, **kwargs)
        event = 'REMOVE_ITEM'
        prefix.append(event)

    elif sort == 'get_money':
        data = _money_change(user, **kwargs)
        event = 'GET_MONEY'
        prefix.append(event)

    elif sort == 'remove_money':
        data = _money_change(user, **kwargs)
        event = 'REMOVE_MONEY'
        prefix.append(event)

    else:
        print 'no sort:---', sort
        return

    # TODO account login登录没有对应的server是master，默认走1服id ？
    f_name = bdc_log_file(user._server_name)
    log = get_log(f_name, logging_class=StatLoggingUtil, propagate=0)
    if not data:
        return
    if isinstance(data[0], list):
        for d in data:
            log.info(settings.BDC_LOG_DELITIMER.join((force_unicode(i) for i in chain(prefix, d))))
    else:
        log.info(settings.BDC_LOG_DELITIMER.join((force_unicode(i) for i in chain(prefix, data))))



## TODO LIST
#  PVE_FINISH 扫荡次数怎么记录的
# ldt	PVE_FINISH	sid,aid,rid,rlv	副本类型19,副本ID20,组队ID21,是否胜利22,扫荡次数23,通关时长,通关评级	完成PVE副本

# pvp 没有战斗场景、id之类的
# ldt	PVP_INSTANCE	sid,aid,rid,rlv	战斗ID24,战斗模式ID,战斗类型ID	进入PVP战斗
# pvp 后端自动战斗，几百毫秒结束
# ldt	PVP_FINISH	sid,aid,rid,rlv	战斗ID24,战斗模式ID,战斗类型ID,场景ID,组队人数25,是否胜利,战斗时长,排名



# ldt	NEWG	sid,aid,rid	引导类型id27,步骤N28	新手引导
# ldt	LOTTERY	sid,aid,rid,rlv,vip	抽奖类型29,获得物品30,花费代币类型11,扣除代币数	抽奖
