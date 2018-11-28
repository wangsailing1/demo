#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from bisect import bisect_left as bisect

from gconfig import game_config
from tools.gift import add_mult_gift_by_weights, add_gift, del_mult_goods, add_mult_gift


class ItemLogic(object):
    def __init__(self, mm):
        self.mm = mm
        self.item = self.mm.item
        self.aitem = self.mm.awaken_item

    def use_item(self, item_id, item_num, reward_index):
        """ 使用普通道具

        :param item_id:
        :param item_num:
        :param reward_index: X选x宝箱专用, 奖励的下标[0,1]
        :return:
        """
        cur_item_num = self.mm.item.get_item(item_id)
        item_config = game_config.use_item.get(item_id)
        if item_config is None:
            return 1, {'update_item': {'item': self.item.items}}

        if cur_item_num < item_num:
            return 2, {'update_item': {'item': self.item.items}}

        is_use = item_config['is_use']
        if is_use == 0:
            return 3, {}

        use_effect = item_config['use_effect']

        reward = {}

        if is_use == 1:  # 宝箱
            rc, reward = self.use_box_item(use_effect, item_num, reward_index)
            if rc != 0:
                return rc, {}
        elif is_use == 2:  # 金币
            reward = add_gift(self.mm, 1, [[0, use_effect]] * item_num, cur_data=reward)
        elif is_use == 3:  # 道具
            reward = add_gift(self.mm, 5, use_effect * item_num, cur_data=reward)
        # elif is_use == 4:  # 进阶材料
        #     reward = add_gift(self.mm, 7, use_effect * item_num, cur_data=reward)
        # elif is_use == 5:  # 采集物
        #     reward = add_gift(self.mm, 5, use_effect * item_num, cur_data=reward)
        elif is_use == 6:  # 装备
            reward = add_gift(self.mm, 6, use_effect * item_num, cur_data=reward)
        elif is_use == 11: #碎片合成艺人
            got_num = item_num / item_config['use_num']
            if not got_num:
                return 111, {}  #碎片不足
            item_num = got_num * item_config['use_num']
            reward = add_gift(self.mm, 5, use_effect * got_num, cur_data=reward)
        elif is_use == 15:  # 增加艺人
            reward = add_gift(self.mm, 8, use_effect * item_num, cur_data=reward)
        elif is_use == 16:  # 点赞
            reward = add_gift(self.mm, 16, [[0, use_effect]] * item_num, cur_data=reward)
        elif is_use == 18:  # 增加艺人名片
            rc = self.mm.friend.check_actor(use_effect)
            if rc != 0:
                return rc, {}
            reward = add_gift(self.mm, 18, [[use_effect, item_num]], cur_data=reward)
        else:
            return 5, {}

        self.mm.item.del_item(item_id, item_num)
        self.mm.item.save()
        return 0, {
            'reward': reward,
        }

    def use_box_item(self, box_item_id, box_item_num, reward_index):
        """ 使用宝箱道具

        :param box_item_id:
        :param box_item_num:
        :param reward_index:
        :return:
        """
        box_item_config = game_config.use_item_box.get(box_item_id)
        if box_item_config is None:
            return 100, {}

        story = box_item_config['story']
        sort = box_item_config['sort']
        user_level = self.mm.user.level
        effect = box_item_config['effect']
        reward = {}

        if user_level < box_item_config['use_lv']:
            return 101, {}

        if sort == 1:  # 普通宝箱
            for level, gift, num in story:
                if level and not (level[0] <= user_level <= level[1]):
                    continue
                for i in xrange(num * box_item_num):
                    add_mult_gift_by_weights(self.mm, gift, cur_data=reward)
        elif sort == 2:  # 钥匙宝箱
            rc, _ = del_mult_goods(self.mm, effect * box_item_num)
            if rc != 0:
                return rc, {}
            for level, gift, num in story:
                if level and not (level[0] <= user_level <= level[1]):
                    continue
                for i in xrange(num * box_item_num):
                    add_mult_gift_by_weights(self.mm, gift, cur_data=reward)
        elif sort == 3:  # x选x宝箱
            for i in xrange(box_item_num):
                if len(reward_index) > effect:
                    return 102, {}  # 选择的奖励数量不对
                gift = []
                reward1 = []
                for level, _gift, num in story:
                    if level and not (level[0] <= user_level <= level[1]):
                        continue
                    reward1 = _gift
                    break

                for index in reward_index:
                    if index >= len(reward1):
                        continue
                    gift.append(reward1[index])
                if not gift:
                    return 101, {}
                add_mult_gift(self.mm, gift, cur_data=reward)
        elif sort == 4:  # 伪概率宝箱
            for i in xrange(box_item_num):
                box_times = self.item.get_box_times(box_item_id)
                k = box_times % sum(effect)
                if k == 0:
                    k = sum(effect)
                for index, num in enumerate(effect):
                    if k <= num:
                        break
                    else:
                        k -= num
                else:
                    index = 0

                level, gift, num = story[index]
                for j in xrange(num):
                    add_mult_gift_by_weights(self.mm, gift, cur_data=reward)
                self.item.add_box_times(box_item_id)

        return 0, reward

    def set_item_group(self, group_id, name, group):
        """ 设置道具组

        :param group_id:
        :param icon:
        :param group:
        :return:
        """
        if not (1 <= group_id <= self.mm.battle_item.GROUP_NUM):
            return 1, {}

        if not (0 <= len(group) <= self.mm.battle_item.EACH_GROUP_MAX_NUM):
            return 2, {}

        for item_id in group:
            if not item_id:
                continue
            if item_id not in game_config.battle_item_skill:
                return 3, {}

        if not self.mm.battle_item.groups[group_id]['status']:
            return 4, {}

        self.mm.battle_item.groups[group_id]['name'] = name
        self.mm.battle_item.groups[group_id]['group'] = group

        self.mm.battle_item.save()

        return 0, {'bitem_groups': self.mm.battle_item.groups}

    def synthesis_aitem(self, awaken_id, num):
        """
        合成觉醒材料
        :param awaken_id: 觉醒材料id
        :param num: 合成数量
        :return:
        """
        awaken_config = game_config.awaken_material.get(awaken_id, {})
        if not awaken_config:
            return 1, {}  # 没有该觉醒材料的配置

        cost = awaken_config['cost'] * num
        rc, _ = del_mult_goods(self.mm, cost)
        if rc != 0:
            return rc, {}

        self.aitem.add_item(awaken_id, num)
        self.aitem.save()

        return 0, {}

    def synthesis_item(self, item_id, num):
        """
        道具碎片合成
        :param item_id: 碎片道具id
        :param num: 合成几个目标道具
        :return:
        """
        item_config = game_config.use_item.get(item_id)
        if not item_config:
            return 'error_config', {}

        if not item_config['is_piece'] or item_config['is_use'] != 11:
            return 1, {}  # 不能合成

        use_num = item_config['use_num'] * num
        use_effect = item_config['use_effect']

        if self.item.get_item(item_id) < use_num:
            return 'error_item', {}  # 道具不足

        self.item.del_item(item_id, use_num)
        reward = add_gift(self.mm, 3, use_effect * num)

        self.item.save()

        return 0, {
            'reward': reward,
        }

    def sell_item(self, item_type, item_id, num):
        """
        出售道具
        :param item_type: 道具类型
        :param item_id:
        :param num:
        :return:
        """
        item_obj = None
        config = None

        if item_type == 'item':
            pass
        elif item_type == 'grade_item':
            item_obj = self.mm.grade_item
            config = game_config.grade_lvlup_item
        elif item_type == 'awaken_item':
            pass
        else:
            return 'error_100', {}

        if not item_obj or not config:
            return 'error_100', {}

        if item_obj.get_item(item_id) < num:
            return 'error_gitem', {}

        if item_id not in config:
            return 'error_config', {}

        icon_exchange = config[item_id].get('price', 0) * num
        if icon_exchange <= 0:
            return 1, {}  # 不可出售

        item_obj.del_item(item_id, num)
        self.mm.user.add_silver(icon_exchange)

        item_obj.save()
        self.mm.user.save()

        return 0, {
            'reward': {'silver': icon_exchange}
        }
