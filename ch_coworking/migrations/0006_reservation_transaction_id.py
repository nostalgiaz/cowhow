# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_coworking', '0005_auto_20150711_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='transaction_id',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
