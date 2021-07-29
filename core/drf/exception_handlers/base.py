# coding: utf-8

import abc
from typing import Type

from django.http import JsonResponse


class BaseExcHandler(metaclass=abc.ABCMeta):
    """异常处理基类"""

    __slots__ = ()

    @abc.abstractmethod
    def get_exception(self) -> Type[Exception]:
        pass

    @abc.abstractmethod
    def handler(self, exception: Exception, context: dict) -> JsonResponse:
        pass
