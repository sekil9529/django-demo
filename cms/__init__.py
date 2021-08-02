# coding: utf-8

import pymysql
from monkey_patch import django_db_backends_mysql_operations


# pymysql 猴子补丁
pymysql.install_as_MySQLdb()

# django.db.backends.mysql.operations 猴子补丁
django_db_backends_mysql_operations.patch()
