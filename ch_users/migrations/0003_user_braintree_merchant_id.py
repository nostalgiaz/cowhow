# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ch_users', '0002_user_braintree_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='braintree_merchant_id',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
