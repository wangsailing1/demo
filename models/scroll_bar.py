#! --*-- coding: utf-8 --*--
__author__ = 'yanyunfei'

import json
import time

from tools.task_event import TaskEventBase, TaskEventDispatch
from gconfig import game_config
from lib.db import ModelTools, ModelBase
from lib.core.environ import ModelManager
import settings


class ScrollBar(ModelBase, TaskEventBase):
    """
    跑马灯
    """
    # 任务类型
    S_GET_HERO = 1          # 获得xx品质英雄
    S_GET_EQUIP = 2         # 获得xx品质装备
    S_HIGH_LADDER_RANK = 3  # 竞技场xx名
    S_BOMBINE_HERO = 4      # 合成xx品质英雄
    S_COMBINE_EQUIP = 5     # 合成xx品质装备
    S_RED_BAG = 6           # 天降红包

    MAX_NUM = 30    # 跑马灯最大条数
    SYS_SORT = 0    # 系统信息的类型

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'log': [],
        }
        super(ScrollBar, self).__init__(self.uid)
        # self.mm = mm
        # father_name = settings.get_father_server(self.mm.server)
        # self.server_name = father_name
        # self._key = self.make_key(self.__class__.__name__, father_name)
        # self.redis = self.get_father_redis(father_name)

    @classmethod
    def get(cls, uid, server_name='', **kwargs):
        father_name = settings.get_father_server(server_name)
        o = super(ScrollBar, cls).get(uid, server_name=father_name, **kwargs)
        o.server_name = father_name
        o._key = cls.make_key_cls(cls.__name__, father_name)
        o.redis = o.get_father_redis(father_name)
        return o

    def add_message(self, data):
        """
        增加跑马灯信息
        :param data: {
            'uid': '',
            'name': '',
            'target_sort': 0,   # 对应卡牌的品质, 装备的品质
            'target_name': '',
        }
        :return:
        """
        # if self.redis.llen(self._key) >= self.MAX_NUM:
        #     self.redis.lpop(self._key)
        #
        # data = json.dumps(data)
        # self.redis.rpush(self._key, data)

        from chat.to_server import send_to_all
        try:
            send_to_all(data, self.server_name)
        except:
            print 'scroll_bar send msg err'

    def generate_msg(self, mid, uid='', name='', target1='', target2='', hero_id='', equip_id='', arena_rank=''):
        """
        生成跑马灯信息
        :param mid: 跑马灯配置id
        :param uid:
        :param name:
        :param target1:
        :param target2:
        :return:
        """
        data = {
            'message_id': mid,
            'uid': uid,
            'name': name,
            'target1': target1,     # 卡牌档次
            'target2': target2,     # 卡牌配置id
            'hero_id': hero_id,
            'equip_id': equip_id,
            'arena_rank': arena_rank,
        }
        return data

    def script_first_luck(self, mm):
        """拍片首次爆款"""
        msg = self.generate_msg('')
        msg['msg'] = u'test_first_luck %s' % mm.uid
        self.add_message(msg)

    def script_step_luck(self, mm):
        """拍片爆款后达成阶段性目标"""
        msg = self.generate_msg('')
        msg['msg'] = u'test_step-luck %s' % mm.uid
        self.add_message(msg)

    # ########################
    # 对应触发任务 start
    # ########################

    def high_ladder(self, *args, **kwargs):
        """
        竞技场排名
        :param args:
        :param kwargs:
        :return:
        """
        sort = self.S_HIGH_LADDER_RANK
        cur_rank = kwargs.get('cur_rank')
        mm = kwargs.get('mm')

        if not cur_rank or not mm:
            return

        message_config_mapping = game_config.get_message_mapping(sort)
        for i, j in message_config_mapping.iteritems():
            if not j['is_show'] or j['target2'] != cur_rank:
                continue
            msg = self.generate_msg(i, uid=mm.uid, name=mm.user.name, target1=cur_rank, arena_rank=cur_rank)
            self.add_message(msg)
            break

    # ########################
    # end
    # ########################


ModelManager.register_model('scroll_bar', ScrollBar)
# TaskEventDispatch.register_model('scroll_bar', ScrollBar)
