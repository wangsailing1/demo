#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time
from celery_app import app

@app.task
def multiply(x, y):
    time.sleep(2)
    return x * y
