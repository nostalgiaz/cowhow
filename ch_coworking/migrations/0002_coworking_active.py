# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_coworking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coworking',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
