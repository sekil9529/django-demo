# Generated by Django 2.2.24 on 2021-08-01 12:16

import core.db.models
from django.db import migrations, models
import libs.uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_id', core.db.models.FixedCharField(default=libs.uuid.make_uuid, max_length=32, unique=True, verbose_name='用户id')),
                ('user_type', core.db.models.TinyIntField(choices=[(1, '普通用户'), (2, 'VIP用户')], default=1, verbose_name='xxx类型')),
                ('name', models.CharField(default='', max_length=50, verbose_name='名称')),
                ('is_deleted', models.BooleanField(default=0, verbose_name='是否已删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户表',
                'db_table': 't_user',
            },
        ),
    ]
