# -*- coding: utf-8 –*-

"""
Created on 2018-12-18

@author: sm
"""

import time
from aliyun.log.logitem import LogItem
from aliyun.log.logclient import LogClient
from aliyun.log.putlogsrequest import PutLogsRequest

from celery_app import app
import settings
from lib.utils.encoding import force_unicode

end_point = settings.BDC_END_POINT
access_key_id = settings.BDC_ACCESS_KEY_ID
access_key = settings.BDC_ACCESS_KEY_SECRET

project = settings.BDC_LOG_PROJECT
logstore = settings.BDC_LOG_STORE_SERVER
topic = ''
source = ''


@app.task
def do_send_bdc_log_to_aliyun(log_contents, compress=True):
    """

    :param log_contents:
    :param compress:
    :return:
    """
    start = time.time()
    client = LogClient(end_point, access_key_id, access_key)

    log_items = []
    if isinstance(log_contents, dict):
        log_contents = [log_contents]

    for log_content in log_contents:
        log_item = LogItem()
        log_content = [(k, force_unicode(v)) for k, v in log_content.items()]
        log_item.set_contents(log_content)
        log_item.set_time(int(time.time()))
        log_items.append(log_item)

    req2 = PutLogsRequest(project, logstore, topic, source, log_items, compress=compress)
    res2 = client.put_logs(req2)
    # res2.log_print()
    print 'spend_time: %s' % (time.time() - start)
    print log_contents, compress

    # # check cursor time
    # res = client.get_end_cursor(project, logstore, 0)
    # end_cursor = res.get_cursor()
    #
    # res = client.get_cursor_time(project, logstore, 0, end_cursor)
    # res.log_print()
    #
    # res = client.get_previous_cursor_time(project, logstore, 0, end_cursor)
    # res.log_print()


def send_bdc_log_to_aliyun(log_content, compress=True):
    """
    :param log_content:  {'index': 1, 'ts': 1545211975} or [{'index': 1, 'ts': 1545211975},
                                                            {'index': 1, 'ts': 1545211975}]
    :param compress:
    :return:
    """
    if not log_content:
        return

    if settings.BDC_LOG_SEND_TO_ALIYUN:
        # todo 判断是否需要异步执行
        # do_send_bdc_log_to_aliyun(log_content, compress=compress)
        do_send_bdc_log_to_aliyun.apply_async(args=[log_content], kwargs={'compress': compress})
