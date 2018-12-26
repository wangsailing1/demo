#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
from celery_app import app


@app.task
def add(x, y):
    time.sleep(0.1)
    return x + y
