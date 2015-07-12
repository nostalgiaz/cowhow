# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_coworking', '0008_auto_20150712_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='coworking',
            name='photos',
            field=models.ManyToManyField(to='ch_coworking.CoworkingPhoto', blank=True),
        ),
    ]
