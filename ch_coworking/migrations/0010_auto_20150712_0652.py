# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_coworking', '0009_coworking_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
