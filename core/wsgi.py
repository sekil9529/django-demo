# coding: utf-8

from types import SimpleNamespace

from django.core.handlers.wsgi import WSGIHandler, WSGIRequest


class ExtWSGIRequest(WSGIRequest):
    """扩展WSGIRequest"""

    def __init__(self, *args, **kwargs):
        super(ExtWSGIRequest, self).__init__(*args, **kwargs)
        self.ext = SimpleNamespace()  # 用于临时绑定自定义字段


def wsgi_handler_bind_ext_request_class():
    """绑定扩展request类"""
    WSGIHandler.request_class = ExtWSGIRequest
