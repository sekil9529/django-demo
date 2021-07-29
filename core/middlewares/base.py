# coding: utf-8

import abc
from typing import Callable, Optional

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from core.wsgi import ExtWSGIRequest


class BaseMiddleware(MiddlewareMixin, metaclass=abc.ABCMeta):
    """中间件基类"""

    @abc.abstractmethod
    def process_request(self, request: ExtWSGIRequest) -> None:
        """请求前"""
        pass

    @abc.abstractmethod
    def process_view(self, request: ExtWSGIRequest, view_func: Callable, view_args: tuple, view_kwargs: dict) -> None:
        """url匹配成功，视图执行前"""
        pass

    @abc.abstractmethod
    def process_exception(self, request: ExtWSGIRequest, exception: Exception) -> Optional[HttpResponse]:
        """视图执行出现异常"""
        pass

    @abc.abstractmethod
    def process_response(self, request: ExtWSGIRequest, response: HttpResponse) -> HttpResponse:
        pass
