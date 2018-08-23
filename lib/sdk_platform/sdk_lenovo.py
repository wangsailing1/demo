# coding: utf-8

import urllib
import json
import base64
import httplib
from lib.utils.debug import print_log

from helper import http
from helper import utils

PLATFORM_NAME = 'lenovo'
# 分配的app_id
APP_ID = '1712260967884.app.ln'
APP_KEY = """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAII8Cg1d1GRM31rF
8FsZGAPpE3khuNs0ljezNQbUQj7IOn2CoBS2kxCr+jD/dHadNtlJfP2sAQp7lNcA
ftxOE903bFRazVztJRfLgm0sc2/pU0OEBcjT2/JMEIE+4h+a6P5eVyPPeKNihcCy
3E5OSQFYYTPvUXdUjeTmnYgMgvHvAgMBAAECgYAjf0fiIswMVqOec0szGWDhV/sV
zio7nVbAcdknNl2kDSFcKmmFm8n0BlwYVNiip/FWQmCOJ/7Uo6CLBbiORb3F72bc
HOikX7nah+KK/BTNGHqw1gzZqYu97lJsrOA5QzL2HqO3K2U+UcSIC8znLEQ36iVD
4x/gRl6W//Lha6H4AQJBAMIhGR2S2qCt2FGR6hiYbxpvNRkz3eclNtGqhBKO9NoD
HqPSDfNatzuwHEg3g2jpi/RxI6uAoW50Am62KGSYLe8CQQCrvc2B+rO1Lm1MF7XC
J+NWyIV4mMwXpQMTjUkRQSaMYoXkMpjf/qfZO5Gx9P2rWqtXrpGrw5oelSvol6+0
BXwBAkAZttql0TMGf6CcxXA1y9NDtCFbckRdfs9xHF4cOzVxv2IKnyNb7dNBo8VL
R5cviWgRe/8Wk5ZOlC1STuywznufAkB6YD4PD4B8az+wh/iZB+lDzpDk9SQA+TEu
/m8BX4ZDZHT5vWAXxJMABSV1RBh5wJr1WMwuM6wffLYT//pQcdQBAkEAqq7f+spA
4pI/xdeWFsneIRvWORr9ihngxZ5RRGLUREXyHslj0xeY+XTvUxvg1kRGmJibrwmy
McH7B0ho2v7Itg==
-----END PRIVATE KEY-----"""
HOST = 'passport.lenovo.com'
PATH = '/interserver/authen/1.2/getaccountid'
VERIFY_TOKEN_URL = 'http://%s%s' % (HOST, PATH)
# 支付成功和失败之后的返回值
RETURN_DATA = {
    0: 'SUCCESS',
    1: 'FAILURE',
}

def login_verify(req, lpsust=None):
    """登陆验证
    Args:
        lpsust: 用来标志用户身份的一个ticket,这ST(Token)
    Returns:
        openid
    """
    if not lpsust:
        lpsust = req.get_argument('session_id')

    query_data = urllib.urlencode({
        'lpsust': lpsust,
        'realm': APP_ID,
    })
    conn = httplib.HTTPConnection(HOST)
    conn.request("GET", PATH + '?'+query_data)
    # 忽略http 406错误
    res = conn.getresponse()
    content = res.read()

    result = utils.xml2dict(content)
    return {
        'openid': result.get('AccountID'),           # 平台用户ID
    }


def payment_verify(req, params=None):
    """支付验证
    Args:
        params: 验证需要的所有数据,以下是必须的
            sign: 签名
            transdata: 票据，JSON格式
                exorderno: 外部订单号  商户生成的订单号
                transid:   交易流水号  计费支付平台的交易流水号
                appid:     游戏 id  平台为商户应用分配的唯一代码
                waresid:   商品编码 商品编号,目前默认为 1
                feetype:   计费方式 计费类型:0–消费型_应用传入价格
                money:     交易金额  本次交易的金额,单位:分
                count:     购买数量 本次购买的商品数量
                result:    交易结果 交易结果:0–交易成功;1–交易失败
                transtype: 交易类型 交易类型:0 – 交易;1 – 冲正
                transtime: 交易时间 交易时间格式: yyyy-mm-dd hh24:mi:ss
                cpprivate: 商户私有信息
                paytype:   支付方式
    Returns:
        验证成功返回支付数据，失败返回None
    """
    if not params:
        params = {
            'sign':         req.get_argument('sign', ''),
            'transdata':    req.get_argument('transdata', ''),
        }

    sign = utils.force_str(params['sign'])
    transdata = utils.force_str(params['transdata'])

    if not sign or not transdata:
        return RETURN_DATA, None

    data = json.loads(transdata)
    # 按接受成功处理
    if int(data['result']) != 0:
        return_data = dict(RETURN_DATA)
        return_data[1] = RETURN_DATA[0]
        return return_data, None
    new_sign = utils.rsa_private_sign(APP_KEY, transdata)
    if new_sign != sign:
        return RETURN_DATA, None

    pay_data = {
        'app_order_id':       data['exorderno'],         # 自定义定单id
        'order_id':           data['transid'],             # 平台定单id
        'platform':           PLATFORM_NAME,                  # 平台标识名
        'real_price':         float(data['money']) / 100      # 实际充值人民币数　单位元
    }
    return RETURN_DATA, pay_data


if __name__ == '__main__':
    pass
    # lpsust = 'ZAgAAAAAAAGE9MTAwMjk0MjI2MTMmYj0yJmM9NCZkPTEyNzY3JmU9REU4OUJDQTgyNTRCODhFQkNFRDFFMEFFMkVBODM0QzMxJmg9MTQzNjg2MDA1NTg1NiZpPTQzMjAwJmo9MCZvPTg2NjY1NDAyMzIxNDgwOSZwPWltZWkmcT0wJnVzZXJuYW1lPTE1NjUyMzQzMTMxJmlsPWNuPCUD-eiUhGOKJyOWKXcOvg'
    # print login_verify(None, lpsust)
    # print parse_key(APP_KEY)
    # transdata = '{"exorderno":"10004200000001100042","transid":"02113013118562300203","waresid":1,"appid":"20004600000001200046","feetype":0,"money":3000,"count":1,"result":0,"transtype":0,"transtime":"2013-01-31 18:57:27","cpprivate":"123456"}'
    # key = 'MjhERTEwQkFBRDJBRTRERDhDM0FBNkZBMzNFQ0RFMTFCQTBCQzE3QU1UUTRPRFV6TkRjeU16UTVNRFUyTnpnek9ETXJNVE15T1RRME9EZzROVGsyTVRreU1ETXdNRE0zTnpjd01EazNNekV5T1RJek1qUXlNemN4';
    # sign = '28adee792782d2f723e17ee1ef877e7 166bc3119507f43b06977786376c0434 633cabdb9ee80044bc8108d2e9b3c86e';
    # print payment_verify({'sign': sign, 'transdata': transdata, 'key': key})
    #print parse_key(APP_KEY)

