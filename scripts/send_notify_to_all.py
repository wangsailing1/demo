#!/usr/bin/env python
# coding: utf-8

"""
批量向指定 ID 的玩家發送系統郵件 - 可以帶獎勵
"""

import sys
import os.path

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(CUR_PATH, os.path.pardir)
sys.path.insert(0, ROOT_PATH)

import settings

env = sys.argv[1]
filename = sys.argv[2]

settings.set_env(env)

from lib.core.environ import ModelManager

def send_user_notify(user_id):
    title = u''
    content = u''''''
    gifts = []
    mm = ModelManager(user_id)
    mail_dict = mm.mail.generate_mail(
        content,
        title=title,
        gift=gifts,
    )
    mm.mail.add_mail(mail_dict, save=True)
    mm.mail.save()

    return user_id

success = []

# 获取区服列表
if not os.path.exists(filename):
    exit(1)
f = open(filename)

for l in f:
    user_id = l.strip()
    print send_user_notify(user_id)
