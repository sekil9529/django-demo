# coding: utf-8

from libs.error_code.enum import BaseECEnum, ECData


class ECEnum(BaseECEnum):
    """错误码枚举类"""
    ServerError = ECData('500', '服务异常，请稍后重试')

    TestError = ECData('TEST', '测试错误')

    # 客户端错误
    MethodNotAllowed = ECData('405', '非法的请求方式')
    InvalidVersion = ECData('420', '无效的版本号')
    # 用户
    UserExist = ECData('1000', '已存在的用户')
