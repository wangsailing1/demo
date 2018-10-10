#! --*-- coding: utf-8 --*--

import time
import math

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class Block(ModelBase):

    def __init__(self,uid=None):
        self.uid = uid
        self._attrs = {
            'block':1,
            'cup':0,
            'block_group':1,
        }