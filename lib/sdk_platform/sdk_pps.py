# -*- coding: utf-8 -*-
# Android系统 PPS爱奇艺平台

__version__ = '1.5.6'


from lib.utils import crypto
from lib.sdk_platform.manager import SDKManager


PLATFORM_INFO = {
    'pps': {
        'app_id': 521,
        'app_key': '74974bf301ff7e270d0e1e6860735f38',
        'payment_key': '&^PPSgames',
    },
}


STRING_VERIFICATION_URL = 'http://passport_i.25pp.com:8080/account?tunnel-command=2852126760'


class SDKPPS(object):

    SUCCESS = {'result': 0, 'message': 'success'}
    FAIL = {'result': -1, 'message': 'sign error'}

    def __init__(self, pf, *args, **kwargs):
        self.name = pf
        self.app_id = PLATFORM_INFO.get(pf, {}).get('app_id', '')
        self.app_key = PLATFORM_INFO.get(pf, {}).get('app_key', '')
        self.payment_key = PLATFORM_INFO.get(pf, {}).get('payment_key', '')

    def login_check(self, *args, **kwargs):
        """

        :param session_id:
        :param args:
        :param kwargs:
        :return:
        """
        return {}

    def payment_verify(self, data_dict):
        """支付验证

        :param data_dict:
            参数名	     说明	   样例	        是否必填
            user_id	    用户id	 65430637	        是
            role_id	    角色ID，没有传空 	xxxxxxxx	是
            order_id	平台订单号（唯一）	45816888	是
            money	    充值金额（人民币，单位元）	100	是
            time	    时间戳 time()	132526542	是
            userData	"回传参数(urlencode)。
                        注意：该参数内容为游戏方自定义内容,如游戏方服务器ID等。PPS将原样传回给游戏方"	xxxxxx	是
            sign	    "经过加密后的签名，sign= MD5($user_id.$role_id.$order_id.$money.$time.$key)
                        注意：上面的 MD5函数中的“.” 号实为PHP语言字符串拼接符，等同于Java语言中的”+”号，非常规意义的点号"		是
        :return True: 支付成功, 已经加过商品
                False: 支付失败
                {}: 支付成功, 返回详细信息
        """
        sign = data_dict.get('sign')

        if sign is None:
            return False

        gen_sign = crypto.md5('%s%s%s%s%s%s' % (data_dict['user_id'], data_dict['role_id'], data_dict['order_id'],
                                                data_dict['money'], data_dict['time'], self.payment_key))

        if sign != gen_sign:
            return False

        pay_data = dict(game_order_id=data_dict['userData'], order_id=data_dict['order_id'],
                        amount=float(data_dict['money']), uin=data_dict['user_id'])

        return pay_data


SDKManager.register('sdk_pps', SDKPPS)
