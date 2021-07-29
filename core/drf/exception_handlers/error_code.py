# coding: utf-8
from typing import Type

from django.http import JsonResponse

from .base import BaseExcHandler
from libs.error_code.exception import ECException
from core.response import response_fail


class ErrorCodeExcHandler(BaseExcHandler):

    def get_exception(self) -> Type[Exception]:
        return ECException

    def handler(self, exception: ECException, context: dict) -> JsonResponse:
        return response_fail(enum=exception.enum)
