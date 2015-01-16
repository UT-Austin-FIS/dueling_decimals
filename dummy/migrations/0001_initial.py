# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dummy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a', models.DecimalField(null=True, max_digits=15, decimal_places=2, blank=True)),
                ('b', models.DecimalField(null=True, max_digits=15, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
