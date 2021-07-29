# coding: utf-8

from django.db import models
from django.utils.translation import gettext_lazy as _


class FixedCharField(models.Field):
    """char类型"""

    description = _("Char")

    def db_type(self, connection):
        """
        限定生成数据库表的字段类型为 char，长度为 max_length 指定的值
        """
        return 'char(%s)' % self.max_length


class BinaryFixCharField(models.Field):
    """char binary 类型"""

    description = _("Char Binary")

    def db_type(self, connection):
        return 'char(%s) binary' % self.max_length


class BinaryCharFiled(models.Field):
    """varchar binary类型"""

    description = _('Varchar Binary')

    def db_type(self, connection):
        return 'varchar(%s) binary' % self.max_length


class TextField(models.TextField):
    """text类型"""

    description = _('Text')

    def db_type(self, connection):
        return 'text'


LongTextField = models.TextField


class TinyIntField(models.IntegerField):
    """tinyint类型"""

    description = _('Tiny (1 byte) integer')
    MAX_TINYINT = 127

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': -TinyIntField.MAX_TINYINT - 1,
            'max_value': TinyIntField.MAX_TINYINT,
            **kwargs,
        })

    def db_type(self, connection):
        return 'tinyint'
