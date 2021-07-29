# coding: utf-8

from django.db import models

from core.db.enum import TypeFieldEnum
from core.db.models import FixedCharField, TinyIntField
from libs.enum import first_value_unique
from libs.uuid import make_uuid

__all__ = (
    'User',
)


class User(models.Model):

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'

    @first_value_unique
    class UserTypeEnum(TypeFieldEnum):
        """用户类型枚举类"""

        NORMAL = (1, '普通用户')
        VIP = (2, 'VIP用户')

    id = models.BigAutoField(primary_key=True)
    user_id = FixedCharField(verbose_name='用户id', max_length=32, null=False, default=make_uuid, unique=True)
    user_type = TinyIntField(verbose_name='xxx类型', null=False, default=UserTypeEnum.NORMAL.val,
                             choices=UserTypeEnum.to_tuple())
    name = models.CharField(verbose_name='名称', max_length=50, null=False, default='')
    is_deleted = models.BooleanField(verbose_name='是否已删除', null=False, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, auto_now=True)
