# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='braintree_customer_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
