#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import json
import traceback
import urllib

from M2Crypto import BIO, RSA

from lib.utils import crypto
from lib.utils.debug import print_log
from lib.utils.encoding import force_str
from lib.utils import salt_generator


BATTLE_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDTiJvCjmd3nHgzy/4Jp7lVKP2c
TQM1vDKs4B7qqIXV7m55FSvkvqIWgK3rQRli5V3GDYGipWBPGZ7FvGbHGvtooynD
ilRT/uz8NMtrcn3TreSnKTgw37iPKITtr+39OogIGAOcv/uH7fDBmAM4hMfxAU05
Uc4qoH+k8ZWiJ6qLPQIDAQAB
-----END PUBLIC KEY-----
"""

BATTLE_PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQDTiJvCjmd3nHgzy/4Jp7lVKP2cTQM1vDKs4B7qqIXV7m55FSvk
vqIWgK3rQRli5V3GDYGipWBPGZ7FvGbHGvtooynDilRT/uz8NMtrcn3TreSnKTgw
37iPKITtr+39OogIGAOcv/uH7fDBmAM4hMfxAU05Uc4qoH+k8ZWiJ6qLPQIDAQAB
AoGAd491CkhW7uI/hnc8RNTKCfo7LgbRU6PluJSMpPFPhBVZ15JB1u5wyus8YgXP
hXhCwliL9xQmFU9T0Eumg88aXYg90n1LzHAMpVgjgiQCEi0h5X2gDE2w4Y5cjYl4
ssZJ7grUYthYnDJRgw0WEf6G1QDp1fCbq7JNm/LFkei75bkCQQD8Zm8vGCT3uXlL
x64snN3bdbkmkMPqM8De1gcUHut/WhCFjZG4KRTTU5eN40bfXOhKE67ZbEtCuGwb
ODjyqeCzAkEA1oz2QuRtwQvcHOkvYM2GaDy8uVEe4SoVGpquAbtUXGVu3aaPopsy
4T193eLbPICWBXPLnGfQXpWuhDkjDrr8TwJAA0gBogcaU+4hWY7bANF5QOUi5xFy
upS5qSv3I5fTT/CHznSstEw0bRrlGX8e6MB4dJ4U49a4k8F6BlCQzPbQaQJAV/6i
ddb4SMfTdCwTWXGR4aifgqYJszGuTCYKnf014VtcuB27JWbf3E97Ewka/9qBLSVL
6g8N/+0GEYbZoQ4BswJAMRqi+EnJuDQI3wqhC+AAsbavj5TosMx0XpFFLTi9fBB7
SO2KJORu715sgJo4iu/9gkrXKEHOEKga3Hl6P7521Q==
-----END RSA PRIVATE KEY-----
"""


class BattleCrypto(object):
    """ 战斗验证
        前端持有公钥, 服务器持有私钥

    """
    def __init__(self):
        self.public_key = BATTLE_PUBLIC_KEY
        self.public_bio = BIO.MemoryBuffer(self.public_key)
        self.public_rsa = RSA.load_pub_key_bio(self.public_bio)
        self.private_key = BATTLE_PRIVATE_KEY
        self.private_bio = BIO.MemoryBuffer(self.private_key)
        self.private_rsa = RSA.load_key_bio(self.private_bio)

    def battle_start_decrypt(self, key, data):
        """ 战斗开始前解密前端数据

        :param key:
        :param data:
        :return:
        """
        try:
            key = key.replace(' ', '+')
            data = data.replace(' ', '+')
            aes_key = crypto.rsa_private_decrypt(self.private_key, key, rsa=self.private_rsa)
            print_log('BattleCrypto.battle_start_decrypt: ', aes_key, data)
            aes_data = crypto.aes_decrypt(aes_key, data)
        except:
            print_log(traceback.print_exc())
            return {}

        try:
            return json.loads(aes_data)
        except:
            return {}

    def battle_start_encrypt(self, uid, dict_data):
        """ 战斗开始前加密战斗数据

        :return:
        """
        try:
            key = '1234567890123456'  # '%skqg%s' % (uid, salt_generator())
            aes_key = crypto.rsa_private_encrypt(self.private_key, key, rsa=self.private_rsa)
            data = json.dumps(dict_data)
            aes_data = crypto.aes_encrypt(key, data)
        except:
            print_log(traceback.print_exc())
            return {}
        return {'key': aes_key, 'data': aes_data}

    def battle_end_decrypt(self, key, data):
        """ 战斗结束后解密前端数据

        :param key:
        :param data:
        :return:
        """
        try:
            key = key.replace(' ', '+')
            data = data.replace(' ', '+')
            aes_key = crypto.rsa_private_decrypt(self.private_key, key, rsa=self.private_rsa)
            print_log('BattleCrypto.battle_end_decrypt: ', aes_key, data)
            aes_data = crypto.aes_decrypt(aes_key, data)
        except:
            print_log(traceback.print_exc())
            return {}

        try:
            return json.loads(aes_data)
        except:
            return {}

    def battle_test_encrypt(self, uid, dict_data):
        """ 战斗测试加密战斗数据

        :return:
        """
        try:
            key = '1234567890123456'  # '%skqg%s' % (uid, salt_generator())
            aes_key = crypto.rsa_public_encrypt(self.public_key, key, rsa=self.public_rsa)
            data = json.dumps(dict_data)
            aes_data = crypto.aes_encrypt(key, data)
        except:
            print_log(traceback.print_exc())
            return {}
        return {'key': aes_key, 'data': aes_data}

battle_crypto = BattleCrypto()


_ARG_DEFAULT = []


def crypto_battle_start(func):

    def decorator(hm, *args, **kwargs):
        key = hm.get_argument('key', strip=False)
        data = hm.get_argument('data', strip=False)
        params = battle_crypto.battle_start_decrypt(key, data)

        real_get_argument = hm.get_argument
        real_get_mapping_argument = hm.get_mapping_argument

        def get_argument(name, default=_ARG_DEFAULT, is_int=False, strip=True):
            value = params.get(name)
            if value is None:
                return real_get_argument(name, default=default, is_int=is_int, strip=strip)
            elif is_int:
                return int(float(value))
            else:
                return value

        def get_mapping_argument(name, is_int=True, num=2, split='_'):
            value = params.get(name)
            if value is None:
                return real_get_mapping_argument(name, is_int=is_int, num=num, split=split)
            elif is_int:
                return map(int, value)
            else:
                return value

        hm.get_argument = get_argument
        hm.get_mapping_argument = get_mapping_argument

        modify_args = {
            'delete': ['key', 'data'],
            'update': params,
        }

        rc, data = func(hm, *args, **kwargs)

        encrypt_result = battle_crypto.battle_start_encrypt(hm.mm.uid, data)
        encrypt_result['modify_args'] = modify_args

        return rc, encrypt_result

    return decorator


PARAMS_TYPE = (int, int)


def crypto_battle_end(func):

    def decorator(hm, *args, **kwargs):
        key = hm.get_argument('key', strip=False)
        data = hm.get_argument('data', strip=False)
        params = battle_crypto.battle_end_decrypt(key, data)

        real_get_argument = hm.get_argument
        real_get_mapping_argument = hm.get_mapping_argument
        real_get_mapping_arguments = hm.get_mapping_arguments

        def get_argument(name, default=_ARG_DEFAULT, is_int=False, strip=True):
            value = params.get(name)
            if value is None:
                return real_get_argument(name, default=default, is_int=is_int, strip=strip)
            elif is_int:
                return int(float(value))
            else:
                return value

        def get_mapping_argument(name, is_int=True, num=2, split='_'):
            value = params.get(name)
            if value is None:
                return real_get_mapping_argument(name, is_int=is_int, num=num, split=split)
            elif is_int:
                return map(int, value)
            else:
                return value

        def get_mapping_arguments(name, params_type=PARAMS_TYPE, split='_', result_type=list):
            value = params.get(name)
            if value is None:
                return real_get_mapping_arguments(name, params_type=params_type, split=split, result_type=result_type)
            else:
                return value

        hm.get_argument = get_argument
        hm.get_mapping_argument = get_mapping_argument
        hm.get_mapping_arguments = get_mapping_arguments

        modify_args = {
            'delete': ['key', 'data'],
            'update': params,
        }

        rc, data = func(hm, *args, **kwargs)

        data['modify_args'] = modify_args

        return rc, data

    return decorator
