# coding: utf-8

from rest_framework.request import Request
from rest_framework.decorators import api_view

from core.response import response_ok
from core.error_code import ECEnum
from libs.error_code.exception import ECException


@api_view()
def hello(request: Request):
    """hello world"""
    return response_ok('hello world!')


@api_view()
def error_unknown(request: Request):
    """未知异常"""
    raise


@api_view()
def error_test(request: Request):
    """错误码异常"""
    raise ECException(ECEnum.TestError)
