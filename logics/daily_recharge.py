# -*- coding: utf-8 –*-

from gconfig import game_config
from tools.gift import add_mult_gift


class DailyRecharge(object):

    def __init__(self, mm):

        self.mm = mm
        self.dailyrecharge = self.mm.daily_recharge

    def index(self):
        """ 首页信息
        """
        dailyrecharge = self.dailyrecharge
        if not dailyrecharge.is_open():
            return 'error_active_time', {}
        day = dailyrecharge.day
        version = dailyrecharge.version
        dailyrecharge.done_data.setdefault(day, dailyrecharge.new_record())

        return 0, {
            'day': day,
            'version': version,
            'dailyrecharge': dailyrecharge.done_data,
        }

    def reward(self, day):
        """ 领奖
        """
        dailyrecharge = self.dailyrecharge
        day = day or self.dailyrecharge.day

        if day > self.dailyrecharge.day:
            return 1, {}            # 领取时间错误

        done_data = dailyrecharge.done_data
        if day not in done_data or not done_data[day]['is_complete']:
            return 2, {}            # 还没完成

        if done_data[day]['reward']:
            return 3, {}            # 已经领取奖励

        version = dailyrecharge.version
        config = game_config.get_daily_recharge_mapping().get(version, {}).get(day, {})
        if not config:
            return 4, {}            # 数据异常

        gift = config['reward']

        reward = add_mult_gift(self.mm, gift)

        done_data[day]['reward'] = 1
        dailyrecharge.save()

        _, data = self.index()
        data['reward'] = reward

        return 0, data


class ServerDailyRecharge(object):
    """ 新服
    """

    def __init__(self, mm):

        self.mm = mm
        self.dailyrecharge = self.mm.server_daily_recharge

    def index(self):
        """ 首页信息
        """
        dailyrecharge = self.dailyrecharge

        if not dailyrecharge.is_open():
            return 'error_active_time', {}

        day = dailyrecharge.day
        version = dailyrecharge.version
        dailyrecharge.done_data.setdefault(day, dailyrecharge.new_record())

        return 0, {
            'day': day,
            'version': version,
            'dailyrecharge': dailyrecharge.done_data,
        }

    def reward(self, day):
        """ 领奖
        """
        dailyrecharge = self.dailyrecharge
        day = day or dailyrecharge.day

        if day > dailyrecharge.day:
            return 1, {}            # 领取时间错误

        done_data = dailyrecharge.done_data
        if day not in done_data or not done_data[day]['is_complete']:
            return 2, {}            # 还没完成

        if done_data[day]['reward']:
            return 3, {}            # 已经领取奖励

        version = dailyrecharge.version
        config = game_config.get_server_daily_recharge_mapping().get(version, {}).get(day, {})
        if not config:
            return 4, {}            # 数据异常

        gift = config['reward']

        reward = add_mult_gift(self.mm, gift)

        done_data[day]['reward'] = 1
        dailyrecharge.save()

        _, data = self.index()
        data['reward'] = reward

        return 0, data



