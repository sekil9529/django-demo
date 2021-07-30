# coding: utf-8

from .base import *
from libs.config import Config


# 配置
CONFIG_INFO = Config(os.path.join(BASE_DIR, '.env')).format()

DEBUG = False

ALLOWED_HOSTS = ['*']

# app
INSTALLED_APPS += [
    'core.djorm_pool',
    'app_demo',
    'app_user',
    'app_ugc',
]

# 中间件
MIDDLEWARE += [
    'core.middlewares.timer.TimerMiddleware',
]

# DJORM POOL
DJORM_POOL_OPTIONS = {
    "pool_size": 20,
    "max_overflow": 0,
    "recycle": 60 * 60 * 2
}
DJORM_POOL_PESSIMISTIC = False

# 数据配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CONFIG_INFO['db']['database'],
        'HOST': CONFIG_INFO['db']['host'],
        'PORT': CONFIG_INFO['db']['port'],
        'USER': CONFIG_INFO['db']['user'],
        'PASSWORD': CONFIG_INFO['db']['password'],
        # 'CONN_MAX_AGE': 60 * 60 * 2,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': 'set session transaction_isolation = "READ-COMMITTED"'
        }
    }
}

# DRF
REST_FRAMEWORK.update({

})
