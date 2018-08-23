#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

from lib.sdk_platform.sdk_hero import unmark_data, mark_sign
from lib.core.environ import ModelManager
from models.server import ServerConfig
from gconfig import game_config
import settings

secret = 'be6fdcb773f5ffc187aaf48518704305'


def user_info(req):
    """
    英雄互娱助手sdk获取玩家信息
    :param hm:
        data: {
            "roleid": 123,
            "serverid": 1,
        }
    :return:
    """
    data = req.get_argument('data', '')
    sign = req.get_argument('sign', '')
    timestamp = req.get_argument('timestamp', '')

    msg = u'成功'
    code = 0
    server_name = ''
    role_name = ''
    level = 1
    vip = 0
    active_time = 0
    reg_time = 0

    new_sign = mark_sign(secret, {'data': data, 'timestamp': timestamp})
    if sign != new_sign:
        code = -2
        msg = u'签名验证失败'
    else:
        try:
            d = unmark_data(data)

            role_id = d['roleid']
            server_id = d['serverid']
            server_id = '%s%s' % (settings.UID_PREFIX, server_id)
            sc = ServerConfig.get()

            mm = ModelManager(role_id)
            server_name = sc.config_value[server_id]['name']
            role_name = mm.user.name
            level = mm.user.level
            vip = mm.user.vip
            reg_time = mm.user.reg_time
            active_time = mm.user.active_time
        except:
            code = -1
            msg = u"数据解析失败"

    result = {
        "code": code,
        "msg": msg,
        "data": {
            "servername": server_name,
            "rolename": role_name,
            "level": level,
            "viplevel": vip,
            "lastlogin_time": active_time,
            "register_time": reg_time,
        }
    }

    return result


def send_prize(req):
    """
    英雄互娱助手sdk 回调问卷发奖接口
    :param hm:
        data = {
            roleid:
            serverid:
            mailTitle:
            mailContrnt:
            itemInfo: [{'propid': "1", 'pronum': 2, 'dateline': 0}]
        }
    :return:
    """
    sign = req.get_argument('sign', '')
    timestamp = req.get_argument('timestamp', '')
    data = req.get_argument('data', '')

    code = 0
    msg = u"成功"

    new_sign = mark_sign(secret, {'data': data, 'timestamp': timestamp})
    if sign != new_sign:
        code = -2
        msg = u'签名验证失败'
    else:
        try:
            d = unmark_data(data)

            role_id = d['roleid']
            title = d['mailTitle']
            content = d['mailContent']
            item_info = d['itemInfo']

            gift = []
            for i in item_info:
                item_id = int(i['propid'])
                item_num = int(i['pronum'])
                if item_id not in game_config.use_item:
                    continue
                gift.append([3, item_id, item_num])

            if not gift:
                code = -4
                msg = u'没有奖励'
            else:
                mm = ModelManager(role_id)
                if not mm.user.question_done:
                    mail_dict = mm.mail.generate_mail(
                        content,
                        title=title,
                        gift=gift,
                    )
                    mm.mail.add_mail(mail_dict)
                    mm.user.question_done = True
                    mm.user.save()
                else:
                    code = -3
                    msg = u'已发过奖励了'

        except:
            code = -1
            msg = u'数据解析失败'

    result = {
        "code": code,
        "msg": msg,
        "data": {}
    }

    return result


def ban_uid(req):
    """
    聊天封号禁言接口
    :param req:
    :return:
    """
    serverid = req.get_argument('serverid', '')
    roleid = req.get_argument('roleid', '')
    locktime = req.get_argument('locktime', '')
    ban_type = req.get_argument('type', '')
    reason = req.get_argument('reason', '')

    code = 0
    msg = u'成功'
    if not serverid or not roleid or not locktime or not ban_type:
        code = -1
        msg = u'缺少参数'

    else:   # 封号，禁言
        try:
            ban_type = int(ban_type)
            mm = ModelManager(roleid)

            if ban_type == 1:       # 封号
                mm.user.ban_user(1, locktime, uname=u'hero', ban_reason=reason)
                mm.user.save()
            elif ban_type == 2:     # 禁言
                mm.user.bchat_user(1, locktime, uname=u'hero', ban_reason=reason)
                mm.user.save()
            else:
                code = -2
                msg = u'type error'

        except:
            code = -3
            msg = u'角色ID错误'

    return {
        'code': code,
        'msg': msg,
    }


def unban_uid(req):
    """
    解封号解禁言接口
    :param req:
    :return:
    """
    serverid = req.get_argument('serverid', '')
    roleid = req.get_argument('roleid', '')
    ban_type = req.get_argument('type', '')

    code = 0
    msg = u'成功'
    if not serverid or not roleid or not ban_type:
        code = -1
        msg = u'缺少参数'

    else:   # 解封号，解禁言 todo
        try:
            ban_type = int(ban_type)
            mm = ModelManager(roleid)

            if ban_type == 1:  # 解封号
                mm.user.ban_user(0, 0, ban_time=0)
                mm.user.save()
            elif ban_type == 2:  # 解禁言
                mm.user.bchat_user(0, 0, ban_time=0)
                mm.user.save()
            else:
                code = -2
                msg = u'type error'

        except:
            code = -3
            msg = u'角色ID错误'

    return {
        'code': code,
        'msg': msg,
    }


def mail_send(req):
    """
    邮件通知
    :param req:
    :return:
    """
    serverid = req.get_argument('serverid', '')
    roleid = req.get_argument('roleid', '')
    title = req.get_argument('title', '')
    content = req.get_argument('content', '')

    code = 0
    msg = u'成功'
    if not serverid or not roleid or not title or not content:
        code = -1
        msg = u'缺少参数'

    else:
        try:
            mm = ModelManager(roleid)
            mail_dict = mm.mail.generate_mail(
                content,
                title=title,
            )
            mm.mail.add_mail(mail_dict)
        except:
            code = -2
            msg = u'角色ID错误'

    return {
        'code': code,
        'msg': msg,
    }


def server_list(req):
    """
    区服列表
    :param req:
    :return:
    """
    data = []

    sc = ServerConfig.get()

    for sid, sinfo in sc.yield_open_servers():
        server_name = sinfo['name']
        _type = settings.HERO_SERVER_TYPE
        server_id = settings.get_server_num(sid)
        is_test = 1 if settings.DEBUG else 0
        joined_id = 0
        father_server = settings.get_father_server(sid)
        if father_server != sid:
            joined_id = settings.get_server_num(father_server)
        data.append({
            'server_name': server_name,
            'type': _type,
            'server_id': server_id,
            'is_test': is_test,
            'joined_id': joined_id,
        })

    return {
        'code': 0,
        'msg': u'成功',
        'data': data,
    }


def ban_info(req):
    """
    IM角色查询接口
    :param req:
    :return:
    """
    serverid = req.get_argument('serverid', '')
    roleid = req.get_argument('roleid', '')
    rolename = req.get_argument('rolename', '')

    code = 0
    msg = u'成功'
    data = {}

    if not serverid or (not roleid and not rolename):
        code = -1
        msg = u'缺少参数'

    else:
        try:
            if roleid:
                mm = ModelManager(roleid)
            else:
                _mm = ModelManager('%s%s1234567' % (settings.UID_PREFIX, serverid))
                uids = _mm.user.get_uid_by_name(rolename)
                if not uids:
                    raise
                mm = ModelManager(uids.pop())

            if mm.user.is_ban:
                ban_type = 1
                bantime = mm.user.ban_expire
                banreason = mm.user.ban_reason
            elif mm.user.ban_chat:
                ban_type = 2
                bantime = mm.user.bchat_expire
                banreason = mm.user.bchat_reason
            else:
                ban_type = 0
                bantime = 0
                banreason = ''

            data = {
                'viplevel': mm.user.vip,    # VIP等级
                'register_time': mm.user.reg_time,  # 注册时间
                'roleid': mm.uid,    # 角色ID
                'serverid': str(serverid),  # 区服ID
                'rolename': mm.user.name,   # 角色名称
                'level': mm.user.level,     # 等级
                'totalpay': mm.user_payment.charge_price,  # 累计充值
                'uid': mm.uid,   # 玩家ID唯一标识 （非必须）
                'diamond': mm.user.diamond, # 当前钻石
                'lastlogin_time': mm.user.active_time,    # 最后登录时间
                'bantime': bantime,   # 角色解封时间  比如 2018-02-03 12:00:00解封，则为：1517630400
                'banreason': banreason, # 封禁原因
                'ban_type': ban_type,  # 当前封禁状态 :1封号 2禁言 0未封禁
            }
        except:
            code = -2
            msg = u'没有查到角色信息'

    return {
        'code': code,
        'msg': msg,
        'data': data,
    }
