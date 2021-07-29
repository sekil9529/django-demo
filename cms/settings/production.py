# coding: utf-8

from .base import *
from libs.config import Config


# 配置
CONFIG_INFO = Config(os.path.join(BASE_DIR, '.env')).format()

DEBUG = True

ALLOWED_HOSTS = ['*']

# app
INSTALLED_APPS += [
    'corsheaders',  # 跨域
    'app_user',
    'app_ugc',
]

# 中间件
MIDDLEWARE += [

]

# 数据配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CONFIG_INFO['db']['database'],
        'HOST': CONFIG_INFO['db']['host'],
        'PORT': CONFIG_INFO['db']['port'],
        'USER': CONFIG_INFO['db']['user'],
        'PASSWORD': CONFIG_INFO['db']['password'],
        'CONN_MAX_AGE': 60 * 60 * 2,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': 'set session transaction_isolation = "READ-COMMITTED"'
        }
    }
}

