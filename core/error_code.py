# coding: utf-8

from libs.enum import first_value_unique
from libs.error_code.enum import BaseECEnum


@first_value_unique
class ECEnum(BaseECEnum):
    """错误码枚举类"""
    ServerError = ('500', '服务异常，请稍后重试')

    TestError = ('TEST', '测试错误')

    # 无效版本号
    InvalidVersion = ('420', '无效的版本号')
    # 用户
    UserExist = ('1000', '已存在的用户')
