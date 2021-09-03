# coding: utf-8

from __future__ import annotations
import abc

from django.http import JsonResponse


class BaseExcHandler(metaclass=abc.ABCMeta):
    """异常处理基类"""

    __slots__ = ()

    @abc.abstractmethod
    def get_exception(self) -> type[Exception]:
        pass

    @abc.abstractmethod
    def handler(self, exception: Exception, context: dict) -> JsonResponse:
        pass
