#! --*-- coding: utf-8 --*--

__author__ = 'sm'


from lib.db import ModelBase
from lib.core.environ import ModelManager
from lib.utils import add_dict


class Equip(ModelBase):
    """ 装备类 game_config.use_equip

    :var equips: 普通装备, {装备id: 数量}
    :var box_equip_times: {宝箱id: 次数}     # 伪概率宝箱开启次数
    """
    _need_diff = ('equips', 'equip_pieces')

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'equips': {},
            'equip_pieces': {},
        }
        super(Equip, self).__init__(self.uid)

    def get_equip(self, item_id):
        """ 获取装备数量

        :param item_id:
        :return:
        """
        return self.equips.get(item_id, 0)

    def add_equip(self, item_id, item_num):
        """ 增加装备

        :param item_id:
        :param item_num:
        :return:
        """
        add_dict(self.equips, item_id, item_num)

    def del_equip(self, item_id, item_num):
        """ 删除装备

        :param item_id:
        :param item_num:
        :return:
        """
        owned_num = self.get_equip(item_id)
        if owned_num < item_num:
            return False
        elif owned_num == item_num:
            self.equips.pop(item_id)
        else:
            add_dict(self.equips, item_id, -item_num)

        return True

    def get_piece(self, piece_id):
        """ 获取碎片数量

        :param piece_id:
        :return:
        """
        return self.equip_pieces.get(piece_id, 0)

    def add_piece(self, piece_id, piece_num):
        """ 增加碎片

        :param piece_id:
        :param piece_num:
        :return:
        """
        piece_num = int(piece_num)
        add_dict(self.equip_pieces, piece_id, piece_num)

    def del_piece(self, piece_id, piece_num):
        """ 删除碎片

        :param piece_id:
        :param piece_num:
        :return:
        """
        owned_num = self.get_piece(piece_id)
        if owned_num < piece_num:
            return False
        elif owned_num == piece_num:
            self.equip_pieces.pop(piece_id)
        else:
            add_dict(self.equip_pieces, piece_id, -piece_num)

        return True


ModelManager.register_model('equip', Equip)
