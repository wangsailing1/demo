# -*- coding:utf-8 -*-

import time
import datetime
import cPickle as pickle

import settings
from lib.db import ModelTools
from admin import auth
from gconfig import game_config


def require_permission(view_func):
    """
    装饰器，用于判断管理后台的帐号是否有权限访问
    """

    def wrapped_view_func(request, *args, **kwargs):

        path = request.request.path
        admin = auth.get_admin_by_request(request)
        request.uname = admin.username if admin else 'default'
        # 所有不进行登录直接访问后续页面的请求都踢回登录页面
        if not settings.DEBUG:
            if admin is None:
                return request.redirect("/%s/admin/gs/login/" % settings.URL_PARTITION)
            elif not admin.is_super and not admin.check_permission(request.module_name, request.method_name):
                Logging(admin).add_admin_logging(request, path, 3)
                return request.finish(u'没权限')
                # return request.redirect("/%s/admin/gs/login/" % settings.URL_PARTITION)

        result = view_func(request, *args, **kwargs)

        if view_func.func_name == path.split('/')[-2]:
            Logging(admin).add_admin_logging(request, path, 1)

        return result

    return wrapped_view_func


class Logging(ModelTools):
    SERVER_NAME = 'master'

    EXPIRE_DAY = 30

    IGNORE = ['menu/top', 'adminlog']

    def __init__(self, admin):
        self.admin = admin
        self._key = self.make_key_cls(time.strftime('%Y-%m-%d'), self.SERVER_NAME)
        self.redis = self.get_redis_client(self.SERVER_NAME)

    def log_contrast(self, request, path):
        try:
            if '/admin/index/' in path:
                return u'登录', ''
            elif '/admin/config/upload/' in path:
                config_name = request.arguments.get('config_name')
                return u'修改游戏配置', config_name
            elif '/admin/virtual_pay/' in path:
                params = dict(request.request.arguments.iteritems())
                return u'后台虚拟充值', params.__str__()
            elif '/admin/give_item_commit/' in path:
                keys = [(item.rsplit('_', 1)[-1], num[0]) for item, num in request.request.arguments.iteritems()
                        if 'item_num' in item and int(num[0])]
                return u'赠送道具', str(keys)
            elif '/admin/give_card_commit/' in path:
                arguments = request.request.arguments
                cards = [(k, int(arguments.get('card_lv_%s' % k, ['0'])[0]),
                          int(arguments.get('card_evolv_%s' % k, ['0'])[0]),
                          int(arguments.get('card_num_%s' % k, ['0'])[0]))
                         for k in game_config.character_detail if int(arguments.get('card_num_%s' % k, ['0'])[0])]
                return u'赠送卡牌', str(cards)
            elif '/admin/give_equip_commit/' in path:
                arguments = request.request.arguments
                equips = [(k, int(arguments.get('equip_lv_%s' % k, ['0'])[0]),
                           int(arguments.get('equip_num_%s' % k, ['0'])[0]))
                          for k in game_config.equip if int(arguments.get('equip_lv_%s' % k, ['0'])[0])
                          and int(arguments.get('equip_num_%s' % k, ['0'])[0])]
                return u'赠送装备', equips
            elif '/admin/give_gem_commit/' in path:
                arguments = request.request.arguments
                gems = [(k, int(arguments.get('gem_num_%s' % k, ['0'])[0]))
                        for k in game_config.gem if int(arguments.get('gem_num_%s' % k, ['0'])[0])]
                return u'赠送宝石', gems
            elif '/admin/give_gem_fate_commit/' in path:
                arguments = request.request.arguments
                gems = [(k, int(arguments.get('gem_num_%s' % k, ['0'])[0]))
                        for k in game_config.gem_fate if int(arguments.get('gem_num_%s' % k, ['0'])[0])]
                return u'赠送命运宝石', gems

            elif '/admin/give_god_stone_commit/' in path:
                arguments = request.request.arguments
                god_stones = [(k, int(arguments.get('god_stone_num_%s' % k, ['0'])[0]))
                              for k in game_config.god_stone if int(arguments.get('god_stone_num_%s' % k, ['0'])[0])]
                return u'赠送圣石', god_stones
            elif '/admin/give_seed_commit/' in path:
                arguments = request.request.arguments
                seeds = [(k, int(arguments.get('seed_num_%s' % k, ['0'])[0]))
                         for k in game_config.seed if int(arguments.get('seed_num_%s' % k, ['0'])[0])]
                return u'赠送种子', seeds
            else:
                params = dict(request.request.arguments.iteritems())
                return '%s' % path, params.__str__()
        except:
            params = dict(request.request.arguments.iteritems())
            return '%s' % path, params.__str__()

    def add_admin_logging(self, request, path, status):
        """添加后台记录
        args:
            method:
            args: 请求参数
            data: 结果
        """
        for ignore in self.IGNORE:
            if ignore in path:
                return

        action, args = self.log_contrast(request, path)  # 动作
        result = {
            'admin': self.admin.username if self.admin else '',  # 后台账号
            'action': action,
            'dt': time.strftime('%Y-%m-%d %H:%M:%S'),  # 操作时间
            'args': args,  # 参数
            'status': status,  # 状态 1.成功 2.失败 3.权限问题
            'ip': request.request.headers.get('X-Real-Ip', ''),
        }
        self.redis.lpush(self._key, pickle.dumps(result, pickle.HIGHEST_PROTOCOL))
        self.redis.expire(self._key, self.EXPIRE_DAY * 3)

    def get_all_logging(self, day=EXPIRE_DAY):
        data = []
        now = datetime.datetime.now()
        for i in [(now - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in xrange(0, day)]:
            data.extend(self.get_logging(i))
        return data

    def get_logging(self, time_str):
        """ 获取指定时间的日志

        :param time_str: "%Y-%m-%d"
        :return:
        """
        data = []
        key = self.make_key_cls(time_str, self.SERVER_NAME)
        for k in self.redis.lrange(key, 0, -1):
            data.append(pickle.loads(k))
        return data


class ApprovalPayment(ModelTools):
    """ 审批支付

    """
    SERVER_NAME = 'master'

    EXPIRE_DAY = 10

    def __init__(self):
        super(ApprovalPayment, self).__init__()
        self._key = self.make_key(self.__class__.__name__, server_name=self.SERVER_NAME)
        # 审批后的key
        self._key_approval = self.make_key('%s_%s' % (self.__class__.__name__, time.strftime('%Y-%m-%d')),
                                           server_name=self.SERVER_NAME)
        self.redis = self.get_redis_client(self.SERVER_NAME)

    def get_all_payment(self):
        """

        :return:
        """
        data = self.redis.hgetall(self._key)
        result = {}
        for key, value in data.iteritems():
            result[key] = pickle.loads(value)
        return result

    def get_payment(self, key):
        """

        :return:
        """
        data = self.redis.hget(self._key, key)
        return pickle.loads(data) if data else {}

    def add_payment(self, admin, uid, goods_id, reason, times, tp, act_id, act_item_id):
        """ 增加审批支付

        :param admin: admin账号
        :param uid: 充值的uid
        :param goods_id: 物品id
        :param reason: 理由
        :param times: 次数
        :return:
        """
        now = int(time.time())
        data = {
            'admin': admin,
            'uid': uid,
            'goods_id': goods_id,
            'reason': reason,
            'times': times,
            'dt': now,
            'approval': '',  # 审批者
            'status': 0,  # 状态0,为审批时, 1为同意, 2为拒绝
            'tp': tp,
            'act_id': act_id,
            'act_item_id': act_item_id,
        }
        key = '%s_%s' % (admin, now)
        self.redis.hset(self._key, key, pickle.dumps(data, pickle.HIGHEST_PROTOCOL))
        return key

    def remove_payment(self, key):
        """ 删除审批支付

        :param key:
        :return:
        """
        self.redis.hdel(self._key, key)

    def add_approval_payment(self, data):
        """ 增加审批支付结果

        :param key:
        :param data:
        :return:
        """
        self.redis.lpush(self._key_approval, pickle.dumps(data, pickle.HIGHEST_PROTOCOL))

    def approval_payment(self, admin, key, refuse=False, pay_tp=''):
        """ 审批支付

        :param key:
        :param refuse: 拒绝，默认为同意
        :return:
        """
        from logics.payment import virtual_pay_by_admin
        # from logics.user import UserLogic
        from lib.core.environ import ModelManager
        pay = self.get_payment(key)
        if pay:
            flag = False
            if not refuse:
                # 同意
                pay['status'] = 1
                # u = mm.get(pay['uid'])
                mm = ModelManager(pay['uid'])
                for i in xrange(int(pay['times'])):
                    flag = virtual_pay_by_admin(mm, pay['goods_id'], pay['admin'], pay['reason'], pay['tp'],
                                                act_id=pay['act_id'], act_item_id=pay['act_item_id'])
            else:
                # 拒绝
                pay['status'] = 2
            pay['approval'] = admin
            pay['argee_time'] = int(time.time())
            self.add_approval_payment(pay)
            self.remove_payment(key)
            return flag
        return False

    def get_all_approval_log(self, day=EXPIRE_DAY):
        data = []
        now = datetime.datetime.now()
        for i in [(now - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in xrange(0, day)]:
            data.extend(self.get_logging(i))
        return data

    def get_logging(self, time_str):
        """ 获取指定时间的日志

        :param time_str: "%Y-%m-%d"
        :return:
        """
        data = []
        key = self.make_key_cls('%s_%s' % (self.__class__.__name__, time_str), server_name=self.SERVER_NAME)
        for k in self.redis.lrange(key, 0, -1):
            data.append(pickle.loads(k))
        return data


Logging('yunfei.yan')
