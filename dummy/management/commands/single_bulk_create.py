from django.core.management.base import LabelCommand

from dummy.models import Dummy


class Command(LabelCommand):
    help = (
        'Do a single bulk_create in the Dummy table. '
        'Use the label "good" for a bulk_create that is expected to work.'
        'Use any other label for a bulk_create that is expected to fail.'
    )

    def handle(self, label, **options):
        if label == 'good':
            objs = [Dummy(a=u'1.00'), Dummy(a=u'2.00')]
        else:
            objs = [Dummy(a=u'1.00'), Dummy(b=u'2.00')]
        Dummy.objects.bulk_create(objs, batch_size=35)
