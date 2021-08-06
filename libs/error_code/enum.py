# coding: utf-8

"""错误码枚举类"""

from typing import Tuple
from enum import Enum, EnumMeta
from collections import namedtuple
from types import DynamicClassAttribute

from libs.enum import keyword_value_unique

__all__ = (
    'ECData',
    'BaseECEnum',
)


"""错误码数据

code: str      # 错误码
message: str   # 错误信息
"""
ECData = namedtuple('ECData', ('code', 'message'))


class _ECEnumMeta(EnumMeta):

    def __new__(mcs, *args, **kwargs):
        enum_class = super(_ECEnumMeta, mcs).__new__(mcs, *args, **kwargs)
        # 校验code唯一
        enum_class = keyword_value_unique(('code',))(enum_class)
        enum_class._member_codes_ = tuple(enum.value.code for enum in enum_class)
        return enum_class

    @property
    def codes(cls) -> Tuple[str, ...]:
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
