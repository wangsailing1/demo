# -*- coding: utf-8 –*-


from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils import weight_choice

############### 任务是否完成判断函数定义 返回flag, value, need #################

GETNUMSORT = [3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


# 1 玩家等级
def target_sort1(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[1]
    value = mm.user.level
    return value >= target_value, value, target_value


# 任意卡牌达到等级
def target_sort2(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data
    num = len(reward_obj.get_count(mission_id)) if isinstance(reward_obj.get_count(mission_id), list) else 0
    return num >= target_value[1], num, target_value[1]


# 直接取数值判断
def target_sort_num(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[1]
    value = reward_obj.get_count(mission_id)
    return value >= target_value, value, target_value


# 票房
def target_sort5(mm, reward_obj, target_data, mission_id, target_data1):
    target_value = target_data[1]
    value = reward_obj.get_count(mission_id)
    return value >= target_value, value, target_value

# 艺人好感度
def target_sort23(mm, reward_obj, target_data, mission_id, target_data1):
    num = 0
    config = game_config.card_basis
    group_ids = []
    target_value = target_data[1]
    for card_id, value in mm.card.cards.iteritems():
        group_id = config[value['id']]['group']
        group_ids.append(group_id)
        if value['love_exp'] >= target_data[0]:
            num += 1
    for g_id in mm.card.attr:
        if g_id not in group_ids and mm.card.attr[g_id].get('like', 0) >= target_data[0]:
            num += 1
    return num >= target_value, num, target_value


class Carnival(object):
    def __init__(self, mm):
        self.mm = mm
        self.carnival = self.mm.carnival

    def index(self, tp=1):
        pre_str = self.carnival.CONFIGMAPPING[tp]
        return 0, {'carnival_data': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_data')),
                   'carnival_done': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_done')),
                   'dice_num': getattr(self.carnival, '%s%s' % (pre_str, 'dice_num')),
                   'carnival_days': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_days')),
                   'carnival_step': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_step')),
                   'max_id': self.carnival.carnival_max_id(tp=tp),
                   'status': self.get_status_by_type(tp),
                   'tp':tp}

    def dice(self, tp=1):
        if tp == 1:
            config = game_config.carnival_new_reward
        else:
            config = game_config.carnival_old_reward
        max_id = self.carnival.carnival_max_id(tp=tp)
        max_step = config[max_id]['num']
        pre_str = self.carnival.CONFIGMAPPING[tp]
        now_step = getattr(self.carnival, '%s%s' % (pre_str, 'carnival_step'))
        if now_step >= max_step:
            return 11, {}  # 格子已达最大
        dice_config = game_config.carnival_random['dice_ratio']
        step_num = weight_choice(dice_config)[0]
        next_step = now_step + step_num
        next_step = next_step if next_step < max_step else max_step
        setattr(self.carnival, '%s%s' % (pre_str, 'carnival_step'), next_step)
        all_steps = range(now_step + 1, next_step + 1)
        reward_ids = []
        for step_id in all_steps:
            for id, value in config.iteritems():
                if step_id == value['num']:
                    reward_ids.append(id)
                    break
        rewards = {}
        old_gift = getattr(self.carnival, '%s%s' % (pre_str, 'reward_data'), [])
        for reward_id in reward_ids:
            gift = config[reward_id]['reward']
            old_gift.extend(gift)
            reward = add_mult_gift(self.mm, gift)
            rewards[reward_id] = reward
        setattr(self.carnival, '%s%s' % (pre_str, 'reward_data'), old_gift)
        dice_num = getattr(self.carnival, '%s%s' % (pre_str, 'dice_num'))
        dice_num -= 1
        setattr(self.carnival, '%s%s' % (pre_str, 'dice_num'), dice_num)
        self.carnival.save()
        _, data = self.index(tp=tp)
        data['reward'] = rewards
        data['choice_num'] = step_num
        return 0, data

    def get_reward(self, tp=1, mission_id=''):
        type = self.carnival.MISSIONMAPPING[tp]
        mission_obj = getattr(self.carnival, type)
        if mission_id not in mission_obj.data:
            return 11, {}  # 任务id错误
        mission_obj.done.setdefault(mission_obj.days, []).append(mission_id)
        if mission_obj.config[mission_id]['if_reuse']:
            mission_obj.data[mission_id] = 0
        else:
            mission_obj.data.pop(mission_id)
        if tp == 2:
            self.carnival.dice_num += mission_obj.config[mission_id]['reward']
        if tp == 1:
            self.carnival.server_dice_num += mission_obj.config[mission_id]['reward']
        self.carnival.save()
        _, data = self.index(tp=tp)
        data['got_num'] = mission_obj.config[mission_id]['reward']
        return 0, data

    def has_reward_by_type(self, tp=1, mission_id=''):
        type = self.carnival.MISSIONMAPPING[tp]
        mission_obj = getattr(self.carnival, type)
        if mission_id:
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            if stats['status'] == 1:
                return 1
            return 0
        for mission_id, value in mission_obj.data.iteritems():
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            if stats['status'] == 1:
                return 1
        return 0

    def get_done_mission(self, tp=1, mission_id=''):
        type = self.carnival.MISSIONMAPPING[tp]
        mission_obj = getattr(self.carnival, type)
        config = mission_obj.config
        if mission_id in mission_obj.done.get(mission_obj.days, []) and not config[mission_id]['if_reuse']:
            return 1
        return 0

    def carnival_red_dot(self, tp=1):
        type = self.carnival.MISSIONMAPPING[tp]
        mission_obj = getattr(self.carnival, type)
        for mission_id in mission_obj.data:
            has_reward = self.has_reward_by_type(type=tp, mission_id=mission_id)
            done = self.get_done_mission(type=tp, mission_id=mission_id)
            if has_reward and not done:
                return True
        return False

    def get_status(self, mission_obj, mission_id, config):
        target_sort = config['sort']
        target_data = config.get('target', [])
        target_data1 = config.get('target1', [])
        if mission_id in mission_obj.done.get(mission_obj.days, []) and not config['if_reuse']:
            status, value, need = -1, 1, 1
        else:
            if target_sort not in [1, 2, 5, 23]:
                target_sort = '_num'
            func = globals()['target_sort%s' % target_sort]
            flag, value, need = func(self.mm, mission_obj, target_data, mission_id, target_data1)
            status = 1 if flag else 0
        return {
            'id': mission_id,
            'value': value,
            'need_value': need,
            'status': status
        }

    def get_status_by_type(self, tp=1):
        type = self.mm.carnival.MISSIONMAPPING[tp]
        mission_obj = getattr(self.carnival, type)
        result = {}
        done = mission_obj.done.get(mission_obj.days, [])
        for mission_id in mission_obj.data:
            stats = self.get_status(mission_obj, mission_id, mission_obj.config[mission_id])
            result[stats['id']] = [stats['value'], stats['need_value'], stats['status']]

        return {
            'result': result,
            'done': done
        }
