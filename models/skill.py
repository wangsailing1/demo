# -*- coding: utf-8 -*-


from lib.db import ModelBase


class Skill(ModelBase):
    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'skill': {},  # 技能

        }