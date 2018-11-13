#! --*-- coding: utf-8 --*--

import time

from lib.db import ModelBase
from lib.core.environ import ModelManager
from gconfig import game_config


class Build(ModelBase):
    def __init__(self, uid=None):
        self.uid = uid
        self._attrs = {
            '_build': {},
        }
        super(Build, self).__init__(self.uid)

    def pre_use(self):
        if not self._build:
            for build_id,value in game_config.building.iteritems():
                if value['default']:
                    self.add_build(build_id,0)
            self.save()

    def add_build(self, build_id, pos):
        if build_id in self._build:
            return
        self._build[build_id] = {'pos': pos,
                                 'build_time': int(time.time())}
        self.save()

    @property
    def group_ids(self):
        _group_ids = {}
        config = game_config.building
        for build_id,value in self._build.iteritems():
            group = config[build_id]['group']
            _group_ids[group] = {'build_id':build_id,
                                      'pos':value['pos'],
                                      'lock_status':self.mm.user.level < config[build_id]['unlock_lv'],
                                      'unlock_lv':config[build_id]['unlock_lv']
                                      }
        return _group_ids

    @property
    def get_pos_info(self):
        pos_info = {}
        for build_id,value in self._build.iteritems():
            pos_info[value['pos']] = build_id
        return pos_info

    def check_build(self,build_id):
        config = game_config.building
        if build_id not in config:
            return 1  #配置错误
        group = config[build_id]['group']
        if group not in self.group_ids:
            return 2  #还未拥有建筑
        if build_id in self._build:
            return 3  #已拥有建筑
        return 0

    def up_build(self,build_id,is_save=False):
        config = game_config.building
        group_id = config[build_id]['group']
        if group_id not in self.group_ids:
            return 1  #请先建造建筑
        old_build_id = self.group_ids[group_id]['build_id']
        self._build[build_id] = self._build[old_build_id]
        self._build[build_id]['build_time'] = int(time.time())
        self._build.pop(old_build_id)
        if is_save:
            self.save()




ModelManager.register_model('build', Build)
