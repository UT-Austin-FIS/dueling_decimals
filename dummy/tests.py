from decimal import Decimal

from django.db import DatabaseError
from django.test import TestCase

from hacks import EnableBulkCreate, USE_HACK_FOR_ORA_12704
from dummy.models import Dummy


class TestDummyDecimalFields(TestCase):

    def _assertBulkCreateBehavior(self, objs, batch_size=None, use_hack=False):
        """
        Create records with bulk_create, watching for DatabaseErrors.
        If batch_size=None, Django will set batch_size=len(objs).
        If use_hack=True, use hacks.EnableBulkCreate

        If a DatabaseError is raised, we'll make sure it wasn't expected before
        raising the alarm.
        """
        cls = objs[0].__class__
        try:
            if use_hack:
                with EnableBulkCreate():
                    cls.objects.bulk_create(objs, batch_size=batch_size)
            else:
                cls.objects.bulk_create(objs, batch_size=batch_size)
        except DatabaseError as e:
            error_is_ora_12704 = e.args[0].code == 12704
            hack_needed_but_not_used = USE_HACK_FOR_ORA_12704 and not use_hack
            if hack_needed_but_not_used and error_is_ora_12704:
                # this failure is expected; carry on
                pass
            else:
                # Fail the test if we weren't expecting to need the hack
                self.failIf((not USE_HACK_FOR_ORA_12704),
                    'Bulk creation of {n} {cls} objects with '
                    'batch_size={batch} unexpectedly raised the following '
                    'exception: {exc}'.format(
                        n=len(objs), cls=cls, batch=batch_size, exc=e,
                    )
                )
                # Fail the test if we used the hack but got ORA-12704 anyway
                self.failIf((use_hack and error_is_ora_12704),
                    'Bulk creation of {n} {cls} objects with '
                    'batch_size={batch} raised the following '
                    'exception when it should not have: {exc}'.format(
                        n=len(objs), cls=cls, batch=batch_size, exc=e,
                    )
                )
                # Fail the test if we got something other than ORA-12704
                self.failIf((not error_is_ora_12704),
                    'Bulk creation of {n} {cls} objects with '
                    'batch_size={batch} raised the following unexpected '
                    'exception: {exc}'.format(
                        n=len(objs), cls=cls, batch=batch_size, exc=e,
                    )
                )

    def test_no_fields_set(self):
        objs = [Dummy(), Dummy()]
        self._assertBulkCreateBehavior(objs)
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_same_first_field_set_unicode(self):
        objs = [Dummy(a=u'123.45'), Dummy(a=u'44.42')]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_same_first_field_set_decimal(self):
        objs = [Dummy(a=Decimal(u'123.45')), Dummy(a=Decimal(u'44.42'))]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_same_second_field_set(self):
        objs = [Dummy(b=u'123.45'), Dummy(b=u'44.42')]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_same_third_field_set(self):
        objs = [Dummy(c=u'123.45'), Dummy(c=u'44.42')]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_same_first_and_third_field_set(self):
        objs = [Dummy(a=u'2.0', c=u'123.45'), Dummy(a=u'4.0', c=u'44.42')]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_two_fields_set(self):
        objs = [Dummy(a=u'123.45', b=1), Dummy(a=u'44.42', b=u'345345345')]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_all_fields_set(self):
        objs = [
            Dummy(a=u'123.45', b=1, c=334),
            Dummy(a=u'44.42', b=u'345345345', c=0),
        ]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateBehavior(objs, batch_size=n)

    def test_different_fields_set_with_batch_size_1(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateBehavior(objs, batch_size=1)

    ### ========================
    ### Originally failing tests
    ### ========================

    def test_different_fields_set_with_batch_size_2(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateBehavior(objs, batch_size=2)

    def test_different_fields_set_with_batch_size_35(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateBehavior(objs, batch_size=35)

    def test_different_fields_set_unicode(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateBehavior(objs)

    def test_different_fields_set_decimal(self):
        objs = [Dummy(a=Decimal(u'123.45')), Dummy(b=Decimal(u'94324.35'))]
        self._assertBulkCreateBehavior(objs)

    def test_one_field_set(self):
        objs = [Dummy(a=u'123.45'), Dummy()]
        self._assertBulkCreateBehavior(objs)

    ### ===================================
    ### Originally failing tests, with hack
    ### ===================================

    def test_different_fields_set_with_batch_size_2_with_hack(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateBehavior(objs, batch_size=2, use_hack=True)

    def test_different_fields_set_with_batch_size_35_with_hack(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateBehavior(objs, batch_size=35, use_hack=True)

    def test_different_fields_set_unicode_with_hack(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateBehavior(objs, use_hack=True)

    def test_different_fields_set_decimal_with_hack(self):
        objs = [Dummy(a=Decimal(u'123.45')), Dummy(b=Decimal(u'94324.35'))]
        self._assertBulkCreateBehavior(objs, use_hack=True)

    def test_one_field_set_with_hack(self):
        objs = [Dummy(a=u'123.45'), Dummy()]
        self._assertBulkCreateBehavior(objs, use_hack=True)

