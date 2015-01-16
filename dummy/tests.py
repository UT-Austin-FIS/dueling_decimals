from django.db import DatabaseError
from django.test import TestCase

from dummy.models import Dummy


class TestDummyDecimalFields(TestCase):

    def _assertBulkCreateWorks(self, objs, batch_size=None):
        """
        Create records with bulk_create, watching for DatabaseErrors.

        If batch_size=None, Django will set batch_size=len(objs).
        """
        cls = objs[0].__class__
        try:
            cls.objects.bulk_create(objs, batch_size=batch_size)
        except DatabaseError as e:
            self.fail(
                'Bulk creation of {n} {cls} objects with '
                'batch_size={batch} raised the following '
                'exception: {exc}'.format(
                    n=len(objs), cls=cls, batch=batch_size, exc=e,
                )
            )

    def test_no_fields_set(self):
        objs = [Dummy(), Dummy()]
        self._assertBulkCreateWorks(objs)
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateWorks(objs, batch_size=n)

    def test_same_field_set(self):
        objs = [Dummy(a=u'123.45'), Dummy(a=44.42)]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateWorks(objs, batch_size=n)

    def test_both_fields_set(self):
        objs = [Dummy(a=u'123.45', b=1), Dummy(a=44.42, b=u'345345345')]
        for n in [1, 2, 3, 4, 10, 20, 50, 100, 1000]:
            self._assertBulkCreateWorks(objs, batch_size=n)

    def test_different_fields_set(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateWorks(objs)

    def test_different_fields_set_with_batch_size_1(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateWorks(objs, batch_size=1)

    def test_different_fields_set_with_batch_size_2(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateWorks(objs, batch_size=2)

    def test_different_fields_set_with_batch_size_35(self):
        objs = [Dummy(a=u'123.45'), Dummy(b=u'94324.35')]
        self._assertBulkCreateWorks(objs, batch_size=35)

    def test_one_field_set(self):
        objs = [Dummy(a=u'123.45'), Dummy()]
        self._assertBulkCreateWorks(objs)

