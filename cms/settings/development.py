# coding: utf-8

from .base import *
from libs.config import Config


# 配置
CONFIG_INFO = Config(os.path.join(BASE_DIR, '.env')).format()

DEBUG = True

ALLOWED_HOSTS = ['*']

# app
INSTALLED_APPS += [
    'rest_framework',
    'django_mysql_geventpool',
    'app_demo',
    'app_user',
    'app_ugc',
]

# 中间件
MIDDLEWARE += [
    'core.middlewares.timer.TimerMiddleware',
]

# 数据库配置
GEVENT_POOL = {
    'MAX_CONNS': 10,  # 最大连接数
    'MAX_LIFETIME': 2 * 60 * 60,  # 连接时间
}

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django_mysql_geventpool.backends.mysql',
        'NAME': CONFIG_INFO['db']['database'],
        'HOST': CONFIG_INFO['db']['host'],
        'PORT': CONFIG_INFO['db']['port'],
        'USER': CONFIG_INFO['db']['user'],
        'PASSWORD': CONFIG_INFO['db']['password'],
        # 'CONN_MAX_AGE': 60 * 60 * 2,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'isolation_level': 'read committed',
            **GEVENT_POOL
        }
    }
}

# DRF
REST_FRAMEWORK.update({

})
