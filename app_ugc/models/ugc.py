# coding: utf-8

from django.db import models

from core.db.models import FixedCharField
from libs.uuid import make_uuid

__all__ = (
    'Ugc',
)


class Ugc(models.Model):

    class Meta:
        db_table = 't_ugc'
        verbose_name = '动态表'

    id = models.BigAutoField(primary_key=True)
    ugc_id = FixedCharField(verbose_name='用户id', max_length=32, null=False, default=make_uuid, unique=True)
    user = models.ForeignKey('app_user.User', to_field='user_id', verbose_name='用户id', null=False,
                             on_delete=models.CASCADE, db_constraint=False)
    title = models.CharField(verbose_name='标题', max_length=50, null=False, default='')
    is_deleted = models.BooleanField(verbose_name='是否已删除', null=False, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, auto_now=True)
