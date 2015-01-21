import sys

import django

import cx_Oracle


PYTHON_2 = sys.version_info.major == 2
CX_ORACLE_5_1 = cx_Oracle.version.startswith('5.1')
DJANGO_AFTER_1_4 = django.VERSION[0:2] > (1, 4)


USE_HACK_FOR_ORA_12704 = PYTHON_2 and CX_ORACLE_5_1 and DJANGO_AFTER_1_4


class EnableBulkCreate(object):
    """
    Context manager to swap out the convert_unicode function in the Oracle
    backend so that we don't get a mixture of cx_Oracle.STRING and
    cx_Oracle.UNICODE types being bound as parameters in our generated
    bulk_create query. This raises ORA-12704 errors in the database. Force them
    all to bytes, like they used to be in Django 1.4 and cx_Oracle 5.0.4.

    If django.db.backends.oracle.base sees that cx_Oracle is at a version >=
    5.1, it will attempt to convert all strings to unicode. We don't want this
    behavior, because mixing optional DecimalField instances across instances
    in bulk_create will cause problems.

    This is only a problem in python 2. In python 3, cx_Oracle's STRING type is
    used for all strings.
    """

    if USE_HACK_FOR_ORA_12704:
        def __enter__(self):
            import django.db.backends.oracle.base
            from django.utils.encoding import force_bytes
            self._original = django.db.backends.oracle.base.convert_unicode
            django.db.backends.oracle.base.convert_unicode = force_bytes

        def __exit__(self, exc_type, exc_val, exc_traceback):
            import django.db.backends.oracle.base
            django.db.backends.oracle.base.convert_unicode = self._original
    else:
        def __enter__(self):
            pass

        def __exit__(self, *args):
            pass

