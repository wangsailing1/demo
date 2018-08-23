# coding: utf-8

"""
使用python第三方包（apscheduler(3.0.0)）实现定时任务
配置说明：
    任务类型:
        cron: 定时循环任务，类似unix系统的crontab
        interval: 间隔任务， 类型tornado的 percallback
        date: 定点一次性任务， 到指定日期时间运行一次
    cron:
        :param int|str year: 4-digit year
        :param int|str month: month (1-12)
        :param int|str day: day of the (1-31)
        :param int|str week: ISO week (1-53)
        :param int|str day_of_week: number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        :param int|str hour: hour (0-23)
        :param int|str minute: minute (0-59)
        :param int|str second: second (0-59)
        :param datetime|str start_date: earliest possible date/time to trigger on (inclusive)
        :param datetime|str end_date: latest possible date/time to trigger on (inclusive)
        :param datetime.tzinfo|str timezone: time zone to use for the date/time calculations
                                             (defaults to scheduler timezone)
    interval:
        :param int weeks: number of weeks to wait
        :param int days: number of days to wait
        :param int hours: number of hours to wait
        :param int minutes: number of minutes to wait
        :param int seconds: number of seconds to wait
        :param datetime|str start_date: starting point for the interval calculation
        :param datetime|str end_date: latest possible date/time to trigger on
        :param datetime.tzinfo|str timezone: time zone to use for the date/time calculations
    date:
        :param datetime|str run_date: the date/time to run the job at
        :param datetime.tzinfo|str timezone: time zone for ``run_date`` if it doesn't have one already
TIMER_JOBS = (
     任务类型（cron,interval,date）, 任务时间参数(参见上面说明)， 要执行的函数， 是否是全局的
    ('cron', dict(second='5,10,15,20,25,30,55'), timer_arena_award_rank, 1)
)
"""
import gevent.monkey
gevent.monkey.patch_all()

import time
import datetime
import cPickle as pickle
from tornado.options import define, options
from apscheduler.schedulers.gevent import GeventScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# 预先导入_strptime模块
datetime.datetime.strptime('2015-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

define("env", default='local', help="settings file name", type=str)

options.parse_command_line()
# 设定进程使用的配置文件
import settings
settings.set_env(options.env, 'all')

from gconfig import game_config, front_game_config
from lib.utils.debug import print_log
from lib.utils import filedefaultdict
from lib.utils.mail import send_sys_mail
from lib.db import ModelTools
from models.server import ServerUidList

# from lib.statistics.data_analysis import do_data_process_hourly, level_pass_rate
# from scrips.statistics.dmp_snapshot import do_snapshot
from lib.utils.online_user import backup_all_server_online_count


# from logics.decisive_battle import mapping_battle_uid, send_duel_rank_award
# from logics.decisive_battle import one_server_battle, vip_auto_enroll

JOBS_RUNTIME_KEY = 'jobs_runtime_key'
# 任务配置，添加分服或任务后，需要重启进程使之生效
TIMEZONE = 'Asia/Harbin'
TIMER_JOBS = (
    # 类型， 类型触发器需要的参数，                              要执行的函数， 是否是全局的
    # ('cron', dict(hour=3, minute=0), do_snapshot, 1),    # 快照放在admin执行，不走timer

    # 每5分钟记录一次在线数据
    ('cron', dict(minute='*/5'), backup_all_server_online_count, 1),

    # 公会战
    # 筛选可参与的公会,分组
    # ('cron', dict(day_of_week='1', hour='9', minute='50'), filter_guild, 0),
    # 分组
    # ('cron', dict(day_of_week='2,3', hour='22'), group_team, 0),
    # 公会战周五晚上结算发奖
    # ('cron', dict(day_of_week='4', hour='22'), settlement_reward, 0),


)
DATE_LIST_JOBS = (
    # 返回时间列表的函数（类似要执行的函数，分全局和非全局）   要执行的函数， 是否是全局的(0,1)
    # #### 工会战   #######
    # (test2, test, 0),
    # # 限时英雄排名发奖
    # (limit_hero_mail_time                       , send_limit_hero_rank_award            , 1),
    # # 新服限时英雄排名发奖
    # (server_limit_hero_mail_time                , server_send_limit_hero_rank_award     , 0),
)


class SelfGeventScheduler(GeventScheduler):
    """任务执行类
    重写_main_loop方法, 方便自动更新
    """
    def _main_loop(self):
        self.config_time = 0
        while self.running:
            if self.config_time % 59 == 0:
                if (game_config and game_config.reload()) or \
                        (front_game_config and front_game_config.reload()):
                    print '----game_config.auto_reload, reload_all_jobs'
                    self.reload_all_jobs()

                if settings.DEBUG and self.debug_sync_change_time():
                    print '----debug_sync_change_time, reload_all_jobs'
                    self.reload_all_jobs()

                self.save_jobs_to_redis()

            wait_seconds = 1
            _wait_seconds = self._process_jobs()
            self._event.wait(wait_seconds if wait_seconds is not None else self.MAX_WAIT_TIME)
            self._event.clear()

            self.config_time += wait_seconds

    cache = ModelTools.get_redis_client('public')
    jobs_to_save = None

    def save_jobs_to_redis(self):
        print 'save_jobs_to_redis start!'
        # new_jobs = set(self.get_jobs())
        new_jobs = {k.id: str(k.next_run_time) for k in self.get_jobs()}
        if new_jobs != self.jobs_to_save:
            print 'save_jobs_to_redis happen!'
            self.jobs_to_save = new_jobs
            r = pickle.dumps(self.jobs_to_save, pickle.HIGHEST_PROTOCOL)
            r = "\x01" + r.encode("zip")
            self.cache.set(JOBS_RUNTIME_KEY, r)

    def add_job_to_scheduler(self, trigger_name, trigger_kwargs, job_func, is_global):
        job_func_name = '%s:%s' % (job_func.__module__, job_func.__name__)
        if is_global:
            job_id = job_func_name
            job = self.add_job(job_func_name, trigger_name,
                               id=job_id, name=job_id,
                               misfire_grace_time=600,
                               replace_existing=True,
                               **trigger_kwargs)
            print job
        else:
            for server_id in ServerUidList.all_server():
                job_id = '%s:%s' % (job_func_name, server_id)
                job = self.add_job(job_func_name, trigger_name, args=(server_id,),
                                   id=job_id, name=job_id,
                                   misfire_grace_time=600,
                                   replace_existing=True,
                                   **trigger_kwargs)
                print job

    def add_time_list_job(self, time_list_func, job_func, is_global):
        job_func_name = '%s:%s' % (job_func.__module__, job_func.__name__)
        trigger_name = 'date'
        if is_global:
            for index, dt in enumerate(time_list_func()):
                # 过期的timer不再加
                if str(dt) < time.strftime('%F %T'):
                    continue
                job_id = '%s:%s' % (job_func_name, index)
                trigger_kwargs = dict(run_date=dt)
                job = self.add_job(job_func_name, trigger_name,
                                   id=job_id, name=job_id,
                                   misfire_grace_time=600,
                                   replace_existing=True,
                                   **trigger_kwargs)
                print job
        else:
            for server_id in ServerUidList.all_server():
                for index, dt in enumerate(time_list_func(server_id)):
                    # 过期的timer不再加
                    if str(dt) < time.strftime('%F %T'):
                        continue
                    job_id = '%s:%s:%s' % (job_func_name, server_id, index)
                    trigger_kwargs = dict(run_date=dt)
                    job = self.add_job(job_func_name, trigger_name, args=(server_id,),
                                       id=job_id, name=job_id,
                                       misfire_grace_time=600,
                                       replace_existing=True,
                                       **trigger_kwargs)
                    print job

    def reload_all_jobs(self):
        for trigger, trigger_kwargs, func_name, is_global in TIMER_JOBS:
            self.add_job_to_scheduler(trigger, trigger_kwargs, func_name, is_global)
        for time_list_func, func_name, is_global in DATE_LIST_JOBS:
            self.add_time_list_job(time_list_func, func_name, is_global)

    def debug_sync_change_time(self):
        """管理进程时间
        # 注意, 正式环境禁止启动此函数
        """
        if not settings.DEBUG:
            return False

        from apscheduler.schedulers import base
        from apscheduler.executors import base as base1
        from lib.utils import change_time
        from models.config import ChangeTime

        delta_seconds = ChangeTime.get()
        delta_seconds = int(float(delta_seconds)) if delta_seconds else 0
        real_time = int(change_time.REAL_TIME_FUNC())
        sys_time = real_time + delta_seconds
        if sys_time != int(time.time()):
            change_time.change_time(sys_time)
            # 修正修改进程时间时apscheduler datetime 类不生效的问题
            base.datetime = change_time.datetime.datetime
            base1.datetime = change_time.datetime.datetime
            print_log('debug_change_time: %s -- %s -- %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(real_time)),
                                                             time.strftime('%Y-%m-%d %H:%M:%S'),
                                                             delta_seconds))
            return True
        return False


def my_listener(event):
    now_str = time.strftime('%Y%m%d')
    if event.exception:
        error_msg = '''\n%s\n\nrun at: %s\n\ntraceback info:\n%s
        ''' % (event.job_id,
               event.scheduled_run_time,
               event.traceback)
        subject = ("[%s RUN_TIMER ERROR] - [%s]") % (settings.ENV_NAME, now_str)
        if not settings.DEBUG:
            send_sys_mail(settings.ADMIN_LIST, subject, error_msg)
        print error_msg
    else:
        f = filedefaultdict(mode='a')
        msg = '%s -- %s\n' % (event.scheduled_run_time, event.job_id)
        f['%slogs/run_timer/%s' % (settings.BASE_ROOT, now_str)].write(msg)


def main():
    # 让打印输出到supervisor_err.log中
    settings.set_debug_print()

    # 启动apscheduler服务
    scheduler = SelfGeventScheduler(timezone=TIMEZONE)
    if settings.DEBUG:
        scheduler.debug_sync_change_time()
    # scheduler.add_jobstore('redis', jobs_key='run_timer.jobs', run_times_key='run_timer.run_times', **settings.GLOBAL_CACHE)
    # scheduler.remove_all_jobs()

    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    g = scheduler.start()
    scheduler.reload_all_jobs()

    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
