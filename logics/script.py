# -*- coding: utf-8 –*-

"""
Created on 2018-09-04

@author: sm
"""

import time
import copy
from gconfig import game_config

from lib.db import ModelBase
from lib.utils import salt_generator


class ScriptLogic(object):
    def __init__(self, mm):
        self.mm = mm

    def index(self):
        script = self.mm.script
        if not script.script_pool:
            step = 0
        else:
            step = 1
            if script.cur_script:
                step = 2
                if script.cur_script['card']:
                    step = 3
                if script.cur_script['style']:
                    step = 4

        return 0, {
            'step': step,
            'script_pool': script.script_pool,
            'cur_script': script.cur_script,
            'scripts': script.scripts,
        }

    def pre_filming(self, ):
        # todo 许可证判断 use_item

        script = self.mm.script
        script.pre_filming()
        script.save()
        rc, data = self.index()
        return rc, data

    def filming(self, script_id, name):
        script = self.mm.script

        if script_id not in script.script_pool:
            return 1, {}  # 不可选剧本

        if script.cur_script:
            return 2, {}  # 拍摄中

        if script.script_pool[script_id]:
            return 3, {}  # 已拍摄

        film = script.make_film(script_id, name)
        script.cur_script = film

        script.script_pool[script_id] = 1
        script.save()
        rc, data = self.index()
        return rc, data

    def set_card(self, role_card):
        """

        :param script_id:
        :param role_card:  [(role, card_id), (role, card_id)]
        :return:
        """
        script = self.mm.script

        cur_script = script.cur_script
        if not cur_script:
            return 1, {}  # 没有拍摄中的剧本
        if cur_script['card']:
            return 2, {}  # 已选完角色

        script_config = game_config.script[cur_script['id']]
        role_ids = script_config['role_id']
        used_role, used_card = set(), set()
        for role, card_id in role_card:
            if role not in role_ids:
                return 2, {}
            if card_id in used_card:
                return 3, {}
            if role in used_role:
                return 3, {}

            used_card.add(card_id)
            used_role.add(role)
            cur_script['card'][role] = card_id

        cur_script['step'] = 2
        script.save()
        rc, data = self.index()
        return rc, data

    def set_style(self, style):
        """
        设置片子类型
        :param style:
        :return:
        """
        script = self.mm.script

        cur_script = script.cur_script
        if not cur_script:
            return 1, {}  # 没有拍摄中的剧本

        if not cur_script['card']:
            return 2, {}  # 没有演员

        cur_script['style'] = style
        cur_script['step'] = 3
        script.save()
        rc, data = self.index()
        return rc, data
