#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import importlib
import time
import json
import traceback
import cStringIO
import pstats
import cProfile as profile

import tornado.web
import tornado.websocket

from lib.utils.debug import print_log
from lib.utils.debug import error_mail
from lib.statistics.dmp import stat
from handler_tools import to_json
import handler_tools
import settings
from lib.core.handlers.htornado import BaseRequestHandler
from lib.core.environ import HandlerManager
from return_msg_config import get_msg_str, i18n_msg
from gconfig import game_config
from models.logging import Logging
from handler_tools import to_json


def lock(func):

    ignore_api_module = []
    ignore_api_method = ['user.guide', 'user.get_red_dot', 'star_reward.index', 'endless.index', 'big_world.login', 'big_world.battle_data']
    # 需要排队的接口
    retry_module = ['big_world']

    def error(handler, msg=''):
        d = {
            'status': 9998,
            'data': {},
            'msg': msg,
            'user_status': {},
        }

        r = json.dumps(d, ensure_ascii=False, encoding="utf-8", indent=2)
        handler.write(r)
        handler.finish()

    def wrapper(handler, *args, **kwargs):
        if handler.hm is None:
            error(handler, 'hm is none')
            return

        method_param = handler.hm.req.get_argument('method')
        module_name, method_name = method_param.split('.')

        if not settings.DEBUG and handler.hm.mm and \
                module_name not in ignore_api_module and method_param not in ignore_api_method:
            user = handler.hm.mm.user
            _client = user.redis
            lock_key = user.make_key_cls('lock.%s' % user.uid, user._server_name)
            retry_times = 3

            while True:
                now = time.time()
                ts = now + 10
                flag = _client.setnx(lock_key, ts)
                if flag:
                    _client.expire(lock_key, 5)

                try:
                    if flag or (now > float(_client.get(lock_key)) and now > float(_client.getset(lock_key, ts))):
                        break
                    else:
                        if module_name in retry_module and retry_times > 0:
                            time.sleep(0.05)
                        else:
                            error(handler, i18n_msg.get(19, handler.hm.req.get_argument('lan', '1')))
                            return
                except:
                    print_log(traceback.print_exc())
                    error(handler, i18n_msg.get(20, handler.hm.req.get_argument('lan', '1')))
                    return

                retry_times -= 1
                if retry_times < 0:
                    break

            result = func(handler, *args, **kwargs)

            t1 = _client.get(lock_key)
            if t1 is not None and time.time() < float(t1):
                _client.delete(lock_key)
        else:
            result = func(handler, *args, **kwargs)

        return result

    return wrapper


class LoginHandler(BaseRequestHandler):
    """ 登录处理

    """
    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def initialize(self):
        """ 初始化操作

        :return:
        """
        self.hm = HandlerManager(self)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def result_info(self, rc, data=None):
        """ 返回信息

        :param rc:
        :param data:
        :param call_status: rc不为0时, 调用是否成功, 默认失败False
        :return:
        """
        msg = ''
        if data is None:
            data = {}

        if rc:
            if data:
                msg = data.get('custom_msg')
            if not msg:
                msg = get_msg_str(self.get_argument('lan', '1')).get(rc)
            if not msg:
                method_param = 'account.%s' % self.get_argument('method')
                msg = get_msg_str(self.get_argument('lan', '1')).get(method_param, {}).get(rc, method_param + '_error_%s' % rc)

        return rc, data, msg, None

    def handler(self):
        """ 处理

        :return:
        """

        rc, data, msg, mm = self.api()

        result = handler_tools.result_generator(rc, data, msg, mm)

        try:
            self.write(result)
        finally:
            self.finish()

    # @stat
    def api(self):

        method_name = self.get_argument('method', 'new_user')

        try:
            module = importlib.import_module('views.account')
        except ImportError:
            print_log(traceback.print_exc())
            return self.result_info('error_module')

        method = getattr(module, method_name, None)
        if method is None:
            return self.result_info('error_method')

        if callable(method):
            rc, data = method(self.hm)
            if rc != 0:
                return self.result_info(rc)

            return self.result_info(rc, data)
        return self.result_info('error_not_call_method')

    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def get(self):
        """

        :return:
        """
        self.handler()

    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def post(self):
        """

        :return:
        """
        self.handler()


class AdminHandler(BaseRequestHandler):

    def get(self, module_name, func_name=None):
        """ get请求

        :param module_name:
        :param func_name:
        :return:
        """
        if func_name:
            module = importlib.import_module('admin.%s' % module_name)
            method = getattr(module, func_name)
            self.module_name = module_name
            self.method_name = func_name
        else:
            module = importlib.import_module('admin.menu')
            method = getattr(module, module_name)
            self.module_name = 'menu'
            self.method_name = module_name
        return method(self)

    def post(self, module_name, func_name=None):
        """ post请求

        :param module_name:
        :param func_name:
        :return:
        """
        return self.get(module_name, func_name=func_name)


class APIRequestHandler(BaseRequestHandler):
    """ 统一的API Handler

    全部API处理公共接口
    """

    # 判断重试接口 可忽略的接口、模块
    retry_api_ignore_api_module = []
    retry_api_ignore_api_method = []

    # 主线、支线任务自动领取接口
    AUTO_RECEIVE_MISSION_AWARD_FUNC = ['user.main', 'user.talk_npc']
    # 主线、支线任务
    MISSION_TASK_UPDATE_FUNC = ['user.buy_point', 'user.buy_silver', 'private_city.sweep', 'shop.buy', 'shop.dark_buy',
                                'shop.guild_shop_buy', 'shop.high_ladder_buy', 'shop.donate_buy', 'shop.rally_buy', 'shop.box_shop_buy',
                                'shop.king_war_buy', 'star_array.add_point', 'team_skill.up_skill_mastery']

    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def initialize(self):
        """ 初始化操作

        :return:
        """
        self.hm = HandlerManager(self)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def result_info(self, rc, data=None):
        """ 返回信息

        :param rc:
        :param data:
        :return:
        """
        msg = ''
        if data is None:
            data = {}

        if rc:
            if data:
                msg = data.get('custom_msg')
            if not msg:
                msg = get_msg_str(self.get_argument('lan', '1')).get(rc)
            if not msg:
                method_param = self.get_argument('method')
                msg = get_msg_str(self.get_argument('lan', '1')).get(method_param, {}).get(rc, method_param + '_error_%s' % rc)

        return rc, data, msg, self.hm.mm

    @lock
    def handler(self):
        """ 处理

        :return:
        """
        method_param = self.get_argument('method')
        module_name, method_name = method_param.split('.')
        # 每个请求生成的时间戳
        __ts = self.get_argument('__ts', '')

        retry_api_flag = '%s%s' % (method_param, __ts)

        # 判断是否是重试api
        user_logging = Logging(self.hm.uid)
        if self.get_argument('kvretry', ''):
            last_api_data = user_logging.get_last_api_data()
            if last_api_data:
                if last_api_data['m'] == retry_api_flag:
                    self.set_header('Content-Type', 'application/json; charset=UTF-8')
                    self.write(last_api_data['d'])
                    self.finish()
                    return

        ################## 线上分析接口性能 ###########################
        if self.get_argument('__check_profile', ''):
            prof = profile.Profile()
            prof.runctx('rc, data, msg, mm = self.api()', globals(), locals())

            out = cStringIO.StringIO()
            stats = pstats.Stats(prof)
            stats.stream = out
            stats.strip_dirs().sort_stats(2).print_stats()

            result = out.getvalue()
            self.write(result)
            self.finish()
            return
        ################## 线上分析接口性能 ###########################

        rc, data, msg, mm = self.api()
        result = handler_tools.result_generator(rc, data, msg, mm)

        # 记录最后一次api返回数据
        if rc == 0:
            if module_name not in self.retry_api_ignore_api_module and \
                            method_param not in self.retry_api_ignore_api_method:
                user_logging.add_last_api_data(retry_api_flag, result)

        try:
            self.write(result)
        finally:
            self.finish()

    def handler_error(self, rc):
        """

        :param rc:
        :return:
        """
        rc, data, msg, mm = self.result_info(rc)
        result = handler_tools.result_generator(rc, data, msg, mm)
        try:
            self.write(result)
        finally:
            self.finish()

    @stat
    def api(self):
        """ API统一调用方法
        """
        user = self.hm.mm.user
        # ########## 封号 start #################
        ban_info = user.get_ban_info()
        if ban_info:
            return self.result_info('error_17173', {'custom_msg': ban_info})
            # ########## 封号 end #################

        # ########## 封ip start #################
        uip = self.hm.req.request.headers.get('X-Real-Ip', '') or self.hm.req.request.remote_ip
        banip_info = user.get_banip_info(uip)
        if banip_info:
            return self.result_info('error_17173', {'custom_msg': banip_info})
            # ########## 封ip end #################

        method_param = self.get_argument('method')
        module_name, method_name = method_param.split('.')

        try:
            module = importlib.import_module('views.%s' % module_name)
        except ImportError:
            print_log(traceback.print_exc())
            return self.result_info('error_module')

        method = getattr(module, method_name, None)
        if method is None:
            return self.result_info('error_method')

        if callable(method):
            pre_status, pre_data = self.pre_handler()
            if pre_status:
                return self.result_info(pre_status, pre_data)

            rc, data = method(self.hm)
            # call_status 只有rc不为0时, 可以传call_status True: 代表执行成功  False: 代表执行失败
            if rc != 0 and not data.get('call_status', False):
                return self.result_info(rc, data)

            post_status = self.post_handler()
            if post_status:
                return self.result_info(post_status, data)

            client_cache_udpate = {}
            old_data = {}

            if self.hm.mm:
                if method_param not in ['user.get_red_dot', 'user.game_info']:
                    cur_lan_sort = self.get_argument('lan', '1')
                    if cur_lan_sort != self.hm.mm.user.language_sort:
                        self.hm.mm.user.language_sort = cur_lan_sort
                    self.hm.mm.user.update_active_time(self.request)
                    self.hm.mm.user.save()

                # 主线任务，支线任务自动领奖
                mission_award = {}
                if method_param in self.AUTO_RECEIVE_MISSION_AWARD_FUNC:
                    pass
                    # mission_award = self.hm.mm.mission_main.auto_receive_award()
                    # if mission_award:
                    #     data['_mission_main'] = mission_award

                if mission_award or method_param in self.MISSION_TASK_UPDATE_FUNC:
                    pass
                    # data['mission_task'] = self.hm.mm.mission_main.get_main_tasks()
                    # data['side_task'] = self.hm.mm.mission_side.get_side_tasks(filter=True)

                from models.mission import Mission
                try:
                    Mission.do_task_api( method_param, self.hm, rc, data)
                except:
                    import traceback
                    print_log(traceback.print_exc())

                from models.carnival import Carnival
                try:
                    Carnival.do_task_api(method_param, self.hm, rc, data)
                except:
                    import traceback
                    print_log(traceback.print_exc())

                # 执行成功保存数据
                self.hm.mm.do_save()

                # 关于客户端数据缓存的更新
                for k, obj in self.hm.mm._model.iteritems():
                    if obj and obj.uid == self.hm.uid and getattr(obj, '_diff', None):
                        client_cache_udpate[obj._model_name] = obj._client_cache_update()
                        old_data[k] = getattr(obj, '_old_data', {})


            data['_client_cache_update'] = client_cache_udpate
            data['old_data'] = old_data
            return self.result_info(rc, data)
        return self.result_info('error_not_call_method')

    def pre_handler(self):
        """ 处理方法之前

        :return:
        """
        # return 0, None
        # DEBUG模式, 验证失效
        if settings.DEBUG:
            return 0, None

        # 验证是否是浏览器
        user_agent = self.request.headers.get('User-Agent')
        #if user_agent == 'libcurl':
        user_agent = None
        browser = self.get_argument('browser', '') == settings.BROWSER
        if not browser and (user_agent is not None or not self.get_argument('method')):
            return 'error_9999', None

        # 强制更新
        version = self.hm.get_argument('version', '')
        tpid = self.hm.mm.user.tpid
        version_config = game_config.version.get(str(tpid), game_config.version.get('all'))
        if version_config and version_config['version'] > version:
            return 'error_9998', {
                'custom_msg': version_config['msg'],
                'client_upgrade': {
                    'url': version_config['url'],
                    'msg': version_config['msg'],
                },
            }

        # 封号
        if self.hm.mm.user.status:
            return 'error_9997', None

        # 多点登录
        ks = self.hm.get_argument('ks', '', strip=False)
        mk = self.hm.get_argument('mk', '')
        frontwindow = self.hm.get_argument('frontwindow', '') == settings.FRONTWINDOW
        if not frontwindow and (self.hm.mm.user.mk != mk or self.hm.mm.user.session_expired(ks)):
            return 'error_9527', None

        return 0, None

    def post_handler(self):
        """ 处理方法之后

        :return:
        """

        return 0

    @tornado.web.asynchronous
    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def get(self):
        """ 处理GET请求
        """
        if self.hm is None or self.hm.mm is None:
            self.handler_error('error_100')
            return None

        self.handler()

    @tornado.web.asynchronous
    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def post(self):
        """ 处理POST请求
        """
        if self.hm is None or self.hm.mm is None:
            self.handler_error('error_100')
            return None

        self.handler()


class SLGRequestHandler(APIRequestHandler):
    """
    slg功能相关接口处理
    """

    def pre_handler(self):
        """ 处理方法之前

        :return:
        """
        return 0, None


class ConfigHandler(BaseRequestHandler):
    """ 配置处理

    """
    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def initialize(self):
        """ 初始化操作

        :return:
        """
        self.hm = HandlerManager(self)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def result_info(self, rc, data=None):
        """ 返回信息

        :param rc:
        :param data:
        :param call_status: rc不为0时, 调用是否成功, 默认失败False
        :return:
        """
        msg = ''
        if rc:
            if data:
                msg = data.get('custom_msg')
            if not msg:
                msg = get_msg_str(self.get_argument('lan', '1')).get(rc)
            if not msg:
                method_param = self.get_argument('method')
                msg = get_msg_str(self.get_argument('lan', '1')).get(method_param, {}).get(rc, method_param + '_error_%s' % rc)

        if data is None:
            data = {}
        self.write(handler_tools.result_generator(rc, data, msg, self.hm.mm))
        self.finish()
        # try:
        #     self.write(handler_tools.result_generator(rc, data, msg, self.hm.mm))
        # finally:
        #     self.finish()
        #     return rc, data, msg, self.hm.mm

    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def api(self):

        method_name = self.get_argument('method', 'resource_version')

        try:
            module = importlib.import_module('views.config')
        except ImportError:
            print_log(traceback.print_exc())
            return self.result_info('error_module')

        method = getattr(module, method_name, None)
        if method is None:
            return self.result_info('error_method')

        if callable(method):
            rc, data = method(self.hm)
            if rc != 0:
                return self.result_info(rc)

            return self.result_info(rc, data)
        return self.result_info('error_not_call_method')

    def get(self):
        """

        :return:
        """
        self.api()

    def post(self):
        """

        :return:
        """
        self.api()


class PayCallback(BaseRequestHandler):

    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def get(self, tp):
        from views import payment

        d = payment.callback(self, tp)
        self.write(d)
        self.finish()

    def post(self, tp):
        return self.get(tp)


class PayOrder(BaseRequestHandler):

    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def get(self):
        from views import payment
        method = self.get_argument('method')
        func = getattr(payment, method)
        # d = payment.pay_order(self, tp)
        rc, d = func(self)

        r = {
            'data': d,
            'status': rc,
            'msg': "",
            'server_time': int(time.time()),
            'user_status': {},
        }
        # 由tornado自动判断是否转JSON
        # self.set_header('content_type', 'application/json; charset=UTF-8')
        # self.set_header('Content-Type', 'application/json; charset=UTF-8')
        # d = json.dumps(d, ensure_ascii=False, encoding="utf-8", default=to_json)
        self.write(r)
        self.finish()

    def post(self, tp):
        return self.get(tp)


class WeixinHandler(BaseRequestHandler):
    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def get(self, tag_name):
        """# get: docstring
        args:
            :    ---    arg
        returns:
            0    ---
        """
        from views import wechat_signin
        method = getattr(wechat_signin, tag_name)
        return method(self)

    def post(self, tag_name):
        """# post: docstring
        args:
            :    ---    arg
        returns:
            0    ---
        """
        result = self.get(tag_name)
        r = json.dumps(result, ensure_ascii=False, separators=(',', ':'), encoding="utf-8", default=to_json)
        self.write(r)
        self.finish()


class HeroHandler(BaseRequestHandler):
    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def get(self, tag_name):
        from views import hero_sdk
        method = getattr(hero_sdk, tag_name)
        result = method(self)

        r = json.dumps(result, ensure_ascii=False, separators=(',', ':'), encoding="utf-8", default=to_json)
        self.write(r)
        self.finish()

    def post(self, tag_name):
        """# post: docstring
        args:
            :    ---    arg
        returns:
            0    ---
        """
        return self.get(tag_name)


class HeroIMHandler(BaseRequestHandler):
    @error_mail(not settings.DEBUG, settings.ADMIN_LIST)
    def get(self, tag_name):
        user_agent = self.request.headers.get('User-Agent')

        from views import hero_sdk
        method = getattr(hero_sdk, tag_name)
        result = method(self)

        r = json.dumps(result, ensure_ascii=False, separators=(',', ':'), encoding="utf-8", default=to_json)
        self.write(r)
        self.finish()

    def post(self, tag_name):
        """# post: docstring
        args:
            :    ---    arg
        returns:
            0    ---
        """
        return self.get(tag_name)


