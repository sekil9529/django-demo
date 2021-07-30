# coding: utf-8

from typing import List
from django.http import JsonResponse

from .base import BaseExcHandler
from .error_code import ErrorCodeExcHandler
from .unknown import UnknownExcHandler
from core.response import response_fail


# 异常处理实例列表
_EXC_HANDLER_LIST: List[BaseExcHandler] = sorted((
    UnknownExcHandler(),
    ErrorCodeExcHandler(),
), key=lambda x: x.get_exception() is Exception)


def handler(exception: Exception, context: dict) -> JsonResponse:
    """异常处理

    :param exception: 异常实例
    :param context:
        {
            'view': <app_user.views.demo.WrappedAPIView object at 0x000001B71B9DBB38>,
            'args': (),
            'kwargs': {},
            'request': <rest_framework.request.Request: GET '/api/user/demo/error/unknown'>
        }
    """
    for exc_handler in _EXC_HANDLER_LIST:
        if isinstance(exception, exc_handler.get_exception()):
            return exc_handler.handler(exception, context)
    return response_fail()
