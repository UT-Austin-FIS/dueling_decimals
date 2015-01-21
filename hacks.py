from django.utils.encoding import force_bytes
import django.db.backends.oracle.base


def setup_hack_for_ora_12704_errors_on_bulk_create():
    """
    If django.db.backends.oracle.base sees that cx_Oracle is at version 5.1,
    it will attempt to convert all strings to unicode. We don't want this
    behavior, because mixing optional DecimalField instances will cause
    problems.

    This is only a problem in python 2. In python 3, cx_Oracle's STRING type is
    used for all strings.

    As far as I can tell, changing the apparent version of cx_Oracle doesn't
    affect anythin other than unicode behavior.
    """
    #import cx_Oracle
    #cx_Oracle.version = '5.0.4'
    ConvertUnicodeFaker()


class ConvertUnicodeFaker(object):
    """
    Swap out the convert_unicode function in the Oracle backend so that we
    don't get a mixture of cx_Oracle.STRING and cx_Oracle.UNICODE types being
    sent as parameters in our query. Force them all to bytes, like they used to
    be in Django 1.4.
    """

    def __init__(self):
        self._original = django.db.backends.oracle.base.convert_unicode

    def __enter__(self):
        django.db.backends.oracle.base.convert_unicode = force_bytes

    def __exit__(self, exc_type, exc_val, exc_tb):
        django.db.backends.oracle.base.convert_unicode = self._original

