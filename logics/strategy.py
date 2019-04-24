# -*- coding: utf-8 –*-

import time
import random
import settings
from math import ceil
from gconfig import game_config
from tools.user import user_info
from lib.utils.debug import print_log
from tools.gift import calc_gift, add_mult_gift, del_mult_goods


class Strategy(object):
    """
    """
    def __init__(self, mm):
        self.mm = mm
        self.strategy = self.mm.strategy

    def index(self):

        if not self.strategy.strategy_uid:

            data = {
                'apply_info': self.strategy.apply_info,
                'invite_info': self.strategy.invite_info,
                'refuse_info': self.strategy.refuse_info,
            }
        else:
            mission = self.mm.strategy.strategy_mission
            data = {
                'tacit': mission.tacit,                     # 默契值
                'level': mission.level,                     # 合作等级
                'point': mission.point,                     # 任务积分
                'missions': mission.strategy_data,          # 任务数据
                'strategy_info': mission.strategy_info,     # 合作双方数据
            }

        return data

    def apply(self, target):
        """ 申请合作
        """
        target_mm = self.mm.get_mm(target)

        applyed = target_mm.strategy.apply_info
        if target in applyed:
            return 0, {}            # 已经发送申请

        # 添加申请信息到对方受邀列表
        apply_info = self.get_user_info(self.mm)
        target_mm.strategy.apply_strategy(apply_info, sort='invite')

        # 自己记录申请信息
        # invite_info = self.get_user_info(target_mm)
        # target_mm.strategy.apply_strategy(invite_info)

        return 0, {}

    def agree_invite(self, target):
        """
        :param target: 合作的 uid
        :return:
        """

        if self.strategy.strategy_uid:
            if self.strategy.strategy_uid == target:
                return 1, {}            # 已经开始合作了
            return 2, {}                # 你的战略合作伙伴已满

        target_mm = self.mm.get_mm(target)
        if target_mm.strategy.strategy_uid:
            return 3, {}                # 对方战略合作伙伴已满

        target_mm.strategy.strategy_uid = self.mm.uid
        self.mm.strategy.strategy_uid = target
        mission = self.mm.strategy.strategy_mission
        mission.start_strategy(self.mm, target_mm)
        mission.save()
        self.mm.strategy.save()
        target_mm.strategy.save()
        # self.mm.strategy.del_apply(target, sort='invite')
        self.mm.strategy.del_all_apply(sort='invite')

        data = self.index()
        return 0, data

    def refuse_invite(self, target):
        """ 拒绝邀请
        """
        self.mm.strategy.del_apply(target, sort='invite')

        refuse_info = self.get_user_info(self.mm)
        target_mm = self.mm.get_mm(target)
        if not target_mm.strategy.strategy_uid:
            target_mm.strategy.apply_strategy(refuse_info, sort='refuse')
        data = self.index()
        return 0, data

    def del_msg(self, target, sort):
        """ 删除消息
        """
        self.mm.strategy.del_apply(target, sort)
        return 0, {}

    def quit_strategy(self):
        """ 退出合作
        """
        strategy_uid = self.mm.strategy.strategy_uid
        target_mm = self.mm.get_mm(strategy_uid)
        target_mm.strategy.strategy_uid = ''
        strategy_mission = self.strategy.strategy_mission
        client = strategy_mission.redis
        strategy_model_key = strategy_mission._model_key
        self.strategy.strategy_uid = ''
        target_mm.strategy.save()
        self.strategy.save()
        client.delete(strategy_model_key)
        if settings.DEBUG:
            print_log('del strategy_model_key', strategy_model_key)

        data = self.index()
        return 0, data

    def get_user_info(self, mm):
        """ 获取用户信息
        """
        info = user_info(mm)
        info['ts'] = int(time.time())
        info['status'] = 0

        return info

    def choice_task(self, task_id):
        """ 选择任务
        """

        strategy_mission = game_config.strategy_mission
        mission_config = strategy_mission.get(task_id)
        if not mission_config:
            return 1, {}

        strategy_mission = self.strategy.strategy_mission

        if not strategy_mission:
            return 'error_strategy', {}     # 没有合作对象

        strategy_data = strategy_mission.strategy_data

        if task_id not in strategy_data:
            return 2, {}            # 没有该任务

        task_info = strategy_data[task_id]
        if task_info['owner']:
            if task_info['owner'] == self.mm.uid:
                data = self.index()
                return 0, data
            return 3, {}            # 该任务已经被领取

        for v in strategy_data.itervalues():
            if v['owner'] == self.mm.uid:
                status = v['status']
                if not status:
                    return 4, {}        # 完成当前任务才可以领取下一任务
                elif status == 1:
                    return 5, {}        # 请先领取奖励再领取任务

        task_info['owner'] = self.mm.uid
        strategy_mission.save()
        data = self.index()
        return 0, data

    def task_reward(self, task_id):
        """
        领取任务奖励
        :param task_id: 任务id
        :return:
        """
        strategy_mission = game_config.strategy_mission
        mission_config = strategy_mission.get(task_id)
        if not mission_config:
            return 1, {}

        a = mission_config['reward_a']
        b = mission_config['reward_b']
        y_income = strategy_mission.strategy_info[self.mm.uid]['y_income']
        gift_num = ceil((a * y_income + b))
        per_reward = mission_config['reward']
        gift = [p[:1] + [p[2] * gift_num] for p in per_reward]

        strategy_mission = self.strategy.strategy_mission

        if not strategy_mission:
            return 'error_strategy', {}     # 没有合作对象

        strategy_data = strategy_mission.strategy_data
        if task_id not in strategy_data:
            return 2, {}            # 没有该任务

        task_info = strategy_data[task_id]
        status = task_info['status']
        if not status:
            return 3, {}            # 该任务还未完成

        if status == 2:
            return 4, {}            # 已经领过该奖励了

        if task_info['owner'] != self.mm.uid:
            return 5, {}            # 只能领取自己接的任务

        gift = calc_gift(gift)
        task_info['status'] = 2
        reward = add_mult_gift(self.mm, gift)
        strategy_mission.add_done_num(task_id)
        strategy_mission.save()

        data = self.index()
        data['reward'] = reward

        return 0, data

    def level_reward(self):
        """ 升级奖励
        """
        strategy = self.strategy
        strategy_mission = strategy.strategy_mission
        level = strategy_mission.level

        strategy_lv_config = game_config.strategy_lv
        lv_config = strategy_lv_config.get(level, {})
        if not lv_config:
            return 1, {}            # 奖励不存在

        mission_amount = lv_config['mission_amount']
        if strategy_mission.done_num < mission_amount:
            return 2, {}            # 完成任务数不足

        gift = lv_config['level_gift']
        friendly = lv_config['friendly']

        if friendly:
            strategy_mission.add_tacit(friendly)
        strategy_mission.lvl_up()

        reward = {}
        if gift:
            gift = calc_gift(gift)
            reward = add_mult_gift(self.mm, gift)
            target = strategy.strategy_uid
            target_mm = self.mm.get_mm(target)
            title = strategy_mission.TITLE
            content = strategy_mission.CONTENT
            msg = target_mm.mail.generate_mail_lan(content, title=title, gift=gift)
            target_mm.mail.add_mail(msg)
        strategy_mission.save()
        data = self.index()
        data['reward'] = reward

        return 0, {}

    def send_gift(self, kind):
        """ 增送礼物
        """
        strategy_kind_gift = game_config.get_strategy_gift_mapping().get(kind, {})
        if strategy_kind_gift:
            return 'error_100', {}          # 参数错误

        strategy_uid = self.strategy.strategy_uid
        if not strategy_uid:
            return 'error_strategy', {}     # 没有合作对象

        target_mm = self.mm.get_mm(strategy_uid)
        level = target_mm.block.block_num
        gift_config = strategy_kind_gift[level]
        cost = gift_config['me_spend']
        gift = gift_config['partner_get']

        rc, _ = del_mult_goods(self.mm, cost)
        if rc:
            return rc, 0
        reward = add_mult_gift(target_mm, gift)

        data = self.index()
        data['reward'] = reward

        return 0, data

    def quick_done(self):
        strategy_mission = self.strategy.strategy_mission

        if not strategy_mission:
            return 'error_strategy', {}     # 没有合作对象

        no_owner = []

        strategy_data = strategy_mission.strategy_data
        for k, v in strategy_data.iteritems():
            if not v['owner'] and v['status'] == 0:
                no_owner.append(k)
        if not no_owner:
            return 1, {}            # 没有符合快速完成条件的任务

        task_id = random.choice(no_owner)

        strategy_mission.quick_done(task_id, self.mm.uid)
        strategy_mission.save()

        data = self.index()

        return 0, data

    def help_done(self, task_id):
        """ 去帮忙
        """
        uid = self.mm.uid
        strategy_mission = game_config.strategy_mission
        mission_config = strategy_mission.get(task_id)
        if not mission_config:
            return 1, {}

        strategy_mission = self.strategy.strategy_mission
        if not strategy_mission:
            return 'error_strategy', {}     # 没有合作对象

        strategy_data = strategy_mission.strategy_data
        if task_id not in strategy_data:
            return 2, {}            # 没有该任务

        task_info = strategy_data[task_id]
        status = task_info['status']
        if status:
            return 3, {}            # 任务已经完成
        owner = task_info['owner']
        if not owner:
            return 4, {}            # 无主的任务,不能帮忙哦
        if owner == uid:
            return 5, {}            # 自己的任务哦, 快去完成吧
        if uid not in task_info['do_uid']:
            task_info['do_uid'].append(uid)
            strategy_mission.save()

        data = self.index()

        return 0, data


