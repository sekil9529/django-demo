# coding: utf-8

"""错误码枚举类"""

from enum import Enum
from types import DynamicClassAttribute


class BaseECEnum(Enum):
    """错误码基类

    定义方式：error = (code, message)
    """

    @DynamicClassAttribute
    def code(self):
        """错误码"""
        return self.value[0]

    @DynamicClassAttribute
    def message(self):
        """错误信息"""
        return self.value[1]

    @DynamicClassAttribute
    def error(self):
        """error码"""
        return self.name
