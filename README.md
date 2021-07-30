# django-demo

使用 nginx + uwsgi + gevent 启动的 Django 脚手架

Python-3.7.10 + Django-2.2.24 + DRF-3.12.4 + pymysql-1.0.2


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
│   │   ├── enum.py              # 枚举
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

10. 修改 `djorm-ext-pool`，为 uwsgi + gevent 环境提供数据库连接池：`core.db.djorm_pool`

    - `djorm-ext-pool` 仅支持Python-2.x，需要修改源码
      
      ```python
      def patch_mysql():
    
          class hashabledict(dict):
              def __hash__(self):
                  # return hash(tuple(sorted(self.items())))
                  return hash(frozenset(self))
      ```

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

# 3.初始化配置
python manage.py makemigrations
python manage.py migrate

### 4.uwsgi配置

- uwsgi.ini

```
[uwsgi]
# 进程
procname-prefix = djangoDemo      # 进程前缀
master = true                     # 开启主进程
workers = 2                       # 工作进程数量，建议设置为 CPU core 数
pidfile = .../uwsgi.pid           # pid文件位置，记录进程id，用于uwsgi关闭
vacuum = true                     # 服务停止时自动移除pid

# 启动
socket = 127.0.0.1:8000           # socket
daemonize = .../uwsgi.log         # 后台启动，日志位置

# 项目位置
chdir = .../django-demo           # 项目根目录
module = cms.wsgi:application     # 指定app

# gevent配置
enable-threads = true             # 开启多线程，gevent下必须开启
gevent = 100                      # 单个进程最大协程数
gevent-early-monkey-patch = true  # 在加载app前自动打猴子补丁，必须设置为true

# 配置优化
max-requests = 10000              # 单个工作进程最大处理请求次数，之后重新加载
lazy-apps = true                  # 在每个worker中加载app而不是master，如果设置为false，master加载app，然后fork给每个worker
cpu-affinity = true               # 进程运行期时不切换 CPU core
thunder-lock = true               # 序列化 accept() 用法（如果可能）
socket-timeout = 30               # 连接超时时间，超时断开与客户端的连接，但是服务器端仍然运行
harakiri = 30                     # 服务器响应超时时间，超时服务器强制终止
harakiri-verbose = true           # 输出harakiri详细信息
disable-logging = false           # 关闭request日志，生产环境建议关闭（true）
memory-report = true              # 日志中输出内存占用情况，必须开启request日志，生产环境建议关闭（false）
reload-on-as = 600                # 单次请求worker占用虚拟内存（单位M）上限，超过时该次结果返回后重启worker
reload-on-rss = 100               # 单次请求worker占用物理内存（单位M）上限，超过时该次结果返回后重启worker
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
        include .../nginx/conf/uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
    }
}
```

- nginx载入配置

```shell script
nginx -s reload
```
