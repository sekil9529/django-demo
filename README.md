# django-demo

Django 脚手架，settings拆分，models拆分
nginx + uwsgi(gevnet) 部署

# 环境

- Python-3.7.10
    - Django==2.2.24
    - djangorestframework==3.12.4
    - PyMySQL==1.0.2
    - django-mysql-geventpool==0.2.5
- uwsgi-2.0.19
- nginx-1.19.10

# 文件组织结构

```
.django-demo
├── app_demo                     # demo app（接口调通）   
│   ├── __init__.py
│   ├── models               
│   │   └── __init__.py
│   ├── urls.py
│   └── views.py                 # 错误码异常捕获测试

├── app_ugc                      # ugc app
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   └── ugc.py               # 用来展示跨app外键如何定义     
│   ├── urls.py
│   └── views
│       └── __init__.py

├── app_user                     # user app
│   ├── __init__.py
│   ├── models                   # 模型定义
│   │   ├── __init__.py          # 导入全部模型
│   │   └── user.py              # 用户相关模型、类型枚举类、自定义字段类型
│   ├── permissions              # 权限相关
│   │   └── __init__.py
│   ├── urls.py                  # 子路由
│   └── views                    # 视图层
│       ├── __init__.py
│       └── user.py

├── cms                          # 主目录
│   ├── __init__.py              # pymysql.install_as_MySQLdb()
│   ├── settings                 # settings.py 重构
│   │   ├── base.py              # 通用配置信息
│   │   ├── development.py       # 开发环境配置
│   │   ├── __init__.py
│   │   └── production.py        # 生产环境配置
│   ├── urls.py                  # 主路由
│   └── wsgi.py                  # wsgi文件，扩展WSGIRequest

├── core                         # 扩展的django核心库

│   ├── db                       # 数据库相关
│   │   ├── enum.py              # 枚举类
│   │   ├── functions.py         # 函数相关
│   │   ├── __init__.py
│   │   ├── models.py            # 模型字段相关
│   │   └── session.py           # 原生SQL扩展类

│   ├── drf                      # djangorestframework框架相关
│   │   ├── exception_handlers   # 异常处理
│   │   │   ├── base.py          # 异常处理基类
│   │   │   ├── error_code.py    # 错误码异常处理
│   │   │   ├── __init__.py      # 包含全部异常处理的实例列表，DRF异常处理方法定义
│   │   │   ├── method.py        # 请求方式异常处理
│   │   │   └── unknown.py       # 未知异常处理
│   │   ├── __init__.py
│   │   └── version.py           # 扩展DRF版本类

│   ├── error_code.py            # 错误码定义
│   ├── __init__.py

│   ├── middlewares              # 中间件相关
│   │   ├── base.py              # 中间件基类
│   │   ├── __init__.py
│   │   └── timer.py             # 超时记录日志

│   ├── response.py              # response相关，扩展JsonResponse

│   └── wsgi.py                  # 参考Sanic Request, 扩展WSGIRequest

├── libs                         # 通用库文件
│   ├── config.py                # 读取配置文件
│   ├── datetime.py              # 日期与unix时间戳相互转换，兼容windows
│   ├── dict.py                  # 扩展dict，实现 __setattr__、__getattr__
│   ├── enum.py                  # 枚举相关

│   ├── error_code               # 错误码相关
│   │   ├── enum.py              # 错误码枚举基类
│   │   ├── exception.py         # 错误码异常
│   │   └── __init__.py

│   ├── __init__.py
│   ├── singleton.py             # 单例
│   └── uuid.py                  # uuid生成

├── monkey_patch                 # 猴子补丁
│   ├── __init__.py              
│   └── django...operations.py   # django.db.backends.mysql.operations 猴子补丁

├── nginx_conf                   # nginx配置目录
│   ├── django-demo.conf         # nginx配置文件

├── Dockerfile                   # Dockerfile文件
├── docker-compose.yml           # docker-compose配置文件

├── uwsgi.ini                    # uwsgi配置文件

├── manage.py                    # 项目启动
...
```

# 项目特点

1. 重构settings.py，开发环境与生产环境配置剥离: `cms.settings`

2. 重构models.py，多个模型可放入不同文件，避免协同开发导致冲突增加: `app_user.models`，`app_ugc.models`

    - 使用 `models package` 代替 `models.py`
    - models.\_\_init\_\_.py：导入全部模型
    - models.xxx.py: 定义模型，外键定义统一使用模型名的的字符串形式 `"User"`，跨app外键关联啊使用app名.模型名 `"app_user.User"`

3. 大量使用 `Variable Annotations` 变量注释，提高代码可读性

4. 利用枚举类定义维护错误码： `core.error_code`

5. 扩展JsonResponse，支持自定义序列化，规范返回内容：`core.response`

6. 利用 `abc.ABCMeta` 实现抽象基类，应用与 django中间件与DRF异常处理等： `core.middlewares`，`core.drf.exception_handlers`

7. 基于 `django.db.connections` 封装原生SQL操作类：`core.db.session`

8. 扩展更多mysql字段类型，使创建表的字段类型更规范，但是仍然推荐手动建表：`core.db.models`

    - Django migrate 的缺陷
        - 无法生成表注释
        - 无法生成字段注释
        - 索引名称无法指定
        - Django内置的ORM字段类型不丰富、不严谨

9. 参考 `Sanic Request` 对 `Django WSGIRequest` 进行扩展：`core.wsgi`

    - WSGIRequest实例增加 ext命名空间，用于自定义临时变量与WSGIRequest的绑定
    - 需要在 `cms.wsgi`, `application = get_wsgi_application()` 之前导入
  
      ```python
      from core.wsgi import wsgi_handler_bind_ext_request_class

      wsgi_handler_bind_ext_request_class()
      ```

10. 使用 `django-mysql-geventpool==0.2.5` 作为mysql连接池

    - 地址：https://github.com/shunsukeaihara/django-mysql-geventpool

    - 个人配置

        ```
        # cms/settings/development.py
        INSTALLED_APPS += [
            'django_mysql_geventpool',
            ...
        ]
        
        # 自定义全局变量，为了与django配置区分开
        GEVENT_POOL = {
            'MAX_CONNS': 25,  # 最大连接数
            'MAX_LIFETIME': 60 * 60 * 2,  # 连接时间
        }
      
        DATABASES = {
            'default': {
                'ENGINE': 'django_mysql_geventpool.backends.mysql',
                # 'CONN_MAX_AGE': 60 * 60 * 2,  
                'OPTIONS': {
                    ...
                    **GEVENT_POOL
                }
            }
        }
        ```

11. 利用猴子补丁解决pymysql导致异常: `monkey_patch.django_db_backends_mysql_operations`

    - 官方推荐使用 MySQLdb模块，这里使用的是 `pymysql.install_as_MySQLdb()`，django-2.2 部分逻辑没有对 `pymysql` 模块进行兼容处理，当 `DEBUG = True` 启动会出现异常
    
        ```python
        '''异常信息：
        ...
          File "...\django-demo\lib\site-packages\django\utils\functional.py", line 80, in __get__
            res = instance.__dict__[self.name] = self.func(instance)
          File "...\django-demo\lib\site-packages\django\db\backends\mysql\features.py", line 82, in is_sql_auto_is_null_enabled
            cursor.execute('SELECT @@SQL_AUTO_IS_NULL')
          File "...\django-demo\lib\site-packages\django\db\backends\utils.py", line 103, in execute
            sql = self.db.ops.last_executed_query(self.cursor, sql, params)
          File "...\django-demo\lib\site-packages\django\db\backends\mysql\operations.py", line 146, in last_executed_query
            query = query.decode(errors='replace')
        AttributeError: 'str' object has no attribute 'decode'
        '''
        ```
      
    - 这里参照Github `django-3.1` 版本代码，利用猴子补丁替换原始 `DatabaseOperations`

# 接口说明

### 1.app_demo

- /api/v1/demos/hello/
    - hello world
- /api/v1/demos/error/test/
    - 测试错误码异常
- /api/v1/demos/error/unknown/
    - 测试未知异常
    
### 2.app_user

- /api/v1/users/
    - GET: 用户列表
    - POST: 新增用户
- /api/v1/users/{user_id}
    - GET: 单个用户信息
    - PATCH: 修改用户信息

### 3.app_ugc

- 仅展示跨app外键定义方式

# 使用与部署

### 1.安装依赖模块

```shell script
python -m pip install -r requirements.txt
```

### 2.配置 .env

```shell script
cp .env_bak .env

vim .env
[db]
user =
password =
host =
port = 3306
database =
```

# 3.初始化db

```shell script
python manage.py makemigrations
python manage.py migrate
```

### 4.uwsgi配置

- 安装uwsgi

```shell script
python -m pip install uwsgi==2.0.19
```

- 配置文件uwsgi.ini

```
[uwsgi]
# 进程
# 进程前缀
procname-prefix = djangoDemo
# 开启主进程
master = true
# 工作进程数量，建议设置为 CPU core 数                    
workers = 2
# pid文件位置，记录进程id，用于uwsgi关闭               
pidfile = .../uwsgi.pid
# 服务停止时自动移除pid
vacuum = true

# 启动
# socket
socket = 127.0.0.1:9000
# 后台启动，日志位置        
daemonize = .../uwsgi.log

# 项目位置
# 项目根目录
chdir = .../django-demo
# 指定app
module = cms.wsgi:application

# gevent配置
# 开启多线程，gevent下必须开启
enable-threads = false
# 单个进程最大协程数           
gevent = 100
# 在加载app前自动打猴子补丁，必须设置为true
gevent-early-monkey-patch = true

# 优化配置
# uWSGI instance平滑重启
reload-mercy = 10
# worker平滑重启
worker-reload-mercy = 10
# 单个工作进程最大处理请求次数，之后重新加载
max-requests = 10000
# 在每个worker中加载app而不是master，如果设置为false，master加载app，然后fork给每个worker
lazy-apps = true
# 进程运行期时不切换 CPU core                 
cpu-affinity = true
# 序列化 accept() 用法（如果可能）
thunder-lock = true
# 连接超时时间，超时断开与客户端的连接，但是服务器端仍然运行
socket-timeout = 30
# 服务器响应超时时间，超时服务器强制终止
harakiri = 30
# 输出harakiri详细信息
harakiri-verbose = true
# 关闭request日志，生产环境建议关闭（true）           
disable-logging = true
# 日志中输出内存占用情况，必须开启request日志，生产环境建议关闭（false）
memory-report = true
# 单次请求worker占用虚拟内存（单位M）上限，超过时该次结果返回后重启worker             
reload-on-as = 600
# 单次请求worker占用物理内存（单位M）上限，超过时该次结果返回后重启worker
reload-on-rss = 100
``` 

- uwsgi启动

```shell script
uwsgi --ini uwsgi.ini
```

### 5.nginx配置

- nginx配置

```
# .../nginx.conf
server {
    ...
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
    }
}
```

- nginx载入配置

```shell script
nginx -s reload
```

# docker环境部署

1. 安装配置docker

2. 安装docker-compose

3. git pull

4. 配置env文件

5. docker-compose启动项目

```shell script
docker-compose up -d
```
