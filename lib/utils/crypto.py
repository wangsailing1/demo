#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import urllib
import hmac
import base64
import hashlib
import cStringIO as StringIO
from M2Crypto import BIO, RSA, EVP
from xml.sax import handler, parseString


def hmac_sha(key, context):
    return hmac.new(key, context.encode('utf-8'), hashlib.sha1).hexdigest()


def md5(context):
    if isinstance(context, unicode):
        context = context.encode('utf-8')
    return hashlib.md5(context).hexdigest()


def hmac_md5(key, context):
    return hmac.new(key, context, hashlib.md5).hexdigest()


def rsa_public_encrypt(public_key, message, rsa=None):
    """ RSA方式公钥加密数据

    :param public_key: 公钥
    :param message: 要加密的数据
    :param rsa: rsa对象
    :return:
    """
    if rsa is None:
        bio = BIO.MemoryBuffer(public_key)
        rsa = RSA.load_pub_key_bio(bio)

    m = rsa.public_encrypt(str(message), RSA.pkcs1_padding)
    return base64.b64encode(m)


def rsa_public_decrypt(public_key, sign, max_decrypt_block=0, rsa=None):
    """ rsa方式公钥解密数据

    :param public_key: 公钥
    :param sign: 要解密的数据
    :param max_decrypt_block: 是否需分段解密 0：无需分段解密；正整数：为分段解密块长度
    :param rsa: rsa对象
    :return:
    """
    if rsa is None:
        bio = BIO.MemoryBuffer(public_key)
        rsa = RSA.load_pub_key_bio(bio)

    b64string = base64.b64decode(sign)

    if max_decrypt_block > 0:
        s = StringIO.StringIO(b64string)
        decrypt_data = ''
        while True:
            data = s.read(max_decrypt_block)
            if not data:
                break
            decrypt_data += rsa.public_decrypt(data, RSA.pkcs1_padding)
        return decrypt_data
    else:
        return rsa.public_decrypt(b64string, RSA.pkcs1_padding)


def rsa_private_encrypt(private_key, message, rsa=None):
    """ RSA方式私钥加密数据

    :param private_key: 公钥
    :param message: 要加密的数据
    :param rsa: rsa对象
    :return:
    """
    if rsa is None:
        bio = BIO.MemoryBuffer(private_key)
        rsa = RSA.load_key_bio(bio)

    m = rsa.private_encrypt(str(message), RSA.pkcs1_padding)
    return base64.b64encode(m)


def rsa_private_decrypt(private_key, sign, rsa=None):
    """ rsa方式私钥解密数据

    :param private_key: 私钥
    :param sign: 要解密的数据
    :param rsa: rsa对象
    :return:
    """
    if rsa is None:
        bio = BIO.MemoryBuffer(private_key)
        rsa = RSA.load_key_bio(bio)

    b64string = base64.b64decode(sign)
    return rsa.private_decrypt(b64string, RSA.pkcs1_padding)


def rsa_private_sign(private_key, message, rsa=None):
    """ RSA方式私钥签名数据

    :param private_key: 私钥
    :param message:
    :return:
    """
    if rsa is None:
        bio = BIO.MemoryBuffer(private_key)
        rsa = RSA.load_key_bio(bio)

    sha1_digest = hashlib.sha1(message).digest()
    m = rsa.sign(sha1_digest, algo='sha1')

    return base64.encodestring(m)


def rsa_verify_signature(public_key, signed_data, signature, md='sha1', rsa=None):
    """ rsa方式验证数据签名

    :param public_key:  公钥， 已格式化的pem
    :param signed_data: 要验证的数据
    :param signature:   签名
    :param md:          数据的算法, 默认sha1
    :param rsa:         rsa对象
    :return:
    """
    if rsa is None:
        bio = BIO.MemoryBuffer(public_key)
        rsa = RSA.load_pub_key_bio(bio)

    key = EVP.PKey()
    key.assign_rsa(rsa, capture=0)
    key.reset_context(md=md)
    key.verify_init()
    key.verify_update(signed_data)
    return key.verify_final(base64.b64decode(signature)) == 1


def rsa_verify_signature_private(private_key, signed_data, signature, md='sha1', rsa=None):
    """ rsa方式验证数据签名

    :param private_key:  私钥， 已格式化的pem
    :param signed_data: 要验证的数据
    :param signature:   签名
    :param md:          数据的算法, 默认sha1
    :param rsa:         rsa对象
    :return:
    """
    if rsa is None:
        bio = BIO.MemoryBuffer(private_key)
        rsa = RSA.load_key_bio(bio)

    key = EVP.PKey()
    key.assign_rsa(rsa, capture=0)
    key.reset_context(md=md)
    key.verify_init()
    key.verify_update(signed_data)
    return key.verify_final(base64.b64decode(signature)) == 1


def aes_encrypt(aes_key, message, iv='\0' * 16):
    """ aes方式加密数据

    :param aes_key:     秘钥
    :param message:     要加密的数据
    :param iv:
    :param cipher:
    :return:
    """
    cipher = EVP.Cipher(alg='aes_128_ecb', key=aes_key, iv=iv, op=1)
    aes_data = cipher.update(message)
    aes_data += cipher.final()
    del cipher
    return base64.b64encode(aes_data)


def aes_decrypt(aes_key, aes_data, iv='\0' * 16):
    """ aes方式解密数据

    :param aes_key:     秘钥
    :param aes_data:    要解密的数据
    :param iv:
    :param cipher:
    :return:
    """
    base64_data = base64.b64decode(aes_data)

    cipher = EVP.Cipher(alg='aes_128_ecb', key=aes_key, iv=iv, op=0)
    buf = cipher.update(base64_data)
    buf += cipher.final()
    del cipher
    return buf


def des3_encrypt(des3_key, data, iv='\0' * 16):
    """ des3方式加密数据

    :param des3_key:
    :param data:
    :param iv:
    :return:
    """
    cipher = EVP.Cipher(alg='des_ede3_ecb', key=des3_key, op=1, iv=iv)

    buf = cipher.update(data)
    buf += cipher.final()
    del cipher
    return buf


def des3_decrypt(des3_key, des3_data, iv='\0' * 16):
    """ des3方式解密数据

    :param des3_key:
    :param des3_data:
    :param iv:
    :return:
    """
    base64_data = base64.b64decode(des3_data)

    cipher = EVP.Cipher(alg='des_ede3_ecb', key=des3_key, op=0, iv=iv)

    buf = cipher.update(base64_data)
    buf += cipher.final()
    del cipher
    return buf


def parse_keqv(data):
    """ 解析key=value为字典

    """
    data = urllib.unquote(data)

    pairs = (s1 for s1 in data.split('&'))

    parsed = {}
    for name_value in pairs:
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            continue
        parsed[nv[0]] = nv[1]
    return parsed


def xml2dict(xml_data):
    """解析支付定单数据xml到字典格式
    Args:
        xml_data: xml数据
    Returns:
        字典格式数据
    """
    if isinstance(xml_data, unicode):
        xml_data = xml_data.encode('utf-8')

    xh = XMLHandler()
    parseString(xml_data, xh)

    return xh.getDict()


class XMLHandler(handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping
