# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_coworking', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coworking',
            name='amenities',
            field=models.ManyToManyField(to='ch_coworking.Amenity', blank=True),
        ),
    ]
