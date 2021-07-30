# django-demo

使用 nginx + uwsgi + gevent 启动的 Django 脚手架

Python-3.7.10 + Django-2.2.24 + DRF-3.12.4 + mysqlclient-2.0.3 + djorm-ext-pool-0.8.2


# 项目文件组织结构

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
│   ├── __init__.py
│   ├── settings                 # settings.py 重构
│   │   ├── base.py              # 通用配置信息
│   │   ├── development.py       # 开发环境配置
│   │   ├── __init__.py          # pymysql.install_as_MySQLdb()
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

10. 使用 djorm-ext-pool 模块，为 uwsgi + gevent 环境提供数据库连接池
