# coding: utf-8

from rest_framework.request import Request
from rest_framework.decorators import api_view

from core.response import response_ok
from core.error_code import ECEnum
from libs.error_code.exception import ECException


@api_view()
def hello(request: Request):
    return response_ok('hello word!')


@api_view()
def error_unknown(request: Request):
    raise


@api_view()
def error_test(request: Request):
    raise ECException(ECEnum.TestError)
