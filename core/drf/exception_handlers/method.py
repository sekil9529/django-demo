# coding: utf-8

from __future__ import annotations

from django.http import JsonResponse
from rest_framework.exceptions import MethodNotAllowed

from .base import BaseExcHandler
from core.response import response_fail
from core.error_code import ECEnum


class MethodExcHandler(BaseExcHandler):
    """请求方式异常处理"""

    def get_exception(self) -> type[Exception]:
        return MethodNotAllowed

    def handler(self, exception: MethodNotAllowed, context: dict) -> JsonResponse:
        return response_fail(enum=ECEnum.MethodNotAllowed)
