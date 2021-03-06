# coding: utf-8

"""错误码枚举类"""

from __future__ import annotations

from typing import NamedTuple
from enum import Enum, EnumMeta, unique
from types import DynamicClassAttribute


__all__ = (
    'ECData',
    'BaseECEnum',
)


class ECData(NamedTuple):
    """错误码数据"""
    code: str     # 错误码
    message: str  # 错误信息

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ECData):
            raise NotImplemented
        return self.code == other.code


class _ECEnumMeta(EnumMeta):

    def __new__(mcs, *args, **kwargs):
        enum_class = super(_ECEnumMeta, mcs).__new__(mcs, *args, **kwargs)
        # 全部code
        enum_class._member_codes_ = tuple(enum.value.code for enum in enum_class)
        # code唯一
        return unique(enum_class)

    @property
    def codes(cls) -> tuple[str, ...]:
        return cls._member_codes_


class BaseECEnum(Enum, metaclass=_ECEnumMeta):
    """错误码基类

    使用示例：
    class ECEnum(BaseECEnum):
        ServerError = ECData(code="500", message="服务异常，请稍后重试")

    """

    @DynamicClassAttribute
    def code(self):
        """错误码"""
        return self.value.code

    @DynamicClassAttribute
    def message(self):
        """错误信息"""
        return self.value.message

    @DynamicClassAttribute
    def error(self):
        """error码"""
        return self.name
