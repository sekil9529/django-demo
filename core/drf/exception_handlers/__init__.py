# coding: utf-8

from django.http import JsonResponse

from .error_code import ErrorCodeExcHandler
from .unknown import UnknownExcHandler
from core.response import response_fail


EXC_HANDLER_LIST = sorted((
    UnknownExcHandler,
    ErrorCodeExcHandler,
), key=lambda x: x().get_exception() is Exception)


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
    for exc_handler_cls in EXC_HANDLER_LIST:
        exc_handler = exc_handler_cls()
        if isinstance(exception, exc_handler.get_exception()):
            return exc_handler.handler(exception, context)
    return response_fail()
