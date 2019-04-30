# -*- coding: utf-8 –*-


from gconfig import game_config
from tools.gift import add_mult_gift


class SingleRecharge(object):

    def __init__(self, mm):

        self.mm = mm
        self.singlerecharge = self.mm.single_recharge

    def index(self):
        """ 首页信息
        """
        singlerecharge = self.singlerecharge
        if not singlerecharge.is_open():
            return 'error_active_time', {}

        version = singlerecharge.version

        return 0, {
            'version': version,
            'end_time': singlerecharge.end_time,
            'singlerecharge': singlerecharge.charge_data,
        }

    def reward(self, reward_id):
        """ 领奖
        """
        singlerecharge = self.singlerecharge
        charge_data = singlerecharge.charge_data
        if reward_id not in charge_data or not charge_data[reward_id]['complete_times']:
            return 2, {}            # 还没完成
        if charge_data[reward_id]['reward'] >= charge_data[reward_id]['complete_times']:
            return 3, {}            # 已经领取奖励

        version = singlerecharge.version
        config = game_config.get_single_recharge_mapping().get(version, {}).get(reward_id, {})
        if not config:
            return 4, {}            # 数据异常

        gift = config['reward']

        reward = add_mult_gift(self.mm, gift)

        charge_data[reward_id]['reward'] += 1
        singlerecharge.save()

        _, data = self.index()
        data['reward'] = reward

        return 0, data


class ServerSingleRecharge(object):

    def __init__(self, mm):

        self.mm = mm
        self.singlerecharge = self.mm.server_single_recharge

    def index(self):
        """ 首页信息
        """
        singlerecharge = self.singlerecharge
        if not singlerecharge.is_open():
            return 'error_active_time', {}

        version = singlerecharge.version

        return 0, {
            'version': version,
            'end_time': singlerecharge.end_time,
            'singlerecharge': singlerecharge.charge_data,
        }

    def reward(self, reward_id):
        """ 领奖
        """
        singlerecharge = self.singlerecharge
        charge_data = singlerecharge.charge_data
        if reward_id not in charge_data or not charge_data[reward_id]['complete_times']:
            return 2, {}            # 还没完成
        if charge_data[reward_id]['reward'] >= charge_data[reward_id]['complete_times']:
            return 3, {}            # 已经领取奖励

        version = singlerecharge.version
        config = game_config.get_server_single_recharge_mapping().get(version, {}).get(reward_id, {})
        if not config:
            return 4, {}            # 数据异常

        gift = config['reward']

        reward = add_mult_gift(self.mm, gift)

        charge_data[reward_id]['reward'] += 1
        singlerecharge.save()

        _, data = self.index()
        data['reward'] = reward

        return 0, data
