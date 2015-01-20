# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dummy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dummy',
            name='c',
            field=models.DecimalField(null=True, max_digits=15, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
