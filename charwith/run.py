#! --*-- coding: utf-8 --*--
from tornado.web import RequestHandler
import redis

class ChatWith(RequestHandler):
    def get(self, *args, **kwargs):
        return 
