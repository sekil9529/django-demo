# coding: utf-8

import logging
from typing import Type

from django.http import JsonResponse

from .base import BaseExcHandler
from core.response import response_fail

log = logging.getLogger(__name__)


class UnknownExcHandler(BaseExcHandler):

    def get_exception(self) -> Type[Exception]:
        return Exception

    def handler(self, exception: Exception, context: dict) -> JsonResponse:
        log.exception(exception)
        return response_fail()
