# -*- coding: utf-8 –*-


from gconfig import game_config
from tools.gift import add_mult_gift
from lib.utils import weight_choice


class Carnival(object):
    def __init__(self, mm):
        self.mm = mm
        self.carnival = self.mm.carnival

    def index(self,tp=1):
        pre_str = self.carnival.CONFIGMAPPING[tp]
        return 0, {'carnival_data': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_data')),
                   'carnival_done': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_done')),
                   'dice_num': getattr(self.carnival, '%s%s' % (pre_str, 'dice_num')),
                   'carnival_days': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_days')),
                   'carnival_step': getattr(self.carnival, '%s%s' % (pre_str, 'carnival_step')),
                   'max_id': self.carnival.carnival_max_id(tp=tp)}

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
        return 0, data
