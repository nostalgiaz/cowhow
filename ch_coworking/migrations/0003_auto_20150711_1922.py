# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_coworking', '0002_coworking_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coworking',
            name='active',
        ),
        migrations.AddField(
            model_name='table',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
