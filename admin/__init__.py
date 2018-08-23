#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import tornado

import settings
import admin_config
from decorators import require_permission
from admin_models import Admin


def render(req, template_file, **kwargs):
    """# render: docstring
    args:
        req, template_file, **kwargs:    ---    arg
    returns:
        0    ---
    """
    kwargs['url_partition'] = settings.URL_PARTITION
    kwargs['PLATFORM'] = settings.PLATFORM or settings.ENV_NAME
    kwargs['PRODUCT_NAME'] = settings.PRODUCT_NAME
    return tornado.web.RequestHandler.render(req, template_file, **kwargs)
