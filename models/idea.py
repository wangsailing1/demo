#! --*-- coding: utf-8 --*--

import settings
from lib.db import make_redis_client

class Idea(object):

    redis = make_redis_client(settings.SERVERS['public']['redis'])
    key = 'idea||player||'
    @classmethod
    def get(cls, uid=None):
        return cls()