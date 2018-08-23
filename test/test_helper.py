#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'


class FackeEnviron(object):
    """# FackeEnviron: docstring"""
    def __init__(self, api_method, params, mm):
        self.test_data = {
            'params': params,
            'method': api_method,
        }
        self.mm = mm
        # self.mm.save()

        class Req(object):
            class TT(object):
                def __init__(self):
                    self.headers = {}
                    self.remote_ip = ''

            def __init__(self):
                self.request = self.TT()

        self.req = Req()

    def get_argument(self, param_name, default=None, is_int=False, strip=True):
        """# get_argument: docstring
        args:
            param_name, default:    ---    arg
        returns:
            0    ---
        """
        value = self.test_data['params'].get(param_name, default)
        if not value:
            return 0 if is_int else ''

        return abs(int(float(value))) if is_int else value

    def get_arguments(self, param_name, default=None):
        """# get_argument: docstring
        args:
            param_name, default:    ---    arg
        returns:
            0    ---
        """
        r = self.test_data['params'].get(param_name, default)
        if isinstance(r, list):
            return r
        else:
            return [r]

    def get_mapping_argument(self, name, is_int=True, num=2, split='_'):
        """

        :param name:
        :param is_int:
        :param num:
        :param split:
        :return:
        """
        return self.get_argument(name)

    PARAMS_TYPE = (int, int)

    def get_mapping_arguments(self, name, params_type=PARAMS_TYPE, split='_', result_type=list):
        """

        :param name:
        :param params_type:
        :param split:
        :param result_type:
        :return:
        """
        return self.test_data['params'].get(name)


def get_hm(mm, params=None, api_method=''):
    """# get_hm: docstring
    args:
        mm, params=None, api_method='':    ---    arg
    returns:
        0    ---
    """
    if params is None:
        params = {}
    return FackeEnviron(
        api_method,
        params,
        mm,
    )
