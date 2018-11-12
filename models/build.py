#! --*-- coding: utf-8 --*--

import time
import datetime
import copy

from lib.core.environ import ModelManager
from gconfig import game_config
from tools.gift import add_mult_gift, has_mult_goods
from lib.utils.time_tools import strftimestamp
from return_msg_config import i18n_msg
from lib.db import ModelBase, ModelTools
from models import server as serverM
from gconfig import get_str_words
import settings