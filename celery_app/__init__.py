#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

from celery import Celery
import settings

app = Celery('demo')
app.config_from_object('celery_app.celeryconfig')


def which_queue(server, city_id=0):
    # num = city_id % 2
    server = settings.get_father_server(server)
    return 'celery_' + server
