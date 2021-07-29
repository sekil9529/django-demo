# coding: utf-8

from abc import ABC
from django.db.models import Aggregate, Func, CharField


class AnyValue(Aggregate, ABC):
    """mysql ANY_VALUE() 函数"""
    function = 'ANY_VALUE'
    name = 'AnyValue'


class IfNull(Func, ABC):
    """mysql IFNULL() 函数"""

    function = 'IFNULL'
    name = 'IfNull'

    def __init__(self, *expressions, default_value='', output_field=None, **extra):
        super(IfNull, self).__init__(*expressions, output_field=output_field, **extra)
        self.default_value = default_value

    def as_mysql(self, compiler, connection, **extra_context):
        default_value = "'%s'" % self.default_value \
            if isinstance(self.default_value, str) else self.default_value
        return super().as_sql(
            compiler, connection, default_value=default_value,
            template="%(function)s(%(expressions)s, %(default_value)s)",
            **extra_context)


class ConcatWS(Func, ABC):
    """mysql CONCAT_WS() 函数"""

    function = 'CONCAT_WS'
    name = 'ConcatWS'

    def __init__(self, *expressions, udf_fields=(), sep=';', output_field=None, **extra):
        if len(expressions) < 2:
            raise ValueError('Concat must take at least two expressions')
        paired = self._paired(expressions)
        super(ConcatWS, self).__init__(*paired, output_field=output_field, **extra)
        self.sep = sep  # 分隔符
        self.udf_fields = udf_fields  # 用户自定义字段

    def as_mysql(self, compiler, connection, **extra_context):
        # user: CONCAT_WS(';', 'ugc_type', 'title_name')
        sep = "'%s'" % self.sep
        return super().as_sql(
            compiler, connection, sep=sep,
            template="%(function)s(%(sep)s, %(expressions)s)",
            **extra_context)

    @staticmethod
    def _paired(expressions):
        # wrap pairs of expressions in successive concat functions
        # exp = [a, b, c, d]
        # -> (IfNull(a), IfNull(b), IfNull(c), IfNull(d))
        return tuple(IfNull(expression, output_field=CharField()) for expression in expressions)


class JsonExtract(Func, ABC):
    """json_field ->> 方法"""

    operator = '->>'

    def __init__(self, json_field, path, output_field=None, **extra):
        """

        :param json_field: str: 字段名称
        :param path: Union[int, str]
            int: 位置，0起始
            str: 关键字
        """
        super(JsonExtract, self).__init__(output_field=output_field, **extra)
        self.json_field = json_field
        self.path = self._path_format(path)

    def as_mysql(self, compiler, connection, **extra_context):
        # user: image_list ->> '$[0]'  # 首图
        return super().as_sql(
            compiler, connection, json_field=self.json_field,
            path=self.path, operator=self.operator,
            template="`%(json_field)s` %(operator)s %(path)s",
            **extra_context)

    @staticmethod
    def _path_format(path):
        if isinstance(path, int):  # 位置
            path = "'$[%s]'" % path
        elif isinstance(path, str):  # 关键字
            path = "'$.%s'" % path
        else:
            raise TypeError('暂不支持的 path 类型: %s' % type(path))
        return path
