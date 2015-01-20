from django.core.management.base import BaseCommand

from dummy.models import Dummy


class Command(BaseCommand):
    def handle(self, **options):
        objs = [Dummy(a=u'1.00'), Dummy(b=u'2.00')]
        Dummy.objects.bulk_create(objs, batch_size=35)
