#! --*-- coding: utf-8 --*--

__author__ = 'sm'


import settings


pre_platform_mapping = {
    'PP': 'pp',
    'JY': 'jy',
    'itools': 'itools',
    'baidu': 'baidu',
    '360': '360',
    'and_haima': 'haima',
    'ios_haima': 'haima',
    'pps': 'pps',
    'le8': 'le8',
    'vivo': 'vivo',
    'yyh': 'yyh',
    'jinli': 'jinli',
    'lenovo': 'lenovo',
    'youku': 'youku',
    'huawei': 'huawei',
    'and_kuaiyong': 'kuaiyong',
    'ios_kuaiyong': 'kuaiyong',
    'uc': 'uc',
    'yy': 'yy',
    'xiaomi': 'xiaomi',
    'woniu': 'woniu',
    'kugou': 'kugou',
    'wandoujia': 'wandoujia',
    'ouwan': 'ouwan',
    'kuaiwan': 'kuaiwan',
    'muzhiwan': 'muzhiwan',
    '91': '91',
    'changtianyou': 'changtianyou',
    'androidkvgames': 'androidkvgames',
    'ioskvgames': 'ioskvgames',
}


def login_verify(hm, channel):
    """ 验证登录

    :param hm:
    :param channel:
        openid:
        session_id:
        token:
        channel_id:
    :return:
    """
    openid = hm.get_argument('openid')
    session_id = hm.get_argument('session_id')
    if not session_id:
        return None, None, None
    module_name = ('sdk_%s' % channel)
    method_name = 'login_verify'
    module = __import__('lib.sdk_platform.%s' % module_name, globals(), locals(), [method_name])
    method_func = getattr(module, method_name, None)
    access_result = None
    if callable(method_func):
        data = method_func(hm)
        if data is None:
            return None, None, None

        channel = data.get('channel', channel)
        if channel == 'coolpad':
            openid = data
            pre_platform = pre_platform_mapping.get(channel, channel)
            account = '%s_%s' % (pre_platform, openid['openid'])
        else:
            openid = data.get('openid', openid)
            pre_platform = pre_platform_mapping.get(channel, channel)
            account = '%s_%s' % (pre_platform, openid)

        return account, openid, channel
