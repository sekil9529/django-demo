# coding: utf-8

import os
import sys
from django.db.backends.mysql.operations import DatabaseOperations as OriginDatabaseOperations
from django.utils.encoding import force_str


class DatabaseOperations(OriginDatabaseOperations):

    def last_executed_query(self, cursor, sql, params):
        # With MySQLdb, cursor objects have an (undocumented) "_executed"
        # attribute where the exact query sent to the database is saved.
        # See MySQLdb/cursors.py in the source distribution.
        return force_str(getattr(cursor, '_executed', None), errors='replace')


def patch() -> None:
    """猴子补丁"""
    setattr(sys.modules['django.db.backends.mysql.operations'], 'DatabaseOperations', DatabaseOperations)
