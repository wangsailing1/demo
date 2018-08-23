#! --*-- coding: utf-8 --*--

__author__ = 'sm'

"""
考虑到有长连接, 所有把数据分开
"""

from lib.db import ModelBase
from lib.core.environ import ModelManager
from lib.utils import add_dict


class Item(ModelBase):
    """ 道具类 game_config.use_item

    :var items: 普通道具, {道具id: 数量}
    :var box_item_times: {宝箱id: 次数}     # 伪概率宝箱开启次数
    """
    _need_diff = ('items',)

    REEL_ITEM = 20071   # 时间胶囊(卷轴)道具id
    MAX_REEL_NUM = 20   # 时间胶囊(卷轴)最大数量

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'items': {},
            'box_item_times': {}
        }
        super(Item, self).__init__(self.uid)

    def get_item(self, item_id):
        """ 获取道具数量

        :param item_id:
        :return:
        """
        return self.items.get(item_id, 0)

    def add_item(self, item_id, item_num):
        """ 增加道具

        :param item_id:
        :param item_num:
        :return:
        """
        item_num = int(item_num)
        if item_id == self.REEL_ITEM and self.get_item(item_id) >= self.MAX_REEL_NUM:   # 时间胶囊(卷轴)道具获得上限
            return
        add_dict(self.items, item_id, item_num)

    def del_item(self, item_id, item_num):
        """ 删除道具

        :param item_id:
        :param item_num:
        :return:
        """
        owned_num = self.get_item(item_id)
        if owned_num < item_num:
            return False
        elif owned_num == item_num:
            self.items.pop(item_id)
        else:
            add_dict(self.items, item_id, -item_num)

        return True

    def get_box_times(self, box_item_id):
        """
        记录伪概率宝箱开启次数
        :param box_item_id:
        :return:
        """
        return self.box_item_times.get(box_item_id, 1)

    def add_box_times(self, box_item_id, num=1):
        """
        记录伪概率宝箱开启次数
        :param box_item_id:
        :return:
        """
        self.box_item_times[box_item_id] = self.box_item_times.get(box_item_id, 1) + num


class GradeItem(ModelBase):
    """ 进阶道具, 勋章, 基因药剂 game_config.grade_lvlup_item

    :var items: 进阶材料道具, {道具id: 数量}
    """
    _need_diff = ('items',)

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'items': {},
        }
        super(GradeItem, self).__init__(self.uid)

    def get_item(self, item_id):
        """ 获取道具数量

        :param item_id:
        :return:
        """
        return self.items.get(item_id, 0)

    def add_item(self, item_id, item_num):
        """ 增加道具

        :param item_id:
        :param item_num:
        :return:
        """
        item_num = int(item_num)
        add_dict(self.items, item_id, item_num)

    def del_item(self, item_id, item_num):
        """ 删除道具

        :param item_id:
        :param item_num:
        :return:
        """
        owned_num = self.get_item(item_id)
        if owned_num < item_num:
            return False
        elif owned_num == item_num:
            self.items.pop(item_id)
        else:
            add_dict(self.items, item_id, -item_num)

        return True


class CollItem(ModelBase):
    """ 采集物道具 game_config.collection_resource

    :var items: 采集物道具, {道具id: 数量}
    """
    _need_diff = ('items',)

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'items': {},
        }
        super(CollItem, self).__init__(self.uid)

    def get_item(self, item_id):
        """ 获取道具数量

        :param item_id:
        :return:
        """
        return self.items.get(item_id, 0)

    def add_item(self, item_id, item_num):
        """ 增加道具

        :param item_id:
        :param item_num:
        :return:
        """
        item_num = int(item_num)
        add_dict(self.items, item_id, item_num)

    def del_item(self, item_id, item_num):
        """ 删除道具

        :param item_id:
        :param item_num:
        :return:
        """
        owned_num = self.get_item(item_id)
        if owned_num < item_num:
            return False
        elif owned_num == item_num:
            self.items.pop(item_id)
        else:
            add_dict(self.items, item_id, -item_num)

        return True


class GuildGiftItem(ModelBase):
    """ 公会礼物道具 game_config.guild_herogift

    :var items: 公会礼物道具, {道具id: 数量}
    """
    _need_diff = ('items',)

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'items': {},
        }
        super(GuildGiftItem, self).__init__(self.uid)

    def get_item(self, item_id):
        """ 获取道具数量

        :param item_id:
        :return:
        """
        return self.items.get(item_id, 0)

    def add_item(self, item_id, item_num):
        """ 增加道具

        :param item_id:
        :param item_num:
        :return:
        """
        item_num = int(item_num)
        add_dict(self.items, item_id, item_num)

    def del_item(self, item_id, item_num):
        """ 删除道具

        :param item_id:
        :param item_num:
        :return:
        """
        owned_num = self.get_item(item_id)
        if owned_num < item_num:
            return False
        elif owned_num == item_num:
            self.items.pop(item_id)
        else:
            add_dict(self.items, item_id, -item_num)

        return True


class AwakenItem(ModelBase):
    """
    觉醒道具 game_config.awaken_material

    :var items: 觉醒道具, {道具id: 数量}
    """

    _need_diff = ('items', )

    SYNTHESIS_NUM = 8   # 8个觉醒材料合成一个更高级的材料

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'items': {},
        }
        super(AwakenItem, self).__init__(self.uid)

    def add_item(self, item_id, item_num):
        """
        增加道具
        :param item_id:
        :param item_num:
        :return:
        """
        item_num = int(item_num)
        add_dict(self.items, item_id, item_num)

    def get_item(self, item_id):
        """
        获得道具
        :param item_id:
        :return:
        """
        return self.items.get(item_id, 0)

    def del_item(self, item_id, item_num):
        """
        删除道具
        :param item_id:
        :param item_num:
        :return:
        """
        owned_item = self.get_item(item_id)
        if owned_item < item_num:
            return False
        elif owned_item == item_num:
            self.items.pop(item_id)
        else:
            add_dict(self.items, item_id, -item_num)

        return True


ModelManager.register_model('item', Item)
ModelManager.register_model('grade_item', GradeItem)
ModelManager.register_model('coll_item', CollItem)
ModelManager.register_model('guild_gift_item', GuildGiftItem)
ModelManager.register_model('awaken_item', AwakenItem)
