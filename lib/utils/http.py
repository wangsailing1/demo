# coding: utf-8

from tornado.httpclient import HTTPClient
import urllib2


# def request(method, url, data=None, headers=None, timeout=2):
#     """一个简单的http请求封装
#     Args:
#         url: string, URL to fetch
#         method: HTTP method, e.g. "GET" or "POST"
#         headers: Additional HTTP headers to pass on the request,
#         data: HTTP body to pass on the request
#     """
#     headers = headers or {}
#     request = urllib2.Request(url, data, headers)
#     try:
#         response = urllib2.urlopen(request, timeout=timeout)
#         code, content = response.getcode(), response.read()
#     # 非200状态会抛异常，只取返回状态码和返回数据
#     except urllib2.HTTPError as e:
#         code, content = e.code, e.fp.read()
#
#     return code, content
#
#
# def get(url, headers=None, timeout=5, validate_cert=False):
#     return request('GET', url, headers=headers, timeout=timeout)
#
#
# def post(url, data=None, headers=None, timeout=5, validate_cert=False):
#     return request('POST', url, data, headers=headers, timeout=timeout)

def request(method, url, **kwargs):
    """使用tornado内置http客户端，其它具体参数请参考tornado文档
    args:
        url: string, URL to fetch
        method: HTTP method, e.g. "GET" or "POST"
        headers: Additional HTTP headers to pass on the request,
                `~tornado.httputil.HTTPHeaders` or `dict`
        body: HTTP body to pass on the request
        connect_timeout: Timeout for initial connection in seconds
        request_timeout: Timeout for entire request in seconds
        validate_cert: bool, For HTTPS requests, validate the server's
            certificate? default is True.
    """
    http = HTTPClient()
    response = http.fetch(url, method=method, **kwargs)

    return response.code, response.body


def get(url, headers=None, timeout=5, validate_cert=False, **kwargs):
    return request('GET', url, headers=headers, connect_timeout=timeout,
                   validate_cert=validate_cert, **kwargs)


def post(url, data=None, headers=None, timeout=5, validate_cert=False, **kwargs):
    return request('POST', url, body=data, headers=headers, connect_timeout=timeout,
                   validate_cert=validate_cert, **kwargs)
