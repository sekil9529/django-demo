# -*-coding:utf-8-*-

import warnings
from contextlib import contextmanager
try:
    from MySQLdb.cursors import DictCursor
except ImportError:
    from pymysql.cursors import DictCursor
from django.db import connections

from libs.singleton import SingletonType


class MySQLSession(metaclass=SingletonType):
    """数据库会话"""

    __slots__ = ('_default_db', '_cursor_class')

    def __init__(self):
        """

        示例：
            session = MySQLSession()
            1.仅执行
                rows = session.exec_sql(sql, params=())
            2.执行并获取单行数据
                result = session.exec_and_fetchone(sql, params=())
            3.执行并获取多行数据
                results = session.exec_and_fetchall(sql, params=())
            4.使用原生cursor对象
                with session.context_cursor() as cur:
                    rows = cur.execute(sql, params=())
                    result = cur.fetchone()
        """
        self._default_db = 'default'
        self._cursor_class = DictCursor

    def _get_conn(self, db=None):
        """获取连接对象

        :param db: Optional[str]: settings.DATABASES.key（库关键字）
        :return: conn obj
        """

        conn = connections[self._default_db if db is None else db]
        conn.ensure_connection()
        conn = conn.connection
        # conn.ping()
        return conn

    def exec_sql(self, sql, params=(), db=None):
        """执行SQL，返回行数

        :param sql: str: SQL语句
        :param params: Union[tuple, dict] = (): SQL值
        :param db: Optional[str]: 库关键字
        :return: int: 影响行数，0表示没有改变实际的行
        """
        with self._get_conn(db).cursor() as cur:
            rows = cur.execute(sql, params)
            return rows

    def exec_and_fetchone(self, sql, params=(), db=None, with_rows=False):
        """执行SQL，返回单行数据

        :param sql: str: SQL语句
        :param params: Union[tuple, dict] = (): SQL值
        :param db: Optional[str]: 库关键字
        :param with_rows: bool: 是否返回行数
        :return:
            with_rows == True:   Tuple[int, Optional[dict]]
            with_rows == False:  Optional[dict]
        """
        with self._get_conn(db).cursor(self._cursor_class) as cur:
            rows = cur.execute(sql, params)
            if rows > 1:
                warnings.warn('获取数据超出超出一行', UserWarning)
            result = cur.fetchone()
            if not result:
                result = None
            if with_rows:
                return rows, result
            return result

    def exec_and_fetchall(self, sql, params=(), db=None, with_rows=False):
        """执行SQL，返回全部数据

        :param sql: str: SQL语句
        :param params: Union[tuple, dict] = (): SQL值
        :param db: Optional[str]: 库关键字
        :param with_rows: bool: 是否返回行数
        :return:
            with_rows == True:   Tuple[int, Optional[Tuple[dict, ...]]]
            with_rows == False:  Tuple[dict, ...]
        """
        with self._get_conn(db).cursor(self._cursor_class) as cur:
            rows = cur.execute(sql, params)
            result = cur.fetchall()
            if not result:
                result = None
            elif not isinstance(result, tuple):
                result = tuple(result)
            if with_rows:
                return rows, result
            return result

    @contextmanager
    def context_cursor(self, db=None):
        """获取原生cursor对象（上下文协议）

        避免手动关闭
        :param db: Optional[str]: 库关键字
        :return: ContextManager
        """
        with self._get_conn(db).cursor(self._cursor_class) as cur:
            yield cur
