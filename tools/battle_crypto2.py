#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import json

import settings
from tools import xxtea


class BattleCrypto(object):
    """ 战斗验证

    """
    def __init__(self):
        pass

    def xxtea_encrypt(self, data, key=None):
        """
        用xxtea加密数据
        :param data:
        :param key:
        :return:
        """
        key = key or settings.XXTEA_SIGNATURE_KEY

        return xxtea.encrypt(data, key, returnhex=True)

    def xxtea_decrypt(self, data, key=None):
        """
        用xxtea解密数据
        :param data:
        :param key:
        :return:
        """
        key = key or settings.XXTEA_SIGNATURE_KEY

        return xxtea.decrypt(data, key, ishex=True)

    def decrypt_battle_result(self, data, key=None):
        """
        解密前端战斗数据，返回json数据
        :param data:
        :param key:
        :return:
        """
        result = self.xxtea_decrypt(data, key)
        # 处理前端的bug 去除字符串尾部的乱七八糟的数据
        # eg: {"page":"0","is_win":1,"stage_step":"1","diffculty_step":"0","chapter":"3"}\x00K
        try:
            return json.loads(result)
        except ValueError:
            suffix_pos = result.rfind('}', 0, len(result) - 1)
            real_result = result[:suffix_pos + 1]
            return json.loads(real_result)

battle_crypto = BattleCrypto()

_ARG_DEFAULT = []
PARAMS_TYPE = (int, int)


def crypto_battle_start(func):

    def decorator(hm, *args, **kwargs):
        data = hm.get_argument('data', strip=False)
        if data:
            params = battle_crypto.decrypt_battle_result(data, settings.XXTEA_SIGNATURE_KEY)
        else:
            params = {}

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
                if result_type == dict and not isinstance(value, result_type):
                    value = dict([[params_type[0](i.split('_')[0]), params_type[1](i.split('_')[1])] for i in value])
                return value

        hm.get_argument = get_argument
        hm.get_mapping_argument = get_mapping_argument
        hm.get_mapping_arguments = get_mapping_arguments

        rc, data = func(hm, *args, **kwargs)
        data['seed'] = hm.get_argument('__ts', is_int=True)

        modify_args = {
            'delete': ['data'],
            'update': params,
        }

        if settings.ENV_NAME not in settings.ENCRYPT_ENV:
            encrypt_result = data
        else:
            encrypt_result = {
                'data': battle_crypto.xxtea_encrypt(json.dumps(data), settings.XXTEA_SIGNATURE_KEY),
            }

        encrypt_result['modify_args'] = modify_args

        return rc, encrypt_result

    return decorator


def crypto_battle_end(func):

    def decorator(hm, *args, **kwargs):
        data = hm.get_argument('data', strip=False)
        if data:
            params = battle_crypto.decrypt_battle_result(data, settings.XXTEA_SIGNATURE_KEY)
        else:
            params = {}

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
            from lib.utils.debug import print_log
            if value is None:
                return real_get_mapping_arguments(name, params_type=params_type, split=split, result_type=result_type)
            else:
                if result_type == dict and not isinstance(value, result_type):
                    value = dict([[params_type[0](i.rsplit('_', 1)[0]), params_type[1](i.rsplit('_', 1)[1])] for i in value])
                return value

        hm.get_argument = get_argument
        hm.get_mapping_argument = get_mapping_argument
        hm.get_mapping_arguments = get_mapping_arguments

        rc, data = func(hm, *args, **kwargs)

        modify_args = {
            'delete': ['data'],
            'update': params,
        }

        data['modify_args'] = modify_args

        return rc, data

    return decorator
